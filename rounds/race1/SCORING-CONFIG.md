# Race 1 scoring configuration

- Suite: v1.3.1, 283 cases; raced base references are in `README.md`.
- Inputs: exact spec/suite copies supplied to arms, read-only; apply the amend-1 patches when public.
- Invocation: `bin/kogen-conformance run --kogen /path/to/kogen --jobs 4 --run-timeout 60 --out results.jsonl`.
- Runner behavior: pinned tool PATH without shims; process group per invocation; clean each case work directory; four cases concurrently; 60 seconds per invocation.
- Official-v2 finals: score one arm at a time on a quiet machine with the shim-free PATH. Superseded scoring rows remain labelled in `scores.tsv`.
- Checkpoints: T+10, T+20, T+30, T+40, T+50, FINAL. Source code snapshots remain private.
