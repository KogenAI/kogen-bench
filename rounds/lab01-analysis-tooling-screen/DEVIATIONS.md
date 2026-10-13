# Deviations and operational notes

## Set 1 validity

The first set 1 attempt is excluded because supervisor work overlapped on the host during the run, violating the isolation condition. It is not included in the measured scores or six-cell ITT cohort. The later valid run supplies the set 1 observations. The invalid attempt is summarized in the appendix without raw outputs.

Sinkhole and transcript audit: Blocking of the designated Kogen destinations was unverified for set 1 and the dry runs because the hosts file's permissions prevented the run user from reading it. The audit checked recorded command and tool inputs for forbidden destinations and network-tool use; it is not a traffic log and does not verify that blocking worked. For set 1 it covered three transcript files from the invalid launch and three from the valid repeat: 6 files, 68 commands, 0 forbidden-destination hits and 0 network-tool hits. For set 2 it covered 63 commands, with 0 hits of either kind. These counts do not establish a dry-run transcript audit. Only counts are published; transcripts and event streams remain private.

## Set 2 operational variant

Set 2 operating changes: The documented variant, called Option F, opened network access for each approved step and restored the restricted state afterward. Reviewed scripts used a shared lock with the scheduled network helper, and the hosts file was made readable by the run user. A bounded metadata scan covered approved evidence roots. An independent timer was armed to restore the restricted network state after 11,700 seconds. The comparison tool rejected the before/after scans because their declared scopes differed, so the preserved rows were classified manually. Two initially unexplained changes were later attributed under a documented supervisory clarification: scheduled helper activity explained the lock, and this run's normal network restoration explained its watcher log.

The final change classification was 2 additions, 9 changes and 0 removals: 7 HARNESS-CACHE (changes to this run's own support artifacts), 4 HOST-BACKGROUND (the expected hosts-file restore and scheduled host activity) and 0 UNEXPLAINED. This final classification supersedes the earlier preliminary stop summary.

## Harness and host incident

The source harness changed between sets. Set 1 used SHA-256 `9872860fb6df2a28e2407be621afe560f8c4877fe31afcbe33c5cae3f9eff31c`; set 2 used `9842756eb59e54509f83fcded53781703f396ae2263d6b4ded9d102a830da297` after Amendment 4.

Between sets, Amendment 4 corrected a smoke-test expectation: the interrupt/resume check had assumed the remaining-arm order from set 1 when checking the reversed sequence. The change affected that qualification check and its tests; scoring, outcome classification and measured-run execution were unchanged. Apparatus smoke tests for both sequences were rerun under the new hash before set 2.

On 12 October at about 18:13 UTC, the host froze during a metadata scan and recovered after reset. The scan and freeze coincided, but the available journal does not establish causation. The hosts-file mode issue meant an earlier DNS failure did not prove the sinkhole was active. Set 2 corrected the file mode and used preflight resolution and probe checks.

## Change-time scans

Set 1's broad scan recorded 3,321 additions, 17 changes and 0 removals, with all changes classified. The established-policy recheck examined 327,578 entries and had no errors, additions or removals apart from the expected hosts-file restore.

Set 2's scoped scan used complete pre- and post-snapshots of 2,085 and 2,087 entries, with zero errors. The comparator rejected the pair because declared scopes differed. The final classification was 2 additions, 9 changes and 0 removals: 7 HARNESS-CACHE, 4 HOST-BACKGROUND (the expected hosts-file restore and scheduled host activity) and 0 UNEXPLAINED. See `harness/CTIME-SCANNER.md` for the method summary.
