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
    "disposition": "This is a retrospective cohort summary, not a standalone executed round. VERIFICATION.md documents its public export calculation; the former arm denominators and API-equivalent cost totals are not reproduced by the public snapshot.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Retrospective cohort with no standalone Kogen commit or launch command.",
    "raw_public_records": [
      "results/run-records/index.json",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round rails-catalogue"
  },
  "round": "rails-catalogue"
}
```
