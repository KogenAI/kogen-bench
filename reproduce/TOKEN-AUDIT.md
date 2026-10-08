# Token-count reconciliation

This audit compares numeric `tokens` in the published cell metadata with the recovered manifest counters. It follows [METHOD.md](../METHOD.md) and the token fields in [schema/run-record.schema.json](../schema/run-record.schema.json): the total is uncached input + cached input + output; reasoning is included in output and is not added again. Missing counters are unknown, not zero.

The machine-readable [token audit](../data/mined/TOKEN-AUDIT.json) contains every compared cell, each published and manifest value, response counts, class totals, and examples. Round pages also list their exact differences. The miner retains only a provider response count; it excludes response IDs, request logs, transcripts, and rollouts.

## Results

| Cause | Cells | Example cell IDs | Decision under the published definition |
|---|---:|---|---|
| Multi-response aggregation | 1,160 | `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-cascade-contract-v2-r48b-studio`; `r48b-elx07-us-elx-07-cli-stats-cascade-contract-v2-r1` | Keep the published metadata number as the reported full-cell total. Keep the manifest sum separately as a raw counter; do not substitute it for the full-cell value. Per-response usage is not in the public bundle, so the metadata aggregate is not independently re-derived here. |
| Cached input excluded (`cached_input_treatment`) | 0 | No mismatch cell IDs | Count cached input exactly once. No mismatch matched the formula that omits cached input. |
| Cached input counted twice | 0 | No mismatch cell IDs | Count cached input exactly once. No mismatch matched the formula that doubles cached input. |
| Reasoning counted twice | 0 | No mismatch cell IDs | Do not add reasoning to output. No mismatch matched that formula. |
| Kogen vs Codex usage format alone | 0 | No mismatch cell IDs; exact-match control: `codex__gpt-6.1-sol__medium__default__syn-14-bug-sla-business-hours__r1-acct-smoke2-codex-acctsmoke2-studio` | This did not produce a separate mismatch class. All differences occurred in Kogen `kh-gpt`/`kh-plan` wrappers; direct Codex had 711/711 exact matches. |
| Rounding | 0 | No mismatch cell IDs | Token counters are integers here; no mismatch was resolved by rounding. |
| Unexplained single-response numeric error | 0 | No mismatch cell IDs | No mismatch remained after separating multi-response scope. |
| Missing values | 0 missing manifest counters among compared cells; 1,162 rows missing published token metadata are outside the comparison | Examples of missing published metadata: `hc-direct__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc-direct-hc1-studio-smoke`; `hc-ladder-solshape__gpt-6-luna__max__default__elx-02-ingest-supervision__r1-hc-ladder-solshape-hc1-studio` | Missing values remain unknown and are excluded from numeric comparison, not treated as zero. More examples are in the audit JSON. |

In all 1,160 differences, the published metadata total is greater than the manifest sum. They split into 815 `kh-gpt` and 345 `kh-plan` cells. Each has 5–116 provider response IDs in the source manifest. In the 4,774-cell comparison, all direct Codex rows with a published token value match the manifest sum (711/711). No published number was changed.

Examples:

- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-cascade-contract-v2-r48b-studio`: published `445841`; manifest `input + cached input + output` `70439`; 7 provider responses.
- `r48b-elx07-us-elx-07-cli-stats-cascade-contract-v2-r1`: published `483496`; manifest `input + cached input + output` `70821`; 13 provider responses.

These are reported as scope differences, not verified arithmetic errors: the metadata field is a cell total, while the sanitized manifest counter has no per-response usage breakdown. `reproduce/build_records.py` also marks `kh` totals missing because captured runner counters do not establish complete all-stage usage. The published metadata total is therefore the number retained for the full-cell definition; the raw manifest sum stays visible as a separate counter pending a public all-response usage breakdown.

An exact-match control demonstrates the formula decisions: `codex__gpt-6.1-sol__medium__default__syn-14-bug-sla-business-hours__r1-acct-smoke2-codex-acctsmoke2-studio` has published total `307326`, input `27241`, cached input `277760`, output `2325`, and reasoning `24`. The published value is `27241 + 277760 + 2325`; reasoning is not added. It is also a direct Codex-format example. The audit JSON has further controls and missing-value example IDs.

The earlier audit reported 588 differences among 2,188 cells. Its cell membership is not retained, so we cannot establish whether that set is a subset of the 4,774-cell comparison or measure the overlap. The two totals are not directly comparable from the retained evidence.

Reproduce the mined records and token report with:

```sh
python3 reproduce/mine_probe.py
python3 reproduce/recompute_mined.py
```

The miner reads manifests and patch files read-only. Archived patches with credential markers are excluded while their hashes and sizes remain in the mined records.
