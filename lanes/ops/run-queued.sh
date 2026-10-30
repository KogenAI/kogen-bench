#!/bin/bash
# run-queued.sh <cg|cc> <id> <tasks dir> <slots> <cell est>   (lanes host, as lanes; launched by refill.sh or by hand)
# Preps an experiment already staged at $P/<id>/experiment.json (cg-prep.sh / cc-prep.sh: build, plan, preflight; no model
# calls), then runs it under the matching day runner: cg -> day-runner-v3.sh (ChatGPT weekly guard), cc -> day-runner.sh.
# cgr/ccr resume a prepared run (no prep): its missing cells run again, e.g. after failed cells were moved aside.
# cc uses LANES_KH (the Kogen home with the seat's stored token); cg uses CHATGPT_KH or kogen-home.
export LANES_TIMEOUT_LEDGER=${LANES_TIMEOUT_LEDGER:-${LANES_P:-$HOME/lanes-work}/timeout-ledger}   # 30 Oct (to2): a task with 2 timeouts of one study/tool/Kogen sha is deferred; override: touch <ledger>/override/<key>
K=$1; E=$2; T=$3; SL=$4; EST=${5:-0.3}; D=$(dirname "$0")
# A new unit first gives older approval debt one gated attempt. Recursive resumes
# do not drain again, and the just-current experiment is left to its normal path.
case $K in cg|cc|cgr|ccr)
  if [ "${LANES_CARRY_ACTIVE:-0}" != 1 ]; then
    [ -n "$LANES_ENV" ] && . "$LANES_ENV"
    export LANES_DIR="$LANES_NPMFIX_HARNESS"
    python3 "$LANES_DIR/bin/lanes-carry" drain "${LANES_P:-$HOME/lanes-work}/approval-carry" "$D/run-queued.sh" "$E" || exit 1
  fi;;
esac
case $K in
  cgr|ccr)
    [ -n "$LANES_ENV" ] && . "$LANES_ENV"
    export LANES_DIR="$LANES_NPMFIX_HARNESS"
    NP=${LANES_P:-$HOME/lanes-work}
    NKH=${LANES_KH:-$HOME/kogen-home}
    [ "$K" = cgr ] && NKH=${CHATGPT_KH:-$NKH}
    mkdir -p "$NP/$E/run-logs"
    HOME=$NKH python3 "$LANES_DIR/bin/lanes-stage" --tasks "$T" --run-dir "$NP/runs/$E" > "$NP/$E/run-logs/stage.out" 2>&1 || exit 1;;
esac
case $K in
  cg) bash $D/cg-prep.sh $E $T $SL || exit 1; exec env SLOTS=$SL DAYDIR=${DAYDIR:-dayspend-chatgpt} /bin/sh $D/day-runner-v3.sh $E:$T:$EST;;
  cc) bash $D/cc-prep.sh $E $T $SL ${CLAUDE_CD:-$HOME/.claude-bench} ${CLAUDE_BIN:-$HOME/.local/bin/claude} || exit 1   # CLAUDE_CD/CLAUDE_BIN: a macOS runner's paths
      exec env SLOTS=$SL KEY_NAME=${KEY_NAME:-default} DAYDIR=${DAYDIR:-dayspend-anthropic} DAYCAP=${DAYCAP:-200} /bin/sh $D/day-runner.sh $E:$T:$EST;;
  cgr) exec env SLOTS=$SL DAYDIR=${DAYDIR:-dayspend-chatgpt} /bin/sh $D/day-runner-v3.sh $E:$T:$EST;;
  ccr) exec env SLOTS=$SL KEY_NAME=${KEY_NAME:-default} DAYDIR=${DAYDIR:-dayspend-anthropic} DAYCAP=${DAYCAP:-200} /bin/sh $D/day-runner.sh $E:$T:$EST;;
  off) exec nice -n 10 /bin/bash ${LANES_P:-$HOME/lanes-work}/offline/$E.sh;;   # model-free unit (OPS-AUTONOMY): lanes-private/offline/<id>.sh
  *) echo "kind must be cg, cc, cgr, ccr or off" >&2; exit 2;;
esac
