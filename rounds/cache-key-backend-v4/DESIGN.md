# Cache key v4: two preregistered endpoint rounds

Frozen before either v4 live request. Prior attempts are cache-replay-v3 (incomplete at both endpoints) and cache-key-sharing (invalid fixed-denominator backend round). Their observations motivated this design and do not enter its test.

## H-BACKEND

On the owner's default Kogen Codex-client login, the first probe in a fresh thread reports cached/input share at least 0.80 with the primer's shared key bundle and at most 0.05 with a distinct bundle. A pair succeeds only when both conditions hold. This is about provider-reported counters on the ChatGPT Codex backend.

## H-API

On the separate official Sign in with ChatGPT subscription login, the first distinct-key probe reports cached/input share at least 0.80. A complete pair succeeds when its distinct-key probe meets that threshold. This is the primary direction supported by v3: all seven transport-valid distinct-key probes reported at least 95.7% cached, whereas the shared arm was mixed (five high and three zero measured probes). The shared-versus-distinct paired share difference is secondary and tested two-sided without a directional threshold. This endpoint is analyzed separately; OAuth grant and route change together.

## Allocation and controls

For each endpoint, target 11 transport-complete pairs. The frozen reserve has 15 fresh pairs (eight builder and seven shaper), four requests each: a primer/probe episode in each key arm. A seeded ChaCha20 shuffle orders pairs and separately orders the two arms within each pair. Primer/probe remain adjacent; each probe is in a new thread. The shared arm retains the primer's `prompt_cache_key`, `session-id`, and matching client/turn session metadata. The distinct arm changes this bundle. The bundle, rather than an isolated field, is the treatment. Episode-specific salts prevent reuse across pairs.

The canonical sanitized fixture manifest has SHA-256 `4f424ac34fdb016dcb4a16ce9e9be4aafb20d184138924536bb24fc9863d16a6`. Each exact primer/probe `instructions` prefix is 11,008 local whitespace tokens, with the same fixture input excerpt and a short probe continuation. Model is `gpt-6-luna`, medium effort; `store=false`, `stream=true`, `tool_choice=none`, no parallel tools, low text verbosity, 384 requested output tokens, and a five-second assigned primer-to-probe gap. The replay adapter enforces output and reasoning stream guards of 512 and 1,024 tokens. The hard endpoint cap is 700,000 charged or reserved input-plus-output tokens and 60 POSTs. The runner stops after 11 complete pairs; it may need fewer than 60 posts. If the token cap prevents target completion, status is INVALID. No third live execution or outcome-dependent retry is authorized.

The smallest complete-pair target allowing one nonsuccess at exact one-sided alpha 0.01 is 11: `P[X≥10 | X~Binomial(11,0.5)] = (11+1)/2048 = 0.005859375`. At 10 pairs, `P[X≥9] = (10+1)/1024 = 0.0107421875`. The attempt cap of 15 is 1.36 times the target, constrained by the 700,000-token endpoint cap. Even if all 15 pairs are needed, runtime admission enforces the token cap before dispatch and marks the round INVALID if the target is not met.

## Transport fix and scope

Prior receipts show HTTP 200 and internally valid final counters on every output-limited stream: output reached exactly the old 256-token request cap, often entirely in reasoning, with no stream-guard truncation or timeout. Two backend primers were incorrectly treated as failed by the replay runner because their terminal response was `incomplete`, so their probes were never sent. The v4 runner permits a probe after an HTTP 200 primer with valid final counters even if its response status is `incomplete`, and raises the request cap to 384. Transport classification uses only HTTP status and final-counter validity, never cached-token values. A measured zero-cache probe remains a nonsuccess.

Raw plans and receipts stay in this private workspace. Published rounds contain only sanitized counters, timing, statuses, hashes, and a scoped conclusion; no credential material or opaque request identifiers.
