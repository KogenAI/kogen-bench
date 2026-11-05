#!/bin/sh
# mon.sh <outfile> <stopfile> : every 5 s append "epoch delivery_procs load1" until stopfile exists
while [ ! -e "$2" ]; do echo "$(date +%s) $(sh $(dirname $0)/gate.sh count) $(cut -d' ' -f1 /proc/loadavg)" >> "$1"; sleep 5; done
