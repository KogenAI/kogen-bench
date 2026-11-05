#!/bin/bash
# Phase 3 cell (arm 1, mode newnonce; stub3.py): start turn, P steps, then K x (/compact + Q steps). Runs as the unprivileged runner user.
# usage: run-cell2.sh <cell-name> <mode> <reserve 0|1> <K> <P> <Q> <drive resume|live> <tools 0|1>
#   mode: marker hash nonce rolling selfcheck firstmsg guide-short guide-exact none (see stub3.py)
#   drive resume = one `claude -p --resume` process per turn (phase 1); live = one process for the whole cell (live.py)
#   tools 1 = Bash, Read, Write, Edit allowed (needed to install a hook); 0 = only the two Studio tools (phase 1)
# env: ROOT (scratch root), KH (login home name under the runner user home), CC_VER,
#      PERM (claude --permission-mode; default = the client default, i.e. writes to .claude/settings*.json are denied)
set -u
NAME=$1 MODE=$2 RESERVE=$3 K=$4 P=$5 Q=$6 DRIVE=$7 TOOLS=$8
ROOT=${ROOT:?set ROOT to an empty scratch dir holding these scripts}
KH=${KH:?set KH to the login home name} CC_VER=${CC_VER:-2.1.312}
MODEL=${MODEL:-claude-sonnet-5-5}; EFFORT=${EFFORT:-medium}; PERM=${PERM:-default}
D=$ROOT/cells/$NAME; mkdir -p "$D/turns" "$D/cellhome"; cd "$D" || exit 1
/usr/bin/python3 -I - "$D/cell.json" <<PY
import json,secrets,sys
w=["heron","otter","lynx","wren","ibis","marten","plover","tern","vole","stoat"]
json.dump({"name":"$NAME","mode":"$MODE","reserve":$RESERVE,"hook_reserve":0,"K":$K,"P":$P,"Q":$Q,"drive":"$DRIVE","tools":$TOOLS,"perm":"$PERM",
 "ticket":"QX-%04d"%secrets.randbelow(10000),"prefix":"lane-"+secrets.choice(w),"brief_rev":"r1","nonce":secrets.token_hex(4),
 "model":"$MODEL","effort":"$EFFORT","client":"claude-code $CC_VER"},open(sys.argv[1],"w"),indent=1)
PY
cat > "$D/mcp.json" <<J
{"mcpServers":{"studio":{"command":"/usr/bin/python3","args":["-I","$ROOT/stub3.py"],"env":{"STUB_CELL":"$D"}}}}
J
# reference hook (paired detector, logs only); passed with --settings, invisible to the agent
cat > "$D/ref-settings.json" <<J
{"hooks":{"SessionStart":[{"matcher":"compact","hooks":[{"type":"command","command":"STUB_CELL=$D /usr/bin/python3 -I $ROOT/stub3.py --hook"}]}]}}
J
LOGINCFG=$HOME/$KH/.kogen/claude-code/config
stat -f '%m %z' "$LOGINCFG/settings.json" > "$D/login-settings.before" 2>/dev/null || echo absent > "$D/login-settings.before"
SID=$(/usr/bin/python3 -I -c "import uuid;print(uuid.uuid4())"); echo "$SID" > "$D/session.id"
TASKS=("list three risks of caching DNS answers for too long" "explain in two sentences why idempotent retries matter"
 "name two trade-offs of using UUIDv7 as a primary key" "summarise what a write-ahead log is for, in two sentences"
 "give two reasons to pin a client version in a benchmark" "explain backpressure in a queue in two sentences"
 "name two ways a cron job can run twice and one guard" "explain what a tombstone is in a replicated store"
 "give two signs that a test is flaky rather than failing" "explain why clock skew breaks lease-based locks"
 "list two costs of very long feature branches" "explain in two sentences what a canary release checks"
 "name two risks of storing secrets in environment variables" "explain the difference between p50 and p99 latency"
 "give two reasons a cache hit rate can drop after a deploy" "explain what head-of-line blocking is")
if [ "$TOOLS" = 1 ]; then TL="Bash,Read,Write,Edit"; AL=(mcp__studio__studio_start mcp__studio__studio_note Bash Read Write Edit)
else TL=""; AL=(mcp__studio__studio_start mcp__studio__studio_note); fi
COMMON=(--model "$MODEL" --effort "$EFFORT" --tools "$TL" --mcp-config "$D/mcp.json" --strict-mcp-config
  --settings "$D/ref-settings.json" --allowedTools "${AL[@]}")
[ "$PERM" != default ] && COMMON+=(--permission-mode "$PERM")
START="You are running a Studio loop. Call the studio_start tool now to get your brief and follow that brief for the whole loop. Reply only with 'ready'."
step() { echo "Step $1: ${TASKS[$(( ($1-1) % 16 ))]}. Then record your answer in Studio with studio_note (step=$1)."; }
# plan: kind<TAB>prompt
: > "$D/plan.tsv"; printf 'start\t%s\n' "$START" >> "$D/plan.tsv"; S=0
for ((i=1; i<=P; i++)); do S=$((S+1)); printf 'step\t%s\n' "$(step $S)" >> "$D/plan.tsv"; done
for ((c=1; c<=K; c++)); do printf 'compact\t/compact\n' >> "$D/plan.tsv"
  for ((i=1; i<=Q; i++)); do S=$((S+1)); printf 'step\t%s\n' "$(step $S)" >> "$D/plan.tsv"; done; done
if [ "$DRIVE" = live ]; then
  /usr/bin/python3 -I -c "import json,sys;json.dump([l.rstrip('\n').split('\t',1) for l in open(sys.argv[1])],open(sys.argv[2],'w'))" "$D/plan.tsv" "$D/plan.json"
  /usr/bin/python3 -I "$ROOT/live.py" "$D" "$D/plan.json" 420 -- /usr/bin/python3 -I "$ROOT/cc2.py" "$KH" "$CC_VER" 3600 "$D/cellhome" \
    -p --input-format stream-json --output-format stream-json --verbose --session-id "$SID" "${COMMON[@]}"
else
  N=0
  while IFS=$'\t' read -r kind prompt; do
    N=$((N+1)); f=$D/turns/$(printf %02d $N)-$kind.json
    if [ $N = 1 ]; then SA=(--session-id "$SID"); else SA=(--resume "$SID"); fi
    t0=$(/usr/bin/python3 -I -c "import time;print(time.time())")
    /usr/bin/python3 -I "$ROOT/cc2.py" "$KH" "$CC_VER" 420 "$D/cellhome" -p "$prompt" "${SA[@]}" "${COMMON[@]}" --output-format json < /dev/null > "$f" 2> "$f.err"
    rc=$?
    /usr/bin/python3 -I -c "import json,time;print(json.dumps({'n':$N,'kind':'$kind','t0':$t0,'t1':time.time(),'rc':$rc,'file':'$(basename "$f")'}))" >> "$D/events.jsonl"
  done < "$D/plan.tsv"
fi
# what the agent installed (settings files only; no credentials), and a check that the shared login home was not touched
mkdir -p "$D/installed"
for s in "$D/.claude/settings.json" "$D/cellhome/.claude/settings.json" "$D/.codex/hooks.json"; do
  [ -f "$s" ] && cp "$s" "$D/installed/$(echo "${s#$D/}" | tr / _)"; done
stat -f '%m %z' "$LOGINCFG/settings.json" > "$D/login-settings.after" 2>/dev/null || echo absent > "$D/login-settings.after"
/usr/bin/python3 -I "$ROOT/extract2.py" "$D" > "$D/extract.out" 2>&1
echo done > "$D/DONE"
