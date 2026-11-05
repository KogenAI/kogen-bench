#!/bin/bash
# orch_tuple.sh <n>...   (TUPPFX=tupleNL: the tuple without the vendored loop) DIAGNOSTIC arm B-tuple: TUPLE=tuples/tuple-<n>.txt pin runs into runs/tuple-<n>; targeted base tests as in orch2.sh
set -u
P=${LAB_ROOT:-$HOME/work.noindex/scratch/research/work/prelanding}
export MIRRORS=$P/mirrors LAB_TMP=$P
echo $$ > "$P/orch_tuple.pid"
log() { echo "$(date -u +%FT%TZ) $*" >> "$P/orch-full.log"; }
gate() { local w=0 other ld
  while :; do
    [ -e "$P/STOP" ] && return 1
    [ "$(date -u +%H%M)" -ge "${DEADLINE:-2400}" ] && { log "TUPLE deadline reached"; return 1; }
    other=$(ps -eo args | grep -E 'scratch/research/(work|runs|unpacked)/' | grep -v -E 'prelanding|grep|ps -eo' | wc -l); ld=$(cut -d' ' -f1 /proc/loadavg)
    if [ ! -e /run/kogen-host-lock ] && [ "$other" -eq 0 ] && [ "$(echo "$ld < 4" | bc)" = 1 ]; then return 0; fi
    [ $((w % 300)) = 0 ] && log "TUPLE waiting: other-research-procs=$other load1=$ld"; sleep 30; w=$((w+30))
  done; }
for want in "$@"; do
  row=$(awk -F'\t' -v n="$want" '$1==n' "$P/runlist.tsv"); IFS=$'\t' read -r n role repo sha kbase <<<"$row"; m12=${kbase:0:12}; od=$P/runs/${TUPPFX:-tuple}-$n
  [ -s "$od/result.json" ] && continue
  gate || break
  log "TUPLE n=$n $role $repo ${sha:0:7} base ${kbase:0:8} start load=$(cut -d' ' -f1 /proc/loadavg)"
  TUPLE=$P/tuples/${TUPPFX:-tuple}-$n.txt bash "$P/bin/prelanding-check.sh" "$repo" "$sha" "$kbase" "$od" pin >> "$P/orch-full.log" 2>&1
  python3 - "$m12" "$od/result.json" "$od/base-ids.txt" "$P/runs" <<'EOP' > "$od/need.count"
import glob, json, os, sys
m12, pinres, outf, runs = sys.argv[1:]
pin = json.load(open(pinres)); known = {}
if os.path.exists(runs + "/base-" + m12 + "/result.json"): known = {"*": 1}
for g in glob.glob(runs + "/basetests-" + m12 + "-*/result.json"):
    for k, v in json.load(open(g)).get("tested", {}).items(): known[k] = v
missing = [i for i in pin["failed_ids"] if i not in known and "*" not in known]
open(outf, "w").write("\n".join(missing) + ("\n" if missing else "")); print(len(missing))
EOP
  if [ "$(cat "$od/need.count")" != 0 ]; then gate || break; log "TUPLE n=$n base tests on $m12"; bash "$P/bin/prelanding-check.sh" "$repo" "$sha" "$kbase" "$P/runs/basetests-$m12-T$n" basetests "$od/base-ids.txt" >> "$P/orch-full.log" 2>&1; fi
done
log "TUPLE end"
