# Verification caller cancellation follow-up

**UNRESOLVED:** one landed attempt and two shaping stops; no natural caller-cancellation witness.

The change makes running verification commands observe caller cancellation in ordinary steps, approval steps and feasibility probes. It also preserves an existing session interruption when cancellation races it. Public documentation changed afterward without changing production Go code.

The first six commits in this range were already screened in [the timeout-evidence finding](https://bench.kogen.dev/findings/kogen-verification-timeout-evidence-5070052/). That unresolved result is retained. This follow-up uses the newest released assembly available at staging, with verification alone overridden to the new head. Other assembly changes relative to the stored adopted release mean task differences are package observations, not isolated causal effects of cancellation.

## Source and model-free checks

- [Kogen release source](https://github.com/KogenAI/kogen/tree/6e69ffb3243603cd5cd9253efd418a0c24130583).
- [Verification candidate source](https://github.com/KogenAI/kogen-verification/tree/f0884fde435ad9d59f9c882b17b93b48ce5dfeeb).
- [Cancellation change](https://github.com/KogenAI/kogen-verification/commit/c025c694888d933e851664df7937c0a535234425).
- [Previous range endpoint](https://github.com/KogenAI/kogen-verification/tree/fb288e6ce4edbbcaf6426ca7f8e8d6de9cf76e47).

Targeted verification contracts and goldens passed at the previous range endpoint (230 test/subtest events) and candidate (244), with no skips or failures and unchanged default timeouts. These fresh checks used Go 1.27.2. The earlier screened intermediate head also passed 244 events. Every tracked input matched its named commit. Existing golden JSON bytes are unchanged; exceptional feedback, resource routing and command custody change, so this is not model-free equivalence. The cancellation acceptance driver is separate from ordinary Go tests and is not claimed exercised by this test pattern.

The candidate compiled with Go 1.27.3, recording the tuple and artifact digests in candidate.json. The task screen is candidate-only: one attempt on each of two process/approval targets and one held-out task, full pipeline, gpt-6.1-terra medium in shaping, building and review, through native Loop on the ChatGPT subscription route. Comparisons are stored adopted-release attempts at the same model and effort. No fresh controls or synthetic cancellations were run. Historical per-cell kit fingerprints are unavailable; current request/config hashes are checked separately. Git versions and host-time differences are reported as comparison limits.

## Rerun

Patch under test: the public cancellation commit linked above, included in verification head f0884fd. This pack contains data, report code and source commit references. It contains no component source or source patch.

In a new scratch directory, with Go 1.27.3 installed, reconstruct the candidate from public source:

```sh
git clone https://github.com/KogenAI/kogen.git kogen
git -C kogen checkout 6e69ffb3243603cd5cd9253efd418a0c24130583
git clone https://github.com/KogenAI/kogen-verification.git kogen-verification
git -C kogen-verification checkout f0884fde435ad9d59f9c882b17b93b48ce5dfeeb
cd kogen/cli
go mod edit -require=github.com/KogenAI/kogen-verification@v0.0.0-29990101000000-f0884fde435a -replace=github.com/KogenAI/kogen-verification=../../kogen-verification
GOWORK=off CGO_ENABLED=0 go build -mod=mod -trimpath -buildvcs=false -o ../../kogen-candidate .
```

The temporary requirement sorts above requirements of companion components; no replacement is committed. Other component versions stay at the released pins. Replacement paths in Go build metadata can make a rebuilt artifact hash differ; the named source tuple is the reproducibility identity. No model calls are made by this command. Repeating stochastic task outcomes also requires the same separately qualified tasks, hidden graders, existing authenticated provider and the public lanes harness; a rebuild alone does not reproduce task scores.

Recompute the recorded descriptive result:

```sh
python3 -I reproduce/kogen-verification-caller-cancellation-f0884fd/report.py reproduce/kogen-verification-caller-cancellation-f0884fd/evidence.json | diff - reproduce/kogen-verification-caller-cancellation-f0884fd/expected-output.txt
```

That report recomputes saved measurements; it does not rerun models or hidden grading. Task timings include failed attempts. Subscription dollar pricing and separate orchestration-model token counts may be unavailable and are never treated as zero. A small screen with no natural cancellation cannot establish that cancellation improves repair outcomes.

## Final results

**UNRESOLVED.** All three candidate attempts completed and were graded without a hidden-grading infrastructure error. Hidden whole-task pass is 0/3 against stored 0/3; one valid Intent in each cohort. No whole-task or valid-Intent discordance supports a cancellation rescue. The performance task changed from refused to a workload-target question: a shaping/class-b stop before verification, not a cancellation effect. The held-out task retained the three-no-tool-turn refusal. The landed task remains hidden-red despite acceptance and review passing; separating acceptance is not independently established.

| Task | Stored → candidate | Valid Intent old/new | Hidden all-pass old/new | Hidden grade candidate | Cause |
| --- | --- | --- | --- | --- | --- |
| T1 | landed → landed | yes/yes | no/no | 5/8 | completed, class e |
| T2 | refused → questions_pending | no/no | no/no | 10/11 | shape, class b |
| T3 | refused → refused | no/no | no/no | 3/9 | shape, class b |

Every row configures shaping, building and review as gpt-6.1-terra / medium / native Loop / ChatGPT; only shaping executes on T2/T3. Candidate walls including failures: 538.27, 60.263, 65.693 seconds. Input 1,167,987, cached input 1,021,952, output 12,159 tokens. Subscription dollar pricing unavailable, not zero. Preparation and unmetered orchestration limits are in workflow-cost.json.

Own run logs contain 4 step_sweep events; no natural caller cancellation or exceptional timeout diagnostic. No synthetic trigger was induced. Current request/config hashes match retained copies; historical per-cell fingerprints are unavailable. Candidate and stored Git both 2.43.0, different Linux machines/times. These package observations do not establish component efficacy or equivalence.

Disposition: **bounded confirmation**. Require a naturally triggered retained cancellation/timeout case and matching stored adopted comparison before another candidate-only Terra confirmation; at most two candidate cells or one hour, stop on first contract failure or two upstream/instrument stops. If no matching natural case exists, run no more cells and retain UNRESOLVED. This is not a release gate or a reason to hold a passing release. No qualified line.

Finished at 2026-11-03T17:03:04.248838441Z (last result.json filesystem mtime; ledger seconds 2026-11-03T17:03:04Z). No new cells after the two upstream stops; the already-running Build was allowed to finish.
