# Review value by builder strength

This model-free analysis pools pre-review grades from published screens. A rescue means review turned failing code into passing code. The rounds are approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

The source rounds are [builder effort](../rounds/builder-low-1/README.md), [the combined lower-cost profile](../rounds/cheap-profile-1/README.md), [prose versus Gherkin](../rounds/prose-vs-gherkin-1/README.md), [named-defect review](../rounds/review-named-defect-1/README.md), and [reviewer effort with a weak builder](../rounds/reviewer-effort-weak-1/README.md). The Sol pool uses bl1, cp1, cp1b, pg1 and rn1; the weak-builder pool uses pg2, rew1, rew1b, rew2 and rn2.

| Builder setting | Attempts reaching review | Already correct before review | Wrong at review | Rescued | Wrong code approved unchanged |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol medium or low | 62 | 62 | 0 | 0 | 0 |
| Weak builder | 41 | 17 | 24 | 24/24 | 0 |

With Sol builders, no wrong tree reached review in 62 attempts. These tasks may be too easy for the Sol builders. With the weak builder, review rescued 24 of 24 wrong trees among 41 attempts that reached review. These are development-task screens; the counts do not estimate how often other tasks will need review.

Excluded are six prose-only attempts on r70-6-elixir-2: both repetitions in both rn1 settings, and both repetitions in pg1's prose setting. Each wrong result was caused by an output-key order that the prose did not specify but a scenario example showed. Those failures do not measure whether review can find a defect stated in the requirements.

No new run or model calls were made. The source grades were generated after the original runs by checking each available pre-review tree against its hidden tests. The 41 include one unscored provider-refusal attempt and one attempt stopped during review on correct code. Seven other weak-builder attempts stopped before review and are excluded.
