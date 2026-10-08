# L4b US release and execution record

STATUS: **VALID** — US scored cohort complete

The public design is a sanitized copy of the frozen source, dated before scored cells. Original-source SHA-256: `94d0158342fd83188e5a49d3aed538bda401cd96f5335b2992a24e5342634ebc`; published-byte SHA-256: `7b6bd259e4dcf0229f1d4840daaed75fbee27722f916cec3fcc5ac9743f8dc7f`, also recorded in [DESIGN.sha256](DESIGN.sha256). The three empty child commits were created and the task metadata repository path was corrected before deployment.

The exact-arm smoke prefix covered the first seven cells in the frozen order. All seven received official grades before the remaining eleven cells were released. The smoke prefix stalled for about 25 minutes at the US disk floor; this caused delay only. The full cohort ran sequentially on `kogen-bench-us`, and all 18 official grades used `r70-macbook-window-v1`.

The dispatcher batches were:

```sh
python3 levers/lanes-2026-10-07/l4b/dispatch.py run --batch first
python3 levers/lanes-2026-10-07/l4b/dispatch.py run --batch rest
```

The public snapshot contains no Standard 1.2 run records for the 18 planned IDs, no strict-validation receipt for the seven-cell smoke prefix before the remaining eleven were released, and no strict-validation receipt for all 18 cells before analysis. The official outcomes and token data are in [cells.csv](data/cells.csv), but those rows do not substitute for the missing records and receipts. The public evidence gap and its effect on release eligibility are detailed in [MEASURED.md](MEASURED.md). Strict checklist completion is not established by this public snapshot. The frozen design and order remain in [DESIGN.md](DESIGN.md) and [ORDER.json](reproduce/ORDER.json); the analysis is rerunnable with [reproduce_us.py](reproduce/reproduce_us.py).

The EU extension `l4b-confirm-eu` is **NOT-RUN**: only task 7 was admitted, its baseline was 5/6, and no cells were spent. The completed 18-cell US cohort has no EU scored result.
