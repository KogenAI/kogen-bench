# kogen-mini localhost protocol, version 1

This is the shared CLI/core and worker/coordinator protocol for both ARCH arms. SPEC.md defines command behaviour, persistence, timing, Git semantics, and JOB_RECORD. There are no HTTP, WebSocket, notification, or binary messages.

## 1. Transport, envelope, and validation

TCP is IPv4 localhost at the coordinator's `--port`. Each request and response is one UTF-8 JSON object followed by LF (`\n`); accept CRLF as well. JSON strings escape embedded newlines. Maximum line size is 8,388,608 bytes excluding the delimiter, on both directions. A line exceeding that size yields `LINE_TOO_LARGE` if a response can be written, then closes the connection. Invalid UTF-8/JSON, a non-object root, or duplicate JSON object keys yields `BAD_JSON`. Blank lines are invalid. EOF before a delimiter discards that incomplete request without acceptance or response. Malformed but complete lines get an error and the connection remains usable unless size is exceeded.

A connection can send repeated requests; process them and emit responses in arrival order, one response per request. There is no unsolicited output. A pending wait blocks that connection's subsequent requests; use another connection for cancellation/heartbeats. Workers use a separate heartbeat connection when a result is being processed. Requests need not use a persistent connection. No authentication is provided: this is an isolated local experiment with trusted workers.

Every valid request has `{"v":1,"request_id":STRING,"type":TYPE,...}`. `request_id` is 1–64 ASCII letters/digits/`._-`, solely for response correlation; it is not a deduplication key. Every success response is `{"v":1,"request_id":STRING,"ok":true,"result":OBJECT}`. Every error response is `{"v":1,"request_id":STRING_OR_NULL,"ok":false,"error":{"code":CODE,"message":TEXT}}`. Use null request ID when a trustworthy syntactically valid ID cannot be extracted. Missing/unsupported `v` gives `UNSUPPORTED_VERSION`; missing/invalid type, ID, required fields, or extra fields gives `INVALID_REQUEST`; an unknown string type gives `UNKNOWN_TYPE`. Only fields explicitly defined for a message are allowed. Field validation has no side effects. Error text is explanatory but not stable.

Integers, booleans, nulls, paths, IDs, object IDs, job inputs, and record fields follow SPEC.md. Session and lease tokens are opaque strings of 64 lowercase hexadecimal characters. No client derives ordering or time from them. A malformed token is `INVALID_REQUEST`, an unknown/obsolete well-formed session is `STALE_SESSION`, and a wrong/expired well-formed lease is `STALE_LEASE`. A worker session binds ID and canonical work path; supplied workspace paths must equal that session's `WORK/jobs/ID/attempt-N/checkout` for the named job/attempt. All mutation success responses follow the durability point in SPEC.md. Transport loss never reverses a committed request.

## 2. Client messages

### `submit`

Request: envelope plus `job`, the complete six-field input object. Validate and normalize before checking idempotent identity; for an already accepted ID the stored normalized input governs replay even if its repository/base is no longer readable. Check replay by field equality after lexical path normalization/canonicalization against the saved repo identity, not by revalidating old Git objects. A genuinely new submission validates repository/base fully.

Result: `{"id":ID,"seq":N,"duplicate":BOOL}`. A new acceptance is durable before response, `duplicate:false`. An identical replay returns `true`, does not allocate a sequence, and never reruns a terminal job. Conflicting input is `ID_CONFLICT`; invalid input is `INVALID_JOB`.

Example request:
```json
{"v":1,"request_id":"s1","type":"submit","job":{"id":"j1","repo":"/tmp/arch-target.git","base":"1111111111111111111111111111111111111111","patch":"diff --git a/a.txt b/a.txt\n...\n","build_cmd":"test -f a.txt","timeout_s":10}}
```
This illustrates encoding; the abbreviated patch and example object ID are not executable fixtures.

### `status`

Request: envelope only. Result: `{"version":1,"jobs":[JOB_RECORD,...]}`, including terminal jobs, sorted by `seq`; no worker/process inventory. Empty queue yields an empty array.

### `wait`

Request: envelope plus `id` and `timeout_s` (integer 0–3600). This timeout is the caller's wait budget and need not equal the job's command budget. Result: `{"job":JOB_RECORD,"timed_out":BOOL}`. A terminal job returns immediately with false. At deadline, reread a linearizable record: if terminal return false; otherwise return true and that nonterminal record. Deadline zero performs this check immediately. `NOT_FOUND` returns immediately for unknown ID. A disconnected waiter has no effect on the job. The timeout starts when the complete valid request is dispatched; response observation may incur scheduling/polling delay up to 250 ms plus local transport time.

### `cancel`

Request: envelope plus `id`. Result: `{"job":JOB_RECORD,"cancel_requested":BOOL}`. Queued jobs return cancelled/true; leased jobs normally return cancelling/true without waiting for cleanup; repeated cancelling/cancelled returns true. Other terminal jobs return false. If an intent is prepared, reconcile it before returning the terminal job with false. Unknown ID is `NOT_FOUND`. The response acknowledges durable cancellation intent, not necessarily completed descendant cleanup; use wait/status for completion.

