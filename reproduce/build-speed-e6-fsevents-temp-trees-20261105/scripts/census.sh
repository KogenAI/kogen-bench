#!/bin/sh
# Passive census window. Args: outdir watch_pid max_seconds. Runs as kogen-runner on mb. Never touches delivery files.
out=$1; wpid=$2; max=$3
R=$HOME/work.noindex/scratch/delivery/t1105
W=$HOME/work.noindex/scratch/research/work/e6
mkdir -p "$out"; : > "$out/marker"
echo "start $(date -u +%FT%TZ) watch_pid=$wpid max=$max" > "$out/window.txt"
$W/fswatch "$out/events-d1.tsv" 1 "$R" /private/tmp /private/var/folders &
echo $! > "$out/fswatch1.pid"
$W/fswatch "$out/events-d2.tsv" 2 "$R" &
echo $! > "$out/fswatch2.pid"
fpid=$(pgrep -x fseventsd | head -1)
echo "fseventsd_pid=$fpid" >> "$out/window.txt"
echo "ts	load1	load5	fseventsd_cputime	fseventsd_pcpu" > "$out/sample.tsv"
t0=$(date +%s)
while :; do
  now=$(date +%s)
  l=$(sysctl -n vm.loadavg | tr -d '{}')
  p=$(ps -o time=,pcpu= -p "$fpid" | tr -s ' ' '\t')
  printf '%s\t%s\t%s\t%s\n' "$(date -u +%T)" "$(echo $l | awk '{print $1}')" "$(echo $l | awk '{print $2}')" "$p" >> "$out/sample.tsv"
  kill -0 "$wpid" 2>/dev/null || { echo "build_exit_seen $(date -u +%FT%TZ)" >> "$out/window.txt"; break; }
  [ $((now - t0)) -ge "$max" ] && { echo "max_reached $(date -u +%FT%TZ)" >> "$out/window.txt"; break; }
  sleep 5
done
kill -TERM $(cat "$out/fswatch1.pid") $(cat "$out/fswatch2.pid") 2>/dev/null
sleep 2
echo "end $(date -u +%FT%TZ)" >> "$out/window.txt"
# survivors: files newer than the marker, per normalised top-level prefix
find "$R" -mindepth 2 -type f -newer "$out/marker" 2>/dev/null | sed -E "s#^$R/##; s#/.*##; s/[-.]?[A-Za-z0-9]{6}\$//; s/[0-9]+\$//" | sort | uniq -c | sort -rn > "$out/survivors.txt"
echo "done $(date -u +%FT%TZ)" >> "$out/window.txt"
