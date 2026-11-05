# Alarm relays to main: one line per event removes every repeat; escalation and leases do not pay

**Finding.** Replaying the recorded alarm stream, 57% of the 1,092 alarm lines that ops-tick relayed to main repeat an event already relayed. Delivering one line per event (a stable kind+subject key, repeats add an occurrence) removes all of those repeats, cuts relay lines from 1,092 to 495 and relay messages from 439 to 303 (-31%), delays no first occurrence and drops none. Adding escalation to the next role adds 523 messages and 247 pages to the project owner at the recorded acknowledgement rate of zero, so it fails the registered rule. Leases have no measured target: one actor launches all work. This closes about a quarter of main's traffic, not the 91% quoted for main in the Studio issues.

## Question
Which layer of the planned Studio event/lease design removes the duplicate load on main: D1 stable key with one owner, D2 plus escalation on a missed acknowledgement, or D3 plus leases on work items? Registered before the replay as Studio Lab lever lab-loops-collide-s0-20261105. Rule: build the smallest layer set that removes at least 70% of duplicate messages reaching main, with no first occurrence delayed beyond the 10-minute acknowledgement interval and no alarm dropped; if escalation adds more messages than it removes, drop it.

## Method (no model, no seats)
Inputs are local operations logs: ops-tick.log (753 ticks, 30 Oct 04:57Z to 5 Nov 09:04Z; 588 relay messages, 1,568 lines), fleet-check.log (the alarm lines each tick saw), the acknowledgement table fleet-acks.tsv, the delivery admission log (2,133 rows) and main's session transcript, from which only timestamp, direction, sender and alarm codes were kept. The raw logs are operational and not republished; data/ holds what the replay reads: per-tick alarm lines cut to six words, daily message counts, admission summaries and the acknowledgement rows.
- D0 replays today's ops-tick rule: key = first two words of a line, relay a new key, relay it again when it has been open over 20 minutes and was last relayed over an hour ago, forget a key that is absent for one tick. It reproduces the logged relays within 4% (messages) and 8% (lines) over 31 Oct 13:08Z to 5 Nov 09:04Z, 606 ticks, 4.83 days. Alarm lines before 31 Oct 13:08Z are gone from fleet-check.log (it changed format), so those 147 ticks have counts only and are in no arm.
- Event = kind plus subject (finer than the ops-tick key for experiment, build-stall, studio-issue and futile-build lines). An event stays one event while its key is absent for no more than a merge window; main arm 60 minutes, sensitivity 0, 30, 120 and 360.
- D1 delivers one line per event at its first tick. D2 delivers to the owning role (declared per alarm kind: delivery, research or main), escalates to main after 10 minutes without acknowledgement and to the project owner after 20; acknowledgement rate swept 0 to 100%. D3 adds leases, measured on the admission log as launches of one item on two hosts within 60 minutes.

## Results
| arm | lines to main | relay messages to main | duplicate lines | events never relayed | messages added |
|---|---|---|---|---|---|
| D0 as is | 1,092 | 439 | 621 (57%) | 24 | - |
| D1 stable key | 495 | 303 | 0 | 0 | 0 |
| D2, 0% acknowledged | 292 (479 more to roles) | 198 | 0 | 0 | +523, 247 pages to the project owner |
| D2, 50% | 154 | 134 | 0 | 0 | +200, 62 pages |
| D2, 90% | 44 | 41 | 0 | 0 | +30, 3 pages |
- D1 removes 100% of duplicate lines at every merge window; duplicates are 39, 45, 57, 67 and 77% of D0 lines at 0, 30, 60, 120 and 360 minutes. Relay messages fall 17, 21, 31, 43 and 57%. The 24 events D0 never relayed were hidden under a coarser key already open.
- D2: recorded acknowledgements are zero in the replay window (40 rows in fleet-acks.tsv, the last expiring 31 Oct 08:33Z, no acknowledged line after the format change). It moves main's wakes to the roles and adds more messages than D1 at every rate below 100%. Its first delivery to main comes 11.5 minutes after the event (10-minute interval plus tick granularity).
- D3: 1,329 admitted launches by delivery (857 items) plus 10 rows whose caller field is not delivery's and carries no item, so no two named actors launch one item; 20 items launched on two hosts within an hour and 161 on one host, which the log cannot tell from retry-after-failure. No second actor collides, so leases have nothing to remove here.
- Reach: on 1 to 4 Nov main sent or received 1,453 messages; 363 (25%) were ops-tick relays, 106 steward messages named an alarm code, 14 restated one seen within 6 hours. One-line-per-event delivery saves 110 wakes (7.6%); removing every relay would save 25%. The remainder is free-form status and directive traffic that no layer of this design addresses.
- Cost of silence: 176 events stayed open over an hour and 32 over 6 hours; they supply 341 of the 621 repeat lines. A repeat relay is followed by the event clearing within an hour in 31% of cases against 21% for windows without a relay (n=607 and 479), a weak and non-causal difference. Long-open events therefore need the owner read (open events by owner with age and occurrence count) instead of re-delivery.

## Limits
- This is a replay of a policy, not of the Studio feature. The same policy can be applied in ops-tick directly; the feature is its product form.
- The owner map for D2 (which role owns which alarm kind) is an assumption, as is a uniform acknowledgement rate; the conclusion against D2 holds at every rate below 100% and rests on the recorded rate of zero.
- Admission rows carry no liveness, so the launch-pair counts are upper bounds. Alarm lines in the ops-tick log that fleet-check.log never held are not in any arm.

## Rerun
`python3 -I report.py` in this folder reads only data/ and prints every number above as JSON (`--json` is the same output); it is deterministic. extract/ holds the scripts that built data/ from the local logs (ops-tick.log, fleet-check.log, fleet-acks.tsv, the admission log, one session transcript) for anyone with equivalent logs: parse.py and d0.py align ticks, extract2.py and cascade.py count the message stream, make_data.py writes data/.
