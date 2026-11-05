#!/bin/bash
# chunks.sh <cond> <rounds> <chunk> <outdir> <dirA> <dirB> : interleaved A/B chunks of the wall-time test; load5 recorded at each chunk start.
set -u
cond=$1; rounds=$2; chunk=$3; out=$4; dirA=$5; dirB=$6
mkdir -p "$out"
echo $$ > "$out/orch.pid"
load5() { if [ -r /proc/loadavg ]; then awk '{print $2}' /proc/loadavg; else sysctl -n vm.loadavg | awk '{print $3}'; fi; }
load1() { if [ -r /proc/loadavg ]; then awk '{print $1}' /proc/loadavg; else sysctl -n vm.loadavg | awk '{print $2}'; fi; }
for r in $(seq 1 "$rounds"); do
  if [ $((r % 2)) -eq 1 ]; then order="A B"; else order="B A"; fi
  for arm in $order; do
    if [ "$arm" = A ]; then d=$dirA; else d=$dirB; fi
    l5=$(load5); l1=$(load1); t0=$(date -u +%FT%TZ)
    ( cd "$d" && go test -json -run '^TestWallTimeDeadlineAndNeverStarted$' -count="$chunk" ./verify ) > "$out/$cond-r$r-$arm.json" 2> "$out/$cond-r$r-$arm.err"
    rc=$?
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$cond" "$r" "$arm" "$t0" "$l5" "$l1" "$rc" >> "$out/chunks.tsv"
  done
done
echo done > "$out/DONE"
