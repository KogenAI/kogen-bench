# Design and execution record

## Research question

The replay asks how endpoint, HTTP affinity, shared-prefix length, spacing, warm versus fresh-prefix control, and conversation scope relate to provider-reported cached input for the same frozen workload. It is about caching request fixtures, not task completion or a Kogen/Codex winner.

## Planned workload

- Model and effort: `gpt-6-luna`, medium, held fixed.
- Fixtures: two synthetic Kogen-derived templates, builder/develop and shaper.
- Prefix lengths: 512, 2,048, and 11,008 local tokens measured with `whitespace-v1`; these are not verified provider-token counts.
- Gap: 0, 5, or 30 seconds from terminal response to next dispatch.
- Core factors: two endpoints, all six HTTP affinity controls on or off, three prefix lengths, three gaps, warm or fresh-prefix control, two fixture repeats, and two requests per episode (288 attempts).
- Header screen: six leave-one-header-out treatments at 2,048 tokens and a 5-second gap, one pair per endpoint and omitted control (48 attempts). These are mechanism screens.
- Scope screen: same conversation/key, new thread with shared key, and new thread with new key at 11,008 tokens and a 5-second gap (24 attempts).
- Total: 180 scheduled attempts per endpoint, 360 assigned attempts. No replacement requests were allowed.

Warm episodes prime the repeated prefix before the probe. The fresh-prefix control uses a sham primer and independently salted probe prefix; it is not a provider-certified empty cache. The all-off treatment removes the six named routing controls while retaining the body cache-key policy. Scope comparisons bundle changes in conversation/thread and, for the new-key level, cache key.

## Execution evidence and deviations

Endpoint-specific plans and dry runs each list 180 requests and report admission with no blockers. The OpenAI receipts use source revision `cf832ba`; the ChatGPT-EU receipts use `1e759ea`. Both use the common replay body profile and record `gpt-6-luna` at medium effort.

The design called for Kogen-owned account selection on both endpoints. The OpenAI run records that source; the ChatGPT-EU run records injected authentication. The source summary also identifies different venues for the two endpoint runs. These differences prevent attribution of their contrast to endpoint alone.

The receipts record 171 OpenAI and 177 ChatGPT-EU dispatches. The remaining 9 and 3 scheduled slots, respectively, were not dispatched after primer failures; they were not replaced. All dispatched rows report valid input, cached-input, and uncached-input counters.

## Analysis status

No pre-registered decision rule existed beyond the design document. The design text proposed a 5-percentage-point mechanism threshold and paired block-bootstrap intervals, but no separate frozen pre-execution registration of those rules is available. This round does not apply them or classify a contrast as supported. All tables are **DESCRIPTIVE**. Leave-one-out results have n=1 per endpoint/header cell and are explicitly indicative.

The supplied design artifact was marked design-only; the later plans and receipts document the subsequent execution. Neither this replay nor its counters provide official grades, Build outcomes, or evidence for an automatic product change.
