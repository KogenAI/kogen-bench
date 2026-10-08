# L6: scoped-auditor replay

## Status

**VALID**

### Why not VALID
- None: the README documents a pre-result registration, execution under its rule, reconciled denominators, recomputable results, matched conditions, and retained evidence.


STATUS: **VALID**

## Required reproduction metadata

- Kogen commit: not applicable; no Kogen benchmark harness or implementation was run.
- Harness commit: not recorded as a Git commit; the public runner fingerprints are SHA-256 values, not Git commits.
- Model and effort: `gpt-6-luna` at max and `gpt-6-sol` at low.
- Task IDs: see the 40-case roster and exact case IDs in `data/case_list.csv`.
- Historical execution command: the recorded `codex exec` command template appears below; exact private task and patch inputs are withheld.
- Raw records: `data/case_list.csv` and `data/calls.csv`; the scoring script is `reproduce/score_l6.py`.

Evidence links: [H67 — scoped reviewer veto](../../hypotheses/f06-checks-review-recovery.md); [F06 findings summary](../../FINDINGS.md#f06-checks-review-and-recovery); claim `CL-L6-AUDITOR-ADVISORY-REPLAY` (**STATUS_ONLY**).

| Lifecycle field | n | Basis |
|---|---:|---|
| Planned requests | 80 | 40 frozen cases × two auditor models. |
| Started requests | 80 | One call-ledger row per request attempt. |
| Finished requests | 80 | All calls have terminal status, including one timeout. |
| Official benchmark grades for auditor calls | 0 | Not applicable to these requests; they do not produce official benchmark grades. |
| Requests with valid auditor verdicts | 79 | 79 requests returned a valid verdict; one timeout has none. |
| ITT denominator | 0 | Offline patch audit; no live Build outcome population. |

The 40 source cases each retain their original official benchmark outcome. Those source-case grades are not grades of the 80 auditor requests.

Pre-registered: yes; design fixed 7 October 2026 before auditor calls, with the small-diff cutoff amended before calls after the sourceable pool had no diffs ≤100 changed lines.
Label: EXPLORATORY
Question: Can a frozen request-scoped auditor veto bad patches with precision ≥0.90 and false-demotion rate on good patches ≤0.05, the targets in Rust Kogen spec §3.8.2?
n: 40 officially graded r70 contestant patches (20 hidden PASS, 20 hidden FAIL); two auditor models; 80 attempts.
Headline: Neither model met both targets; both remain advisory only.
Configuration: Codex `gpt-6-luna` at max and `gpt-6-sol` at low, with the same frozen request-scoped prompt and only one public task prompt plus contestant diff per call. Cases are blinded and balanced by outcome and host. Luna C01–C08 ran serially; Luna C09–C40 and all Sol requests ran in groups of up to four independent invocations. No tool events occurred. One Luna request timed out without a verdict or usage record; it is counted as allow for the confusion matrix and reported as an invalid response.
Limit: Offline patch-level replay, not a live gate; it omits test-source and failure-output inputs used by the in-rung test auditor. Small selected r70 sample; Wilson 95% intervals are reported. A “small diff” is ≤250 changed lines; the sourceable pool had none ≤100, and the final sample contains two PASS and three FAIL cases within 250 lines. One request lacked a verdict and usage.
Sources: Rust spec §3.8.2 at commit [`1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0`](https://github.com/KogenAI/kogen-ex/commit/1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0); [decision rule](DECISION-RULE.md); [results](RESULTS.md); [case ledger](data/case_list.csv); [call ledger](data/calls.csv).

## Reproduce

Kogen implementation commit: not applicable; no Kogen benchmark harness or implementation was run. Spec commit: [`1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0`](https://github.com/KogenAI/kogen-ex/commit/1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0). Codex CLI: `codex-cli 0.160.1`; scoring runtime: Python `3.9.6`. The call runner selected the operator’s dedicated billing profile through `CODEX_HOME`.

Offline runner fingerprints (SHA-256): `run_l6_auditors.py` d236824a065cd4d5af3e083ce59ab974b5accf28d9b6c118426980f99e3079c3; `execute_l6_reserved.py` e2fe3f7c1c3950ac5b536228dea44535476919b99189e39fcf724e49087606d4; `execute_l6_parallel.py` 1355878d9f1d79aeebad3ac534dd39261f6e2889dfa3629bd9572bbf873392fd. The public scoring script is `reproduce/score_l6.py`.

Task IDs in the frozen case roster: r70-1-elixir, r70-1-go, r70-1-ts-bun, r70-2-elixir, r70-2-ts-bun, r70-3-elixir, r70-3-rust, r70-4-elixir-fe2, r70-4-go, r70-4-rust, r70-4-ts-bun, r70-4-ts-bun-fe2, r70-5-elixir, r70-5-gleam, r70-5-go, r70-5-rust, r70-5-ts-bun, r70-6-elixir, r70-6-gleam, r70-6-go, r70-6-rust, r70-6-ts-bun, r70-7-elixir, r70-7-gleam, r70-7-rust, r70-7-ts-bun, r70-8-go-v2, r70-8-rust, r70-8-rust-v2. Exact per-case IDs and outcomes are in `data/case_list.csv`.

Frozen auditor prompt template (provenance: Rust spec §3.8.2 at the linked commit):

> You are the scoped build auditor. You have no tools. Judge only whether the candidate patch below satisfies the explicit requirements in the public Request. Do not use external sources, infer hidden tests, or assume requirements absent from the Request. Veto only for a concrete missing requirement, contradiction, or behavior outside the requested scope. If the Request and patch do not establish a concrete reason to reject the patch, allow it; uncertainty means allow. Return exactly one JSON object with `verdict` (`veto` or `allow`), `reason_class` (`missing_requirement`, `contradiction`, `scope_violation`, `unsupported_behavior`, `none`, or `uncertain`), and a brief `reason` based only on the Request and patch. Do not mention tests or outcomes.
>
> Request: `{public prompt.md}`
> Candidate patch: `{patch.diff}`

The call command template used one blinded case per fresh `codex exec` invocation in an empty temporary directory:

```sh
EMPTY_CWD="$(mktemp -d)"
codex exec --disable shell_tool --disable apps --disable multi_agent --disable remote_plugin --disable web_search \
  --sandbox read-only --skip-git-repo-check --ephemeral --json --cd "$EMPTY_CWD" \
  -m gpt-6-luna -c model_reasoning_effort=max -
```

For Sol, use `-m gpt-6-sol -c model_reasoning_effort=low`. The runner passed the public task prompt and patch diff on stdin; those private inputs are withheld. Token total is uncached input + cached input + output. Public files: `data/case_list.csv`, `data/calls.csv`, and `reproduce/score_l6.py`.

Reproduce the public metrics with:

```sh
python3 reproduce/score_l6.py --cases rounds/l6-auditor-replay/data/case_list.csv --calls rounds/l6-auditor-replay/data/calls.csv
```
