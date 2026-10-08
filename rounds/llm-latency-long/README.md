# LLM latency probe: long reasoning prompts

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first request is documented.
- **INCOMPLETE_EXECUTION:** The collector stopped with six registered requests unstarted.
- **CONDITIONS_MISMATCH:** Fixed order and repeated prompts confound model and effort comparisons.
- **relabelled 2026-10-08 after scrutiny:** Previously labelled VALID; the README describes only confounded client-visible timing.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **DESCRIPTIVE** — DESCRIPTIVE; unscored client-visible timing only.

This EU-only round measured request events through the Codex CLI JSONL interface. It did not measure provider SSE, answer correctness, Build success, or a Kogen intervention. The maximum registered schedule was 24 requests: four model/effort arms, two prompt labels, and up to three repetitions per combination.

## Observations

There were 18 request attempts: 17 completed uncensored and one ended with a collector JSON decode fault during the third Luna-max code request. Six of the 24 possible requests were not started after the collector stopped. All 17 completed requests had a client-visible idle gap over 90 seconds; none reached 600 or 1,200 seconds of total wall time. All 18 observed first stdout bytes arrived within 1.223 seconds. These are client observations, not provider transport timings.

The prompt labels were `P-hard-math` and `P-hard-code`. The model/effort combinations were `gpt-6-luna` at max and xhigh, and `gpt-6.1-sol` at high and medium. No prompt or response text is published.

## Reproduction record

- **Kogen commit:** not applicable; the probe called Codex directly and did not run Kogen.
- **Harness Git commit:** not present in the public record. The source-reported Codex harness snapshot fingerprint is `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`; it is a SHA-256 fingerprint, not a Git commit. The source-reported round-2 probe fingerprint is `ba124e2b471bf07495982db48c7127242e0ff07ae3d3851fbea02714b88046c0`. Both are recorded in [provenance.json](provenance.json).
- **Model and effort:** `gpt-6-luna` at max and xhigh; `gpt-6.1-sol` at high and medium.
- **Task IDs:** no benchmark task IDs were assigned. The exact probe labels are `P-hard-math` and `P-hard-code`.
- **Historical request launch command:** not preserved in the public record. The public analysis command is `python3 rounds/llm-latency-long/reproduce.py` from the repository root.
- **Raw records:** [EU event log](raw/round2-eu-20261006T014516Z.jsonl), SHA-256 `1efbc3f6b617223160d58df4c259b017deb337ec7f4f2205bce18646e26a4c08`. It retains event types, numeric measurements, timestamps, and probe labels, with no prompt or response text.

The reproduction command recomputes the per-request summary from that log. The public records do not support exact provider first-byte, token-gap, or production latency claims. Fixed order and repeated prompts also confound model/effort comparisons.
