#!/bin/bash
# Lab C1 driver: runs a plan file (lines "<arm> <unit> <rep> <tag>") one unit at a time, skipping units
# that already have result.json; waits while a delivery Build runs on this host.
cfg=$1; plan=$2; runs=$3; H=$(cd "$(dirname "$0")" && pwd)
while read -r arm unit rep tag; do
  [ -z "$arm" ] && continue
  out="$runs/$tag/$unit-$arm-r$rep"
  [ -s "$out/result.json" ] && continue
  [ -e "$runs/STOP" ] && { echo "STOP file, ending"; exit 0; }
  while ps -u lanes -o args= | grep -E 'build-runtime\.py|hostbin/kbuild\.sh' | grep -vq grep; do
    echo "$(date -u +%FT%TZ) delivery Build running, waiting"; sleep 60; done
  python3 "$H/run.py" "$cfg" "$arm" "$unit" "$rep" "$out"
done < "$plan"
echo "$(date -u +%FT%TZ) plan done"
