#!/bin/bash
# no-model stand-in round dir for lanes/confirm-eu; arg1=clone, arg2=work dir (new, empty)
set -e
C=$1; W=$2; L=$C/lanes; T=$C/reproduce/loop-high-reasoning-api-replay13/tasks.txt
P=$W/confirmation-eu-replay-20261030; mkdir -p $P/harness $P/tasks $P/cache-snapshot $P/source/kogen-loop $P/bin $W/confirmation-eu-wide-20261029 $W/codex
cp $L/bare/*.py $P/harness/; cp $L/confirm-eu/*.py $P/; ln -s $L $P/grader
for t in $(grep -v '^#' $T | awk '{print $1}'); do mkdir -p $P/tasks/$t; echo '{}' > $P/tasks/$t/task.json; done
echo x > $P/cache-snapshot/f; echo x > $P/source/kogen-loop/f; for b in loop-b8a4046 scr-api-replay-kogen-loop; do echo x > $P/bin/$b; done
echo x > $W/codex/codex; echo x > $W/codex/codex-code-mode-host
python3 -I - "$P" "$T" "$W" <<'PY'
import json,sys,os
P,T,W=sys.argv[1:]
ts=[l.split()[0] for l in open(T) if l.strip() and not l.startswith('#')]
json.dump([{'task':t,'qualified':True} for t in ts],open(P+'/eligibility.json','w'))
json.dump({'tasks_randomized':ts},open(W+'/confirmation-eu-wide-20261029/protocol.json','w'))
print(len(ts),'tasks')
PY
cd $P
export LANES_CONFIRM_DIR=$P CODEX_BIN_DIR=$W/codex
echo "--- freeze"; python3 -I run_confirmation.py freeze && python3 -I -c "import json;d=json.load(open('protocol.json'));print(len(d['cells']),'cells',d['effort'],d['model'])"
echo "--- cell 0 (expect stop at host lease check, before any request)"; python3 -I run_confirmation.py cell --index 0 2>&1 | tail -3 || true
echo "--- replay13 amend / spend / bad index"; python3 -I run_replay13.py amend; python3 -I run_replay13.py spend; python3 -I run_replay13.py cell --index 6 2>&1 | tail -2 || true
