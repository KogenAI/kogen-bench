# L3b repair vs continue

Round date: HISTORICAL (before 2026-10-09)
Publication badge: VALID; NARROW / HISTORICAL; KEPT FOR AUDIT
Publication limits: Validity applies only to the eight selected failures; 193 missing Standard capture fields, incomplete raw captures, and execution-time evidence limits bound this historical result.
Recomputation status: FULLY RECOMPUTABLE


STATUS: **VALID** — registered rule met (difference 2, threshold ≥2); KEEP applies to these eight selected failures only, with per-test evidence published.

Label: VALID for the registered rule — raw captures not retained; results verified against official grades

Publication: release-included with this label under reproduce/release-rounds.json. The strict run-record gap is declared in MISSING.md.

## Reproduction metadata

- Kogen commit: not applicable to direct Codex scored cells; public task base commits are listed below.
- Harness commit: no harness Git commit is recorded; bench-codex wrapper SHA-256 08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300.
- Model and effort: direct Codex gpt-6-luna at max; Codex CLI 0.160.0.
- Task IDs: r70-2-elixir, r70-2-go, r70-4-elixir-fe2, r70-4-ts-bun-fe2, r70-5-go, r70-7-rust.
- Command: python3 rounds/l3b-repair-vs-continue/reproduce/l3b_repair_vs_continue.py
- Raw records: model transcripts and raw grader captures are not retained; sanitized official-grade rows and the three available pilot Standard 1.2 records are published with this round. Rebuild the records with `python3 reproduce/build_l3b_records.py`.

## Question

For an official Luna-max failure with its delivered patch applied, does REPAIR with the L3 self-verification instruction rescue more official full-suite failures than neutral CONTINUE, without regression versus the original failure? RESTART measures fresh performance from the original task base.

## Pre-registered design and closeout

Design SHA-256: 38acbba12ad264a058592b494cc315b89e3cadd89b65006420a39796dcb5abb3. The design file is a private operator record that is not published here, so this hash is source-reported. That it was frozen before the first scored cell is operator-reported and cannot be established from this repository alone. The selected sample is eight paired failures, with 24 planned scored cells. Three pilot cells were officially graded on 2026-10-08 before bulk release; all 24 planned scored cells now have official grades.

## Cell accounting

| Population | Count |
| --- | ---: |
| Planned scored cells | 24 |
| Identified scored starts | 24 |
| Finished cells | 24 |
| Officially graded cells | 24 |
| ITT denominator | 24 |

## Selected original failures

POOL-L3 had 12 entries. The r70-4-rust exclusion and two source-base mismatches left nine initially eligible failures. An admission amendment then excluded r70-2-elixir r31 after its no-op control passed 25/25 against an expected 24/25, leaving eight paired failures. All selected tasks are L1-admitted. No task-8 or r70-4-rust failure is selected.

