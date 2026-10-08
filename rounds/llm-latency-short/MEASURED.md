# Measurement contract: short LLM latency probe

Endpoint: client-visible stdout and Codex JSONL event arrivals; end-to-end wall from before sandbox/launcher startup. It is not provider SSE timing.

| Phase count | n | Definition |
|---|---:|---|
| Scheduled request capacity per round | 36 | Six model/effort arms × three probe labels × two hosts. |
| Started requests | 77 | `request_end` records in the two raw event logs. |
| Terminal request records | 77 | Includes the one operationally censored request. |
| Uncensored completed requests | 76 | Eligible for completed-latency quantiles. |
| Graded / ITT | 0 / not applicable | This was an unscored timing probe without task-success outcomes. |

Quantiles use linear interpolation. The exact per-arm aggregation command and input hashes are in [README.md](README.md) and [reproduce.py](reproduce.py).
