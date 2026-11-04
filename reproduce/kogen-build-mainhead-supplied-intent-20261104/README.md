# Build component head: supplied-Intent paired screen

**Verdict: unresolved, TENTATIVE.** This four-task, one-pair-per-task smoke screen does not establish a component improvement or regression. Both arms used the same frozen, previously generated Intent for each task; approval was performed by the harness. Intent generation and acceptance separation were not measured.

## Comparison and results

The control was [release v0.1.0-dev.41d70052](https://github.com/KogenAI/kogen/releases/tag/v0.1.0-dev.41d70052); the candidate used this release with only the [build component at its tested head](https://github.com/KogenAI/kogen-build/commit/2e10d934cac2a523165a22db13786afbbf42f165). Control archive SHA256 `804016fb34837f60b7269f92aa364053beeba1c87d0831da7faf46b9117b5fdb`; candidate archive SHA256 `0a9011babd9ffcf4cdaffa261be1d97fb35b003efda4a0f0b7811a9b8c3ecaf5`. The candidate was separately compiled, so the compiler difference is a confound. All cells used gpt-6.1-terra medium, identical supplied files within each pair, and one repetition. Review is reached only if Build progresses. The component comparison covers a range of changes, not a single mechanism.

Primary graded result: mean fraction of requested hidden checks passed per graded cell 0.5312 control versus 0.5312 candidate; totals 19/41 versus 19/41. Landed 3/4 versus 3/4; approved supplied Intents 4/4 versus 4/4; hidden all-pass 2/4 versus 2/4. The mean is per task, not pooled; errored checks are counted as not passed by the metrics script and shown explicitly below, so this is not evidence that all errored checks are ordinary assertion failures.

| Task | Control: approval / outcome / hidden passed / all-pass / errors / seconds / input / output | Candidate: approval / outcome / hidden passed / all-pass / errors / seconds / input / output |
|---|---|---|
| T1 | ok / landed / 13/13 / True / 0 / 112.199 / 78,436 / 3,829 | ok / landed / 13/13 / True / 0 / 123.62 / 74,348 / 4,375 |
| T2 | ok / no_progress / 0/15 / False / 15 / 208.263 / 185,307 / 1,168 | ok / review_blocked / 0/15 / False / 15 / 656.146 / 801,995 / 8,637 |
| T3 | ok / landed / 5/5 / True / 0 / 509.186 / 935,211 / 6,512 | ok / landed / 5/5 / True / 0 / 606.73 / 739,113 / 6,286 |
| T4 | ok / landed / 1/8 / False / 7 / 457.272 / 343,501 / 5,138 | ok / landed / 1/8 / False / 7 / 572.056 / 378,949 / 6,384 |

The wall values include failed attempts within each cell. Control versus candidate totals: 1,542,455 versus 1,994,405 input tokens, 16,647 versus 25,682 output tokens, and 1286.92 versus 1958.552 seconds summed cell wall. Costs in dollars are unavailable because the model was unpriced by the receipts; reported zero placeholders are not evidence of free use. Cached input and stage-level token details are in the data file. Whole-workflow helper, assembly and grading costs are not available.

## Attribution and limitations

T2 has different stop types although neither arm passes a hidden check: the release stopped in Build verification after repeated red acceptance and no new tool call; the candidate reached Review and was blocked on findings about repeated attachment references and missing evidence for concurrency and rollout. The review stop is class (c); the release-side Build stop is class (e), because sound acceptance and a component-specific cause have not been established. All 15 requested checks errored in each cell, without an infrastructure diagnosis in the evaluation receipts. These errors do not distinguish implementation defects from grading errors. T1 and T3 match on their requested-check results. T4 also matches at 1/8, with seven errored checks in each arm and no recorded infrastructure diagnosis; both landed and both reviewers approved.

The cause classes are (a) established effect of the changed component, (b) shape or approval, (c) review, (d) infrastructure, and (e) unclear or outside the changed component. An outcome at the changed stage is not sufficient to establish class (a); no class-(a) change is established in these paired logs.


The sample is too small for a claim of significance or equivalence. The source archive identifies the assembled component but is not by itself a witness that any particular change fired. Acceptance separation was not evaluated. Disposition: bounded confirmation only against matching stored release cells, with a predeclared mechanism, qualified target and held-out tasks; stop after two instrument failures or one attributable regression, with a fixed four-cell and $40 nominal cost cap. No adoption request follows from this screen.

## Rerun

To recompute the reported rows from the included sanitized data, run `python3 report.py`. To rerun the experiment, assemble the release with the linked component head and repeat the registered supplied-Intent, build-phase comparison using the same frozen qualified tasks and graders, model, effort and guarded lane admission; then run `lanes-grade <run-dir> --tasks <qualified-task-dir>` and the metrics script on the finished run. The assembly uses `cand-assembly.sh --kogen-src <release-source> --kogen-sha 41d70052bf0ff932a0424df86a0fb388021428fc --override github.com/KogenAI/kogen-build=<component-source>@2e10d934cac2a523165a22db13786afbbf42f165 --repack <release-archive>:804016fb34837f60b7269f92aa364053beeba1c87d0831da7faf46b9117b5fdb --out <output-dir>` with that script and its prerequisites installed. The source is linked above; no source or patch is bundled.
