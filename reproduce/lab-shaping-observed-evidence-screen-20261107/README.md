# Existing-behavior evidence in shaping

An initial instruction to cite inspected evidence for expectations based on existing behavior was screened on ten small requests. The stored release produced 6 ready Intents; the candidate produced 4. One request changed from not ready to ready and three changed from ready to not ready. Neither arm asked a question. The candidate failed the registered no-regression rule and was dropped. This is a screen, not a full-set result or a delivery qualification.

The decision and readiness gates were unchanged. All three regressions ended at readiness reporting a generated Python bytecode path, after earlier intent and decision-check refusals. The gained request ended at the decision-evidence gate in the release and reached ready in the candidate after earlier checks. These are observed stages, not proof that the instruction caused any flip. Intermediate refusals could be repaired; ready means terminal readiness without questions or terminal refusal.

One run per request and arm used the same model and low effort, without an answerer; the release cells were stored results. Times include failed attempts. The shared credit balance showed no movement, but exact attributable spend is unknown. No held-out or complex tasks, hidden checks, or builds were used in this screen, so landing and hidden-check rates are not measured. A single repetition cannot separate these changes from ordinary variation.

The release uses [Kogen source](https://github.com/KogenAI/kogen/tree/47236bbb93385bc960fd2ac353c9b000bd6ed571) and [shaping source](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e). The candidate added only the initial instruction described above; the source trees themselves are not included.

## Rerun

Run `python3 report.py` to reproduce the paired counts from the included data. To repeat the experiment, use the small-request setup described in the [small request finding](../lab-shaping-small-requests-20261107/README.md), use the pinned release as control, add the evidence instruction described above to the initial shaper prompt for the candidate, and shape the same ten climb requests once per arm with the same model, low effort and no answerer. Record terminal readiness, questions, gate refusals and wall time; repeat pairs to measure variation before claiming causality.
