# HC01 amendment 4: official count source, count diagnostics, private raw retention, transport replacement

Recorded 2026-10-08T08:06Z, before any HC01 analysis or decision computation. At recording time **4 HC01 cells have official grades** (pass/fail only): syn-06 OFF r1 and ON r1 (the smoke pair), and board OFF r1 and ON r1. **No count values have been computed.** The only count runs so far are the two AMENDMENT-3 self-test runs on the smoke pair. Both returned "count unavailable" under the old parser and produced no numbers. No D, McNemar, bootstrap or guard value has been computed.

Rulings by the coordinator (careful-rebuild-f2, relaying the owner's authority and his publication standard), 2026-10-08. AMENDMENT-1 to AMENDMENT-3 stand except where this amendment says otherwise. Frozen documents keep their PRE-LAUNCH-SHA256 hashes.

## Why

The AMENDMENT-2/3 extractor looked for ExUnit's `N tests, M failures` summary. The official grader for these tasks does not report its result in that form; it prints its own summary line, `Result: P/T passed`. Integer-only probes of the retained 800-character official tails of the two graded board cells each show exactly one such line. The instrumented count route (night_grade_counts.py 07570bdb) therefore returned "count unavailable" for both smoke cells even on the full output, so the hidden-test guard could never clear.

## 1. Count source (supersedes the parsing definition in AMENDMENT-2 §1 and AMENDMENT-3 §1)

- **Source:** exactly one line `Result: P/T passed` in the full official runner output. ANSI escapes are removed and the line is stripped of surrounding whitespace before matching.
- **Definitions:** tests_total = T, tests_passed = P, failures = T − P.
- **Unavailable:** zero such lines, more than one, or P > T makes the cell "count unavailable". DECISION-RULE's missing-count clause then applies.
- ExUnit summary parsing is dropped as a count source.

Justification: the extractor now reads the official grader's own summary line. The old regex targeted a format this runner does not emit. The fix is arm-symmetric, blind to outcome, and applies identically to all 32 cells.

## 2. Diagnostics (integers only)

Each count row also records `n_result_lines` and `n_exunit_summaries` (the number of ExUnit-style summary lines in the full output). These are diagnostics only and carry no decision weight.

## 3. Private retention of the full runner output (supersedes AMENDMENT-3 §1's no-retention clause)

The full runner output of each count run is kept privately, so every count can be recomputed by script.

- **Store:** on kogen-bench-us, `/var/lib/kogen-bench-private/hc01-raw/<cell>.out`. The directory is root-owned, mode 0700, and lies outside every lane workdir and sandbox bind; each file is mode 0600.
- **Transfer:** the grader produces the output on the Studio grading worker. It is written there once, mode 0600, to a 0700 stage directory. It is then piped to the US root store (never written to MacBook disk) and deleted from the Studio stage only after the US sha256 equals the Studio sha256.
- **Recorded per cell:** raw_output_bytes, raw_output_sha256 (computed in the grader), raw_store_sha256 (computed on US) and raw_store_verified.
- **Hidden-suite rule:** the content never enters any model context. Scripts that read it emit integers and hashes only.

## 4. Outcome-blind transport replacement (new)

Condition checked: none of the 4 graded cells had a transport failure. All four manifests report status ok with no errors and a non-empty patch (14–19 kB).

- **Clause:** a cell whose provider transport failed is re-run in the same slot (same task, arm, repetition and cell parameters), appended at the end of the schedule.
- **What counts as a transport failure:** an HTTP, stream or auth error before any patch was produced, judged from transport receipts alone (manifest error class, provider/transport errors, empty patch). The outcome is never consulted.
- **Cap:** at most 4 replacements per arm. Reaching the cap makes the run INVALID.
- **Never replaced:** a cell that produced a patch, whatever its grade.
- Both the original and the replacement attempt keep their receipts. The replacement's official grade is the cell's primary grade.

## 5. Implementation (hashes at recording)

| File | SHA-256 |
| --- | --- |
| levers/hc01-lane/grade-counts/v2/night_grade_counts_v2.py (Studio copy at ~/bench/hc01-grade-counts/v2/, outside the night tree) | fc5d6884978f19a9c16972c05f33c59bb96246f38b0b6a5d782ac38881814942 |
| Original Studio night_grade.py (unchanged, read-only) | 4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0 |
| Studio runner engine ~/bench/night-2026-10-01/runner/bench.py (mtime 2026-10-01T20:47:36Z) | 089c63ed13a931b1830250ef3f96171e49f85ae565cbd754a80f0d52838d2147 |
| Studio runner engine concurrent_grade.py (mtime 2026-10-01T19:30:08Z) | d40b756291a1e0f5e346b4ad2f3fb3f74a8bf6f690a551ca423d11a4a9929d05 |

The other v2 files (night_grade_counts_v2.diff, grade_cell_counts_v2.sh, run_counts_v2.sh) have their hashes recorded in levers/hc01-lane/grade-counts/v2/SHA256SUMS at recording time.

The v2 diff against the original night_grade.py removes no lines. The verdict row (`rec.update(pass_=…, outcome=…, …)`) is byte-identical to the original, and the counting and retention run only after that verdict update.

The runner engine hashes had no earlier receipt. Their continuity since the first HC01 grade rests on the files' 2026-10-01 mtimes and is recorded as a partial gap in ENVIRONMENT.

The AMENDMENT-3 rules on verdicts and flakes stand:
- the verdict is always the original official grade;
- a disagreeing count run is a flake, keeps its counts with the flag, and cannot help clear the guard.

All 32 cells, including the 4 already graded, get their counts from one v2 count run. The AMENDMENT-3 v1 rows (grades/hc01-counts.jsonl) are superseded and kept for the record.
