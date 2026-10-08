# Results: controlled prompt-cache replay

All cache shares below are weighted shares, `sum(cached input) / sum(total input)`, for usage-valid probes. In each cell, `n` is usage-valid probes / assigned probes; the counter fraction is cached / total input. Primer requests are excluded from probe shares. The coordinator roll-up reproduces the supplied summary's grouping; it combines panels for two warm all-on rows, as noted below.

## Core panel

Each core cell contains up to six assigned probes across the two fixtures and three gaps.

| Prefix tokens | HTTP affinity | Condition | OpenAI Responses | ChatGPT backend |
| --- | --- | --- | --- | --- |
| 11008 | all_on | warm | 96.8% (6/6; 66,048/68,260) | 96.6% (5/6; 55,040/56,999) |
| 11008 | all_on | cold | 0.0% (6/6; 0/68,264) | 96.8% (6/6; 66,048/68,264) |
| 11008 | all_off | warm | 0.0% (6/6; 0/68,257) | 16.1% (6/6; 11,008/68,257) |
| 11008 | all_off | cold | 0.0% (5/6; 0/56,994) | 16.1% (6/6; 11,008/68,256) |
| 2048 | all_on | warm | 58.8% (5/6; 7,168/12,193) | 49.5% (6/6; 7,168/14,491) |
| 2048 | all_on | cold | 0.0% (6/6; 0/12,197) | 74.2% (6/6; 10,752/14,497) |
| 2048 | all_off | warm | 0.0% (5/6; 0/12,198) | 12.4% (6/6; 1,792/14,499) |
| 2048 | all_off | cold | 0.0% (5/6; 0/12,201) | 0.0% (6/6; 0/14,504) |
| 512 | all_on | warm | 0.0% (5/6; 0/4,505) | 0.0% (6/6; 0/5,271) |
| 512 | all_on | cold | 0.0% (6/6; 0/5,266) | 0.0% (6/6; 0/5,266) |
| 512 | all_off | warm | 0.0% (4/6; 0/2,968) | 0.0% (5/6; 0/4,498) |
| 512 | all_off | cold | 0.0% (5/6; 0/4,497) | 0.0% (6/6; 0/5,262) |

## Coordinator summary roll-up

This reproduces the supplied summary table. Its 11,008-token all-on warm row combines the core panel with all conversation-scope probes; its 2,048-token all-on warm row combines the core panel with all-on controls from the individual-header panel. Other cells use the core panel, and the 512-token row pools all core conditions. The mixed-panel warm rows are descriptive roll-ups, not single factorial cells.

| Prefix tokens | HTTP affinity | Condition | OpenAI Responses | ChatGPT backend |
| --- | --- | --- | --- | --- |
| 11,008 | all on | warm | 80.6% (12/12; 110,080/136,523) | 87.9% (11/12; 110,080/125,262) |
| 11,008 | all on | cold | 0.0% (6/6; 0/68,264) | 96.8% (6/6; 66,048/68,264) |
| 11,008 | all off | warm | 0.0% (6/6; 0/68,257) | 16.1% (6/6; 11,008/68,257) |
| 11,008 | all off | cold | 0.0% (5/6; 0/56,994) | 16.1% (6/6; 11,008/68,256) |
| 2,048 | all on | warm | 53.7% (11/12; 14,336/26,693) | 47.0% (11/12; 12,544/26,688) |
| 2,048 | all on | cold | 0.0% (6/6; 0/12,197) | 74.2% (6/6; 10,752/14,497) |
| 2,048 | all off | warm | 0.0% (5/6; 0/12,198) | 12.4% (6/6; 1,792/14,499) |
| 2,048 | all off | cold | 0.0% (5/6; 0/12,201) | 0.0% (6/6; 0/14,504) |
| 512 | any | any | 0.0% (20/24; 0/17,236) | 0.0% (23/24; 0/20,297) |

## Individual-header diagnostics — indicative only

Each omitted-header cell has n=1. These cells can nominate a follow-up but cannot establish that a control is required. The OpenAI session-id probe was not dispatched after its primer failed; it is missing, not a zero-cache observation.

| Omitted HTTP control | OpenAI Responses | ChatGPT backend |
| --- | --- | --- |
| session-id | — (0/1) | 0.0% (1/1; 0/2,297) |
| thread-id | 78.0% (1/1; 1,792/2,298) | 0.0% (1/1; 0/2,299) |
| x-client-request-id | 0.0% (1/1; 0/2,300) | 70.7% (1/1; 1,792/2,533) |
| x-codex-turn-metadata | 70.7% (1/1; 1,792/2,533) | 70.7% (1/1; 1,792/2,535) |
| x-codex-turn-state | 70.7% (1/1; 1,792/2,535) | 78.0% (1/1; 1,792/2,297) |
| x-codex-window-id | 70.7% (1/1; 1,792/2,535) | 0.0% (1/1; 0/2,534) |
| all_on comparator | 49.4% (6/6; 7,168/14,500) | 44.1% (5/6; 5,376/12,197) |

## Conversation-scope diagnostics

Each scope cell has two probes, one per fixture, and is indicative. Scope changes are bundles; these rows do not isolate a single routing control.

| Scope treatment | OpenAI Responses | ChatGPT backend |
| --- | --- | --- |
| S0_same_context | 96.8% (2/2; 22,016/22,751) | 48.4% (2/2; 11,008/22,751) |
| S1_new_thread_shared_key | 96.7% (2/2; 22,016/22,756) | 96.7% (2/2; 22,016/22,756) |
| S2_new_thread_new_key | 0.0% (2/2; 0/22,756) | 96.7% (2/2; 22,016/22,756) |

## Interpretation limits

- All 512-token core probes with valid counters reported zero cached input. This is an observation for these local-tokenizer fixtures, not a provider minimum or cache threshold.
- In the core panel, all-on warm probes had more cached input than all-off warm probes at 2,048 and 11,008 tokens. The one-request header screens vary by control and endpoint; n=1 cells remain indicative.
- Fresh-prefix controls are not provider-certified empty caches. At 11,008 tokens the ChatGPT-backend all-on cold probes were 96.8%, while OpenAI probes were 0.0%; this contrast is confounded by the authentication-source and venue differences.
- The 2,048-token backend all-on cold share (74.2%) exceeded its core warm share (49.5%). These small samples do not establish a warm-primer effect.
- No paired bootstrap, adoption gate, or decision threshold is applied. The round is DESCRIPTIVE and supports no endpoint winner, product change, cache guarantee, or Build-efficacy claim.

Recompute all four tables with `python3 reproduce/cache_replay_tables.py`.
