# Review component head: supplied-Intent paired screen

**Verdict: unresolved, TENTATIVE.** This four-task, one-pair-per-task smoke screen does not establish a component improvement or regression. Both arms used the same frozen, previously generated Intent for each task; approval was performed by the harness. Intent generation and acceptance separation were not measured.

## Comparison and results

The control was [release v0.1.0-dev.41d70052](https://github.com/KogenAI/kogen/releases/tag/v0.1.0-dev.41d70052); the candidate used this release with only the [review component at its tested head](https://github.com/KogenAI/kogen-review/commit/b1cdd8d7f5f81e6d19ef2ffc5fb9a789f595c9db). Control archive SHA256 `804016fb34837f60b7269f92aa364053beeba1c87d0831da7faf46b9117b5fdb`; candidate archive SHA256 `0cf88ccf064abafaf26afe2f39489757ce6fd178e07d720dbc7067135d6772ab`. The candidate was separately compiled, so the compiler difference is a confound. All cells used gpt-6.1-terra medium, identical supplied files within each pair, and one repetition. Review is reached only if Build progresses. The component comparison covers a range of changes, not a single mechanism.

Primary graded result: mean fraction of requested hidden checks passed per graded cell 0.7479 control versus 0.4813 candidate; totals 32/41 versus 18/41. Landed 4/4 versus 3/4; approved supplied Intents 4/4 versus 4/4; hidden all-pass 2/4 versus 1/4. The mean is per task, not pooled; errored checks are counted as not passed by the metrics script and shown explicitly below, so this is not evidence that all errored checks are ordinary assertion failures.

| Task | Control: approval / outcome / hidden passed / all-pass / errors / seconds / input / output | Candidate: approval / outcome / hidden passed / all-pass / errors / seconds / input / output |
|---|---|---|
| T1 | ok / landed / 13/13 / True / 0 / 105.999 / 78,162 / 3,850 | ok / landed / 13/13 / True / 0 / 109.815 / 59,763 / 3,973 |
| T2 | ok / landed / 13/15 / False / 0 / 899.054 / 1,691,549 / 12,486 | ok / no_progress / 0/15 / False / 15 / 409.761 / 758,824 / 3,875 |
| T3 | ok / landed / 5/5 / True / 0 / 540.473 / 880,136 / 5,596 | ok / landed / 4/5 / False / 1 / 406.786 / 615,402 / 4,608 |
| T4 | ok / landed / 1/8 / False / 7 / 355.707 / 348,422 / 6,625 | ok / landed / 1/8 / False / 7 / 552.079 / 427,769 / 5,250 |

The wall values include failed attempts within each cell. Control versus candidate totals: 2,998,269 versus 1,861,758 input tokens, 28,557 versus 17,706 output tokens, and 1901.233 versus 1478.441 seconds summed cell wall. Costs in dollars are unavailable because the model was unpriced by the receipts; reported zero placeholders are not evidence of free use. Cached input and stage-level token details are in the data file. Whole-workflow helper, assembly and grading costs are not available.

## Attribution and limitations

T2 differs in landed outcome and requested checks: the release landed and passed 13 of 15; the candidate stopped in Build verification at `no_progress`, after the same acceptance remained red and the builder responded without a tool call. All 15 candidate checks were recorded as errors. This is upstream Build, class (e), with no evidence that the changed review component caused the stop; the candidate did not reach Review. T3 has a one-check difference (5/5 versus 4/5): both landed and both reviews approved with no findings; the single candidate check errored, and the saved evaluation does not identify whether implementation or grading caused it. Its cause is class (e), not an established review effect. T1 matches on requested checks. T4 matches at 1/8 requested checks, with seven errored checks in each arm; both landed and both reviewers approved.

The cause classes are (a) established effect of the changed component, (b) shape or approval, (c) review, (d) infrastructure, and (e) unclear or outside the changed component. No class-(a) change is established in these paired logs.


The sample is too small for a claim of significance or equivalence. The source archive identifies the assembled component but is not by itself a witness that any particular change fired. Acceptance separation was not evaluated. Disposition: bounded confirmation only against matching stored release cells, with a predeclared mechanism, qualified target and held-out tasks; stop after two instrument failures or one attributable regression, with a fixed four-cell and $40 nominal cost cap. No adoption request follows from this screen.

## Rerun

To recompute the reported rows from the included sanitized data, run `python3 report.py`. To rerun the experiment, assemble the release with the linked component head and repeat the registered supplied-Intent, build-phase comparison using the same frozen qualified tasks and graders, model, effort and guarded lane admission; then run `lanes-grade <run-dir> --tasks <qualified-task-dir>` and the metrics script on the finished run. The assembly uses `cand-assembly.sh --kogen-src <release-source> --kogen-sha 41d70052bf0ff932a0424df86a0fb388021428fc --override github.com/KogenAI/kogen-review=<component-source>@b1cdd8d7f5f81e6d19ef2ffc5fb9a789f595c9db --repack <release-archive>:804016fb34837f60b7269f92aa364053beeba1c87d0831da7faf46b9117b5fdb --out <output-dir>` with that script and its prerequisites installed. The source is linked above; no source or patch is bundled.
