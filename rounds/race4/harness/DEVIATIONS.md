# Race 4: deviations from the frozen DECISION-RULE-v3 (sha256 45b6969f…)

The frozen rule file is unchanged. Every deviation below is disclosed with the results.

1. **Studio power losses (~14:10Z and ~14:59Z).**
   - The first hit before race 4 started.
   - The second killed Studio wave A at ~T+12 min (arms died ~14:58Z). It's kept as `race4-st-a-interrupted`: descriptive only, snapshots T+5 and T+10.
   - The stranded locks were restored at 15:03Z from the recorded modes.
   - A fresh Studio wave A' ran 15:06–16:06Z with identical frozen inputs, rule, kit and harness. Studio wave B ran 16:11–17:11Z.
   - All languages ran concurrently within each completed host wave. The effect of the interruption, restart and changed host timing on their relative results was not measured.
2. **No stop-on-target fired** in any wave: no arm's own full run reached 71/88. Per the rule's fallback, ranking is by official score at the 60-min cap (FINAL). The rule requires searching saved checkpoints for target attainment. Its near-target condition determines which snapshots require repeat scoring. Some searches did not complete, as described in INCIDENT.md.
3. A temporary change attempted to increase scoring concurrency and was reverted. Operator notes report that the shared worker limit prevented it from taking effect. The public bundle does not contain an independent concurrency trace.
4. Cross-host calibration was required to compare the same implementation snapshot on both hosts. This publication does not establish completion of that check or provide its per-case comparison.
5. Additional tests of integrating completed changes into Git missed the input freeze and were not part of the scored suite. No separate results for those tests are published here.
6. **Skipped before launch (deadline):** the real-install smoke and the full selftests on the frozen inputs. Both passed on the provisional inputs: FU3 33/33, FU4 37/37.

## Storage pruning (MacBook, 10 Oct ~18:10Z, main's order for free space)
- Race 3 sprint: build output (target, _build, node_modules, .venv, build, dist) was removed from the MacBook T+ snapshots of race3-mb-w1/w2/w3. Kept: every FINAL, the scored time-to-target crossings and their S−5 guards (w1: rust T+50/55, go and ex T+60/65), all source and all out/. The scores and curves were already computed (phase 3 finished 14:44Z), so no published number changes. Pruned T+ snapshots can't be rescored with executables.
- That's 29.7 GiB logical but only ~2 GiB physical (APFS clones). MacBook free space: 91 → 93 GiB.
- Earlier, main removed race3-mb-dry, r3-gate-dry-mb, race3-v2/smoke and user caches (80 → 91 GiB). Nothing evidential was touched.
