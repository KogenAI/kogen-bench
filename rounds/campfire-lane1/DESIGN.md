# Campfire lane 1 design record

Pre-registration was recorded before execution. This page contains design facts only; lane 1 was withdrawn before formal cells.

| Arm | Application pin recorded in the design | Role |
|---|---|---|
| Candidate | `5c53423372c28a57d2764281e2767ddc65e026ca` | Phoenix/LiveView/SQLite candidate. |
| Elixir reference | `f15fc9eb609286f1e3da970e7dfd95e3bf69f82f`; conditional fallback `3498c18f3705de2bcaff778132cd5699199e1cbc` | Reference application; the fallback was conditional on a build or smoke failure. |
| Rust reference | `1ea6d6f6b24fd21e7d01e69b7c92df5c380bcbde` | Reference application. |

The registered schedule used five repetitions per arm in each of two scenarios: normal clients and ten slow clients. The planned total of 30 formal cells is **source-reported, not reproducible from public data**. The exact benchmark-driver revision, raw records, and formal launch receipts are unavailable. No result is inferable from the pins or schedule.
