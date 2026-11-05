# Packet-only localization over the API on 11 fresh cases: issue and failure output with and without the Kogen Context packet

**Verdict: no measurable gain on these cases.** This is the cheap pre-screen of plan kontext-matched-2 (Studio kontext/kontext-matched-2-plan-20261105). Its role is a pre-screen only: it dropped no case and does not enter the screen rule. One claude-sonnet-5-5 call per cell (no tools, no repository access) was asked for up to 6 ranked files to edit, given the issue and the bounded failure output (arm A) or the same plus the frozen kogen-context evidence packet (arm B). 11 cases in 4 stacks (JavaScript 2, Go 4, Rust 3, Ruby 2), 2 repetitions per arm, 44 calls, no call failed.

| Arm | calls | mean recall of reference files (all) | mean recall (source files only) | first file correct (source) | mean input tokens | list cost |
|---|---|---|---|---|---|---|
| A, no packet | 22 | 0.818 | 0.909 | 18/22 | 1929 | USD 0.0947 |
| B, packet | 22 | 0.886 | 0.909 | 19/22 | 3665 | USD 0.1742 |

Paired per case (mean source-file recall, B minus A): up 0, same 11, down 0 of 11 cases. Arm A already names every source file in 10 of 11 cases from the issue text alone (ceiling), so this pre-screen cannot show a localization gain even if one exists on harder cases. The single case neither arm solves is `kogen` (reference files cli/provider/messages.go and respond.go): its packet abstains (0 rows, 334 bytes) and both arms miss. The packet changed only the rank of the first correct file once (bat2201, repetition 1: rank 2 to rank 1), and cost 1.9 times the input tokens. "All" recall includes documentation files in the reference patch (CHANGELOG) that neither arm names; "source" drops documentation-only reference files.

Per case (source recall per repetition, rank of the first correct file; packet bytes):

| case | stack | A recall | A rank | B recall | B rank | packet bytes |
|---|---|---|---|---|---|---|
| axios | JavaScript | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 3050 |
| axios4731 | JavaScript | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 4014 |
| gin405 | Go | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 3390 |
| kogen | Go | 0.00, 0.00 | none | 0.00, 0.00 | none | 334 (abstains) |
| gin3741 | Go | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 4275 |
| gin3820 | Go | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 3503 |
| bat2201 | Rust | 1.00, 1.00 | 2, 2 | 1.00, 1.00 | 1, 2 | 3830 |
| bat2650 | Rust | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 3558 |
| tokio6752 | Rust | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 3374 |
| faker | Ruby | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 3565 |
| jekyll9141 | Ruby | 1.00, 1.00 | 1, 1 | 1.00, 1.00 | 1, 1 | 4371 |

This measures where the packet helps localization only; it runs no build and says nothing about verified outcomes (that is the separate screen of the same plan).

## Source and runtime
Frozen binary kogen-context-build-evidence 0.3.0-failure-evidence, SHA-256 59ee239c2abf96b1737cc809063136fd3334df368ff0637a8b1e6aac7b69f747; packet flags `--deadline 1s --bytes 6500 --ranges 6` (every packet under 1.01 s). Model claude-sonnet-5-5, effort medium, Anthropic API, key anthropic-optimum-tech (running total after the run USD 8.0568), 44 calls, USD 0.2689 list, cap USD 2.
Cases: four DockYard kits (axios, gin405, kogen, faker) from the Kontext build-bench research handoff, and seven public SWE-bench Multilingual instances at their base commits (data/swebench-origins.tsv; e.g. https://github.com/sharkdp/bat/tree/02a9d191ed06e6e37d4e352f12e25e65e8037dd0). Every case is red on base and green on its reference with the hidden check (qualified on the Studio runner). The failure text is each case's red diagnostic, bounded to 4,000 bytes. No source is copied into this pack.

## Rerun
`python3 -I report.py data/results.jsonl` reproduces the tables from the published rows (no network, no key). A fresh run needs the case kits, the frozen binary and an API key in `~/kogen-home-optimum/.kogen/credentials/anthropic.json`: `python3 -I localize_api.py WORKDIR OUT.jsonl` (WORKDIR holds kit/cases, q/<case>-base receipts and bin/kogen-context-build-evidence; the script is the one that produced data/results.jsonl).
