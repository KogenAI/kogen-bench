# Preventing transient bytecode in shaping checks

A prompt instruction asked generated acceptance steps to avoid transient Python bytecode writes in the checked project. The stored release produced 6 ready Intents on ten small requests; the candidate produced 7. Two requests changed from not ready to ready and one changed from ready to not ready. Neither arm asked a question. The regression fails the registered no-regression condition, and the net gain is within the previously observed paired flip range. The candidate was dropped. This is a screen, not a full-set result or a delivery qualification.

The readiness mutation gate remained unchanged. The instruction fired in one ready candidate: its generated step invoked Python with bytecode suppression. That request was ready in the release too. The regression ended at the decision check, and the gains involved other gates. These observations are not proof of causality. Intermediate refusals could be repaired; ready means terminal readiness without questions or terminal refusal.

Each request ran once per arm on the same model and low effort, without an answerer; the release cells were stored results. Times include failed attempts and are in the data. The shared credit balance did not move, but exact attributable spend is unknown. No held-out or complex tasks, hidden checks, or builds were used in this screen, so landing and hidden-check rates are not measured. A single repetition cannot separate these changes from ordinary variation.

The release uses [Kogen source](https://github.com/KogenAI/kogen/tree/47236bbb93385bc960fd2ac353c9b000bd6ed571) and [shaping source](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e). The candidate added only the initial instruction described above; source trees themselves are not included.

## Rerun

Run `python3 report.py` to reproduce the paired counts from the included data. To repeat the experiment, use the small-request setup described in the [small request finding](../lab-shaping-small-requests-20261107/README.md), use the pinned release as control, add the bytecode instruction described above to the initial shaper prompt for the candidate, and shape the same ten climb requests once per arm with the same model, low effort and no answerer. Record terminal readiness, questions, gate refusals, generated step behavior and wall time; repeat pairs before claiming causality.
