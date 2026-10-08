# Captured grade IDs and public official-export scope

The refreshed public `grades.final.jsonl` export exact-joins **5,020/5,020** unique captured graded IDs using `source_record_id == public_cell_id == grades.final.jsonl cell_id`, with unique IDs on both sides. The pre-refresh snapshot at benchmark commit `58c9ca5ee40fb958c61c61e381191a922886f88f` (2026-10-07T16:18:30+03:00; export SHA-256 `cbf85effb6334c650fa0204da6e2777ed8a5a699f14ab854529d998b5177703a`) matched 4,892 IDs; the 2026-10-07 refresh appended the remaining 128 authoritative post-cut official-grade rows. The refreshed export SHA-256 is `4d639a3848b3661dcb5646630b6a4914e5053ff4b94ab029424d47d040e3c977`. The validator now reports zero capture-reported-only mappings.

The 128 added rows comprise **84 model PASS, 19 model FAIL, and 25 invalid `control_apply` rows**. Those 25 rows have `result=invalid` and `outcome=fail`; they are controls, not model failures. The cells export represents these official results as `invalid` and leaves their ITT outcome unresolved or not scored under the existing control policy.

The before/after tables classify each official row by its source `kind` and `result`. Before this refresh, `cells.*` displayed the two already-present invalid controls in these target rounds as `outcome=fail`; the regenerated export now displays their official `result=invalid` classification while preserving their prior ITT handling. The exporter applies this classification consistently to all 199 `control_apply` rows in the refreshed input, including the 25 additions.

| Round | Official rows before (snapshot 58c9ca5, 2026-10-07T16:18:30+03:00) | Rows added | Official rows after | Added model PASS / FAIL | Added invalid controls |
|---|---:|---:|---:|---:|---:|
| r69 | 95 | 55 | 150 | 46 / 9 | 0 |
| r67b | 1 | 42 | 43 | 17 / 8 | 17 |
| r71 | 18 | 31 | 49 | 21 / 2 | 8 |
| **Total** | **4,892** | **128** | **5,020** | **84 / 19** | **25** |

The builder [reproduce/build_grade_join.py](../reproduce/build_grade_join.py) checks equality and uniqueness for all 5,020 captured IDs, requires each to have an official-export row, and rebuilds `grade-join.csv` and the corresponding exact links in the indexed [source-crosswalk partitions](source-crosswalk/index.json).

## Capture identity mappings and public-export matches by round and venue

