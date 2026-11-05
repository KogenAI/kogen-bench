#!/bin/sh
# One measured run of the census-top test on mb, as kogen-runner. Args: arm(A|D) tag outdir watch(0|1)
#   go test -run '^TestAssemblyUsesThePinnedComponents$' in the arm's scratch clone (kA = unmodified, kD = A + assembly_test.go single-member extract).
# Gate: load5 <= 24 (2 x 12 cores, the delivery launch gate), no Build verify/landing process, heavy-lock queue empty; waits up to 20 min, else rc 3.
arm=$1; tag=$2; OUT=$3; watch=$4
W=$HOME/work.noindex/scratch/research/work/e6d
TD=$HOME/work.noindex/scratch/research/tmp-20261105/d-$arm-$tag
mkdir -p "$OUT"
gate() {
  l5=$(sysctl -n vm.loadavg | tr -d '{}' | awk '{print $2}')
  v=$(pgrep -f 'verify\.test|kogen-verify|verify-land|landtree-|kogen intent verify' | head -1)
  q=$(ls /var/tmp/kogen-heavy.lock.q 2>/dev/null | head -1)
  pq=$(ls $W/hold 2>/dev/null | head -1)
  awk -v l="$l5" 'BEGIN{exit !(l <= 24)}' && [ -z "$v" ] && [ -z "$q" ] && [ -z "$pq" ]
}
until gate; do [ "$(date +%s)" -gt "${GATE_DEADLINE:?}" ] && { l5=$(sysctl -n vm.loadavg | tr -d "{}" | awk "{print \$2}"); echo "gate timeout load5=$l5 verify=$(pgrep -f 'verify\.test|kogen-verify|verify-land|landtree-|kogen intent verify' | head -3 | tr '\n' ' ') queue=$(ls /var/tmp/kogen-heavy.lock.q 2>/dev/null | head -1)" > "$OUT/$arm$tag.gate"; exit 3; }; sleep 10; done
mkdir -p "$TD/go"
. $HOME/work.noindex/hostbin/kenv.sh >/dev/null 2>&1
export PATH="$PATH:/usr/sbin:/sbin" TMPDIR="$TD/" GOTMPDIR="$TD/go"
cd "$W/k$arm/cli" || exit 4
fw=
[ "$watch" = 1 ] && { $W/fswatch "$OUT/$arm$tag.events.tsv" 4 "$TD" & fw=$!; }
fpid=$(pgrep -x fseventsd | head -1)
c0=$(ps -o time= -p $fpid | tr -d ' ')
l0=$(sysctl -n vm.loadavg | tr -d '{}' | awk '{print $2}')
t0=$(python3 -c 'import time;print(time.time())')
s0=$(date -u +%T)
go test -count=3 -v -run '^TestAssemblyUsesThePinnedComponents$' . > "$OUT/$arm$tag.gotest.txt" 2>&1
rc=$?
t1=$(python3 -c 'import time;print(time.time())')
c1=$(ps -o time= -p $fpid | tr -d ' ')
l1=$(sysctl -n vm.loadavg | tr -d '{}' | awk '{print $2}')
[ -n "$fw" ] && { sleep 1; kill -TERM $fw; wait $fw 2>/dev/null; }
left=$(find "$TD" -type f 2>/dev/null | wc -l | tr -d ' ')
verdict=$(grep -E '^(--- (PASS|FAIL)|ok|FAIL|PASS)' "$OUT/$arm$tag.gotest.txt" | tr '\n' ';' | cut -c1-300)
python3 -I - "$t0" "$t1" "$c0" "$c1" "$l0" "$l1" "$s0" "$rc" "$left" "$arm" "$tag" "$OUT" "$watch" "$verdict" <<'PY'
import sys, json, os
t0,t1,c0,c1,l0,l1,s0,rc,left,arm,tag,out,watch,verdict = sys.argv[1:]
def secs(s):
    m, r = s.split(':'); return int(m) * 60 + float(r)
rec = dict(arm=arm, tag=tag, start=s0, rc=int(rc), wall=round(float(t1) - float(t0), 2), fseventsd_cpu_s=round(secs(c1) - secs(c0), 2),
           load5_start=float(l0), load5_end=float(l1), survivors_after=int(left), watched=watch == '1', verdict=verdict)
if watch == '1':
    ev = [l.rstrip('\n').split('\t') for l in open('%s/%s%s.events.tsv' % (out, arm, tag))][1:]
    rec['files_created_events'] = sum(int(r[1]) for r in ev if r[0] != '#TOTAL')
    rec['file_events_total'] = sum(int(r[5]) for r in ev if r[0] != '#TOTAL')
open('%s/%s%s.metrics.json' % (out, arm, tag), 'w').write(json.dumps(rec))
print(json.dumps(rec))
PY
find "$TD" -mindepth 1 -delete 2>/dev/null; rmdir "$TD" 2>/dev/null
