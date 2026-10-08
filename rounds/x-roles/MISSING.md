# Declared data gaps: x roles

This declaration applies to the public snapshot checked for this A2 page. It does not assert that no historical run occurred.

- Exact cell IDs and arm-to-cell crosswalk: unavailable.
- Complete planned, started, finished, graded and ITT partitions: unavailable where not separately reported in [reported-data.json](reported-data.json).
- Full exact harness/Kogen revision: Exact harness/Kogen revision per role cohort was not recovered.
- Exact task IDs: The worker pilot used one CSV task. The implementation cohort task IDs and reviewer fixture IDs are not recovered.
- Exact launch command: Not recovered; no public launch command or exact cell IDs are available.
- Raw per-cell records and transcripts: not present in the public snapshot.
- Official cell and run-record exports contain no rows with this exact round ID.
- All documentary numeric aggregates are marked **source-reported, not reproducible from public data**; see [reported-data.json](reported-data.json).

The page does not publish raw transcripts, stderr, egress logs, private paths, hidden tests, grader internals, credentials, or reference solutions.

## Historical record declaration for x-roles

```json
{
  "round": "x-roles",
  "cells": 0,
  "fields": {},
  "gap_sources": {
    "lost": {},
    "reconstructable": {}
  }
}
```
