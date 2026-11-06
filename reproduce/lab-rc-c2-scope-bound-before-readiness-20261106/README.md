# Lab RC-C2: the scope size bound counts files the review never carries, and the one change that passes it removes the gate

**Finding.** After Lab C's decision-record change, shaping stops next at the scope gate on three of four recorded shapes: one review of the attempt-1 package is estimated at 1,348,267, 1,182,205 and 1,194,443 bytes against a 524,288-byte bound. The bytes are not the package. The Intent package (Intent text, acceptance feature, step files, model) is 87 to 140 KB, 7 to 10% of each estimate. The other 90 to 93% is the size at HEAD of every file the Intent names in backticks, whether it is to be changed or not, and one generated data file of 597,140 bytes is 44 to 50% on its own. The review stage uses the same 524,288-byte constant but measures a different thing: its prompt holds the Intent, feature and model, the check results, the diff of changed files and the text of added files, and a source over the bound is reviewed in ordered parts, not refused. Counting generated data and repeated lines once is not enough (all three stay 12 to 43% over). One line that stops adding named files to the estimate lets the scope gate pass on 3 of 3 oversize trees and still refuses a package whose own text is over the bound, but it fails 4 of the delivered scope tests, and a package that large already ends shaping at the shaper's own context window, so the change removes what the gate does. The registered rule (no new suite failure) is not met: the verdict is no and no change is requested. Readiness still runs on 0 of 4. No model call was made.

## Question