## 3. Worker messages

Each worker first registers, then polls and heartbeats. A session must heartbeat at least once per second even when idle; idle session expiry is eight seconds from its last acknowledgement. Coordinator restart invalidates all sessions without resetting persisted job deadlines. After `STALE_SESSION`, a worker kills/reaps its old attempt, discards that lease, then re-registers. After `STALE_LEASE`, it kills/reaps the stale attempt and polls; it may not send a new result for that token except replaying an already saved receipt. A worker must not execute an assignment obtained after its own local hard deadline without a successful timely renewal.

### `worker_register`

Request: envelope plus `worker_id`, `work` (absolute directory path, already created and exclusively locked by the worker). Result: `{"session":TOKEN,"heartbeat_interval_ms":1000,"lease_duration_ms":8000}`. Canonicalize `work`. An existing live session with the same worker ID or work path gives `WORKER_CONFLICT`. Re-registration after expiry or coordinator restart creates a distinct session. It cannot revive an old attempt or steal its protected landing intent. Registration does not imply a job assignment.

### `worker_poll`

Request: envelope plus `session`. Result: `{"assignment":ASSIGNMENT_OR_NULL,"action":ACTION}`. ACTION is `idle`, `run`, `hold`, or `cancel`:

* `idle`: no leased job and no grantable queue entry; assignment is null.
* `run`: a new build grant or the one-time transition of an owned ready job into landing.
* `hold`: an already delivered running/ready/landing assignment; the worker continues its existing operation or waits for the lane, and must not start another copy of the command.
* `cancel`: the owned job is cancelling; assignment describes the existing lease for cleanup only.

Every non-null assignment contains exactly:
```json
{"id":"j1","attempt":1,"lease_token":"TOKEN","lease_expires_at_ms":0,"phase":"build","job":{"id":"j1","repo":"/tmp/arch-target.git","base":"OID","patch":"PATCH","build_cmd":"COMMAND","timeout_s":10},"target_ref":"refs/heads/main","expected_head":null}
```
Placeholders above represent values with the specified types. `phase` is `build` for running or ready (ready means hold after build result), `landing` for landing, and the last phase for cancelling. `expected_head` is null for build and the captured full ID for landing. `target_ref` is always the captured branch. A lease token stays unchanged across build/ready/landing; a retry gets a new token and increased attempt. Poll does not renew an existing lease; use heartbeat. Replayed/lost poll responses return hold with the same assignment until a result changes its state. A worker that has not started its locally recorded assignment may start it upon hold once; it keys execution by `(session,id,attempt,phase)`.

A free worker receives the lowest-sequence queued job. A ready owner receives landing run only when its per-repo FIFO predecessors are terminal. The coordinator stores that transition and expected head before replying. Only that owner can run the landing rerun. There is no assignment push.

### `worker_heartbeat`

Request: envelope plus `session`, `id`, `attempt`, `lease_token`. These last three fields must all be null for an idle heartbeat, or all be non-null (valid ID, positive integer, token) for an owned attempt. Result: `{"lease_expires_at_ms":INTEGER_OR_NULL,"action":"continue"|"cancel"}`. An idle heartbeat renews only the session and returns null/continue. An active heartbeat renews session and the unexpired job lease by eight seconds from acknowledgement's durable decision point. Cancellation action forbids new work and orders cleanup; it may renew the session but **must not extend the cancelling job's hard deadline**. Prepared intents are protected from expiry; return their existing deadline without extending cancelled command execution. An idle heartbeat while owning an attempt, or a mismatched owner/attempt/token, is `STALE_LEASE`. Success never revives an expired attempt.

### `worker_result`

Request: envelope plus `session`, `id`, `attempt`, `lease_token`, `phase`, `outcome`, `reason`, `workspace`, `commit`.

`phase` is `build`, `landing`, or `cleanup`; `outcome` is `ok`, `failed`, `timed_out`, or `cancelled`. Every field is present. `reason`, `workspace`, `commit` use null where indicated:

| Phase/outcome | Required values and effect |
| --- | --- |
| build/ok | reason null, workspace exact owned checkout path, commit full private patch commit ID; running -> ready. |
| build/failed | reason `clone_failed`, `patch_failed`, or `build_failed`; workspace and commit null; running -> failed after full-tree cleanup. |
| build/timed_out | reason `build_timeout`; workspace and commit null; running -> timed_out after cleanup. |
| landing/ok | reason null, workspace owned path, commit rebased candidate ID; landing -> durable intent -> compare-and-swap -> landed. |
| landing/failed | reason `rebase_failed`, `landing_build_failed`, or `target_changed`; workspace and commit null; landing -> rejected after cleanup. |
| landing/timed_out | reason `landing_timeout`; workspace and commit null; landing -> rejected after cleanup (an unsuccessful rerun). |
| cleanup/cancelled | reason `user_cancelled`; workspace and commit null; cancelling -> cancelled after full-tree death. |

