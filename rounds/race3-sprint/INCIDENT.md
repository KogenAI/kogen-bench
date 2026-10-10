# Race 3 wave 1 incident: continue turns failed (10:44–10:52Z)

**What happened.** `arm.sh` resumed each session with `codex exec resume "${FLAGS[@]}"`. FLAGS contains `-s workspace-write`, and codex-cli 0.162.1's `exec resume` rejects `-s`. So every continue turn failed in 0.01 s, and the loop spun (no agent work) from the moment an arm's first turn ended. The no-model smoke couldn't catch this, because it never resumes a model session.

**Second bug.** The stall regex `429|…` matched "85534293 instructions retired" in the `/usr/bin/time -l` output. That logged a fake stall (60 s wait) for Studio go and raised a false quota alert.

**Correction.**
- `arm.sh.fixed`: the resume uses `-c sandbox_mode="workspace-write"` (same sandbox, same network setting), the stall regex is word-bounded and ignores the time block, and a fast-fail guard was added.
- `arm-cont.sh` continues each arm from its saved thread (never a new turn 0).
- Deployed 10:51–10:52Z to all 10 arms. The original main loop was killed; any in-flight turn was left running.
- Verified: same thread ids, resumed turns stream events, a codex process is alive for every arm.

**Affected arms (no agent working between first-turn end and fix):**

| Host | Arm | Turn 0 ended | Resumed | Lost |
|---|---|---|---|---|
| Studio | go | 10:44:44 | ~10:51:25 | ~6.7 min (plus 1 fake stall entry, turn 18) |
| Studio | rust | 10:51:16 | ~10:51:50 | < 1 min |
| MacBook | go | 10:51:25 | ~10:52:00 | < 1 min |
| MacBook | ts | 10:50:50 | ~10:51:55 | ~1 min |

The other 6 arms were still in turn 0 and were never affected.

**Scoring/metrics treatment (proposal).**
- Disclose the incident.
- Report adjusted times with each arm's lost window subtracted, the same way as stalls, and keep raw times next to them.
- Remove the fake stall entry for Studio go from stall adjustment and replace it with the lost window.
- Note: Studio go reported 50/56 on its own suite run at the end of turn 0 (~T+34 min), so its primary time likely falls before the incident.
- Wave 2 runs with `arm.sh.fixed`, copied into the w2 dirs after the w1 unlock and before 13:20Z.


## Retrospective bundle note

The text above is the sanitized contemporaneous incident note. Its lost-time treatment was a proposal, not a completed registered adjustment. Amendment A1 invalidates w1 because the frozen harness changed mid-race. The sprint ended w1 early at 11:17Z; actual w2 was 11:31–12:01Z and w3 12:06–12:36Z, each with a 30-minute cap. The note's later planned start is historical.

The copied stderr streams confirm 100 rejected resume attempts: Mac Studio Go 67, Mac Studio Rust 8, MacBook Go 9 and MacBook TypeScript 16. Those private stderr files are not published. The supplied audit flags consist of the corresponding missing receipts. The sole logged quota stall is the fake Mac Studio Go entry at 10:46:16Z after turn 18; its alert is retracted and no quota wait is subtracted in the descriptive tables. Approximate lost windows remain separately disclosed; they are not promoted into exact timings.
