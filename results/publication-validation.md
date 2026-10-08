# Publication validation

This report distinguishes archive consistency checks from release eligibility. The repository validator checks archive consistency; the publication release validator also requires every evidence gate resolved and every required scored round either strict-release-eligible or explicitly included with a verified descriptive label.

## Public grade-export scope

**B1 is resolved.** The refreshed public `grades.final.jsonl` export exact-joins **5,020/5,020** unique captured graded IDs using `source_record_id == public_cell_id == grades.final.jsonl cell_id`. The 2026-10-07 refresh appended the 128 authoritative official rows missing from the prior snapshot; the exact join now has zero capture-reported-only mappings. See [results/GRADE-JOIN.md](GRADE-JOIN.md) for the builder output and per-round counts.

Historical “official rows before” counts in the table below refer to the pre-refresh snapshot at benchmark commit `58c9ca5ee40fb958c61c61e381191a922886f88f`, committed `2026-10-07T16:18:30+03:00` (export SHA-256 `cbf85effb6334c650fa0204da6e2777ed8a5a699f14ab854529d998b5177703a`). The refreshed export SHA-256 is `4d639a3848b3661dcb5646630b6a4914e5053ff4b94ab029424d47d040e3c977`.

The 128 additions contain **84 model PASS, 19 model FAIL, and 25 invalid `control_apply` rows**. The controls carry `result=invalid` and `outcome=fail`; they are invalid controls, not model failures. The refreshed cells export preserves them as invalid and keeps their ITT treatment under the existing control policy.

The before/after tables classify rows by source `kind` and `result`. The previous `cells.*` export displayed the two pre-existing invalid controls in these target rounds as `outcome=fail`; the refreshed export now displays their official `result=invalid` classification. This classification is applied to all 199 `control_apply` rows in the refreshed input, including the 25 additions.

| Round | Official rows before (snapshot 58c9ca5, 2026-10-07T16:18:30+03:00) | Added | Official rows after | Added model PASS / FAIL | Added invalid controls |
|---|---:|---:|---:|---:|---:|
| r69 | 95 | 55 | 150 | 46 / 9 | 0 |
| r67b | 1 | 42 | 43 | 17 / 8 | 17 |
| r71 | 18 | 31 | 49 | 21 / 2 | 8 |
| **Total** | **4,892** | **128** | **5,020** | **84 / 19** | **25** |

The round verdicts remain INTERIM. r69's registered rule requires 400 official grades plus a gain of at least 15 percentage points and one-sided task-stratified p < 0.05; its refreshed public export verifies 150 of the 327 official grades in the recovered L0 cohort. r67b has no recovered public predeclared decision rule and its task/arm assignments remain unresolved. r71 has no located promotion threshold and only 40 model outcomes for 48 planned model slots; its nine invalid controls are not model failures. No decision or verdict changed.

The repository exact-join check verifies unique IDs on both sides and every capture ID against the refreshed export. The specification-fragment and round-inclusion checks are recorded below.

## Validation output

- `python3 reproduce/build_grade_join.py`: PASS — wrote 5,020 exact public official-export matches and 0 capture-reported-only mappings.
- The B1 exact-join predicate in `validate_repo.py`: PASS — no B1 join, count, report, or status errors were emitted.
- `python3 reproduce/validate_spec_snapshot.py`: PASS — 134 linked v1.2 fragments resolve; provenance, local navigation, and published-byte hashes verify.
- `python3 reproduce/test_validate_release.py`: PASS — six policy cases cover acceptance and rejection conditions for release-included-with-label.
- `python3 reproduce/validate_repo.py`: PASS — all five r67b task mappings reconcile to official grade rows and exact source-crosswalk identities; the pinned specification checks pass.
- `python3 reproduce/validate_release.py`: PASS — B1 and B2 are resolved; all three descriptive rounds pass strict declaration validation and their official-grade reproducers.

## Specification and decision sources

The locally sanitized [specification snapshot](../spec/README.md) preserves the v1.2 clause-reference content cited at original revision `1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0`; the public-release sanitization basis is revision `30d9b25e4eefa7117121de44298fed504b429f4e`. `spec/SOURCE.json` separates original-source hashes from hashes of the exact published bytes, and the SHA-256 manifest verifies the complete snapshot. All 134 linked v1.2 fragments in EVIDENCE-MAP.md are locally verified. **B2 is resolved for this cited-fragment subset.** The decision ledger is absent, so comprehensive decision-to-clause coverage remains limited.

## Scored-round record and release status

