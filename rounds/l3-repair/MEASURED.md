# Measurements — l3-repair

Question: See [README.md](README.md). The scored unit is an exact cell ID. The result uses only committed, sanitized data and the lane receipts linked by the round page.

Required measures: Official full-pass outcome, aggregate hidden-test count, wall seconds, and uncached/cached/output tokens. Per-test pass-set preservation is not measured in the public bundle.

Coverage: Six new repair cells have Standard 1.2 rows; their six paired originals remain in the Round 70 cohort and are not duplicated here. Every published scored row has an as-graded outcome. The all-planned denominator beyond the listed cohort is not inferred from these records.

Coverage counts: 6 Standard records; 6 officially graded rows; 390 explicitly missing scalar/array capture slots across the records. Exact paths, reasons, and their impact are in [MISSING.md](MISSING.md).

Verdict impact: Explicit receipt gaps limit protocol compliance and measurement completeness. The recorded as-graded outcomes, aggregate test counts, wall values, and token totals are unchanged. The separate publication release gate remains blocked by any open publication evidence gate and by these historical deviations.
