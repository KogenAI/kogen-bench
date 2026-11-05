#!/bin/bash
# One Claude Code cell: start turn, P steps, then K x (/compact + Q steps). Runs as a dedicated cell user.
# usage: run-cell.sh <cell-name> <mode marker|firstmsg|none> <reserve 0|1> <hook_reserve 0|1> <K> <P> <Q>
# env: ROOT (scratch root), KH (name of a logged-in client home directory under $HOME), CC_VER (client version dir)
set -u
NAME=$1 MODE=$2 RESERVE=$3 HRES=$4 K=$5 P=$6 Q=$7
ROOT=${ROOT:-$HOME/work.noindex/scratch/research/compaction-marker}
KH=${KH:?set KH to a logged-in client home name}; CC_VER=${CC_VER:-2.1.312}
MODEL=${MODEL:-claude-sonnet-5-5}; EFFORT=${EFFORT:-medium}
D=$ROOT/cells/$NAME; mkdir -p "$D/turns"; cd "$D" || exit 1
/usr/bin/python3 -I - "$D/cell.json" <<PY
import json,secrets,sys
w=["heron","otter","lynx","wren","ibis","marten","plover","tern","vole","stoat"]
json.dump({"name":"$NAME","mode":"$MODE","reserve":$RESERVE,"hook_reserve":$HRES,"K":$K,"P":$P,"Q":$Q,
 "ticket":"QX-%04d"%secrets.randbelow(10000),"prefix":"lane-"+secrets.choice(w),"brief_rev":"r1","nonce":secrets.token_hex(4),
 "model":"$MODEL","effort":"$EFFORT","client":"claude-code $CC_VER"},open(sys.argv[1],"w"),indent=1)
PY
cat > "$D/mcp.json" <<J
{"mcpServers":{"studio":{"command":"/usr/bin/python3","args":["-I","$ROOT/stub.py"],"env":{"STUB_CELL":"$D"}}}}
J
cat > "$D/settings.json" <<J
{"hooks":{"SessionStart":[{"matcher":"compact","hooks":[{"type":"command","command":"STUB_CELL=$D /usr/bin/python3 -I $ROOT/stub.py --hook"}]}]}}
J
SID=$(/usr/bin/python3 -I -c "import uuid;print(uuid.uuid4())"); echo "$SID" > "$D/session.id"
TASKS=("list three risks of caching DNS answers for too long" "explain in two sentences why idempotent retries matter"
 "name two trade-offs of using UUIDv7 as a primary key" "summarise what a write-ahead log is for, in two sentences"
 "give two reasons to pin a client version in a benchmark" "explain backpressure in a queue in two sentences"
 "name two ways a cron job can run twice and one guard" "explain what a tombstone is in a replicated store"
 "give two signs that a test is flaky rather than failing" "explain why clock skew breaks lease-based locks"
 "list two costs of very long feature branches" "explain in two sentences what a canary release checks"
 "name two risks of storing secrets in environment variables" "explain the difference between p50 and p99 latency"
 "give two reasons a cache hit rate can drop after a deploy" "explain what head-of-line blocking is")
N=0
turn() { # $1 kind, $2 prompt, extra args...
  local kind=$1 prompt=$2; shift 2; N=$((N+1)); local f=$D/turns/$(printf %02d $N)-$kind.json t0 rc
  t0=$(/usr/bin/python3 -I -c "import time;print(time.time())")
  ( cd "$D" && /usr/bin/python3 -I "$ROOT/cc.py" "$KH" "$CC_VER" 420 -p "$prompt" "$@" --model "$MODEL" --effort "$EFFORT" \
    --tools "" --mcp-config "$D/mcp.json" --strict-mcp-config --settings "$D/settings.json" \
    --allowedTools mcp__studio__studio_start mcp__studio__studio_note --output-format json ) > "$f" 2> "$f.err"
  rc=$?
  /usr/bin/python3 -I -c "import json,time,sys;print(json.dumps({'n':$N,'kind':'$kind','t0':$t0,'t1':time.time(),'rc':$rc,'file':'$(basename "$f")'}))" >> "$D/events.jsonl"
}
turn start "You are running a Studio loop. Call the studio_start tool now to get your brief and follow that brief for the whole loop. Reply only with 'ready'." --session-id "$SID"
S=0
for ((i=1; i<=P; i++)); do S=$((S+1)); turn step "Step $S: ${TASKS[$(( (S-1) % 16 ))]}. Then record your answer in Studio with studio_note (step=$S)." --resume "$SID"; done
for ((c=1; c<=K; c++)); do
  turn compact "/compact" --resume "$SID"
  for ((i=1; i<=Q; i++)); do S=$((S+1)); turn step "Step $S: ${TASKS[$(( (S-1) % 16 ))]}. Then record your answer in Studio with studio_note (step=$S)." --resume "$SID"; done
done
/usr/bin/python3 -I "$ROOT/extract.py" "$D" "$HOME/$KH/.kogen/claude-code/config" > "$D/extract.out" 2>&1
echo done > "$D/DONE"
