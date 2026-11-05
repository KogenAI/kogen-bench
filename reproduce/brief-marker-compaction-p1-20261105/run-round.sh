#!/bin/bash
# Exact commands of the measured round (run as a dedicated cell user in the scratch root that holds stub.py, cc.py, run-cell.sh,
# extract.py, analyze.py). Use a client home that is already logged in.
# run-cell.sh <name> <mode> <reserve> <hook_reserve> <K compactions> <P steps before> <Q steps after each compaction>
set -u
cd "${ROOT:-$HOME/work.noindex/scratch/research/compaction-marker}" || exit 1
export KH=${KH:?set KH to a logged-in client home name} CC_VER=${CC_VER:-2.1.312}
R=${ROUND:-m1}
./run-cell.sh $R-marker      marker   0 0 4 2 2 &
./run-cell.sh $R-marker-rs   marker   1 0 4 2 2 &
./run-cell.sh $R-first       firstmsg 0 0 4 2 2 &
./run-cell.sh $R-first-rs    firstmsg 1 0 4 2 2 &
./run-cell.sh $R-hook        none     0 0 4 2 2 &
./run-cell.sh $R-hook-rs     none     0 1 4 2 2 &
./run-cell.sh $R-ctl-marker  marker   1 0 2 12 2 &   # long steady run (12 steps) then 2 compactions; round m1 ran this via a BSD seq quirk
./run-cell.sh $R-ctl-first   firstmsg 1 0 2 12 2 &
wait
/usr/bin/python3 -I analyze.py cells/$R-*
