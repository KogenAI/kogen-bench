# Lab: do small, ordinary request-only shapes reach readiness once the shaper prompt names the forms Kogen's gates require? (shaping climb, stage 3)

**Finding.** On ten short, ordinary requests over three small repositories (Python, Go, Node: a new function, a validation rule, a CLI flag, a rename, a bug fix, each "with a test"), Kogen release v0.1.0-dev.47236bbb, shaping with the request only, reached readiness on **3 of 25** cells and never at the first attempt: its own gates refused what its shaper prompt had asked for. Six rounds of small, general changes, almost all of them prompt text, got the candidate (C6) to readiness on 10 of 10 of those requests, 7 at the first attempt. On **five held-out requests** it was never tuned on, two reps each, C6 reached readiness on **10 of 10 cells, 8 at the first attempt**, and the release on 2 of 10, none at the first attempt. On the five request-only Rails tasks the release was refused on, the same kogen-shaping changes (built on release 3607552, where those refusals were measured) reached readiness on **0 of 5**: the shapes now got past the gates that stopped the release and stopped at later ones (the wrong-implementation file `controls.json` that no prompt names, the decision record refusing probe runs cited as evidence, earlier-round decisions dropped from the Intent), two of them at the 30-minute deadline. The registered rule needs 2 of 5, and one of those later refusals may come from the change itself, so the candidate does not pass and no request is filed from this stage. The changes keep every rebuilt must-refuse gate case refused (19 of 19) and leave kogen-shaping's test suite as it is at the release's pin. The small-request result stands on its own: it is what a new user meets first; the Rails part shows the next walls. **Verdict: no.**

## Question

Earlier stages of this climb found that request-only shapes of five Rails tasks were refused at shaping because the shaper prompt does not tell the shaper the forms its gates require (stage 0: 60 of 89 refusal lines were a prompt-versus-gate contradiction), and that a first-run user's "add subtract(a, b) with a unit test" was refused by the same gates. Each Rails shape takes 15 to 30 minutes, too slow to climb on; a small request takes one to two. Does a small, general change (prompt text first; a gate changed only where a prompt and a gate contradict each other) get ordinary small requests to readiness, at the first attempt, on requests it was not tuned on, and does it carry over to the Rails tasks?

## Arms

