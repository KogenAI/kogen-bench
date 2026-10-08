# Measured counters

| Probe arm | Measured | Cached / input | Aggregate share | Individual high-cache / zero-cache probes |
|---|---:|---:|---:|---:|
| Shared key | 11 | 77,056 / 124,789 | 61.75% | 7 / 4 |
| Distinct key | 11 | 22,016 / 124,797 | 17.64% | 2 / 9 |

All 11 pairs had four HTTP 200 requests and valid final counters. The exact static primer/probe prefix was 11,008 local whitespace tokens; the assigned primer-to-probe gap was 5,000 ms, with observed gaps of 5,000–5,005 ms. All responses reported `gpt-6-luna`. Each arm used fresh sessions, and arm order was randomized within each pair. [sanitized.csv](sanitized.csv) gives each pair's counters, share, stream terminal status, and gap without request identifiers.

Aggregate cached share is descriptive. The pre-registered pair threshold determines the primary finding.
