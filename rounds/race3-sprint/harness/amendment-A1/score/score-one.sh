#!/bin/bash
# score-one.sh HOST W LABEL ARM [TAG] — score one arm-snapshot (cached per TAG; waits for an in-flight scoring of the same arm-snapshot); prints scored pass count
H=$1; W=$2; L=$3; A=$4; TAG=${5:-prio}; R=~/Scratch.noindex/race3-$H-$W; cd $R || exit 1
inflight(){ for p in $(pgrep -f "score-arm.sh $L $A\$"); do c=$(/usr/sbin/lsof -a -p $p -d cwd -Fn 2>/dev/null | sed -n 's/^n//p'); [ "$c" = "$R" ] && return 0; done; return 1; }
while inflight; do sleep 5; done
c=$(awk -F'\t' -v l="$L" -v a="$A" -v t="$TAG" '$1==l && $2==a && $6==t' out/scores-$TAG.tsv 2>/dev/null | tail -1)
if [ -z "$c" ]; then case "$L" in (T+*) export SCORE_CASES=$(cat ~/Scratch.noindex/r3-armfix-v2/score/SCORED-56.csv);; esac; SCORE_JOBS=${SCORE_JOBS:-2} SCORE_TAG=$TAG ./score-arm.sh "$L" "$A" >/dev/null 2>&1; c=$(awk -F'\t' -v l="$L" -v a="$A" '$1==l && $2==a' out/scores-$TAG.tsv | tail -1); fi
echo "$c" | cut -f4 | awk '{print $2}' | cut -d/ -f1