The strict record validator has Standard records, `MEASURED.md`, and exact `MISSING.md` declarations for [language replication](../rounds/lang-sol-replication/README.md), [L3 repair](../rounds/l3-repair/README.md), and [L3b repair vs continue](../rounds/l3b-repair-vs-continue/README.md). The language round has 1,782 missing Standard capture slots and four declared deviations; L3 repair has 390 missing slots and four declared deviations; L3b has 193 missing slots and two declared deviations. Their labelled-release policy requires `DESCRIPTIVE — raw captures not retained; results verified against official grades`, exact gap/deviation declarations, and passing official-grade reproducers. All three reproducers pass. Missing receipts have not been reconstructed: the language smoke-gate exception receipt and per-cell L3 grade receipts are unavailable. L3b publishes its per-test no-regression result as a boolean only, with the private checker identified by SHA-256.

## Archive claims and limits

- **Sol-medium language replication:** The raw combined totals and post-hoc equal-task rates are reproduced from the round CSV. The original formula and the four-pass scale are unrecorded, so the equal-task calculation is a sensitivity analysis, not an executable registered branch. See [round results](../rounds/lang-sol-replication/RESULTS.md) and [claim ledger](claim-ledger.jsonl).
- **L3 repair:** The aggregate CSV reproduces two rescues among six repairs; the three-rescue threshold was not met. Per-test pass-set preservation is unverifiable, and the sample does not establish causal repair benefit. See [round results](../rounds/l3-repair/RESULTS.md).
- **L3b repair vs continue:** The sanitized 24-cell table reproduces 3/8 REPAIR, 1/8 CONTINUE, and 2/8 RESTART rescues. The registered REPAIR-minus-CONTINUE threshold is met, and the private per-test no-regression result is published as a boolean. The result remains descriptive because of the disclosed DEV-1 overlap, hidden-suite exposure, and run-record gaps. See [round results](../rounds/l3b-repair-vs-continue/RESULTS.md).
- **L6 auditor replay:** In the offline 40-patch replay, neither auditor met both predeclared precision and false-demotion targets. The 79 valid verdicts among 80 requests are auditor outputs, not official benchmark grades. The result supports advisory-only use for this sample, not a live Build gate.
- **R70 extension outcomes:** The public test-count ledger supports the pre-registered reps 31–32 full-pass counts for this extension: Rust 5/6, Elixir 4/6, Go 4/6, and TypeScript/Bun 6/6. Keep rep 33 separate as a post-hoc addition; the small, one-model cohorts do not support a stack ranking.
- **L1 grader controls:** Official controls found that all 14 wrong mutants failed and all 7 valid alternatives passed across the seven admitted variants. Two mutants failed at build and are weaker controls; each affected variant also had a behavior-level mutant failure. This supports only the listed task/grader control outcomes, not general grader fairness or Build success.
- **Latency probes:** The short and long probes support descriptive client-visible Codex CLI timing summaries from their public raw logs. Report 77 short-probe attempts and 76 uncensored completions, and 18 long-probe attempts and 17 uncensored completions. These do not establish provider transport latency, task success, production limits, or a model/effort ranking.
- **Task-8 smokes:** Four public task-8 smoke rows each record 1/25 hidden-test assertions and are explicitly unscored. They support smoke diagnostics only, with no task-8 efficacy or language-comparison claim.
- **L0 reconciliation:** `python3 reproduce/reconcile_l0.py` reproduces the published sanitized CSV analyses. It does not make each row an independently joined official outcome. R74 remains WITHDRAWN, and R72/R69/R57 remain bounded by their existing cohort status and join coverage.

Family summaries remain bounded. They do not establish a general comparative Build-success effect, and interim, confounded, withdrawn, not-run, or source-reported historical counts are not promoted into verified comparisons.

## Validation contract

- The archive validator checks source integrity and reports open publication gates without treating a successful exit as release authorization.
- `python3 reproduce/validate_round.py --round ID --strict` validates the Standard record structure and exact gap/deviation declarations. `PASS WITH DECLARED DEVIATIONS` is release-included only under the tested descriptive-label rule and a passing official-grade reproducer.
- `python3 reproduce/validate_release.py` checks all registered required scored rounds and fails for open evidence gates, missing Standard rows, undeclared gaps, undeclared protocol deviations, an invalid descriptive label, or a failed official-grade reproducer.
- `npm run build` creates and checks the archive site. The publication build path runs the release validator first and stops while any release gate remains open.
- The site checker validates the generated snapshot's revision and source hashes against the current committed `HEAD`.
