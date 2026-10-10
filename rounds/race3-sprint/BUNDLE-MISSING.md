# Missing data and deliberate public omissions

All 30 FINAL case-result files are present and validate against the 144-ID inventory. The current frozen input source independently matches the registered digest. The following reporting gaps remain in the supplied sources; the bundle did not rerun agents or implementations to fill them.

- No FINAL has a repeat result file: 30 missing FINAL repeats.
- Only 15 of 92 first-pass snapshots in the 47–53 band have a repeat: 77 missing band repeats. Coverage is per host/wave/arm, not just per minute.
- No clean-copy FINAL regrade is present.
- No structured token_count events are present. All 30 FINAL cumulative totals are unavailable because each arm has an active unfinished turn. Eight w1 arms supply 11 terminal usage events; 22 arms supply none.
- Missing curve result files (eight):
  - Mac Studio w3 Rust: curve result files missing at T+025m
  - Mac Studio w3 Go: curve result files missing at T+025m
  - Mac Studio w3 TypeScript/Bun: curve result files missing at T+020m, T+025m
  - Mac Studio w3 Gleam/BEAM: curve result files missing at T+020m, T+025m
  - Mac Studio w3 Elixir: curve result files missing at T+020m, T+025m

Historical score TSVs have no headers; the derived TSVs do. Priority tables exist only for w1; no missing w2/w3 priority table is invented. Dedicated fast-fail logs contain no entries in the copies; explicit resume rejections are still counted from private stderr. Full per-turn timing sidecars are kept private with the streams, and numeric usage/timing summaries are public.

The public input copy redacts absolute home paths and one synthetic signing private-key body. It has separate exported SHA256SUMS and per-file original hashes. Tests requiring that redacted key cannot be replayed exactly from the public copy. Raced fixture emails ending in .invalid and fake protocol access examples remain as clearly synthetic data. No actual account auth file is included.

The public per-case JSONL is a deliberate field projection, preserving case identities/statuses/failure counts/step metrics while excluding captured file bodies, stdout/stderr, provider/OAuth payloads and other potentially identifying or source-bearing bodies. No raw per-case payload is copied elsewhere in this bundle. Full arm source, snapshots, toolchain/library kits and agent completion-message reports are excluded from publish. Full per-arm event JSONL, stderr and timestamp sidecars are kept only in private, byte for byte, as requested.
