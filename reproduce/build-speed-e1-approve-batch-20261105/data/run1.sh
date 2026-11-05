#!/bin/sh
# run1.sh <fixture> <slug> <arm A|B|C|BC> <rep>: one measured approve on a fresh clone of a frozen fixture.
# A/B: kbuild's two calls (preview -> digest -> approve). C/BC: one call with the digest from shape's package
# record (.kogen/local/packages/<slug>.json sha256); on a digest refusal it falls back to the two calls.
# A/C use release d98cfe01; B/BC the Lab build with batched bindingCollision. Model-free.
fx=$1; S=$2; arm=$3; rep=$4
E=$HOME/work.noindex/scratch/research/work/e1
# A run taken over by a separate stream (kip, 09:50Z) is skipped by the main scheduler unless FORCE=1.
[ -z "${FORCE:-}" ] && [ -e "$E/skip/$fx.$arm.$rep" ] && { echo "skip $fx $arm $rep"; exit 0; }
# 09:55Z: two streams share the light fixtures; each run is claimed once (atomic mkdir).
mkdir -p "$E/claim"; mkdir "$E/claim/$fx.$arm.$rep" 2>/dev/null || { echo "claimed $fx $arm $rep"; exit 0; }
RUN=$HOME/work.noindex/scratch/research/runs/e1-approve/$fx.$arm.$rep
case $arm in A|C) REL=$HOME/work.noindex/releases/kogen-d98cfe0;; B|BC) REL=$HOME/work.noindex/scratch/research/unpacked/e1-b;; esac
[ -e "$RUN" ] && mv "$RUN" "$RUN.aside-$(date +%s)"; mkdir -p "$RUN"
cp -c -R -p "$E/frozen/$fx" "$RUN/tree" || exit 3
KOGEN_RELEASE=$REL; export KOGEN_RELEASE
. $HOME/work.noindex/hostbin/kenv.sh >/dev/null 2>&1
KH=$HOME/kogen-home-personal-exec
cd "$RUN/tree" || exit 3
now() { python3 -c 'import time;print("%.3f"%time.time())'; }
uptime | sed 's/.*averages*: //' > "$RUN/load0"
kogen --version > "$RUN/version" 2>&1
t0=$(now); fb=0; H=; rc1=; t1=
two() {
  HOME=$KH kogen intent approve $S --project . > "$RUN/out1" 2>&1; rc1=$?; t1=$(now)
  H=$(grep -oE "[0-9a-f]{64}" "$RUN/out1" | tail -1)
  if [ -n "$H" ]; then HOME=$KH kogen intent approve $S $H --project . > "$RUN/out2" 2>&1; rc2=$?; else rc2=; fi
}
case $arm in
  A|B) two;;
  C|BC) REC=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["sha256"])' .kogen/local/packages/$S.json 2>/dev/null)
     echo "${REC:-none}" > "$RUN/shape-record-digest"
     # 09:30Z: shape's record is stale on trees shaped by 41d70052 and after kbuild's post-shape override, so C's
     # digest comes from the Lab helper (the release's own project.Hash of the Intent baseline; no checks run).
     H=$($E/labdigest "$RUN/tree" $S 2>/dev/null); echo labdigest > "$RUN/digest-source"
     if [ -n "$H" ]; then HOME=$KH kogen intent approve $S $H --project . > "$RUN/out2" 2>&1; rc2=$?
       if [ $rc2 != 0 ] && grep -qiE "does not match|mismatch|hash_mismatch" "$RUN/out2"; then mv "$RUN/out2" "$RUN/out-c-refused"; fb=1; two; fi
     else fb=1; two; fi;;
esac
t2=$(now)
cp .kogen/local/approvals/$S.json "$RUN/approval.json" 2>/dev/null
uptime | sed 's/.*averages*: //' > "$RUN/load1"
python3 - "$RUN" "$fx" "$S" "$arm" "$rep" "$t0" "${t1:-}" "$t2" "${rc1:-}" "${rc2:-}" "$fb" "${H:-}" <<'PY'
import json,sys,os
run,fx,S,arm,rep,t0,t1,t2,rc1,rc2,fb,H=sys.argv[1:]
def rd(n):
    p=os.path.join(run,n)
    return open(p,errors='replace').read() if os.path.exists(p) else None
r=dict(digest_source=(rd('digest-source') or 'shape-record' if arm in ('C','BC') else 'preview').strip(), shape_record_digest=(rd('shape-record-digest') or '').strip() or None, fixture=fx,slug=S,arm=arm,rep=int(rep),start=float(t0),wall_s=round(float(t2)-float(t0),3),
  call1_s=round(float(t1)-float(t0),3) if t1 else None, rc1=rc1 or None, rc2=rc2 or None, fallback=int(fb), digest=H or None,
  load0=rd('load0').strip(), load1=rd('load1').strip(), version=rd('version').strip())
open(os.path.join(run,'result.json'),'w').write(json.dumps(r)+'\n')
PY
cd "$RUN" && find "$RUN/tree" -mindepth 1 -delete && rmdir "$RUN/tree"
echo "done $fx $arm $rep"
