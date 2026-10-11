# Harness archive

DECISION-RULE-v3.md governed; original SHA-256 `45b6969f78f0397f7976b14525eb13609e4a3f73a9cb2a3452fda6568ea8707c`. Available Studio harness copies match that source pin. Staged MacBook sources contain out/ and logs only, so MacBook harness-copy byte comparisons remain unavailable; their checks report the same input and kit pins.

DECISION-RULE-v3-INTERNET.md did not govern; original SHA-256 `60bc3db1b6f20cdd3d859dd928061e77d9f5e0d74700b7dbd4105a8e065060ab`. Its title identifies it as “Race 4 internet policy — supervisor merge text.” The governing rule itself includes that internet/package-install policy.

This archive contains sanitized harness and scoring scripts, contestant briefs, rules and aggregate metadata. Case-ID inventories and run-version copies are withheld. The published comparison tables summarize available source checks; they do not supply those original files.

The scorer uses two runner jobs, ≤3 simultaneous arm-snapshots per host in a shared pool, a 60-second invocation timeout and an untimed version warm-up capped at 900 seconds. First-pass 68–74 counts require a second scoring and per-snapshot both-pass intersection. None of the retained first scores is in that band.

README-RACE4.md and RACE4-CHANGES.md retain preparation-era “pending” wording; frozen COUNTS.txt, TARGET.md, SCORE_CASES.txt, inputs.sha and run checks establish the admitted 88-case inventory. EXCLUDED-V3.txt is historical context; SPEC-BUG-CASES.txt is empty. Exact runnable regrading awaits the withheld suite and private implementations, neither supplied here.
