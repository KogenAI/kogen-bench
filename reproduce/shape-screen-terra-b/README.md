# Shape screen of three shaping patches, Terra: only the Linux half is valid

Screen, not a confirmation. Kogen 3e759e88 with its vendored Loop pin 8a2fcdae; every arm shapes with openai/gpt-6.1-terra at medium effort; four arms, 13 development tasks, 2 repetitions each, 104 shapes from the request text only, no build. Arms: B0 (unpatched), S1 (patch digest aa4acc9f), S2 (a700d61c), S3 (1dcd9260). The shaping model was told nothing about the arms; Intents were stored under random labels and scored before the label-to-arm map was opened. Finished 31 October 2026.

## The second-host half is an invalid instrument

8 of the 13 tasks (64 shapes) ran on a second host whose unpacked Kogen builds lacked the file the installer writes to locate Node, so every shape there failed to load its step files. Not one produced an accepted Intent in any arm, including the unpatched one. Those 64 shapes say nothing about the shaper or the patches, and an earlier version of this page counted them as failures (61-65% "not accepted"). That number was a harness fault, not a property of Kogen. The clean rerun of the unpatched shaper against one patch, with the file present, accepted 25 of 26 shapes in both arms: see [shape-screen-s5](../shape-screen-s5/README.md). None of S1, S2 or S3 was rerun cleanly.

## Result (Linux half only: 5 tasks, 2 reps, 10 shapes per arm)

Accepted Intent: B0 9/10, S1 10/10, S2 10/10, S3 9/10 (one S3 shape has no scored row). Coverage of the accepted Intents against the frozen per-task requirement lists, by literal token matching (a floor, paraphrase is missed; contradictions were not scored): B0 .284, S1 .285, S2 .263, S3 .267. In the rerun output the arms are labelled b0, p2 = S1, p4 = S2, s3 = S3.

Paired change against B0 on the same task and repetition, both accepted (covered requirements, patched minus B0):

| Task / rep | S1 | S2 | S3 |
| --- | --- | --- | --- |
| agingq-go r2 | +1 | 0 | +1 |
| backoff-go r1 | 0 | +2 | +1 |
| backoff-go r2 | 0 | -1 | +1 |
| bizday-go r1 | -2 | 0 | not paired |
| bizday-go r2 | -3 | -3 | -4 |
| durfmt-go r1 | +4 | +1 | 0 |
| durfmt-go r2 | +1 | -1 | -1 |
| tmplvar-go r1 | 0 | -1 | 0 |
| tmplvar-go r2 | +1 | +1 | 0 |

Pairs higher/lower/equal: S1 4/2/3, S2 3/4/2, S3 3/2/3. S1 is lower on both repetitions of bizday-go; S2 and S3 are lower on r2 (S3 has no r1 pair). Rule applied (keep if higher on at least two more tasks than lower, no task lower on both reps, validity not lower; drop if lower on more tasks): no arm is a keep, none is dropped. No arm shows a coverage gain; five tasks are too few to say more. Verdict: **unresolved**.

## Rerun

    python3 -I report.py data/rows.tsv   # reproduces expected-output.txt

data/rows.tsv (sha256 in the commit's listing, `sha256sum data/rows.tsv`) holds one row per scored shape: arm, task, rep, class, counts of covered requirements, scenarios and bloat scenarios, and `half` (`linux` for the valid Linux half, `second_host_invalid` for the shapes that could not load their step files). The requirement lists and Intent texts are kept private.
