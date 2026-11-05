#!/bin/sh
# Sequence of A/B/C runs; one at a time. Arg: outdir. Logs to $OUT/seq.log. Rotation so each arm sees each position.
OUT=$1; W=$HOME/work.noindex/scratch/research/work/e6
mkdir -p "$OUT"; echo $$ > "$OUT/seq.pid"
r() { echo "$(date -u +%T) start $1 $2 watch=$3" >> "$OUT/seq.log"; sh $W/abrun2.sh $1 $2 "$OUT" $3 >> "$OUT/seq.log" 2>&1; echo "$(date -u +%T) end $1 $2 rc=$?" >> "$OUT/seq.log"; }
r A w0 1; r B w0 1; r C w0 1
i=1
for o in "A B C" "B C A" "C A B" "A C B" "B A C" "C B A" "A B C" "B C A"; do
  for a in $o; do r $a u$i 0; done; i=$((i+1))
done
i=1
for o in "A B C" "C B A" "B A C"; do
  for a in $o; do r $a w$i 1; done; i=$((i+1))
done
echo "$(date -u +%T) SEQ-DONE" >> "$OUT/seq.log"
