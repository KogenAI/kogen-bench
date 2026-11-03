# Shaping repair: completed paired screen

**Decision: KEEP.** All eleven registered pairs completed and were graded. Control produced 6/11 valid Intents and landed 2/11 tasks; candidate produced 4/11 valid Intents and landed 4/11. Complete hidden all-pass was 1/11 versus 1/11.

The owner rule reverts only when the candidate has fewer valid Intents **and** no more landed tasks. Keeping under this rule is an operational decision; it does not establish general improvement or a causal rescue. This new finding completes the earlier nine-pair screen without changing that published result.

## Comparison

Control: [published release](https://github.com/KogenAI/kogen/commit/6e69ffb3243603cd5cd9253efd418a0c24130583), shaping pinned at 94eabe5. Candidate: same assembly with only [shaping at 2192ae21](https://github.com/KogenAI/kogen-shaping/commit/2192ae219448148250d30144ff4ea9385be26679). This includes intervening shaping ancestors; it does not isolate the last commit. Both binaries used Go 1.27.2.

Control archive SHA256: `2779df93030406504f013c72304dfc7370094cd02c624edf7998e83a9749630c`. Candidate archive SHA256: `52679d4e842e6662ebe2d6179ed803d2c3676266d1b3a5095fc3ead088fbd2c8`. Control binary SHA256: `ceedfa2237027cce2c3d7b2fa2ac6aee1969337f9995959140547571b323e477`. Candidate binary SHA256: `42091999ff176d7c6fbc28323cd428b04a9815ef47c50a93abbc1b4bddc9024b`.

Request-only full pipeline; gpt-6.1-terra medium for shape, build and review, native ChatGPT route. Each task used concurrent arms in the same execution environment. One repetition per task. Nine tasks target previously diagnosed shaping failures; two are existing qualified guards. Tasks are anonymized below. Selection on prior failures and stochastic variation limit inference. No extra cells or trials. The two completion pairs used the original artifacts and kits, following renewed owner authorization after the earlier launch cutoff.

## Paired results

| Task | Selection | Control Intent / outcome / hidden | Candidate Intent / outcome / hidden |
| --- | --- | --- | --- |

| T1 | target | yes / landed / 7/8 | yes / landed / 7/8 |

| T2 | target | yes / build_blocked / 1/8 | yes / landed / 1/8 |

| T3 | target | yes / build_blocked / 0/14 | no / refused / 0/14 |

| T4 | target | no / questions_pending / 0/12 | no / questions_pending / 0/12 |

| T5 | target | yes / build_blocked / 0/15 | no / refused / 0/15 |

| T6 | target | no / questions_pending / 0/6 | no / refused / 0/6 |

| T7 | target | no / questions_pending / 1/8 | no / refused / 1/8 |

| T8 | target | no / questions_pending / 2/6 | no / questions_pending / 2/6 |

| T9 | held out | yes / build_blocked / 0/5 | yes / landed / 2/5 |

| T10 | target | no / questions_pending / 0/13 | no / refused / 0/13 |

| T11 | held out | yes / landed / 13/13 | yes / landed / 13/13 |


Hidden columns count requested checks only. Baseline regression checks and all-pass are separate columns in the data. A valid Intent means a saved package accepted by shaping; pending questions do not count. Acceptance separation is unknown because request-only task copies omit qualification reference trees. This evaluator limitation does not turn a partial hidden score into success.

## Mechanism and limits

Model-free audit covers every discordant pair. T3 and T5 lose valid Intent at shaping after malformed or incomplete submissions. T2 and T9 land only in the candidate after their independently shaped acceptance differs; this attributes the earliest difference to shaping (class a), without proving correct acceptance. T6 and T7 differ in stop type within shaping but neither has valid Intent. T1, T4 and T8 have unchanged principal endpoints. T10 changes from pending questions to an invalid package (class a, shaping), without a valid-Intent or hidden-result change. T11 lands and passes every hidden check in both arms; no discordant endpoint requires attribution.

Candidate recovery entry is directly observed in retained recovery events; it is not equivalent to a successful repair or proof of the isolated last commit effect. Five candidate cells exhausted incomplete or malformed packages despite recovery; two stopped on permitted interface questions. Existing repair, submission, decision and environment requests cover these mechanisms; no gate was weakened and no new duplicate request was created.

## Cost and time

Control: 3,096,811 input and 40,993 output tokens, 1622.888 seconds summed cell stage wall. Candidate: 4,383,752 input and 47,289 output tokens, 1973.260 seconds. Failed attempts and recovery are included. Review spans may overlap Build, so role wall columns must not be added again to cell totals. Reasoning is a subset of output and is not added twice. Cached input and role receipts are supplied in the tables.

Dollar cost is unknown for this unlisted model; zero placeholders are not cost evidence. Assembly, preparation, grading and assistant overhead are unpriced and excluded from the model-cell totals. No whole-workflow efficiency claim is made.

## Rerun

The candidate change is the public shaping commit linked above; no source or source patch is shipped. Recompute the decision and totals from the self-contained sanitized receipts:

```sh
python3 report.py
```

A new model run requires the original qualified task kits and hidden graders, which are not redistributed in this pack. Use the two exact archive hashes above, request-only mode, one repetition, Terra medium in every role, paired concurrent arms, the original 3600-second deadline and normal admission. Run the registered guarded queue command and grade each completed cell with the qualified harness. This pack reproduces the analysis; model outcomes are stochastic.
