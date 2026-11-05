# Packet-only localization over the API: issue and failure output with and without the Kogen Context packet

**Verdict: unresolved.** One claude-sonnet-5-5 call per cell (no tools, no repository access) asked for up to 6 ranked files to edit, with the issue and bounded failure output (arm A) or the same plus the frozen kogen-context evidence packet (arm B). Four decision cases, 2 repetitions per arm. This measures where the packet helps localization only; it does not run a build and says nothing about verified outcomes.

| Arm | scored calls | mean recall of reference files | mean precision | first file correct | mean input tokens | list cost |
|---|---|---|---|---|---|---|
| A, no packet | 8 | 0.688 | 0.348 | 4/8 | 2169 | USD 0.0418 |
| B, packet | 7 | 0.857 | 0.39 | 7/7 | 3827 | USD 0.0675 |

Per case (recall per repetition, rank of the first correct file):

| case | arm | recall | first-hit rank |
|---|---|---|---|
| rg-ignore | A | 1.00, 0.00 | 3, None |
| rg-ignore | B | 1.00, 1.00 | 1, 1 |
| ripgrep | A | 0.50, 0.50 | 2, 2 |
| ripgrep | B | 0.50, parse error | 1 |
| gin | A | 0.75, 0.75 | 1, 1 |
| gin | B | 0.75, 0.75 | 1, 1 |
| axios-timeout | A | 1.00, 1.00 | 1, 1 |
| axios-timeout | B | 1.00, 1.00 | 1, 1 |

The packet moved the first-hit rank to 1 in every scored B call (A: 4 of 8), mostly by fixing rg-ignore repetition 2 and ripgrep, and left gin and axios-timeout unchanged. One B call (ripgrep, repetition 2) returned unparseable JSON and is excluded from B's scored calls (7 of 8). With 4 cases and 2 repetitions this is a descriptive pilot; reference files include documentation files that neither arm can be expected to name (ripgrep CHANGELOG, gin README). The failure text is the case's red diagnostic, bounded to 4,000 bytes.

## Source and runtime
Frozen binary kogen-context-build-evidence 0.3.0-failure-evidence, SHA-256 59ee239c2abf96b1737cc809063136fd3334df368ff0637a8b1e6aac7b69f747; packet flags `--deadline 1s --bytes 6500 --ranges 6`; cases and plan from kontext-matched-1. claude-sonnet-5-5, effort medium, Anthropic API. Total 16 calls, USD 0.12 (cap USD 5).

## Rerun
`python3 -I report.py data/results.jsonl` reproduces the table from the published rows. A fresh run needs the case kits and the frozen binary (see the kontext-matched-1 plan): `python3 -I localize_api.py KITDIR OUT.jsonl`.
