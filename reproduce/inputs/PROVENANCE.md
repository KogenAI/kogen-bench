# Outcome extract provenance

The official outcome source location is withheld. Source-reported SHA-256: `eb766d9070975d53ee03d0cdb1ba4fc3916c97f3a5a9dc70549f06b6338a55ea`. The source report lists 4,892 ledger rows before duplicate reconciliation; its source file is not included, so that fingerprint and extraction are not independently verifiable.

Sanitized public input: [`grades.final.jsonl`](grades.final.jsonl), SHA-256 `4d639a3848b3661dcb5646630b6a4914e5053ff4b94ab029424d47d040e3c977`. This is the refreshed 2026-10-07 export. Only outcome, arm, task, repetition, venue, and time identifiers are retained. Grader diagnostics, failure lists, patches, host details, and identity fields are withheld.


The sanitized input also includes 29 official R70 extension grades, latest per exact cell ID. Public arm labels are the four language stacks. Per-cell wall and input, cached-input, and output token totals are retained in numeric metadata; unknown cost remains null. Admission controls and task-8 smoke outcomes are not scored rows.

## Round 70 completeness evidence

The following sanitized inputs support the descriptive RvE and timing tables. They are numeric or categorical extracts from the approved Round 70 evidence sources; raw host paths, user identities, command text, private patches, and grader diagnostics are omitted.

- `r70-original-own-checks.jsonl` contains only the latest recorded own-check status for the 40 original RvE cell IDs, joined to the official public test-count ledger.
- `r70-original-resource-receipts.jsonl` contains 20 scored Rust/Elixir RvE resource receipts: model/effort, harness version/fingerprint, host, token counters, wall, and source-reported API-equivalent cost with its price-table and calculator hashes.
- `r70-original-excluded-resource.jsonl` contains numeric resource accounting for five ungraded deliveries, with anonymous delivery labels. These are separate from scored outcomes; the approved summary does not carry their price-table or calculator hashes.
- `r70-native-diagnostic-samples.jsonl` contains 45 per-repetition measurements for tasks 1, 4, and 6 across five stacks: cold build, incremental build, full check, and hidden-wrapper timing. `r70-completeness.py` computes the median and range tables.
- `r70-compile-host.json` contains the reported compile-host CPU/RAM/kernel fields and 75 pre-cold 1-minute load samples. The host snapshot and median load paragraph are recomputed by `r70-completeness.py`.
- `r70-transcript-share-samples.jsonl` contains 108 sanitized per-cell timing totals for the original r70 transcript wall diagnostic. It has no cell IDs or command text; the script computes command shares and quartiles.

The 44 extension and FE2 rerun resource rows do not have verified cost, reasoning-counter, effective model/effort, or harness-version receipts in the permitted evidence. Those fields remain null in the public cost/time ledger. The cost metadata states the accounting caveat and the fields that are not available.

The larger sanitized run, context, and ungraded evidence files are partitioned into per-round JSONL files. Each family directory has an `index.json` with row counts, byte lengths, and SHA-256 hashes. Compact missing-value markers are resolved by `results/missing-reasons.json`.
