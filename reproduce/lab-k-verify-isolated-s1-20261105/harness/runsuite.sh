#!/bin/bash
# runsuite.sh <repo copy> <features path> <report.ndjson> <order: defined|random:N> <tmpdir> [extra --require file]
# The readiness acceptance command (project.yaml acceptance.run) with --order and an optional extra step file.
# Prints "WALL <seconds> RC <rc>" on the last line. Runs as lanes on EU; no model, no secrets.
set -u
copy=$1; feat=$2; rep=$3; order=$4; tmpd=$5; extra=${6:-}
. "$LABW/env.sh"
M=$HOME/.local/share/mise/installs
export PATH=$M/erlang/29.1.1/bin:$M/elixir/1.20.4-otp-29/bin:$PATH
rel=$(ls -d "$LABW"/rel/kogen-*-linux-x86_64)
export KOGEN_NODE=$M/node/24.21.0/bin/node KOGEN_CUCUMBER=$rel/lib/cucumber/node_modules KOGEN_QUINT=$rel/lib/quint
export KOGEN_ARCHIVE=$(ls "$LABW"/kogen/dist/kogen-*-linux-x86_64.tar.gz)
set -- $feat; first=$1
export KOGEN_ACCEPTANCE_FEATURES=${KENV:-$first} KOGEN_ACCEPTANCE_REPORT=$rep
mkdir -p "$tmpd" && export TMPDIR=$tmpd
cd "$copy" || exit 9
args=(--strict --require 'features/steps/*.js')
[ -n "$extra" ] && args+=(--require "$extra")
[ "$order" != defined ] && args+=(--order "$order")
args+=(--format "message:$rep")
t0=$(date +%s.%N)
NODE_PATH="$KOGEN_CUCUMBER" "$KOGEN_NODE" "$KOGEN_CUCUMBER/@cucumber/cucumber/bin/cucumber.js" "${args[@]}" $feat > "$rep.stdout" 2>&1
rc=$?
t1=$(date +%s.%N)
echo "WALL $(echo "$t1 - $t0" | bc) RC $rc"
