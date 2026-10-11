# Files changed for race 4

Historical preparation notes: statements below about pending inputs, placeholders and candidate failures describe work before the race. They are not the final run status. See the round README and publication validation record for the completed experiment.

New: `waves.sh`, `target-watch.sh`, `target_watch.py`, `score-wave.sh`, `bsearch.py`, `prepare-inputs.py`, `DECISION-RULE-v3.md`, `DECISION-RULE-v3.tmpl`, `LINUX-PORT.md`, `README-RACE4.md`, `selftest-race4.sh`, `test-target-watch.py`, `test-race4-syntax.py`, `test-race4-scoring.py`, `test-race4-prep.py`, `RACE4-SELFTEST.txt`, `CANDIDATE-VALIDATION.txt`, and this change inventory.

Updated runners/snapshots/audit: `start.sh`, `wave-plan.sh`, `arm.sh`, `arm-cont.sh`, `snap.sh`, `audit.py`.

Updated scoring/metrics: `score-arm.sh`, `score-one.sh`, `bsearch.sh`, `score-phase2.sh`, `score-all.sh`, `score-snap.sh`, `live-scorer.sh` (disabled), `scoring_config.py`, `validate-results.py`, `compare-scores.py`, `metrics.py`.

Updated gates/locks: `checks.py`, `suite-checks.py`, `brief-equality.sh`, `lock-studio.sh`, `lock-macbook.sh`.

Updated documents/metadata: `BRIEF.tmpl`, `BRIEF-rust.md`, `BRIEF-go.md`, `BRIEF-ts.md`, `BRIEF-gleam.md`, `BRIEF-ex.md`, `TARGET.md`, `COUNTS.txt`, `SPEC-BUG-CASES.txt`, `inputs.sha`, `DECISION-RULE.sha256`. Final-input metadata is intentionally pending, and the freeze step derives/renders all target values and IDs.

Deleted: `DECISION-RULE.md`, `DECISION-RULE-A1.md`, and the stale race3 scored-ID cache `SCORED-56.csv` (replaced by freeze-generated `SCORE_CASES.txt`).

The candidate in `inputs-placeholder/` is unchanged. No race, Codex session, network operation, install or commit was run. The initial prep read no files under Areas, user Codex homes or user Library. The reviewer follow-up explicitly authorized one real token_count format sample from the stated Codex session directory; no real rollout content was copied into this directory. Fixtures, output and changes stayed inside this harness directory.

Scoring is deferred until both waves finish to preserve the fixed five-minute B gap and no-live-scoring rule. The search also verifies earlier checkpoints after binary search to certify the first target snapshot when scores regress; this can take longer than pure binary search.

Reviewer token follow-up: added self-contained tokens-at.py, its tokens_at.py import adapter and test-tokens-at.py; updated target-watch.sh / target_watch.py, metrics.py, snap.sh (ISO TAKEN_AT), DECISION-RULE-v3.md / .tmpl, watcher/scoring/snapshot tests, selftest-race4.sh, README-RACE4.md, this inventory and RACE4-SELFTEST.txt. The real rollout format check was limited to one matching token_count line. Token tests use disposable rollouts inside this harness.

Reviewer scoring follow-up: added `combined_score.py`, `scoring-common.sh` and `test-combined-score.py`; updated `score-one.sh`, `score-wave.sh`, `bsearch.py` / `.sh`, `compare-scores.py`, `score-snap.sh`, `score-phase2.sh`, the metrics comment, both v3 rule files, scoring tests, the self-test driver, README and this inventory. Near-target FINALs now receive a second scoring. Official scores are per-snapshot/per-arm both-pass intersections; old wave-wide flaky-case penalties are superseded. SCORE_CONCURRENCY defaults to 3, accepts 1–3 and is enforced across wave directories by a shared host pool. Both rules and the race 3 sprint timing-case rationale are in the decision rule.
