Follow-up from the reviewer (do these now, then redo the counts and sha if anything changed):
(a) Runner patch: remove the mandatory `/input` request predicate (the runner must check only `/model` and `/reasoning/effort`), wherever the runner itself adds it beyond the manifests.
(b) Confirm the Gherkin fake provider (`gherkin_runner` / its fake provider code) also checks only model/effort. If it still asserts instructions, tools or headers, patch it the same way.
(c) Confirm that any review/approve steps T1 inserted to capture the hash are read-only per CORE (intent approve without a hash only shows the card and has no side effects). Say where CORE states it.
(d) Rerun the dedupe after T1 + the exclusions, then recompute N, TARGET, the inputs sha and `inputs.sha`; re-run the unit tests and brief equality.
Also report `shasum -a 256 final/harness/DECISION-RULE.md`.
Final message: N_total, N, TARGET, the excluded count by reason, the inputs sha, the decision-rule sha256, unit tests, brief equality.
(e) **Locale, mandatory:** every environment the runners give to a `kogen` invocation or the warm-up must use `LANG=en_US.UTF-8` and `LC_ALL=en_US.UTF-8`. The smoke showed Elixir failing UTF-8 bytes under `C.UTF-8`. Fix: `runner.py:326-327` (now C.UTF-8), `quint_runner.py:769` and `:1881` (now `LC_ALL=C`, if they run kogen), the warm-up in `harness/score-arm.sh`, and any JSON-runner path. Helper calls to ps/lsof/git that never run kogen may stay `C`. List every env site and what you set it to.
The two runner unit tests that failed in the sandbox will be rerun by the supervisor unsandboxed. Just print the exact command to run them.
