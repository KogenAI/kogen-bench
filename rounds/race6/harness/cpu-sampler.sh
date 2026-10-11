#!/bin/bash
# cpu-sampler.sh R — every 10 s: per-arm %CPU of the arm's whole process tree (rooted at out/<arm>/pid), plus load; until STOP
R=$1; ARMS=$(cat $R/ARMS)
while [ ! -f $R/STOP ]; do
  snap=$(ps -axo pid=,ppid=,pcpu=)
  line="$(date -u +%T) load=$(python3 -c 'import os;print(os.getloadavg()[0])')"
  for A in $ARMS; do root=$(cat $R/out/$A/pid 2>/dev/null); [ -n "$root" ] || { line="$line $A=0"; continue; }
    t=$(echo "$snap" | awk -v r=$root 'BEGIN{k[r]=1} {p[NR]=$1; pp[NR]=$2; c[NR]=$3} END{ch=1; while(ch){ch=0; for(i=1;i<=NR;i++) if(k[pp[i]] && !k[p[i]]){k[p[i]]=1; ch=1}} s=0; for(i=1;i<=NR;i++) if(k[p[i]]) s+=c[i]; printf "%.0f", s}')
    line="$line $A=$t"; done
  echo "$line" >> $R/out/cpu-samples.log; sleep 10
done
