# Evidence-path instructions in shaping

A prompt instruction about evidence paths was screened on ten small requests. The stored release produced 6 ready Intents; the candidate produced 8. Three requests changed from not ready to ready and one changed from ready to not ready. Neither arm asked a question. The regression fails the registered no-regression condition, and the net gain is within a previously observed paired flip range. The candidate was dropped; this is a screen, not a full-set result or a delivery qualification.

The candidate told the shaper, in feedback after a decision-record rejection, to cite one bare tracked path per item without line ranges or explanatory prose. The decision and evidence gates remained unchanged. One gained request had failed at another gate in the release; another met the evidence gate in both arms before the candidate recovered. The regression ended at the evidence gate. These observations identify stages, not proven causes of stochastic flips. Intermediate submission refusals were allowed to recover; ready means terminal readiness without questions or terminal refusal.

The comparison used one run per request and the same model and low effort, with no answerer. Times include failed attempts; individual durations are in the data. The account-wide balance showed no movement, but it cannot establish attributable spend. The observed sample is too small to distinguish the net improvement from ordinary variation. The held-out requests and complex tasks were not used in this screen. No hidden checks or product Build stage were run, so landing and hidden-check rates are not measured.

The release uses [Kogen source](https://github.com/KogenAI/kogen/tree/47236bbb93385bc960fd2ac353c9b000bd6ed571) and [shaping source](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e). The candidate changes only the evidence-format feedback instruction; the source trees themselves are not included here.

## Rerun

Run `python3 report.py` to reproduce the paired counts from the included data. To repeat the model experiment, use the small-request setup described in the [small request finding](../lab-shaping-small-requests-20261107/README.md), use the pinned release as control, add the feedback instruction described above for the candidate, and shape the same ten climb requests once per arm with the same model, low effort and no answerer. Record terminal readiness, questions, gate refusals and wall time; repeat pairs to estimate variation before drawing a causal conclusion.
