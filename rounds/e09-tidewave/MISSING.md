# Declared data gaps: e09 locators and Tidewave

This declaration applies to the public snapshot checked for this A2 page. It does not assert that no historical run occurred.

- Exact cell IDs and arm-to-cell crosswalk: unavailable.
- Complete planned, started, finished, graded and ITT partitions: unavailable where not separately reported in [reported-data.json](reported-data.json).
- Full exact harness/Kogen revision: No locator Kogen harness run is reported. Exact revision for the runtime-tool cohort is not recovered.
- Exact task IDs: The oracle cohort spans seven stacks; exact case and runtime task IDs are not recovered.
- Exact launch command: Not recovered; no public locator or Tidewave launch commands are available.
- Raw per-cell records and transcripts: not present in the public snapshot.
- Official cell and run-record exports contain no rows with this exact round ID.
- All documentary numeric aggregates are marked **source-reported, not reproducible from public data**; see [reported-data.json](reported-data.json).

The page does not publish raw transcripts, stderr, egress logs, private paths, hidden tests, grader internals, credentials, or reference solutions.

## Historical record declaration for e09-tidewave

```json
{
  "round": "e09-tidewave",
  "cells": 0,
  "fields": {},
  "gap_sources": {
    "lost": {},
    "reconstructable": {}
  }
}
```
