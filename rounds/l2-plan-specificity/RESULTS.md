# Results

STATUS: **VALID**

The current cohort has 78/78 officially graded exact cell IDs: 42 gate cells and 36 rep-2 bulk cells. It includes 72 planned factorial cells and six Luna-low no-plan cells. Every included current row is labeled VALID; the historical Luna-max no-plan baseline is a separate descriptive cohort.

## Per-cell outcomes and builder tokens

Token rule: uncached input + cached input + output; total = the sum of those three components. Builder tokens below include the provided frozen plan in the builder prompt. No hidden grader details are included.

| Task / variant | Level | Builder | Rep | Stage | Status | Outcome | Cell ID | Uncached | Cached | Output | Total |
|---|---|---:|---:|---|---|---|---|---:|---:|---:|---:|
| `r70-2-elixir` | none | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-elixir__r1` | 31,788 | 231,168 | 4,187 | 267,143 |
| `r70-2-elixir-l2approach` | approach | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-elixir-l2approach__r1` | 20,935 | 88,064 | 1,858 | 110,857 |
| `r70-2-elixir-l2approach` | approach | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-elixir-l2approach__r2` | 15,882 | 233,472 | 3,849 | 253,203 |
| `r70-2-elixir-l2approach` | approach | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-elixir-l2approach__r1` | 209,777 | 9,861,120 | 84,230 | 10,155,127 |
| `r70-2-elixir-l2approach` | approach | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-elixir-l2approach__r2` | 317,097 | 8,334,848 | 106,857 | 8,758,802 |
| `r70-2-elixir-l2criteria` | criteria | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-elixir-l2criteria__r1` | 83,829 | 1,040,896 | 7,757 | 1,132,482 |
| `r70-2-elixir-l2criteria` | criteria | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-elixir-l2criteria__r2` | 97,041 | 1,399,552 | 13,443 | 1,510,036 |
| `r70-2-elixir-l2criteria` | criteria | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-elixir-l2criteria__r1` | 177,269 | 7,560,704 | 75,061 | 7,813,034 |
| `r70-2-elixir-l2criteria` | criteria | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-elixir-l2criteria__r2` | 312,914 | 18,456,064 | 123,669 | 18,892,647 |
| `r70-2-elixir-l2steps` | steps | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-2-elixir-l2steps__r1` | 57,881 | 576,512 | 8,200 | 642,593 |
| `r70-2-elixir-l2steps` | steps | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-2-elixir-l2steps__r2` | 64,917 | 714,752 | 15,237 | 794,906 |
| `r70-2-elixir-l2steps` | steps | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-2-elixir-l2steps__r1` | 260,423 | 8,961,792 | 113,232 | 9,335,447 |
| `r70-2-elixir-l2steps` | steps | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-2-elixir-l2steps__r2` | 194,177 | 9,452,288 | 78,703 | 9,725,168 |
| `r70-2-go` | none | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-go__r1` | 15,864 | 153,600 | 3,204 | 172,668 |
| `r70-2-go-l2approach` | approach | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-go-l2approach__r1` | 16,611 | 142,592 | 2,700 | 161,903 |
| `r70-2-go-l2approach` | approach | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-go-l2approach__r2` | 19,744 | 224,256 | 3,866 | 247,866 |
| `r70-2-go-l2approach` | approach | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-go-l2approach__r1` | 66,021 | 916,480 | 35,961 | 1,018,462 |
| `r70-2-go-l2approach` | approach | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-2-go-l2approach__r2` | 47,881 | 578,304 | 31,512 | 657,697 |
| `r70-2-go-l2criteria` | criteria | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-go-l2criteria__r1` | 14,676 | 83,200 | 2,430 | 100,306 |
| `r70-2-go-l2criteria` | criteria | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-go-l2criteria__r2` | 20,598 | 105,216 | 2,620 | 128,434 |
| `r70-2-go-l2criteria` | criteria | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-2-go-l2criteria__r1` | 47,033 | 777,216 | 29,716 | 853,965 |
| `r70-2-go-l2criteria` | criteria | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-go-l2criteria__r2` | 52,090 | 684,032 | 27,313 | 763,435 |
| `r70-2-go-l2steps` | steps | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-2-go-l2steps__r1` | 45,413 | 204,800 | 4,095 | 254,308 |
| `r70-2-go-l2steps` | steps | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-2-go-l2steps__r2` | 17,136 | 147,712 | 4,358 | 169,206 |
| `r70-2-go-l2steps` | steps | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-2-go-l2steps__r1` | 52,186 | 292,352 | 21,989 | 366,527 |
| `r70-2-go-l2steps` | steps | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-2-go-l2steps__r2` | 65,768 | 644,096 | 28,362 | 738,226 |
| `r70-4-elixir-fe2` | none | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2__r1` | 25,119 | 185,856 | 3,184 | 214,159 |
| `r70-4-elixir-fe2-l2approach` | approach | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2-l2approach__r1` | 32,734 | 432,640 | 4,628 | 470,002 |
| `r70-4-elixir-fe2-l2approach` | approach | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2-l2approach__r2` | 18,192 | 229,632 | 3,824 | 251,648 |
| `r70-4-elixir-fe2-l2approach` | approach | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l2approach__r1` | 107,325 | 1,471,744 | 35,803 | 1,614,872 |
| `r70-4-elixir-fe2-l2approach` | approach | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l2approach__r2` | 71,983 | 592,896 | 19,273 | 684,152 |
| `r70-4-elixir-fe2-l2criteria` | criteria | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2-l2criteria__r1` | 57,723 | 331,264 | 5,585 | 394,572 |
| `r70-4-elixir-fe2-l2criteria` | criteria | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2-l2criteria__r2` | 31,917 | 281,088 | 3,612 | 316,617 |
| `r70-4-elixir-fe2-l2criteria` | criteria | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l2criteria__r1` | 48,351 | 548,864 | 24,040 | 621,255 |
| `r70-4-elixir-fe2-l2criteria` | criteria | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l2criteria__r2` | 58,537 | 911,360 | 28,170 | 998,067 |
| `r70-4-elixir-fe2-l2steps` | steps | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2-l2steps__r1` | 25,233 | 159,744 | 2,769 | 187,746 |
| `r70-4-elixir-fe2-l2steps` | steps | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-elixir-fe2-l2steps__r2` | 117,662 | 1,199,872 | 13,422 | 1,330,956 |
| `r70-4-elixir-fe2-l2steps` | steps | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l2steps__r1` | 60,230 | 881,408 | 27,388 | 969,026 |
| `r70-4-elixir-fe2-l2steps` | steps | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l2steps__r2` | 59,480 | 869,120 | 26,787 | 955,387 |
| `r70-4-go-fe2` | none | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-go-fe2__r1` | 16,741 | 106,240 | 2,315 | 125,296 |
| `r70-4-go-fe2-l2approach` | approach | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-4-go-fe2-l2approach__r1` | 15,838 | 177,920 | 4,281 | 198,039 |
| `r70-4-go-fe2-l2approach` | approach | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-go-fe2-l2approach__r2` | 14,730 | 140,544 | 2,722 | 157,996 |
| `r70-4-go-fe2-l2approach` | approach | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l2approach__r1` | 59,420 | 863,488 | 25,418 | 948,326 |
| `r70-4-go-fe2-l2approach` | approach | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l2approach__r2` | 36,397 | 399,616 | 20,173 | 456,186 |
| `r70-4-go-fe2-l2criteria` | criteria | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-go-fe2-l2criteria__r1` | 4,732 | 33,024 | 216 | 37,972 |
| `r70-4-go-fe2-l2criteria` | criteria | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-go-fe2-l2criteria__r2` | 21,856 | 184,832 | 2,994 | 209,682 |
| `r70-4-go-fe2-l2criteria` | criteria | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l2criteria__r1` | 89,064 | 1,393,664 | 41,067 | 1,523,795 |
| `r70-4-go-fe2-l2criteria` | criteria | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l2criteria__r2` | 47,152 | 708,096 | 26,708 | 781,956 |
| `r70-4-go-fe2-l2steps` | steps | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-go-fe2-l2steps__r1` | 24,968 | 285,696 | 3,857 | 314,521 |
| `r70-4-go-fe2-l2steps` | steps | Luna-low | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-go-fe2-l2steps__r2` | 13,047 | 174,848 | 2,341 | 190,236 |
| `r70-4-go-fe2-l2steps` | steps | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l2steps__r1` | 55,099 | 691,968 | 25,790 | 772,857 |
| `r70-4-go-fe2-l2steps` | steps | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l2steps__r2` | 71,562 | 908,288 | 32,930 | 1,012,780 |
| `r70-4-ts-bun-fe2` | none | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2__r1` | 22,848 | 103,424 | 1,757 | 128,029 |
| `r70-4-ts-bun-fe2-l2approach` | approach | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2-l2approach__r1` | 11,670 | 85,248 | 1,873 | 98,791 |
| `r70-4-ts-bun-fe2-l2approach` | approach | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2-l2approach__r2` | 27,467 | 258,560 | 3,861 | 289,888 |
| `r70-4-ts-bun-fe2-l2approach` | approach | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l2approach__r1` | 48,507 | 518,656 | 28,377 | 595,540 |
| `r70-4-ts-bun-fe2-l2approach` | approach | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l2approach__r2` | 58,375 | 718,592 | 28,704 | 805,671 |
| `r70-4-ts-bun-fe2-l2criteria` | criteria | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2-l2criteria__r1` | 18,685 | 231,424 | 2,714 | 252,823 |
| `r70-4-ts-bun-fe2-l2criteria` | criteria | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2-l2criteria__r2` | 20,882 | 130,560 | 2,598 | 154,040 |
| `r70-4-ts-bun-fe2-l2criteria` | criteria | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l2criteria__r1` | 50,249 | 235,776 | 16,232 | 302,257 |
| `r70-4-ts-bun-fe2-l2criteria` | criteria | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l2criteria__r2` | 50,576 | 558,592 | 25,881 | 635,049 |
| `r70-4-ts-bun-fe2-l2steps` | steps | Luna-low | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2-l2steps__r1` | 26,853 | 103,424 | 1,780 | 132,057 |
| `r70-4-ts-bun-fe2-l2steps` | steps | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-4-ts-bun-fe2-l2steps__r2` | 17,101 | 198,400 | 2,792 | 218,293 |
| `r70-4-ts-bun-fe2-l2steps` | steps | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l2steps__r1` | 35,638 | 237,824 | 21,900 | 295,362 |
| `r70-4-ts-bun-fe2-l2steps` | steps | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l2steps__r2` | 46,346 | 620,032 | 25,218 | 691,596 |
| `r70-7-rust` | none | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust__r1` | 27,266 | 149,760 | 3,384 | 180,410 |
| `r70-7-rust-l2approach` | approach | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust-l2approach__r1` | 13,258 | 119,552 | 3,324 | 136,134 |
| `r70-7-rust-l2approach` | approach | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust-l2approach__r2` | 33,481 | 166,144 | 5,522 | 205,147 |
| `r70-7-rust-l2approach` | approach | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-7-rust-l2approach__r1` | 46,385 | 220,928 | 15,984 | 283,297 |
| `r70-7-rust-l2approach` | approach | Luna-max | 2 | bulk | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-7-rust-l2approach__r2` | 27,476 | 220,160 | 13,087 | 260,723 |
| `r70-7-rust-l2criteria` | criteria | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust-l2criteria__r1` | 24,048 | 189,184 | 3,503 | 216,735 |
| `r70-7-rust-l2criteria` | criteria | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust-l2criteria__r2` | 18,204 | 123,648 | 2,959 | 144,811 |
| `r70-7-rust-l2criteria` | criteria | Luna-max | 1 | gate | VALID | FAIL | `codex__gpt-6-luna__max__default__r70-7-rust-l2criteria__r1` | 41,237 | 293,376 | 16,574 | 351,187 |
| `r70-7-rust-l2criteria` | criteria | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-7-rust-l2criteria__r2` | 65,051 | 375,552 | 15,298 | 455,901 |
| `r70-7-rust-l2steps` | steps | Luna-low | 1 | gate | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust-l2steps__r1` | 31,485 | 222,720 | 3,563 | 257,768 |
| `r70-7-rust-l2steps` | steps | Luna-low | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__low__default__r70-7-rust-l2steps__r2` | 29,076 | 147,712 | 4,382 | 181,170 |
| `r70-7-rust-l2steps` | steps | Luna-max | 1 | gate | VALID | PASS | `codex__gpt-6-luna__max__default__r70-7-rust-l2steps__r1` | 43,185 | 441,344 | 19,205 | 503,734 |
| `r70-7-rust-l2steps` | steps | Luna-max | 2 | bulk | VALID | PASS | `codex__gpt-6-luna__max__default__r70-7-rust-l2steps__r2` | 39,815 | 371,200 | 16,648 | 427,663 |

## Descriptive full-task outcomes

- Luna-low no-plan cells: 1/6.
- Luna-low criteria: 4/12; approach: 4/12; steps: 6/12.
- Luna-max criteria: 6/12; approach: 7/12; steps: 6/12.
- Historical Luna-max no-plan baseline: 20/32 valid official cells; this is unrandomized historical context.

## Primary Luna-low paired comparison

| Measure | Steps vs criteria |
|---|---:|
| Steps-only wins | 3 |
| Criteria-only wins | 1 |
| Ties | 8 |
| Net (wins − losses) | 2 |

| Source task | Rep | Steps | Criteria | Pair result |
|---|---:|---|---|---|
| `r70-2-elixir` | 1 | PASS | FAIL | steps win |
| `r70-2-elixir` | 2 | PASS | FAIL | steps win |
| `r70-2-go` | 1 | PASS | FAIL | steps win |
| `r70-2-go` | 2 | FAIL | FAIL | tie |
| `r70-4-elixir-fe2` | 1 | FAIL | FAIL | tie |
| `r70-4-elixir-fe2` | 2 | FAIL | FAIL | tie |
| `r70-4-go-fe2` | 1 | FAIL | FAIL | tie |
| `r70-4-go-fe2` | 2 | FAIL | FAIL | tie |
| `r70-4-ts-bun-fe2` | 1 | FAIL | PASS | criteria win |
| `r70-4-ts-bun-fe2` | 2 | PASS | PASS | tie |
| `r70-7-rust` | 1 | PASS | PASS | tie |
| `r70-7-rust` | 2 | PASS | PASS | tie |

The preregistered adoption screen required net +3 across 12 pairs and lower total tokens per official pass than criteria. The observed net was +2; steps do not meet the adoption screen. The observed one-sided exact sign test, excluding ties, is p = 5/16 = 0.3125 (3 wins among 4 discordant pairs). The minimal +3 screen outcome of three wins and zero losses would still have p = 1/8 = 0.125; treat this as a pilot screen, not confirmatory evidence.

## Planner receipts

The 18 frozen-plan generations used Luna-max. Receipt components sum to uncached 138,159, cached 694,784, output 54,278, total 887,221 tokens.

## Tokens per official pass

Each plan receipt is included in the cost view. Amortized charges allocate one plan receipt over its four planned uses (two builder efforts × two reps). One-off charges assign the full receipt to each task-level scored result. Cost totals keep uncached input, cached input, and output separate; no dollar conversion or wall-time combination is used.

### Amortized planning cost

- **criteria / Luna-low:** 4 of 12 cells passed; builder uncached/cached/output/total = 414,191/4,133,888/50,431/4,598,510; plan charge uncached/cached/output/total = 21,434.5/116,992/5,899.5/144,326; combined charged uncached/cached/output/total = 435,625.5/4,250,880/56,330.5/4,742,836; tokens per official full-task pass = 1,185,709.
- **criteria / Luna-max:** 6 of 12 cells passed; builder uncached/cached/output/total = 1,039,523/32,503,296/449,729/33,992,548; plan charge uncached/cached/output/total = 21,434.5/116,992/5,899.5/144,326; combined charged uncached/cached/output/total = 1,060,957.5/32,620,288/455,628.5/34,136,874; tokens per official full-task pass = 5,689,479.
- **approach / Luna-low:** 4 of 12 cells passed; builder uncached/cached/output/total = 240,542/2,298,624/42,308/2,581,474; plan charge uncached/cached/output/total = 27,432.5/112,384/7,984/147,800.5; combined charged uncached/cached/output/total = 267,974.5/2,411,008/50,292/2,729,274.5; tokens per official full-task pass = 682,318.6.
- **approach / Luna-max:** 7 of 12 cells passed; builder uncached/cached/output/total = 1,096,644/24,696,832/445,379/26,238,855; plan charge uncached/cached/output/total = 27,432.5/112,384/7,984/147,800.5; combined charged uncached/cached/output/total = 1,124,076.5/24,809,216/453,363/26,386,655.5; tokens per official full-task pass = 3,769,522.2.
- **steps / Luna-low:** 6 of 12 cells passed; builder uncached/cached/output/total = 470,772/4,136,192/66,796/4,673,760; plan charge uncached/cached/output/total = 20,212.5/118,016/13,255.5/151,484; combined charged uncached/cached/output/total = 490,984.5/4,254,208/80,051.5/4,825,244; tokens per official full-task pass = 804,207.3.
- **steps / Luna-max:** 6 of 12 cells passed; builder uncached/cached/output/total = 983,909/24,371,712/438,152/25,793,773; plan charge uncached/cached/output/total = 20,212.5/118,016/13,255.5/151,484; combined charged uncached/cached/output/total = 1,004,121.5/24,489,728/451,407.5/25,945,257; tokens per official full-task pass = 4,324,209.5.

### One-off planning cost

- **criteria / Luna-low:** 4 of 12 cells passed; builder uncached/cached/output/total = 414,191/4,133,888/50,431/4,598,510; plan charge uncached/cached/output/total = 85,738/467,968/23,598/577,304; combined charged uncached/cached/output/total = 499,929/4,601,856/74,029/5,175,814; tokens per official full-task pass = 1,293,953.5.
- **criteria / Luna-max:** 6 of 12 cells passed; builder uncached/cached/output/total = 1,039,523/32,503,296/449,729/33,992,548; plan charge uncached/cached/output/total = 85,738/467,968/23,598/577,304; combined charged uncached/cached/output/total = 1,125,261/32,971,264/473,327/34,569,852; tokens per official full-task pass = 5,761,642.
- **approach / Luna-low:** 4 of 12 cells passed; builder uncached/cached/output/total = 240,542/2,298,624/42,308/2,581,474; plan charge uncached/cached/output/total = 109,730/449,536/31,936/591,202; combined charged uncached/cached/output/total = 350,272/2,748,160/74,244/3,172,676; tokens per official full-task pass = 793,169.
- **approach / Luna-max:** 7 of 12 cells passed; builder uncached/cached/output/total = 1,096,644/24,696,832/445,379/26,238,855; plan charge uncached/cached/output/total = 109,730/449,536/31,936/591,202; combined charged uncached/cached/output/total = 1,206,374/25,146,368/477,315/26,830,057; tokens per official full-task pass = 3,832,865.3.
- **steps / Luna-low:** 6 of 12 cells passed; builder uncached/cached/output/total = 470,772/4,136,192/66,796/4,673,760; plan charge uncached/cached/output/total = 80,850/472,064/53,022/605,936; combined charged uncached/cached/output/total = 551,622/4,608,256/119,818/5,279,696; tokens per official full-task pass = 879,949.3.
- **steps / Luna-max:** 6 of 12 cells passed; builder uncached/cached/output/total = 983,909/24,371,712/438,152/25,793,773; plan charge uncached/cached/output/total = 80,850/472,064/53,022/605,936; combined charged uncached/cached/output/total = 1,064,759/24,843,776/491,174/26,399,709; tokens per official full-task pass = 4,399,951.5.

### No-plan cost context

Current Luna-low no-plan cells: 1/6 passed; uncached/cached/output/total = 139,626/930,048/18,031/1,087,705; tokens per official full-task pass = 1,087,705. No planner charge applies, so both planning-cost views coincide. The historical Luna-max no-plan baseline is reported for outcome context only and is not mixed into the L2 planning-cost comparison.

## Grading provenance note

The final two EU rep-2 cells, `r70-4-elixir-fe2-l2criteria` and `r70-4-elixir-fe2-l2steps`, were officially graded with grade_worker SHA prefix `0e6f8aa0` rather than `73dc09af`. The difference was an inventory-glob-only change; scoring code was byte-identical. The result rows above use the latest official row for each exact cell ID.
