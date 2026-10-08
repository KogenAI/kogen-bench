# Declared data gaps: kh climb

This declaration applies to the public snapshot checked for this A2 page. It does not assert that no historical run occurred.

- Exact cell IDs and arm-to-cell crosswalk: unavailable.
- Complete planned, started, finished, graded and ITT partitions: unavailable where not separately reported in [reported-data.json](reported-data.json).
- Full exact harness/Kogen revision: kh@b3009982 is reported as an 8-character prefix. A full exact SHA and public source mapping were not recovered.
- Exact task IDs: Seven development tasks are reported; the exact public task IDs are not recovered.
- Exact launch command: Not recovered. The launch command and exact selected cell IDs are absent from the public snapshot.
- Raw per-cell records and transcripts: not present in the public snapshot.
- Official cell and run-record exports contain no rows with this exact round ID.
- All documentary numeric aggregates are marked **source-reported, not reproducible from public data**; see [reported-data.json](reported-data.json).

The page does not publish raw transcripts, stderr, egress logs, private paths, hidden tests, grader internals, credentials, or reference solutions.

## Historical record declaration for kh-climb

```json
{
  "round": "kh-climb",
  "cells": 0,
  "fields": {},
  "gap_sources": {
    "lost": {},
    "reconstructable": {}
  }
}
```
