# Validation

Host: eu. Revision: R3 (AUTHOR-2). Plain validation.

| Language | Base check rc | Base suite tests/failures/errors | Reference check rc | Reference suite tests/failures/errors | Identical repeat passes |
| --- | ---: | --- | ---: | --- | ---: |
| rust | 0 | 29/29/0 | 0 | 29/0/0 | 3/3 |
| go | 0 | 29/29/0 | 0 | 29/0/0 | 3/3 |
| ts-bun | 0 | 29/29/0 | 0 | 29/0/0 | 3/3 |

R3 sandbox operations: 29; leftover=0; zombies=0.
Final suite runs: 15; errors=0; skipped=0; leftovers=0; zombies=0.
Reference repeats: 3 identical final JSON verdicts per language.

| Language | Main suite ms | Repeat suite ms |
| --- | ---: | --- |
| rust | 67139 | 66931, 66883, 66916 |
| go | 67336 | 67299, 67225, 67319 |
| ts-bun | 69841 | 69922, 69995, 70746 |

Final suite total runtime ms: 1017467.
Final suite sandbox total runtime ms: 1060478.

Cleanup proof: planted descendants=3; planted zombies=1; final=0/0; rc=0.
Strict JSON proof: rejected=8; strict type/key proof: rejected=3; rc=0.
Hanging-suite proof: budget ms=15000; runtime ms=13557; tests=29; failures=29; errors=0; rc=0; cleanup=0/0.
Archive restore: files=65; hash mismatches=0; rc=0.
Repositories: base commits=1 each; reference commits=2 each; signature verification rc=0 for all 6; dirty trees=0.
Suite alarm seconds: 60; SPEC per-test contract seconds: 45.
SPEC changed: true; prompts changed: true (committed-storage isolation); stack notes changed: false.
Difficulty notes changed: false.

Loaded-run courtesy check: running bench-c4* units=1.
Loaded determinism: 0/5 per reference; skipped because a bench-c4* unit was running; loaded runs pending.

## SHA-256

| File | SHA-256 |
| --- | --- |
| SPEC.md | 6722d7bc3ef34b0fe2a30fa867fe139db172bb003248429cc38debdff845319b |
| prompt-rust.md | 5553b1862084ebd27de551ac38789bca6419431bf5008b4ff30e6a654ceb91dc |
| prompt-go.md | e957488a14013cd7866048bd11fd1c907be50eb364bad2d50e2e64e28a3c8841 |
| prompt-ts-bun.md | 07d9d1a9087c2cd4938ddccaef07e5f66e106bca9aa12c13dd1d0ec91c169e2e |

Evidence: author/validation-results.jsonl; author/proof-guards-R3.jsonl; author/courtesy-R3-final.json; author/repositories.json; author/restore-proof-R3.json.
Full external ASTRA review + one AUTHOR-2 fix round + targeted R3 recheck; writer=primary GPT-6; reviewer=gpt-6.1-sol high.
