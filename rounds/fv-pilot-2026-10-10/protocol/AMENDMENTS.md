> Publication copy: account identity and private locations are removed.

# Protocol amendments

## 2026-10-10 — Interpretation of '60,000 total model tokens'

This interpretation was **decided by the operator before any scored trial**.
It applies identically to Lean and Quint, without changing the 900-second or
ten-cycle limits.

The capped total is `(input_tokens - cached_input_tokens) + output_tokens`:
uncached input plus all output. Cached input is excluded from the cap, but
retained in the usage and cost record. The raw total is
`input_tokens + output_tokens`. Each ledger row records input, cached input,
output, reasoning output, capped total and raw total. Cache-write input, when
reported, is also retained; it is already part of input and is not added again.

Codex re-sends the full context each turn. Counting all input would end most
trials after about 5–7 requests, creating a floor effect in both arms. The
earlier toy smoke's FIRST request used 7,767 input tokens. The operator ruled
that the smoke's 5,000-token ceiling likewise means uncached input plus output;
the authorized replacement smoke uses a low test threshold of 3,000.

For the pinned Codex CLI 0.161.0, `reasoning_output_tokens` is **already inside
`output_tokens`** and must not be added. The Responses usage conversion maps
`output_tokens` unchanged and copies `output_tokens_details.reasoning_tokens`
into its separate breakdown. Its parser test has output=10, reasoning=5 and
raw total=110 with input=100. Codex's own `TokenUsage::blended_total()` uses
uncached input plus output. Sources:

- [Pinned usage conversion and parser test](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/codex-api/src/sse/responses.rs#L127)
- [Pinned Codex token accounting](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/protocol/src/protocol.rs#L2426)
- [Official OpenAI reasoning documentation](https://developers.openai.com/api/docs/guides/reasoning), which identifies reasoning as output usage.

Downloaded pinned source evidence is retained privately:
`responses.rs` SHA256 `327127fb7e6886b0ffe73c74c753cc44b2c09e72c090600a861756334397cd2b`,
`protocol.rs` SHA256 `d3d3d384da91b2824c10091de4331a2bc26ec5474887ed0aef1e3f3c4ae110f4`.

The harness monitors cumulative usage in this fresh session's JSON events and
kills the process group at the first report reaching the threshold. Duplicate
stdout/session reports are not summed. Reports arrive atomically after model
requests, so the recorded total can overshoot the threshold; retain the actual
usage and overshoot. Wall time and cycle caps remain independently enforced.
No scored repair trial has run. Historical smoke rows remain append-only under
their recorded earlier token definition; they are not silently reinterpreted.

## 2026-10-10 — Equal initial inputs and shared reporting

No package supplies precomputed checker output, including initial exit summaries,
logs, compiled outputs or counterexample traces. Diagnostics are obtained only
by running a counted check.
Assembly copies authored runtime inputs and an explicit per-arm verification
file allowlist; operator-only initial checker evidence stays in raw/build.

Operator choice (b): strip authored Quint replay to source locations only,
matching Lean. Both backends use bridge/shared/replay.py: one failing evaluation
for F01, or the final failing transition for workflows, with the same sorted
file:line:column format and no authored argument, result or state printing.
Each backend retains its native diagnostics, including native counterexamples.
Quint verify runs at its default verbosity and its complete native stdout/stderr
is displayed without filtering. Lean's emitted #eval FV-COUNTEREXAMPLE records
are authored replay transport, not native diagnostics: they are consumed
privately for source mapping and never printed to the trial agent. Lean's
native error text is preserved verbatim. This clarification was decided by the
operator before any scored trial, after reviewing the first side-by-side output.
This is the smaller change and removes authored causal information without
adding a new diagnostic advantage to either backend. This was decided by the
operator before any scored trial.

Execution is mediated by a root broker with separate agent and checker mount
views. Project setup and test inputs are frozen; grading uses clean trusted
workspaces, validated source exports and compiled inspection with completion
attestations. Host and expected account are explicit launch parameters; US
preparation does not authorize trials or change its Codex configuration.

## 2026-10-10 — Review-fix requalification waiver

The operator waived a second model’s review of the fixes to save time. The supervisor inspected the changes instead, and the full qualification checks were repeated.

## 2026-10-10 — Infrastructure-invalid trials

Infrastructure-invalid trials (the agent could not execute any command) are re-run; their rows are kept.
The four excluded attempts were repeat 2 of tenant access and exact approval, each with Lean and Quint. The command executor was missing from the agent’s execution environment. Correction rows retain the original usage and mark those attempts as infrastructure failures; their artifacts remain archived privately. Replacement attempts used the same scheduled combinations. Valid completed trials were retained. Before restarting, an operational test had to demonstrate command execution, documentation access, a counted check and prevention of bypassing the counted checker. Caps and grading were unchanged.

## 2026-10-10 — Single-host completion

Decided by the operator during the run, for speed:
All 24 valid trials ran on one Hetzner Linux host in Europe, with two virtual CPUs and at most two simultaneous trials, instead of the planned 12 trials in Europe and 12 in the United States. The same harness, readiness approval, Codex binary and account were used for all 24. Schedule rows 13–24 moved to that host and its existing account configuration; the earlier allocation was retained. The United States host ran no trials. Task order, packages, model, effort, caps, checking, isolation and grading were unchanged.
