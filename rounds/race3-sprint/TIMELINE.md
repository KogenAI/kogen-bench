# Sprint timeline

All entries are on 2026-10-10, in UTC. Times rounded to minutes are descriptive; exact host clocks are in results/run-clocks.tsv and results/snapshot-copy-times.tsv.

| Time | Event and evidence |
| --- | --- |
| Before 10:10Z | v2 wording/suite/harness patch assembled from the reviews; 144 total, 88 excluded, 56 scored, target 50. Every host/wave checks.txt reports inputs hash 2eeacf689c103dc3 and PASS frozen-inputs. |
| 10:10Z | w1 starts; actual START 10:10:02 MacBook and 10:10:08 Mac Studio. Original planned cap was 180 minutes. |
| 10:44:44Z | Mac Studio Go turn 0 ends. Resume rejects the sandbox -s flag and begins repeated immediate failures. |
| 10:46:16Z | Mac Studio Go logs its fake quota stall after failed turn 18; the regex matched an instruction-count substring in timing stderr. |
| 10:50:50–10:51:25Z | MacBook TypeScript, Mac Studio Rust and MacBook Go also reach their first resume and are affected. See the incident note's approximate lost windows. |
| 10:51–10:52Z | Resume/regex fixes and continuation script deployed mid-w1. Original loop killed while in-flight turns were left running; saved threads retained. The incident describes deployment approximately; copied rejection logs extend to about 10:52 on MacBook. |
| 11:17Z | w1 ended early by decision; FINAL copies complete at 11:17:44 MacBook / 11:17:41 Mac Studio. The mid-race harness change invalidates w1 as registered, per A1. |
| From 11:18:56Z | Initial w1 priority scoring begins, as shown by retained result metadata; historical priority.tsv files are included. |
| 11:31–12:01Z | w2, 30-minute cap. START 11:31:02 / 11:31:07; FINAL copies 12:01:07 / 12:01:14 (MacBook / Mac Studio). |
| 12:06–12:36Z | w3, 30-minute cap. START 12:06:02 / 12:06:07; FINAL copies 12:36:09 / 12:36:14. |
| After sprint FINALs | All-wave FINALs, accelerated time-to-target scoring, available repeats and then curve filling. Helper scripts allow concurrent scoring; metadata and warmup.tsv record actual scoring work. |
| 13:06Z | Transient subset validation rejects valid 56-case files against a 144-ID inventory. Corrected branch validates requested subset coverage; the five flags remain in copied logs. The minute is supplied by the bundle request, not timestamped in those flags. |
| Through 14:43:55Z | Latest retained scoring start is Mac Studio w3 Go T+020. Its w3 curve remains incomplete in the copied sources. This is a result start timestamp, not a completion time. |

The original rule planned two waves with three-hour caps. A1 planned replacement registered waves at 13:20Z and 16:30Z. Those times were overtaken by the actual sprint and are retained only as historical registration documents. The public bundle labels the whole sprint descriptive, preserving w1's explicit invalidation and the scoring/schedule departures.