All arms are Kogen [`47236bbb`](https://github.com/KogenAI/kogen/commit/47236bbb93385bc960fd2ac353c9b000bd6ed571) (the adopted release), darwin-arm64, Go 1.27.2, the Claude Code route with claude-sonnet-5-5 at high effort for shaping (the repository's `.kogen/models.yaml`), Claude Code 2.1.312, one Mac. The release pins kogen-shaping [`0484edf`](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e); every other arm replaces it by a scratch copy of that commit plus changes, built with `go build -trimpath -buildvcs=false`. A plain rebuild gives the release binary byte for byte, and every arm's module list differs from it only on the kogen-shaping line.

- **A (release):** the published release tarball as it is.
- **S1 (stage 1's change, rebased):** kogen-shaping `0484edf` plus the four changes of stage 1 of this climb, applied unchanged: B1 (the decision check counts an `(assumption: ...)` or `(evidence: ...)` marker anywhere on the Intent line that holds the checked statement; a statement over several lines needs it on every line), B2 (an evidence item that starts with tracked paths followed by prose counts as those paths; an item whose first word is not a tracked path, or that names an untracked file later, stays refused), B3 (shaping may write up to 16 files of up to 64 KiB under the Intent's own folder), P (one Decisions template line for an assumption, one paragraph naming the assumption marker and the evidence-marker form, one feasibility-guidance sentence about fixtures in the Intent folder).
- **C1 to C5 (this stage's iterations, prompt text only on top of S1):** each a new version of one block of text in the shaper prompt (`shape/prompts/shaper.md`), written after classifying the previous round's refusals; no gate was changed after S1.
  - C1: Decisions holds what the request or an answer decides; repository facts are cited with an evidence marker or left out; every Decision line ends with exactly `(source: request)` or `(source: answer <n>)`; concrete examples belong in the feature file; the Tests line form; step sentences are Cucumber Expressions (parentheses are optional text); an exit-code step runs a built program, not `go run`.
  - C2: C1 reworded: repository facts are not Decisions; "other inputs work as before" is a statement the request does not make; Tests lists only rules the request adds, changes or removes.
  - C3: C2 plus a Decisions template line for a choice the repository settles, with its evidence marker (`- <a choice the repository settles, such as where the tests go> (evidence: <path tracked at HEAD>) (source: request)`), the current behaviour a change replaces counted as a repository fact, examples kept out of Tests lines, and "Given steps pass today; the failure comes from a Then step". From C3 on, P's feasibility-guidance sentence is left out (see Deviations), and the package's prompt goldens are regenerated with its own `go test -update`.
  - C5: C3 with the intent.md prose template line changed from "the outcome and its boundaries, including what existing behavior is replaced or removed" to "the outcome in the request's words and what the change replaces or removes; a fact about the current code ends with its evidence marker; no sentence about behavior that stays as it is, about what is not added, or that only something changes", and the same named in the repository-fact paragraph. (C4, C3 with only the template line, was built and replaced by C5 before it ran.)
  - **C6 (the candidate):** C5 plus three template and prompt lines (the Tests template names the rule in the request's words and the test by file and purpose without inputs or expected values; the Source comparison template names scenarios by their titles; the layer `existing` is for a requested rule an existing test already covers, and the decision check reads Tests and Source comparison too) and one sentence in the decision checker's own instructions (`shape/decision.go`, text only, no logic), R1: "A concrete result obtained by applying a rule the request states to another input, computed correctly, follows the request; quote the passage that states the rule. A result the request's rule does not decide (an edge case, a default, an error or message, a format or any other value the request leaves open) is unsupported." R1 is the only gate-side text added after S1; every C6 cell's 'follows' items were audited for it.

## Method

1. **Requests.** 15 short requests written for this Lab (listed in `data/requests.json`), over three scratch repositories set up the way a new user's repository looks after `kogen init`: one check (`python3 tests/test_calc.py`, `go test ./...`, `node --test test/`), the Cucumber acceptance command, a model lineup with claude-sonnet-5-5 high for shaping. Kinds: new function (with or without a refusal case), validation rule, CLI flag, rename, bug fix, behaviour change. Ten are the climb set (patches were written from their refusals); five are held out (never used to write a change) and were run only for the final candidate and the release. One climb request is the one a first-run user was refused on earlier ("add subtract(a, b) with a unit test").
2. **Cells.** One cell = a fresh copy of the repository and one `kogen intent shape` call with the request file, no answers, stopped at readiness or refusal; the login of the subscription seat admitted for that cell; at most three cells at once. Measures, from the cell's own shaping events: reached readiness (exit 0 and a readiness receipt), refused submissions, first-attempt readiness (no refused submission), the gate and problem lines of each refusal, the coding agent's reported list-equivalent cost, wall time.
3. **Rounds.** Round 1: A and S1 on the ten climb requests. Rounds 2 to 6: the newest candidate on the ten climb requests (with A cells on five of them in rounds 2 to 4 for a second and third release rep). After each round every refusal line was classified by a fixed text rule (the kind of each problem line is recorded in `data/cells.json`): a repository fact written as a request statement, a concrete example result in intent.md, another unmarked open value, prose inside an evidence marker, a source tag that is not exact, a Tests line in the wrong form, a step pattern that is not a valid Cucumber Expression, an exit-code step through `go run`, a write outside the Intent's files, controls.json missing, a scenario that fails today in a Given step; and by class: (a) the arm's prompt names the form and the shaper did not use it, (b) the arm's prompt does not name the form the gate requires, (c) no named way to pass without an answerer.
4. **Held out.** The final candidate and A, each on the five held-out requests twice (20 cells, interleaved, same seats).
5. **The Rails tasks.** The final candidate's shaping changes, built on release 3607552 (the release the five Rails refusals were measured on; see Deviations), shape-only on the five request-only Rails tasks of the earlier rounds, one rep each, 1800 s per cell, compared with the stored release cells of the same tasks.
6. **Model-free checks on the candidate tree.** kogen-shaping's own suite (`go test -count=1 -v ./...`) against the release's pin; stage 0's must-refuse gate cases.

## Results

Climb set (ten requests, one cell per request and arm per round; "first" = reached readiness with no refused submission):

| round | arm | ready | first | refusals by gate (submissions) | cost USD |
|---|---|---|---|---|---|
| 1 | A | 1 of 10 | 0 | decision check 12, evidence 8, Intent lint 7, step self-check 2 | 4.79 |
| 1 | S1 | 5 of 10 | 1 | decision check 14, Intent lint 3, step self-check 2, contract review 1 | 5.71 |
| 2 | A | 1 of 5 | 0 | decision check 8, evidence 5, Intent lint 1 | 2.66 |
| 2 | C1 | 8 of 10 | 2 | decision check 12, Intent lint 2, readiness 1 | 5.81 |
| 3 | A | 0 of 5 | 0 | decision check 9, evidence 4, Intent lint 1, step self-check 1 | 2.42 |
| 3 | C2 | 9 of 10 | 4 | decision check 7, Intent lint 1, validation 1, contract review 1 | 5.68 |
| 4 | A | 1 of 5 | 0 | decision check 8, evidence 4, Intent lint 1, step self-check 1 | 3.03 |
| 4 | C3 | 10 of 10 | 4 | decision check 7, Intent lint 1 | 6.85 |
| 5 | C5 | 10 of 10 | 3 | decision check 5, step self-check 2, validation 1, contract review 1 | 6.45 |
| 6 | C6 | 10 of 10 | 7 | decision check 3 | 4.20 |

The release over rounds 1 to 4: 3 of 25 ready, 0 at the first attempt.

Held-out set (five requests never used to write a change, two reps each, interleaved):

| arm | cells | ready | first attempt | refusals by gate (submissions) | cost USD |
|---|---|---|---|---|---|
| A (release) | 10 | 2 | 0 | decision check 18, evidence 7, Intent lint 1, step self-check 1 | 5.58 |
| C6 | 10 | 10 | 8 | decision check 2 | 4.38 |

Per request (R = ready at the first attempt, r = ready later, x = refused; cells in order):

```
c01  new function                 A:xrx  S1:R  C1:r  C2:r  C3:R  C5:r  C6:R
  c02  validation rule              A:xxx  S1:r  C1:x  C2:r  C3:R  C5:r  C6:R
  c03  new function with a refusal  A:xxr  S1:r  C1:r  C2:R  C3:r  C5:R  C6:R
  c04  rename                       A:xxx  S1:x  C1:x  C2:R  C3:r  C5:R  C6:R
  c05  CLI flag                     A:xxx  S1:r  C1:R  C2:x  C3:r  C5:R  C6:R
  c06  bug fix                      A:xx  S1:x  C1:r  C2:R  C3:r  C5:r  C6:r
  c07  new function                 A:xx  S1:x  C1:R  C2:r  C3:R  C5:r  C6:R
  c08  behaviour change             A:rx  S1:r  C1:r  C2:r  C3:r  C5:r  C6:R
  c09  validation rule              A:xx  S1:x  C1:r  C2:r  C3:r  C5:r  C6:r
  c10  new function                 A:xx  S1:x  C1:r  C2:R  C3:R  C5:r  C6:r
  h1   new function with a refusal  A:xr  S1:-  C1:-  C2:-  C3:-  C5:-  C6:RR
  h2   validation rule (CLI)        A:xx  S1:-  C1:-  C2:-  C3:-  C5:-  C6:rR
  h3   rename                       A:rx  S1:-  C1:-  C2:-  C3:-  C5:-  C6:Rr
  h4   CLI flag                     A:xx  S1:-  C1:-  C2:-  C3:-  C5:-  C6:RR
  h5   bug fix                      A:xx  S1:-  C1:-  C2:-  C3:-  C5:-  C6:RR
```

What the refusals were (problem lines over all cells, by kind; `data/gate-texts.json` has the gate, its file and line at the pins, and one example line per kind):

| kind | gate | A | S1 | C1 | C2 | C3 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|
| repository fact written as a request statement | decision check | 28 | 5 | 12 | 4 | 3 | 6 | 2 |
| concrete example result in intent.md | decision check | 71 | 27 | 5 | 1 | 0 | 0 | 0 |
| other unmarked open value | decision check | 47 | 5 | 3 | 6 | 4 | 0 | 3 |
| prose inside an evidence marker | evidence | 49 | 0 | 0 | 0 | 0 | 0 | 0 |
| source tag not exact | Intent lint | 14 | 1 | 1 | 0 | 2 | 0 | 0 |
| Tests line form | Intent lint | 3 | 3 | 2 | 1 | 0 | 0 | 0 |
| step pattern not a Cucumber Expression | step self-check | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| exit-code step through go run | step self-check | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| other step self-check (undefined step, file does not load) | step self-check | 1 | 0 | 0 | 0 | 0 | 4 | 0 |
| controls.json missing | contract review | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| write outside the Intent files | validation | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| scenario fails today in a Given step | readiness | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| readiness detail lines | readiness | 0 | 0 | 17 | 0 | 0 | 0 | 0 |

The release's refusals are the stage 0 classes on small requests: a test location or an unchanged behaviour tagged as something the request says; concrete example results in intent.md; prose inside `(evidence: ...)`; a source tag that is not exactly `(source: request)`; a step sentence with parentheses (Cucumber reads them as optional text). Stage 1's change (S1) removed the evidence refusals; the prompt text of C1 to C3 removed the step and form refusals and most repository-fact and example lines; what stayed was the decision check reading sections the prompt itself requires (the prose "boundaries", the Tests and Source comparison lines) and refusing results the request's own rule decides; C5 and C6 address those.

The Rails tasks (C6's kogen-shaping changes built on release 3607552, shape only, request only, one rep, 1800 s per cell; tasks labelled 1 to 5, `data/aor-cells.json`):

| task | outcome | refusals (attempt: gate, problem lines) | wall s | cost USD |
|---|---|---|---|---|
| task 1 | refused | 1: decision record 4; 2: decision record 1; 3: carried decisions 4 | 1398 | 9.53 |
| task 2 | refused | 1: decision record 4; 2: carried decisions 3; 3: contract review 1 | 1115 | 7.53 |
| task 3 | deadline | 1: contract review 1 | 1801 | 2.47 |
| task 4 | deadline | 1: contract review 1 | 1802 | 1.54 |
| task 5 | refused | 1: contract review 1; 2: contract review 7; 3: contract review 7 | 1468 | 7.59 |

0 of 5 reached readiness (the stored release cells of the same tasks: 0 of 6). No cell stopped at the gates that stopped the release (decision check on unmarked statements, evidence, Intent lint). Where they stopped instead: (1) contract review, all five tasks: the wrong-implementation check needs `.kogen/intents/<slug>/controls.json` (a correct implementation and wrong ones), a file no shaper prompt names, so it is first met after every other gate has passed; two cells then ran out of the 30-minute deadline, one wrote controls whose steps did not match its scenarios. (2) The decision record (kogen-shaping `shape/ledger.go`): sourced decisions citing probe runs outside the repository (`ran` commands with prose) or the Intent's own new step file, refused as "not a file tracked at HEAD", although the evidence form the prompt names allows `ran` commands. (3) Carried decisions (`shape/ledger.go`): technical decisions of the first round dropped from the Intent in a later attempt; the new prompt text that keeps repository facts out of the Decisions section may push the shaper to drop them, so this refusal is not ruled out as introduced by the change. A first run of two of these cells was void: the seat reached its five-hour limit and both ended in the first shaper round with an API error, before any submission; they were rerun after the seat's window reset.

Model-free checks on C6's kogen-shaping tree: `go test -count=1 -v ./...` gives 895 PASS, 3 FAIL lines, 2 SKIP, the same as the pin (two tests that need a model provider and Quint on the host fail in both); stage 0's 19 must-refuse cases (rebuilt, see Deviations) stay refused and its 4 controls pass. The checker sentence (R1) was audited on every C6 cell: of the items the checker judged as following the request (42 in round 6, 26 on the held-out set), none was a default, error, message or format the request leaves open; two held-out items generalise an example the request gives ("the cents are always two digits" from the $0.05 report).

## Verdict: no

Registered before the first cell: the candidate passes if, on the 5 held-out requests x 2 reps, it reaches readiness in at most 3 attempts on at least 9 of 10 cells and at the first attempt on at least 6 of 10 while the release reaches it on fewer; and it reaches readiness on at least 2 of the 5 Rails refused-set tasks (1 rep, shape only); and it shows no new refusal class introduced by a change, keeps every stage 0 negative case refused, and adds no kogen-shaping suite failure against the pin.

- **Held-out: holds.** 10 of 10 ready (needs 9), 8 of 10 at the first attempt (needs 6); the release 2 of 10.
- **Rails tasks: fails: 0 of 5 reached readiness (needs 2); a carried-decisions refusal on two tasks is not ruled out as introduced by the change.**
- **No new refusal class: holds on the small requests, not shown on the Rails tasks.** C6's refusals on small requests (5 problem lines in 30 cells) are decision-check lines of kinds the release shows; on the Rails tasks the carried-decisions refusal may come from the new prompt text.
- **Negative cases and suite: hold.** 19 of 19 refused; suite counts equal to the pin.

## Deviations and limits (plain)

1. **Base release.** The brief allowed release 3607552 or the adopted release; this Lab used the adopted release 47236bbb, whose kogen-shaping pin `0484edf` is four commits after stage 1's `c3f9c5e`. Stage 1's four changes apply to it unchanged, and the shaper prompt and the decision check are byte-identical in the two commits.
2. **Rails tasks on 3607552.** 47236bbb reads the model lineup only from `.kogen/models.yaml` and refuses it in `.kogen/project.yaml` (checked without a model), while the harness that runs the Rails tasks writes it into `project.yaml`. So the Rails check ran the candidate's kogen-shaping changes on release 3607552 (`c3f9c5e` plus the same changes; shaper prompt and decision check byte-identical to the candidate), which is also the release the stored Rails refusals come from.
3. **Feasibility guidance.** Stage 1's sentence in `feasibility-guidance.md` cannot ship in kogen-shaping alone: a package test requires kogen-verification's copy of the guidance to be identical. It was in S1, C1 and C2 and was left out from C3 on; none of the small requests wrote files in the Intent folder, so the climb numbers do not depend on it.
4. **Goldens.** A prompt change fails the package's three prompt golden tests until they are regenerated (`go test -update` in the package); the candidate tree has them regenerated, and its suite is compared to the pin with that done.
5. **Negative cases rebuilt.** Stage 0's case files were not kept; its 19 must-refuse cases were rebuilt from its published description on a scratch repository and run through stage 0's own harness; 4 controls added.
6. **Small numbers, one seat at a time.** Each climb round has one cell per request and arm; shaping is stochastic (earlier screens measured 18 to 27 percent of paired cells flipping with identical arms). Counts, no significance claim. Cells ran on two subscription seats (the first seat in rounds 1-2, then the second; both again for the Rails cells), as admission allowed; the account does not change the model, effort or release.
7. **Cost** is the coding agent's own list-equivalent figure; the seats are subscriptions, not a bill.
8. **Not ablated.** The candidate's pieces (B1, B2, B3, P, the prompt text) were not run one at a time on the held-out set; which pieces fired is read from the refusal kinds (the evidence-gate and Cucumber/exit-code refusals of the release disappear from S1 on; the repository-fact and example kinds shrink round by round with the prompt text).

## Rerun

1. Make three small repositories as in `data/requests.json` (`repo`): a Python module with `add(a, b)` and a unittest file, a Go module with `text.Slugify` (repeated spaces give repeated hyphens) and a `cmd/slug` command with a `run(args, stdout, stderr) int` function, a CommonJS Node module with `formatPrice(cents)` (cents not zero-padded) and a `bin/price.js` CLI, each with one check in `.kogen/project.yaml`, the Cucumber acceptance command Kogen's `init` writes, and `.kogen/models.yaml` with `shape: claude-code / claude-sonnet-5-5 / high`. Commit each once.
2. Install release [v0.1.0-dev.47236bbb](https://github.com/KogenAI/kogen/releases/tag/v0.1.0-dev.47236bbb) (arm A). For a candidate arm, build Kogen [`47236bbb`](https://github.com/KogenAI/kogen/commit/47236bbb93385bc960fd2ac353c9b000bd6ed571) in `cli/` with `go mod edit -replace=github.com/KogenAI/kogen-shaping=<a copy of kogen-shaping 0484edf with the changes described under Arms>` and `go build -trimpath -buildvcs=false` (Go 1.27.2), and swap the release's `bin/kogen`.
3. For each request and arm: copy the repository, write the request to a file outside it, run `kogen intent shape <slug> <request file>` in the copy with the shaping login, stop at its exit, and read `.kogen/local/shaping/<slug>/events.ndjson` (`submission_refused` events: `attempt`, `gate`, `problems`; cost from `executor_round_ended` `model_usage[].cost_usd`) and the readiness receipt `.kogen/local/readiness/<slug>.json`.
4. `python3 -I report.py .` prints every table above from `data/cells.json` (one record per cell, with refusal kinds) and `data/requests.json`.
