#!/bin/bash
# unlock.sh — restore the exact modes recorded by the lock step
set -e
R=$(cd "$(dirname "$0")" && pwd); while IFS=$'\t' read -r mode dir; do chmod "$mode" "$dir"; echo "restored $mode $dir"; done < "$R/locks.tsv"
