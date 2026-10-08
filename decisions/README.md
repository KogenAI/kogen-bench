# Benchmark decisions

These records summarize measured tradeoffs. A design default is not itself a measured winner. See the [public glossary](../rounds/GLOSSARY.md) for statistical terms and arm aliases.

| Topic | Public result | Limit |
| --- | --- | --- |
| Builder assistance | [R51](../rounds/r51/README.md): Luna-low recorded 14/16 passes with planning steps and 5/16 without. Recomputed 6 Oct 2026 with a one-sided Fisher exact test and Holm adjustment across nine plan-versus-none contrasts: adjusted p=0.014349. A two-sided Fisher/Holm-9 calculation gives adjusted p=0.028699. | Descriptive, post-hoc comparison; it does not establish improvement across several tasks. The original p=0.003472 is not reproducible from the public record. |
| Stage removal | [R56](../rounds/r56/README.md) evaluated single-stage ablations and context packs. | The tests did not support removing all stages together; some contrasts were underpowered. |
| Builder tools | [R57](../rounds/r57/README.md) reported fewer median tokens for shell-only in 16 of 16 pooled strata. | One final closure cell was missing. The reported non-inferiority bounds are not independently reproduced because the interval method and resampling inputs are unavailable. |
| Harness comparison | [R53](../rounds/r53/README.md) reports observed pass counts of 28/36, 32/36, and 34/36 across its three arms. | Counts are descriptive. The reported directional p-value is not reproducible because its test, comparison unit, and multiplicity family are not specified. Venue differs by family. |
| Effort | [R66](../rounds/r66/README.md): Sol medium passed 17/20 tasks, Luna max passed 6/20, and Sol high passed 19/20. | Five repetitions per task do not establish equivalence. |
| Stack comparison | [R70](../rounds/r70/README.md) has no scored stack conclusion for its frozen core study. The fixed-skeleton task 1/task 4 report records 11/15 passes in [the published rerun results](../rounds/r70-rve-rerun/RESULTS.md). | The original task 1/task 4 evidence is confounded. The public record does not include passing control receipts for all corrected front ends, so the rerun counts are reported but not independently validated as the preregistered cohort. |

Offline experiments have distinct coverage, pairing, and cost definitions; their counts are not added to online-cell denominators.
