#!/bin/bash
# kitsum.sh — sorted sha256 manifest of the race3 kit (excluding logs/, cache/tmp/, pass logs); prints the overall hash
R=$(cd "$(dirname "$0")" && pwd)
M=${RACE_KIT_MANIFEST:-$R/out/kit-manifest.sha256}
K=${RACE3_KIT_DIR:-$(dirname "$R")/race3-kit}; cd "$K" || exit 1
if command -v shasum >/dev/null; then SHA=(shasum -a 256); else SHA=(sha256sum); fi
find . -type f -not -path './logs/*' -not -path './cache/tmp/*' -not -name 'pass2-*' -not -name 'events.jsonl' -not -name 'stderr.log' -not -name 'last.md' -not -name '*.detach.log' -print0 | LC_ALL=C sort -z | xargs -0 "${SHA[@]}" > "$M"
echo "files $(wc -l < "$M") hash $("${SHA[@]}" "$M" | cut -c1-64)"
