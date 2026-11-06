# Lab: why kogen-shaping refused five request-only Rails shapes, and what a gate-side change can and cannot do

**Finding.** In a smoke round of Kogen release v0.1.0-dev.36075527 against the same coding agent used alone, all five Kogen cells ended at shaping: three refused submissions each, request only, no answerer. A replay of the 13 recorded refusals that kogen-shaping's own gates produce reproduced every recorded problem count exactly. The 89 problem lines split as follows: **60 are a contradiction between what the shaper prompt asks for and what a gate accepts** (class b), 15 are plain shaper errors (class a), and 14 are prose statements where the only form that passes is not named, or is lost when the checker copies part of a line (class c). All three small gate-side changes tried (B1 to B3) keep every negative case refused and accept every stored Intent the pinned code accepted, but together they turn **2 of the 5 first refusals** into passes, and the registered rule needs 4. **Verdict: no.** The two first refusals that pass are the two that wrote observer or fixture files into the Intent folder; the other three are Intents that state values the request does not state without marking them, or break the Tests-line format, which no gate change may pass without dropping the gate.

## Question

The five trees (T1 to T5) are the Kogen cells of block 1 of the smoke round, five Rails tasks run request only (no answerer, no human information, no hidden-test content). Each ended `refused` at shaping after three refused submissions, so every Kogen cell scored the start-tree floor, while the other arm finished all five. Which gates refused what, is any refusal a gate with no way to pass in a request-only run or a prompt that asks for what a gate refuses, and does a small general change remove the contradiction without loosening what the gate protects?

## Arms

