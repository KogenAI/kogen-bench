# An allow-list for the budget-off consumer test: not measured, no quiet Linux host

**Finding.** The measured comparison (the budget-off test as written against an allow-list projection, 32 producer trees, quiet and loaded, plus a mutation control) did not run: neither Linux host allowed to run it was ever quiet. In 260 checks of the two hosts between 11:06 and 12:42 UTC on 5 Nov 2026, not one found a host free of delivery Builds and other Lab runs with a load average under 1. The first host was held by another Lab until about noon and then ran a delivery Build; the second was released by the build-speed Lab at 11:05 (which never ran its own loaded arms either) but was then in use by a third Lab and delivery Builds at a load average near 18. A key-level replay of the recorded red diffs, which needs no host, shows what the measured run would have tested: all 4 differing keys behind the reported reds were red under the deny-list of their own window's test version, one of the 4 (a toolchain-probe status) is still red under today's deny-list, and none of the 4 is compared by the allow-list; the allow-list keeps any key that mentions a budget, so the planted-budget mutation key stays visible. This is a design check, not a measured false-red rate: the verdict is unresolved.

## Question
Does comparing an allow-list projection (the requests, the order and role of events, the checkpoint keys, the result outcome, the commit message, and every budget field) in `TestBuildRequestBudgetOff`, instead of the whole record minus a growing deny-list of volatile keys, remove its false reds without losing real ones? Registered rule (Studio Lab lever `lab-c6-consumer-overcoupling-allowlist-20261105`): 0 false reds for the allow-list across the trees and load levels, and the planted budget field caught in every run. Assumption `build-failures-c6-consumer-overcoupling-20261105`.

## What ran
- **Static replay (done, model-free, no host):** the four keys that differed in the saved red land logs and the classified table (`request_offset_ms`, `load_average`, step-sweep `ms`, toolchain-probe `status`) were checked against the deny-list of each kogen-build version of the test that was live in that window (V0 initial 2 Nov, V1 772102a, V2 10f190b, V3 edb7e91, head 956b151) and against the allow-list. `data/deny-lists.json` holds each version's volatile keys and suffix rules, with the link to the public file at that commit.
- **Measured part (prepared, not run):** `harness/` holds everything: 12 red-window trees (consumer = kogen-build main at the window time, producer = the window's candidate where a copy still exists, 3 of 12, otherwise the producer main it was landing onto) and 20 green producer mains (`trees.tsv`), the allow-list test `budget_allow_test.go` built into the same test binary as the tree's own test, a one-line mutation of a copy, the loaded level (Lab E2's four-stream replay, reused), and `analyze_c6.py` for the tables. Design size 32 trees x 2 arms x 2 load levels x 3 reps = 384 probes plus 12 for the mutation.

## Results
| check | result |
|---|---|
| recorded differing keys behind the reds | 4 (`request_offset_ms`, `load_average`, `ms`, `status`) |
| red under the deny-list of their own window's version | 4 of 4 |
| still red under today's deny-list (956b151) | 1 of 4 (`status`) |
| compared (so able to turn red) by the allow-list | 0 of 4 |
| versions of the test that had to change the mask during the window | 2 (V1, V3) |
| planted budget key kept by the allow-list | yes |
| measured probes (arms x trees x levels) | 0 of 396 designed; no false-red rate, no mutation result |
| guard checks of the two Linux hosts for a quiet moment | 260, quiet 0 |

- The red windows are 12 of the 14 reported; the other 2 are not identifiable from the saved land logs. For 9 of the 12, the candidate commit no longer exists in any host mirror, so those trees would have been base-only proxies.
- The static replay says nothing about false reds the deny-list could still produce on keys not yet seen, nor about whether the allow-list misses a real defect outside its fields; only the measured run and its mutation control test that.

## What this decides
Unresolved. No request is filed for the budget-off test: the allow-list is not proven, and kogen-build already masks 3 of the 4 keys. The other consumer-test pins named in the same analysis were listed without measurement; one, the scripted-executor fixture that fails when a producer adds a correction round, is a plain fixture change a request can make without a Lab. Run the measured part on a quiet Linux host (about 2 to 3 hours of host time) with the steps below.

## Rerun
```
cd reproduce/lab-c6-consumer-overcoupling-allowlist-20261105
python3 -I static_replay.py
```
This prints the four rows above and a JSON line with `keys 4, red_under_window_version 4, still_red_at_head 1, red_under_allow_list 0, mutation_key_kept_by_allow_list true`. The measured part: on a quiet Linux host with Go 1.27.2 and local mirrors of the public KogenAI repositories, as the lanes user, copy `harness/` and the Lab E2 files (`e2.py`, `sched.json`, `heavy-lab.sh` from its published pack) into one directory, then `bash driver.sh 25 12 20` (setup, quiet and load minutes) and `python3 -I analyze_c6.py <work>/out/probes.jsonl <work>/out/setup.tsv`. The test source lives in the public [kogen-build](https://github.com/KogenAI/kogen-build/blob/956b151/build/build_request_budget_test.go) repository.
