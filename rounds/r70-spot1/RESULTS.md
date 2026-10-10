# spot1 results

**DESCRIPTIVE SPOT CHECK; not a registered comparison.** Two tasks (r70-5 in Europe and r70-7 in the US) were run once in each of four languages. The retained launcher script sets a 1,200-second (20-minute) limit; the launcher log records 1,216 seconds between the Go task-7 start and timeout/end timestamps. Results are per cell.

The Go r70-7 attempt is an official FAIL because the launcher timed out (rc 124). A separate grade of the tree retained after stopping is PASS (24/24 tests); this does not change the official timeout outcome. The retained launcher script sets the cutoff at 1,200 seconds; its log timestamps span 1,216 seconds from start to timeout/end. Firewall rejection deltas were constant within each host: 30 per Europe cell and 72 per US cell.

| Cell | Task | Exact arm label | Official outcome | Tests | Failures + errors | Tests ran | After-stop tree grade | Launcher rc | Wall s | Firewall rejects |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| spot1-eu-r70-5-elixir | r70-5-elixir | elixir | FAIL | 24 | 1 | yes | — | 1 | 410 | 30 |
| spot1-eu-r70-5-go | r70-5-go | go | PASS | 24 | 0 | yes | — | 0 | 230 | 30 |
| spot1-eu-r70-5-rust | r70-5-rust | rust | PASS | 24 | 0 | yes | — | 0 | 210 | 30 |
| spot1-eu-r70-5-ts-bun | r70-5-ts-bun | ts-bun | PASS | 24 | 0 | yes | — | 0 | 231 | 30 |
| spot1-us-r70-7-elixir | r70-7-elixir | elixir | PASS | 24 | 0 | yes | — | 0 | 410 | 72 |
| spot1-us-r70-7-go | r70-7-go | go | FAIL (timeout) | 24 | 0 | yes | PASS (24/24) | 124 | 1216 | 72 |
| spot1-us-r70-7-rust | r70-7-rust | rust | PASS | 24 | 0 | yes | — | 0 | 180 | 72 |
| spot1-us-r70-7-ts-bun | r70-7-ts-bun | ts-bun | PASS | 24 | 0 | yes | — | 0 | 160 | 72 |

The corrected audit produced no flagged cells. Per-cell audit details are in [`audit-corrected.jsonl`](pulled-all/audit-corrected.jsonl); the retained audit outputs are in [`out/`](out/). A stage-probe attempt to label Elixir failures was withdrawn because the public Elixir environment did not reproduce the grading environment. No Elixir stage labels are used here.