| Original failure cell ID | Tests passed / total | Original source base | Failed-state base commit | Delivered patch SHA-256 | Host |
| --- | ---: | --- | --- | --- | --- |
| codex__gpt-6-luna__max__default__r70-2-elixir__r33 | 21/25 | [470ba65c1d3c](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) | bcf8ab895355cfe822b08d187373dbc6faccb36c | d1b79a381c4f526b4b4cdb0c6d3526d417245e856414653706e1c2ed721e3f89 | kogen-bench-eu |
| codex__gpt-6-luna__max__default__r70-2-go__r32 | 21/25 | [13a08875ea5e](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) | a25ca44fcd42ac0f98b47de2361517171775480a | 44995e2f56574eaa2c94c15eb76d88a06ba458d8f4b10b030f28af1bf629c1c3 | kogen-bench-us |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9 | 17/18 | [5ccd0bf1e816](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) | 123de8a8f281a2c1ae5bdd07c47a5a90383d249e | 9e6c42031d4716aadff5283855b92ac8222404b4621560decfc7661fbfcf11da | kogen-bench-eu |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10 | 17/18 | [5ccd0bf1e816](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) | a06ebe6275402f8bc55e7d84f973ecbaf22145c8 | f85028bdb5082885b678f7577f23f77cdca74b16f347d5164ef6c4327580fc09 | kogen-bench-eu |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13 | 17/18 | [5ccd0bf1e816](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) | d3c4244af14088776ea541cfca512c928847dda5 | 57c2437118828a5723b658ab7a38430127c888657b65d3762303f305ae29ead3 | kogen-bench-eu |
| codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9 | 17/18 | [cc3a831a1670](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) | d7a7c0f26f1871c900f5986653fce91aaaa33736 | eaed02b9e5c7cf04714145c224ea16687f45023112ac0fad0aae7d3cfb3272e5 | kogen-bench-us |
| codex__gpt-6-luna__max__default__r70-5-go__r32 | 23/24 | [e0b4a2478a17](https://github.com/KogenAI/kogen-ex/commit/e0b4a2478a17a924fcecb965b2941ca3396f49d6) | 54091c79f09540e6d773be15dcc54df6232a48d8 | 87b9707bc9d8728c14079e9e95872574d59513cd85d1b8720ba222a6c9483183 | kogen-bench-us |
| codex__gpt-6-luna__max__default__r70-7-rust__r31 | 23/24 | [111a0c776ae6](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) | ec773802393fe9d7cd19e493a5e749809470cb03 | a1e123612f79ae599035f01085462c6941473bf21df7593f7a82bed682119536 | kogen-bench-eu |

Excluded candidates:

- codex__gpt-6-luna__max__default__r70-4-rust__r10: explicitly excluded by design.
- codex__gpt-6-luna__max__default__r70-4-go-fe2__r820: recorded base 748ebe3a3bc03a112dab83e785159654e0709f9e is absent from the available public task snapshot.
- codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r819: recorded base 880afb00474fe33e9cf38a6d70016ddcd4e38e81 is absent from the available public task snapshot.
- codex__gpt-6-luna__max__default__r70-2-elixir__r31: admission-inadmissible after no-op passed 25/25 at the failed-state base; expected 24/25. Admission controls are outcome-independent.

## Results

Rescues: **REPAIR 3/8; CONTINUE 1/8; RESTART 2/8**. The observed difference for these eight selected failures is 2 (threshold ≥2). The public per-test pass/fail sets cover all 8 original failures and 24 scored cells. Per-test no-regression is recomputed from the public pass/fail sets: no REPAIR cell adds a failure absent from its original. **Observed KEEP for these eight selected failures**; this is not a general repair policy. The full 24-cell table and recomputed totals are in [RESULTS.md](RESULTS.md); [MEASURED.md](MEASURED.md) summarizes usage and limitations.

## Limits

- Restored to VALID 2026-10-08: the round executed its registered rule as registered and its numbers recompute; the points below are limits on public evidence, not contradictions in the round's own files.

- Only 3 of 24 scored cells have Standard records; the public outcome CSV supplies aggregates for the others.
- Both dated host captures in [ENVIRONMENT.md](ENVIRONMENT.md) were taken at 05:51Z, after contestant execution ended at 05:47Z, so execution-time conditions are not established by those captures.
- The rule's public Git commit follows the first scored start. Matching private design bytes and an earlier filesystem time do not independently establish pre-registration.
- [DEV-1](#deviation-dev-1) records concurrent admission-control grading with another round's cell. A later [hidden-suite exposure](#limit) reached a non-contestant job after contestant execution; the chronology and lack of contestant access are operator-reported. The exposed per-test names and outcomes are now published so the registered no-regression rule can be recomputed.

Private check script (operator record, not in this repository; hash source-reported): levers/lanes-2026-10-07/l3b/l3b_rule_check.py, SHA-256 17ebe3ef4a67bd09c83c8a8568505e8c3e42ea31981afc80ae7bcdc5c046d4a2.

## Configuration

- REPAIR uses the source base plus the delivered patch, original prompt, and L3 self-verification instruction verbatim.
- CONTINUE uses the same failed-state base and original prompt plus exactly: “A previous attempt is already in this repository. Continue and finish the task.”
- RESTART uses the original task base and prompt, fresh and without a prior attempt.
- Direct Codex, gpt-6-luna at max; Codex CLI 0.160.0; bench-codex wrapper SHA-256 08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300; 3,600-second cap; zero retries; same runner and sandbox.
- Rust and Elixir run on EU; Go and TS-Bun run on US. Scored cells were scheduled one at a time per host, and no two L3b scored cells overlapped on a host. See [DEV-1](#deviation-dev-1) for an L3b admission-control grading window that overlapped another round's cell.
- One random.Random(20261009) shuffle covers all cells. Host queues are stable filters of that order. Reps r9000–r9026 were checked against every grade file and both hosts’ result directories.


## Deviation DEV-1

Procedural deviation, not an exclusion. On kogen-bench-us, the official grade window for the 12 L3b US admission controls (reference and no-op controls for r70-2-go-l3b32c/r, r70-4-ts-bun-fe2-l3b9c/r and r70-5-go-l3b32c/r; no model involved) ran 03:24:53–03:30:06Z. That overlapped the last ~214 seconds of a scored cell from a different round (a Kogen tier-1 syn-31 cell, 03:00:38–03:28:27Z). Cause: an operator watcher meant to start the window after that round finished matched an earlier log word instead of an exact completion marker. Effect on L3b: the admission controls were graded on a host also running one other cell. All 12 came out as expected: references passed in full, and every no-op reproduced its original failure count. No L3b scored cell ran during the window, so the 24 scored cells are unaffected and stay in the ITT denominator. Limitation: CPU contention during those ~214 seconds can't be ruled out for the control grading itself. The interval and scope come from private operator records (operator-reported). Fix: operator watchers now trigger only on exact completion markers.

## Limit

n=8 paired failures; 24 planned cells, below the approved ceiling of 36. The pool is heterogeneous across six task/stack combinations and does not support general model ranking. Two base-mismatched entries were excluded to preserve exact starting states. The strict-validation exception was declared in [MISSING.md](MISSING.md) before the bulk release (about 04:09Z host time; operator-reported). DEV-1 was recorded in private operator records at 03:33Z, also before the bulk release, and is described publicly in the [deviation section](#deviation-dev-1) (timing operator-reported). The result does not support a causal claim beyond the registered sample and decision rule.

Hidden-suite exposure (2026-10-08): an operator documentation job that ran 05:51:38–06:22:34Z printed L3b grade rows, so 20 failed-test names from the r70-2, r70-4, r70-5 and r70-7 hidden suites reached that non-contestant job and its model provider. All 24 L3b contestant executions had finished by 05:47:42Z, before the job began. The last 14 official grades finished at 06:06:26Z, inside the job's interval. Retained timestamps don't establish whether the printing commands came before or after that grading. Grading applies each fixed patch to the hidden suite and takes no input from the job. No contestant cell or agent session had access to the names (operator-reported). Future rounds that use these suites should treat them as exposed. Details and the guard added since are in the [task-suite contamination log](../../tasks/CONTAMINATION-LOG.md#2026-10-08--failed-test-names-in-an-operator-codex-job).

## Sources and reproduction

- POOL-L3, 7 October operator pool, with public cell IDs, counts, and patch evidence.
- [L3 repair round](../l3-repair/README.md), including reused failed-state builds and verification wording.
- [Public outcome table](data/scored-cells.csv), [original failure rows](data/original-failures.csv), and [rule evidence](data/rule-evidence.json).
- [Environment record](ENVIRONMENT.md), [missing-field declaration](MISSING.md), and [decision rule](DECISION-RULE.md).

Recompute the 24-cell table, arm rescue counts, usage totals, and rule result with:

    python3 rounds/l3b-repair-vs-continue/reproduce/l3b_repair_vs_continue.py

The reproducer reads only the published aggregate CSV and boolean evidence JSON. It does not replay model execution or official grading. The source grade rows were filtered to scored reps at or above 9000 and sanitized with safe_rows.py before the public exports were written; admission-control rows were excluded.
