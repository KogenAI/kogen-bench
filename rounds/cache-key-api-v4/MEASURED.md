# Measured counters

| Probe arm | Measured | Cached / input | Aggregate share | Individual high-cache / zero-cache probes |
|---|---:|---:|---:|---:|
| Shared key | 11 | 99,072 / 125,022 | 79.24% | 9 / 2 |
| Distinct key | 11 | 11,008 / 125,024 | 8.80% | 1 / 10 |

All 11 pairs had four HTTP 200 requests and valid final counters. The exact static primer/probe prefix was 11,008 local whitespace tokens; the assigned primer-to-probe gap was 5,000 ms, with observed gaps of 5,000–5,005 ms. All responses reported `gpt-6-luna`. Each arm used fresh sessions, and arm order was randomized within each pair. [sanitized.csv](sanitized.csv) gives each pair's counters, share, stream terminal status, and gap without request identifiers.

Aggregate cached share is descriptive. The pre-registered pair threshold determines the primary finding.
