# Declared data gaps: x continuation

This declaration applies to the public snapshot checked for this A2 page. It does not assert that no historical run occurred.

- Exact cell IDs and arm-to-cell crosswalk: unavailable.
- Complete planned, started, finished, graded and ITT partitions: unavailable where not separately reported in [reported-data.json](reported-data.json).
- Full exact harness/Kogen revision: No live Kogen/harness revision is attributable to a scored model run.
- Exact task IDs: No live task IDs are attributable; scripted test IDs are not in the public snapshot.
- Exact launch command: The scripted-provider test command was not recovered.
- Raw per-cell records and transcripts: not present in the public snapshot.
- Official cell and run-record exports contain no rows with this exact round ID.
- All documentary numeric aggregates are marked **source-reported, not reproducible from public data**; see [reported-data.json](reported-data.json).

The page does not publish raw transcripts, stderr, egress logs, private paths, hidden tests, grader internals, credentials, or reference solutions.

## Historical record declaration for x-continuation

```json
{
  "round": "x-continuation",
  "cells": 0,
  "fields": {},
  "gap_sources": {
    "lost": {},
    "reconstructable": {}
  }
}
```
