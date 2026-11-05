# Compaction detection without a hook, phase 2: markers, a self-check and installing the hook

Question: after an agent's context is compacted, how can a work-loop service (the stand-in here is called Studio) tell that the agent no longer holds the standing brief word for word, and how does it put the brief back? Phase 1 (`brief-marker-compaction-p1-20261105`) showed that one marker echoed on every call detects nothing, while the client's SessionStart(compact) hook detects every compaction. Phase 2 asks whether any other value held in context works, whether the agent can be told to install the hook itself, and which brief text to send.

**Result: mixed.** Markers held in context caught 0 of 8 compactions per variant. A self-check (`brief_seen`) caught every compaction that lost the brief, 31 of 31, with no false alarm in 90 calls. A hook that the agent installs fired on 29 of 29 compactions where the client let it write the file, and was refused 9 of 9 times in the client's default permission mode. The recommended text recovered the brief after 22 of 22 compactions. Codex was not run.

## Method
- Stand-in service: `stub2.py`, a stdlib Python MCP stdio server, plus a command-line stand-in `bin/studio brief --loop <id>`. `studio_start` issues a brief of 11 standing rules plus the arm's signal rule. Two rules are checked mechanically on every `studio_note` call: a ticket string and a note-text prefix, both random per cell. Every call is logged with the signal it carried, and a call is logged when the command-line stand-in runs, with the hook event if one arrives on stdin.
- Client: Claude Code 2.1.312, model `claude-sonnet-5-5`, effort medium, headless. Each cell runs with its own HOME and config directory, so anything an agent installs stays in the cell. Compaction is forced with `/compact` in the same session.
- Two drives: `resume` (one client process per turn) and `live` (one process for the whole cell, stream-json input), the closer model of a long interactive session.
- Cell: a start turn, P small writing steps ("answer, then record it with `studio_note`"), then K times a `/compact` and Q more steps. Step prompts never repeat the rules, the ticket, the prefix or the signal.
- A reference hook (SessionStart, matcher `compact`) is passed to every cell through `--settings`, invisible to the agent, and only logs. Every compaction is therefore also scored for a harness-installed hook: 102 of 102 fired.
- Arms:
  - `hash`: the signal is a content hash of the brief text. `nonce`: a random value. `rolling`: every response issues a new receipt and the next call must carry the latest one ("fetch it fresh").
  - `selfcheck` / `selfcheck2`: each `studio_note` carries `brief_seen="verbatim"` or `"summary"`; the service returns the brief on `"summary"`. `selfcheck2` is worded so that a re-served brief counts as verbatim. Run with and without re-serve, in both drives.
  - `guide-short`: the brief tells the agent to install a hook if its harness has one, with a receipt as fallback. `guide-exact`: the same plus the exact settings JSON. `guide-final`: the recommended text below, exact hook install plus the always-on self-check, with re-serve. The guidance arms get Bash, Read, Write and Edit, and run in the client's default permission mode and in `bypassPermissions`.
- Size: 8 forced compactions per marker variant (2 cells x 4), the size phase 1 chose from a paired sign test (8 events, all one way, give p = 0.004). The guidance arms were sized by sessions, since each install is one decision. Stop rule from phase 1: a variant at 1 of 8 or lower while the hook is at 8 of 8 is decided. One dry cell per new arm ran first and is not counted (`cells/p2dry-*`).
- Totals: 34 measured cells, 102 compactions, 0 failed turns, about 30 USD at list prices.

## Results
Per arm, counted over the measured cells (`python3 -I analyze2.py cells/m2-*`; the original output is `analysis-m2.txt`).

