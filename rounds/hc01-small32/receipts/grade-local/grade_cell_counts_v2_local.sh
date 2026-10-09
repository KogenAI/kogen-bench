#!/bin/bash
# grade_cell_counts_v2_local.sh CELL_ID TASK FILTERED_PATCH [PREFIX] [RAW_TAG]
# HC01 AMENDMENT-6: the AMENDMENT-4 count route (night_grade_counts_v2.py fc5d6884, run_counts_v2.sh 1296046f, filter_stream.py 7ddb4967,
# safe_rows.py 28579898; same shas as the Studio copies) run on this MacBook from ~/bench/hc01-grade-counts, with BENCH_TASKS =
# ~/bench/hc01-grade-tasks (see grade_cell_local.sh). The full runner output is still written once (0600) to a 0700 local stage and piped
# to the US root-only store, then removed locally only after the US sha equals the local sha. PREFIX (default counts2-) names the work
# files; RAW_TAG (default empty) is inserted into the US store filename so parity runs never collide with the official count file.
set -uo pipefail
C="$1"; T="$2"; P="${3:-}"; PFX="${4:-counts2-}"; TAG="${5:-}"
ROOT=${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02
W="$ROOT/probe-luna-low-20261002/grades/work"; N="$PFX$C"; STAGE_N="probe-$C-$PFX"
H=$HOME/bench/hc01-grade-counts; G=$H/work; RAW_STAGE=$H/v2/raw-stage
US_ROOT=${BENCH_ADMIN}@${BENCH_HOST_IP}; US_KEY=$HOME/.ssh/bench_orchestrator_ed25519; US_RAW=/var/lib/kogen-bench-private/hc01-raw
OUT="$W/$N-results.jsonl"; SAFE_TMP="$W/$N-safe.jsonl"
export BENCH_ROOT=$HOME/bench BENCH_TASKS=$HOME/bench/hc01-grade-tasks NIGHT_STAGE=$HOME/bench/.concurrent-grader/night-stage-$STAGE_N HC01_RAW_STAGE=$RAW_STAGE
NG_SHA=fc5d6884978f19a9c16972c05f33c59bb96246f38b0b6a5d782ac38881814942
mkdir -p "$W"; rm -f "$SAFE_TMP"
[ -e "$OUT" ] && { echo "grade_cell_counts_v2_local.sh $C: count result already exists; preserving it" >&2; exit 4; }
write_infra_row() {
  python3 - "$C" "$T" "$1" > "$OUT" <<'PY'
import json,sys,time
c,t,m=sys.argv[1:4]
u={"tests_total":None,"failures":None,"tests_passed":None,"status":"count unavailable"}
print(json.dumps({"id":c,"task":t,"outcome":"grader_error","pass_":False,"cause":m,"counts":u,"route":"macbook-local","started":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())},sort_keys=True))
PY
}
fail() { echo "grade_cell_counts_v2_local.sh $C: $1" >&2; write_infra_row "$1"; rm -rf "$NIGHT_STAGE"; exit 3; }
[ -n "$P" ] && [ -f "$P" ] || fail "filtered patch is missing"
EXPECTED_SHA=$(python3 - "$C" "$ROOT" <<'PY'
import sys
from pathlib import Path
root=Path(sys.argv[2]); sys.path.insert(0,str(root/"levers/lib"))
from safe_rows import load_rows,sanitize
rows=[sanitize(r) for r in load_rows(str(root/"levers/hc01-lane/grades/hc01-grades.jsonl"))]
m=[r.get("filtered_patch_sha256") for r in rows if r.get("id")==sys.argv[1]]
if len(m)!=1 or not m[0]: raise SystemExit(2)
print(m[0])
PY
) || fail "no unique official filtered-patch hash"
[ "$(shasum -a 256 "$P" | awk '{print $1}')" = "$EXPECTED_SHA" ] || fail "filtered patch SHA does not match the official grade"
mkdir -p "$G/patches" && mkdir -p -m 700 "$RAW_STAGE" && chmod 700 "$RAW_STAGE" && rm -f "$RAW_STAGE/$C.out" || fail "could not create local work/raw-stage directories"
python3 - "$C" "$T" "$G" > "$G/$N-jobs.json" <<'PY' || fail "could not write jobs file"
import json,sys
c,t,g=sys.argv[1:4]
print(json.dumps([{"id":c,"task":t,"patch":g+"/patches/"+c+".diff","control":"candidate"}]))
PY
cp "$P" "$G/patches/$C.diff" || fail "could not stage filtered patch"
RELS=$(zsh -lc "cd ~/bench/night-2026-10-01 && python3 tools/night_grade.py --rels $T") || fail "could not list the route's staged rels"
mkdir -p "$NIGHT_STAGE" && chmod 700 "$HOME/bench/.concurrent-grader" "$NIGHT_STAGE" || fail "could not create private staging directory"
RELLIST=$(python3 -c "import json,sys;print(' '.join(sorted({r for v in json.loads(sys.argv[1]).values() for r in v})))" "$RELS") || fail "could not parse staged rels"
for rel in $RELLIST; do
  mkdir -p "$NIGHT_STAGE/$(dirname "$rel")" || fail "could not create staged rel directory"
  rsync -a --exclude _build --exclude deps --exclude node_modules ~/bench-sealed/$rel "$NIGHT_STAGE/$(dirname "$rel")/" || fail "could not stage the route's private rels"