| Round | Capture ID mappings | Studio | US | EU | MacBook | Public official-export matches |
|---|---:|---:|---:|---:|---:|---:|
| r1 | 48 | 21 | 12 | 15 | 0 | 48 |
| r10 | 12 | 0 | 6 | 6 | 0 | 12 |
| r11 | 25 | 25 | 0 | 0 | 0 | 25 |
| r12 | 24 | 0 | 12 | 12 | 0 | 24 |
| r13 | 20 | 20 | 0 | 0 | 0 | 20 |
| r14 | 10 | 10 | 0 | 0 | 0 | 10 |
| r15 | 25 | 25 | 0 | 0 | 0 | 25 |
| r16 | 18 | 0 | 9 | 9 | 0 | 18 |
| r17 | 35 | 29 | 3 | 3 | 0 | 35 |
| r18 | 20 | 20 | 0 | 0 | 0 | 20 |
| r19 | 42 | 30 | 6 | 6 | 0 | 42 |
| r2 | 64 | 39 | 12 | 13 | 0 | 64 |
| r20 | 6 | 6 | 0 | 0 | 0 | 6 |
| r21 | 31 | 19 | 6 | 6 | 0 | 31 |
| r22 | 39 | 30 | 0 | 9 | 0 | 39 |
| r23 | 29 | 23 | 6 | 0 | 0 | 29 |
| r24 | 40 | 20 | 10 | 10 | 0 | 40 |
| r25 | 36 | 0 | 18 | 18 | 0 | 36 |
| r26 | 49 | 34 | 6 | 9 | 0 | 49 |
| r27 | 150 | 60 | 42 | 48 | 0 | 150 |
| r28 | 41 | 27 | 5 | 9 | 0 | 41 |
| r29 | 73 | 43 | 0 | 30 | 0 | 73 |
| r3 | 105 | 15 | 42 | 48 | 0 | 105 |
| r30 | 109 | 79 | 12 | 18 | 0 | 109 |
| r31 | 17 | 12 | 5 | 0 | 0 | 17 |
| r32 | 15 | 10 | 5 | 0 | 0 | 15 |
| r32b | 11 | 11 | 0 | 0 | 0 | 11 |
| r33 | 75 | 21 | 30 | 24 | 0 | 75 |
| r34 | 10 | 0 | 5 | 5 | 0 | 10 |
| r34b | 2 | 2 | 0 | 0 | 0 | 2 |
| r35 | 32 | 32 | 0 | 0 | 0 | 32 |
| r36 | 30 | 12 | 6 | 12 | 0 | 30 |
| r37 | 62 | 28 | 22 | 12 | 0 | 62 |
| r37c | 25 | 20 | 5 | 0 | 0 | 25 |
| r38 | 5 | 5 | 0 | 0 | 0 | 5 |
| r39 | 1 | 1 | 0 | 0 | 0 | 1 |
| r39b | 11 | 11 | 0 | 0 | 0 | 11 |
| r4 | 42 | 18 | 12 | 12 | 0 | 42 |
| r40 | 20 | 14 | 3 | 3 | 0 | 20 |
| r41 | 10 | 0 | 5 | 5 | 0 | 10 |
| r42 | 12 | 0 | 6 | 6 | 0 | 12 |
| r43 | 29 | 29 | 0 | 0 | 0 | 29 |
| r44 | 12 | 0 | 6 | 6 | 0 | 12 |
| r45 | 63 | 48 | 6 | 9 | 0 | 63 |
| r46 | 65 | 50 | 6 | 9 | 0 | 65 |
| r47 | 54 | 39 | 6 | 9 | 0 | 54 |
| r48 | 60 | 45 | 6 | 9 | 0 | 60 |
| r48b | 14 | 11 | 3 | 0 | 0 | 14 |
| r49 | 62 | 32 | 12 | 18 | 0 | 62 |
| r49b | 23 | 0 | 9 | 14 | 0 | 23 |
| r5 | 12 | 12 | 0 | 0 | 0 | 12 |
| r50 | 174 | 129 | 18 | 27 | 0 | 174 |
| r51 | 191 | 143 | 24 | 24 | 0 | 191 |
| r52 | 1 | 1 | 0 | 0 | 0 | 1 |
| r53 | 106 | 32 | 37 | 37 | 0 | 106 |
| r53b | 47 | 34 | 7 | 6 | 0 | 47 |
| r54 | 30 | 0 | 12 | 18 | 0 | 30 |
| r55 | 30 | 0 | 18 | 12 | 0 | 30 |
| r56 | 200 | 80 | 60 | 60 | 0 | 200 |
| r56b | 226 | 226 | 0 | 0 | 0 | 226 |
| r56c | 127 | 71 | 38 | 18 | 0 | 127 |
| r56d | 14 | 12 | 1 | 1 | 0 | 14 |
| r56p2 | 321 | 65 | 176 | 80 | 0 | 321 |
| r57 | 41 | 0 | 41 | 0 | 0 | 41 |
| r57b | 96 | 96 | 0 | 0 | 0 | 96 |
| r57c | 80 | 0 | 0 | 80 | 0 | 80 |
| r57d | 96 | 96 | 0 | 0 | 0 | 96 |
| r57e | 78 | 78 | 0 | 0 | 0 | 78 |
| r58 | 93 | 0 | 78 | 15 | 0 | 93 |
| r58b | 4 | 0 | 4 | 0 | 0 | 4 |
| r59 | 60 | 60 | 0 | 0 | 0 | 60 |
| r6 | 45 | 15 | 15 | 15 | 0 | 45 |
| r60 | 129 | 129 | 0 | 0 | 0 | 129 |
| r60b | 33 | 33 | 0 | 0 | 0 | 33 |
| r61 | 34 | 0 | 21 | 13 | 0 | 34 |
| r62 | 18 | 0 | 10 | 8 | 0 | 18 |
| r62b | 72 | 0 | 36 | 36 | 0 | 72 |
| r63 | 34 | 34 | 0 | 0 | 0 | 34 |
| r63b | 47 | 47 | 0 | 0 | 0 | 47 |
| r64 | 38 | 38 | 0 | 0 | 0 | 38 |
| r64b | 61 | 61 | 0 | 0 | 0 | 61 |
| r64c | 90 | 90 | 0 | 0 | 0 | 90 |
| r64d | 19 | 19 | 0 | 0 | 0 | 19 |
| r64e | 27 | 27 | 0 | 0 | 0 | 27 |
| r65 | 16 | 0 | 10 | 6 | 0 | 16 |
| r65b | 90 | 0 | 56 | 34 | 0 | 90 |
| r66 | 20 | 0 | 15 | 5 | 0 | 20 |
| r67 | 1 | 0 | 1 | 0 | 0 | 1 |
| r67b | 43 | 0 | 23 | 20 | 0 | 43 |
| r68 | 8 | 0 | 5 | 3 | 0 | 8 |
| r68b | 24 | 0 | 12 | 12 | 0 | 24 |
| r69 | 150 | 150 | 0 | 0 | 0 | 150 |
| r7 | 27 | 26 | 0 | 1 | 0 | 27 |
| r71 | 49 | 0 | 25 | 24 | 0 | 49 |
| r8 | 35 | 20 | 6 | 9 | 0 | 35 |
| r9 | 20 | 20 | 0 | 0 | 0 | 20 |
| unmapped | 50 | 4 | 19 | 19 | 8 | 50 |
| **Total** | **5020** | **2874** | **1133** | **1005** | **8** | **5020** |

The `unmapped` row label is retained from the crosswalk and does not identify a numbered round. This table groups the capture identity map by round and venue. After the 2026-10-07 refresh, the final column equals the capture-ID count for every row: all 5,020 captured graded IDs have a unique exact match in the public official-grade export.
