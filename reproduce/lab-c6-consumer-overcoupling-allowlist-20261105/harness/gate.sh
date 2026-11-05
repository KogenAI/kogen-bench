#!/bin/sh
# gate.sh quiet [maxwait_s]  : wait until no delivery process is on the host (and none of mine), polling 10 s; exit 1 on timeout
# gate.sh count              : print the number of delivery processes now
# Delivery = anything under scratch/delivery or work.noindex/src, kogen intent/kbuild/hostbin heavy.sh, or user kbuild; mine (build-speed-e2e3) excluded.
cnt() { ps -eo user:12,args | grep -E 'scratch/delivery|work\.noindex/src|kogen intent|kbuild\.sh|hostbin/heavy\.sh|^kbuild ' | grep -v -E 'grep|build-speed-e2e3|ps -eo|gate\.sh|systemd|sd-pam|dbus' | wc -l; }
if [ "$1" = count ]; then cnt; exit 0; fi
max=${2:-900}; t=0
while [ $t -lt $max ]; do
  c=$(cnt); l=$(cut -d' ' -f1 /proc/loadavg)
  if [ "$c" -eq 0 ] && [ "$(echo "$l < 0.5" | bc)" = 1 ]; then echo "quiet load1=$l waited=${t}s"; exit 0; fi
  sleep 10; t=$((t+10))
done
echo "NOT QUIET after ${max}s: $(cnt) delivery processes, load1=$(cut -d' ' -f1 /proc/loadavg)"; exit 1
