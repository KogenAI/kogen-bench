#!/bin/bash
# Grade HC01 cells as they complete (same official route as tier 1): fetch patch.diff, drop harness-added
# .kogen/project.yaml and .setup-compile.log hunks (pre/post sha recorded), grade once via grade_cell.sh.
# Usage: grade_hc01.sh HOST EXPERIMENT:CELL_ID:TASK ...   Writes grades/hc01-grades.jsonl.
set -u
B=${BENCH_HOME}/Areas/Kogen/benchmark-recovery-2026-10-02
OUT=$B/levers/hc01-lane/grades; mkdir -p "$OUT"
H=$1; shift
for item in "$@"; do
  exp=${item%%:*}; rest=${item#*:}; cid=${rest%%:*}; task=${rest#*:}
  rd=/srv/bh/bench/results/$exp/$cid
  if grep -q "\"id\": \"$cid\"" "$OUT/hc01-grades.jsonl" 2>/dev/null; then echo "$cid already graded"; continue; fi
  until ssh -n kogen-bench-$H "test -f $rd/COMPLETE.json"; do sleep 60; done
  st=$(ssh -n kogen-bench-$H "python3 -c 'import json;print(json.load(open(\"$rd/manifest.json\"))[\"status\"])'")
  n=$(ssh -n kogen-bench-$H "ls -d $rd/attempt-* | wc -l")
  att=$rd/attempt-$n
  L=/tmp/claude-501/$cid/attempt-1; mkdir -p "$L"
  if ! scp -q kogen-bench-$H:$att/patch.diff "$L/raw.diff" 2>/dev/null || [ ! -s "$L/raw.diff" ]; then
    printf '{"id": "%s", "task": "%s", "host": "%s", "cell_status": "%s", "outcome": "no_patch", "pass_": false}\n' "$cid" "$task" "$H" "$st" >> "$OUT/hc01-grades.jsonl"
    echo "$cid no patch (status $st)"; continue
  fi
  python3 - "$L/raw.diff" "$L/patch.diff" <<'PY'
import re,sys
blocks=re.split(r'(?m)(?=^diff --git )',open(sys.argv[1]).read())
drop={'a/.kogen/project.yaml','b/.kogen/project.yaml'}
def keep(b):
    p=b.splitlines()[0].split()[2:] if b.startswith('diff --git ') else []
    return not (drop.intersection(p) or any(x.split('/')[-1]=='.setup-compile.log' for x in p))
open(sys.argv[2],'w').write(''.join(b for b in blocks if keep(b)))
PY
  pre=$(shasum -a 256 "$L/raw.diff" | cut -c1-64); post=$(shasum -a 256 "$L/patch.diff" | cut -c1-64)
  bash $B/probe-luna-low-20261002/grades/grade_cell.sh "$cid" "$task" "$L/patch.diff"; grc=$?
  python3 - "$B/probe-luna-low-20261002/grades/work/probe-$cid-results.jsonl" "$H" "$st" "$pre" "$post" "$grc" >> "$OUT/hc01-grades.jsonl" <<'PY'
import json,sys
f,h,st,pre,post,grc=sys.argv[1:7]
d=json.loads(open(f).readline())
keep={k:d.get(k) for k in ("id","task","grader","host","started","base","patch_sha256","pass_","outcome","kind","cause","tests_ran")}
keep.update(cell_host=h, cell_status=st, raw_patch_sha256=pre, filtered_patch_sha256=post, grade_cell_rc=int(grc))
print(json.dumps(keep))
PY
  echo "$cid graded: $(tail -1 "$OUT/hc01-grades.jsonl" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("outcome"),d.get("pass_"))')"
done
echo "HC01 GRADER DONE $H"
