#!/bin/bash
# deploy.sh R ARM DL — replace the running main arm.sh loop for ARM with arm-cont.sh (keeps any in-flight turn running)
R=$1; L=$2; DL=$3; O=$R/out/$L; cur=$(cat $O/pid 2>/dev/null)
for p in $(pgrep -f "$R/arm.sh $R $L "); do
  [ "$p" = "$cur" ] && continue
  pp=$(ps -o ppid= -p $p | tr -d ' '); pc=$(ps -o args= -p $pp 2>/dev/null)
  case "$pc" in *"/arm.sh $R $L "*) continue;; esac   # subshell of the loop, keep it
  kill -9 $p && echo "killed main loop $p ($L)"
done
/usr/bin/python3 $R/detach.py $O/arm-cont.log /bin/bash $R/arm-cont.sh $R $L $DL
sleep 1; echo "cont: $(pgrep -f "$R/arm-cont.sh $R $L " | tr '\n' ' ') inflight=$cur alive=$(kill -0 $cur 2>/dev/null && echo yes || echo no)"
