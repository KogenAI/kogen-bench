# L3b results

STATUS: **VALID** — registered rule met for the eight selected failures; per-test no-regression is recomputed from public pass/fail sets.

Label: VALID for the registered rule — raw captures not retained; results verified against official grades

The table below is regenerated from data/scored-cells.csv, data/original-failures.csv, and data/per-test-results.json. The public pass/fail sets reproduce the per-test no-regression comparison used by the registered rule.

<!-- L3B-RESULTS:BEGIN -->

### Arm totals

| Arm | Cells | Full-suite rescues | Uncached input | Cached input | Output | Total tokens | Wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| REPAIR | 8 | 3 | 796,472 | 16,684,800 | 288,379 | 17,769,651 | 3227.436 |
| CONTINUE | 8 | 1 | 288,227 | 2,626,048 | 118,358 | 3,032,633 | 1512.299 |
| RESTART | 8 | 2 | 451,463 | 5,742,848 | 200,515 | 6,394,826 | 2288.914 |

Rescues: **REPAIR 3/8; CONTINUE 1/8; RESTART 2/8**.
Rule: REPAIR − CONTINUE = **2** (threshold ≥2); per-test no-regression recomputed **true**. Result: **observed KEEP for these eight selected failures**.
The no-regression comparison is recomputed from [per-test-results.json](data/per-test-results.json); the public sets include names because the selected suites are exposed.

### Scored cells

