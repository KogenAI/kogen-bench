#!/bin/bash
# kitsum.sh — sorted sha256 manifest of the race3 kit (excluding logs/, cache/tmp/, pass logs); prints the overall hash
M=${RACE_KIT_MANIFEST:-/tmp/kit-manifest.sha256}
K=${RACE3_KIT_DIR:-$HOME/retained-run/race3-kit}; cd "$K" || exit 1
find . -type f -not -path './logs/*' -not -path './cache/tmp/*' -not -name 'pass2-*' -not -name 'events.jsonl' -not -name 'stderr.log' -not -name 'last.md' -not -name '*.detach.log' -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 > "$M"
echo "files $(wc -l < "$M") hash $(shasum -a 256 "$M" | cut -c1-64)"
