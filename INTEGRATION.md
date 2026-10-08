# Integration summary

This publication branch combines `mine-probe`, `token-audit`, `mine-studio`, `mine-hosts`, `rails-kits`, and `apparatus` in that order. Round IDs and source records are retained as unions where the branches overlapped. The recovered `pilot73` source is registered as a separate descriptive round; it does not represent registered `r73`.

## Recomputable source summaries

Historical rounds are published as labelled records. Each round page declares its original status as a publication badge, recomputation status, and limits; non-VALID records include a `Why not VALID` explanation. The strict Standard capture gate, requiring complete capture and no protocol deviations, applies to new rounds dated 2026-10-09 or later. L3b remains **VALID** for its registered rule and is labelled **NARROW / HISTORICAL**; its 193 missing capture fields remain visible as limits on its page.

**132 mined round tags** now have `recomputed.json` summaries generated from the merged safe-source records. These are observed-source recomputations; they do not by themselves reconstruct every published cohort or headline.

- `claim-b-rerun-1`, `claim-b-screen-1`, `confirm-combined-1`, `e06-context`, `e09-tidewave`, `hard1-calibrate-1`, `harness-compare-1`, `harness-pick-2026-09-29`, `hc-1`, `hc-2`, `hc-3`, `hc-4`, `kh-compare-2026-09-29`, `l1-task-grader-trust`, `night-2026-10-01`, `pilot73`
- `r1`, `r10`, `r11`, `r12`, `r13`, `r14`, `r15`, `r16`, `r17`, `r18`, `r19`, `r2`, `r20`, `r21`, `r22`, `r23`
- `r24`, `r25`, `r26`, `r27`, `r28`, `r29`, `r3`, `r30`, `r31`, `r32`, `r32b`, `r33`, `r34`, `r34b`, `r35`, `r36`
- `r37`, `r37c`, `r38`, `r39`, `r39b`, `r4`, `r40`, `r41`, `r42`, `r43`, `r44`, `r45`, `r46`, `r47`, `r48`, `r48b`
- `r49`, `r49b`, `r5`, `r50`, `r51`, `r52`, `r53`, `r53b`, `r54`, `r55`, `r56`, `r56b`, `r56c`, `r56d`, `r56p2`, `r57`
- `r57b`, `r57c`, `r57d`, `r57e`, `r58`, `r58b`, `r58x-studio`, `r59`, `r6`, `r60`, `r60b`, `r61`, `r62`, `r62b`, `r63`, `r63b`
- `r64`, `r64b`, `r64c`, `r64d`, `r64e`, `r65`, `r65b`, `r66`, `r67`, `r67b`, `r68`, `r68b`, `r69`, `r7`, `r70`, `r70-rve`
- `r70-rve-ext`, `r70-rve-rerun`, `r70-rve-task8v2`, `r71`, `r72`, `r74`, `r8`, `r9`, `unmapped`, `x-context`, `x-ladder`, `x-minikogen`, `x-mining`, `x-models`, `x-parallel`, `x-race`
- `x-recovery`, `x-review`, `x-roles`, `x-surface`

## Published round summaries still not fully recomputable

**51 rounds** still lack enough evidence to reconstruct their complete published cohort or headline. The main gaps are missing planned/ITT denominators, incomplete or unsafe source-to-round joins, absent controls or arms, unavailable records, and historical execution environments that cannot be replayed. Some of these rounds have partial observed-source summaries above. The linked [round-by-round register](rounds/NOT-RECOMPUTABLE.md) records the current recovered counts and the specific reason for each round.

- `campfire-lane1`, `campfire-lane2`, `candidate-counterfactual`, `claim-b-screen-1`, `ctx-store`, `e06-context`, `e09-tidewave`, `frontier`, `grok-frontier`, `harness-pick-2026-09-29`, `intent-coverage-audit`, `jev-route-ctx`, `jev-triage-ctx`, `kh-climb`, `kh-compare-2026-09-29`, `kogen-rs-ladder-luna-r74x`
- `l1-task-grader-trust`, `night-2026-10-01`, `offline-aa-bo3`, `offline-contract-audit`, `offline-review`, `offline-review3`, `overstrict-replay`, `r32a`, `r57-studio`, `r57-t90-studio`, `r70`, `r70-compile`, `r70-task8`, `r73`, `rails-catalogue`, `stack-oneshot-conformance`
- `studio-kogen`, `studio-kogen-80a4`, `studio-shaper-pilot`, `t100-cache-lane`, `t98-cache-smoke`, `unmapped`, `x-compaction`, `x-context`, `x-continuation`, `x-ladder`, `x-minikogen`, `x-mining`, `x-models`, `x-parallel`, `x-race`, `x-recovery`
- `x-review`, `x-roles`, `x-surface`

## Task kits and credits

**Complete task kits: 50.** Each complete kit is marked `kit_complete: true` in its task metadata.

Credits identify **37signals LLC** (Fizzy, Fizzy SaaS, and Writebook), the **Rails Foundation** and **Evil Martians** (Agents on Rails), and **Optimum Tech** (credited harness and fixture bases). Task records identify additional task-specific sources, authorship evidence, licenses, and redistribution terms. See [CREDITS.md](CREDITS.md) and each task's `credits` metadata.

## Size

Tracked files total about **202.3 MB (193.5 MiB)**. No tracked file exceeds 50 MB; the largest is the 13,353,871-byte Rails base bundle. The checked-out tree is about 206 MB including filesystem overhead.
