#!/bin/sh
# Fake release script for tests: dist/kogen-<version>-<target>.tar.gz with bin/kogen, like the Go Kogen's.
set -eu
cd "$(dirname "$0")/.."
echo package >> "${LANE_BUILD_COUNT:-/dev/null}"
name="kogen-dev+$(cat VERSION)-test"
mkdir -p "dist/$name/bin" "dist/$name/lib"
printf '#!/bin/sh\necho "kogen dev+%s (2026-01-01, uncommitted source)"\n' "$(cat VERSION)" > "dist/$name/bin/kogen"
chmod +x "dist/$name/bin/kogen"
tar -C dist -czf "dist/$name.tar.gz" "$name"
echo "dist/$name.tar.gz"
