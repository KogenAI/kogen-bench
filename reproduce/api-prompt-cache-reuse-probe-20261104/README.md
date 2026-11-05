# Prompt-cache reuse on the Anthropic API: what keeps a cached prefix warm

**Verdict: unresolved. This is an unconfirmed probe (n = 11 calls, one prefix, one run), not a confirmed result.** In this probe a ~14.9k-token cached prefix (system + two tools + first user turn) was reused after changing effort (low to high and back), after omitting the thinking field, on a mid-conversation per-message effort change (beta), and within one model. It was not reused when thinking was switched to `between_tools`, nor across models. An earlier run of the same probe showed the same pattern, but no registered confirmation has been run, so the pattern is not stated as a cause or relied on for any decision.

| call | model | effort | thinking | cache write | cache read | result |
|---|---|---|---|---|---|---|
| a | sonnet | low | adaptive | 14901 | 0 | miss |
| b | sonnet | low | adaptive | 0 | 14901 | hit |
| c | sonnet | high | adaptive | 0 | 14901 | hit |
| c2 | sonnet | low | adaptive | 0 | 14901 | hit |
| d1 | sonnet | low | omit | 0 | 14901 | hit |
| d2 | sonnet | low | between_tools | 14900 | 0 | miss |
| e | haiku | low | adaptive | 14901 | 0 | miss |
| h1 | haiku | low | adaptive | 0 | 14901 | hit |
| h2 | haiku | high | adaptive | 0 | 14901 | hit |
| f0 | sonnet | low | adaptive | 0 | 14901 | hit |
| f1 | sonnet | low | adaptive | 0 | 14901 | hit |

11 calls, USD 0.095 at list price (cap USD 5). Each probe run uses a fresh nonce, so no cache is shared between runs. Caveat: one prefix, one run, no repetition; the Haiku rows show the model-keyed cache, not a quality comparison.

## Source and runtime
`probe.py` is a stdlib-HTTP port of an earlier probe script (same calls, same prices).

## Rerun
`ANTHROPIC_API_KEY=... python3 -I probe.py OUT.jsonl`; the table is in data/results.jsonl.
