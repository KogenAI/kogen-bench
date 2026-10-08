# L4b-CONFIRM decision rule

The primary outcome is each cell's official full-suite pass indicator. A timeout counts as a failure. Pair packet and no-packet cells by source variant and seed.

For each variant v, P_v is packet-arm full passes out of 3 and C_v is control-arm full passes out of 3. Calculate Σ_v(P_v − C_v) across the three variants.

Report **CONFIRM** only when the sum is at least +2 and no variant's packet mean `tests_passed` is more than 1 below its control mean. Otherwise report **NOT CONFIRMED**.

A **rescue** is a paired seed where the no-packet control fails and the packet cell passes. A **loss** is the reverse. Report rescues and losses by variant and seed, plus per-arm pass counts and mean `tests_passed`.

Use intention-to-treat for all launched cells. Exclude a cell only for a proven environment or adapter fault and record the evidence and disposition. No other exclusions or early stopping are permitted.

Use one token definition: uncached input, cached input, and output; total is their sum. No alternate token accounting is permitted.

This is a coarse independent replication with n=3 per arm per variant. It supports no general claim beyond this cohort.
