# Declared gaps: short LLM latency probe

- Exact Codex harness Git commit and the original request-launch command are not preserved; the available SHA-256 fingerprints identify snapshots, not commits.
- Kogen is not used, and there is no benchmark task ID or Build outcome.
- The observation channel is Codex CLI JSONL, not provider SSE. It cannot verify provider first-byte or idle-gap limits.
- Fixed order, prompt reuse, cache effects, host, and time are not isolated.
- One request was operationally stopped by the R70 stop condition and remains censored; its latency is not included in completed-request quantiles.
