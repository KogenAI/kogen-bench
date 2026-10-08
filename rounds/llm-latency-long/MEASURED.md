# Measurement contract: long-reasoning LLM latency probe

Endpoint: client-visible stdout and Codex JSONL event arrivals; end-to-end wall from before sandbox/launcher startup. It is not provider SSE timing.

| Phase count | n | Definition |
|---|---:|---|
| Maximum planned requests | 24 | Four model/effort arms × two prompt labels × three repetitions. |
| Started requests | 18 | Raw `request_start` and `request_end` records. |
| Terminal request records | 18 | Includes one collector-fault record. |
| Uncensored completed requests | 17 | Eligible for completed-latency summaries. |
| Requests not launched | 6 | Remaining slots from the maximum planned schedule after the collector stopped. |
| Graded / ITT | 0 / not applicable | This was an unscored timing probe without task-success outcomes. |

The output summaries are reconstructed by [reproduce.py](reproduce.py) from the [raw event log](raw/round2-eu-20261006T014516Z.jsonl).
