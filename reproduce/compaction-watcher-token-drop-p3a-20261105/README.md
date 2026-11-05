# Compaction detection without a hook, phase 3 stage A: transcript watcher and token-drop detector

Question: when an agent's context is compacted, can a work-loop service (the stand-in here is called Studio) notice it without asking the model, so that it can put the standing brief back? Phases 1 and 2 (`brief-marker-compaction-p1-20261105`, `brief-compaction-detection-p2-20261105`) showed that values held in context fail and that a self-check works. Phase 3 stage A tests two detectors that need no model call.

**Result: both detectors work on real long sessions; only the watcher works on short ones.** The transcript watcher caught 173 of 173 forced compactions in the phase 1 and 2 cells, 129 of 129 real Claude Code compactions (124 automatic) and 165 of 165 real Codex compactions. The last two rates hold by construction (see Limits). The token-drop detector caught 0 of 173 in the short cells, and 129 of 129 and 165 of 165 on real sessions, with about 0.002 false alarms per 100 Claude calls and none on Codex. This is a model-free replay: no model call was made. The new-nonce instruction arm (stage B) is not part of this finding.

## Method
- **Watcher (arm 2):** a process outside the model reads the harness transcript and reports a compaction entry. Claude Code: a `system` entry with subtype `compact_boundary` (and the summary entry that follows it). Codex: a top-level `compacted` rollout entry. It tails the file by byte offset, parses only lines that contain a marker string, and uses the standard library only. Code: `watch3.py`, `detect3.py`.
- **Token-drop detector (arm 3):** fires when the context size of a model call fell against the previous call by at least 40% and at least 5000 tokens. Both thresholds were fixed in the registered plan and not tuned. Context size: Claude Code = input + cache read + cache creation tokens of the call; Codex = input tokens of the last-call usage record (the running total only grows). Code: `detect3.py`.
- **Replay (a), phase 1 and 2 cells:** 62 cells with 173 forced compactions (148 in one-process-per-turn cells, 25 in 11 single-process cells). Truth = the forced `/compact` turns, which equal the hook firings and the summaries found in the transcripts (173 = 173 = 173). Code: `analyze3.py`; counts: `phase3-cells-aggregate.json`.
- **Replay (b), real sessions:** the author's own Claude Code sessions (95 files, 99,519 model calls, main chain only) and Codex rollouts (4,950 files, 77,340 calls), read in place and read-only. Truth = the compaction entries themselves. A compaction is counted once by its boundary id, because resumed files replay older entries. Code: `real3.py`; counts: `phase3-real-aggregate.json`.
- A "turn" is one model call. Latency = model calls completed after the compaction before the detector fires.

## Results
| detector | phase 1 and 2 cells (173 forced) | real Claude Code (129) | real Codex (165) | false alarms | latency |
|---|---|---|---|---|---|
| transcript watcher | 173/173 | 129/129 (by construction) | 165/165 (by construction) | 0 | 0 calls: the entry is written before the next call |
| token drop | **0/173** | 129/129 | 165/165 | 0 in 582 cell calls; Claude 2 events (1 distinct) in 99,519 calls, about 0.002 per 100; Codex 0 in 77,340 | 1 call: the drop shows only in the first call made from the compacted context |

- **Why token drop fails on short cells:** the contexts are 3.6 to 10 thousand tokens, mostly the fixed system prompt, tools and brief. After `/compact` the next call is as large as or larger than the one before (for example 7,824 to 9,051 tokens), so no drop appears.
- **Real sessions:** the drops are large. Median context before and after: Claude Code 816k to 14k tokens (smallest context before a compaction 217k), Codex 243k to 20k. Of the 129 Claude Code compactions, 124 were automatic and 5 manual. 20 more boundary entries were replayed copies at the start of resumed files; they have no earlier call in their file, so the token-drop detector has no baseline there and they are not counted as misses.
- **The one distinct Claude false alarm:** a 760k to 72k fall with no compaction entry, next to resume-like entries. The cause cannot be proved from the entries; it is probably a context loss from a restart, which is also a lost-brief event. It is counted as a false alarm for "compaction".
- **Watcher cost:** in a replay of a synthetic file fed from a live stream, 24 polls in 14.4 s used 0.0038 s of CPU (0.026% of one core) and 18 MB of memory; a compaction was reported 0.48 s after it was written, one poll interval. A cold scan of the largest transcript (231 MB, 125k lines) took 0.43 s of CPU and 38 MB.
- **Neither detector says whether the brief survived the summary.** They trigger a re-serve on every compaction, which costs about 200 to 480 tokens.

## What this means for a service
- Both detectors can only act at the agent's next call to the service, so a flag re-serves the brief there. A hook acts before the next model call.
- The transcript does not name the service's loop. The launcher has to pass the loop id and the transcript path to the watcher.
- Claude Code: use the hook where it can be installed; use the watcher where it cannot and as a cross-check; keep the self-check as the always-on fallback. Codex: the watcher plus the self-check, token drop as a cross-check. Harnesses without a readable transcript: the self-check, plus token drop on long sessions and only if the harness reports per-call usage.

## Limits
- On real sessions the watcher is checked against the same entries that define the truth, so its 100% is by construction. The independent evidence is the token-drop detector agreeing on all 294 observable compactions, and, in the cells, hook = summaries = forced compactions (173 each). A compaction the client failed to write an entry for would be missed by both detectors only if the context also did not drop; none was seen.
- The real-session corpus is private (one user's own sessions, windows up to 1M tokens, models not tabulated). Only aggregate counts are published; no transcript, excerpt, path or session id is included, so the real-session numbers cannot be recomputed by an outside reader. Other clients, client versions and window sizes were not tested. Claude Code subagent transcripts were skipped.
- Codex compactions could include replayed copies after a resume; all 165 timestamps were unique.
- The watcher cost was measured on a synthetic feed, not on a running production loop. `watch3.py` is a stand-in and is not wired to any product.
- The raw cell logs of phases 1 and 2 are published with those findings, not here; the cell numbers here are their aggregate.

## Rerun
Python 3, standard library only; no login and no model call.
1. Copy `detect3.py`, `watch3.py`, `real3.py` and `analyze3.py` into one empty directory.
2. Phase 1 and 2 cells: run `python3 -I analyze3.py <cell directories>` over cell directories from the two earlier findings (each holds `events.jsonl`, `hooks.jsonl` and the turn or stream logs). The result should match `phase3-cells-aggregate.json`.
3. Real sessions: run `python3 -I real3.py` on a machine with your own Claude Code or Codex sessions. It prints aggregate counts only. Your numbers will differ from `phase3-real-aggregate.json`, which comes from the private corpus; the check is that the token-drop detector agrees with the compaction entries and raises few false alarms.
4. Watcher on one file: `python3 -I watch3.py --harness claude --loop <id> --file <session-log.jsonl> --from-start` (`--harness codex` for rollouts).

Files: `detect3.py` (both detectors), `watch3.py` (live tail), `real3.py` (real-session replay), `analyze3.py` (cell replay), `phase3-cells-aggregate.json`, `phase3-real-aggregate.json`.
