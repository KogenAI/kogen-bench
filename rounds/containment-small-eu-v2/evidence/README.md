# Compact evidence bundle

The public compact bundle contains 198 privacy-edited records: 99 fixture repetitions and 99 overhead records. Each row retains its original source SHA-256 and omits local paths, command lines, output streams, scope identities, and observer-note bodies.

The original compact evidence pack has SHA-256 `ae2d5a940a88fc3ccab2e61158c21ca1cb2c0ba10d8ddfb6f61561c6f6a48fd6`. The privacy-edited public bundle `compact-evidence-public.tar.gz` has SHA-256 `137d5ff74a925d1cb0ffea212c9712f71285d25c21b738b2883c3e719696edee`. The bundle includes `compact-records.jsonl` and `manifest.json`.

The manifest replaces source file names with entry numbers. The required safe reader redacted digest and size values for 438 log-path entries; the remaining digests and sizes are retained. This preserves every file entry without exposing local filenames or raw logs.
