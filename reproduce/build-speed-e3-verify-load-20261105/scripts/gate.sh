#!/bin/sh
# gate.sh quiet [maxwait_s]  : wait until the host is free of delivery AND of any other helper's go/node/kogen/.test process, load1 < 1.2, settle 8 s, re-check; exit 1 on timeout
# gate.sh count              : print the number of foreign busy processes now (delivery patterns + other helpers' go/node/kogen/beam/cucumber-js/*.test)
# "Mine" = anything whose command line or cwd contains build-speed-e2e3.
cnt() {
  d=$(ps -eo user:12,args | grep -E 'scratch/delivery|work\.noindex/src|kogen intent|kbuild\.sh|hostbin/heavy\.sh|^kbuild ' | grep -v -E 'grep|build-speed-e2e3|ps -eo|gate\.sh|systemd|sd-pam|dbus' | wc -l)
  o=0
  for p in $(ls /proc | grep -E '^[0-9]+$'); do
    c=$(cat /proc/$p/comm 2>/dev/null) || continue
    case "$c" in go|node|kogen|npm|beam.smp|cucumber-js|*.test) ;; *) continue;; esac
    cw=$(readlink /proc/$p/cwd 2>/dev/null); cm=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
    case "$cw$cm" in *build-speed-e2e3*) continue;; esac
    o=$((o+1))
  done
  echo $((d+o))
}
if [ "$1" = count ]; then cnt; exit 0; fi
max=${2:-900}; t=0
while [ $t -lt $max ]; do
  c=$(cnt); l=$(cut -d' ' -f1 /proc/loadavg)
  if [ "$c" -eq 0 ] && [ "$(echo "$l < 1.2" | bc)" = 1 ]; then
    sleep 8; c=$(cnt); [ "$c" -eq 0 ] && { echo "quiet load1=$l waited=${t}s"; exit 0; }
  fi
  sleep 10; t=$((t+10))
done
echo "NOT QUIET after ${max}s: $(cnt) foreign busy processes, load1=$(cut -d' ' -f1 /proc/loadavg)"; exit 1