| Cell ID | Original failure | Arm | Outcome | Test fraction | Patch SHA-256 | Started at (UTC) | Finished at (UTC) | Uncached input | Cached input | Output | Total tokens | Wall seconds |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `codex__gpt-6-luna__max__default__r70-2-elixir-l3b33r__r9004` | `codex__gpt-6-luna__max__default__r70-2-elixir__r33` | REPAIR | fail | 21/25 | `d1b79a381c4f526b4b4cdb0c6d3526d417245e856414653706e1c2ed721e3f89` | 2026-10-08T05:08:28.922+00:00 | 2026-10-08T05:24:30.762+00:00 | 188,958 | 8,343,808 | 75,918 | 8,608,684 | 947.088 |
| `codex__gpt-6-luna__max__default__r70-2-elixir-l3b33c__r9005` | `codex__gpt-6-luna__max__default__r70-2-elixir__r33` | CONTINUE | fail | 21/25 | `d1b79a381c4f526b4b4cdb0c6d3526d417245e856414653706e1c2ed721e3f89` | 2026-10-08T05:35:23.092+00:00 | 2026-10-08T05:41:12.534+00:00 | 53,598 | 570,368 | 25,639 | 649,605 | 334.672 |
| `codex__gpt-6-luna__max__default__r70-2-elixir__r9003` | `codex__gpt-6-luna__max__default__r70-2-elixir__r33` | RESTART | pass | 25/25 | `—` | 2026-10-08T04:16:32.244+00:00 | 2026-10-08T04:29:27.619+00:00 | 133,454 | 2,858,752 | 58,736 | 3,050,942 | 760.470 |
| `codex__gpt-6-luna__max__default__r70-2-go-l3b32r__r9007` | `codex__gpt-6-luna__max__default__r70-2-go__r32` | REPAIR | fail | 21/25 | `44995e2f56574eaa2c94c15eb76d88a06ba458d8f4b10b030f28af1bf629c1c3` | 2026-10-08T04:28:02.873+00:00 | 2026-10-08T04:34:01.673+00:00 | 65,034 | 900,352 | 34,866 | 1,000,252 | 351.479 |
| `codex__gpt-6-luna__max__default__r70-2-go-l3b32c__r9008` | `codex__gpt-6-luna__max__default__r70-2-go__r32` | CONTINUE | fail | 21/25 | `44995e2f56574eaa2c94c15eb76d88a06ba458d8f4b10b030f28af1bf629c1c3` | 2026-10-08T04:22:38.838+00:00 | 2026-10-08T04:25:30.404+00:00 | 30,198 | 331,776 | 14,919 | 376,893 | 164.337 |
| `codex__gpt-6-luna__max__default__r70-2-go__r9006` | `codex__gpt-6-luna__max__default__r70-2-go__r32` | RESTART | fail | 21/25 | `—` | 2026-10-08T04:10:38.804+00:00 | 2026-10-08T04:13:52.872+00:00 | 50,381 | 212,992 | 17,515 | 280,888 | 186.926 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10r__r9013` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10` | REPAIR | fail | 17/18 | `f85028bdb5082885b678f7577f23f77cdca74b16f347d5164ef6c4327580fc09` | 2026-10-08T04:46:19.011+00:00 | 2026-10-08T04:52:50.330+00:00 | 129,425 | 1,950,976 | 34,112 | 2,114,513 | 376.476 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10c__r9014` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10` | CONTINUE | fail | 17/18 | `f85028bdb5082885b678f7577f23f77cdca74b16f347d5164ef6c4327580fc09` | 2026-10-08T04:40:46.918+00:00 | 2026-10-08T04:45:26.457+00:00 | 47,549 | 556,032 | 17,195 | 620,776 | 264.680 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9012` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10` | RESTART | fail | 17/18 | `—` | 2026-10-08T05:41:14.120+00:00 | 2026-10-08T05:46:24.775+00:00 | 57,274 | 669,696 | 27,266 | 754,236 | 295.980 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13r__r9016` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13` | REPAIR | fail | 17/18 | `57c2437118828a5723b658ab7a38430127c888657b65d3762303f305ae29ead3` | 2026-10-08T03:32:22.354+00:00 | 2026-10-08T03:38:19.395+00:00 | 70,238 | 1,262,080 | 28,653 | 1,360,971 | 341.955 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13c__r9017` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13` | CONTINUE | fail | 17/18 | `57c2437118828a5723b658ab7a38430127c888657b65d3762303f305ae29ead3` | 2026-10-08T05:05:13.904+00:00 | 2026-10-08T05:08:27.385+00:00 | 41,380 | 203,776 | 11,635 | 256,791 | 178.812 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9015` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13` | RESTART | fail | 17/18 | `—` | 2026-10-08T05:24:31.997+00:00 | 2026-10-08T05:29:12.139+00:00 | 36,934 | 380,416 | 16,988 | 434,338 | 265.299 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9r__r9010` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9` | REPAIR | fail | 17/18 | `9e6c42031d4716aadff5283855b92ac8222404b4621560decfc7661fbfcf11da` | 2026-10-08T04:10:35.451+00:00 | 2026-10-08T04:16:29.204+00:00 | 95,642 | 947,712 | 24,276 | 1,067,630 | 338.766 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9c__r9011` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9` | CONTINUE | fail | 17/18 | `9e6c42031d4716aadff5283855b92ac8222404b4621560decfc7661fbfcf11da` | 2026-10-08T05:33:05.065+00:00 | 2026-10-08T05:35:20.353+00:00 | 22,071 | 221,696 | 7,497 | 251,264 | 120.759 |
| `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9009` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9` | RESTART | fail | 17/18 | `—` | 2026-10-08T04:33:04.574+00:00 | 2026-10-08T04:37:14.628+00:00 | 48,617 | 403,200 | 18,321 | 470,138 | 235.390 |
| `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9r__r9019` | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9` | REPAIR | pass | 18/18 | `eaed02b9e5c7cf04714145c224ea16687f45023112ac0fad0aae7d3cfb3272e5` | 2026-10-08T04:13:53.820+00:00 | 2026-10-08T04:20:24.438+00:00 | 136,239 | 2,039,040 | 40,064 | 2,215,343 | 389.022 |
| `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9c__r9020` | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9` | CONTINUE | pass | 18/18 | `eaed02b9e5c7cf04714145c224ea16687f45023112ac0fad0aae7d3cfb3272e5` | 2026-10-08T03:37:24.495+00:00 | 2026-10-08T03:41:36.057+00:00 | 55,769 | 515,840 | 24,569 | 596,178 | 250.208 |
| `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9018` | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9` | RESTART | pass | 18/18 | `—` | 2026-10-08T03:32:24.577+00:00 | 2026-10-08T03:37:23.281+00:00 | 65,662 | 677,120 | 31,788 | 774,570 | 297.295 |
| `codex__gpt-6-luna__max__default__r70-5-go-l3b32r__r9022` | `codex__gpt-6-luna__max__default__r70-5-go__r32` | REPAIR | pass | 24/24 | `87b9707bc9d8728c14079e9e95872574d59513cd85d1b8720ba222a6c9483183` | 2026-10-08T04:34:02.899+00:00 | 2026-10-08T04:38:25.242+00:00 | 55,794 | 692,480 | 25,028 | 773,302 | 255.329 |
| `codex__gpt-6-luna__max__default__r70-5-go-l3b32c__r9023` | `codex__gpt-6-luna__max__default__r70-5-go__r32` | CONTINUE | fail | 23/24 | `87b9707bc9d8728c14079e9e95872574d59513cd85d1b8720ba222a6c9483183` | 2026-10-08T04:20:26.830+00:00 | 2026-10-08T04:22:38.118+00:00 | 18,186 | 165,376 | 9,789 | 193,351 | 124.142 |
| `codex__gpt-6-luna__max__default__r70-5-go__r9021` | `codex__gpt-6-luna__max__default__r70-5-go__r32` | RESTART | fail | 10/24 | `—` | 2026-10-08T04:25:32.856+00:00 | 2026-10-08T04:27:59.630+00:00 | 30,032 | 289,280 | 17,394 | 336,706 | 139.895 |
| `codex__gpt-6-luna__max__default__r70-7-rust-l3b31r__r9025` | `codex__gpt-6-luna__max__default__r70-7-rust__r31` | REPAIR | pass | 24/24 | `a1e123612f79ae599035f01085462c6941473bf21df7593f7a82bed682119536` | 2026-10-08T05:29:14.085+00:00 | 2026-10-08T05:33:02.803+00:00 | 55,142 | 548,352 | 25,462 | 628,956 | 227.321 |
| `codex__gpt-6-luna__max__default__r70-7-rust-l3b31c__r9026` | `codex__gpt-6-luna__max__default__r70-7-rust__r31` | CONTINUE | fail | 23/24 | `a1e123612f79ae599035f01085462c6941473bf21df7593f7a82bed682119536` | 2026-10-08T05:46:26.170+00:00 | 2026-10-08T05:47:42.188+00:00 | 19,476 | 61,184 | 7,115 | 87,775 | 74.689 |
| `codex__gpt-6-luna__max__default__r70-7-rust__r9024` | `codex__gpt-6-luna__max__default__r70-7-rust__r31` | RESTART | fail | 23/24 | `—` | 2026-10-08T04:56:37.279+00:00 | 2026-10-08T04:58:26.917+00:00 | 29,109 | 251,392 | 12,507 | 293,008 | 107.659 |

Scored attempts total: **27,197,110 tokens; 7028.649 seconds**. Including the eight original attempts once: **38,997,124 tokens; 12072.850 seconds**.

Patch hashes identify the delivered public patch for each matched failure; RESTART has no patch.

<!-- L3B-RESULTS:END -->
