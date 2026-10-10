# Public secret and PII scan

**PASS — zero unresolved secret/PII findings; zero agent transcripts or arm source trees.** This is a content/pattern scan of every public regular file, including this report. It is not a guarantee against every possible identifier format.

| Check | Matches | Classification |
| --- | --- | --- |
| Email-shaped strings | 5931 in 77 files | All are synthetic fixture addresses ending in .invalid; zero account emails. |
| sk- API keys | 0 | None. |
| Bearer tokens | 4 in 2 files | Only the two named fake protocol examples in the raced spec; zero actual access credentials. |
| Absolute home paths | 0 | None; public home paths were normalized to ~. |
| auth.json filename references | 53 in 23 files | Suite/audit code and documentation references only. |
| Actual auth.json files | 0 | No account credential file copied. |
| Private-key blocks | 0 | The synthetic signing-key body was redacted. |
| AWS access keys | 0 | None. |
| JWT-shaped credentials | 0 | None. |
| Original personal hostnames | 0 | None; normalized to MacBook/Mac Studio. |
| Per-arm transcript filenames / event rows | 0 / 0 | No turn JSONL, stderr, timestamp sidecars or agent event objects in public. |
| Arm-language or snapshots directories | 0 | None. Benchmark models, fixture programs and runner code are the requested suite inputs. |

SECRET-SCAN-MATCHES.tsv lists file/category/count/classification for every benign match without reproducing account or credential values. Per-case exports use an explicit field allowlist; captured file/source bodies, stdout/stderr, provider/OAuth and sandbox payloads are excluded. Private streams were not scanned into or copied to the public artifact. Only publish/ is suitable for publication.
- 2026-10-10T19:11:52Z: an account label in 32 files was replaced with 'the shared Codex account' and SHA256SUMS regenerated.
- 2026-10-10: a private infrastructure reference in a spec helper was reworded; its logic is unchanged and SHA256SUMS was regenerated.
