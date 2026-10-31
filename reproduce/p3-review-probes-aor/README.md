# p3-review-probes-aor

A Kogen patch that adds review probes (P3) did not help. **On 13 Go tasks it passed the hidden checks on 9, against 11 for unpatched Kogen**: it gained one task and lost three, net -2, while the keep rule needed at least +3. On 6 Ruby on Rails feature tasks (AoR) the patch changed no pair's result (see below), so it cannot add the net wins the rule needs. Verdict: **no** (patch dropped; Kogen stays as it is). Finished 31 October 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task, cells interleaved.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p3 | review probes (`patch/p3-review-probes.diff`) | 608a6654c65e923bd3acfae4cdf251fb1a80accaa9fa620c860ee37031f6dd2e as run; the published copy has one test e-mail address on one line replaced by `<redacted>` (its own hash is in `patch/p3-review-probes.diff.sha256`) |

- **Go half:** 13 Go tasks (G01 to G13) on one Linux host, hidden checks of each task; a cell passes only if every hidden check passes.
- **AoR half:** 6 Rails feature tasks (A1 to A6, alphabetical: activity-feed-api, cancelled-account-cleanup, comment-reaction-live-echo, entropy-sweep, kamal-deploy, saas-billing) on a Mac host, graded by each task's own hidden test file after the build.

## Result: Go tasks

| Arm | Hidden pass | Wall s | Tokens |
| --- | --- | --- | --- |
| b0 | 11/13 | 4443 | 4602234 |
| p3 | 9/13 | 5146 | 4986350 |

Wall and tokens are summed per cell and **include cells that ended build_blocked, review_blocked or no_progress**. Pairs that differ: p3 gains G04 (b0 was build_blocked); p3 loses G01 and G03 (build_blocked) and G13 (20 of 21 hidden checks). G08 fails in both arms. Cost stays within 1.5 times (wall 1.16, tokens 1.08). The probe event fired in 10 of 13 p3 cells; in two of the three lost cells (G01, G03) it never fired, so those losses may be build-stage variance at one trial.

## Result: AoR tasks

**Grading incomplete; it cannot change the verdict.** 12 cells ran (one trial per arm). Outcomes: b0 landed 1, ended asking questions 4, refused 1; p3 landed 2, refused 1, build_blocked 1, questions 1, memory_cap 1 (the build host's 3 GB memory limit, peak 3.33 GB; an infrastructure end, reported as such, not rerun). Five cells were graded when this result was written and **none passed**: A1 (both arms, nothing built; 3 of 17 checks, the always-passing regression ones), A2 (both arms landed, b0 4 of 8, p3 3 of 8), A3 b0 (2 of 9). One p3 cell that landed (A4) was still waiting for the grader; b0 did not land on A4, so even a pass would add one win. Counting a cell that did not land as no pass: 0 wins, 0 losses, 5 pairs without difference, 1 open. The best possible AoR total is +1, so the net across both halves stays below the +3 the rule needs.

Graded cells show the hidden checks separate built from unbuilt work: an unbuilt tree passes only the 3 or 4 regression checks, while each task's reference solution passed all of its checks twice in qualification. The per-pair table is in `expected-output.txt` section 5.

## Limits

- One trial per arm per task, so a difference of one task is within run-to-run variance. The decision rests on the pre-set rule (net wins at least +3), which the Go half alone already misses.
- Intent validity and acceptance separation are not scored by the harness for these cells; the numbers above are the hidden-check results only.
- The Go cells ran with a cold Go cache on a laptop-class host, so wall times are not comparable with other hosts.
- Cost is recorded as token counts; the model has no listed price.

## Reproduce the numbers

```sh
python3 -I reproduce/p3-review-probes-aor/report.py reproduce/p3-review-probes-aor/data | diff - reproduce/p3-review-probes-aor/expected-output.txt
```

`report.py` uses only the standard library. `data/go_cells.tsv` and `data/aor_cells.tsv` have one row per cell. Task names, hidden suites and logs are not included.

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with the patch applied, the same tasks and a ChatGPT login.
