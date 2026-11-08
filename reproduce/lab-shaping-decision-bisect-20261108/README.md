# Shaping decision-check attribution

With the same historical Kogen client, same model and host, the shaper immediately before [1e795ed](https://github.com/KogenAI/kogen-shaping/commit/1e795ede88104c4cf496683c5c3ad660ce30e042) was ready 12/12; at that commit it was ready 7/12. Among matched task/repetition pairs, 5 changed from ready to not ready and 0 in the reverse direction. 3 of the losses terminated at the decision check introduced by this commit. The observed drop exceeds the approximate ±1 per ten noise described for the previous comparison, but the set was selected for prior regressions and is not a population pass rate.

The [f04edcea historical shaper](https://github.com/KogenAI/kogen-shaping/tree/f04edcea9896db525855a810bf6c0429b8494278) was ready 11/11 in the supplemental cells. The final c02 repetition was not run because its launch check refused on host load at the conservative 40-attempt cap. The supplemental cells ran after the adjacent arms, rather than being interleaved. All arms used Kogen [d98cfe01](https://github.com/KogenAI/kogen/tree/d98cfe018ef5717de8e67d91fb39f91f997bea9e), Sol low, no answerer, and the same host within each pair; the eight non-shaping Go dependency entries matched. Timings include failed attempts. Each cell resolved Apple Git 2.54.0 (Apple Git-157) via /usr/bin. The three binaries were hashed at setup; the remaining launches also checked their hashes. The conservative cap counted 35 model cells, two zero-call login failures and three prelaunch refusals. Shared balance readings cannot attribute exact credits, and usage includes unknown calls.

| Task | Rep | f04edcea | Parent | 1e795ed | Post-commit terminal gate |
| --- | ---: | --- | --- | --- | --- |
| c01 | 1 | ready | ready | ready | — |
| c01 | 2 | ready | ready | ready | — |
| c02 | 1 | ready | ready | ready | — |
| c02 | 2 | not measured | ready | not ready | decision_evidence |
| c03 | 1 | ready | ready | ready | — |
| c03 | 2 | ready | ready | ready | — |
| c05 | 1 | ready | ready | not ready | decision_check |
| c05 | 2 | ready | ready | ready | — |
| c07 | 1 | ready | ready | not ready | question_check |
| c07 | 2 | ready | ready | ready | — |
| c09 | 1 | ready | ready | not ready | decision_check |
| c09 | 2 | ready | ready | not ready | decision_check |

The terminal decision-check refusals recorded unsupported statements and no contradictions. At this commit [the checker receives the request and candidate Intent](https://github.com/KogenAI/kogen-shaping/blob/1e795ede88104c4cf496683c5c3ad660ce30e042/shape/decision.go#L194-L195), without the probe transcript. That is a specific mechanism for investigation, not proof that each disputed statement was correct. Other losses ended at existing later gates after a decision-check refusal; those causal paths remain unresolved. The [current decision-check file](https://github.com/KogenAI/kogen-shaping/blob/0484edf817f6dc74f691f44d5234cf7f6ae0435e/shape/decision.go) differs from the introduced version only in loop import paths, while its integration and other gates changed.

The current endpoint could not be built with the historical client without selecting newer dependencies that conflict on old and public loop types. The reverse pairing also failed in prior setup. Thus this study isolates the adjacent commit on the historical client; it does not measure a same-client comparison against current [0484edf8](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e) or establish that a revert repairs the current release. The smallest reversible investigation candidate is the decision-check integration and its evidence input; retain the useful gate and do not treat this as a delivery fix. Valid Intent beyond readiness, discriminating acceptance, implementation landing and hidden-grader outcomes were not independently measured. Go and Node task workspaces were reconstructions whose byte identity with the original study is unverified.

## Rerun

Run `python3 report.py` to recompute the paired readiness counts from `data.json`. To repeat the model study, use the [small-request setup](../lab-shaping-small-requests-20261107/README.md), the source pins above, a single compatible Kogen client and host per pair, Sol low and no answerer; capture terminal readiness, question status and wall times. The historical client reads its model lineup from project.yaml. Compare fresh same-host pairs and preserve useful evidence gates.
