# Frozen decision and results

**STATUS VALID. Primary finding NOT SUPPORTED.** The frozen distinct-key ≥80% condition held in 1 of 11 complete pairs. The rule required at least 10 successes among 11 complete pairs. K=1/11; exact one-sided p=0.9995117188; 99% Clopper–Pearson CI=[0.000456, 0.508565]. The exact p is the upper tail under the frozen 0.5 pair-success benchmark; the interval describes sampled pair-success frequency, not a future cache guarantee.

| Item | Value |
|---|---:|
| Transport-complete pairs / target | 11 / 11 |
| Successful pairs | 1 |
| Attempted pairs / attempt cap | 11 / 15 |
| Replaced transport-incomplete pairs | 0 |
| Dispatched POSTs / cap | 44 / 60 |
| Charged or reserved tokens / cap | 503,588 / 700,000 |
| Shared probes ≥80% cached | 9 / 11 |
| Distinct probes ≥80% cached | 1 / 11 |
| HTTP 200 requests with valid final counters but incomplete terminal stream | 0 |

The secondary two-sided paired sign test on distinct-minus-shared share omitted exact ties: 9 nonzero differences, p=0.00390625. This secondary comparison does not alter the primary verdict.
Every attempted pair was transport-complete, so no pair was replaced. The backend's two incomplete terminal streams had valid final counters and remained measured under the frozen transport rule. No stream guard fired, no request failed authentication, and the runner did not abort. A measured zero-cache probe remained in the denominator.
