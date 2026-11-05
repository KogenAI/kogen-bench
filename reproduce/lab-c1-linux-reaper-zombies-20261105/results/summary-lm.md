| unit | host | arm | n | pass | median s (min-max) | orphans alive/zombie | 10m timeouts | failing tests |
|---|---|---|---|---|---|---|---|---|
| shaping | lm | A | 1 | 0/1 | 605.0 (605.0-605.0) | 0/0 | 1 | TestKillGroupOnExit  |
| shaping | lm | B | 1 | 1/1 | 210.5 (210.5-210.5) | 0/0 | 0 |   |
| shaping | lm | C | 1 | 1/1 | 217.9 (217.9-217.9) | 0/0 | 0 |   |
| verification | lm | A | 1 | 1/1 | 60.6 (60.6-60.6) | 0/0 | 0 |   |
| verification | lm | B | 1 | 1/1 | 70.5 (70.5-70.5) | 0/0 | 0 |   |
| sweep | lm | A | 1 | 1/1 | 11.6 (11.6-11.6) | 0/0 | 0 |  X-V1 survivors: none |
| sweep | lm | B | 1 | 1/1 | 11.5 (11.5-11.5) | 0/0 | 0 |  X-V1 survivors: none |
| sweep | lm | C | 1 | 1/1 | 11.5 (11.5-11.5) | 0/0 | 0 |  X-V1 survivors: none |
| fixture | lm | A | 1 | 0/1 | 5.2 (5.2-5.2) | 0/0 | 0 |  zprobe pass 0/1 |
| fixture | lm | B | 1 | 1/1 | 0.2 (0.2-0.2) | 0/0 | 0 |  zprobe pass 1/1 |
| fixture | lm | C | 1 | 1/1 | 0.2 (0.2-0.2) | 4/0 | 0 |  zprobe pass 1/1 |

arm A {"gotest_runs": 2, "gotest_passed": 1, "gotest_wall_s": 665.6, "orphans_alive": 0, "orphans_zombie": 0, "fixture_runs": 1, "fixture_orphans": 0, "sweep_runs": 1, "sweep_passed": 1}
arm B {"gotest_runs": 2, "gotest_passed": 2, "gotest_wall_s": 280.9, "orphans_alive": 0, "orphans_zombie": 0, "fixture_runs": 1, "fixture_orphans": 0, "sweep_runs": 1, "sweep_passed": 1}
arm C {"gotest_runs": 1, "gotest_passed": 1, "gotest_wall_s": 217.9, "orphans_alive": 0, "orphans_zombie": 0, "fixture_runs": 1, "fixture_orphans": 4, "sweep_runs": 1, "sweep_passed": 1}
B/C median shaping lm: 210.5 / 217.9 = -3.4%

dry runs: lm/fixture/A:FAIL:5s:orph0 lm/fixture/B:pass:0s:orph0 lm/fixture/C:pass:0s:orph4 lm/sweep/A:pass:12s:orph0 lm/sweep/B:pass:12s:orph0 lm/sweep/C:pass:12s:orph0
