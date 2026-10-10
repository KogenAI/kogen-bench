One more harness change (in `final/harness/lock-studio.sh` only), then re-verify `bash -n`, recompute nothing else unless the sha covers the harness (it covers `inputs/` only):
- Replace the single `$B/cx-jobs` lock candidate with every immediate subdirectory of `$B/cx-jobs` EXCEPT these six live publishing dirs: `PUB-PUSH`, `PUB-RTG1-STUDIO-1`, `CF-FIX`, `CF-CHECK-STUDIO-1`, `PUB-RTG1B`, `PUB-RTG1B-STUDIO-1`. `cx-jobs` itself stays unlocked. `$B/cx-live` is never locked.
- Use exact name matching, and keep the dedupe and the mode-000 refusal logic.
- Print the would-be candidate list with a dry-run flag `--list` (add it if missing) without changing any modes, and run `bash lock-studio.sh --list` to show it.
Then print `shasum -a 256 final/harness/DECISION-RULE.md` again.
