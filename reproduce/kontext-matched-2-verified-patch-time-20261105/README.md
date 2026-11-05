# Context packet and time to a verified patch: five cases, ten pairs (screen)

**Verdict: UNRESOLVED.** Under the screen rule fixed before the first cell, Kogen Context neither shortened nor lengthened the time to an independently verified patch. All 10 matched pairs produced a verified patch in both arms, and the stack medians of the per-case time ratio were 1.02 (Zig, Crane) and 1.00 (Rust), against the 0.85 the rule needs. The cells also cannot say much about speed: 13 of the 20 arm-runs ended at the 300 s attempt cap with the fix already on disk, because the agent was still running the repository's whole test suite. Their time is the cap plus grading, not the agent's speed.

## Claim and rule

Claim under test: Kogen Context shortens the time from a real task to an independently verified patch, on Crane (Zig) and on one other stack (Rust).

- Arm A `direct`: Claude Code 2.1.318, claude-sonnet-5-5, medium effort, the issue text and a bounded failing-test output, normal tools.
- Arm B `assisted`: arm A plus the deterministic packet from `kogen-context evidence ... --deadline 1s --bytes 6500 --ranges 6`. Same model and effort in both arms. 300 s per attempt, one follow-up allowed.
- Time to verified patch T = the harness row's `total_s` (arm start to final grade: packet retrieval, every attempt, every grade) when the hidden check passes (outcome `green` or `green_after_followup`); otherwise T is censored at 1200 s. The hidden check is run by the harness, never by the agent. Timings include failed attempts and grading.
- Per case: ratio = median T(B) / median T(A) over two repetitions (the second with `--rotate 1`, which changes the arm order).
- CLEAR LOSS: two or more cases where B is red in both repetitions and A green in both; or B verified patches at least 2 below A; or median ratio >= 1.15 with B verified <= A verified. PROMISING: B verified >= A verified, no such loss case, and on Crane and on Rust separately median ratio <= 0.85 with B verified >= A verified. Otherwise UNRESOLVED.

## Result

| case | stack | verified A / B | median T A (s) | median T B (s) | ratio B/A | packet (bytes) |
|---|---|---|---|---|---|---|
| crane-xmlpe | Zig | 2 / 2 | 213.0 | 231.8 | 1.088 | 5,531 |
| crane-cssesc | Zig | 2 / 2 | 377.2 | 237.9 | 0.631 | 4,793 |
| crane-cssshape | Zig | 2 / 2 | 324.4 | 331.8 | 1.023 | 6,381 |
| bat2201 | Rust | 2 / 2 | 306.6 | 306.2 | 0.999 | 3,682 |
| bat2650 | Rust | 2 / 2 | 307.4 | 307.8 | 1.001 | 3,558 |

Stack medians of the per-case ratio: Zig 1.023 (verified 6 / 6), Rust 1.000 (verified 4 / 4); all cases 1.001. Matched pairs 10, dropped 0.

Per pair (T in seconds, A then B; "cap" = Claude hit the 300 s limit with no result event):

| pair | T A | T B | A | B |
|---|---|---|---|---|
| xmlpe r1 | 230.5 | 232.6 | finished | finished |
| xmlpe r2 | 195.5 | 231.0 | finished | finished |
| cssesc r1 | 385.8 | 106.3 | cap | finished at 30 s, no test run |
| cssesc r2 | 368.5 | 369.6 | cap | cap |
| cssshape r1 | 276.9 | 299.7 | finished | finished |
| cssshape r2 | 371.8 | 363.8 | cap | cap |
| bat2201 r1 | 307.6 | 305.8 | cap | cap |
| bat2201 r2 | 305.6 | 306.7 | cap | cap |
| bat2650 r1 | 308.4 | 308.5 | cap | cap |
| bat2650 r2 | 306.4 | 307.0 | cap | cap |

What the transcripts show (model-free):

