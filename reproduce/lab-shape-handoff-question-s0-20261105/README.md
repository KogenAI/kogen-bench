# Shaping handoff questions: a census says the evidence gate is not needed, the missing-options check is

Finding `lab-shape-handoff-question-s0-20261105`. Stage 0 of a Lab study (no model call, no seat, 5 Nov 2026) on one question: when shaping stops on a question of kind `handoff` (sign-in, access, platform), is a guard on that class worth building, and which one?

Candidate guards (lane patches on [kogen-shaping](https://github.com/KogenAI/kogen-shaping/tree/42424ca), none changes the CLI):

- H0: no change.
- H1: every question that is printed, stored as pending or returned to a machine caller has options and exactly one recommended option; a malformed one goes back to the shaper as repairable feedback.
- H2: H1, plus a handoff reaches the user only when something the shaper read or ran shows a user-only action is needed.
- H3: H2, plus options that wait, pause or defer are refused.

Registered rule: if handoff-ended shaping runs are under 2 per 100 and no legitimate question would be refused by H2, H1 alone is built and H2 and H3 are dropped as unproven.

## Result

- **626 shaping runs** in the delivery logs of two Mac hosts (27 Oct to 5 Nov): 51 stopped on questions, 11 of them on a question the shaper called an authentication or security handoff. That is 1.76 per 100 runs.
- **All 11 ran on releases from before the question check** (landed in kogen-shaping 37d5474 on 3 Nov; the releases 41d70052 and d98cfe01 carry it). Before it: 11 of 429 runs (2.56 per 100). With it: **0 of 197 runs** (upper 95% bound 1.52 per 100; chance of 0 in 197 at the earlier rate 0.015). Question-stops of any kind fell from 50 of 429 runs to 1 of 197.
- **549 stored research shaping cells** (unique cell and start time): 26 ended on questions, 22 of them with a recorded class `ui_ux` (the other 4 have no check record). The check recorded 80 question items across them, **none of class `handoff`**; 11 were class `environment` and refused.
- **None of the 11 handoffs was clearly legitimate.** Reading the question text: 8 asked for something shaping could decide or that is not an authentication step (host access for a platform check, a missing source revision or export, a toolchain restore, a policy choice); 3 are contested (a real signed-in environment, read access to a private repository, a repository admin setting). Four items stopped on a handoff in more than one round (up to four); in three of them (a package-manager fault, provider setup, a contracts snapshot) later rounds repeated the same ask after the answer had supplied nothing new. 14 of 81 question blocks offered a pause or defer option (keyword match) and 4 of them recommended it.
- **The malformed question is real but rare**: 1 of 81 question blocks (and 1 of 20 handoff blocks) had no options and no recommended mark, which fails `all: recommended` with `answers_invalid`. The current main (kogen-shaping 42424ca) still accepts it: `validateQuestions` treats options as optional and `recommendedAnswers` only checks the mark when the answers are expanded.

## Verdict

H1 is built alone. H2 and H3 are dropped: the problem they target is at 0 per 100 on the current release, 3 of the 11 historical handoffs might have been refused wrongly, and at a rate of at most 1.5 per 100 a Stage 2 smoke test (12 pairs) would see at most 0.4 handoff events, so it could not show a gain. Reopen them only if the handoff-ended rate on current releases exceeds 2 per 100 over at least 300 shaping runs.

## Limits

- Delivery logs are overwritten by retries, so some question-stops are lost; counts include retries and answer rounds as separate runs.
- The era split is by release and is confounded with the work mix and with the other shaping changes of 3 and 4 Nov; the exact test is descriptive.
- The kind and class of each pre-check question comes from the printed marker "authentication or security handoff"; the legitimacy reading is the helper's own, from question text, and is in `data/handoff-cases.tsv`.
- Hosts read: the Studio and the MacBook. The eu2 host was not read.
- Raw logs hold the request texts and stay private; the data files hold counts, release ids, item ids and the reading only.

## Rerun

Everything below runs offline from the published data files, with no model call:

```
python3 -I report.py data
```

`data/delivery-shape-logs.tsv`: one row per shaping log (host, log name, last-write time, kogen release, question blocks, handoff blocks, blocks without options or recommended mark, blocks with a deferral option). `data/research-cells.tsv`: one row per stored research shaping cell (outcome and question-check classes). `data/handoff-cases.tsv`: the 11 handoff-ended items with the reading.
