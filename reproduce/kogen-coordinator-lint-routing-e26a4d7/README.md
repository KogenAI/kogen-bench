# Coordinator validation feedback screen

Verdict: **UNRESOLVED**. The changed head remains unqualified. All three candidate attempts finished and were hidden-graded.

The coordinator changes how Intent validation reports multiple errors, adds
Bundler/Rails project detection, and introduces a routing API. The task harness skips project initialization,
so Bundler detection has model-free coverage only. Revised contract
and golden checks pass. The changed feedback prevents a model-free equivalence
claim. The routing API is not imported by the build component in the release
used here, so these task attempts cannot validate its integration.

## Comparison

Candidate: released Kogen 6e69ffb3, with only coordinator e26a4d7 overridden.
Companion components retain that release's pins. Comparison: stored adopted
573d023 attempts at the same model and effort. Newer release changes are a
confound; a task improvement would be a package observation.

Three candidate-only tasks, one attempt each. Shape, build and review all use
gpt-6.1-terra medium through native Loop / ChatGPT. The screen shares release
bundles and the execution queue with the verification follow-up. No fresh control
was run. This sample is a smoke screen, with no significance or equivalence claim.

## Source

The landed change set is 8d24cc7, 741ddac, ffca707 and e26a4d7, after qualified
656694f. Public source remains in its repositories; this pack contains data,
report scripts and commit references, with no source files or source patches.

- [Qualified coordinator base](https://github.com/KogenAI/kogen-coordinator/tree/656694f4b3ef0a982691cabcce8b924ec77eeee9)
- [Coordinator candidate](https://github.com/KogenAI/kogen-coordinator/tree/e26a4d75cdcc3bbcd6d900f2698cac8144bfdc19)
- [Released assembly source](https://github.com/KogenAI/kogen/tree/6e69ffb3243603cd5cd9253efd418a0c24130583)

Every component source link, artifact digest and toolchain is in runtime.json.
model-free.json records the four changed golden outputs, source identity and
98/124 passing targeted test/subtest events at base/head. Git-commit fixtures
were excluded because they override identity/signing/hook configuration.

## Rerun

Named patch: the landed coordinator change set above, referenced by public
commits. No source patch is distributed.

Recompute the golden comparison directly from the public commit files:

```sh
python3 replay.py
```

Read the captured comparison without network access:

```sh
python3 replay.py --offline
```

Rebuild the coordinator-only candidate from the public release source (Go 1.27.3):

```sh
git clone https://github.com/KogenAI/kogen.git kogen
git -C kogen checkout 6e69ffb3243603cd5cd9253efd418a0c24130583
git clone https://github.com/KogenAI/kogen-coordinator.git kogen-coordinator
git -C kogen-coordinator checkout e26a4d75cdcc3bbcd6d900f2698cac8144bfdc19
cd kogen/cli
go mod edit -require=github.com/KogenAI/kogen-coordinator@v0.0.0-29990101000000-e26a4d75cdcc -replace=github.com/KogenAI/kogen-coordinator=../../kogen-coordinator
GOWORK=off CGO_ENABLED=0 go build -mod=mod -trimpath -buildvcs=false -o ../../kogen-candidate .
```

The temporary candidate version sorts above all companion requirements. Keep
all companion release pins and commit no module replacement. Local replacement
paths in Go build metadata can change the binary digest after reconstruction;
record the exact source tuple and toolchain as well as the new digest.

The production test command at each coordinator revision was:

```sh
go test -count=1 -buildvcs=false -json ./project ./contract \
  -run 'Test(CheckIntentRules|IntentCheckMatchesElixir|IntentReadMatchesElixir|Detect.*|GoldenIsCurrent|GherkinMatchesElixir|ParseModelSpec|RouteCycleAndResume|Cycle.*|Resume.*|Resumed.*|StagesAreThePersistedNames)$'
```

At candidate head, add `./route` to the package arguments. Default Go timeout;
Go 1.27.2. Tests resolve the upstream Loop commit c6e2360 through a temporary
workspace. No committed module replacement is required.

To repeat the paid screen, reconstruct the candidate from runtime.json with the
public `cand-assembly.sh` harness and replace only the release's binary/version
stamps. Use the existing qualified tasks named in results.json, one candidate lane,
three planned cells, one slot, and unchanged 3600-second deadline. The counted
command after build/plan/preflight, release and task checks, and normal admission:

```sh
python3 "$LANES_DIR/bin/lanes-run" "$RUN_DIR" \
  --tasks "$TASKS_DIR" --hosts "$RUN_DIR/hosts.json"
```

Stop after three cells, two apparatus failures, or one hour from first launch.
Never start a new control. Stored kit digests were not recorded historically;
input identity and host/load gaps must be disclosed. A new stochastic draw may
not reproduce these task outcomes. Missing natural lint/detection/routing triggers
leave those mechanisms unresolved even when task attempts complete normally.

## Results and costs

| Task | Stored outcome | Candidate outcome | Valid Intent old/new | Hidden whole-task pass old/new |
| --- | --- | --- | --- | --- |
| Account cleanup | landed | build_blocked | yes/yes | no/no |
| Sweep performance | refused | landed | no/yes | no/no |
| Comment reactions, held-out | refused | questions_pending | no/no | no/no |

All three assigned tasks remain in the primary result. Candidate grader totals
were 3/8, 10/11 and 3/9, with complete grading and no whole-task grading
infrastructure error. Acceptance separation is not established: the task copies
lack reference trees for the separate shape matrix. That gap is distinct from
completed final-tree hidden grading.

The first outcome worsened from landing to a protected-baseline stop: its shaped
acceptance invokes Rails without preparing an isolated database, while protected
setup is empty. Source inspection supports that missing precondition; the
builder's missing-table claim was not independently rerun. The second attempt
reached a valid Intent and landed, while its stored counterpart stopped at shaping
without tool use. The held-out attempt asks a UX question about anonymous visitors
adding reactions, while the stored attempt stopped without tool use. A UX question
is not classified here as a product defect. All three first differences are
neighboring shaping/acceptance behavior; none has a changed-lint witness.

No changed-lint output appears in retained own logs. Initialization is skipped,
and the released build does not import the new routing API. These task results
therefore establish neither efficacy nor equivalence for those changed paths.
The result is a three-task package smoke, not evidence of a causal rescue.

Last cell result timestamp: 2026-11-03T17:18:45.645151587Z. Candidate walls including
failed attempts: 433.920, 334.099 and 46.002 seconds (814.021 total). Measured input,
cached input and output: 1,523,329 / 1,295,488 / 13,579 tokens. Reasoning tokens
are a subset of output and are not added twice. Subscription pricing and separate
helper orchestration tokens are unavailable, not zero. One native candidate build
passed in 14.468 seconds; targeted base/head tests passed. One failed setup attempt
found already-deleted shared build inputs before any build/model call; fresh exact
inputs were fetched. Build/test/source inspection trees were then deleted.

Disposition: **bounded confirmation**. Require a retained natural lint-refusal case
and matching stored adopted comparison before any next cells; at most two
candidate-only Terra-medium cells and one hour total. Stop if the changed feedback
never fires. No further cells in this job; retain the previous qualified endpoint.

The saved descriptive task table can be recomputed without models or grading:

```sh
python3 report.py results.json
```
