#!/bin/bash
# at-w1-done.sh HOST(st|mb) — after wave 1 DONE (dirs unlocked): install v2 arm loop into w2, build pristine w3 template, arm wave3.sh for 16:30Z
H=$1; S=~/Scratch.noindex; V=$S/r3-armfix-v2; T3=1791649800
until [ -f $S/race3-$H-w1/DONE ]; do sleep 20; done; sleep 5
[ "$(stat -f %Lp $S/race3-$H-w2)" = 0 ] && { echo "w2 still locked"; exit 1; }
[ "$(stat -f %Lp $S/race3-v2)" = 0 ] && { echo "race3-v2 still locked"; exit 1; }
cp $V/arm.sh $S/race3-$H-w2/arm.sh && cp $V/arm-cont.sh $V/DECISION-RULE-A1.md $S/race3-$H-w2/ && bash -n $S/race3-$H-w2/arm.sh && echo "$(date -u +%T) w2 patched: $(grep -c RFLAGS $S/race3-$H-w2/arm.sh) RFLAGS lines"
T=$S/r3-harness-w3; rm -rf "${T:?}"; cp -c -R $S/race3-v2/final/harness $T && cp $V/arm.sh $V/arm-cont.sh $V/DECISION-RULE-A1.md $T/ && rm -rf "${T:?}/out" "${T:?}/snapshots" "${T:?}/score-wd" && echo "$(date -u +%T) w3 template ready"
cd $S && HARNESS_SRC=$T /usr/bin/python3 $S/race3-$H-w1/detach.py $S/race3-$H-w3.wave3.log /bin/bash $V/wave3.sh $T3 180 5 && echo "$(date -u +%T) wave3.sh armed for $T3"
