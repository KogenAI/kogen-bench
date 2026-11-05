# No registered review arm passes Stage 0: today's review already cuts the wide change from 9 parts to 3, but stops on a few thousand tiny paths

Finding `lab-k-review-wide-stage0-20261105`. A model-free Lab (no model call, no seat, 5 Nov 2026), Stage 0 of Lab k-review-wide-change-cost-linear.

## Finding

No registered arm passes the Stage 0 gate. A model-free replay of the K-MODELS-FILE review request sequence (kogen 733363b to 408a1e4, regenerated from the public diff) shows that today's kogen-review main (R0, with 7a9fac6) already cuts the 9-part, 4,142,106-byte legacy sequence to 3 parts and 1,403,877 bytes (66.1% less), and passes the 3x and bounded-growth gates, but it stops on a change of a few thousand tiny paths, because the repeated catalog alone exceeds the 524,288-byte ceiling. R1 fails the same way. R3 as registered (path and status for every other path) sends but inflates to 9.644x on 4,000 paths. R2 fails all three gates. The parked Build (4c421b7, not landed) would pass all three; it is shown only as an informational row.

Same-Build token estimate (not a measurement): the 12,802,581 logged input tokens (11,016,987 cached) and $16.99 become about 4,335,788 tokens (601,819 uncached, 3,733,969 cached) and about $5.74 for R0.

## Question

Does any arm of Lab k-review-wide-change-cost-linear (R0 control, R1 fresh part plus running digest, R2 on_demand material, R3 slice-local catalog) keep the review input of a wide change linear in the change, before any model is run? Stage 0 of the Lab: no model call, no seat. Studio record `lab-review-wide-change-cost-linear-20261105`, revision 2, written before the results.

## Method

