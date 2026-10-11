The recorded scan did not catch all identifying metadata: published method notes still contain personal analysis paths or account-label fragments. Its sanitization conclusion requires correction. This pattern scan does not guarantee the absence of identifying information.

PASS — zero unresolved findings, zero account emails, credential payloads, personal home paths/hostnames, case IDs, transcripts or arm/suite artifacts. Every public regular file is scanned, including metadata and this report; SHA256SUMS receives a final closure scan after generation. This is a content/pattern check, not a guarantee against every possible identifier.

| Check | Unresolved matches | Basis |
| --- | --- | --- |
| account_emails | 0 | All public content and paths checked. |
| personal_home_paths | 0 | All public content and paths checked. |
| personal_hostnames | 0 | All public content and paths checked. |
| personal_account_identifiers | 0 | All public content and paths checked. |
| API_keys | 0 | All public content and paths checked. |
| private_key_blocks | 0 | All public content and paths checked. |
| JWT_payloads | 0 | All public content and paths checked. |
| credential_assignment_candidates | 0 | All public content and paths checked. |
| suite_case_ID_pattern | 0 | All public content and paths checked. |
| exact_106_case_ID_inventory | 0 | All public content and paths checked. |
| withholding_boundary | 0 | All public content and paths checked. |
| nontext_public_file | 0 | All public content and paths checked. |

Classified benign matches: GitHub git SSH transport references are syntax, not account emails; named `kogen-fake-access` / `kogen-fake-access-old` authorization examples are public fake-protocol labels, not credentials. The generic user-home regex in archived checks.py is a normalization pattern, not a personal path. Credential-file references in orchestration/specification are not credential content; no authentication files were read or exported.

The private scanner compares public text against the complete 106-case ID inventory and a general feature/Quint ID pattern, and rejects suite/fixture/model/check/transcript/source directory boundaries. Selftest/smoke fixture code, raw case outputs, arm code, command bodies, transcripts and original input filenames/manifests remain private. Publish only publish/.

Counts/classifications are in SECRET-SCAN-MATCHES.tsv; values and commands are never shown. Private scan evidence is in private/.
