# Measurement scope

The ledger retains task, arm, repeat, status, diagnosis ordering and score,
recorded outcome, cycles, wall seconds and input/cache/output/reasoning usage.
It is a sanitized append-only lifecycle export with 59 rows. Standard records
contain 24 final valid trials and four uniquely identified excluded attempts.
Phase-level usage, host boundary telemetry, provider-effective settings and
billed cost are missing. RESULTS.md describes the denominator and formulas.
