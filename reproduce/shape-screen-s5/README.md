# Shape screen S5: refusal-hint patch against the unpatched shaper, no headroom

Screen, not a confirmation. Kogen 3e759e88 with its vendored Loop pin 8a2fcdae; shaper openai/gpt-6.1-terra at medium effort; 13 development tasks, 2 repetitions, 52 shapes from the request text only, no build; B0 (unpatched) against S5 (patch digest 3a7d7d25: the "undefined step" refusal names a harmless cause when the step text shows one: surrounding whitespace, an unclosed quote, a trailing full stop; no rule relaxed). Finished 31 October 2026.

## Result

Accepted Intent: B0 25/26, S5 25/26. Mean wall 165 s vs 158 s (wall is the whole shape command, so it includes any refused attempts); mean input tokens 132k vs 135k, output 4.9k vs 4.8k. Per task and repetition (paired in `expected-output.txt`): both arms accepted in 25 of 26 pairs; the only unequal pair is goose-labels-go, where B0 failed on repetition 2 and S5 on repetition 1, each time because the shaper answered without a tool call, not because of a refusal the hint addresses. Wall deltas (S5 minus B0) range from -92 s to +47 s with no pattern by task. S5 has no measurable effect on validity: nothing to fix remained. Verdict: **no headroom**, patch dropped.

## Correction to the earlier shape screen

The 61-65% not-accepted rate in the earlier screen ([shape-screen-terra-b](../shape-screen-terra-b/README.md)) came mostly from the harness, not the shaper: on one of the two hosts the unpacked Kogen builds lacked the file the installer writes to locate Node, so every step file failed to load (52 of 64 shapes on that host failed this way). With the file present, B0 is accepted in 25 of 26 shapes across both hosts. The earlier screen's validity numbers are valid only for its Linux half.

## Rerun

    python3 -I report.py data/rows.tsv   # reproduces expected-output.txt

data/rows.tsv holds one row per shape: arm, task, rep, host kind (`linux` or `mac`), class, wall seconds and token counts. Intent texts are kept private.
