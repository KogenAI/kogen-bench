# LLM latency probe: short prompts

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first request is documented.
- **CONDITIONS_MISMATCH:** Fixed order, prompt, cache-warming, host, and minute effects are not separated.
- **relabelled 2026-10-08 after scrutiny:** Previously labelled VALID; the README describes only confounded client-visible timing.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **DESCRIPTIVE** — DESCRIPTIVE; unscored client-visible timing only.

This round measured event arrival through the Codex CLI JSONL interface. It did not measure provider SSE, task correctness, Build success, or a Kogen intervention. Startup and sandbox time are included in request wall time.

## Observations

The source records 77 request attempts: 76 completed uncensored and one stopped when the R70 stop condition fired. There were no provider or collector errors. Six model/effort arms were sampled in fixed order on the US and EU venues.

| Model | Effort | Attempts | Uncensored complete | First stdout byte p50 / p90 (s) | Total wall p50 / p90 (s) |
|---|---|---:|---:|---:|
| `gpt-6-luna` | medium | 15 | 15 | 0.723 / 1.363 | 5.416 / 7.256 |
| `gpt-6-luna` | high | 14 | 13 | 0.708 / 0.987 | 5.331 / 6.722 |
| `gpt-6-luna` | xhigh | 12 | 12 | 0.653 / 0.939 | 6.820 / 8.216 |
| `gpt-6-luna` | max | 12 | 12 | 0.670 / 1.021 | 7.116 / 8.266 |
| `gpt-6.1-sol` | medium | 12 | 12 | 0.922 / 1.149 | 6.973 / 7.958 |
| `gpt-6.1-sol` | high | 12 | 12 | 0.738 / 1.002 | 7.342 / 8.902 |

These are descriptive distributions from a short fixed-order window. Arm, prompt, cache-warming, host, and minute effects are not separated. First stdout byte and client-visible JSONL events do not establish provider first-byte or token-idle times. No latency ranking or production cap validation follows.

## Reproduction record

- **Kogen commit:** not applicable; the probe called Codex directly and did not run Kogen.
- **Harness Git commit:** not present in the public record. The source-reported Codex harness snapshot fingerprint is `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`; it is a SHA-256 fingerprint, not a Git commit. The source-reported probe fingerprint is `567eb558abbb9a33145c1063090ee52a65429f5e5970ba4beffd48175bf6e98a`. Both are recorded in [provenance.json](provenance.json).
- **Model and effort:** `gpt-6-luna` at medium, high, xhigh, and max; `gpt-6.1-sol` at medium and high.
- **Task IDs:** no benchmark task IDs were assigned. The exact probe labels are `P-short`, `P-reason`, and `P-tool`.
- **Historical request launch command:** not preserved in the public record. The public analysis command is `python3 rounds/llm-latency-short/reproduce.py` from the repository root.
- **Raw records:** [US event log](raw/us-20261005T223819Z.jsonl), SHA-256 `0d6a2e25b7a828b7ba82122c5e70842aa0aae34230df7cb2ffca9e89f9abb4d5`; [EU event log](raw/eu-20261005T223815Z.jsonl), SHA-256 `5a3af05c1f3105d3e60419c02a538ddf7566f2fd815b45042c082ea29563fc23`. Logs retain event types, numeric measurements, timestamps, and probe labels; they contain no prompt or response text.

The summary command recalculates arm counts and quantiles from the raw records. Replaying the historical requests requires runner and runtime details that are not in this public snapshot.
