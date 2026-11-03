# A coherent component update remains unqualified

**Unresolved.** Nine full-pipeline attempts ran against one committed component set. One produced a valid Intent, landed a change and reached an approved review. None passed every hidden check. Three additional shape-only attempts produced no Intent. This smoke screen does not qualify the assembled update or any of its pinned component revisions for adoption.

The candidate is Kogen `c92d8971a91bb005058838eced451b7a9d56596c`, including all the component versions it commits. Both platform releases use that committed tree. Uncommitted changes in the delivery checkout were excluded. This avoids the interface incompatibilities that prevented earlier screens of isolated component heads from assembling.

Every role—shape, build and review—uses **gpt-6.1-terra, medium effort, native OpenAI backend**. There is one candidate attempt per full-pipeline task and no new control arm. Comparators are frozen stored adopted-release attempts for the same tasks, model and effort. Three held-out tasks lack valid stored comparators and serve as descriptive guards. Different platforms, toolchains, Git versions and unavailable historical load readings limit attribution.

## Outcomes

The task labels preserve the development and held-out split without exposing the private kits. Model, effort and backend above apply to each row; unentered roles remain configured but did not run.

| Task | Group | Candidate outcome | Valid Intent | Landed | Hidden all-pass | Stored valid / attempts | Stored landed / attempts | Stored hidden pass / graded |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | targeted | landed, review approved | 1/1 | 1/1 | 0/1 | 11/19 | 2/19 | 0/11 |
| B | targeted | refused during shaping | 0/1 | 0/1 | 0/1 | 3/9 | 3/9 | 0/7 |
| C | targeted | refused at readiness | 0/1 | 0/1 | 0/1 | 4/8 | 0/8 | 0/4 |
| D | targeted | refused at readiness | 0/1 | 0/1 | 0/1 | 2/8 | 1/8 | 0/7 |
| E | targeted | refused during shaping | 0/1 | 0/1 | 0/1 | 0/8 | 0/8 | 0/8 |
| F | targeted | pending UI question | 0/1 | 0/1 | 0/1 | 0/6 | 0/6 | 0/6 |
| G | held-out | refused during shaping | 0/1 | 0/1 | 0/1 | — | — | — |
| H | held-out | pending UI question | 0/1 | 0/1 | 0/1 | — | — | — |
| I | held-out | pending formatting question | 0/1 | 0/1 | 0/1 | — | — | — |

In A, the final tree passed seven of eight checks, including all three regression checks. One requested check errored; the grade has no infrastructure flag. The shaped acceptance passed and review approved with no findings. Acceptance separation is therefore unestablished; passing those checks did not establish complete task correctness. No acceptance-separation replay was added to this screen.

B, E and G failed because the submitted acceptance file was absent. C was refused because its scenarios omitted required deployment, persistence and background-job behavior. D combined missing database preparation in a fresh copy with missing scenario coverage of filtering, representations, access and pagination. These useful checks were preserved. F, H and I asked presentation or formatting questions with no answerer. Shaping is the first stopping stage in all eight non-landed attempts; these are product outcomes, not excluded instrument failures. The assembled update changes that stage, but this design cannot isolate an individual component's causal effect.

## Registered rule and uncertainty

The rule compares each candidate outcome with that task's stored rate. It flags a mean drop of at least 0.15 or an individual drop of at least 0.34, and requires a separate reading excluding stored approval timeouts.

The valid-Intent guard flags harm: C changes from 4/8 ready Intents to 0/1. Its readiness refusal names incomplete coverage, so the result does not justify relaxing the gate. Mean Intent change is -0.110 with approval timeouts retained and -0.177 with them excluded. Hidden all-pass change is zero among available stored grades. Mean landed change is +0.073 or +0.046, below the improvement threshold. B's landed drop is -0.333 with timeouts retained and -0.429 without them, crossing the individual harm threshold only in the latter reading. The registered disagreement override therefore returns **UNRESOLVED**, with the readiness harm flag retained.

Stored grades exist for 43 of 58 compared attempts; the other 15 remain unknown. The held-outs have no valid stored comparator. One attempt per task is a smoke screen, not evidence of equivalence, significance or a causal rescue. All harms remain in the primary accounting.

## Phase score

