# Race 4 timeline

All race entries are 2026-10-10 UTC. Incident minutes come from DEVIATIONS.md; snapshot clocks come from out/snap-times.log. MacBook scheduled epochs are independently retained in arms.log and the staged waves record; original START files were not staged.

| Time | Event |
| --- | --- |
| ~14:10Z | First Studio power loss, before Race 4 launch. |
| Before launch | Freeze: 88 total/scored cases, target 71; pending Quint landing group omitted. Frozen-input real-install smoke and full selftests skipped for the deadline. |
| 14:47Z | MacBook A and original Studio A start epoch. MacBook first event streams begin just after the epoch. |
| ~14:58–14:59Z | Second power loss kills Studio A around T+12; T+5/T+10 incident telemetry retained. |
| 15:03Z | Stranded Studio lock modes restored, per deviations. |
| 15:06–16:06Z | Fresh Studio A′, counted A. FINAL 16:06:00.178957Z; set copy 10.2 seconds. |
| 15:47Z | MacBook A FINAL 15:47:00.508500Z; set copy 8.9 seconds. Waves record says done 15:47:25Z. |
| 15:52–16:52Z | MacBook B scheduled window. FINAL 16:52:00.032568Z; set copy 8.8 seconds. Waves record says done 16:52:24Z. |
| 16:11–17:11Z | Studio B. FINAL 17:11:00.227807Z; set copy 8.9 seconds. |
| ~17:03–17:10Z | Brief higher-concurrency edit, reverted; shared pool remained ≤3 according to deviations. |
| ~18:10Z | Older Race 3 storage pruning on MacBook; no Race 4 score changes stated. |
| Through 18:55:43Z | Studio waves record says B scored 18:55:39Z and A scored 18:55:43Z. Separate source logs report search/boundary failures on both hosts; labels do not establish complete searches. |
| Publication update | All 20 counted FINALs included; all 39 static flags adjudicated. Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. |

Linux dry cells were mechanics checks only and are not Race 4 results.
