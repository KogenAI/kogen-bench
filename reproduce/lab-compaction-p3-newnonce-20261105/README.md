# Compaction detection, phase 3 stage B: a new-nonce instruction on Claude Code (5 Nov 2026)

Question: if the first message tells the agent to invent a NEW nonce after its context is compacted, and the service
(Studio, here a stand-in) checks that the value changed, does that detect compaction without a hook?
Earlier phases: a static nonce, hash or receipt caught 0 of 8 compactions each, because the compaction summary copies the
value (`brief-marker-compaction-p1-20261105`, `brief-compaction-detection-p2-20261105`). This arm asks the model to change it.

## Result (registered before the run; stop rule: arm 1 at most 1 of 8 while the hook is 8 of 8 = rejected, no second round)
| detector | compactions detected | false alarms | latency | cost |
|---|---|---|---|---|
| new-nonce instruction (arm 1) | **8/8** (all 8 values new, none reused or missing) | **0 in 36 other Studio calls** (28 steady-state, 8 after a first post-compaction call) | the first Studio call after the compaction, 4.1-6.8 s later (median 5.1 s), i.e. the first step; no step ran unnoticed | 8 hex characters per call plus a rule of about 100 tokens once in the brief |
| SessionStart(compact) hook, same cells (paired reference) | 8/8 | 0 | before the next model call | 0 tokens per turn |

- Stop rule: not triggered (arm 1 caught 8/8). Decision rule fixed in advance for arm 1 ("adopted only if it detects at least what the
  self-check did, with 0 false alarms"): detection and false alarms meet it; brief loss is not measured by this arm (see Limits).
- All 8 compaction summaries still mentioned the nonce rule (8/8), which is why the model could obey it. A summary that drops the rule would
  show up as a missing nonce, which the scorer counts as a miss, not a hit.
- Cells: 2 compaction cells (start, P=2 steps, then K=4 x forced `/compact` + Q=2 steps) and 2 steady cells (12 steps, no compaction).
  4 cells, 56 client turns, 97 model calls, 0 failed turns. No re-serve of the brief.
- Setup: Claude Code 2.1.312, claude-sonnet-5-5, effort medium, headless `claude -p` with `--resume`, one process per turn, a per-cell
  home, only the two Studio stand-in tools. The stand-in Studio is `stub3.py` (mode `newnonce`).
- Scoring: `analyze3_nonce.py`. A compaction is a hit if the first Studio note after it carries a nonce different from the previous one;
  `changed-fresh` (never issued before) is counted separately from `changed-reused`. Any change outside a first post-compaction call is a false alarm.

Aggregates only: `phase3-newnonce-aggregate.json` (per-cell counts, signals, per-compaction latency). Session transcripts are kept private.

## Limits
- n = 8 compactions. With 8 of 8 the 95% lower bound on the hit rate is about 63%, so this is tentative; it clears the registered stop rule, it does not establish a rate.
- Short headless sessions (3-10k tokens of context), one model, one client version, forced `/compact`. Real long sessions and automatic compactions were not tested.
- The arm detects that a compaction happened (the model's own state changed), not whether the whole brief survived the summary; it only shows the nonce rule did.
- It depends on the model obeying the rule, and Studio can only act at the next call, not before the next model call as the hook does. No re-serve was tested here.
- Codex was not run (ChatGPT runs paused).

## Rerun
The scripts here are the ones that ran, except that the per-cell client home directory is named `cellhome` instead of `home`, the path defaults for ROOT and the login home were removed (set them yourself), and one unused settings-file name was dropped from the "installed" listing.
Needs the pinned Claude Code 2.1.312 client under a login home, as an unprivileged runner user (this step makes about 97 model calls).
```
ROOT=<new empty scratch dir>; mkdir -p $ROOT/cells $ROOT/bin
cp run-cell3.sh stub3.py stub2.py cc2.py extract2.py analyze3_nonce.py dry3.sh $ROOT/; cp bin/studio $ROOT/bin/
chmod +x $ROOT/run-cell3.sh $ROOT/dry3.sh $ROOT/bin/studio; cd $ROOT
./dry3.sh $ROOT/dry3-scratch                 # no model call; must print DRY3 PASS
export ROOT KH=<login home name with the pinned client>
./run-cell3.sh n1 newnonce 0 4 2 2 resume 0   # compaction cells, one at a time
./run-cell3.sh n2 newnonce 0 4 2 2 resume 0
./run-cell3.sh s1 newnonce 0 0 12 0 resume 0  # steady cells
./run-cell3.sh s2 newnonce 0 0 12 0 resume 0
/usr/bin/python3 -I analyze3_nonce.py cells/n1 cells/n2 cells/s1 cells/s2
```
Expected shape: `compactions 8, hook 8, hit 8, false_alarms 0`. The model's wording varies from run to run, so the exact nonces and latencies will differ.
The published aggregate is in `phase3-newnonce-aggregate.json`.
