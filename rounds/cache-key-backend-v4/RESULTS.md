# Frozen decision and results

**STATUS VALID. Primary finding NOT SUPPORTED.** The frozen shared-key ≥80% and distinct-key ≤5% condition held in 5 of 11 complete pairs. The rule required at least 10 successes among 11 complete pairs. K=5/11; exact one-sided p=0.7255859375; 99% Clopper–Pearson CI=[0.114469, 0.830688]. The exact p is the upper tail under the frozen 0.5 pair-success benchmark; the interval describes sampled pair-success frequency, not a future cache guarantee.

| Item | Value |
|---|---:|
| Transport-complete pairs / target | 11 / 11 |
| Successful pairs | 5 |
| Attempted pairs / attempt cap | 11 / 15 |
| Replaced transport-incomplete pairs | 0 |
| Dispatched POSTs / cap | 44 / 60 |
| Charged or reserved tokens / cap | 503,482 / 700,000 |
| Shared probes ≥80% cached | 7 / 11 |
| Distinct probes ≥80% cached | 2 / 11 |
| HTTP 200 requests with valid final counters but incomplete terminal stream | 2 |

Every attempted pair was transport-complete, so no pair was replaced. The backend's two incomplete terminal streams had valid final counters and remained measured under the frozen transport rule. No stream guard fired, no request failed authentication, and the runner did not abort. A measured zero-cache probe remained in the denominator.
