# Fake provider and OpenID scripts

These names are immutable script ids used by feature steps. The runner compiles each entry to QUINT-SUITE.md's
version-1 script envelope, hashes the envelope without its digest field, routes the complete KOGEN_PROVIDER_URL to
the local Responses endpoint, and checks the exact request count. A scripted response is a valid completed Responses
event stream unless a failure is the point of the fixture. Each semantic turn is encoded as literal JSON/SSE bytes;
no fake endpoint edits the candidate, claims a check result, or changes a Git ref.

The request predicates include the model, effort, semantic role, input content and permitted tool set stated below.
Shape requests require the Shaper model and high effort; Build requests require the Builder model and maximum effort.
Injected auth fixtures use a synthetic access token with a base64url JWT payload and account_id acct-test. Its exp is
later than the test wall clock for valid auth and earlier for expired auth. They are reread for each request and are
not saved accounts.
Emit the QUINT-SUITE.md envelope with schema 1, digest, turns, min_requests, and max_requests. Each normal provider
request is a POST with JSON input, and its predicate requires the semantic model, effort, role, and inputs listed
below. A normal turn returns HTTP 200 with a valid text/event-stream Responses completion encoded as ordered literal
chunks. Tool calls are ordinary Responses tool-call outputs consumed by Kogen's dispatcher; their result appears
only in the next scripted turn. A gated chunk uses its named QUINT-SUITE ProviderGate label; a delayed chunk uses
real delay_ms. Fixture routing is to the complete local KOGEN_PROVIDER_URL ending in
/scripts/<escaped-id>/responses.
For CORE's currently open wire-level role/tool names, compare the request fields that the implementation exposes and
keep the script's semantic role and tool permission assertions in the trace manifest. Tool calls are normal responses
to Kogen's dispatcher; Kogen returns their actual results in the next provider turn. Every request is counted,
including a canceled request. A fixture response is never retried by the fake server.

## Responses scripts

### basic-farewell

- One request, minimum 1 and maximum 1; role Shaper, model gpt-6.1-sol, effort high.
- Require the input to contain the caller's exact request bytes. The feature scenarios use “Write goodbye.txt with
  Goodbye.” from either a file or stdin.
- Reply with one successful completed Responses stream. Its output is a shaped Intent for slug farewell, preserving
  the request and specifying the requirement to create goodbye.txt with the exact text Goodbye. It includes
  nonempty Acceptance and Verify criteria and selects criteria-only acceptance, with no acceptance source.
- It contains no approval, Build, or extra shaping audit. The expected caller-visible result is the Intent, its path,
  and the approve command.

### cargo-farewell

- One request, minimum 1 and maximum 1; role Shaper, model gpt-6.1-sol, effort high.
- Require root Cargo project context and the exact request bytes “Write goodbye.txt with Goodbye.”
- Reply with a valid completed Responses stream containing an Intent with nonempty Acceptance and Verify criteria
  and one Cargo integration test source at .kogen/local/acceptance/farewell.rs. The source bytes are:

  ~~~rust
  use greeter::farewell_message;
  #[test]
  fn acceptance_a1() {
      assert_eq!(farewell_message(), "Goodbye");
  }
  ~~~

- It maps acceptance id a1 to acceptance_a1. The fixture Cargo crate has no such public function at the base, so its
  sole primary compiler error is the expected unresolved import in the staged acceptance test. The fake does not
  edit the crate to make the base compile.

### research-account-shape

- One Shaper request, minimum 1 and maximum 1; model gpt-6.1-sol, effort high, caller request as in basic-farewell.
- Require the semantic account identity acct-research from the selected saved login, not injected auth and not the
  global default acct-default.
- Reply with the same successful criteria-only farewell Intent as basic-farewell. This script checks that a
  project-specific provider choice is used by the ordinary provider request path.

### farewell-questions

- One request, minimum 1 and maximum 1; Shaper model gpt-6.1-sol, effort high.
- Require a caller request about an unspecified greeting tone.
- Reply with a successful completed Responses stream containing one concise branching question and no Intent
  payload. This represents the CORE questions outcome; it must not produce an approval or acceptance source.

### farewell-build

- One Build conversation with exactly two requests: Builder model gpt-6-luna, effort max, Build role.
- The first completed response makes one ordinary dispatcher tool call that writes goodbye.txt with exactly
  Goodbye followed by LF in the private candidate workspace. The second completed response ends the Builder turn.
- No tool call writes the project config, approved Intent, acceptance package, or origin checkout. Kogen itself runs
  the configured check and owns all check evidence. The same script is used for pass, red, and timeout check fixtures;
  only the configured check fixture differs.
- The fixture does not add a repair turn after the final response. This keeps the check-result witness attributable to
  the configured check, while a separate implementation may exercise bounded self-fix in its own trace.

### farewell-build-held

- Two Builder requests, same role/model/effort and same candidate edit as farewell-build.
- The second response has a chunk gate named builder-next-turn. It emits no response bytes until ProviderGate releases
  that label. Use it to observe a live Build, request queue stop, and let the current Build finish normally.
- The gate delays only the provider response. Build and process deadlines continue to run.

### farewell-build-delayed

- Two Builder requests, same role/model/effort and candidate edit as farewell-build.
- The second successful response is delayed by 3000 real milliseconds before its response chunk. A scenario sets a
  smaller absolute build.budget_ms, so the controller's Build deadline expires first. The fake server never advances
  Kogen's test clock or monotonic clock.

### farewell-build-hook

- Three Builder requests, role Builder, model gpt-6-luna, effort max.
- The first response edits goodbye.txt exactly as farewell-build. The second completes the Builder turn. After Git
  returns the failing hook output, the third request must include that output in the Builder's context; its completed
  response makes no candidate repair. The hook still fails, so the target ref must remain unchanged.
- This script verifies the hook error reaches the repair path. It never changes the hook or bypasses Git commit.

### farewell-build-crash

- The first Builder response performs the normal goodbye.txt edit. The next response request reaches a gate named
  crash-after-edit and remains there until the runner aborts the trace-owned queue process.
- Require exactly the first request and the gated second request when both have arrived. The gated response is not
  released in the crash witness. The changed candidate is unverified and may only be preserved as recovery evidence.

### no-provider-turns

- Zero requests: min_requests 0, max_requests 0, turns is empty.
- It is paired with expired injected auth. Any HTTP request means Kogen failed to reject the credentials before making
  a provider request and fails the trace.

## OpenID fixtures

OpenID fixtures use QUINT-SUITE.md's local discovery/JWKS/token/revocation server model, not Responses scripts.
The server advertises issuer https://auth.openai.com at the overridden discovery base, returns a JWKS key that signs
the fixture ID token, checks the authorization request's state and PKCE values, and validates the callback exchange.
The temporary browser executable captures the printed authorization URL and follows the ordinary callback flow. It
must not return a fabricated success string to Kogen.

### login-default

- One owned ChatGPT login for label default and synthetic account acct-default.
- Discovery, authorization callback, token exchange, and signed ID token succeed. The access token and account id
  belong only to this trace; no real credential is used.

### login-research

- One owned ChatGPT login for label research and synthetic account acct-research.
- Same protocol checks as login-default, with a distinct account id so account isolation can be observed.

### logout-research

- One revocation exchange for acct-research succeeds. It does not revoke acct-default or alter project selection.

Every OIDC fixture binds dynamic state, nonce, PKCE verifier/challenge, authorization code, and token claims to the
ordinary flow. The fixture may not replace issuer, signature, expiry, callback, or account-id validation with a
pre-approved login result.
