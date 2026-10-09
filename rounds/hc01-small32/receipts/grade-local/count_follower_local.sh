#!/bin/bash
# AMENDMENT-4/5: after each grade.sh-family (board, erase) cell's official grade appears in grades/hc01-grades.jsonl,
# run ONE v2 count run for it (sequential, Studio brief). Validation-family (syn-06, syn-31) cells get no count run.
# A grader_error count row (grading transport/lock failure) is set aside and retried at most twice.
set -u
B=${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02; cd $B
W=probe-luna-low-20261002/grades/work; GR=levers/hc01-lane/grades/hc01-grades.jsonl
for item in $(tr '\n' ' ' < levers/hc01-lane/ops-logs/bulk-grade-items.txt); do
  rest=${item#*:}; c=${rest%%:*}; t=${rest#*:}
  case $t in elx-port-board-publish-unpublish-public-boundary|elx-port-erase-account) ;; *) continue;; esac
  until grep -q "\"id\": \"$c\"" $GR; do sleep 60; done
  # non-delivery: DECISION-RULE counts it as effective tests_passed=0 (ITT convention), so no count run
  grep "\"id\": \"$c\"" $GR | grep -q '"outcome": "no_patch"' && { echo "$(date -u +%TZ) COUNT2 SKIP $c no_patch (effective tests_passed=0 by rule)"; continue; }
  for try in 1 2 3; do
    [ -e $W/counts2-$c-results.jsonl ] && ! grep -q '"outcome": "grader_error"' $W/counts2-$c-results.jsonl && break
    [ -e $W/counts2-$c-results.jsonl ] && mv $W/counts2-$c-results.jsonl $W/counts2-$c-results.jsonl.infra-$(date -u +%H%M%S) && sleep 120
    echo "$(date -u +%TZ) COUNT2 START $c try=$try"
    bash levers/hc01-lane/grade-local/grade_cell_counts_v2_local.sh "$c" "$t" public-source-location-withheld
    echo "$(date -u +%TZ) COUNT2 END $c rc=$?"
  done
done
echo "COUNT FOLLOWER DONE"
