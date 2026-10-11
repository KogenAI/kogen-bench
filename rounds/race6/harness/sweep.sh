#!/bin/bash
# sweep.sh DIR — kill every process whose cwd is under DIR (orphans of scored kogen runs)
D=$1; for pid in $(ps -axo pid=); do c=$(lsof -a -p $pid -d cwd -Fn 2>/dev/null | sed -n 's/^n//p'); case "$c" in "$D"*) kill -9 $pid 2>/dev/null && echo "swept $pid $c";; esac; done
