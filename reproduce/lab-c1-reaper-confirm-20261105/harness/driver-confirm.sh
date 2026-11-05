#!/bin/bash
# Lab C1 confirmation driver (lm, as lanes). Runs a plan ("<arm> <unit> <rep> <tag>" lines) one unit at a time, skipping units that already have result.json.
# Before every run: waits (never kills) while a delivery process (build-runtime.py, hostbin/kbuild.sh, kogen intent) is on the host, and logs each one with its start time.
# During every run: a watcher records Build processes that appear; such a run is set aside (runs/intruded/) and repeated, up to 2 repeats.
cfg=$1; plan=$2; runs=$3; H=$(cd "$(dirname "$0")" && pwd)
LOG=$runs/INTRUSIONS.log; SEEN=$runs/.intr-seen; touch "$SEEN"
PRE='build-runtime\.py|hostbin/kbuild\.sh|kogen intent'
DUR='build-runtime\.py|hostbin/kbuild\.sh'
scan() { ps -eo user:12,pid,lstart,args | grep -E "$1" | grep -v -E 'grep|driver-confirm|launch-confirm' | cut -c1-300; }
note() { # note <phase> <ps lines on stdin>
  while IFS= read -r l; do [ -z "$l" ] && continue; k=$(echo "$l" | awk '{print $2}')_$(echo "$l" | awk "{print \$3\$4\$5\$6\$7}")
    grep -qxF "$k" "$SEEN" || { echo "$k" >> "$SEEN"; echo "$(date -u +%FT%TZ) $1 :: $l" >> "$LOG"; }; done; }
while read -r arm unit rep tag; do
  [ -z "$arm" ] && continue
  out="$runs/$tag/$unit-$arm-r$rep"
  [ -s "$out/result.json" ] && continue
  attempt=0
  while :; do
    [ -e "$runs/STOP" ] && { echo "$(date -u +%FT%TZ) STOP file, ending"; exit 0; }
    while [ -n "$(scan "$PRE")" ]; do
      scan "$PRE" | note "PAUSE-before-$tag/$unit-$arm-r$rep"; echo "$(date -u +%FT%TZ) delivery process on host, pausing before $unit-$arm-r$rep"; sleep 30; done
    intr="$runs/.during-$unit-$arm-r$rep"; : > "$intr"
    ( while :; do scan "$DUR" >> "$intr"; sleep 5; done ) & w=$!
    python3 "$H/run.py" "$cfg" "$arm" "$unit" "$rep" "$out"
    kill $w 2>/dev/null; wait $w 2>/dev/null
    if [ -s "$intr" ]; then
      sort -u "$intr" | note "DURING-$tag/$unit-$arm-r$rep"
      if [ $attempt -lt 2 ]; then attempt=$((attempt+1)); mkdir -p "$runs/intruded"
        mv "$out" "$runs/intruded/$tag-$unit-$arm-r$rep-a$attempt"
        echo "$(date -u +%FT%TZ) $tag/$unit-$arm-r$rep: delivery Build appeared during the run; set aside as intruded a$attempt, repeating" | tee -a "$LOG"; continue
      else echo "$(date -u +%FT%TZ) $tag/$unit-$arm-r$rep: intruded again after 2 repeats; kept, flagged" | tee -a "$LOG"; touch "$out/INTRUDED"; fi
    fi
    break
  done
  rm -f "$intr"
done < "$plan"
echo "$(date -u +%FT%TZ) plan done"
