#!/bin/bash
# Count-only HC01 rerun through the same Studio private grader and staging route.
set -uo pipefail
if [ "$#" -lt 2 ]; then
  echo "usage: grade_cell_counts.sh CELL_ID TASK_ID FILTERED_PATCH" >&2
  exit 2
fi
C="$1"; T="$2"; P=""
if [ "$#" -ge 3 ]; then P="$3"; fi
ROOT=${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02
W="$ROOT/probe-luna-low-20261002/grades/work"
S=grading-mac
N="counts-$C"
STAGE_N="probe-$C"
G=bench/hc01-grade-counts/work
OUT="$W/counts-$C-results.jsonl"
SAFE_TMP="$W/$N-safe.jsonl"
ENVS="export BENCH_ROOT=\$HOME/bench BENCH_TASKS=\$HOME/bench/tasks NIGHT_STAGE=\$HOME/bench/.concurrent-grader/night-stage-$STAGE_N"
NIGHT_ORIGINAL_SHA=4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0
NIGHT_COUNTS_SHA=07570bdba47c539ac24e2002e867cd2555251bae5b693c9aeebaaa0d8be2b940
GRADE_CELL_ORIGINAL_SHA=52563c104e42de3076d0f95a6461fe32d9acb79836cde0db023cb8d41be48efe
COUNT_TESTS_SHA=9e74d7bd4dee64bfa07d2758c9e742cb6509318300d20432615a78ead84920f0

mkdir -p "$W"
rm -f "$SAFE_TMP"
if [ -e "$OUT" ]; then
  echo "grade_cell_counts.sh $C: count result already exists; preserving it" >&2
  exit 4
fi

write_infra_row() {
  python3 - "$C" "$T" "$0" <<'PY' > "$OUT"
import hashlib,json,sys,time
c,t,script=sys.argv[1:4]
unavailable={"tests_total":None,"failures":None,"invalid":None,"skipped":None,"excluded":None,"tests_passed":None,"status":"count unavailable"}
shas={"night_grade_original":"4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0","night_grade_counts":"07570bdba47c539ac24e2002e867cd2555251bae5b693c9aeebaaa0d8be2b940","grade_cell_original":"52563c104e42de3076d0f95a6461fe32d9acb79836cde0db023cb8d41be48efe","grade_cell_counts":hashlib.sha256(open(script,"rb").read()).hexdigest(),"count_tests":"9e74d7bd4dee64bfa07d2758c9e742cb6509318300d20432615a78ead84920f0"}
print(json.dumps({"id":c,"task":t,"outcome":"grader_error","pass_":False,"counts":unavailable,"grader_shas":shas,"started":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())},sort_keys=True))
PY
}

fail() {
  echo "grade_cell_counts.sh $C: $1" >&2
  write_infra_row
  ssh -n "$S" "rm -rf ~/bench/.concurrent-grader/night-stage-$STAGE_N" >/dev/null 2>&1 || true
  exit 3
}

if [ -z "$P" ] || [ ! -f "$P" ]; then fail "filtered patch is missing"; fi
EXPECTED_SHA=$(python3 - "$C" "$ROOT" <<'PY'
import sys
from pathlib import Path
root=Path(sys.argv[2])
sys.path.insert(0,str(root/"levers/lib"))
from safe_rows import load_rows,sanitize
rows=[sanitize(r) for r in load_rows(str(root/"levers/hc01-lane/grades/hc01-grades.jsonl"))]
matches=[r.get("filtered_patch_sha256") for r in rows if r.get("id")==sys.argv[1]]
if len(matches)!=1 or not matches[0]: raise SystemExit(2)
print(matches[0])
PY
) || fail "no unique official filtered-patch hash"
ACTUAL_SHA=$(shasum -a 256 "$P" | awk '{print $1}') || fail "could not hash filtered patch"
if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then fail "filtered patch SHA does not match the official grade"; fi

