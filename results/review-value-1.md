# Review value by builder strength

This model-free analysis pools pre-review grades from published screens. A rescue means review turned failing code into passing code. The rounds are approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

The source rounds are [builder effort](../rounds/builder-low-1/README.md), [the combined lower-cost profile](../rounds/cheap-profile-1/README.md), [prose versus Gherkin](../rounds/prose-vs-gherkin-1/README.md), [named-defect review](../rounds/review-named-defect-1/README.md), [reviewer effort with a weak builder](../rounds/reviewer-effort-weak-1/README.md), [cheap profile confirmation](../rounds/confirm-cheap-profile-1/README.md), [reviewer polish](../rounds/reviewer-polish-1/README.md), [the first medium reviewer confirmation](../rounds/confirm-reviewer-medium-1/README.md), and the later [hard-task review screen](../rounds/review-off-hard-1/README.md). The table below summarizes the earlier reviewed-attempt pools; the hard-task screen is separate because its fixed rule evaluates all 16 first-green builds, including the eight submitted without review.

The earlier Sol-builder pool includes 102 attempts that reached review, including the four-task follow-up to the lower-cost profile and the fresh-task confirmation and reviewer-polish screens. The weak-builder pool includes 57 attempts that reached review, including the first medium-reviewer confirmation.

| Builder setting | Attempts reaching review | Already correct before review | Wrong at review | Rescued | Wrong code approved unchanged |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol medium or low | 102 | 102 | 0 | 0 | 0 |
| Luna low (weak builder) | 57 | 26 | 31 | 31/31 | 0 |

With Sol builders, no wrong tree reached review in 102 attempts. On the four additional development tasks, all eight trees were correct before review; six were approved unchanged and two were polished. With the weak builder, review rescued all 31 wrong trees it received among 57 attempts that reached review. These results combine development screens and fresh-task confirmations; they do not estimate how often other tasks will need review.

Six prose-only attempts are excluded because their prose omitted a requirement present in the executable scenarios: both repetitions for each reviewer instruction in the first named-defect run, and both prose-only repetitions in the first prose-versus-Gherkin run. Those failures do not measure whether review can find a defect stated in the requirements.

This pooling analysis made no additional model calls. The source grades were generated after the runs by checking each available pre-review tree against its hidden tests. The 57 include one unscored provider-refusal attempt and one attempt stopped during review on already-correct code; seven attempts stopped before review and are excluded.

## Update: earlier Sol-builder evidence

Later grading of saved code snapshots, without additional model calls, added 51 Sol-builder attempts with a gradable first-green tree before review. All 51 were correct at that point, extending the earlier Sol-builder count from 102 to 153. Runs pd2 and bs1 could not be graded because their Lab builds rejected the current task qualification files; they are excluded from these counts. The protocol also lists nine specification-gap failures caused by requirements omitted in prose; review fixed none of them (0 of 9). Those failures do not count as genuine wrong-at-review cases.


## Update: harder-task screen

The [hard-task review screen](../rounds/review-off-hard-1/README.md) adds 16 first-green builds across four public task IDs, with two repetitions per task per setting. All 16 were correct when first green, including the eight review-disabled submissions. The fixed rule required at least 4 of 16 first-green builds to be wrong for the task set to be informative; 0 were wrong, so the decision was **NOT INFORMATIVE** and the screen does not establish whether review should be disabled.

No genuinely wrong first-green trees were found among 169 included Sol-builder attempts; eight were submitted without review. The 169 comprise 153 earlier first-green attempts plus the 16 builds in this screen.
