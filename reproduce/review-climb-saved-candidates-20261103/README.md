# Saved-candidate reviews before and after four changes

**Verdict: unresolved.** All 36 prescribed reviews completed: nine correlated saved cases, two repetitions per arm. HELD-OUT target mechanisms detected were A 4/14 and B 3/14. This screen does not establish that B catches more defects without extra false blocks.

DEV was scored and frozen before the first HELD-OUT call. Every assigned case remains in the tables. Repetitions are not additional independent tasks, and this is a component-phase screen with no significance or end-to-end rescue claim.

## What the counts mean

A detection requires concrete evidence for the predeclared mechanism, including a corrective source edit that identifies it. Reported findings and attempted repairs are separate columns. **Repairs remain unverified:** the shipped standalone command refuses external verification after edits. A submitted approval followed by that refusal is not a final approval of the original defective tree. No hidden grader was run on the edited trees.

The case labelled clean has a real fixture failure on the execution environment and an additional demonstrated unlabelled defect. Its observed blocks are retained, but a false-block rate on a genuinely clean tree is not established. Some scoring-key expectations are narrower than the explicit prose contract; those misses remain in the primary totals and are diagnosed separately. The initial adapter evidence declares a green pass with no executed checks; it is not a measured qualification receipt.

## Source and runtime

A is [kogen-review 889ed92](https://github.com/KogenAI/kogen-review/commit/889ed928501c31799fedc8cbf6542fd5393e7a99). B is [kogen-review 3e1f93f](https://github.com/KogenAI/kogen-review/commit/3e1f93f3de911cd737832dbccc626b026a6bd072), whose review implementation is unchanged from [f01c92e](https://github.com/KogenAI/kogen-review/commit/f01c92eae077f6471c678117cedbb881c6501ac8). B includes the four changes under examination. Both arms use the same dependency pins and observation adapter, gpt-6.1-terra medium through ChatGPT, and the same toolchain and Git. Binary and adapter hashes are in data/versions.json. This comparison does not isolate the four changes individually.

## Lever observations

All 36 configured and effective model/effort/backend observations match, and the four initial trees match within every case. B submitted nonempty requirement ledgers in 18/18 runs. Maximum logical requests were A 9, B 12; forced submission at or after request 13 fired 0 times. Recorded repair rounds reached 0; the adapter refusal prevents this screen from exercising the nonconverging-repair bound. These observations do not isolate individual item effects.

## Cost and wall time

All review walls include failed attempts and the tools invoked within a review. Delivery waits and preparation are outside per-review wall measurements. The known route subtotal, including one apparatus-invalid setup attempt, is **$8.671432 at the guard proxy rate**. This is not an actual subscription bill or a published Terra price. Helper/orchestration model cost is unavailable, so a complete whole-workflow monetary total cannot be claimed. The extra attempt's requests, wall and guarded cost are retained in data/workflow-extras.json.

The last counted result file was written at 2026-11-03T20:52:37.964115404Z. Scoring completed at 2026-11-03T20:53:11.459590+00:00; feedback followed the last climb item by 3.970 hours.

## Rerun

Recompute every published per-case and per-arm table with Python's standard library:

```sh
python3 report.py data/scores.tsv
```

The command checks all 36 assigned arm/repetition rows before reporting. data/scores.tsv uses anonymous case labels; it contains no candidate source, evaluator label text or private-reference patches. The public commits above allow inspection of the component changes.

Reproduction scope is the published analysis. Exact live replay requires the evaluator-custodied candidates, scoring key and identical observation adapter; they are not redistributed here. The original command was the standalone kogen-review entry point with a candidate base, approved Intent slug, fresh root, model, provider and effort supplied explicitly.

## Disposition

**Drop this exact screen as qualification evidence.** No automatic extension, component revert or adoption hold is asserted. The comparison does not qualify an improvement claim. A separate mechanism-only follow-up addresses evidence citations that fail to establish a promised postcondition. Normal repository and release gates remain authoritative.

## Paired descriptive tables

| split | case | arm | n | detected targets | missed targets | requests | wall seconds | guarded cost USD |
|---|---|---|---:|---:|---:|---:|---:|---:|
| DEV | D1 | A | 2 | 0 | 0 | 13 | 151.044 | 0.480727 |
| DEV | D1 | B | 2 | 0 | 0 | 7 | 96.365 | 0.434036 |
| DEV | D2 | A | 2 | 0 | 2 | 11 | 146.327 | 0.303443 |
| DEV | D2 | B | 2 | 0 | 2 | 10 | 148.430 | 0.473339 |
| DEV | D3 | A | 2 | 0 | 2 | 13 | 136.775 | 0.478570 |
| DEV | D3 | B | 2 | 0 | 2 | 9 | 157.356 | 0.468327 |
| DEV | D4 | A | 2 | 2 | 0 | 11 | 129.779 | 0.459388 |
| DEV | D4 | B | 2 | 1 | 1 | 11 | 160.024 | 0.483804 |
| DEV | D5 | A | 2 | 2 | 0 | 5 | 30.813 | 0.419450 |
| DEV | D5 | B | 2 | 2 | 0 | 10 | 86.445 | 0.518624 |
| HELD-OUT | H1 | A | 2 | 0 | 2 | 11 | 143.032 | 0.453691 |
| HELD-OUT | H1 | B | 2 | 0 | 2 | 8 | 123.415 | 0.450487 |
| HELD-OUT | H2 | A | 2 | 0 | 4 | 12 | 126.537 | 0.449937 |
| HELD-OUT | H2 | B | 2 | 0 | 4 | 10 | 129.204 | 0.449158 |
| HELD-OUT | H3 | A | 2 | 2 | 0 | 17 | 138.573 | 0.507009 |
| HELD-OUT | H3 | B | 2 | 1 | 1 | 17 | 207.820 | 0.556518 |
| HELD-OUT | H4 | A | 2 | 2 | 4 | 15 | 132.741 | 0.471552 |
| HELD-OUT | H4 | B | 2 | 2 | 4 | 20 | 289.447 | 0.595746 |

| split | arm | n | detected targets | missed targets | requests | wall seconds | guarded cost USD |
|---|---|---:|---:|---:|---:|---:|---:|
| DEV | A | 10 | 4 | 4 | 53 | 594.737 | 2.141578 |
| DEV | B | 10 | 3 | 5 | 47 | 648.622 | 2.378130 |
| HELD-OUT | A | 8 | 4 | 10 | 55 | 540.883 | 1.882189 |
| HELD-OUT | B | 8 | 3 | 11 | 55 | 749.886 | 2.051909 |
| ALL | A | 18 | 8 | 14 | 108 | 1135.620 | 4.023767 |
| ALL | B | 18 | 6 | 16 | 102 | 1398.507 | 4.430039 |

All attempted repairs remain unverified. Guard estimates are not subscription bills.