done
zsh -lc "cd ~/bench/night-2026-10-01 && $H/v2/run_counts_v2.sh $G/$N-jobs.json $G/$N-results.fifo $G/$N-safe.jsonl" > "$W/$N-grade.log" 2>&1 || fail "instrumented local grade route failed"
rm -rf "$NIGHT_STAGE"
cp "$G/$N-safe.jsonl" "$SAFE_TMP" || fail "sanitized grade result missing"
rm -f "$G/$N-jobs.json" "$G/$N-safe.jsonl" "$G/patches/$C.diff"
RAW_SHA_REMOTE=""
if [ -f "$RAW_STAGE/$C.out" ]; then
  DEST="$US_RAW/$C${TAG}.out"
  RAW_SHA_REMOTE=$(ssh -i "$US_KEY" -o BatchMode=yes "$US_ROOT" "umask 077; test ! -e $DEST && cat > $DEST && chmod 600 $DEST && sha256sum $DEST | cut -c1-64" < "$RAW_STAGE/$C.out") || RAW_SHA_REMOTE=""
  RAW_SHA_LOCAL=$(shasum -a 256 "$RAW_STAGE/$C.out" | cut -c1-64)
  if [ -n "$RAW_SHA_REMOTE" ] && [ "$RAW_SHA_REMOTE" = "$RAW_SHA_LOCAL" ]; then rm -f "$RAW_STAGE/$C.out"
  else echo "grade_cell_counts_v2_local.sh $C: raw transfer unverified; local stage copy kept (0600)" >&2; RAW_SHA_REMOTE=""; fi
fi
python3 - "$SAFE_TMP" "$OUT" "$0" "$RAW_SHA_REMOTE" "$NG_SHA" <<'PY' || fail "sanitized grade result could not be recorded"
import hashlib,json,sys
from pathlib import Path
root=Path("${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02"); sys.path.insert(0,str(root/"levers/lib"))
from safe_rows import load_rows,sanitize
rows=load_rows(sys.argv[1])
if len(rows)!=1: raise SystemExit(2)
row=sanitize(rows[0]); keep={k:row[k] for k in ("id","task","outcome","pass_","counts","started") if k in row}
if not isinstance(keep.get("counts"),dict): keep["counts"]={"tests_total":None,"failures":None,"tests_passed":None,"status":"count unavailable"}
c=keep["counts"]; c["raw_store_sha256"]=sys.argv[4] or None; c["raw_store_verified"]=bool(sys.argv[4]) and sys.argv[4]==c.get("raw_output_sha256")
keep["route"]="macbook-local"
keep["grader_shas"]={"night_grade_original":"4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0","night_grade_counts_v2":sys.argv[5],"grade_cell_counts_v2_local":hashlib.sha256(Path(sys.argv[3]).read_bytes()).hexdigest()}
tmp=Path(sys.argv[2]+".tmp"); tmp.write_text(json.dumps(keep,sort_keys=True)+"\n"); tmp.replace(sys.argv[2])
PY
rm -f "$SAFE_TMP"
echo "count result written: $OUT"