- In every one of the 13 capped arm-runs the first edit to the fixed file was made within about 35 s, and the harness's hidden check passed on the final tree. The time then ran to the cap because the agent had started `cargo test` or `zig build test -Dspec=css` over the whole suite and that command was still running when the process was stopped. Time to verified patch therefore measures that choice plus the cap in 13 of 20 runs.
- Both arms located and edited the reference file in every Crane run (and in the Rust runs on bat2650). On bat2201 the four runs per arm edited different files (A: `app.rs` in r1 and `clap_app.rs` in r2; B: `app.rs` plus `clap_app.rs` in r1 and `app.rs` in r2), the reference changes `clap_app.rs`, and every one of those fixes passed the hidden check. No pair shows the packet changing where the agent looked in a way that changed its time.
- The only large gap is cssesc r1 (385.8 s vs 106.3 s): both arms edited the same file; B never started the long test run and stopped at 30 s, A did and hit the cap. That is variation in the agent's test habits with the same localization, so it is not a packet effect; it alone produces the 0.631 ratio.
- Uncapped pairs (xmlpe r1, r2; cssshape r1) differ by +1% to +18% (B slower) with the same edited file.
- Tokens (input + cache creation + cache read + output) exist only for the 7 arm-runs that wrote a result event: A 363.7k median on xmlpe, 594.4k on cssshape; B 343.7k and 502.6k; cssesc B r1 266.1k. They are descriptive only.
- Packets were valid and non-empty in all 10 assisted rows (bytes in the table).

## Custody

Every unit ran Claude Code 2.1.318 with `claude-sonnet-5-5` only (all 305 assistant messages and all 20 session inits report that model), the frozen binary `kogen-context` with SHA-256 `59ee239c2abf96b1737cc809063136fd3334df368ff0637a8b1e6aac7b69f747`, grader `scripts/qualify-m4.py` (SHA-256 `373c98bb32619435fe481aa7ec9db4de1e8ca7ef4d784355432811b1cf72f066`) and harness `scripts/build_bench-confirmation.py` (SHA-256 `52d805f8800476e5a17621c4fb1c5c093e2a6d71847018d155a1c0ead93211b6`). Zig 0.16.0 for the Crane cases. `scripts/report_m4.py` (SHA-256 `3529e41a54f1bf99d7d3534873382a68d1d49fcf72810f89b719e0018cfa1028`) produced `data/report.json`. The case builder used for the screen had SHA-256 `270d27ad6343bd33f5454236d6c62ea0e74cf8c3c994ee886a3a5c6a91617197`; `scripts/mk-crane-case.sh` differs from it only in taking its work directory from `$WORK`. The harness file's hash was checked on the run host after the screen; `data/custody.csv` lists the Claude, model, packet-tool and grader hashes recorded for each unit.

Excluded infrastructure runs: 7 earlier units were refused by the Claude client with a weekly usage limit in at least one arm; they are not results and are not in the data. No unit was ungraded and no unit needed an infrastructure rerun.

## Cases (public revisions)

