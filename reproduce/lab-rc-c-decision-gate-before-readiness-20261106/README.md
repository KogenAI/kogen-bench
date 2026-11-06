# Lab RC-C: the decision-record gate costs a shaping attempt, but it is not what ends these shapes before readiness

**Finding.** In four shaping runs that ended `intent/not_ready` with "readiness 0.0 s", kogen-shaping's decision-record gate refused attempt 1 on all four trees (7 problem lines: 4 command text, 2 URLs, 1 file the same package proposes, 0 missing files), which used one of the three attempts. But no run ended on a citation: the endings were `decision_check`, a `revises` text that names no standing decision, `scope` and `carried_decisions`. A small change that notes such sources as unverified instead of refusing them lets all four attempt-1 decisions through and still refuses a real missing file, with no new test failure. It does not let readiness run: the same attempt-1 packages then stop at `scope` (three trees, 1.18 to 1.35 MB of review input against a 524,288-byte bound) and at `carried_decisions` (one tree). The registered rule (readiness runs on every tree where the gate ended shaping) is not met, so the verdict is no and no change is requested. No model call was made.

## Question

kogen-shaping [`ae07c4a`](https://github.com/KogenAI/kogen-shaping/commit/ae07c4a8caa05345e941e85b26fa1176039fcd6b) ("Carry sourced decisions across shaping rounds") refuses a decision whose evidence item is not a file tracked at HEAD (`shape/ledger.go`, the decision record gate). Four shapes of one delivery window ended `intent/not_ready` with readiness 0.0 s. Did the gate end them before Kogen's own readiness could show the shaper its acceptance and feasibility defects, and would letting readiness run first change that?

## Arms

Both arms are kogen-shaping [`c3f9c5e`](https://github.com/KogenAI/kogen-shaping/commit/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3), the commit pinned in the failing release, built with Go 1.27.2 on one Mac Studio as an unprivileged user.

- **A:** the commit as it is.
- **B:** A plus a change to the decision record gate (about 50 lines in `shape/ledger.go` and one call site): before a decision is checked, its evidence items that are no file and no probe move into its uncertainty as `unverified sources: <item>`. An item moves when it is not tracked at HEAD and either the same or an earlier submission proposes it, or it is text (it contains whitespace or `://`, or starts with `<`). A path that is none of these stays as evidence and is refused as before ("is not a file tracked at HEAD"). The change is applied before the decision is compared with the recorded ones, so submitting the same decision again records nothing new. The change and its 12 tests are not copied here; the registered patch is kept with the research notes.
- Why this option and not "run readiness first": readiness is the last step after eleven others (intent lint, ownership, retained artifacts, contract, scope, carried decisions, evidence, decision check, literal check, step self-check, static checks), three of them model sessions (contract, decision and literal checks). Running it first would reorder that chain and could publish before refusing a decision.

The inputs are four kept shaped trees (T1 a Go repository, T2 to T4 an Elixir and Go repository), used as scratch copies. Their shaping events record each attempt's gate and problems.

## Method

1. **Classification.** Read each tree's recorded shaping events: the gate and problem lines of the three attempts. Classify each attempt-1 decision-record problem as command text, observation URL, file proposed by the same package, or missing file.
2. **Readiness without the gate.** Run `kogen intent approve` on a scratch copy of each tree (setup, feasibility and acceptance dry run, no model).
3. **Gate replay.** Replay the recorded decisions of every attempt through the gate of each arm, with the tree's own git repository as HEAD (`data/replay-A.json`, `replay-B.json`).
4. **Negative and synthetic cases** and the existing suite: `go test ./...` on A (pristine) and B, with the Kogen Node and Cucumber tools set.
5. **Reach replay.** Shape a clean copy of each tree with a stub shaper that submits the recorded attempt-1 package every round, and stub checker sessions that answer "no findings", as the package's own fixtures do; record which gate stops it and whether readiness ran (`data/reach-A.json`, `reach-B.json`). The model provider was a closed port; `provider_calls` is 0 in every session.
6. **Fixture end to end.** An external shaper whose decision cites a URL, on the package's fixture project (`data/fixture.json`).

Every Go and approval command ran one at a time under the host's heavy-check lock.

## Results

Part 1: the gate against the endings.

| tree | attempt-1 problems | class | gates of attempts 1 to 3 | ended at | readiness without the gate (approve) |
|---|---|---|---|---|---|
| T1 | 3 | command text | decision_record, carried_decisions, decision_check | decision_check | ran, 53 s, acceptance red as expected, 3 unexercised steps |
| T2 | 1 | command text | decision_record, scope, decision_record | decision_record, but the problem is a `revises` text, not a citation | ran, 119 s, 18 unexercised steps |
| T3 | 2 | observation URL | decision_record, intent, scope | scope | ran, 197 s, 48 unexercised steps |
| T4 | 1 | file proposed by the same package | decision_record, scope, carried_decisions | carried_decisions | ran, 90 s, 5 unexercised steps |

12 attempts: decision_record 5 (4 citation, 1 `revises`), scope 3, carried_decisions 2, decision_check 1, intent 1. Missing-file problems: 0 of 7. Readiness ran on all four trees once the shape was out of the way and refused none; what the shapers never saw was 3, 18, 48 and 5 acceptance steps it could not exercise.

Part 2: the arms.

| check | A | B |
|---|---|---|
| recorded attempt-1 decisions through the gate (replay) | refused 4 of 4 (7 problem lines, matching the recorded events) | refused 0 of 4 |
| recorded attempt 3 of T2 (a `revises` naming no standing decision) | refused | refused (a real ledger problem is kept) |
| synthetic cases: command tag, command text, URL, observation text, proposed file | 0 of 5 pass | 5 of 5 pass |
| missing file (3 paths) | refused 3 of 3 | refused 3 of 3 |
| missing file beside a URL and a command tag | all three refused | only the missing file is a problem |
| fixture shaper citing a URL | blocked after 3 attempts, acceptance ran once (the runner check) | ready, acceptance ran twice (runner check and readiness) |
| suite `go test ./...` | 881 pass, 3 fail lines, 2 skip | 894 pass, the same 3 fail lines, 2 skip |
| reach replay on the 4 real trees | decision_record on every submission; readiness ran on 0 of 4 | carried_decisions (T1) and scope (T2 to T4, 1,348,267 / 1,182,205 / 1,194,443 bytes of one review against 524,288); readiness ran on 0 of 4 |

The suite is not green on this host for A either: `TestShapeProbeMinimalEnvironmentWiring` and `TestExamplesRevertShapeApproval` fail the same way on both (temporary path, no model provider, Quint tools not installed in the checkout), so B adds no failure. Counts are `--- PASS` and `--- FAIL` lines of `go test -v`, subtests included; B's 13 extra passes are its 12 new tests and subtests plus the replay harness.

## Verdict: no

- **Held:** a real missing-file decision is still refused; the suite has no new failure against A.
- **Not held:** B lets readiness run on 0 of 4 recorded packages. The gate costs one attempt of three on every tree, but these runs ended elsewhere: three of the four endings are gates B does not touch, and the fourth is a ledger problem that B keeps. The Intents these shapers wrote were over the one-review size bound at attempt 1 in three of four cases, which readiness would not have shown them either.
- **Not tested:** what a real shaper does with the attempt B gives back; the reach replay repeats one recorded package and answers every checker session with "no findings". That needs a model and was not run.
- B is small and safe, so it can be taken as hygiene for the lost attempt, but this result gives no evidence that it removes "readiness 0.0 s". The cause of that outcome in these four trees is the later gates, chiefly the Intent size bound.

## Rerun

1. Clone [kogen-shaping at `c3f9c5e`](https://github.com/KogenAI/kogen-shaping/tree/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3) twice (arms A and B). Make B's change as described under Arms. Set `KOGEN_CUCUMBER` and `KOGEN_NODE` to Kogen's Cucumber modules and Node, and run `go test -count=1 -v ./...` in each (needs `go` 1.27.2 on PATH); count the pass, fail and skip lines with `sh suite-counts.sh <output file>`.
2. For the gate replay and the reach replay, take the shaped Intent trees of a failed shape (each has `.kogen/local/shaping/<slug>/events.ndjson` and the shaper's recorded submissions), write a small test in the `shape` package that builds a `shaping` over the tree and passes the recorded decisions to `decisionRecordGate` (replay), and one that runs `Shape` on a clean copy with a stub external executor that returns the recorded attempt-1 package every round (reach). Record the gates from `events.ndjson`.
3. For readiness without the gate, run `kogen intent approve <slug> --project .` on a scratch copy of each tree and read `Acceptance exit` and `Unexercised acceptance steps` from its output.
4. `python3 -I report.py .` prints every table above from `data/` (the shipped results of this run, with the trees labelled T1 to T4).

Files: `report.py`, `suite-counts.sh`, `replay.json`, and `data/` (`replay-A.json`, `replay-B.json`, `reach-A.json`, `reach-B.json`, `fixture.json`, `approve.tsv`, `gate-classification.tsv`, `suite-counts.tsv`).
