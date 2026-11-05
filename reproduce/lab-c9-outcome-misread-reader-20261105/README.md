# Reading a Build's final outcome instead of its first line: 156 of 157 right, no green Build read as failed

**Finding.** Delivery decided what to do with a failed Build from the first `candidate/`, `intent/` or `shape/` line in its log. Over the 157 failed Builds of 2-5 Nov 2026 that read agreed with the hand-assigned real outcome in 107 cases (68.2%), and delivery recorded 3 of the 4 Builds that were actually green as failed. A reader that takes the Build's final outcome agrees in 156 of 157 (99.4%), reads all 4 green Builds as green, and reads none of 472 further landed Builds as failed. Delivery's own interim fix of 5 Nov (last outcome line; a `landed` line with no `EXIT=` counts as green) already reaches 153 of 157; the reader's extra value is the two "already present at HEAD" Builds, a Build killed during approval, a lost `EXIT=` after a terminated wrapper, and a record of every stop in order.

## Question
Does reading Kogen's final structured stop (not the first matching line), counting a `landed <slug> <sha>` line as success even without `EXIT=`, and counting `EXIT=0` "already present at HEAD" as done, classify at least 95% of Build outcomes correctly and never call a green Build a failure? (Section 3, cluster C9 of the 5 Nov 2026 build-failures analysis; Studio assumption `build-failures-c9-outcome-misread-20261105`; Studio Lab lever `lab-c9-outcome-misread-reader-20261105`.)

## Method
Model-free: no model call, no seat, no host load. The 157 failed Builds classified by hand (73 on two Macs, 84 on three Linux hosts) were each matched to their saved Build log by slug, host and start time. The hand-assigned real outcome is derived only from the hand text (reported code, cluster tag, real-cause sentence); 7 of the 157 were refined from that text after a first pass (column `refined_from_hand_text` in `data/truth.tsv`), and the pack reports both scores. A control set of 472 further Builds whose log has a `landed` line checks that no green Build is read as failed. Arms: the old first-line read (baseline), delivery's interim fix, reader v1 (the three fixes exactly as written) and reader v2 (v1 plus one rule added after the first pass: an approval step that ends `no approval digest:` without a structured line is `intent/not_ready`). `data/skeletons/` holds, for each log, only the lines the reader looks at (step markers, stop codes, `landed`, `EXIT=`, the approval marker); the reader gives the same answer on a skeleton as on the full log for all 629 logs.

## Results
| arm | final-stop agreement (157) | green Builds read as failed (of 4) |
|---|---|---|
| old first-line read | 107 (68.2%) | 3 (as recorded by delivery) |
| delivery interim fix (5 Nov) | 153 (97.5%) | 2 |
| reader v1 | 153 (97.5%) | 0 |
| reader v2 | **156 (99.4%)** | **0** |

- Failed Builds read as green: 0 for every arm. Class agreement (green, red, usage limit, no outcome) for v2: 157 of 157. Control: 472 of 472 landed Builds read as green.
- Against the unrefined truth (the reported code only, no hand-text refinement) v1 scores 146 and v2 149 of 157 (94.9%, just under the 95% bar); the 7 refined rows are flagged in `data/truth.tsv` and are rows where the log's final stop differs from the reported code in the way the hand text says.
- The one miss: a log with `candidate/build_blocked` and, a few lines later, `candidate/recovery_refused` (a custody refusal while keeping the blocked candidate). The reader reports the last stop and keeps the chain `build_blocked>recovery_refused`; the hand reading is `build_blocked`.
- `EXIT=` under signals (sleep-only fake builds, `trap-test.sh`): with today's wrapper a TERM to the wrapper leaves 0 `EXIT=` lines (the failure reproduced) while the child lands; the trap wrapper `run-with-exit.sh` writes `EXIT=143` and stops the child; SIGKILL still loses `EXIT=`, which the `landed` rule covers.

## What this decides
Verdict yes on the registered rule (at least 95% agreement and 0 green read as failed): the reader is handed to delivery with this reader as the reference; no Kogen component changes. Limits: the rules were fitted while looking at these 157 logs, the control set only tests the green side, the hand truth has no second labeller, and the trap wrapper was exercised on a macOS shell only.

## Rerun
```
cd reproduce/lab-c9-outcome-misread-reader-20261105
python3 -I check.py
```
`check.py` runs `read-outcome.py` over `data/skeletons/` (157 hand-classified Builds) and `data/control/` (472 landed Builds), compares with `data/truth.tsv`, prints the table above (`157 rows, 156 agree (v2); 0 green read as failed (v2); 472 of 472 control logs read green`) and writes `data/results.json`. Host names are replaced by `mac-a`, `mac-b`, `linux-a`, `linux-b`, `linux-c`; log text other than step markers, stop codes, `landed` and `EXIT=` lines is omitted. `trap-test.sh <dir> <path to read-outcome.py>` repeats the signal test in a scratch directory (copy `run-with-exit.sh` into that directory first).
