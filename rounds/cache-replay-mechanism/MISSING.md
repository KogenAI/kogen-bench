# Missing data and protocol limits

This is request telemetry rather than a scored benchmark round, so it has zero Standard cell records. The Standard missing-field declaration below therefore has no cell-level gaps. Experiment-specific incomplete slots and the authentication-source deviation are recorded in [measured coverage](MEASURED.md), [design](DESIGN.md), and [results](RESULTS.md).

No request bodies, header values, full identifiers, paths, or credentials are published. The request-level gaps are 9 undispatched slots for OpenAI and 3 for ChatGPT backend, all dependent attempts after primer failures. These slots remain in the assigned denominator and are not represented as zero-cache outcomes.

```json
{
  "round": "cache-replay-mechanism",
  "cells": 0,
  "fields": {},
  "gap_sources": {
    "reconstructable": {},
    "lost": {}
  },
  "protocol_deviations": [
    "The ChatGPT-backend run used injected authentication instead of the design's Kogen-owned account selection.",
    "Twelve assigned request slots were not dispatched after primer failures; no replacements were sent."
  ]
}
```
