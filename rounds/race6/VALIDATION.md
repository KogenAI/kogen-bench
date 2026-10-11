# Bundle validation

PASS: the original governing rule SHA-256 is b4e10a643a138d3402698bd8d326fba4bffd9e2e633d4c7f43fe3a56580b8033. Source/exported hashes are distinguished in PROVENANCE.tsv. The frozen host manifests differ only in the TCC probe and corresponding test; the literal invalid-round reading and accepted-deviation descriptive reading are both explicit.

PASS: all 16 source FINAL combined receipts were independently counted, each with 106 distinct cases. Their pass/fail/error totals agree with cells.tsv, the retained score receipts and source results JSON. No case rows or IDs are exported. First scores are below 103 and require no repeat. All 16 arms have classify-note audits and valid model/effort receipts under the accepted deviation; literal scores remain non-deciding.

PASS: python3 results/recompute.py independently verifies all 16 public per-arm counts, separate Elixir/Go medians, differences, spreads, paired differences, strict-separation direction labels, ambiguity labels and valid-slot counts. It verifies all 16 recovered cumulative token totals, cutoff timestamps, subset accounting and eight token-median rows. Original completed-turn usage remains absent; session-rollout usage is recovered and labelled separately. T+030m is unavailable everywhere.

PASS: the README's first prose paragraph matches the current RESULTS-R6.md first paragraph verbatim. The header uses five plain lines; both language tables, direction labels, the one tokens-to-kill-point table and current incident disclosures are included. Eight language/condition briefs plus TARGET.md and INTERFACE.md are present.

PASS: 247 source spec classifications verified: 15 PROSE, 161 QUINT, 8 GHERKIN, 63 D-ONLY. All four public subsets contain only the identical shared 15-file PROSE set; both host source subsets agree. The 232-row withheld manifest contains path/class/original SHA-256 only. The exact 401 B/C/D subset copies and 232-file unique union were hashed using the required C-locale pipeline. Source/export hashes agree with provenance and the source frozen manifest where registered.

PASS: no public payload hash equals a withheld suite or B/C/D file; no actual case IDs, inventory lists, per-case rows, suite/arm/runner payloads or agent rollouts are published. The audit summary withholds three arm-source excerpts while retaining its classifications, empty-substitution fix, supplemental parser guard and limitations. Fixture-bearing selftests/smokes and suite decoding/deduplication artifacts are omitted.

PASS: 16 rollout copies, eight per host, are byte-verified and retained only in owner-only private/. No network operation, commit, remote write, arm/suite execution, historical rebuild or regrade was performed during assembly. The public recomputation tool reads only public aggregate files.

SECRET-SCAN.md records the all-file secret/PII scan. SHA256SUMS is generated as the final public file after all content, scan reports and provenance, excludes itself, and is verified with shasum -a 256 -c SHA256SUMS. A final read-only closure scan includes every public file and checksum metadata. No public file is changed after checksum generation.