| arm | compactions | reference hook | detected without a hook | brief lost in summary and flagged | agent installed the hook | agent hook fired | false alarms / steady calls | signal tokens per call | rule violations after compaction |
|---|---|---|---|---|---|---|---|---|---|
| content hash | 8 | 8/8 | **0/8** (summary kept the hash 8/8) | 0/8 | n/a | n/a | 0/12 | ~7 | 0/16 |
| nonce | 8 | 8/8 | **0/8** (summary kept it 8/8) | 0/8 | n/a | n/a | 0/12 | ~6 | 0/16 |
| rotating receipt | 8 | 8/8 | **0/8** (summary kept the latest receipt 8/8) | 0/8 | n/a | n/a | 0/12 | ~6 | 0/16 |
| self-check, no re-serve | 14 | 14/14 | 4/4 first compactions | 4/4 | n/a | n/a | 0/30 | ~6.4 | 0/28 |
| self-check + re-serve | 18 | 18/18 | 15/18 | **13/13** (the 3 quiet ones: the summary held the whole brief word for word) | n/a | n/a | 0/36 | ~6.4 | 0/36 |
| guidance, default permissions (short wording, receipt fallback) | 4 | 4/4 | 0/4 | 0/4 | **0/2** (write refused) | 0/4 | 0/6 | ~6 | 0/8 |
| guidance, bypassPermissions (short and exact wording; both drives) | 20 | 20/20 | fallback unused | n/a | **10/10** | **20/20** | 0/30 | 0 | 0/40 |
| **recommended text, default permissions** | 16 | 16/16 | **16/16** | **14/14** | 0/4 (refused) | 0/16 | 0/24 | ~6.4 | 0/32 |
| **recommended text, bypassPermissions** | 6 | 6/6 | stays "verbatim" 6/6 (the hook put the brief back) | n/a | **3/3** | **6/6** | 0/9 | ~6.5 | 0/12 |

Pooled readings:
- **Markers:** the three variants together detected 0 of 24. Claude Code's compaction summary copies the current value every time, including the latest receipt, which sits in the most recent tool result. No value the agent can read in its own context works as a compaction signal. The first-message variant stays as phase 1 measured it: the service cannot observe it without a hook, and the agent-reported version caught 3 of 10.
- **Self-check:** it flagged 31 of 31 compactions after which the summary had lost the verbatim brief (one-sided 95% lower bound 91%) and raised no false alarm in 90 steady calls (upper bound 3.3%). It stayed quiet on 3 of the 7 compactions where the summary still held the whole brief word for word; there was nothing to restore. With re-serve it flagged 10 of 10 consecutive compactions in one arm. Cost: about 6 output tokens per call plus one brief (250 to 480 tokens here) per flagged compaction.
- **Guidance:** agents attempted the install in 25 of 25 sessions, before step 1. In the default permission mode the client refused the write to the settings file 9 of 9 times; the agents did not retry or ask, and switched to the fallback. Under `bypassPermissions` the install succeeded 16 of 16 and the agent's hook fired on 29 of 29 compactions (measured cells and dries), including single-process sessions where a hook installed mid-session fired on the next compaction.
- **Exact wording matters:** with the exact JSON in the brief, all 8 measured sessions wrote matcher `startup|compact`. With the short wording the agents chose 4 different matchers; where `resume` was included the brief was re-served on every resumed turn (14 extra re-serves, about 480 tokens each).
- **Recommended text:** the brief came back after 22 of 22 compactions (self-check 16 of 16 in default mode, hook 6 of 6 under bypass), 0 rule violations, 0 false alarms. The receipt as a fallback detected 0 of 4 where the install was refused, so the fallback must be the self-check.
- **Rule violations after compaction:** 0 in every arm (0 of 204 post-compaction calls). Every one of the 102 summaries kept both checked rules, so whether re-serving reduces violations is still unmeasured.

## Chosen mechanism
- **Claude Code:** a SessionStart hook with matcher `startup|compact` running `studio brief --loop <id>`, with the self-check always on as fallback and cross-check. Where the client runs in its default permission mode the agent's write is refused, so the launcher has to install the hook.
- **Codex:** not measured. Hooks are a stable feature in codex-cli 0.166.0 but need persisted trust per hook, so a hook the agent writes is not expected to run unattended; the brief must not ask the agent to write trust. The `.codex/hooks.json` line is inferred, not verified.
- **Harnesses without hooks:** the self-check with re-serve.

