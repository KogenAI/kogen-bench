# Extracting one release member instead of the whole archive cuts the largest MacBook temp-file writer by 46%

The release-assembly test (`TestAssemblyUsesThePinnedComponents`, the largest single temp-file writer in a Build on the MacBook) unpacks the whole release archive, about 7,500 entries, to read one executable. [The earlier census](../build-speed-e6-fsevents-temp-trees-20261105/README.md) found it makes 24% of a Build's file creations and that two ways of sharing the packaged files (`tar -h`) change 11 archive links. This follow-up measures the one edit that cannot change the archive: the test extracts only the `bin/kogen` member it inspects (17 inserted lines in cli/assembly_test.go; packaging unchanged).

Source: [kogen at 24136fc](https://github.com/KogenAI/kogen/commit/24136fca70dc16fe2f97907cecd924c4a403470b), scratch edit only, no Kogen commit. Registered in Studio lab lab-e6-fsevents-temp-trees-20261105 (revision 7) before the first run. Model-free; run on the MacBook as the build user with the delivery build environment, one run at a time, only while load5 was at most 24 and no verify or landing process or heavy-queue entry existed. Eight interleaved unwatched rounds (alternating order) and three watched rounds (file-create events per component), `go test -count=3` per window.

| Arm | Runs passed | Files created per test run | Change | fseventsd CPU per window (median) | Lower than A | Median wall |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| A: unmodified | 8/8 (+3/3 watched) | 15,425 | - | 6.73 s | - | 28.1 s |
| D: single-member extract | 8/8 (+3/3 watched) | 8,297 | -46.2% | 4.01 s | 7/8 rounds (one-sided sign test p=0.035) | 25.1 s |

In A the whole-archive extract is 21.7k of 44-48k file creations per window; in D it is zero. What remains is the packaging work dir (about 21-22k per window), which this edit does not touch.

**The package is identical.** Packaging is unchanged; building it in the A and D trees gives 7,549 entries each with identical path, type, mode and sha256 (0 differing), unlike the shared-store arms of the earlier study.

**Verdict under the registered rule: D passes** (tests and package identical, files at least 25% lower, file-event CPU lower in the rounds with p<=0.05). A change request for the test is filed (Lab-first outbox). Caveats: CPU is read from 25-30 s unwatched windows with delivery work running nearby (load5 19 in the first round, 5-10 later), so it is paired per round, not absolute; round 1 had D higher.

`metrics.json` maps run counts onto the climb fields (cells = test runs, all_pass and hidden_* = passed tests); it has no Intents, so valid_intent and landed are 0.

## Rerun
Everything needed is in this folder and the public source. Clone kogen at 24136fc into two scratch copies kA and kD; in kD run `python3 -I scripts/mkc.py cli/assembly_test.go` (adds the single-member extract). Put the scripts and a build of `scripts/fswatch.swift` (`swiftc -O fswatch.swift -o fswatch`) in the parent directory of kA/kD, set the paths at the top of each script, then run `sh scripts/abseq.sh <absolute outdir> <gate deadline, epoch seconds>` on a quiet host (each run is `scripts/abrun2.sh`) and `sh scripts/eqcheck.sh <absolute outdir>` for package identity. Reproduce the table from the recorded data with `python3 -I report.py data ab AD` (reads data/ab; the identity result is data/eq.json).
