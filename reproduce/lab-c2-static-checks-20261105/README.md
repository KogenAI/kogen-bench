# Lab C2 step 1: do the repo's own static checks catch shaper-written acceptance defects before approve?

Question: when the shaper writes acceptance files with a defect the builder must then refuse (builder-blocked), would running the repository's own static checks on the shaped files at readiness, before approve, have caught it? Step 1 of a two-step Lab; model-free, no seat tokens. Studio Lab record `lab-c2-static-checks-20261105` is the lever record `lab-c2-static-checks-step1-20261105`; assumption `kogen/build-failures-c2-shaped-harness-defects-20261105`.

**Result: no, not enough.** The checks caught 1 of 22 builder-blocked defects (4.5%), the Go driver that was not gofmt-clean. Counting the 6 report_invalid rows (5 Intents) that the readiness acceptance run already refused, 7 of 28 targeted failures (25%) are stopped before approve, but only the one is due to the new checks. The 60% bar is not met, so the Lab's step 2 (a shape-repair round fed the builder's report, against a fresh rebuild) is needed: about 24 Builds and 8 seat-hours, not run here. False refusals were not the problem: 0 of a 30-Intent random sample, 0 of 327 landed Intents on gofmt and node --check, and 1 of 12 in-scope Go packages under the configured `go vet ./...` (a driver that calls an API the Intent adds).

## Method
- Arm (a): applied to the shaped files laid over the base, before approve: (1) the repo's `format` check, `test -z "$(gofmt -l .)"` (gofmt is per file, so replayed as `gofmt -l` on each shaped `.go` file); (2) the repo's `vet` check `go vet ./...` (replayed as `go list ./...` to see whether the shaped Go package is in scope, then `go vet` of that package, on the base tree with the shaped files laid over); (3) `node --check` on shaped `.js` and `.cjs`.
- Fixtures: the 22 builder-blocked and 6 report_invalid rows of the 72-hour build-failure classification (`data/c2-table.json`), and 333 Intents landed since 2 Nov, of which 30 were drawn at random (seed 20261105, `data/green-sample30.json`). Landed Intents are listed with their repository and landing commit in `data/green-landed-intents.json`; the shaped files are the files each landing commit added under the Intent folder and the steps folder. Source is public: github.com/KogenAI/<repo>/commit/<sha>.
- Data limit: the shaped bytes of most failures no longer exist (a retry re-shapes, trees are reused, older run folders were removed). Shaped files were recovered for 5 of the 28 targeted failures (3 builder-blocked, 2 report_invalid), and for 4 of those 5 they are a later shape of the same Intent. The other 23 are scored from the logged defect text, backed by defect-class probes: one minimal file per logged defect, run through the same checks (`data/class-probes.json`).
- Tools: gofmt, go vet and go 1.27.2, node 24.21.0 from the build host's installs; git 2.54.0 (Apple Git). Go checks ran under the host's shared test lock after delivery work had drained, cheap checks earlier at low priority.
- What is already in flight: the request `k-shape-artifact-static-checks` covers arm items 1 and 2 (configured format, lint and vet checks on shaped paths in the readiness copy, a named refusal, recheck, unrelated-failure attribution). It does not run `node --check`, which flagged nothing here.

## Results
| Set | Checked | Flagged |
|---|---|---|
| builder-blocked defects (22) | arm (a) | **1** (gofmt-unclean Go driver) |
| recovered failing trees (5 of C2 plus the C10 tree, 12 JS files) | node --check | 0 |
| 327 landed Intents with checkable files (451 files) | gofmt, node --check | 0 |
| 30-Intent random sample (28 with checkable files) | gofmt, node --check, vet | 0 false refusals |
| 33 landed Intents that shaped Go files | `go vet` in `./...` scope: 12 packages | 11 pass, **1 false refusal**; 21 packages are outside `./...` (testdata folders, ignore build tag, no module at the repo root) |
| same 33, naive `go vet` of every shaped Go package | not the configured check | 9 type errors against code not yet written, 11 not compilable alone |

Defect-class probes: a gofmt-unclean Go driver is flagged. Not flagged by gofmt, node --check or go vet: `$$` through JS replace, double-escaped regex dots, JSON field case, fixture total 140 against 120, a trap and sleep timing loop, byte equality over elapsed time, a Go fixture calling t.Parallel twice.

## Reading
Everything except formatting is semantic: contradictory steps, wrong expected values, fixtures that do not match the code under test, timing, string escaping. Static checks are cheap and should stay (they stop the one class they can), but they will not remove the cluster. Caution for any implementation: a shaped Go driver that type-checks only against code the Intent adds fails `go vet` on the base; that must be reported as pre-implementation, not as a shaped-file defect.

## Rerun
Everything above is recomputed offline from the published data, with no model call:

```
python3 -I report.py data
```

It prints the catch rate over the 22 builder-blocked defects, the cheap-check and vet counts, the false refusals in the sample and in the in-scope Go packages, and the probe results. The raw checks were produced by running gofmt, node --check and go vet on the files named in `data/green-landed-intents.json` at their landing commits' parents; those commits are public.

## Limits
Five real trees of 28; the rest is classification from logs plus probes. One host, one toolchain version. The report_invalid rows are counted as already caught because the readiness acceptance run is what refused them.
