#!/bin/bash
# start.sh MINUTES "ARMS" SNAP_MIN LOCK|NOLOCK [START_AT_EPOCH] — race 3 wave runner (no scoring during or right after the race):
# optional wait until a shared start epoch (both hosts start together), lock other implementations, fresh arms from the kit,
# Codex arms (Sol high, 2-core caps, CODEX_HOME from ./CODEX_HOME), CPU sampler, snapshots every SNAP_MIN min, alert-only guard.
# Stopper: FINAL snapshot, stop agents, unlock (+ verify none left at 000), audit, remove live build dirs. Score later with score-all.sh.
R=$(cd "$(dirname "$0")" && pwd); M=$1; ARMS=$2; I=$3; LK=$4; AT=$5; cd $R
[ -s inputs/NCASES ] && [ -s SPEC-BUG-CASES.txt ] && [ -s TARGET.md ] || { echo "inputs not ready"; exit 1; }
rm -f STOP DONE STOP-*; mkdir -p out snapshots; : > out/arms.log; echo "$ARMS" > ARMS
./setup-arms.sh > out/setup.txt || { echo "setup failed"; exit 1; }
./checks.sh || { echo "pre-start checks failed (out/checks.txt)"; exit 1; }
if [ -n "$AT" ]; then echo "waiting for start epoch $AT ($(date -u -r $AT +%T))" >> out/arms.log; while [ $(date +%s) -lt $AT ]; do sleep 0.5; done; fi
if [ "$LK" = LOCK ]; then L=./lock-studio.sh; case "$(hostname)" in *MacBook*) L=./lock-macbook.sh;; esac; $L > out/lock.txt 2>&1 || { echo "lock failed"; cat out/lock.txt; exit 1; }; fi
S=$(date +%s); DL=$((S+M*60)); echo $S > START; echo $DL > DEADLINE
echo "start $(date -u +%T) minutes=$M arms=$ARMS snap_every=${I}m host=$(hostname -s) codex_home=$(cat CODEX_HOME 2>/dev/null || echo ~/.codex)" >> out/arms.log
for A in $ARMS; do /usr/bin/python3 $R/detach.py $R/out/arm-$A.log $R/arm.sh $R $A $DL; done
/usr/bin/python3 $R/detach.py $R/out/cpu-sampler.out $R/cpu-sampler.sh $R
/usr/bin/python3 $R/detach.py $R/out/snap-loop.out $R/snap-loop.sh $I
/usr/bin/python3 $R/detach.py $R/out/guard.out $R/guard.sh
cat > $R/stopper.sh <<EOS
#!/bin/bash
R=$R
while [ \$(date +%s) -lt $DL ] && [ ! -f \$R/STOP ]; do sleep 0.5; done
\$R/snap.sh FINAL > \$R/out/final-snap.txt 2>&1
touch \$R/STOP; echo "snapshot FINAL then STOP at \$(date -u +%T)" >> \$R/out/arms.log
pkill -f "\$R/snap-loop.sh"; sleep 10; pkill -TERM -f "\$R/arm.sh"
for p in \$(pgrep -f "codex exec"); do c=\$(/usr/sbin/lsof -a -p \$p -d cwd -Fn 2>/dev/null | sed -n 's/^n//p'); a=\$(ps -o args= -p \$p); case "\$c \$a" in *\$R/*) kill -TERM \$p && echo "stopped codex \$p";; esac; done >> \$R/out/arms.log
echo "agents stopped at \$(date -u +%T)" >> \$R/out/arms.log
[ -s \$R/locks.tsv ] && \$R/unlock.sh > \$R/out/unlock.txt 2>&1
left=\$(find ~/Areas/Kogen ~/Scratch.noindex -maxdepth 1 -perm 000 2>/dev/null | wc -l | tr -d ' '); echo "dirs left at mode 000 after unlock: \$left" >> \$R/out/arms.log
/usr/bin/python3 \$R/audit.py > \$R/out/audit.txt 2>&1
for A in $ARMS; do case "\$R/\$A/target" in "\$R/"?*) rm -rf "\$R/\$A/target";; esac; done
touch \$R/DONE; echo "finished at \$(date -u +%T) (scoring deferred: run score-all.sh)" >> \$R/out/arms.log
EOS
chmod +x $R/stopper.sh; /usr/bin/python3 $R/detach.py $R/out/stopper.log $R/stopper.sh
echo "launched: $ARMS until $(date -u -r $DL +%T)"