python3 - "$C" "$T" "$G" > "$W/$N-jobs.json" <<'PY' || fail "could not write jobs file"
import json,sys
c,t,g=sys.argv[1:4]
print(json.dumps([{"id":c,"task":t,"patch":"${BENCH_HOME}/bench/hc01-grade-counts/work/patches/"+c+".diff","control":"candidate"}]))
PY
ssh -n "$S" "mkdir -p $G/patches" || fail "could not create external Studio patch directory"
scp -q "$P" "$S:$G/patches/$C.diff" || fail "could not stage filtered patch"
scp -q "$W/$N-jobs.json" "$S:$G/$N-jobs.json" || fail "could not stage count job file"
RELS=$(ssh -n "$S" "zsh -lc '$ENVS; cd ~/bench/night-2026-10-01 && python3 tools/night_grade.py --rels $T'") || fail "could not list the route's staged rels"
ssh -n "$S" "mkdir -p ~/bench/.concurrent-grader/night-stage-$STAGE_N && chmod 700 ~/bench/.concurrent-grader ~/bench/.concurrent-grader/night-stage-$STAGE_N" || fail "could not create private staging directory"
RELLIST=$(python3 -c "import json,sys;print(' '.join(sorted({r for v in json.loads(sys.argv[1]).values() for r in v})))" "$RELS") || fail "could not parse staged rels"
for rel in $RELLIST; do
  ssh -n "$S" "mkdir -p ~/bench/.concurrent-grader/night-stage-$STAGE_N/$(dirname "$rel")" || fail "could not create staged rel directory"
  rsync -a --exclude _build --exclude deps --exclude node_modules ~/bench-sealed/$rel "$S:bench/.concurrent-grader/night-stage-$STAGE_N/$(dirname "$rel")/" || fail "could not stage the route's private rels"
done
ssh -n "$S" "zsh -lc '$ENVS; cd ~/bench/night-2026-10-01 && ~/bench/hc01-grade-counts/run_counts.sh ~/bench/hc01-grade-counts/work/$N-jobs.json ~/bench/hc01-grade-counts/work/$N-results.fifo ~/bench/hc01-grade-counts/work/$N-safe.jsonl'" > "$W/$N-grade.log" 2>&1 || fail "instrumented Studio grade route failed"
ssh -n "$S" "rm -rf ~/bench/.concurrent-grader/night-stage-$STAGE_N" >/dev/null 2>&1 || true
scp -q "$S:bench/hc01-grade-counts/work/$N-safe.jsonl" "$SAFE_TMP" || fail "sanitized grade result could not be retrieved"
ssh -n "$S" "rm -f ~/bench/hc01-grade-counts/work/$N-jobs.json ~/bench/hc01-grade-counts/work/$N-safe.jsonl ~/bench/hc01-grade-counts/work/patches/$C.diff" >/dev/null 2>&1 || true

python3 - "$SAFE_TMP" "$OUT" "$0" <<'PY' || fail "sanitized grade result could not be recorded"
import hashlib,json,sys
from pathlib import Path
root=Path("${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02")
sys.path.insert(0,str(root/"levers/lib"))
from safe_rows import load_rows,sanitize
rows=load_rows(sys.argv[1])
if len(rows)!=1: raise SystemExit(2)
row=sanitize(rows[0])
keep={k:row[k] for k in ("id","task","outcome","pass_","counts","started") if k in row}
if not isinstance(keep.get("counts"),dict):
    keep["counts"]={"tests_total":None,"failures":None,"invalid":None,"skipped":None,"excluded":None,"tests_passed":None,"status":"count unavailable"}
keep["grader_shas"]={"night_grade_original":"4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0","night_grade_counts":"07570bdba47c539ac24e2002e867cd2555251bae5b693c9aeebaaa0d8be2b940","grade_cell_original":"52563c104e42de3076d0f95a6461fe32d9acb79836cde0db023cb8d41be48efe","grade_cell_counts":hashlib.sha256(Path(sys.argv[3]).read_bytes()).hexdigest(),"count_tests":"9e74d7bd4dee64bfa07d2758c9e742cb6509318300d20432615a78ead84920f0"}
tmp=Path(sys.argv[2]+".tmp")
tmp.write_text(json.dumps(keep,sort_keys=True)+"\n")
tmp.replace(sys.argv[2])
PY
rm -f "$SAFE_TMP"
echo "count result written: $OUT"
