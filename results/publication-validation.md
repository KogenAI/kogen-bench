# Publication validation

This report distinguishes repository consistency checks from the configured release gate. `validate_repo.py` checks repository indexes, records, cross-references, covered numbers, privacy rules, and authored relative links. `validate_release.py` validates the historical round-label inventory, applies strict Standard-record checks only to rounds dated 2026-10-09 or later, checks the registered publication gates, and then runs `validate_repo.py`. It does not run scrutiny, require independent-review receipts, or invoke official-grade round reproducers.

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
- `python3 reproduce/validate_release.py`: PASS — 177 rounds are classified as historical; there are no rounds dated from the strict cutoff of 2026-10-09; the registered publication gates and repository checks pass. This result does not mean scrutiny or independent review receipts were checked.

## Specification and decision sources

The locally sanitized [specification snapshot](../spec/README.md) preserves the v1.2 clause-reference content cited at original revision `1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0`; the public-release sanitization basis is revision `30d9b25e4eefa7117121de44298fed504b429f4e`. `spec/SOURCE.json` separates original-source hashes from hashes of the exact published bytes, and the SHA-256 manifest verifies the complete snapshot. All 134 linked v1.2 fragments in EVIDENCE-MAP.md are locally verified. **B2 is resolved for this cited-fragment subset.** The decision ledger is absent, so comprehensive decision-to-clause coverage remains limited.

## Scored-round record and release status

The separate `validate_round.py --round ID --strict` command can check Standard-record structure and declared gaps/deviations for [language replication](../rounds/lang-sol-replication/README.md), [L3 repair](../rounds/l3-repair/README.md), and [L3b repair vs continue](../rounds/l3b-repair-vs-continue/README.md). Their records declare 1,782, 390, and 193 missing Standard capture slots respectively, with four, four, and two deviations. These rounds predate the configured strict cutoff, so `validate_release.py` does not run those strict checks for them and does not invoke their official-grade reproducers. The historical round pages retain their own evidence limits and status labels; missing receipts have not been reconstructed.

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

- `python3 reproduce/validate_repo.py` checks indexes, records, cross-references, covered numbers, privacy constraints, and authored relative links. It does not independently rerun historical model calls or hidden grading.
- `python3 reproduce/validate_round.py --round ID --strict` checks one round's Standard record structure, exact gap/deviation declarations, and the strict eligibility predicate. It is a separate command; `validate_release.py` does not call it for historical rounds.
- `python3 reproduce/validate_release.py` checks that round pages and `rounds/STATUS.md` agree on historical labels, badges, reasons, dates, and recomputation states; applies strict `validate_round.py` checks only to rounds dated 2026-10-09 or later; verifies that the publication-blocker register is well-formed and resolved; and runs `validate_repo.py`. It does not run `scrutinize.py`, inspect or require independent-review receipts, or run official-grade round reproducers. On this snapshot it reports 177 historical rounds, zero new strict rounds, and `RELEASE GATE: PASS`.
