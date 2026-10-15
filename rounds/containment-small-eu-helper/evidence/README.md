# Evidence package

The published compact evidence pack contains a privacy-edited matrix, run summary, overhead summary, cell diagnostics, the source pack digest, and a per-file manifest. The source compact pack's SHA-256 is `d81438a67bbe7fb4ea3e9ea72aa43ded82ff5b7e18c4fcda12c8a819715bcbb8`. The published compact bundle SHA-256 is `92849efd3382690fe493558a5e5382403f1e6019b0fde318c1021287450f916b`; its public file manifest is `manifest.json`.

The full archive has 827 members and remains on the test server. Its recorded SHA-256 is `73e9802dd654ffd0b191074232676c9516116cabbd27976bf23318ae488bce5b`. The per-file archive manifest covers 713 files. The full archive was not copied to or re-hashed on the publishing machine.

Privacy scrubbing removed the digests and sizes of some log files in the full archive manifest; the permitted safe-reader view does not expose their count. The compact pack omits raw observation coverage, individual samples, final-read snapshots, and some token fields. Hashes establish integrity against recorded digests; they do not establish measurement correctness.

The source summary identifies a compact pack and a separate full archive, but does not identify a standalone measurement transcript. No transcript or event stream is published here. The published compact pack is the audit surface available to readers.