kogen-shaping [`c3f9c5e`](https://github.com/KogenAI/kogen-shaping/commit/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3) refuses a candidate whose estimated one-review size is over `tools.InputBudgetBytes` (524,288). Lab C found three of four kept shapes stop there after its decision change. What does the bound measure, where do the 1.18 to 1.35 MB go, could the same behaviour fit under the bound, and does a small change let the scope gate pass without letting a truly oversize package through?

## Arms

All arms are kogen-shaping `c3f9c5e`, the commit pinned in release [`3607552`](https://github.com/KogenAI/kogen/commit/360755276001531e5f9182d74fb72717f89ccfb4), built with Go 1.27.2 on one Mac Studio as an unprivileged user.

- **A:** the commit as it is. Alone it never reaches the scope gate: the attempt-1 package of every tree stops at the decision-record gate (Lab C).
- **A+:** A plus the decision-record change of Lab C, used only so the scope gate is reachable. The scope gate is judged against this arm.
- **B:** A+ plus a one-line change in the scope estimate: a named file is still listed in the refusal and counted in areas, but its size at HEAD is no longer added to the estimate (the review prompt carries a changed file as a diff and an unchanged one not at all). The patch is not copied here; it is the removal of one `estimate += size` line. A rewritten variant of the four scope tests it breaks is described under Results.

Review stage read at kogen-review [`66be20d`](https://github.com/KogenAI/kogen-review/commit/66be20d31658), kogen-loop at [`31036b2`](https://github.com/KogenAI/kogen-loop/commit/31036b2c02e8) (shaping's pin; review's pin `dea3eb3` has the same constant).

## Method

1. **What the bound measures.** Read the scope estimate and its bound in kogen-shaping, and the review stage's use of the same constant.
2. **Bytes per class.** For each of the four recorded attempt-1 packages, re-implement the gate's own rules (package files, plus HEAD size of every backticked path that is a tracked blob outside `.kogen/` and outside the package) and split the estimate by class (`analyze.py`; `data/breakdown.json`). The totals equal the gate-measured ones for two trees; the third is 637 bytes higher because the gate formats its package.
3. **Measured once.** Recompute the estimate with the generated file counted as zero, with repeated and copied lines counted once, with the package only, and with the review authority only.
4. **Reach replay.** Shape a clean copy of each tree with a stub shaper that submits the recorded attempt-1 package every round and stub checker sessions that answer "no findings", through A, A+ and B; record the gate that stops it and whether readiness ran (`data/reach.json`). The model provider was a closed port; `model_calls` is 0 in all 12 replays.
5. **Synthetic packages.** One small, one that names a 600,000-byte file at HEAD, one whose own text is 540,440 bytes, through the gate function of A and B (`data/synthetic.json`).
6. **Suite.** `go test -count=1 -v ./...` on A, on B with the delivered scope tests, and on B with the four tests it breaks rewritten or removed (`data/suite-counts.tsv`).

Every Go command ran one at a time under the host's heavy-check lock.

## Results

Where the numbers come from (file and line at the pinned commits): the estimate is the package bytes plus the HEAD size of each named file (`shape/scope.go`, `scopeLines`), the bound is `tools.InputBudgetBytes` (`shape/scope.go`, `scopeRefusal`) which is `provider.InputBudgetBytes = 524288` ("the inclusive ceiling of one complete next request", kogen-loop `provider/respond.go:99-100`). The review stage reads the same constant (`review/parts.go:42`), measures its exact first prompt, and above the bound reviews in ordered parts (`review/external.go:150`), stopping only when mandatory material leaves under 6,000 bytes of room (`review/parts.go:225`).

Bytes per class (T1 is the Go repository and was never over the bound; T2 to T4 are an Elixir and Go repository):

| class | T2 | T3 | T4 | T1 |
|---|---|---|---|---|
| estimate | 1,348,267 | 1,182,842 | 1,194,443 | 55,996 |
| Intent text | 39,241 | 34,231 | 23,557 | 10,922 |
| acceptance feature | 45,045 | 29,963 | 34,720 | 1,597 |
| step files | 52,953 | 36,480 | 25,291 | 9,482 |
| model | 2,941 | 2,789 | 3,747 | 0 |
| package total (share) | 140,180 (10.4%) | 103,463 (8.8%) | 87,315 (7.3%) | 22,001 (39.3%) |
| named generated data file (1 file) | 597,140 (44.3%) | 597,140 (50.5%) | 597,140 (50.0%) | 0 |
| named existing tests | 462,028 (34.3%) | 260,530 (22.0%) | 271,005 (22.7%) | 4,567 |
| named docs | 75,245 | 78,612 | 75,245 | 0 |
| named existing acceptance files (pins) | 72,969 | 72,969 | 72,969 | 27,866 |
| named other source and config | 705 | 70,128 | 90,769 | 1,562 |
| named total (share) | 1,208,087 (89.6%) | 1,079,379 (91.2%) | 1,107,128 (92.7%) | 33,995 (60.7%) |

The largest class is the one generated data file (44 to 50%), which is regenerated by a documented command and kept current by a test; at 597,140 bytes it is over the bound by itself. Repeated lines inside the package are 0.8 to 3.4 KB (0.1 to 0.3%), lines also found elsewhere in the tree 3.8 to 5.9 KB, and the packages gzip to 22 to 35 KB: duplication is not the cause. No diff exists at shaping time (no Build ran).

What remains of the estimate (bound 524,288):

| measure | T2 | T3 | T4 | T1 |
|---|---|---|---|---|
| gate estimate | 1,348,267 over | 1,182,842 over | 1,194,443 over | 55,996 fits |
| generated file counted as zero | 751,127 over | 585,702 over | 597,303 over | 55,996 fits |
| and repeated lines once | 750,364 over | 582,309 over | 595,233 over | 55,806 fits |
| package only | 140,180 fits | 103,463 fits | 87,315 fits | 22,001 fits |
| review authority only (Intent, feature, model) | 87,227 fits | 66,983 fits | 62,024 fits | 12,519 fits |

No requested behaviour has to go: the packages are 4 to 6 times under the bound. The estimate crosses it because whole existing tests, docs, pin-update files and one generated file are summed, none of which the review prompt holds in full. A real Build's review size for these Intents is not measured here.

Reach replay (3 attempts per tree; readiness 0 ms and acceptance executions 0 in every row):

| arm | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| A | decision_record | decision_record | decision_record | decision_record |
| A+ | carried_decisions | scope | scope | scope |
| B | carried_decisions | scope passes, carried_decisions | scope passes, carried_decisions | scope passes, carried_decisions |

B lets the scope gate pass on 3 of 3 oversize trees, and the next gate on all four is `carried_decisions`; readiness ran on 0 of 4 in every arm. (The lines that gate asks to keep include the "unverified sources" text that the A+ and B decision change adds, so part of that refusal comes from the earlier change.)

Synthetic packages:

| case | A | B |
|---|---|---|
| 3 scenarios, small | accepted | accepted |
| one 600,000-byte file named at HEAD | refused (estimate 600,910) | accepted |
| package text 540,440 bytes | refused | refused |

B no longer refuses a named file of any size. It refuses a package whose own text is over the bound; submitted through a full shaping run that package ended with `context_budget_exceeded` (the shaper's own next request, 589,867 bytes, carries it), so the scope refusal cannot reach the shaper for the only class B refuses (one run, not a designed experiment).

Suite (`--- PASS` and `--- FAIL` lines of `go test -v`, subtests included; the 3 fail lines of A are the same environment failures as in Lab C):

| arm | pass | fail | skip | new failures against A |
|---|---|---|---|---|
| A | 881 | 3 | 2 | 0 |
| B with the delivered scope tests | 877 | 7 | 2 | 4 |
| B with those 4 tests rewritten (3) or removed (1) | 880 | 3 | 2 | 0 |

The 4 failing tests each assert that a named file counts at its HEAD size (estimate at the bound, stage units, declared model and outline rows, recorded refusal ending not-ready). Rewriting them is a change of the delivered specification, not "no new failure".

## Verdict: no

- **Held:** the scope gate passes on 3 of 3 oversize trees under B; a package whose own text is over the bound is still refused.
- **Not held:** the suite shows 4 new failures against A (the rule is no new failure); readiness runs on 0 of 4 under B.
- **Cause, stated:** the gate's estimate is a sum of whole files at HEAD, which the review prompt does not hold; the review stage goes on in parts above the bound where the gate refuses. The only small change that lets these trees pass removes the gate's function. Whether the gate stays as a deliberate cost guard (measured from what a review would carry, which needs Builds) or the named-file term is retired is a design decision, so no change is requested here.
- **Not tested:** what a real shaper does with the guidance or with the next gate; a Build's real review size for these Intents.

## Rerun

1. Clone [kogen-shaping at `c3f9c5e`](https://github.com/KogenAI/kogen-shaping/tree/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3) as arm A. For A+, apply Lab C's decision-record change (published as `lab-rc-c-decision-gate-before-readiness-20261106`). For B, delete the line `estimate += f.size` in `scopeLines` of `shape/scope.go`. Set `KOGEN_CUCUMBER` and `KOGEN_NODE` to Kogen's Cucumber modules and Node, and run `go test -count=1 -v ./...` (Go 1.27.2); count with `sh suite-counts.sh <output file>`.
2. Reach replay: as in Lab C, take the shaped Intent trees of failed shapes (each has `.kogen/local/shaping/<slug>/events.ndjson` and the recorded submissions), run `Shape` on a clean copy with a stub external executor that returns the recorded attempt-1 package every round and stub checker sessions, and read the gates from `events.ndjson`.
3. Bytes per class: `python3 -I analyze.py <tree with HEAD> <slug> <dir with the recorded package>` prints the class totals only (it reads the tree and writes no path).
4. `python3 -I report.py .` prints every table above from `data/` (the shipped results of this run, with the trees labelled T1 to T4).

Files: `report.py`, `analyze.py`, `suite-counts.sh`, `replay.json`, and `data/` (`breakdown.json`, `reach.json`, `synthetic.json`, `suite-counts.tsv`).
