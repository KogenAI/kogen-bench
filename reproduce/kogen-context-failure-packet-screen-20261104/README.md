# Kogen Context failure packet: matched screen across four public tasks

**Question.** When a coding agent starts from a failing check, does an automatic Kogen Context source packet help it finish the task correctly, sooner or with fewer tokens than the same agent without the packet?

**Result: unresolved.** Every cell passed its hidden check in both arms. On the four decision tasks the packet arm was not faster: median model time was 43.6 s without the packet and 46.0 s with it (+5.6%). It also used more uncached input tokens: 99,066 against 122,166 in total (+23.3%). On both Rust tasks the packet did not name the file the agent finally edited. The earlier single-host speedup on ripgrep 2208 did not replicate here: 39.3 s and 31.3 s without the packet, against 45.2 s and 46.8 s with it. The registered rule (PROMISING needs outcomes at least equal plus 15% faster or cheaper; CLEAR LOSS needs the packet arm red where the plain arm is green in both repetitions) gives UNRESOLVED. Nothing here supports a general speed, cost or localization claim.

## Setup
- Tasks: four public SWE-bench Multilingual cases (Rust: ripgrep 2208 and ripgrep 2574; Go: a gin header-binding feature; JavaScript: an axios timeout case), plus one calibration case that is reported but kept out of the decision. Each task's hidden check was confirmed red on the parent commit and green on the reference fix on the same machine before any cell.
- Arms, matched in everything else: the same model (claude-sonnet-5-5, medium effort), client version, issue text, bounded initial failure output (4,000 bytes), tool allow-list, time cap (300 s per attempt) and one bounded follow-up after a red check. The packet arm also received the packet from a frozen Kogen Context research build (failure-evidence mode, 6,500-byte and 6-range caps, 1 s deadline). Packets were 3.1 to 5.5 KB and took under 0.31 s.
- Size: 5 tasks x 2 arms x 2 repetitions = 20 cells on one machine, run one at a time. The arm that went first was swapped in repetition 2. Only claude-sonnet-5-5 requests were seen, and list-price cost was $2.23.

## Results (model seconds and uncached input tokens per cell)

| task | rep | no packet | packet | packet named the edited file |
| --- | --- | --- | --- | --- |
| ripgrep 2208 | 1 | pass, 39.3 s, 16,288 | pass, 45.2 s, 16,669 | no |
| ripgrep 2208 | 2 | pass, 31.3 s, 13,867 | pass, 46.8 s, 17,611 | no |
| ripgrep 2574 | 1 | pass, 53.8 s, 16,786 | pass, 40.2 s, 17,383 | no |
| ripgrep 2574 | 2 | pass, 47.8 s, 14,965 | pass, 39.9 s, 18,009 | no |
| gin header binding | 1 | pass, 30.7 s, 10,380 | pass, 29.5 s, 10,973 | 1 of 4 files |
| gin header binding | 2 | pass, 29.4 s, 8,930 | pass after one follow-up, 59.5 s, 22,818 | 1 of 5 files |
| axios timeout | 1 | pass, 156.1 s, 10,377 | pass, 146.1 s, 9,273 | yes |
| axios timeout | 2 | pass, 146.8 s, 7,473 | pass, 143.8 s, 9,430 | yes |
| calibration (not in decision) | 1 | pass, 25.8 s, 24,559 | pass, 28.6 s, 28,185 | yes |
| calibration (not in decision) | 2 | pass, 27.2 s, 25,335 | pass, 19.9 s, 26,529 | yes |

## Limits
- Small sample: 4 decision tasks, 2 repetitions each, one machine. Single-cell timing differences of this size flip between repetitions (ripgrep 2574 and gin both did).
- Every task passed in both arms, so this screen cannot show an outcome effect. The tasks were not hard enough to separate the arms.
- The packet came from a frozen research build, not the current product binary.

## Rerun
From the published data: `python3 report.py cells.json` prints the table, the medians, the token totals and the registered verdict. `cells.json` has one record per cell: outcome, attempts, model, grade and packet seconds, token counts, list cost, models seen, packet bytes and packet recall. A fresh run needs the four public SWE-bench Multilingual instances above at their parent commits, each instance's own test patch as the hidden check, and Claude Code running both arms with the settings in Setup.
