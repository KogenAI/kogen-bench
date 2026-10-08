# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 0,
  "fields": {},
  "gap_sources": {
    "lost": {},
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "No r74-tagged rows occur in the public delivery or official outcome exports. Preserve WITHDRAWN. Later execution/stop details are not recoverable from these public files and must not replace the page lifecycle with an efficacy claim.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Source-reported pin cde7a380 resolves to cde7a380455e9793cb1fc8315791bc9beffb863b on public GitHub; no public r74 cell row verifies per-cell use.",
    "raw_public_records": [
      "results/run-records/index.json",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r74"
  },
  "round": "r74"
}
```
