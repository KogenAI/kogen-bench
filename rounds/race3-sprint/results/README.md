# Results guide

Each host/wave directory holds sanitized score tables and operational logs plus `per-case/`. There is one public JSONL for each supplied scored arm-snapshot/tag: 267 files in total. `prio` is the first/priority scoring tag; `rep` is the repeat. Same-name overwritten attempts cannot be recovered from the supplied copies. Historical TSV tables may contain multiple rows for a key; the available per-case file is the retained result for that key.

The public per-case projection retains meta fields (suite, start time, configured jobs, timeout, case count, implementation digest), and case ID, title, suite file, status, no-executable reason, failure count/classification counts, and per-step index/elapsed/exit/timeout. It omits stdout/stderr, captures, observed file contents, request/response and OAuth bodies, process/sandbox bodies and other payload fields. No raw agent event or agent message is included. The source SHA and public SHA are recorded in `result-inventory.tsv` and PROVENANCE.tsv. A source implementation digest is an identifier, not a copy of its source.

Some no-executable results contain all 144 failure rows even when the score-table denominator is 56. `curves.tsv` distinguishes the available result inventory from the 56 scored cases. It does not manufacture /144 passes from subset scores. It derives counts from the retained per-case statuses, not from filenames or historical score strings.

| File | Meaning |
| --- | --- |
| FINAL.tsv | Raw FINAL /144 and /56, observed-flip-adjusted /56, historical search and earliest available crossings. |
| curves.tsv | Every retained first/repeat case-status score, with actual snapshot time and elapsed seconds. |
| flips.tsv | Per-case first/repeat status differences, scoped to the same host/wave/arm. |
| repeat-coverage.tsv | First-pass 47–53-band coverage and missing repeats, including every FINAL's absence of a repeat. |
| reach-counts.tsv | Per-language raw FINAL and observed crossing counts; denominators are explicit. |
| tokens.tsv | FINAL availability and completed-turn usage sums, with coverage flags. |
| token-usage-events.tsv | The 11 available usage events, stream/index/time and numeric usage only. |
| turns-stalls-fastfails.tsv | Attempt files versus actually started/completed turns, resume rejections and logged stalls/fast-fails. |
| cpu-summary.tsv | Peak/p95 sampled whole-process-tree percent CPU by arm; 100 percent is approximately one core. |
| load-summary.tsv | Peak/p95 host one-minute load from the same sample log. |
| snapshot-copy-times.tsv | Completed copy clock, copy duration and elapsed time; duration covers the snapshot set, not an individual arm. |
| audit-summary.tsv | Flag/receipt counts; complete supplied sanitized audit text remains alongside each run. |
| run-clocks.tsv | Actual START, planned deadline and FINAL-copy clocks. |
| result-inventory.tsv | Row/ID coverage and source/export checksums per JSONL. |

All percentiles use nearest rank: sorted sample at ceil(0.95 × N), with no interpolation. Samples are about ten seconds apart and report rounded CPU percentages. The sampler roots process trees at `out/<arm>/pid`; reparented/detached work and handoff races can escape attribution. CPU peaks are observations rather than hard limits or integrated CPU-seconds.

Token method: search structured events for `token_count` and take the last `total_token_usage` before FINAL if present. None is present here. Fallback: sum the numeric `turn.completed.usage` fields up to FINAL, aligned to corresponding `turn-*.ts` event timestamps. Reported total = input_tokens + output_tokens; cached input and reasoning output are subsets and are not added again. The fallback is exactly a sum of reported terminal usage, not an inferred missing active-turn total. Resumed-session receipts may be cumulative or overlap; the supplied CLI streams do not establish independently additive billing usage, so these sums must not be treated as exact cost. All arms were interrupted with an active turn; all FINAL totals are unavailable. Blank values mean missing, not zero.

The supplied streams contain 141 attempt files, 41 started turns and 11 completed turns. There are 100 w1 resume-flag rejection stderr files. The only logged stall is Mac Studio w1 Go after turn 18, the false-positive quota detection in INCIDENT; confirmed quota-stall count is zero in the supplied stall logs. There are no dedicated fast-fail log entries in the copies. The 100 explicit resume rejections are reported separately rather than disappearing into a zero fast-fail count. Absent turns/stall/fast-fail logs mean no copied entry, not proof that no wait or failure occurred. `arms.log` turn numbers are indices, not counts of successful agent turns.

Flakiness adjustment takes the union of observed flipped IDs per host/wave/arm and suppresses passes for those IDs at every snapshot in that run. It never penalizes another arm or another wave. Both raw and adjusted scores are exported. These adjustments are provisional because most repeats and every FINAL repeat are absent. The historical search can disagree with earliest observed crossing because it gates on FINAL and binary-searches a nonmonotone curve.
