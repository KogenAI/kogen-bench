# Declared gaps: long-reasoning latency probe

- Exact Codex harness Git commit and historical request-launch command are not preserved; available SHA-256 fingerprints identify snapshots, not commits.
- Kogen is not used, and there is no benchmark task ID, grade, or Build outcome.
- A collector fault left one request incomplete; six later planned requests were never started.
- The observation channel is Codex CLI JSONL, not provider SSE. Provider first-byte and token-idle distributions are unavailable.
- Fixed order and repeated prompts confound model, effort, prompt, and cache effects; no causal arm comparison follows.
