Task: Tenant access
Contract: contract.md
Checks: ./fv check (regenerates current application, checks fixed laws, runs starter tests).
Caps: 900 seconds; 60000 uncached input + output tokens (reasoning included in output); 10 complete check cycles.
Write DIAGNOSIS.md before your first patch.

Identify the violated property and causal function, explaining your evidence before patching. Repair the application to satisfy the fixed contract and preserve its API. Keep accepted laws and assumptions unchanged. Regenerate formal representations from the changed application and run the supplied checks. If verification fails because of a proof or tooling limitation, distinguish that from an implementation defect. Submit the patch and verification results within the budget.