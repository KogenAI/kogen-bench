#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
. ./toolchain-env.sh
test "$(zig version)" = '0.17.0'
