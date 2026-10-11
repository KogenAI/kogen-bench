# Race 6 timeline

All times are UTC on 2026-10-11. Approximate incident times follow the supervisor's record; FINAL copy clocks are per arm in results/run-clocks.tsv. Aborted/stopped attempts are disclosure only and never enter the score tables.

| Time | Event |
|---|---|
| 05:37 | Pre-launch smoke caught the nested-sandbox arm-killing bug; outer sandbox removed and harness re-frozen. |
| ~05:53 | Mac Studio TCC lock abort; no agents and no new mode-000 roots. |
| ~05:58 | MacBook inventory scan stopped; no agents or locks. |
| 06:02 | Relaunch on 67499abb; Mac Studio later failed the TCC probe on ENOENT versus EACCES. |
| 06:12 | Earlier MacBook attempt launched. |
| 06:13 | Earlier MacBook attempt stopped at ~1–3 minutes, unlocked; detached scoring killed. |
| 06:16 | Project lead accepted differing host probes/tests by speed call (RULES 31); literal rule still invalidates the round. |
| 06:26 | Counted MacBook wave began: Elixir and Go A–D together. Scheduler crashed at launch. |
| 06:28 | Counted Mac Studio wave began: Elixir and Go A–D together. Scheduler crashed at launch. |
| 07:26 | MacBook 60-minute cap reached; FINAL retained. |
| 07:28 | Mac Studio 60-minute cap reached; FINAL retained. Both frozen checks aborted during detached scoring; stop-time audits also crashed. |
| ~07:31 | Manual freeze checks passed without file differences. |
| ~07:33 | Detached scoring restarted; no earlier scores existed, no duplicate scoring. |
| 07:40 | Locale-dependent sort identified as freeze/spec-marker mismatch cause. |
| 07:41 | Empty-shell-substitution audit crash identified; post-hoc fix and supplemental parser guard disclosed. |
| 07:50 | Launch-time snapshot scheduler argument failure identified; T+030m unavailable everywhere. |
| After FINAL scoring | MacBook metrics failed on integer .strip(); ripgrep absent for pruning checks. Post-hoc audits classified all 16 arms classify-note. |
| ~08:35 | Publication overrides: initial status framing (superseded by main’s descriptive-pilot ruling under RULES 2); counts only; PROSE plus withheld manifests/hashes during L1–L3. |

INCIDENTS.md retains the full supervisor disclosures; results/AUDIT-SUMMARY.md records the subsequent audit resolution and frozen-version comparison.