Other combinations are `INVALID_REQUEST`. Result is `{"job":JOB_RECORD,"duplicate":BOOL}`. Persist an exact request-body receipt (excluding envelope/correlation ID) with its successful mutation. An identical retransmission from the same saved session/token returns the current job and duplicate true even after session/lease expiry or restart, without another transition or Git update. No saved receipt means fencing is enforced normally. A different result for an already consumed `(lease_token,phase)` is `RESULT_CONFLICT`. Receipts do not bypass field validation. Build and landing have separate receipts for the same lease.

Results in the wrong state with a still current lease are `INVALID_STATE`; a stale assignment is `STALE_LEASE`. If cancellation won before intent preparation, discard a crossing build/landing result, return `CANCEL_PENDING`, and require cleanup/cancelled; do not accept a success receipt. For a landing proposal, coordinator verifies the candidate exists in the supplied checkout, has exactly expected_head as its one parent, and has the expected job subject. Invalid artifacts give `INVALID_ARTIFACT` without mutating the target; the worker must report a landing failure or clean up. Worker claims about command success/tree death are trusted but externally tested. Only the coordinator performs Git target updates, including after a worker goes away.

### `worker_shutdown`

Request: envelope plus `session`, `id`, `attempt`, `lease_token` with the same idle/active null rule as heartbeat. The worker sends this **after** terminating and reaping all attempt descendants. Result: `{"released":BOOL,"job":JOB_RECORD_OR_NULL}`. Idle shutdown yields false/null and retires the session. Active unprepared shutdown yields true and the requeued job (or cancelled job if cancellation pending), and retires the session. Protected intent is completed first; return false and its terminal job. Preserve all acceptance data and attempts. A lost shutdown response can be retried on the same running coordinator while its retired-session receipt is retained; reply the same result. This receipt is retained until coordinator restart; after restart a shutdown replay may return `STALE_SESSION`, and the already released job must still remain durable. Mismatched owner/token gives `STALE_LEASE`; unknown session gives `STALE_SESSION`. Work directory exclusivity remains until worker exit.

## 4. Complete error catalogue

| Code | Trigger | Client CLI exit when applicable |
| --- | --- | --- |
| `BAD_JSON` | Invalid UTF-8/JSON/object/duplicate keys. | 3 |
| `LINE_TOO_LARGE` | Framing limit exceeded; close connection. | 3 |
| `UNSUPPORTED_VERSION` | Missing or non-1 protocol version. | 3 |
| `UNKNOWN_TYPE` | Unknown string message type. | 3 |
| `INVALID_REQUEST` | Envelope, fields, type/range, combination, or unknown field invalid. | 2 |
| `INVALID_JOB` | Job input/repository/base validation fails. | 2 |
| `ID_CONFLICT` | Same accepted ID, different normalized input. | 2 |
| `NOT_FOUND` | Unknown ID on wait/cancel. | 2 |
| `WORKER_CONFLICT` | Duplicate live worker ID/work registration. | 2 |
| `STALE_SESSION` | Expired/unknown/restarted worker session. | 3 |
| `STALE_LEASE` | Expired/fenced/wrong attempt or idle/active ownership mismatch. | 3 |
| `INVALID_STATE` | Current owner reports a result impossible in its state. | 3 |
| `RESULT_CONFLICT` | Different result body for consumed phase receipt. | 3 |
| `CANCEL_PENDING` | Cancellation won; worker must perform cleanup. | 3 |
| `INVALID_ARTIFACT` | Missing/wrong-path/wrong-parent/wrong-subject candidate. | 3 |
| `REPO_CHANGED` | Prepared intent cannot reconcile against current target. | 3 |
| `DATA_CORRUPT` | Durable snapshot cannot be validated/recovered safely. | 3 |
| `INTERNAL` | Other storage/Git/internal failure; no false success. | 3 |

No remote error is a terminal job outcome unless the state machine explicitly records it. Storage failure must not acknowledge a mutation; retries and restart resolve any already durable intent. Startup corruption may be reported solely as the CLI stderr error since the coordinator must not advertise readiness. Protocol errors that leave the connection open do not cancel an existing lease. Large outgoing records that cannot fit the limit return `INTERNAL` rather than truncated JSON; fixtures keep status snapshots below the limit.

## 5. Canonical client success example

```json
{"v":1,"request_id":"s1","ok":true,"result":{"id":"j1","seq":1,"duplicate":false}}
{"v":1,"request_id":"q1","ok":true,"result":{"version":1,"jobs":[{"id":"j1","repo":"/tmp/arch-target.git","seq":1,"state":"queued","attempt":0,"worker_id":null,"lease_expires_at_ms":null,"accepted_at_ms":1,"updated_at_ms":1,"landed_commit":null,"reason":null}]}}
{"v":1,"request_id":"w1","ok":true,"result":{"job":{"id":"j1","repo":"/tmp/arch-target.git","seq":1,"state":"landed","attempt":1,"worker_id":null,"lease_expires_at_ms":null,"accepted_at_ms":1,"updated_at_ms":2,"landed_commit":"2222222222222222222222222222222222222222","reason":null},"timed_out":false}}
```
