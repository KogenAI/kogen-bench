# Build main head: paired release screen

Four matched request-only tasks compared a release with the same release assembled with the later main head of its build component. Both arms used gpt-6.1-terra medium in every role, one attempt per task and arm, with 3,600-second deadlines and no retries. Two tasks targeted retained build-stage stops, one was a smoke check and one was a previously passing guard. Each pair ran on the same host; the first three pairs ran sequentially on a single slot, and the guard ran concurrently on two slots.

Both arms of each targeted pair stopped in shaping without a valid Intent or landing, with hidden all-pass false. On the smoke task, the control had a valid Intent and landed while the candidate stopped in shaping; neither passed all hidden checks. On the guard both had valid Intents and landed, and neither passed all hidden checks. The candidate-worse smoke outcome is **tentative** at one pair and occurred before the changed build stage; it does not establish a build regression. No explicit no-edit or skip-verification lever marker was found in the candidate guard's own logs, which does not prove the mechanism did not execute. Acceptance separation was not established.

All attempts, including failures, are included in wall and token totals. Dollar prices are unavailable for this model; zero-valued placeholders are not evidence of zero cost. The candidate was built with Go 1.27.3; compiler differences from the published release remain a limitation. These observations do not establish a correctness rescue or a causal speed change.

The disposition is bounded confirmation: at most four candidate-only cells on existing qualified tasks against matching retained release cells, stopping after two upstream shaping stops or one attributable build-stage harm. This screen is not an adoption gate.

The original per-cell logs, grade files and final trees were inadvertently deleted after the summary data was extracted. The preserved data file contains the recorded outcomes, aggregate grades, timing and tokens; the raw traces cannot currently be independently audited.

## Rerun

The change is the full build range from [release pin](https://github.com/KogenAI/kogen-build/commit/b9990a3d090306d79e28ac0d858ba47c8f3b0ed4) to [main head](https://github.com/KogenAI/kogen-build/commit/2e10d934cac2a523165a22db13786afbbf42f165), applied as a single component override to [the release source](https://github.com/KogenAI/kogen/tree/41d70052bf0ff932a0424df86a0fb388021428fc). In a scratch copy, use `go mod edit -replace=github.com/KogenAI/kogen-build=<build-main-head-dir>`, keep the other modules at the release pins, build the Linux binary with `CGO_ENABLED=0 go build -trimpath -buildvcs=false`, and insert it into a copy of the verified release archive. Confirm the module list, release setup, qualified tasks and admission before running request-only matched pairs with one repetition and a 3,600-second deadline. Hidden graders and account credentials are not included here.

Control archive SHA256 `804016fb34837f60b7269f92aa364053beeba1c87d0831da7faf46b9117b5fdb`; candidate binary `00f1946bff818fe00682fbe6775f432aa6d8e66a96d940e27e6fd023bf24183e`; candidate archive `0a9011babd9ffcf4cdaffa261be1d97fb35b003efda4a0f0b7811a9b8c3ecaf5`. Reproduce the recorded summary with `python3 report.py`.
