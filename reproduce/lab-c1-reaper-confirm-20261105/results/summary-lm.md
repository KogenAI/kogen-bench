# Lab C1 confirmation results (lm)

```
| unit | host | arm | n | pass | median s (min-max) | orphans alive/zombie | 10m timeouts | failing tests |
|---|---|---|---|---|---|---|---|---|
| shaping | lm | A | 10 | 0/10 | 641.0 (605.1-641.4) | 0/0 | 10 | TestKillGroupOnExit  |
| shaping | lm | B | 10 | 10/10 | 238.4 (204.5-250.7) | 0/0 | 0 |   |
| shaping | lm | C | 10 | 10/10 | 240.4 (219.2-261.5) | 0/0 | 0 |   |
| verification | lm | A | 10 | 10/10 | 69.1 (68.7-69.5) | 0/0 | 0 |   |
| verification | lm | B | 10 | 10/10 | 68.9 (68.8-69.6) | 0/0 | 0 |   |
| verification | lm | C | 10 | 10/10 | 68.9 (68.5-69.1) | 0/0 | 0 |   |
| loop | lm | A | 10 | 0/10 | 649.7 (602.1-652.2) | 0/0 | 10 | TestCallerShellBoundCustody TestCallerShellBoundCustody/exits TestCallerShellBoundCustody/ignores TestCallerShellBoundObservationFailure TestContextEndTerminatesTheShellGroupBeforeRunReturns TestDeadlineTerminatesARunningShellGroup TestInterruptKillsAGroupThatIgnoresSIGTERM TestInterruptStopsAndRefuses  |
| loop | lm | B | 10 | 10/10 | 84.8 (32.8-87.7) | 0/0 | 0 |   |
| loop | lm | C | 10 | 10/10 | 86.1 (65.5-87.8) | 0/0 | 0 |   |
| sweep | lm | A | 10 | 10/10 | 11.6 (11.5-11.6) | 0/0 | 0 |  X-V1 survivors: none |
| sweep | lm | B | 10 | 10/10 | 11.6 (11.5-11.6) | 0/0 | 0 |  X-V1 survivors: none |
| sweep | lm | C | 10 | 10/10 | 11.6 (11.5-11.6) | 0/0 | 0 |  X-V1 survivors: none |
| fixture | lm | A | 10 | 0/10 | 5.2 (5.2-5.2) | 0/0 | 0 |  zprobe pass 0/10 |
| fixture | lm | B | 10 | 10/10 | 0.2 (0.2-0.2) | 0/0 | 0 |  zprobe pass 10/10 |
| fixture | lm | C | 10 | 10/10 | 0.2 (0.2-0.2) | 40/0 | 0 |  zprobe pass 10/10 |

arm A {"gotest_runs": 30, "gotest_passed": 10, "gotest_wall_s": 13480.3, "orphans_alive": 0, "orphans_zombie": 0, "fixture_runs": 10, "fixture_orphans": 0, "sweep_runs": 10, "sweep_passed": 10}
arm B {"gotest_runs": 30, "gotest_passed": 30, "gotest_wall_s": 3813.9, "orphans_alive": 0, "orphans_zombie": 0, "fixture_runs": 10, "fixture_orphans": 0, "sweep_runs": 10, "sweep_passed": 10}
arm C {"gotest_runs": 30, "gotest_passed": 30, "gotest_wall_s": 3898.4, "orphans_alive": 0, "orphans_zombie": 0, "fixture_runs": 10, "fixture_orphans": 40, "sweep_runs": 10, "sweep_passed": 10}
B/C median shaping lm: 238.4 / 240.4 = -0.8%
B/C median verification lm: 68.9 / 68.9 = +0.0%
B/C median loop lm: 84.8 / 86.1 = -1.5%

dry runs: lm/fixture/A:FAIL:5s:orph0 lm/sweep/A:pass:12s:orph0 lm/verification/A:pass:61s:orph0 lm/fixture/B:pass:0s:orph0 lm/sweep/B:pass:12s:orph0 lm/verification/B:pass:69s:orph0 lm/fixture/C:pass:0s:orph4 lm/sweep/C:pass:12s:orph0 lm/verification/C:pass:69s:orph0
```

## Rule check
- B go-test: 30/30 passed (rule needs 30/30 of the registered 30)
- B vs C median shaping: 238.4 / 240.4 s = -0.9% (n=10/10)
- B vs C median verification: 68.9 / 68.9 s = +0.1% (n=10/10)
- B vs C median loop: 84.8 / 86.1 s = -1.5% (n=10/10)
- B vs C pooled go-test wall: -2.2% (equal n only)
- B orphans over all B units (go-test, sweep, fixture): 0
- C fixture orphans alive (no helper, expected > 0): 40 over 10 runs
- A go-test fail rate (literal rule, all 3 repos): 20/30 = 67%
  A shaping: 10/10 failed, 10 hit the 10 min timeout
  A verification: 0/10 failed, 0 hit the 10 min timeout
  A loop: 10/10 failed, 10 hit the 10 min timeout
- Kill-group zombie probe pass: A 0/10, B 10/10, C 10/10
- A fail rate on hang-capable units (kogen-shaping go-test + fixture probe): 20/20 = 100%
- Runs set aside because a delivery Build appeared during them (repeated): 1; kept despite intrusion after 2 repeats: 0

- B clauses (30/30, within 10% of C per repo, 0 orphans): PASS
- A clause (>= 80% fail, literal, 30 go-test runs): NOT MET
- VERDICT: B CONFIRMED; the A >= 80% clause is not met at the literal reading (see A rows: only repos whose tests kill a group and wait hang)
