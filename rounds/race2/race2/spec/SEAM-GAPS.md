# Black-box seam gaps

Inspection is of the read-only `core/` tree. No Rust changes are part of step 0. The required interface is the new
Test seam subsection in [CORE](CORE.md); trace operations are defined in [QUINT-SUITE](../suite/QUINT-SUITE.md).

| Gap | Evidence / implementation location | Required addition and blocked witnesses |
|---|---|---|
| G1: shared controllable wall clock | `core/crates/kogen-core/src/recovery/project.rs:39` calls its private `now_ms`; `:355` reads SystemTime directly. `core/crates/kogen-core/src/provider/auth.rs:209` validates injected expiry and `:281` defines real `now_seconds`. Further lifecycle wall reads: `core/crates/kogen-core/src/status/project.rs:331`, `core/crates/kogen-core/src/build/single_rung/execute/helpers.rs:616`, `core/crates/kogen-core/src/git/landing/persist.rs:208`. These are not CLI-injectable; the recovery tests' `reconcile_with_now` is an in-process test helper. | Implement `KOGEN_TEST_CLOCK_PATH` exactly as CORE specifies, route persisted lifecycle wall timestamps and credential/recovery wall reads through it, reread in running processes, and propagate malformed-file errors. Do not alter monotonic deadlines or OS process-start identity. Blocks generated preservation → persisted expiry → status cleanup/journal witnesses without editing implementation-private state or waiting days. |
| G2: candidate-change boundary | `core/crates/kogen-core/src/git/landing/repository.rs:259` implements candidate commit policy; `:270` snapshots the workspace and compares its tree before creating the commit. No environment/file barrier exists. | Implement armed `before-candidate-recheck` in the ordinary hooked commit path, before the snapshot comparison, with the workspace and expected base in the arrival. Blocks deterministic post-check tree mutation/crash witnesses. Internal hook-free record creation must not consume this ordinary-commit pause. |
| G3: publication and lost-CAS boundaries | `core/crates/kogen-core/src/git/landing/engine.rs:75` defines LandingPoint; `:147` installs NoLandingObserver in the normal entry point. `:316` reaches BeforeBaseCas only through the observer trait; `:318` publishes; `:332` deletes the stale incoming ref and `:343` begins replacement integration. | Expose `KOGEN_TEST_BARRIER_DIR`'s `before-publication` immediately before the branch operation and `after-cas-loss` after stale incoming deletion, before replacement integration. Adapt the existing observer where suitable. Bound waits, continue deadline/custody checks, and use the CORE arrival/release protocol. Blocks reliable lost-CAS, replacement-tip and four-turn race traces; sleeps or internal Rust observer injection do not satisfy the black-box seam. |

G1 also includes ID-token expiry: `core/crates/kogen-core/src/provider/auth/jwt.rs:59` calls the JWT library's decode
with its real-time expiry validation, before the explicit `now_seconds` check at `:83`. Make both expiry checks
clock-consistent while retaining signature/issuer/audience/nonce validation. Changing only auth.rs's clock would
leave owned-login fixtures subject to two different clocks.

G2 and G3 are one control-directory seam, not separate flags. The supervisor can implement G1 and the shared barrier
adapter independently. No fake-provider transport addition is needed.

| Existing seam | Source evidence | Exact usable scope |
|---|---|---|
| `KOGEN_PROVIDER_URL` | `core/crates/kogen-core/src/provider/http/wire.rs:48`, `:73` | Complete HTTP(S) Responses endpoint override for both auth modes; not a base-URL prefix. |
| `KOGEN_AUTH_PATH` | `core/crates/kogen-core/src/provider/auth.rs:88`, `:183`, `:209` | Re-read injected token/account JSON, require future exp; injected auth bypasses saved request credentials, not provider login. |
| `KOGEN_CREDENTIAL_STORE=file` | `core/crates/kogen-core/src/provider/auth/store.rs:227`, `:250` | Private JSON credential files instead of macOS Keychain; no extra env seam needed. |
| `KOGEN_AUTH_URL` | `core/crates/kogen-core/src/provider/auth/oauth.rs:278`, `:291`, `:395` | Local discovery allowed; issuer/JWT validation remains. Browser is launched via PATH's open/xdg-open, so a temporary runner shim suffices. Fixed callback port 1455 (`:17`) requires serial OAuth traces; no new browser flag needed. |
| `KOGEN_TIME_SCALE` | `core/crates/kogen-core/src/provider/http/client.rs:28`, `:53`; `core/crates/kogen-core/src/build/provider.rs:190`, `:588`; `core/crates/kogen-core/src/run/script.rs:74`; `core/crates/kogen-core/src/build/single_rung/landing.rs:598`; `core/crates/kogen-core/src/provider/auth/local.rs:60`; `core/crates/kogen-core/src/provider/auth/lock.rs:152` | Partial real-duration scaling, as documented in CORE. Valid suite values are strictly positive and finite; zero handling differs between paths and is outside the seam contract. |

The absolute controller deadline is unscaled at
`core/crates/kogen-core/src/build/single_rung/execute/start.rs:36`; configured check timeouts are unscaled at
`core/crates/kogen-core/src/gate/checks.rs:81`; watch sleeps for two real seconds at
`core/crates/kogen-cli/src/handlers/status.rs:55`. These are documented limits, **not required additions**: emitted
project config can select short Build/check budgets, and watch tests can use real polling. Never use TIME_SCALE
as a recovery-retention clock.

Host process-group permission failures (`core/crates/kogen-core/src/run/watchdog.rs:160`) and Linux address-space
limits require appropriate host fixtures/capabilities. The model can express them; a runner on an unsuitable host
must report missing coverage. Do not introduce a broad fault-injection API or claim a simulated probe tests the real
Unix custody behavior. Provider scripts, hook/check executables and the public seam above cover the ordinary suite.
