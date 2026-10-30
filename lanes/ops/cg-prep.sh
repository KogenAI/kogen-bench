#!/bin/bash
# lanes host: build + plan + preflight a ChatGPT experiment already written to $P/<id>/experiment.json (no model calls).
# cg-prep.sh <id> <tasks dir> <slots>   (26 Oct: ChatGPT on every host; sign-in home $CHATGPT_KH or ~/kogen-home)
if [ -n "$LANES_ENV" ]; then . "$LANES_ENV"; else eval "$(mise activate bash --shims)"; export KOGEN_LANES_HOME=$HOME/.cache/kogen-lanes PATH=$PATH:/usr/local/bin; fi   # append: one Linux host has a system go 1.27.3 there that must not shadow mise go (26 Oct)
[ -n "$LANES_NPMFIX_HARNESS" ] && export LANES_DIR="$LANES_NPMFIX_HARNESS"
[ -z "$LANES_ENV" ] && export MISE_DATA_DIR=$HOME/.local/share/mise MISE_CACHE_DIR=$HOME/.cache/mise MISE_CONFIG_DIR=$HOME/.config/mise MISE_TRUSTED_CONFIG_PATHS=/
P=${LANES_P:-$HOME/lanes-work}; L=${LANES_DIR:-$(cd "$(dirname "$0")/.." && pwd)}; KH=${CHATGPT_KH:-$HOME/kogen-home}
E=$1; K=$2; SLOTS=${3:-3}; OUT=$P/cg-prep.log; mkdir -p $P/$E/run-logs
MM=$(cat $P/cell-memory-max 2>/dev/null); MMJ=${MM:+,\"cell_memory_max\":\"$MM\"}   # per-host memory cap per cell (27 Oct, after a Linux host ran out of memory)
echo "{\"local\":{\"target\":\"local\",\"slots\":$SLOTS$MMJ}}" > $P/$E/hosts.json
echo "$(date -u +%FT%TZ) cg-prep $E" >> $OUT
if HOME=$KH python3 $L/bin/lanes-stage --tasks "$K" --run-dir "$P/$E" > "$P/$E/run-logs/stage.out" 2>&1 \
   && python3 $L/bin/lanes-build $P/$E/experiment.json --run-dir $P/runs/$E > $P/$E/run-logs/build.out 2>&1 \
   && python3 $L/bin/lanes-plan $P/$E/experiment.json --run-dir $P/runs/$E --tasks $K > $P/$E/run-logs/plan.out 2>&1 \
   && cp $P/$E/hosts.json $P/runs/$E/ \
   && HOME=$KH python3 $L/bin/lanes-preflight $P/runs/$E --tasks $K > $P/$E/run-logs/preflight.out 2>&1; then
  echo "$E ready: cells=$(wc -l < $P/runs/$E/plan.jsonl)" | tee -a $OUT
else echo "$E FAIL: $(tail -n 3 $P/$E/run-logs/*.out | tr '\n' ' ')" | tee -a $OUT; exit 1; fi
