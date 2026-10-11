#!/bin/bash
# start.sh 180 "ARMS" 5 LOCK|NOLOCK [START_AT_EPOCH] — race 5 wave runner (no live scoring).
# optional wait until a shared start epoch (both hosts start together), lock other implementations, fresh arms from the kit,
# Codex arms (Sol high, 2-core caps, CODEX_HOME from ./CODEX_HOME), CPU sampler, snapshots every SNAP_MIN min, alert-only guard.
# Stopper: FINAL snapshot, stop agents, unlock (+ verify none left at 000), audit, remove live build dirs. Score later with score-wave.sh.
set -e
R=$(cd "$(dirname "$0")" && pwd); M=${1:-180}; ARMS=${2:-"rust go ts ex py"}; I=${3:-5}; LK=${4:-LOCK}; AT=${5:-}; cd "$R"
[ "$M" = 180 ] && [ "$I" = 5 ] || { echo "race 5 requires a 180-minute cap and 5-minute snapshots"; exit 2; }
[ -x inputs/conformance/bin/kogen-conformance ] && [ -f SPEC-BUG-CASES.txt ] && [ -s COUNTS.txt ] && [ -s TARGET.md ] || { echo "inputs not ready"; exit 1; }
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$R/prepare-inputs.py"
rm -f STOP DONE STOP-*; mkdir -p out snapshots; : > out/arms.log; : > out/target-stops.tsv; echo "$ARMS" > ARMS
export RACE_CAP_MIN="$M" RACE_SNAPSHOT_MIN="$I"
# Admit disk before copying the private caches into fresh arms.
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$R/checks.py" --disk-only || { echo "disk admission failed"; exit 1; }
./setup-arms.sh > out/setup.txt || { echo "setup failed"; exit 1; }
./checks.sh || { echo "pre-start checks failed (out/checks.txt)"; exit 1; }
if [ -n "$AT" ] && [ "$(date +%s)" -ge "$AT" ]; then echo "missed shared start epoch; choose a later epoch" >&2; exit 1; fi
if [ "$LK" = LOCK ]; then L=./lock-studio.sh; case "$(hostname)" in *MacBook*) L=./lock-macbook.sh;; esac; $L > out/lock.txt 2>&1 || { echo "lock failed"; cat out/lock.txt; exit 1; }; fi
S=${AT:-$(date +%s)}; DL=$((S+M*60)); echo $S > START; echo $DL > DEADLINE
echo "start $(date -u +%T) minutes=$M arms=$ARMS snap_every=${I}m host=$(hostname -s) codex_home=$(cat CODEX_HOME 2>/dev/null || echo $HOME/.codex)" >> out/arms.log
# Exact result paths are private to this wave; clear prior-wave output before launch.
for A in $ARMS; do
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - "$R" "$A" <<'PYCODE'
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from target_watch import result_path
path = result_path(Path(sys.argv[1]), sys.argv[2])
path.unlink(missing_ok=True)
PYCODE
done
if [ -n "$AT" ]; then echo "waiting for start epoch $AT ($(date -u -r $AT +%T))" >> out/arms.log; while [ $(date +%s) -lt $AT ]; do sleep 0.5; done; fi
for A in $ARMS; do
  /usr/bin/python3 "$R/detach.py" "$R/out/arm-$A.log" "$R/arm.sh" "$R" "$A" "$DL"
  /usr/bin/python3 "$R/detach.py" "$R/out/target-watch-$A.log" "$R/target-watch.sh" "$A"
done
/usr/bin/python3 $R/detach.py $R/out/cpu-sampler.out $R/cpu-sampler.sh $R
/usr/bin/python3 $R/detach.py $R/out/snap-loop.out $R/snap-loop.sh $I
/usr/bin/python3 $R/detach.py $R/out/guard.out $R/guard.sh
/usr/bin/python3 "$R/detach.py" "$R/out/pruner.log" /usr/bin/python3 "$R/prune-snapshots.py" --root "$R" --loop
cat > $R/stopper.sh <<EOS
#!/bin/bash
R=$R
while [ \$(date +%s) -lt $DL ] && [ ! -f \$R/STOP ]; do sleep 0.5; done
\$R/snap.sh FINAL > \$R/out/final-snap.txt 2>&1
touch \$R/STOP; echo "snapshot FINAL then STOP at \$(date -u +%T)" >> \$R/out/arms.log
pkill -f "\$R/snap-loop.sh"; pkill -f "target_watch.py --root \$R "; sleep 10; pkill -TERM -f "\$R/arm.sh"
for p in \$(pgrep -f "codex exec"); do c=\$(/usr/sbin/lsof -a -p \$p -d cwd -Fn 2>/dev/null | sed -n 's/^n//p'); a=\$(ps -o args= -p \$p); case "\$c \$a" in *\$R/*) kill -TERM \$p && echo "stopped codex \$p";; esac; done >> \$R/out/arms.log
echo "agents stopped at \$(date -u +%T)" >> \$R/out/arms.log
[ -s \$R/locks.tsv ] && \$R/unlock.sh > \$R/out/unlock.txt 2>&1
left=\$(find $HOME/Areas/Kogen $HOME/retained-run -maxdepth 1 -perm 000 2>/dev/null | wc -l | tr -d ' '); echo "dirs left at mode 000 after unlock: \$left" >> \$R/out/arms.log
/usr/bin/python3 \$R/audit.py > \$R/out/audit.txt 2>&1
for A in $ARMS; do case "\$R/\$A/target" in "\$R/"?*) rm -rf "\$R/\$A/target";; esac; done
touch \$R/DONE; echo "finished at \$(date -u +%T) (scoring deferred: run score-wave.sh)" >> \$R/out/arms.log
EOS
chmod +x $R/stopper.sh; /usr/bin/python3 $R/detach.py $R/out/stopper.log $R/stopper.sh
echo "launched: $ARMS until $(date -u -r $DL +%T)"
