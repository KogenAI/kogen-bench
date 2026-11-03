# kogen-build-nodefect-scope-269823f

Does Kogen's build component (`269823f`) behave differently from the adopted one (`3109cd1`) in the review step our benchmark runs use? **No difference in the retained review data: the changed check never fired in 2041 reviews, and the old and new versions agree on all 77 blocking findings. Same behaviour on this evidence, so nothing changes. This is a model-free check; no run was made and none is needed to support the verdict.**

## What changed

The review step checks every finding a reviewer submits. One rule refused a blocking finding whose message says no defect was found, because a blocker that asserts "no problem" contradicts itself. The change narrows that rule in two ways:

- **Only in on-demand review.** The rule now applies only when a project sets the experimental on-demand review material mode. The default mode (parts) no longer applies it, so there a self-contradicting blocker is accepted as a normal "changes" verdict and the build ends review-blocked.
- **Quoted text is ignored.** In on-demand mode the match runs on the message with quoted and backticked spans removed, so a finding that merely quotes the phrase is no longer refused.

The pattern itself, and every other review check (approval needs every part read, the unread-hunk gate, protected paths, the retry allowance), are unchanged.

| Mode | Finding | Before | After | Differs |
| --- | --- | --- | --- | --- |
| parts (default) | blocking, matches the pattern | refused | accepted | yes |
| parts | any other finding | same | same | no |
| on-demand | blocking, phrase unquoted | refused | refused | no |
| on-demand | blocking, phrase only inside quotes | refused | accepted | yes |
| on-demand | any other finding | same | same | no |

## Does our review path reach the changed branch?

The check runs on every submitted review, so the branch is reached; it can change an outcome only when a blocking finding matches the pattern. The benchmark task kits set no review material mode, and all 12 review-material events in the retained run logs say parts. So our runs take the first row of the table.

## Evidence (retained run data, no model calls, cost 0)

- **Reviews scanned:** 2041 review events (2009 approved, 32 changes) with 336 findings, 77 of them blocking, from retained run logs of earlier Kogen runs. Most are Go tasks plus Rails tasks.
- **Old against new:** the pattern and the old and new match functions were run over all 77 blocking messages. The old check refuses 0, the new check refuses 0, and they differ on none.
- **The replay runs the real functions:** on the change's own examples the quoted-only phrase flips from refused to accepted, while the unquoted, mixed and "no defect was found, but the inspection is not complete" messages stay refused in both.
- **No verdict was ever rejected:** the 6 retry-allowance events all report 0 rejected verdicts, no review ended as invalid feedback, and the refusal text for this rule appears in no retained log. So the old rule has never fired in this data.
- **Delivery's own checks:** the build of this change reported format, compile, vet and tests passing, and its review approved with one cosmetic note. Those tests were not repeated here.

## Why no matched run

A matched run could show a difference only if a reviewer wrote a blocking finding that matches the pattern. That happened in 0 of 77 blockers and 0 of 2041 reviews, so six pairs would expect no such event, and any cell-level difference would be ordinary rerun variation (18 to 27 % per pair) rather than this change.

## Limits

- The retained review files keep accepted verdicts only. The "no rejected verdict" statement rests on the allowance counters and the absence of any invalid-feedback outcome, which would both show a rejection.
- Other reviewers may phrase blockers differently from the retained ones. If one ever writes a no-defect blocker, the only effect is that a retry for invalid feedback becomes a review-blocked ending in the default mode, which is the intended behaviour of the change.
- Retained logs come from one set of task kits and reviewers; this says nothing about on-demand review, which no benchmark run uses.
- Registered stop: if a future run log shows a rejected review verdict carrying this rule's problem text, reopen with a review-only replay.

## Rerun

```sh
python3 -I reproduce/kogen-build-nodefect-scope-269823f/report.py reproduce/kogen-build-nodefect-scope-269823f/data/review_counts.tsv reproduce/kogen-build-nodefect-scope-269823f/data/path_table.tsv | diff - reproduce/kogen-build-nodefect-scope-269823f/expected-output.txt
```

`report.py` uses only the standard library and rebuilds the counts above from `data/review_counts.tsv`, and the table from `data/path_table.tsv`.

To repeat the scan itself you need the two build component versions (control `3109cd1`, candidate `269823f`) and retained review files. Put the pattern and the old and new match functions in a standalone program, feed it the messages of every finding with severity "blocking" from each run's review files, and compare the two results per message; then count review events, verdicts, allowance events and invalid-feedback outcomes in the run logs. The expected result is the table in `data/review_counts.tsv`.
