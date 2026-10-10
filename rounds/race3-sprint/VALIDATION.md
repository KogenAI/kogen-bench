# Bundle validation

PASS: original input digest independently matches 2eeacf689c103dc3; original decision-rule SHA matches its A1 pin. All 494 sanitized input file checksums verified. The six source copies remain read-only.

PASS: all 267 public per-case files preserve original case ID/status pairs, have unique IDs and allowed statuses, and contain the complete 144-ID or 56-ID inventory. All 30 FINALs have all 144 IDs and match the derived FINAL table. Per-case fields and step metrics conform to the public projection allowlist; captured source, command output and provider/auth payloads are absent.

PASS: 267 latest historical score-table keys compared against the retained case files; 0 differences. score-table-comparison.tsv records any differences without silently rewriting historical tables.

PASS: repeat coverage is 0/30 FINALs and 15/92 band snapshots; 100 rejected resume attempts, 11 terminal usage events and unavailable FINAL token totals for all 30 arms verified. Missing curves are reported explicitly. This verifies the supplied data, not completion of the registered protocol.

PASS: all 423 private event/stderr/timestamp files are byte-identical to their sources and match private checksums. Private directory permissions are restricted to its owner. New public guide links resolve locally. Source-derived historical documents can refer to unbundled original locations.

No agents, arm programs, scorer scripts or test fixtures were executed. No network or git operations were used. Public secret/PII and transcript-boundary checks are recorded in SECRET-SCAN.md.
