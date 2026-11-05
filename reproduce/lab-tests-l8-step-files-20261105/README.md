# Archiving per-Intent step files changes no spec requirement, but 29 of 220 name tests that exist nowhere today and 69 cannot be mapped

Finding `lab-tests-l8-step-files-20261105`. A static, model-free Lab (no model call, no suite run, 5 Nov 2026), step 0 of Lab L8 of the K-TESTS-ACCEPTANCE-FIRST request. The Studio record `lab-tests-l8-step-files-20261105` was registered before the inventory and holds the fixed rule.

## Question

The request would move the per-Intent step files that only wrap `go test -run` (and the ticket-named ones) out of `features/steps/` into `.kogen/intents/<slug>/`, and merge lasting scenarios into layer A or B. Does that lose a requirement, or the only check of a behaviour?

## Method

1. Inventory at the request's main snapshots of the nine Go repos (`data/step_files.json`): every `features/steps/*.js` that spawns `go test`, and the test names in it (from `-run` arguments when literal, otherwise any `Test...` token). A name is checked against the `func Test...` definitions of all nine repos (an unanchored match, as `go test -run` does), then against a driver the step file generates or a non-test file carries. A name found nowhere is `stale`.
2. The request's section 6 tables (`data/section6_names.tsv`): each named test with its verdict (DEL, REW, MOVE, REL, FAST).
3. Layer A: `spec/tools/check.mjs --trace` of kogen 24136fc in a scratch copy, before and after moving 99 kogen step files (78 ticket-named plus 61 that spawn `go test`, 99 distinct) to `.kogen/intents/_archived/steps/`; the full output is compared (`data/spec_trace_before.txt`, `data/spec_trace_after.txt`).

## Fixed rule (registered)

Yes: the trace output is identical before and after, and every step file's test names exist and are not deleted by section 6, or have a named replacement. No: the trace output changes, or at least one step file has a name that neither exists nor has a named replacement. Unresolved: more than 10% of the go-test step files yield no extractable test name. Names that do not exist before any change count against `yes`.

## Result

| Measure | Value |
|---|---|
| Step files in the nine repos (`features/steps/*.js`) | 598 |
| Step files that spawn `go test` (the request counted 253) | 289 |
| ...with an extractable test name | 220 (79 from a literal `-run` argument, 141 from test tokens) |
| ...without one (package paths or names built at run time) | 69 (23.9%) |
| Of the 220: run tests that exist in a repo's `_test.go` | 77 |
| Of the 220: run a driver the step file or a non-test file supplies | 114 |
| Of the 220: name a test that exists nowhere (stale) | 29 (5 on a literal `-run` argument) |
| Step files naming a test that section 6 deletes, rewrites or moves | 12 files (DEL 5, REW 7, MOVE 7 name hits) |
| Spec requirements / scenarios in the trace | 108 / 209 |
| Trace output before vs after moving 99 step files | identical (`spec check: ok` both times) |

- The spec trace reads `spec/features` and the Quint models only; per-Intent step files and per-Intent features are not among its inputs, so archiving them cannot remove a requirement's scenario. The check confirms it: byte-identical output.
- The 77 step files that run real repo tests duplicate what each repo's own `go test ./...` already runs, so archiving them loses no test. The 114 driver-based files carry their own Intent-specific Go driver; archiving keeps it with the Intent.
- Stale observers are real: for example a loop step file still runs `-run ^TestPrefixLog` for a test that kogen-loop removed with its experimental levers. These per-Intent files are not part of the offline acceptance run, so nothing notices.
- The 12 files whose names section 6 changes all have a destination in section 6 (a rewritten behaviour sentence, a producer's layer B, or the loop contract), but none of those scenarios exists yet; two hits the parser flagged were not changes (a replacement test, and a prefix of a land-red list) and are excluded.

## Verdict

**No** (the registered bar fails; the change itself is not shown to lose a requirement). The trace is unchanged, but 29 step files already name tests that exist nowhere, which the rule counts against `yes`. The unresolved condition also holds for the 69 package-level or run-time-named files. The conclusion for the request: archiving is safe for layer A coverage; before it, the stale and package-level observers need a one-time pass so that "every archived observer's names exist" can be shown.

## What step 1 needs

A package-level mapping for the 69 files (which package each runs and whether it stays in the default gate); a decision for the 29 stale observers (delete with the Intent's archive); and, once layer B exists, a re-run of this inventory against the new scenario names. Cost: no host time (static); about one hour of review.

## Limits

- The count of step files that spawn `go test` (289) differs from the request's 253: the inventory counts a file that names `go test`, a `go` spawn with a `test` argument, or `-run` together with a `go` spawn; the request does not state its predicate.
- For 141 files the names come from any `Test...` token, which includes names used as inputs of the file's own self-test; the 5 stale files on the literal `-run` basis are the firm ones.
- Whether a replacement named in section 6 is a good replacement was read, not tested.

## Rerun

Offline, from the published data, no model call:

```
python3 -I report.py data
```

It recounts every number above from `data/` and checks them against `replay.json`. `scripts/l8_inventory.py <delivery checkouts> <out>` rebuilds `step_files.json` from the nine repositories at the commits in `replay.json`; `scripts/l8_section6.py <request.md> <out.tsv>` rebuilds `section6_names.tsv` from the request text. The spec trace is `node spec/tools/check.mjs --trace` run in `spec/` of https://github.com/KogenAI/kogen at commit 24136fca70dc before and after moving the files listed by the rule above. Sources are public at the commits in `replay.json`: https://github.com/KogenAI/kogen and the other kogen-* repositories.
