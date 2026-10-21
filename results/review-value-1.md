# Review value by builder strength

This model-free analysis pools pre-review grades from published screens. A rescue means review turned failing code into passing code. The rounds are approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

The source rounds are [builder effort](../rounds/builder-low-1/README.md), [the combined lower-cost profile](../rounds/cheap-profile-1/README.md), [prose versus Gherkin](../rounds/prose-vs-gherkin-1/README.md), [named-defect review](../rounds/review-named-defect-1/README.md), [reviewer effort with a weak builder](../rounds/reviewer-effort-weak-1/README.md), [cheap profile confirmation](../rounds/confirm-cheap-profile-1/README.md), [reviewer polish](../rounds/reviewer-polish-1/README.md), and [the first medium reviewer confirmation](../rounds/confirm-reviewer-medium-1/README.md). The pool includes the first fresh-task confirmation for medium review; it does not include the later second confirmation.

The Sol-builder pool includes 102 attempts that reached review, including the four-task follow-up to the lower-cost profile and the fresh-task confirmation and reviewer-polish screens. The weak-builder pool includes 57 attempts that reached review, including the first medium-reviewer confirmation.

| Builder setting | Attempts reaching review | Already correct before review | Wrong at review | Rescued | Wrong code approved unchanged |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol medium or low | 102 | 102 | 0 | 0 | 0 |
| Luna low (weak builder) | 57 | 26 | 31 | 31/31 | 0 |

With Sol builders, no wrong tree reached review in 102 attempts. On the four additional development tasks, all eight trees were correct before review; six were approved unchanged and two were polished. With the weak builder, review rescued all 31 wrong trees it received among 57 attempts that reached review. These results combine development screens and fresh-task confirmations; they do not estimate how often other tasks will need review.

Six prose-only attempts are excluded because their prose omitted an output-key ordering requirement shown in a scenario: both repetitions for each reviewer instruction in the first named-defect run, and both prose-only repetitions in the first prose-versus-Gherkin run. Those failures do not measure whether review can find a defect stated in the requirements.

No new model calls were made. The source grades were generated after the original runs by checking each available pre-review tree against its hidden tests. The 57 weak-builder attempts include one unscored attempt after a provider refusal and one attempt stopped during review on code that was already correct. Seven other weak-builder attempts stopped before review and are excluded.
