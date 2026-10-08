# Decision rule

For each model, hidden FAIL is positive and `veto` is a positive prediction. Compute:

- Veto precision = TP / (TP + FP).
- Recall = TP / (TP + FN).
- False-demotion rate = FP / all hidden PASS cases.

Report two-sided 95% Wilson intervals for all three proportions. Undefined precision (zero vetoes) fails the precision target. The target check uses observed point estimates: a model is eligible for automatic demotion only if precision is at least 0.90 and false-demotion rate is at most 0.05. Otherwise its verdicts remain advisory. Wilson intervals describe uncertainty; this EXPLORATORY offline replay does not change a live gate.

At 20 cases per model, the first 20 are balanced 10 PASS / 10 FAIL. If false demotions exceed 5 of those 10 good cases, stop that model only when the projected remaining usage (first-20 mean total tokens × 20) exceeds 250,000 tokens; otherwise finish its remaining calls. Record any stop.

An eligible result means the model meets both target point estimates under this offline replay. This round is an offline replay and does not configure a live gate.
