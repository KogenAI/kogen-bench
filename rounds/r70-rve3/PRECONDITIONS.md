# rve3 preconditions: verified evidence (operational record, before the first cell)

Host preparation and network checks were recorded privately before execution; the findings are summarized here.

| Precondition | EU | US |
|---|---|---|
| Kit at 2ac8194…; doctor 0 FAIL | [R] setup rc 0, 80 OK / 0 FAIL, kit path ends 2ac8194… | [R] setup rc 0, 80 OK / 0 FAIL, kit resolves 2ac8194… |
| Root git safe.directory | [R] "safe.directory … present". [B] the check required the value `*` | [R] "`safe.directory` … present". [B] same |
| resolv.conf is a regular file | [R] "resolv.conf … present". [B] the check was `test -f && ! -L` | [R] "regular resolver configuration file" |
| Egress firewall table | [R] "nft table … present". [E] provider-only firewall present | [R] "nft table … present". [E] same check passed |
| Egress probe | [R] DNS passed; chatgpt.com HTTP 403; three GitHub URLs blocked (000). [B] run as bench inside the lane's agent sandbox | [R] DNS works; chatgpt.com 403; GitHub blocked/000. [B] same |
| Prompt preflight r70-{1,5,7}-{rust,elixir} | [R] all six OK | [R] all six OK |
| Dry cell with full record | [R] rc 0; patch 16,805 B; grade.json and manifest present; runner_rc 0; graded; prompt 6a593a6a; tests 24, failures 0, tests_ran; failure-set ≠ rve2's d4c076d11e. [B] run id rve3-dry-eu, task r70-5-rust | [R] rc 0; patch 11,960 B; grade + manifest present; runner_rc 0; graded; prompt 10d81ef5; 24/0, tests_ran; ≠ rve2's a54b7e2e29. [B] run id rve3-dry-us, task r70-7-elixir |

The dry cells are unscored and outside the round: **[P]** `PLAN.json` contains no `rve3-dry` run id (0 matches).
