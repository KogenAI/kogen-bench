# MacBook temp-file load: where it comes from, and what sharing a source copy does

The delivery MacBook's file-event service (fseventsd) ran at 76-90% of a core. The suspects were four temp-tree writers: the public-package exercise
trees, the per-mode exercise trees in the step files, the studio pixel trees and the parts-candidate/driver trees. A Studio Lab record
(lab-e6-fsevents-temp-trees-20261105, product studio) was registered before any measured run, and revised six times; each revision predates the runs it governs, except that
revision 5 was recorded about 25 s after its first watched run had started (that run is not decision data). No model calls; everything ran as the build user on the MacBook.

## Census (one real Build, passive)
A swiftc-built FSEvents counter (no sudo) counted file-create events under the delivery temp root while one kogen-build Build ran, 23 min 17 s, with a second Build running beside it.
**1,718,803 file creations (73.8k a minute, about 369k per 5 minutes; the brief's 18k per 5 minutes is about 20x lower).** Only one file survived to the end of the window, so snapshot-based counting cannot see this load.

| Source | Creations | Share |
| --- | ---: | ---: |
| Go test temp dirs | 1,138,930 | 66.3% |
| of which one release-assembly test | 413,718 | 24.1% |
| acceptance suite release tree (archive extract + install) | 361,496 | 21.0% |
| kogen-index trees | 124,314 | 7.2% |
| kogen-verify trees | 86,819 | 5.1% |
| all four suspects named in the request | 0 | 0% |

fseventsd used 370 CPU-s in the 1,397 s window (26.5% of a core mean, 164% peak, at least 50% in 18% of samples) with two of my counter clients attached; the 76-90% did not recur in this window.
The shared unit is the release archive's bundled npm packages (about 7,300 files): rebuilt by every packaging call and unpacked again by tests.

## A/B/C on the largest test
Test `TestAssemblyUsesThePinnedComponents` (go test -count=3 per window) in the cli of [kogen at 24136fc](https://github.com/KogenAI/kogen/commit/24136fca70dc16fe2f97907cecd924c4a403470b), run on the MacBook with the delivery build environment, one run at a time, only
while load5 was at most 24 and no verify or landing process ran. Eight interleaved rounds in rotating order (verdict, wall, fseventsd CPU from ps) and three watched rounds (files created, by component).

- **A**: unmodified. **B**: the packaging script builds each bundle's node_modules once into a digest-keyed shared store and links it into the payload (archived with `tar -h`). **C**: B, plus the test extracts only the one executable member it inspects. (The edits are about 30 lines in packaging/package.sh and 17 in cli/assembly_test.go; they are described here, not shipped.)

| Arm | Runs passed | Files created per test run | Change | fseventsd CPU per window (median) | Lower than A | Median wall |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| A | 8/8 (+3 watched) | 16,929 | - | 7.56 s | - | 30.1 s |
| B | 8/8 (+3 watched) | 8,423 | -50.2% | 5.89 s | 7/8 rounds (sign test p=0.035) | 26.3 s |
| C | 8/8 (+3 watched) | 545 | -96.8% | 2.59 s | 8/8 rounds (p=0.004) | 24.0 s |

In A, 54% of the files are the packaging work dir, 42% the whole-archive extract inside the test and 2.8% the source copy (cli, docs, test, packaging). **A shared read-only source copy could remove at most 2.8%, far below the 25% floor, so the hypothesis in the request is dropped.**
Loads fell from 21 to 8 across the rounds and B's last round had a 17.4 s outlier, so the CPU figures are paired by round, not absolute.

**Archive equivalence fails for B and C.** Packages built by A, B and C have 7,549 entries each, but 11 differ (all `node_modules/.bin/*`): `tar -h` follows every symlink, so npm's relative links become file copies. Neither arm passes the registered rule, whatever its file and CPU saving.

## Not measured
Arm D (A plus only the single-member extract; the package is identical by construction) was registered but not run: the load/verify gate held its starts (20, 5 and 5 minutes, load5 up to 80) and I stopped rather than start during a delivery verify step or past the 2 h budget. No fix is proven, so no change request was filed; arms D, B' (store without `tar -h`), C' and E (acceptance suite reusing one built archive, 21% of the Build) went to the Lab-first outbox.
The public-package exercise driver and the studio pixel trees did not occur in this window; the driver needs a real `npm ci` per call by design, so a shared node_modules store cannot apply to it.
`metrics.json` maps run counts onto the climb fields (cells = test runs, all_pass and hidden_* = passed tests); it has no Intents, so valid_intent and landed are 0.

## Rerun
Everything needed is in this folder and the public source. Census: `swiftc -O scripts/fswatch.swift -o fswatch`, then `sh scripts/census.sh <outdir> <pid of a running Build> <max seconds>` (edit the delivery temp root at the top). Ranking: `ranking.json` and `data/census1/*.top60.tsv` hold the published slice.
A/B/C: clone kogen at 24136fc into three scratch copies, edit packaging/package.sh and cli/assembly_test.go as described, then `sh scripts/abseq.sh <outdir>` (sequence) on a quiet host; each run is `scripts/abrun2.sh`. Equivalence: `scripts/eqcheck.sh`. Reproduce the tables from the recorded data with `python3 -I report.py data ab ABC` (reads data/ab).
