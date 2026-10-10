# Black-box step vocabulary

The conformance runner launches the ordinary Kogen executable with a fresh temporary HOME and Git repository for
each scenario. It may use Git and filesystem operations to arrange fixtures and inspect outcomes; it must drive Kogen
only through its executable. It never invokes a shell for a Kogen command.

The patterns below are the complete step vocabulary. A quoted {string} is a double-quoted Gherkin string parameter;
{int} is a signed decimal integer. A trailing colon introduces a Gherkin doc string whose bytes are used exactly,
including its final newline. Paths are relative to the temporary repository unless they begin with ~/ (temporary
HOME). The reserved command tokens @repo and @home expand to their absolute fixture paths.

| Exact pattern | Parameters | Runner behavior |
|---|---|---|
| Given a temporary HOME and a Git repository on branch "{string}" | Branch name | Create an isolated trace directory, temporary HOME, unborn repository, trace-owned executable path, synthetic identity, and the fixed environment from ../QUINT-SUITE.md, including KOGEN_CREDENTIAL_STORE=file. The first such step resets any pending fixture scripts. |
| Given the repository has committed file "{string}" containing: | Relative path; exact bytes | Write the file, stage only it, and create a fixture commit on the named initial branch. |
| Given file "{string}" contains: | Relative or ~/ path; exact bytes | Atomically write exact bytes into the named fixture path without staging it. |
| Given executable file "{string}" contains: | Relative or ~/ path; exact bytes | Atomically write exact bytes and mark the file executable. |
| Given fake provider script "{string}" is configured with auth "{string}" | Script id from FAKES.md; valid, expired, malformed, or absent | Queue this immutable Responses script for the next Kogen command that makes provider requests. Route its complete KOGEN_PROVIDER_URL to the trace-local fixture server without appending a path. The script validates request count, model, effort, role, permissions, and specified input fields. For valid or expired, create KOGEN_AUTH_PATH with synthetic JWT credentials whose exp is respectively future or past relative to the test wall clock; malformed writes invalid JSON; absent unsets the variable. |
| Given fake OpenID script "{string}" is configured | OpenID fixture id from FAKES.md | Queue this local discovery/JWKS/token fixture for the next provider login. Set KOGEN_AUTH_URL and put a browser shim first on PATH; preserve normal state, nonce, PKCE, issuer, and JWT checks. Do not set injected auth. |
| Given project check "{string}" returns "{string}" within {int} milliseconds and Build budget {int} milliseconds | Check name; pass, red, or timeout; check timeout; positive Build budget | Create a small executable check fixture and a valid project config containing it and build.budget_ms. Commit that fixture config as setup. pass exits zero with complete generic evidence; red exits nonzero; timeout exceeds its configured timeout. The fixture records each invocation outside the repository. |
| Given landing barrier "{string}" is armed | One of the three CORE barrier names | Create the runner-owned KOGEN_TEST_BARRIER_DIR and its named .arm file. |
| Given Kogen's test clock starts at {int} milliseconds | Nonnegative Unix milliseconds | Create the runner-owned clock JSON and set KOGEN_TEST_CLOCK_PATH. This changes Kogen's test wall clock only; it never changes OS time or monotonic deadlines. |
| Given Kogen's time scale is "{string}" | Positive finite decimal | Set KOGEN_TIME_SCALE to this value; do not scale the absolute Build budget, check timeouts, recovery retention, status polling, or runner waits. |
| When I run "{string}" | One kogen command line | Split on ASCII whitespace with no shell, quotes, escapes, globbing, or environment expansion; then expand complete argv tokens @repo, @home, and previously captured {{name}} values to one argv element each. Invoke the configured executable directly and observe the complete result. |
| When I run "{string}" with stdin: | One kogen command line; exact stdin bytes | As above, then pass the doc string as stdin and close it. Do not copy stdin content into argv. |
| When I start "{string}" in the background as "{string}" | One kogen command line; unique handle | Start and register the trace-owned process. At launch, do not wait for or assert its exit or complete output. |
| When I wait for provider script "{string}" at gate "{string}" | Script id; gate label | Await that fake server's named request/chunk gate. Timeout is a fixture failure, not an expected Kogen result. |
| When I release provider script "{string}" at gate "{string}" | Script id; gate label | Release the named fake server gate. |
| When I wait for landing barrier "{string}" as "{string}" | Barrier point; binding name | Await the next arrival at the named CORE barrier and retain its ticket and metadata under the binding name. |
| When I release landing barrier saved as "{string}" | Previously captured binding name | Release that exact ticket through the documented barrier directory. |
| When I commit on branch "{string}" with subject "{string}" and file "{string}" containing: | Branch, subject, relative path, exact bytes | Use real Git to make a fixture commit during the scenario. Stage only the named file and use the trace's synthetic identity. |
| When I change one byte in the shaped Intent "{string}" | Intent slug | Find the single Intent file path reported by the most recent shape command, fail if it is missing or ambiguous, append one ASCII space byte, and leave acceptance files and the index untouched. |
| When I advance Kogen's test clock by {int} milliseconds | Nonnegative delta | Atomically advance the clock fixture by this amount. Never edit Kogen recovery records or alter real time. |
| When I kill the trace-owned detached Kogen queue process | None | Resolve the queue PID from this trace's status output, verify it is the registered Kogen child with the same process start identity, then send SIGKILL to that process only. |
| Then the exit code is {int} | Exact integer | Compare the most recent foreground Kogen command's exit code; signal exits use 128 plus the signal number. |
| Then stdout contains "{string}" | Literal text | Assert that the most recent command's normalized stdout contains the exact literal. |
| Then project check "{string}" ran at least {int} times | Check name; minimum count | Read the trace-local invocation counter for that generated check fixture and require at least this many executions. |
| Then stdout captures the Intent approval hash as "{string}" | Binding name | Extract the unique displayed approval hash of at least six hexadecimal characters from the most recent review card and bind it immutably. |
| Then the file "{string}" contains: | Relative or ~/ path; exact bytes | Compare the complete raw file bytes. |
| Then the file "{string}" is absent | Relative or ~/ path | Assert lstat reports no path at that location. |
| Then the file "{string}" includes text "{string}" | Relative or ~/ path; literal text | Assert the exact literal occurs in the complete raw file bytes after UTF-8 decoding. |
| Then branch "{string}" has head commit subject "{string}" | Branch; exact subject | Inspect the real branch ref and compare the head commit's subject line. |
| Then branch "{string}" has head commit with only trailer "{string}" | Branch; exact trailer text | Inspect Git-parsed trailers; require exactly the one specified trailer and a nonempty ordinary subject. |
| Then the last commit changes exactly: | One relative path per line in the doc string | Compare the exact changed-path set against HEAD and its first parent; do not stage the working index. |
| Then Git ignores path "{string}" | Relative path | Run read-only git check-ignore against the fixture repository and require the path to be ignored. |
| Then Git does not ignore path "{string}" | Relative path | Run read-only git check-ignore --no-index against the fixture repository and require no matching ignore rule, even when the path is already tracked. |
| Then there is no new commit | None | Compare the current branch ref with the ref captured immediately before the most recent Kogen command. |
| Then "{string}" JSONL output has an intent row with status "{string}" | Kogen status command; lowercase status | Run the named command through the ordinary executable and parse every stdout line as one JSON value, rejecting blank lines, non-JSON, and duplicate keys. Validate the complete CORE status JSONL schemas, key sets, types, ordering, nulls, queue positions, recovery arrays, and row categories; also require an intent row with this status. |
| Then background command "{string}" prints a frame containing "{string}" | Handle; literal text | Await the first matching text in that process's stdout while keeping the process registered and its eventual complete output available. For kogen status --watch, require the first frame within two real seconds and require the watch process to remain alive after the Building frame while work is still active. |
| Then background command "{string}" eventually exits with code {int} | Handle; exact integer | Await bounded completion and compare its complete exit and streams. A runner timeout is a suite failure. |
| Then the latest status output reports a failed or interrupted intent with preserved unverified recovery and an expiry | None | Parse the most recent status output and require the intent's status to be failed or interrupted, a preserved recovery location, an expiry time, and explicitly unverified state. Save the location and journal path for the expiry assertion. |
| Then status confirms expired recovery is removed and deletion is journaled | None | Use the previously observed recovery location and run journal; require the expired ref/archive to be absent, no longer listed as preserved, and the actual deletion event to be present in the journal. |
| Then provider account choices are under temporary HOME and absent from repository | None | Require account selection data under temporary HOME and verify no account-choice or credential path is present in the project repository. |

All command outputs use the comparison rules in ../QUINT-SUITE.md. Captured names are immutable and are expanded only
when written as {{name}} in a later command string. Unknown names, duplicate bindings, unexpected provider turns,
unconfirmed process cleanup, and missing required test-seam capabilities fail the scenario; they are not silently
skipped.

Quint tag targets and their integration renames are listed in [suite README](../README.md). Scenario names remain unchanged.
