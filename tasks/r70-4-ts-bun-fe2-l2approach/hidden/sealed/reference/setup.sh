#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
. ./toolchain-env.sh
if [ ! -d node_modules ]; then cp -R /srv/bh/bench/toolchains/bun-1.4.2/node-template/node_modules .; fi
if [ ! -f bun.lock ]; then cp /srv/bh/bench/toolchains/bun-1.4.2/node-template/bun.lock .; fi
