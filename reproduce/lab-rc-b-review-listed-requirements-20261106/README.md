# A refused review submission should not make its requirement texts binding

**Finding.** Yes. In kogen-review, an independent review records the requirement texts of every submission, accepted or refused, and a later approval may not drop one. The review also gets one refused submission. A reviewer whose first submission is refused for an evidence problem and who then splits or rewords the requirements is refused again, only because the first wording is "missing", and the review ends without a verdict. Making only an accepted submission's texts binding lets all 5 recorded refusal sequences through (3 failed Builds, 2 reviews each except one), still refuses a submission that really drops a requirement an accepted submission listed, and keeps the Go test suite green once the one test that asserts the replaced rule is updated.

## Question
Does listing the requirement texts only when `validate` accepts the submission (instead of when the array is well formed) end the `rejected_verdict_exhausted` stops seen in 3 Builds since the release that carries the rule, without letting a real drop through? Registered in the Studio Lab record of the same id before any replay or suite run: verdict yes if (1) the unchanged code ends `rejected_verdict_exhausted` on every replayed sequence, (2) the patched code accepts every one including the round that restored the accepted texts, (3) a submission that drops a requirement of an accepted earlier submission is still refused, (4) the existing suite stays green (one run per tree, same host).

## Method (model-free, 0 model calls)
- Code under test: kogen-review [66be20d](https://github.com/KogenAI/kogen-review/commit/66be20d31658374a86b98f23a1d8476e861193e0) (`review/independent.go`: `requirements()`, `missing()`; the rule was added by [c8e5c9b](https://github.com/KogenAI/kogen-review/commit/c8e5c9b2e37e991da878d28666b2229a5fd5fde7)).
- Inputs: the ordered `StructuredOutput` submissions of the reviews in the logs of three failed Builds (two Macs and a Linux host): two reviews of the first, one review of 4 rounds of the second, two reviews of the third. 5 sequences. The second one's reviewer edited the candidate itself in round 1, so its accepted round 2 was followed by a repair pass and a re-review (rounds 3 and 4). Private logs and requirement texts stay private: `data/sequences-anonymized.json` keeps only what the rule and the evidence check depend on (identity of each text, evidence kind, met, which scenario a citation names, scenario status, round order, the round of the edit). Per-round results on the real texts and on the anonymized inputs are identical for both arms.
- Replay: each sequence runs through `review.NewExternal(...).Review` (the external-review path the Builds used: `validate`, `requirements`, `missing`, the one-rejection rule and the repair loop are the product's) with a scripted executor that returns the recorded submissions in order and edits the candidate in the recorded round. Evidence is judged against the recorded acceptance result of each run's pass. `harness/replay_test.go` is that test (it uses the repository's own test fixtures; copy it into the `contract` package).
- Arm A: the code as is. Arm B: the same code where `requirements()` collects the texts a submission would list into a field of the run instead of appending them to the review's `Listed`, and `validate()` appends them only when it returns no problems. The B test changes (inverting the assertions of the one test that pinned the old rule, and 4 new cases) are described below; the diff itself is not shipped.

## Results
| sequence | A | B |
|---|---|---|
| review 1 of Build 1 | refused r1 (1 citation names no scenario), refused r2 (2 missing): rejected_verdict_exhausted | r1 refused (same), r2 accepted: approved |
| review 2 of Build 1 | same shape (1; 2 missing): rejected_verdict_exhausted | approved at r2 |
| review of Build 2 (4 rounds) | r1 refused (3 citations of an older tree), r2 accepted, r3 refused (18 missing), r4 refused (8 missing): rejected_verdict_exhausted | r1 refused, r2 accepted, r3 refused (18 missing, correct: drops texts r2 had accepted), r4 accepted: approved |
| review 1 of Build 3 | r1 refused (6 citations name no scenario), r2 refused (4 missing): rejected_verdict_exhausted | approved at r2 |
| review 2 of Build 3 | r1 refused (4 citations name no scenario), r2 refused (1 missing): rejected_verdict_exhausted | approved at r2 |

- **A reproduces the logs.** The missing-problem counts of A's final refusals (2, 2, 8, 4, 1) equal the counts in the logs, and the accepted round 2 and refused rounds 3 and 4 of the second Build match its log. The first-round refusal text is not in the logs, so its cause here (a citation naming no scenario, or acceptance of an older tree after the reviewer's edit) is the replay's reading of the recorded evidence.
- **Negative case.** B2's round 3 drops 18 of the 23 texts round 2 had accepted and is still refused on B. Four unit cases through the same path: a reworded repair of a refused submission is accepted; after an accepted submission of R1, R2, R3 a submission with R1, R2 is refused with exactly one problem naming R3, and restoring R3 is accepted; the same drop twice ends the review `rejected_verdict_exhausted`; respelling an accepted requirement keeps the first accepted spelling. A fails the first case and passes the other three; B passes all 4; a mutant that never lists anything passes only the first.
- **Suite** (`go test ./... -count=1`, one run per tree, same host, subtests included): A 269 passing, 0 failing. B with only the code change: 268 passing, 1 failing, `TestIndependentReviewJudgesACitedProbeByItsLatestRun`, whose `session-listed` cases assert that a refused submission's text stays binding (an approval that omits it must end invalid, and the checkpoint lists the refused text). With those assertions inverted (the second submission is accepted; the checkpoint lists only what it listed) and the 4 new cases: 274 passing, 0 failing. No other test changed. Condition 4 is read, as registered beforehand, as "every other test passes unmodified and the updated cases pass": no fix of this rule can pass a test that pins it.
- **Replay runtime.** 2.9 s (A), 3.0 s (B) for the 5 sequences.

## Limits
- B2 passes on B only because round 4 restored round 2's 23 texts exactly; a reviewer whose round 4 also rewords still ends `rejected_verdict_exhausted` after an accepted round and a repair pass. That is the rule working as intended, not something this change alters.
- Single-session replay (the fixture is small, the real review of the second Build was cut into 2 parts; part 2 never ran). No recorded sequence of the native (API) reviewer; the change is in the shared `validate`, covered there by the updated test and the suite. A review resumed from a checkpoint written by the unchanged code keeps the refused texts it recorded. Go suite only; the repository's Cucumber features were not run.

## Rerun
```
cd reproduce/lab-rc-b-review-listed-requirements-20261106
python3 -I check.py
```
`check.py` recomputes `replay.json` and the table from `data/` and checks the four conditions. To regenerate `data/outcomes-A.json` and `data/outcomes-B.json`: clone kogen-review at the commit above, copy `harness/replay_test.go` into `contract/`, and run
```
REPLAY_FILE=<path to data/sequences-anonymized.json> REPLAY_OUT=<out.json> go test ./contract -run TestReplayRecordedSequences -count=1
```
once on the unchanged tree (arm A) and once with the change described under Method applied (arm B). `data/suite-counts.json` and `data/unit-cases.json` are the counts of the suite runs and the 4 unit cases (`go test -json`).
