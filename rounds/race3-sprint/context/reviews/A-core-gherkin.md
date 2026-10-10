# Spec review A: CORE + Gherkin (Opus, read-only, frozen race3 inputs)

**Kogen spec review: race fitness** (read-only; scope `~/Scratch.noindex/race3-harness/inputs/spec/`)

**BLOCKER**

1. **The model wire protocol is undefined, but every lifecycle scenario depends on it.** FAKES.md:21 says "CORE's currently open wire-level role/tool names". QUINT-SUITE.md:228 says "OPEN wire fields are compared only where CORE fixes semantics". CORE:391 leaves "Provider mapping" OPEN. Yet the scripts are literal SSE bytes that must contain a write-file tool call (FAKES:76), an Intent payload, a questions payload and an acceptance source.
   - Example: the Go arm names its tool `write_file` and the Rust arm uses `apply_patch`. The same script bytes can only work for one of them. Nothing says what literal "maximum effort" (CORE:303) is ("max" or "xhigh"). Nothing says how the account id reaches the request (header name) or where it sits in the ID token, and research-account-shape (FAKES:61) checks it.
   - Fix: add a normative wire appendix: request JSON with literal effort values, headers, ID-token claim path, tool schemas, a Shaper output schema (intent, questions, acceptance source), and SSE event types.

2. **CORE says the product is written in Rust.** CORE:3 says "contract for the minimal Rust core". CORE:7 says "a Rust, single-binary". CORE:11 says "reuse Kogen's existing Rust lifecycle mechanisms". CORE:69 uses `<crate-version>` and "fails the build". CORE:82 says "using the existing YAML preflight". CORE:291 says "no resident daemon or VM".
   - Example: an Elixir arm breaks §1 by definition. The coverage row `1.platform` asks for "artifact/source review", so a reviewer could fail every non-Rust arm. No arm can reuse a "YAML preflight" it doesn't have.
   - Fix: make the wording language-neutral and define the YAML subset as a grammar.

3. **The status formats are under-specified, but the steps check them strictly.**
   - STEPS:48 validates the "complete CORE status JSONL schemas, key sets, types". CORE:58 gives only key names. It never says whether `queued` is a count or a list, nor gives the types of `next`, `priority`, `blocks_on`, `events` or `activity`, nor the element keys inside `recovery`.
   - STEPS:51 parses *text* `kogen status` to find an "explicitly unverified state" and a journal path. CORE requires neither in the text overview.
   - Example: two correct implementations give different `queued` types, and only one passes. The crash scenario (05:28–29) has nothing it can reliably parse.
   - Fix: publish a JSON Schema for each row type. Have the crash step read `status --json` or slug detail. Either add an `unverified` field or drop "explicitly".

**MAJOR**

4. **CORE and the fake scripts disagree on how many Builder turns happen.**
   - CORE:247 says "integration turn is one Builder repair followed by that gate rerun". CORE:176 says "may fix its own failing checks".
   - farewell-build allows "exactly two requests" (FAKES:75), and the lost-CAS (04:380) and red-check scenarios use it.
   - Example: an implementation that follows CORE literally makes a third request and fails max_requests. In the other direction, farewell-build-hook requires exactly three requests (FAKES:100), but CORE:262 never bounds how many hook-repair rounds happen.
   - Fix: state exactly when the Builder is re-invoked and how many times.

5. **The recovery-expiry test lands exactly on the boundary.** CORE:281 says "expire after `recovery_retention_days`". 05:30 advances the clock by exactly 1209600000 ms, so now equals expiry. An implementation using `now > expiry` keeps the ref and fails. Fix: specify `now_ms >= expiry_ms`, or advance the clock by 1 ms more.

6. **Features assert exit codes, statuses and output text that CORE never states.**
   - Invalid config must exit 3 (04:80, 98, 114), but CORE:87 only says "an invalid one is an error".
   - A questions-only shape must exit 0 (04:156), though 5 ("decision needed") is just as reasonable.
   - A timed-out check must give status "blocked", exit 1 and the stdout text "could-not-check" (04:327–331). CORE:208 never maps could-not-check to a status or exit code.
   - Fix: add an outcome → exit code → status → required-text table to CORE.

7. **Config bytes and YAML syntax are not fixed.** 04:33–37 requires exactly `name: project\nchecks: []\n`, but CORE:85–86 doesn't fix the serialization. The YAML that the runner writes for STEPS:20 may be rejected by an arm's "strict subset". Fix: give the literal bytes init writes, plus a grammar.

