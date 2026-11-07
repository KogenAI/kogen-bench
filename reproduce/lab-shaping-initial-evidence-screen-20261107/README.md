# Initial evidence-path instruction in shaping

An instruction to cite each file as a separate bare path was added to the initial shaper prompt and screened on ten small requests. The stored release produced 6 ready Intents and the candidate 5. Two requests changed from not ready to ready and three changed from ready to not ready. Neither arm asked a question. The candidate failed the registered no-regression rule and was dropped. This is a small screen, not a full-set result or delivery qualification.

The gates were unchanged. Two regressions ended at readiness with a generated Python bytecode path reported; the third ended at an acceptance-step check. One gained request met the evidence gate in both arms before candidate recovery, while the other encountered different gates. These are observed stages, not proven causal effects of the instruction. Intermediate refusals could be repaired; ready means terminal readiness with no questions or terminal refusal.

Each request ran once per arm on the same model and low effort, with no answerer; the control cells were stored results. Times include failed attempts and are in the data. The shared credit balance did not move, but exact attributable spend is unknown. No held-out or complex tasks, hidden checks, or builds were used in this screen, so landing and hidden-check rates are not measured. One repetition does not separate the observed changes from ordinary variation.

The release uses [Kogen source](https://github.com/KogenAI/kogen/tree/47236bbb93385bc960fd2ac353c9b000bd6ed571) and [shaping source](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e). The candidate added only the initial evidence-format instruction; the source trees themselves are not included.

## Rerun

Run `python3 report.py` to reproduce the paired counts from the included data. To repeat the experiment, use the small-request setup described in the [small request finding](../lab-shaping-small-requests-20261107/README.md), use the pinned release as control, add the evidence-format instruction described above to the initial shaper prompt for the candidate, and shape the same ten climb requests once per arm with the same model, low effort and no answerer. Record terminal readiness, questions, gate refusals and wall time; repeat pairs to measure variation before claiming causality.
