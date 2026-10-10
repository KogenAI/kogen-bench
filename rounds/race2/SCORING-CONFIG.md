# Race 2 scoring configuration

- Suite: frozen generated 144-case suite, input tree prefix `784e6599908f2eeb`; include all 30 SPEC-BUG cases in the primary denominator.
- Inputs: shared Quint + Gherkin spec at `race2/spec/` and suite at `race2/suite/`; copies were read-only during the race.
- Invocation: `suite/bin/kogen-conformance run --kogen /path/to/kogen --jobs 4 --timeout 60 --out results.jsonl`; summarize with `suite/bin/kogen-conformance summary results.jsonl`.
- Runner behavior: shim-free pinned environment, per-invocation process groups and cleanup, four cases concurrently, 60-second invocation bound.
- Checkpoints: T+10, T+20, T+30, T+40, T+50, FINAL. Completed Race 2 and Race 2S final scores were produced with arms in parallel; Race 2B stopped after 15 minutes 20 seconds; only its ten-minute checkpoint scores were retained. Source code snapshots remain private.
