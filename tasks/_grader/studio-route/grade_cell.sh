#!/bin/bash
# grade_cell.sh CELL_ID TASK PATCH : one-cell variant of night grade_batch2.sh (same route: MacBook pushes sealed rels to Studio stage, night_grade v2 / mac-private-v2, purge).
# Fails loudly: any staging step that fails (patch missing locally, scp/ssh/rsync error, result not retrieved) writes an infra result row
# ({"outcome":"grader_error","kind":"infra","cause":"patch_missing: ..."|"stage_failed: ..."}), prints the reason on stderr and exits 3. poll.py records that as
# invalid/infra (never control_apply) and grades the cell again. A normal grade returns 0 (night_grade's own verdict is in the results file).
set -uo pipefail
C="$1"; T="$2"; P="${3:-}"; N="probe-$C"; W=${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02/probe-luna-low-20261002/grades/work; S=${BENCH_GRADER_HOST}
ENVS="export BENCH_ROOT=\$HOME/bench BENCH_TASKS=\$HOME/bench/tasks NIGHT_STAGE=\$HOME/bench/.concurrent-grader/night-stage-$N"
G=bench/night-2026-10-01/grading
rm -f "$W/$N-results.jsonl"   # never let poll.py read the result of an earlier grade of this cell
fail() {  # fail "kind: reason"
  echo "grade_cell.sh $C: $1" >&2; echo "grade_cell.sh: $1" >> "$W/$N-grade.log"
  python3 - "$C" "$T" "$1" > "$W/$N-results.jsonl" <<'PY'
import json,sys
c,t,m=sys.argv[1:4]
print(json.dumps({"id":c,"task":t,"control":"candidate","outcome":"grader_error","kind":"infra","pass_":False,"cause":m}))
PY
  ssh -n $S "rm -rf ~/bench/.concurrent-grader/night-stage-$N" >/dev/null 2>&1 || true
  exit 3
}
if [ -n "$P" ] && [ ! -f "$P" ]; then fail "patch_missing: local patch not found: $P"; fi
python3 - "$C" "$T" "$G" > $W/$N-jobs.json <<PY || fail "stage_failed: could not write jobs file"
import json,sys
c,t,g=sys.argv[1:4]
print(json.dumps([{"id":c,"task":t,"patch":"${BENCH_HOME}/"+g+"/patches/"+c+".diff" if "$P" else "","control":"candidate"}]))
PY
ssh -n $S "mkdir -p $G/patches" || fail "stage_failed: ssh $S mkdir patches (rc=$?)"
if [ -n "$P" ]; then
  scp -q "$P" "$S:$G/patches/$C.diff" || fail "patch_missing: scp of $P to $S:$G/patches/$C.diff failed (rc=$?)"
  ssh -n $S "test -f $G/patches/$C.diff" || fail "patch_missing: $S:$G/patches/$C.diff absent after scp"
fi
scp -q $W/$N-jobs.json $S:$G/$N-jobs.json || fail "stage_failed: scp jobs file to $S failed (rc=$?)"
RELS=$(ssh -n $S "zsh -lc '$ENVS; cd ~/bench/night-2026-10-01 && python3 tools/night_grade.py --rels $T'") || fail "stage_failed: night_grade --rels $T failed (rc=$?)"
ssh -n $S "mkdir -p ~/bench/.concurrent-grader/night-stage-$N && chmod 700 ~/bench/.concurrent-grader ~/bench/.concurrent-grader/night-stage-$N" || fail "stage_failed: ssh $S mkdir stage (rc=$?)"
RELLIST=$(python3 -c "import json,sys;print(' '.join(sorted({r for v in json.loads(sys.argv[1]).values() for r in v})))" "$RELS") || fail "stage_failed: could not parse rels: ${RELS:0:120}"
for rel in $RELLIST; do
  ssh -n $S "mkdir -p ~/bench/.concurrent-grader/night-stage-$N/$(dirname $rel)" || fail "stage_failed: ssh $S mkdir $(dirname $rel) (rc=$?)"
  rsync -a --exclude _build --exclude deps --exclude node_modules ~/bench-sealed/$rel $S:bench/.concurrent-grader/night-stage-$N/$(dirname $rel)/ || fail "stage_failed: rsync of sealed $rel to $S failed (rc=$?)"
done
ssh -n $S "zsh -lc '$ENVS; cd ~/bench/night-2026-10-01 && python3 tools/night_grade.py grading/$N-jobs.json grading/$N-results.jsonl'" > $W/$N-grade.log 2>&1 || echo "rc=$?" >> $W/$N-grade.log
ssh -n $S "rm -rf ~/bench/.concurrent-grader/night-stage-$N"
scp -q $S:bench/night-2026-10-01/grading/$N-results.jsonl $W/$N-results.jsonl || fail "stage_failed: result file not retrievable from $S (grade log: $(tail -c 200 $W/$N-grade.log | tr '\n' ' '))"