## Recommended brief text
Two standing rules at the end of the brief; the service fills `<loop-id>` and `<rev>`.

```
Context recovery, part 1 (once, now, before step 1): if your harness supports hooks, install a project-level hook in this working directory that runs `studio brief --loop <loop-id>` when a session starts and after every context compaction. Claude Code: merge this into .claude/settings.json: {"hooks": {"SessionStart": [{"matcher": "startup|compact", "hooks": [{"type": "command", "command": "studio brief --loop <loop-id>"}]}]}} . Codex: write the same JSON to .codex/hooks.json. If the write is refused or your harness has no hooks, do not retry and do not ask; part 2 covers you.
Context recovery, part 2 (always): every studio_note carries brief_seen="verbatim" if the full text of this Studio brief (the "STUDIO BRIEF rev <rev>" header and every rule, word for word, as Studio sent it, in any Studio response or hook output) is in your context window now, or brief_seen="summary" if you only have a summary or paraphrase of it. When you send "summary", Studio returns the brief.
```

The service side: `studio brief --loop <id>` prints the current brief on stdout (Claude Code adds SessionStart hook output to the context); every call takes an optional `brief_seen` field and returns the full brief on `"summary"`, or when the field goes missing after it was sent before; the brief revision stays in the header so a revised brief is also noticed.

## Limits
- Headless Claude Code only, with short sessions (10 to 19 thousand tokens per turn) and a forced `/compact`. Interactive sessions and auto-compaction of a long, full context were not run; rules could be dropped there, and only then does re-serving matter.
- One client version, one model, one effort, briefs of 200 to 480 tokens.
- The self-check is a model's report about its own context. It was accurate here, but it could drift with another model or a much longer context; the hook does not depend on the model.
- Only the client default and `bypassPermissions` were run; `acceptEdits` and a per-file allow rule for the settings file were not.
- Codex was not run. The Codex scripts were prepared and their command lines checked offline, but no model call was made.
- The service CLI and the `brief_seen` field are stand-ins in `stub2.py`; no product code was changed.
- Raw logs are redacted: paths, session ids and login names are replaced by placeholders and the per-cell session files were removed. `analyze2.py` still prints the per-arm table, but its per-cell "settings untouched" check needs the before/after stat files that were removed; use `analysis-m2.txt` for that check.

## Rerun
You need Claude Code 2.1.312 (the pinned release), a subscription login for it, Python 3 with only the standard library, and a scratch directory.
1. Copy the scripts into an empty scratch root: `mkdir -p $ROOT/cells && cp stub2.py cc2.py live.py run-cell2.sh extract2.py analyze2.py run-round2*.sh $ROOT/ && cp -R bin $ROOT/ && chmod 755 $ROOT/run-cell2.sh $ROOT/run-round2*.sh $ROOT/bin/studio`.
2. Set `ROOT` to that directory and `KH` to the name of a folder under `$HOME` that holds the client at `.kogen/claude-code/2.1.312/claude` and the login in `.kogen/credentials/claude-code.json` (`cc2.py` reads the token from that file into the environment; it never goes into argv).
3. Run the four batches one after another from `$ROOT`: `./run-round2a.sh; ./run-round2b.sh; ./run-round2c.sh; ./run-round2d.sh`. Batch d is the recommended text; batch a holds the marker variants and the self-check.
4. `python3 -I analyze2.py cells/m2-*` prints the per-arm table. To check the published numbers without running a model, run the same command on `cells/m2-*` in this folder and compare with `analysis-m2.txt`.

Files: `stub2.py` (service stand-in and reference hook), `cc2.py` (client launcher), `live.py` (single-process drive), `run-cell2.sh` (one cell), `run-round2a.sh` to `run-round2d.sh` (the measured batches), `extract2.py` (pulls each compaction summary from the transcript and checks what it kept), `analyze2.py` (table), `bin/studio` (command-line stand-in), `cells/` (redacted raw logs: `m2-*` measured, `p2dry-*` dry), `versions.txt`.
