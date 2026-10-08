#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
. ./toolchain-env.sh
if [ ! -d build/packages ]; then cp -R /srv/bh/bench/toolchains/gleam-1.18.1/cache/project/build .; fi
if [ ! -f manifest.toml ]; then cp /srv/bh/bench/toolchains/gleam-1.18.1/cache/project/manifest.toml .; fi
find src test -type f -exec touch {} +
