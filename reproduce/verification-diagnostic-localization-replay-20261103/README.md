# Retained verification diagnostic localization replay

Verdict: **unresolved**. Model-free replay of ten retained inputs across five component repositories; eight mechanisms. The report formatter names the attributed responsible file in five cases, a relevant line or function in three, and the full actually-tested revision tuple in none. Missing revision evidence does not demonstrate a stale revision. Finished 2026-11-03T18:18:46.650465Z.

This is a diagnostic probe. Four inputs are synthetic witnesses or classifier fixtures, six are retained landing failure summaries. Two pairs share mechanisms. It is not a cohort of ten independently observed failed repairs. One test-fixture attribution is provisional: excluding it gives file 4/9, line/function 2/9 and full tuple 0/9.

Current verification f4d004d correctly avoids classifying two quoted resource assertions as host failures; historical replay classified both as host failures. That classification repair has already landed. No new candidate patch or model run was tested. Time to correct repair, irrelevant reads, repair tokens and hidden correctness were not measured. No model/API call was made by the probe; orchestration-model accounting and historical repair costs are unavailable.

The exported formatter source blob is identical at adopted 587f67d, retained 5070052 and current f4d004d. The current replay used verification f4d004d, coordinator c4a49a4 and Loop c6e2360 with Go 1.27.2. It called exported Diagnostic and EnvFailure from an external Go test and did not edit a component. Transforming retained landing summaries is a feedback proxy, not reconstruction of lost historical report envelopes. Retained declared module pins are not proof of runtime dependency overrides.

The conditional candidate comparison remains incomplete: the audited task and plan catalog contained no same-case adopted-release comparator. A fresh control would violate the candidate-only protocol. The present result supports collecting exact source provenance and testing localization separately; it does not establish faster or more accurate repairs.

## Public source references

- [kogen-build 7757726](https://github.com/KogenAI/kogen-build/commit/77577264387a164f1ce1928fd414e852916cc6ed)
- [kogen-build b47cde7](https://github.com/KogenAI/kogen-build/commit/b47cde70dcdf4fea58f2043b31619b07e8bdc9da)
- [kogen-build b9990a3](https://github.com/KogenAI/kogen-build/commit/b9990a3d090306d79e28ac0d858ba47c8f3b0ed4)
- [kogen-loop 3372dcf](https://github.com/KogenAI/kogen-loop/commit/3372dcfd45bf28deeb8379618a094a032f4930d8)
- [kogen-review 4870fdd](https://github.com/KogenAI/kogen-review/commit/4870fdd4b571ccda55a516a6ef30bafd050ae40c)
- [kogen-shaping 0f3c76f](https://github.com/KogenAI/kogen-shaping/commit/0f3c76f5c6db3e6bf85ab2f570f11fe53ab31bfa)
- [kogen-verification c025c69](https://github.com/KogenAI/kogen-verification/commit/c025c694888d933e851664df7937c0a535234425)
- [kogen-verification f4d004d](https://github.com/KogenAI/kogen-verification/commit/f4d004d53a8d2928c778462944993a93fc5f5ee4)

## Rerun

Patch under test: none. This probe evaluates the unmodified public verification commits above and links later component fixes as source-location ground truth. The pack contains retained diagnostic data, commit ids and a reporting script; it contains no component source or source patch.

From the repository root:

```sh
python3 -I reproduce/verification-diagnostic-localization-replay-20261103/report.py reproduce/verification-diagnostic-localization-replay-20261103/evidence.json | diff - reproduce/verification-diagnostic-localization-replay-20261103/expected-output.txt
```

This command verifies input hashes and recomputes descriptive scores from the recorded manual attribution. It does not independently prove that attribution or rerun repairs. Inspect each public fix and responsible region when reassessing scores. File credit permits basenames; line/function credit excludes assertion sites that merely call the broken helper.

A bounded follow-up permits at most three candidate-only Terra medium cells after qualified same-task snapshots, runtime tuples and stored adopted comparators exist. It stops on the first setup/provenance failure or its fixed cell/time cap. This is not a qualified improvement or a release gate.