- Inputs: public commits only. KogenAI/kogen `733363bdf04a2db673ffcaba643a0f2e0aa37b3f` to `408a1e46d50f1773074d855706c6181891f02165` (the K-MODELS-FILE change, landed as Build 69f25f32); kogen-review `b33665f2509d24ec2f6e48b73ce49ca66671add6` (R0); kogen-build `81a609a3aa9622a9c766bce222e39357b1ca2031` (contains 7a9fac6); kogen-review `4c421b724f654c109e94b2124b8cdc18e0c28304` (the parked Build; present in the delivery object store, not on main).
- The MacBook run dir of the Build is gone, so the sequence is regenerated: `replay.py` is a Python port of kogen-review `review/parts.go` (the cutter: `maxTo`, `endBefore`, `hasRoom`, `reviewPartHeader`, block rule) and of the source layout of `review/material.go`. The source is the diff of the 85 paths (949,115 B of diff for changed paths, 1,973,680 B of changed-file text, 63,792 B of added-file text).
- Calibration: the one-session prompt at 733363b was logged as 3,096,086 B (`k-models-file-1835.log:77`). Subtracting the legacy source (2,992,258 B) leaves 103,824 B of authority, task and executor constraints (the Intent, README and testing rules), the one number fitted. The cut that follows gives 9 parts, which is the logged 9 and was not fitted.
- Fixtures: K9 (the real change, 85 paths); C6, C9, C12 (K9's per-path sizes cycled to 132, 205, 284 paths so that R0's current cut gives 6, 9, 12 parts); T4000 (4,000 tiny paths: path 48 B, diff 326 B for the changed ones, one in ten added with a 354 B text), with T1000, T2000, T8000 as a sweep outside the registered fixtures. The legacy cut gives 6 parts at 51 paths and 13 (not 12) at 112.
- Request = what Kogen sends: the first prompt of each part session (R0, R1, R3, R0'), or the first prompt and each ranged read of the single on_demand session (R2). Prompt length = stable + 4 + header + slice, the executor's `FirstPromptBytes`. Ceiling 524,288 B inclusive, `MaterialPartBytes` 6,000 B.
- Arms: R1 adds a digest of 3,000 B (the size of the existing repaired-paths section) to every part after the first. R2 is `on_demand` as a lane patch: `review_material` is no longer a setting (`project.ReviewMaterial` is always `parts`) and the on_demand text exists only in the native reviewer, so the first prompt carries authority, checks, catalog and a hunk manifest, and each pinned part covering a changed hunk (all of them here) is read by one ranged read that re-sends the context. R3 gives the slice's catalog entries in full and every other path as `{path, status}`. R0' gives the slice's entries in full and the rest only as a count with a retained file (the 4c421b7 header, modelled by its format, not run).
- Gate (Lab, Stage 0): an arm survives only if (1) total input <= 3x the total part size on the registered fixtures, (2) per-request growth beyond a bounded digest is 0, (3) the thousands-of-paths fixture sends. Growth of request k is the bytes of request k that depend on earlier requests, less the digest bound.

## Results

Total first-prompt input over all requests and its ratio to the source bytes the parts carry:

| Arm | K9 (85 paths) | C6 (132 paths) | C9 (205 paths) | C12 (284 paths) | T4000 (4000 paths) |
|---|---|---|---|---|---|
| R0 control (kogen-review b33665f) | 1,403,877 B (1.376x) | 2,700,905 B (1.45x) | 4,272,229 B (1.5x) | 5,849,979 B (1.576x) | stops |
| R1 fresh part + digest | 1,409,877 B (1.381x) | 2,715,905 B (1.458x) | 4,296,229 B (1.508x) | 5,882,977 B (1.585x) | stops |
| R2 on_demand (6 KB reads) | 120,132,024 B (117.707x) | 365,141,712 B (195.982x) | 824,820,416 B (289.536x) | 1,384,735,280 B (373.026x) | stops |
| R2 on_demand (64 KB reads) | 11,658,413 B (11.423x) | 34,318,770 B (18.42x) | 75,728,655 B (26.583x) | 125,114,874 B (33.704x) | stops |
| R3 slice-local catalog (path+status) | 1,380,825 B (1.353x) | 2,482,099 B (1.332x) | 3,880,556 B (1.362x) | 5,062,788 B (1.364x) | 15,707,046 B (9.644x) |
| R0' parked Build 4c421b7 (UNLANDED, informational) | 1,374,263 B (1.347x) | 2,457,569 B (1.319x) | 3,804,494 B (1.335x) | 4,920,684 B (1.326x) | 4,611,560 B (2.832x) |
| legacy 733363b (the Build as run) | 4,142,106 B (1.384x), 9 parts | - | - | - | - |

Number of parts (R2: ranged reads in one session):

| Arm | K9 | C6 | C9 | C12 | T4000 |
|---|---|---|---|---|---|
| R0 control (kogen-review b33665f) | 3 | 6 | 9 | 12 | stops |
| R1 fresh part + digest | 3 | 6 | 9 | 12 | stops |
| R2 on_demand (6 KB reads) | 172 reads | 312 reads | 476 reads | 620 reads | stops |
| R2 on_demand (64 KB reads) | 17 reads | 30 reads | 45 reads | 58 reads | stops |
| R3 slice-local catalog (path+status) | 3 | 5 | 8 | 10 | 30 |
| R0' parked Build 4c421b7 (UNLANDED, informational) | 3 | 5 | 8 | 10 | 9 |

The real change K9, request by request (bytes at request k, non-source material per part, room left):

| Arm | parts | bytes at request 1 / 2 / 3 | non-source bytes per part | room left under 524,288 per part | mandatory (first part) |
|---|---|---|---|---|---|
| R0 control (kogen-review b33665f) | 3 | 503,908 / 522,011 / 377,958 | 127,755 / 127,760 / 127,761 | 20,380 / 2,277 / 146,330 | 127,750 |
| R1 fresh part + digest | 3 | 503,908 / 487,132 / 418,837 | 127,755 / 130,760 / 130,761 | 20,380 / 37,156 / 105,451 | 127,750 |
| R3 slice-local catalog (path+status) | 3 | 516,264 / 523,004 / 341,557 | 116,112 / 116,304 / 127,808 | 8,024 / 1,284 / 182,731 | 111,765 |
| R0' parked Build 4c421b7 (UNLANDED, informational) | 3 | 512,685 / 523,234 / 338,344 | 112,533 / 113,124 / 128,005 | 11,603 / 1,054 / 185,944 | 106,893 |
| R2 on_demand (6 KB reads) | 1 session, 172 requests | 159,792 / 166,092 / 172,392 ... last 1,237,092 | 159,792 then +6,300 per read | 364,496 first, -712,804 last | 159,792 |
| R2 on_demand (64 KB reads) | 1 session, 17 requests | 159,101 / 224,937 / 290,773 ... last 1,212,477 | 159,101 then +65,836 per read | 365,187 first, -688,189 last | 159,101 |
| legacy 733363b | 9 | 503,908 / 522,011 / 512,236 ... | 127,755 each | 2,277 to 365,455 | 127,750 |

Thousands-of-paths sweep (T4000 is the registered fixture):

| Arm | T1000 | T2000 | T4000 | T8000 |
|---|---|---|---|---|
| R0 control (kogen-review b33665f) | 3 parts, 3.731x | stops | stops | stops |
| R1 fresh part + digest | 3 parts, 3.746x | stops | stops | stops |
| R2 on_demand (6 KB reads) | sends, 123.68x | stops | stops | stops |
| R3 slice-local catalog (path+status) | 3 parts, 3.229x | 6 parts, 3.816x | 30 parts, 9.644x | stops |
| R0' parked Build 4c421b7 (UNLANDED, informational) | 3 parts, 3.0x | 5 parts, 2.894x | 9 parts, 2.832x | 18 parts, 2.833x |

Gate:

| Arm | 1. total input <= 3x part size (K9, C6, C9, C12, T4000) | 2. growth beyond a bounded digest = 0 | 3. thousands of paths send | Survives |
|---|---|---|---|---|
| R0 control (kogen-review b33665f) | pass | pass | FAIL | no |
| R1 fresh part + digest | pass | pass | FAIL | no |
| R2 on_demand (6 KB reads) | FAIL | FAIL | FAIL | no |
| R2 on_demand (64 KB reads) | FAIL | FAIL | FAIL | no |
| R3 slice-local catalog (path+status) | FAIL | pass | pass | no |
| R0' parked Build 4c421b7 (UNLANDED, informational) | pass | pass | pass | would survive (not a registered row) |

### Same-Build token estimate

| Same Build 69f25f32 | input tokens | uncached | cached | estimated USD |
|---|---|---|---|---|
| as run (logged, legacy 733363b, 9 parts) | 12,802,581 | 1,785,594 | 11,016,987 | 16.9858 |
| R0 control (kogen-review b33665f), replay | 4,335,788 | 600,992 to 602,923 | 3,733,969 | 5.73 to 5.74 (3.5 B/token: 5.74) |
| R1 fresh part + digest, replay | 4,353,461 | 602,492 to 604,923 | 3,749,927 | 5.75 to 5.76 (3.5 B/token: 5.76) |
| R3 slice-local catalog (path+status), replay | 4,267,889 | 595,229 to 595,239 | 3,672,656 | 5.66 to 5.66 (3.5 B/token: 5.66) |
| R0' parked Build 4c421b7 (UNLANDED, informational), replay | 4,248,561 | 593,052 to 593,588 | 3,655,203 | 5.64 to 5.64 (3.5 B/token: 5.64) |

Method: the legacy replay sends 9 first prompts of 4,142,106 B in total; the logged cached tokens are read as (turns - 1) times the first-prompt tokens, which fixes turns per session at 8.98 to 11.64 for 3 to 4 bytes per token, and the rest of the logged uncached tokens as a per-session extra (tool results and outputs). An arm keeps the same turns and extra per session and its own first-prompt bytes. USD scales the logged $16.99 by the arm's weighted tokens (uncached 1, cached 0.1). Cached tokens come out the same for every byte-per-token value because they scale with prompt bytes.

### What the numbers say

- Today's R0 is not the problem the Lab was filed for. The 12.8 M tokens were nine fresh sessions (at 733363b every part after the first is its own session, `review_external.go`), each a near-ceiling prompt of 158,833 to 522,011 B read about 10.31 times. 7a9fac6 removes the full text of changed files and the same change becomes 3 sessions.
- What R0 still repeats in every part is the authority and the catalog: 127,755 B per part, 81% of it the 103,824 B authority. None of R1 to R3 changes the authority. The cost of the catalog grows with parts x paths: R0's total over source rises with the number of parts: K9 1.376x, C6 1.45x, C9 1.5x, C12 1.576x.
- R1 is R0 plus 6,000 B on K9: the sessions are already fresh, so a digest only adds bytes (its value, if any, is verdict quality, which Stage 2 would measure).
- R2 grows by construction: a required read per part re-sends the whole context, so the sum is quadratic (117.707x on K9 with 6 KB reads, 11.423x with 64 KB reads) and the context passes the 524,288 B window at request 59. Its catalog and manifest also stop the review on T4000.
- R3 as registered keeps 4,000 paths under the ceiling but leaves 458,178 to 485,677 B of non-source per part, so 4,000 tiny paths take 30 parts. The count-only variant (R0') leaves 293,101 to 399,554 B and takes 9 parts.

## Limits

- A Python port of the Go cutter, not the Go code run; it reproduces the logged 9 parts and the logged 3,096,086 B prompt only through the one fitted authority size. The tree is the landed tree 408a1e4, not the pass-2 tree the reviewer saw; the check-results text is assumed 2,500 B; JSON escaping of `<`, `>`, `&` in Go is not modelled.
- The T fixtures reuse K-MODELS-FILE's authority size. A smaller authority moves where each arm breaks, not which gates it fails.
- R1 to R3 are modelled by their request text in `replay.py`, not built as Go patches; Stage 1 is where their code runs. R0' is modelled from its header format; it has not landed, so it is not a registered row and no verdict about it is made.
- The token estimate assumes the same turns per session as the logged Build. It is an estimate from one logged Build, not a measurement.
- Nothing here says which arm gives the better review. No verdict quality was measured.

## Rerun

No model, no seat, about 20 s on a laptop:

```
git clone https://github.com/KogenAI/kogen kogen-src   # public; needs commits 733363b and 408a1e4
python3 -I replay.py kogen-src out
```

`out/results.json` is `data/results.json` of this pack (deterministic). The pins are in `replay.json` and above. `arms-spec.md` states each arm's request text.
