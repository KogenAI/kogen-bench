# Measured coverage

This round measures provider-reported input and cached-input counters for replay requests. It has no scored benchmark cells or official grades.

| Endpoint plan | Assigned attempts | Dispatched | Usage-valid counters | Unexecuted slots |
|---|---:|---:|---:|---:|
| OpenAI Responses | 180 | 171 | 171 | 9 |
| ChatGPT backend | 180 | 177 | 177 | 3 |
| **Total** | **360** | **348** | **348** | **12** |

The 12 unexecuted slots followed primer failures and were not replaced. Every dispatched row has provider total input, cached input, and uncached input counters; all satisfy `input = cached + uncached`. A zero counter is retained as reported, not treated as missing.

The sanitized attempt files retain the factors needed for the published tables: panel, request phase, local prefix length, affinity treatment, cache condition, conversation-scope treatment, dispatch and usage-valid flags, and the three input counters. Probe shares are weighted as the sum of cached input divided by the sum of total input within each reported group.

No model-generated content, request bodies, header values, request identifiers, paths, or credential material is in the public CSVs. No task success, tool-use behavior, invoice cost, latency, or official grade is measured by this round. The design varied request gaps, but the supplied result summary did not report a gap analysis; no gap effect is claimed here.