The same release ran three shape-only attempts on the exact staged export reference inputs. All three stopped with UI presentation questions. There was no Intent to judge: validity **0/3**, coverage **0/41** per attempt, exposure zero, invented requirements zero, essential items missing **22/22**. Both stored arms also produced 0/3 Intents. Their questions concerned imported-access behavior; the candidate's questions concerned presentation. That topic change does not improve the registered outcome. The evaluator-only judge and sealed rubric were unchanged, and no judge call was made without an Intent. Executable mutation separation remains outside this measurement.

Those three attempts consumed 434,009 input tokens, including 366,080 cached tokens, and 3,085 output tokens, with 220.215 seconds of cell wall time. There is no phase-score improvement.

## Witnesses, cost and feedback

The candidate's own logs contain one build, two verification passes and one approved native review. The reviewer made eleven shell calls. There were no wide-review-parts delivery or read-ledger-reset events. Ordinary review was exercised; wide-source overflow, reset and exceptional timeout behavior remain unexercised. Verification here is the older committed component revision, not a later timeout-evidence head; Loop is the committed vendored revision, not the later line-cut head. Exact component SHAs and release hashes are in `data.json`.

All twelve attempts consumed **2,830,910 input tokens**, including **2,404,864 cached input tokens**, and **30,237 output tokens**, including **6,796 reasoning tokens**. Reasoning is already part of output and is not added twice. There were 156 requests; cell wall times total **2,073.703 seconds**, including failed attempts. Dollar cost is unavailable because the subscription model is unlisted. There were no additional model helpers, forks, fresh controls or judge calls. Orchestration-model tokens are unmetered; setup faults, builds, queue waits and grading are retained in the workflow record and are not represented as zero cost.

The committed source dates from 13:32:58Z; the last result was written at 14:47:44.485784066Z: source-head-to-feedback 1h14m46.486s. Registration to last result took about twenty minutes, including preparation and queue waits after registration. The build returned verification feedback 44.689 seconds after `finish`. Individual edit-to-feedback time is unavailable because retained shell arguments are hashed; no edit interval is invented. Grading completed later and does not change the result finish timestamp.

## Disposition

Bounded confirmation, with no adoption or qualified component line. A follow-up may use at most three candidate-only attempts on existing compared tasks that can exercise build and review, with the same stored comparators and unchanged useful gates. Stop after two upstream or infrastructure stops, or the first broken contract. It must resolve the timeout-sensitive reading and retain every harm. No additional model attempts are launched by this pack.

## Rerun

The screened component commits are public: build [`45e455e`](https://github.com/KogenAI/kogen-build/commit/45e455ef8c5be18512e8940a96d39ff0f8eb3d8a), coordinator [`ffca707`](https://github.com/KogenAI/kogen-coordinator/commit/ffca7072fe15303cfe24e50418250bbc909750d4), executor [`e3c1ac8`](https://github.com/KogenAI/kogen-executor/commit/e3c1ac803c2779117ffb75f579e9fc113dab1bb0), review [`cfc2fb2`](https://github.com/KogenAI/kogen-review/commit/cfc2fb29917c9ce667d17ae7e092827641f551fa), setup [`2c226c2`](https://github.com/KogenAI/kogen-setup/commit/2c226c2eb13030abe897aaf4121534c2d0a69842), shaping [`5a0ca3d`](https://github.com/KogenAI/kogen-shaping/commit/5a0ca3dfb7bb340e036c4afcfb8593f5b5bba79e), verification [`11a5244`](https://github.com/KogenAI/kogen-verification/commit/11a5244e95ee730f578cd97cbebdec417b1a2dbe). They were assembled together by the Kogen re-pin candidate `c92d897`; `data.json` records every pin, the vendored loop and both release SHA-256 values that identify the artifacts actually screened.

Recompute the reported outcomes, tokens and both rule readings:

```sh
python3 -I reproduce/kogen-coherent-set-c92d897/report.py reproduce/kogen-coherent-set-c92d897/data.json | diff - reproduce/kogen-coherent-set-c92d897/expected-output.txt
```

New model attempts require the same qualified private task kits and hidden evaluators, which are withheld. The published data supports the descriptive replay, not a public re-creation of those hidden evaluations.