| case | repository | base | fix | hidden check |
|---|---|---|---|---|
| crane-xmlpe | github.com/zig-whatwg/crane | [70bb3b6487ce](https://github.com/zig-whatwg/crane/commit/70bb3b6487ce3cf1277ee3c490e734516af84b6b) | [60e2f035f720](https://github.com/zig-whatwg/crane/commit/60e2f035f720c3c1f36faef673b175f9606fdc27) | `tests/xml/xm1_entity_declaration_test.zig` (5 tests) |
| crane-cssesc | github.com/zig-whatwg/crane | [c6c132d18191](https://github.com/zig-whatwg/crane/commit/c6c132d18191dc92132395e7ef38154bfa683498) | [3b3dadf622f2](https://github.com/zig-whatwg/crane/commit/3b3dadf622f2e94f8a7c6cf9b02ba8b754db5653) | `tests/css/om1_name_eql_escapes_test.zig` (8 tests) |
| crane-cssshape | github.com/zig-whatwg/crane | [c6c1522b8fd1](https://github.com/zig-whatwg/crane/commit/c6c1522b8fd143367c971fc01ca49dcd5d7276f2) | [5b0343a8df53](https://github.com/zig-whatwg/crane/commit/5b0343a8df53414d99432104f4a701b9c5bf3793) | `tests/css/ci1_shape_scalar_extended_units_test.zig` (1 test) |
| bat2201 | SWE-bench Multilingual `sharkdp__bat-2201` (sharkdp/bat) | instance base commit | instance patch | the instance's target test |
| bat2650 | SWE-bench Multilingual `sharkdp__bat-2650` (sharkdp/bat) | instance base commit | instance patch | the instance's target test |

The base of each Crane case is the parent of its fix commit. The hidden check is the fix's own new test file, run with `zig build test -Dspec=<dir> -Dtest-file=<file> --summary all`; it calls only functions already present on the base, so it checks behaviour, not guessed names. Selection rule: among fix commits since 2026-09-19, a fix whose tests are a separate new file calling only APIs present on the base, buildable without V8. `briefs/` holds the symptom-only issue texts for the three Crane cases (written by us from the public commit and its tests after seeing the fix; they name no file, function or module). Bat cases use the SWE-bench issue text. Case kits and patches are not shipped.

The published `scripts/qualify-m4.py` and `scripts/mk-crane-case.sh` name the fix's source diff `fix.patch`; the run used the same code with that file named differently, which is the only change. The executed `qualify-m4.py` had SHA-256 `373c98bb32619435fe481aa7ec9db4de1e8ca7ef4d784355432811b1cf72f06` (the custody hash above); the published copy has `4ca70efb6c2485bf02a254f4490afc4500c48fe2dca6b8c453c0d135aed5b6e5`. The diff comes from the public Crane fix commit named in the table.

## Rerun

1. Tools: Zig 0.16.0 from ziglang.org; Claude Code 2.1.318 (`npm i -g @anthropic-ai/claude-code@2.1.318`) logged in, or `ANTHROPIC_API_KEY` set in the environment; Rust stable with cargo; Python 3. The packet tool is the public source at github.com/KogenAI/kogen-context (it has no release tag; build the `evidence` subcommand version and compare `shasum -a 256` of the binary with the hash above).
2. Crane cases: `git clone --bare https://github.com/zig-whatwg/crane $WORK/crane.git`, then for each row of the table: `WORK=$WORK bash scripts/mk-crane-case.sh <case> <fix sha> <test file>`. This writes `$WORK/kit/cases/<case>/{base,test.patch,fix.patch,origin}`; add the brief from `briefs/<case>.txt`. Bat cases: take `sharkdp__bat-2201` and `sharkdp__bat-2650` from the SWE-bench Multilingual dataset (base commit, test patch, instance patch).
3. Red/green controls: `python3 -I scripts/qualify-m4.py <case> base --out <dir>` must be red and `... ref --out <dir>` green before any model run.
4. Screen, per case and repetition (rep 2 adds `--rotate 1`):
   `python3 -I scripts/build_bench-confirmation.py --cases <case> --context <kogen-context binary> --context-sha256 59ee239c2abf96b1737cc809063136fd3334df368ff0637a8b1e6aac7b69f747 --qualify scripts/qualify-m4.py --zig-dir <zig 0.16.0 dir> --summary-name result.json --diag-name diagnostic.txt --red <case>=<red receipt dir> --green <case>=<green receipt dir> --out <runs>/kxm4-screen-<case>-r<rep>`
   (`--preflight` checks packets without a model.) Use shared Zig caches for both arms and the grader so neither pays a cold build.
5. Report: copy each `summary.json` into one directory per unit named `kxm4-screen-<case>-r<rep>/` and run `python3 -I scripts/report_m4.py <that directory> --out report.json`. To check this pack without any model, rebuild the layout from `data/units/<case>-r<rep>.json` (they are the harness summaries with host paths removed) and run the same report; its verdict line is `UNRESOLVED`.

## Files

- `data/units/*.json`: harness rows per unit (host paths and account names removed). `data/rows.csv`: one line per arm-run. `data/custody.csv`: versions and hashes per unit. `data/per_case.csv`: the case table. `data/report.json`: the report.
- `scripts/`: our harness, grader, case builder and report script.
- `briefs/`: Crane issue texts.

## Limits

Screen only: two repetitions on five cases, one model, one effort. No general speed claim. The 300 s cap and the agent's habit of running the whole test suite dominate most times, so a rerun with a different cap or a test-scoped instruction could give different times. Matched-1 (five cases, every row green in both arms) and the earlier pre-screen are separate and are not pooled here.
