#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
. ./toolchain-env.sh
export MIX_ENV=test
if [ ! -d deps ]; then cp -R /srv/bh/bench/toolchains/elixir-1.20.2-otp29/project/deps .; fi
if [ ! -f mix.lock ]; then cp /srv/bh/bench/toolchains/elixir-1.20.2-otp29/project/mix.lock .; fi
mkdir -p .r70
if [ ! -f .r70/deps.plt ]; then
  cp /srv/bh/bench/toolchains/elixir-1.20.2-otp29/project/_build/test/dialyxir_erlang-29.0.3_elixir-1.20.2_deps-test.plt .r70/deps.plt
  cp /srv/bh/bench/toolchains/elixir-1.20.2-otp29/project/_build/test/dialyxir_erlang-29.0.3_elixir-1.20.2_deps-test.plt.hash .r70/deps.plt.hash
fi
mix deps.compile
