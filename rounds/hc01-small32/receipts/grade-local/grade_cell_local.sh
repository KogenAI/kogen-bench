#!/bin/bash
# grade_cell_local.sh CELL_ID TASK PATCH [PREFIX]
# HC01 AMENDMENT-6: the official night_grade v2 / mac-private-v2 route run on this MacBook instead of over ssh on the Studio.
# The grader code is the byte-identical ~/bench/night-2026-10-01 tree (runner/bench.py 089c63ed, runner/concurrent_grade.py d40b7562,
# tools/night_grade.py 4f35bbe9, night-env.sh 4bdbaebb). BENCH_TASKS is ~/bench/hc01-grade-tasks: a byte copy of the Studio's grading
# task root (synthetic/{bin,warm,trackline,ports} tree-sha-equal; the 4 HC01 task dirs), with only the absolute path prefix in task.json
# relocated (see ~/bench/hc01-grade-tasks-asrun/RELOCATION.txt). Sealed rels are staged from ~/bench-sealed exactly as grade_cell.sh does.
# Invoked as the original: zsh -lc with exported BENCH_ROOT/BENCH_TASKS/NIGHT_STAGE (toolchain pinned by task.json env).
# Same failure semantics as grade_cell.sh (infra row + exit 3). PREFIX (default probe-) names the work files; parity runs use another prefix.
set -uo pipefail
C="$1"; T="$2"; P="${3:-}"; PFX="${4:-probe-}"; N="$PFX$C"
W=${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02/probe-luna-low-20261002/grades/work
export BENCH_ROOT=$HOME/bench BENCH_TASKS=$HOME/bench/hc01-grade-tasks NIGHT_STAGE=$HOME/bench/.concurrent-grader/night-stage-$N
G=$HOME/bench/night-2026-10-01/grading
rm -f "$W/$N-results.jsonl"
fail() {
  echo "grade_cell_local.sh $C: $1" >&2; echo "grade_cell_local.sh: $1" >> "$W/$N-grade.log"
  python3 - "$C" "$T" "$1" > "$W/$N-results.jsonl" <<'PY'
import json,sys
c,t,m=sys.argv[1:4]
print(json.dumps({"id":c,"task":t,"control":"candidate","outcome":"grader_error","kind":"infra","pass_":False,"cause":m}))
PY
  rm -rf "$NIGHT_STAGE"
  exit 3
}
if [ -n "$P" ] && [ ! -f "$P" ]; then fail "patch_missing: local patch not found: $P"; fi
python3 - "$C" "$T" "$G" "$P" > $W/$N-jobs.json <<'PY' || fail "stage_failed: could not write jobs file"
import json,sys
c,t,g,p=sys.argv[1:5]
print(json.dumps([{"id":c,"task":t,"patch":(g+"/patches/"+c+".diff") if p else "","control":"candidate"}]))
PY
mkdir -p "$G/patches" || fail "stage_failed: mkdir patches"
if [ -n "$P" ]; then cp "$P" "$G/patches/$C.diff" || fail "patch_missing: copy of $P failed"; fi
cp "$W/$N-jobs.json" "$G/$N-jobs.json" || fail "stage_failed: copy jobs file"
RELS=$(zsh -lc "cd ~/bench/night-2026-10-01 && python3 tools/night_grade.py --rels $T") || fail "stage_failed: night_grade --rels $T failed"
mkdir -p "$NIGHT_STAGE" && chmod 700 "$HOME/bench/.concurrent-grader" "$NIGHT_STAGE" || fail "stage_failed: mkdir stage"
RELLIST=$(python3 -c "import json,sys;print(' '.join(sorted({r for v in json.loads(sys.argv[1]).values() for r in v})))" "$RELS") || fail "stage_failed: could not parse rels"
for rel in $RELLIST; do
  mkdir -p "$NIGHT_STAGE/$(dirname $rel)" || fail "stage_failed: mkdir $(dirname $rel)"
  rsync -a --exclude _build --exclude deps --exclude node_modules ~/bench-sealed/$rel "$NIGHT_STAGE/$(dirname $rel)/" || fail "stage_failed: rsync of sealed $rel failed"
done
zsh -lc "cd ~/bench/night-2026-10-01 && python3 tools/night_grade.py grading/$N-jobs.json grading/$N-results.jsonl" > $W/$N-grade.log 2>&1 || echo "rc=$?" >> $W/$N-grade.log
rm -rf "$NIGHT_STAGE"
cp "$G/$N-results.jsonl" "$W/$N-results.jsonl" || fail "stage_failed: result file not produced (grade log: $(tail -c 200 $W/$N-grade.log | tr '\n' ' '))"
