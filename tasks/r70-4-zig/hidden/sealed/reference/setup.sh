#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
. ./toolchain-env.sh
VERSION=$(zig version)
if [ "$VERSION" != "0.17.0" ]; then
	printf 'expected Zig 0.17.0, got %s\n' "$VERSION" >&2
	exit 1
fi
