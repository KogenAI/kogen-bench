#!/bin/bash
# orch2.sh [first-n last-n]   (EU, as lanes, detached; one run at a time). Same gate and pin runs as orch.sh full, but the base
# comparison is targeted: after a red pin run, only the tests that failed on the pin and are not yet known for that kogen main are
# run on the unpinned base (`go test -run`), cached per kogen main. A red before the test stage gets one base run up to go vet.
set -u
P=${LAB_ROOT:-$HOME/work.noindex/scratch/research/work/prelanding}
lo=${1:-1}; hi=${2:-48}
export MIRRORS=$P/mirrors LAB_TMP=$P
echo $$ > "$P/orch2.pid"
log() { echo "$(date -u +%FT%TZ) $*" >> "$P/orch-full.log"; }
gate() { # one suite per host: no host lock, no other research suite, load1 < 4 (delivery's suites queue on heavy.sh)
  local w=0 other ld
  while :; do
    [ -e "$P/STOP" ] && return 1
    other=$(ps -eo args | grep -E 'scratch/research/(work|runs|unpacked)/' | grep -v -E 'prelanding|grep|ps -eo' | wc -l)
    ld=$(cut -d' ' -f1 /proc/loadavg)
    if [ ! -e /run/kogen-host-lock ] && [ "$other" -eq 0 ] && [ "$(echo "$ld < 4" | bc)" = 1 ]; then return 0; fi
    [ $((w % 300)) = 0 ] && log "waiting: host-lock=$([ -e /run/kogen-host-lock ] && echo yes || echo no) other-research-procs=$other load1=$ld"
    sleep 30; w=$((w+30))
  done; }
need() { # need <kogen12> <pin result.json> <out ids file>: failing pin ids with no base fact yet; prints the count
  python3 - "$1" "$2" "$3" "$P/runs" <<'EOP'
import glob, json, os, sys
m12, pinres, outf, runs = sys.argv[1:]
pin = json.load(open(pinres)); known = {}
full = runs + "/base-" + m12 + "/result.json"
if os.path.exists(full):
    f = json.load(open(full)); known = {"*": set(f["failed_ids"])}
for g in glob.glob(runs + "/basetests-" + m12 + "-*/result.json"):
    for k, v in json.load(open(g)).get("tested", {}).items(): known[k] = v
missing = [i for i in pin["failed_ids"] if i not in known and "*" not in known]
open(outf, "w").write("\n".join(missing) + ("\n" if missing else ""))
print(len(missing))
EOP
}
while IFS=$'\t' read -r n role repo sha kbase; do
  [ "$n" -ge "$lo" ] && [ "$n" -le "$hi" ] || continue
  [ -e "$P/STOP" ] && { log "STOP file: ending"; break; }
  od=$P/runs/pin-$n; m12=${kbase:0:12}
  if [ -s "$od/result.json" ]; then log "n=$n pin done already"; else
    gate || { log "STOP file: ending"; break; }
    log "n=$n $role $repo ${sha:0:7} base ${kbase:0:8} start load=$(cut -d' ' -f1 /proc/loadavg)"
    bash "$P/bin/prelanding-check.sh" "$repo" "$sha" "$kbase" "$od" pin >> "$P/orch-full.log" 2>&1
    log "n=$n status=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["status"])' "$od/result.json" 2>/dev/null || echo none)"
  fi
  st=$(python3 -c 'import json,sys;r=json.load(open(sys.argv[1]));print(r["status"]+"|"+r["detail"][:10])' "$od/result.json" 2>/dev/null || echo none)
  case $st in
    red\|go\ test*)
      c=$(need "$m12" "$od/result.json" "$od/base-ids.txt")
      if [ "$c" != 0 ]; then gate || break; log "n=$n base tests on $m12: $c ids"
        bash "$P/bin/prelanding-check.sh" "$repo" "$sha" "$kbase" "$P/runs/basetests-$m12-$n" basetests "$od/base-ids.txt" >> "$P/orch-full.log" 2>&1; fi ;;
    red\|*)
      if [ ! -s "$P/runs/basevet-$m12/result.json" ] && [ ! -s "$P/runs/base-$m12/result.json" ]; then gate || break; log "n=$n base to go vet on $m12"
        STOP_AFTER=vet bash "$P/bin/prelanding-check.sh" "$repo" "$sha" "$kbase" "$P/runs/basevet-$m12" base >> "$P/orch-full.log" 2>&1; fi ;;
  esac
done < "$P/runlist.tsv"
log "end (orch2)"
