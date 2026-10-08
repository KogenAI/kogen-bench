# Decision rule

Primary outcome is official full-suite rescue count, paired by original failure. Keep REPAIR with verification only if its rescue count exceeds CONTINUE by at least two and no REPAIR cell regresses versus the original failure. Determine regression from per-test PASS SET comparisons when official grade rows carry per-test outcomes. Publish the per-cell pass/fail sets in [data/per-test-results.json](data/per-test-results.json) and recompute the condition with [l3b_per_test_rule.py](reproduce/l3b_per_test_rule.py). If per-test outcomes are unavailable, state “no-regression unverifiable” and require aggregate tests_passed >= the original failure count. Otherwise do not keep the instruction.

REPAIR vs RESTART and CONTINUE vs RESTART are secondary descriptive comparisons only. No imputation or significance claim. Use only VALID, CONFOUNDED, INVALID, INTERIM, WITHDRAWN, and NOT-RUN.