All arms are kogen-shaping [`c3f9c5e`](https://github.com/KogenAI/kogen-shaping/tree/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3), the commit pinned in the release, built with Go 1.27.2 on one Mac Studio as an unprivileged user, scratch copies only.

- **A:** the commit as it is.
- **B1 (decision check, marker on the line):** the decision check copies a part of an Intent line as the statement; a marker `(assumption: ...)` or `(evidence: ...)` elsewhere on that same line now counts for it. A marker on another line never counts, and a statement that sits on several lines needs the marker on every one (`shape/decision.go`, one function and one call, 27 changed lines).
- **B2 (evidence gate, path then prose):** an evidence item that is not itself a tracked path but starts with tracked paths followed by prose counts as those paths, with the read and listed rules unchanged. The item stays refused when its first word is not a tracked path, or when a later word is a file path that is not tracked (`shape/evidencemark.go`, 61 changed lines).
- **B3 (validation, Intent folder):** shaping may also write files under the Intent's own folder, at most 16 files of 64 KiB, besides the four named files and the step files (`shape/shape.go`, one case and two constants, 13 lines).
- **B:** B1, B2 and B3 together (101 changed product lines).

Not run as arms, with the reason: (i) a `(decided: <reason>)` form. The two Intent-lint refusals (T2, T4 attempt 1) come from kogen-coordinator's Intent lint, not from kogen-shaping, and one of them (T4) also holds six Tests lines in the wrong format, so even a lint that accepted `(decided: ...)` could turn at most one more first refusal (3 of 5 in all). (ii) Marking unsupported statements automatically: it would pass T1's first refusal (14 unmarked statements, no marker anywhere) only by dropping the gate. (iii) A prompt change (name the assumption and evidence forms in the Decisions template, name the Intent folder for observer files): it needs a model to measure and, as a builder-prompt change, a Kogen-level screen; it is written down but not measured.

## Method

1. **Classification.** Read the recorded shaping events of each tree: the gate and the problem lines of each attempt (15 refusals, 89 problem lines). Classify each problem line: (a) the gate is right and the shaper erred (the refusal text names a form that would pass, or the item is not a file); (b) the shaper prompt asks for X and a gate refuses X (the first time a gate refused a form the prompt never names, or observer files the guidance asks for and the validation refuses); (c) the gate has no named or controllable way to pass in a request-only run.
2. **Gate replay.** The recorded input of each shaping-gate refusal goes through the package's own gate function: the decision check (`decisionOutcome` with the checker's recorded verdicts replayed, no model), the evidence check on the task's start tree as HEAD, and the write validation on the recorded paths. Attempt-3 Intents exist in full; for attempts 1 and 2 only the recorded statements, items and paths exist (the events keep a 256-byte head of each file), so those replays use the recorded gate inputs and not the whole package. A matches the recorded problem counts on 13 of 13.
3. **Negative and change cases.** 28 synthetic cases on the same functions: 19 that must stay refused (a fabricated or untracked path, a code reference, a path after prose, a tracked path the session never read, an unsupported or contradicted statement beside or on the same lines as a marked one, a product file, the project file, another Intent's folder, a step file without the Intent prefix, a JSON file in the steps folder, a traversal, 17 extra files, one oversize file), 5 that each change should flip, 4 controls.
4. **Held-out.** 388 stored, approved Intents of seven other Kogen repositories (other tasks, not these five): the write validation on each Intent's own files, the evidence check on the 26 Intents that cite evidence, and the decision check with two stub checkers (the whole Decisions line, and a 30-character fragment of it, each as unsupported).
5. **Fixture end to end.** The package's one-shot fixture with one observer file added to the Intent folder.
6. **Suite.** `go test -count=1 -v ./...` on A and on B.

No model call anywhere: the checker's answers are the recorded ones or stubs, the provider was never reached. Every Go command ran one at a time under the host's heavy-check lock.

## Results

Part 1: the 15 recorded refusals (rows: attempt; problems per attempt).

| tree | attempt 1 | attempt 2 | attempt 3 (end) |
|---|---|---|---|
| T1 | decision check, 14 unmarked statements (b) | evidence, 5 items: 2 path-then-prose (b), 3 code references (a) | decision check, 7 prose statements, no marker anywhere (c) |
| T2 | Intent lint, 2 Decisions lines without a source tag (a) | decision check, 2 Decisions lines (b) | evidence, 1 item path-then-prose (b) |
| T3 | validation, 1 observer file in the Intent folder (b) | decision check, 8 (b) | decision check, 1 prose statement (c) |
| T4 | Intent lint, 6 Tests lines in the wrong format and 4 Decisions lines without a source tag (a) | decision check, 17 (b) | evidence, 7 items all path-then-prose (b) |
| T5 | validation, 5 files (an observer, four JSON fixtures) in the Intent folder (b) | decision check, 3 (b) | decision check, 6 prose statements: 3 with a marker on the same line that the copied text omits, 3 without (c) |

Problem lines by gate and class: decision check 58 (b 44, c 14), evidence 13 (b 10, a 3), validation 6 (b), Intent lint 12 (a). By class: a 15, b 60, c 14. By submission (the class with most lines): b 9, a 3, c 3. The three endings at the decision check are class c (prose); the two at the evidence gate are class b. No tree ended on a shaper error alone.

What the code and prompt say (kogen-shaping `c3f9c5e`): the shaper prompt's Decisions template shows only `(source: request)` and `(source: answer <n>)` (`shape/prompts/shaper.md:43-45`) and asks for exact expected values; the decision check refuses any statement the request does not state unless it carries `(assumption: ...)` or `(evidence: ...)` (`shape/decision.go:170`, `:257`), and names only the Decisions-line form of the assumption marker (`:33`), which has no meaning for a prose statement; its feedback recommends `(evidence: ...)` without the accepted form, which the evidence gate states only on the next refusal (`shape/evidencemark.go:208`, items are tracked paths or `ran` commands separated by `; `, `:109-167`). The Feasibility guidance asks for observer controls and local fixtures named by repository path (`shape/prompts/feasibility-guidance.md:5`), while the write validation allows no other file in the Intent folder (`shape/shape.go:2228`). The Intent lint (`kogen-coordinator` `project/intent.go:345`, `:398`) fixes the Tests-line and Decisions-line formats the prompt already shows.

Part 2: the arms (all numbers are counts of the replays; REF = refused).

| check | A | B1 | B2 | B3 | B |
|---|---|---|---|---|---|
| recorded refusals replayed (13) that still refuse | 13 | 13 | 11 | 11 | 9 |
| first refusals turned to a pass (of 5; rule needs 4) | 0 | 0 | 0 | 2 (T3, T5) | 2 |
| attempt-3 refusals turned to a pass (T2, T4 evidence) | 0 | 0 | 2 | 0 | 2 |
| problem lines of the 13 replayed | 77 recorded | -3 (74) | -10 (67) | -6 (71) | -19 (58) |
| negative cases refused (19) | 19 | 19 | 19 | 19 | 19 |
| change cases accepted (5, by design) | 0 | 1 | 2 | 2 | 5 |
| controls accepted (4) | 4 | 4 | 4 | 4 | 4 |
| held-out Intents A accepts (415 checks) refused by the arm | n/a | 0 | 0 | 0 | 0 |
| held-out Intents A refuses but the arm accepts | n/a | 8 (fragments of fully marked lines) | 2 (tracked path then prose) | 0 | 10 |
| suite `go test -v ./...` | 881 pass, 3 fail lines, 2 skip | not run | not run | not run | 881 pass, 3 fail lines, 2 skip |

The held-out checks: 388 write validations (A accepts 388, every arm accepts the same), 26 evidence checks (A accepts 19; B2 also accepts 2 that A refuses, both a tracked path then prose), 388 whole-line decision checks and 388 fragment checks (the stub checker calls every Decisions line unsupported, so only Intents whose lines all carry a marker pass: 8 of 388; with fragments only B1 accepts those 8). Fixture end to end: A refuses the package with the extra file (exit 4 after the refused submission, no file written, no readiness receipt); B reaches readiness (exit 0, file written, readiness receipt published).

The suite is not green on this host for A either (`TestShapeProbeMinimalEnvironmentWiring` and `TestExamplesRevertShapeApproval`: temporary path, no model provider, Quint tools not installed in the checkout); B has the same failing tests and adds none. Counts are `--- PASS` and `--- FAIL` lines of `go test -v`, subtests included. B1 to B3 were run through the replays and cases only; the suite was run on A and on B.

## Verdict: no

Registered before measuring: yes if B turns at least 4 of the 5 first-refusal inputs into passes at the gate that refused them, every negative case stays refused, every held-out package A accepted is accepted by B, and the suite has no failure A lacks.

- **Held:** every negative case stays refused (19 of 19 in every arm); every held-out check A accepts, B accepts (415 of 415); the suite has no new failure.
- **Not held:** B turns 2 of 5 first refusals (T3 and T5, the two that wrote observer or fixture files into the Intent folder). T1's first refusal has 14 unmarked statements and no marker anywhere; T2 and T4 are refused by the Intent lint of another repository (T4 also for six wrong Tests lines). No change that keeps the gates can pass them: the shaper has to write the marker or the format, and the prompt does not tell it how (class b).
- **Terminal attempt:** B2 passes the evidence gate on the two trees that ended there (T2, T4); the decision check, which comes after it, never ran on those packages and needs the checker's verdict on the new text, so whether they would have passed it is not tested. B1 clears 3 of the 6 problems at T5's end; T1 and T3 end on prose statements that no marker covers.
- **Not tested:** what a real shaper does with the extra attempts these changes would give back (needs a model), and the prompt change, which is the smallest change that addresses the 60 class-b lines (name the assumption and evidence forms next to the Decisions template and name the Intent folder for observer files); as a prompt change it needs a Kogen-level screen with a model before delivery.
- B2 and B3 are small and safe, so delivery may take them as hygiene for lost attempts, but this Lab gives no evidence that they make these shapes succeed.

## Deviations and limits (plain)

1. The full attempt-1 and attempt-2 packages were not kept (the shaping events hold a 256-byte head of each file), so "attempt-1 package" means the recorded gate input of that refusal. Attempt 3 is complete for every tree. The two Intent-lint refusals (T2, T4 attempt 1) are another repository's gate and are classified, not replayed.
2. The held-out set is 388 stored, approved Intents of seven Kogen repositories, not stored cells of earlier Rails and Go blocks: those cells ran older Kogen versions that have no decision check, so there is no recorded checker verdict to replay. "A accepts" means the pinned code accepts the stored Intent now. The checker for the held-out decision checks is a stub (every line unsupported), so it exercises the marker logic only.
3. The checker's verdicts in the gate replay are the recorded model answers; a different Intent text would get different verdicts, so B's effect on the decision check beyond the recorded statements is not tested.
4. A package that passes one gate meets the next; only the evidence-then-decision-check order matters here, and the decision check never ran on T2's and T4's last packages.
5. The classes are mine and rule-based (stated under Method); problem lines, not submissions, are the unit, and the submission-level split uses the class with most lines.
6. B1, B2 and B3 were measured on the replays and cases; the suite was run on A and on B (all three together).

## Rerun

1. Clone [kogen-shaping at `c3f9c5e`](https://github.com/KogenAI/kogen-shaping/tree/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3) once per arm. Make B1, B2 and B3's changes as described under Arms (each is one function or case in the file named). Copy `harness/aor_replay_test.go` and `harness/aor_fixture_test.go` into the `shape` directory of each clone.
2. Build the case files the harness reads (a JSON list of cases: gate, slug, recorded decision-check items or evidence text or paths, optional intent file and request file, expected outcome). The five trees of this Lab are private task material and are not shipped; use the shaping events of any failed shape (`events.ndjson` under `.kogen/local/shaping/<slug>/`) for the replay, and the stored Intents of the kogen repositories listed in `replay.json` (their `.kogen/intents/` folders) for the held-out checks, with each repository's commit as HEAD of a scratch git repository.
3. Set `KOGEN_CUCUMBER` and `KOGEN_NODE` to Kogen's Cucumber modules and Node. Run `AOR_ARM=<arm> AOR_REPLAY=<cases.json> AOR_OUT=<out.json> go test -count=1 -run '^TestAORReplay$' ./shape/`, the same with `AOR_CASES` and `AOR_CASES_OUT` and `-run '^TestAORCases$'`, and `AOR_FIX_OUT=<out.json> go test -run '^TestAORFixtureInIntentFolder$' ./shape/`. Delete the two harness files, then run `go test -count=1 -v ./...` in A and B and count with `sh suite-counts.sh <output>` (needs `go` 1.27.2 on PATH).
4. `python3 -I report.py .` prints every table above from `data/` (the shipped results of this run, with the trees labelled T1 to T5).

Files: `report.py`, `suite-counts.sh`, `replay.json`, `harness/` (the two Go test files), and `data/` (`recorded-refusals-replay.json`, `refusal-classes.json`, `negative-cases.json`, `heldout.json`, `fixture.json`, `suite-counts.tsv`).
