#!/bin/sh
# A/D sequence, one run at a time. Args: outdir gate-deadline-epoch-for-first-run. Each later run waits at most 20 min.
OUT=$1; W=$HOME/work.noindex/scratch/research/work/e6d
mkdir -p "$OUT"; echo $$ > "$OUT/seq.pid"
GATE_DEADLINE=$2; export GATE_DEADLINE
r() { echo "$(date -u +%T) start $1 $2 watch=$3" >> "$OUT/seq.log"; sh $W/abrun2.sh $1 $2 "$OUT" $3 >> "$OUT/seq.log" 2>&1; rc=$?; echo "$(date -u +%T) end $1 $2 rc=$rc" >> "$OUT/seq.log"
  [ $rc = 3 ] && { echo "$(date -u +%T) SEQ-STOPPED gate" >> "$OUT/seq.log"; exit 3; }
  GATE_DEADLINE=$(( $(date +%s) + 1200 )); export GATE_DEADLINE; }
r A w0 1; r D w0 1
i=1
for o in "A D" "D A" "A D" "D A" "A D" "D A" "A D" "D A"; do
  for a in $o; do r $a u$i 0; done; i=$((i+1))
done
i=1
for o in "A D" "D A" "A D"; do
  for a in $o; do r $a w$i 1; done; i=$((i+1))
done
echo "$(date -u +%T) SEQ-DONE" >> "$OUT/seq.log"
