# Provenance

PROVENANCE.tsv maps copied/derived source evidence to original and public hashes. Generated metadata and the offline verifier are publication-only artifacts covered by SHA256SUMS. Original-source hashes differ from public hashes when home paths, hostnames or account identifiers were sanitized. The governing rule retains its exact original SHA-256. Input commitments use the recipe and scopes in INPUTS-SHA256.txt; private filenames, suite IDs and transcripts are not exported.

The complete original analysis and selected local/remote production turn streams were copied to private/, with read-only SSH/rsync or bench-manager host-root reads. Only permitted production run/harness paths were read; authentication files were not accessed. No commits, source changes, regrading or harness execution occurred.
