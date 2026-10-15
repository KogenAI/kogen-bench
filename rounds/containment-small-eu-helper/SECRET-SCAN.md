# Privacy and digest gate

The staging gate script scanned the complete round, including the harness and the compact evidence archive. It found no malformed 40–128 character hexadecimal strings, forbidden run identifiers or private references, qualification-program identifiers, or token/key credential patterns.

Every 64-character digest in `README.md`, `ENVIRONMENT.md`, `DEVIATIONS.md`, `MEASURED.md`, `PROVENANCE.tsv`, and `INPUTS-SHA256.txt` matched a cited source digest or an explicitly hashed source harness file. The source pack digest, full-archive digest, and full-archive per-file manifest were accessed only through the required safe reader.

The safe-reader output does not expose the count of full-archive log files whose per-file digests and sizes were removed. The public round therefore states that privacy scrubbing removed those values for some log files and preserves the reported 713-file manifest count without inventing a redaction count. The source harness `SHA256SUMS` file is also a manifest: its safe-reader output does not provide the source file's own whole-file digest. The privacy-edited public harness manifest is included and hashed in this round.
