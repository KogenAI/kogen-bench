#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
. ./toolchain-env.sh
version=$(zig version)
if [ "$version" != "0.17.0" ]; then
    echo "expected Zig 0.17.0, found $version" >&2
    exit 1
fi
