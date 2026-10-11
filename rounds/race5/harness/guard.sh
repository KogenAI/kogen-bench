#!/bin/bash
# guard.sh — every 5 min: log this host's Codex weekly usage; ALERT main (no stop) at >= 90 % and on each arm's first quota refusal
R=$(cd "$(dirname "$0")" && pwd); OUTBOX="$HOME/Library/Application Support/Kogen/operations/outbox/supervisors/build-research"
alert() { printf -- '- %s %s: %s\n' "$(date -u +%FT%TZ)" "$(hostname -s)" "$1" >> "$OUTBOX/HEALTH-EVENT.md" 2>/dev/null || printf -- '- %s: %s\n' "$(date -u +%T)" "$1" >> $R/out/HEALTH-EVENT.md; echo "ALERT $1" >> $R/out/arms.log; }
a90=0
while [ ! -f $R/STOP ] && [ ! -f $R/DONE ]; do
  u=$(CODEX_HOME=$(cat $R/CODEX_HOME 2>/dev/null || echo $HOME/.codex) /usr/bin/python3 $R/codex-usage.py 2>/dev/null | grep -o 'primary=[0-9.]*' | cut -d= -f2)
  echo "$(date -u +%T) usage=$u" >> $R/out/quota.log
  [ $a90 = 0 ] && awk -v u="${u:-0}" 'BEGIN{exit !(u>=90)}' && { alert "$(basename $R): [account removed] weekly usage ${u}% (>= 90%)"; a90=1; }
  for A in $(cat $R/ARMS); do [ -f $R/out/$A/QUOTA-REFUSAL ] && [ ! -f $R/out/$A/QUOTA-ALERTED ] && { alert "$(basename $R): arm $A got its first quota/rate-limit refusal (waiting and resuming)"; touch $R/out/$A/QUOTA-ALERTED; }; done
  sleep 60
done
