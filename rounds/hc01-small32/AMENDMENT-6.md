# HC01 amendment 6: official grading moves from the Mac Studio to the MacBook (conditional on a parity control)

Recorded 2026-10-08T13:44Z, before any HC01 analysis or decision computation and before any MacBook grade. At recording time 18 of 32 HC01 cells have official grades, all from the Studio route; cell 19 (syn-06 ON r3) ended at 13:42:41Z and is being graded on the Studio as usual. No D, McNemar, bootstrap or guard value has been computed.

## Why
Ruling by the coordinator (careful-rebuild-f2), relaying the owner's request on 2026-10-08: the Mac Studio is to be reinstalled. The change is operational and outcome-blind: the grading location is chosen from the machine schedule, without reference to any grade.

## What changes
1. **Where the grader runs.** The official route (night_grade v2 / mac-private-v2) runs on the MacBook instead of over ssh on the Studio, via `levers/hc01-lane/grade-local/grade_cell_local.sh` (sha256 461c71daf100f5d36d52d145728548f3ecaee23798567a1640d40284a870eb29). The AMENDMENT-4 count route runs there too, via `grade_cell_counts_v2_local.sh` (04b69623144b487910da76f4db5b97ac364e0893a420ebff013f92d65818144f).
2. **Grader code: unchanged and byte-identical.** The MacBook copy `~/bench/night-2026-10-01` matches the Studio's: runner/bench.py 089c63ed…, runner/concurrent_grade.py d40b7562…, tools/night_grade.py 4f35bbe9…, night-env.sh 4bdbaebb…. The count-route copies in `~/bench/hc01-grade-counts` have the recorded shas: night_grade_counts_v2.py fc5d6884…, run_counts_v2.sh 1296046f…, filter_stream.py 7ddb4967…, safe_rows.py 28579898….
3. **Sealed suites.** These are staged from the MacBook's `~/bench-sealed`, which was already the source that grade_cell.sh pushed to the Studio for every earlier grade.
4. **Task root.** `BENCH_TASKS=~/bench/hc01-grade-tasks` is a byte copy of the Studio's grading task root. The tree digests of synthetic/bin (1d5cdeb3, 31 files), warm (d7ded606, 3,364), trackline (c16b8678, 3,641) and ports (00c247ca, 1,179) all equal the Studio's. The task root also holds the 4 HC01 task dirs.
   - The MacBook's own `~/bench/tasks` differs and is not used.
   - The only edit is the absolute path prefix `…/bench/tasks/` → `…/bench/hc01-grade-tasks/` in the 4 task.json files. The as-run and relocated shas are in `~/bench/hc01-grade-tasks-asrun/RELOCATION.txt`, and the as-run copies are kept there.
   - The withheld-source-artifact files are unchanged.
5. **Toolchain.** It is pinned by each task.json env (BENCH_EXTRA_PATH = elixir 1.20.2-otp-29 and erlang 29.0.3), not by the login PATH.
   - Erlang 29.0.3: the install tree is byte-identical on both machines (6b21201b…, 3,438 files).
   - Elixir 1.20.2-otp-29: compiler and libraries are identical. The install's `.mix` differs only in a phx_new generator archive (1.8.9 on the MacBook, 1.8.15 on the Studio) and two dialyzer PLT caches; none of these is used by `mix test`.
6. **Recorded OS differences.** macOS 26.6.2 on the MacBook vs 26.7.1 on the Studio, which affects the sandbox-exec and system frameworks. `/usr/bin/python3` is Python 3.9.6 on both, supplied by each OS.
7. **Raw-output retention.** AMENDMENT-4 §3 still applies: the output is staged locally at 0600 in a 0700 directory, piped to the US root store, and removed locally only after the shas match.

## Parity control (gate for the switch)
Before the switch, two already-graded cells are re-graded on the MacBook through the new route. The work-file prefixes are distinct, the US store files carry a `.macparity` tag, and no official file is overwritten.
- **board OFF r1** (official: FAIL; AMENDMENT-4 count 8/9): the verdict and the count must both match.
- **syn-06 OFF r1** (official: PASS): the verdict must match.

**Switch only if both match.** Otherwise grading stays on the Studio, this amendment is marked "not applied", and the coordinator is told.

The parity re-grades are controls. They never replace or modify any official grade.

## What does not change
- Every cell's VERDICT is its official grade from whichever route graded it.
- The Studio grades stay valid.
- The rules of AMENDMENT-1 through AMENDMENT-5 stand.
- Each grade row records its route: `grader`/`host` fields, plus `route: macbook-local` on count rows.
