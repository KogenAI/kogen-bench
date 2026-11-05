# A brief marker did not detect compaction; the hook did

**Question.** Can a Studio-style service notice, without any harness hook and without a model call, that an agent lost its brief to context compaction? The mechanism tested: the brief carries a short marker, every Studio call echoes it, and the service flags a missing or stale marker. **Decision rule set beforehand:** adopt the hook-free marker if its detection is at least that of the Claude Code `SessionStart(compact)` hook and its token cost per call is near zero.

**Verdict: no.** The marker caught 0 of 26 forced compactions. The hook caught 52 of 52 on the same sessions. The decision rule fails; the marker is not a compaction detector.

## Method
- A small stand-in Studio server (`stub.py`, stdlib Python, an MCP stdio server) issues a brief of 11 standing rules plus the signal rule. Two rules are checked mechanically on every note call: a ticket id of the form `QX-nnnn`, and a note prefix `[lane-<word>]`. Both values are random per cell.
- Client: Claude Code 2.1.312, model `claude-sonnet-5-5`, effort medium, built-in tools off, only the two stub tools allowed. Each turn is a headless `claude -p --resume` call.
- Compaction is forced with `/compact` as the prompt of a resumed session. Claude Code then writes a compaction boundary and fires `SessionStart(source=compact)`. Compaction from a full long context was not tested.
- Arms:
  1. **marker**: every call carries `marker=SB-xxxxxxxx`, a hash of the brief revision plus a nonce.
  2. **first-message**: every call carries the first 8 words of the first user message the agent sees. This is agent-reported; the server cannot compute it (see limits).
  3. **hook** (reference): a `SessionStart` hook with matcher `compact`. Its firings are logged in every cell, so the hook is scored paired on every compaction.
- Each hook-free arm ran with and without "re-serve" (the server returns the brief when the signal is missing or changed).
- Cells: a start turn, P steps, then K times (`/compact` and Q steps). Step prompts never repeat the rules, ticket, tag or marker. Measured round m1: 8 cells. Stress batch s1: 3 cells with 8 back-to-back compactions each. Two dry rounds were instrument checks and are not counted. Raw logs for all of them are in `cells/`.
- Sizing: a paired exact sign test needs at least 5 events all one way for one-sided p < 0.05. The planned 8 events per hook-free arm, with the stop rule "marker at most 1/8 while the hook is 8/8", was reached in round m1, so no further sized round ran. The stress batch was extra.

## Results (measured cells m1 + s1)
| detector | compactions | detected |
|---|---|---|
| hook `SessionStart(compact)` | 52 | **52/52**, 0 firings outside a compaction |
| marker | 26 | **0/26** |
| first-message (agent-reported) | 10 | **3/10** (the first compaction in a session only; 0/7 later) |

- Paired marker vs hook: 26 compactions where only the hook fired, none the other way; exact one-sided sign test p = 0.5^26 ≈ 1.5e-8.
- Why: the compaction summary quotes the marker word for word (marker kept in 26/26 summaries here), so a compacted agent keeps sending a valid marker.
- Marker cost: about 6 tokens per call (`"marker": "SB-xxxxxxxx"`, chars/4). First-message: about 14. Hook: 0 per call, about 180-210 tokens once per compaction when it re-serves the brief.
- False alarms: 0 in 56 steady calls (30 marker, 26 first-message), one-sided 95% upper bound about 5.4 per 100.
- Rule loss: all 52 summaries kept both checked rules, and 0 of 80 post-compaction note calls broke a rule, with or without re-serve (95% upper bound about 3.7%). In this setting re-serving was not needed.
- Summaries of summaries (8 nested compactions) did not erode the marker or the rules: 24/24 kept both checked rules, with summary length growing from 4.0k to 6.3k characters.
- Output tokens per step turn were 338-453 across arms, within the noise of free-text answers.
- Notional cost of the counted cells: about 14 USD at list prices (subscription, no API key). The client's reported cost is an estimate.

## What this means
- Do not rely on a hook-free marker to detect compaction in Claude Code. Use the harness hook where one exists.
- A marker can still flag a stale brief revision (the service changes it) or a context with no marker at all (a fresh session). That is a brief-version check, not a compaction detector. It was not measured here.
- The first-message variant is not observable by a service without a hook or harness change; as an agent-reported proxy it depends on how the agent reads its context.

## Limits
- **Codex arm not run** (paused for budget reasons), so nothing here transfers to Codex, whose summarizer differs.
- Forced `/compact` in short sessions (about 10-12k tokens) with the brief in a tool result. Automatic compaction of a long context, with the brief far back, was not tested; rules could be dropped there, and only then would re-serving matter.
- One client version, one model and effort, one brief of 11 rules (about 200 tokens). Real briefs are longer.
- Headless resume starts a new client process per turn, so the stub restarts each turn. Interactive sessions were not tested.
- The planned no-compaction control cells ran 12 steady steps followed by 2 compactions (a shell `seq` quirk, since fixed), so false alarms are measured on steady calls inside other cells.

## Rerun
Needs a macOS or Linux machine, Python 3 (standard library only), the pinned client in `versions.txt` and a client home that is already logged in; no API key is needed or used. Create an empty working directory, copy `stub.py cc.py run-cell.sh run-round.sh extract.py analyze.py` into it and make the two `.sh` files executable. Then:

```
cd <working directory>
ROOT=$PWD KH=<logged-in client home name under $HOME> ROUND=m1 ./run-round.sh
ROOT=$PWD KH=<home> ./run-cell.sh s1-marker-a marker 0 0 8 2 1 &
ROOT=$PWD KH=<home> ./run-cell.sh s1-marker-b marker 0 0 8 2 1 &
ROOT=$PWD KH=<home> ./run-cell.sh s1-hook none 0 0 8 2 1 & wait
python3 -I analyze.py cells/m1-* cells/s1-*
```

`run-cell.sh <name> <mode> <reserve> <hook_reserve> <K> <P> <Q>` takes mode `marker`, `firstmsg` or `none`. To check the recorded numbers without running the client, run `python3 -I analyze.py cells/m1-* cells/s1-*` in this folder: it prints the per-arm table from the raw logs. Each cell's `summaries.jsonl` holds the compaction summaries with `kept_marker`, `kept_ticket` and `kept_tag` flags. Session ids and local paths in the logs are replaced with placeholders.