8. **What the approval hash covers is ambiguous.**
   - CORE:60 calls it the "Intent hash". CORE:166–167 says approval binds the Intent *and* the acceptance bytes.
   - CORE doesn't say whether Intent bytes come from the working tree or from the committed/approved copy.
   - Example: at 04:196–198 and 04:243–252, an implementation that hashes the committed blob, or the Intent alone, returns 0 where the feature expects 1.
   - STEPS:32 must find the Intent path in free-form shape output, but CORE:271–275 leaves the layout OPEN.
   - Fix: define the hash inputs and their source, and require a fixed `Intent: <path>` line in shape output.

9. **The lost-CAS barrier may never be reached.** CORE:252–254 publishes with `git merge --ff-only` when the branch is checked out, which is the case in this scenario. The "stale incoming ref" in CORE:249 and 341 is never defined. An implementation that treats a failed fast-forward as a moved base never reaches `after-cas-loss`, so the runner times out at 04:388. Fix: define the incoming ref and state that a failed `--ff-only` publication counts as a lost CAS.

10. **The watch command may exit without printing a final frame.** CORE:58 says "emit only changed frames, and return when the queue is stopped". 03:65 needs a "Landed" frame. An implementation that checks the exit condition before rendering exits without it. Fix: "render the final state, then return".

11. **Timing margins favour fast-starting runtimes.** At 04:338/351 a 1000 ms Build budget must cover workspace setup and both Builder requests (FAKES:93). If an arm is slow, the deadline can expire before the second request is sent, which breaks the request-count check. STEPS:49 also requires the first watch frame within 2 real seconds, including runtime boot and reconciliation, which is tight for BEAM. Fix: use budget ≥5 s, delay ≥30 s, min_requests 1, and a 5 s first frame.

12. **Process control is far easier in some languages.** CORE:187–202 requires group TERM/KILL, "Only ESRCH confirms", a Linux rlimit with a close-on-exec setup pipe, and process-start identity. That is trivial in Rust (`pre_exec`, libc). Go has no pre-exec hook. BEAM can't set process groups or read errno without a NIF or a wrapper. Fix: allow a helper executable, or mark these behaviours unscored.

13. **Notes about the old Rust code contradict the contract.**
    - CORE:61: remove happens "in one commit" vs "not implemented (planned) … deleted separately".
    - CORE:70: the help grammar vs "is rejected".
    - CORE:74: exit 130 on SIGINT.
    - CORE:109: the AGENTS.md warning "not emitted".
    - CORE:372/382: "Check discovery at init … later work" vs check detection in §4.1.
    - Fix: delete these notes and pick one behaviour each.

14. **Several adapters and config keys are left undefined.** ExUnit and Rails adapters, the location of the `format` and `acceptance.adapter` keys, which wins between `build.budget_ms` and `wall_minutes`, and the base of `run/reports/cargo-target` (CORE:128–155, 181) are all unspecified.

**MINOR**

15. **COVERAGE overclaims.** COVERAGE:151 (`5.unverified`) and the `5.dead` "unless reachable" row cite the crash scenario, which never re-approves anything and never tests reachability. `7.signing` and `7.trusted` cite the trailer scenario, which configures neither. `6.seam.scale` cites the login scenario, which sets no time scale. `3.status.args` cites the help scenario.

16. **Some steps are weak or unclear.**
    - 06:32 `"signed in"` also matches "not signed in".
    - FAKES:140 requires a revocation call on logout, but CORE:67 never says logout revokes.
    - 06:12 expects login to print the label, which CORE doesn't state.
    - STEPS:38 needs a "unique" hex string of ≥6 characters, which fails if the review card also prints a commit SHA.
    - STEPS:34 says "registered Kogen child", but the detached queue is not the runner's child.
    - STEPS:44's "first parent" is undefined for a root commit.
    - STEPS never says which working directory Kogen is run from.

17. **Stale references.**
    - `INTEGRATION.md` is missing (STEPS:60, COVERAGE).
    - CORE:348–349 links `../SEAM-GAPS.md` and `../QUINT-SUITE.md`, but those files sit next to CORE.
    - SEAM-GAPS:3 links `spec/CORE.md` and cites paths in the old Rust source tree (`core/crates/…`).
    - CORE:301–302 has a roadmap line, and CORE:62–63 repeats the queue row.
    - QUINT-SUITE:83 passes Rust and Go toolchain variables through but nothing for BEAM or Bun.

18. **Some required behaviour is never tested.** The default macOS Keychain store (CORE:321) is never exercised. The build-time version behaviour (CORE:69) cannot be tested from outside the binary.

**Verdict**
- The spec is not yet fit to decide the race. Rust is written into CORE, and an undefined model protocol plus loose status schemas mean almost every lifecycle scenario can only pass for an implementation that happens to guess the same choices.
- Fix first: findings 1, 2 and 3, then the turn-count and exit/status contradictions (4, 6, 8) and the timing margins (5, 11).
- After that, findings 9–14 decide whether the score reflects quality or noise.