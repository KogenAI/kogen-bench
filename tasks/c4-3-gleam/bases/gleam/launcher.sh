#!/bin/sh
set -eu
C4_APP_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export C4_APP_PATH="$C4_APP_ROOT/bin/app"
export ERL_CRASH_DUMP=/dev/null
exec /opt/bench/mise/installs/erlang/29.0.3/bin/erl +S 2:2 +SDcpu 1 +SDio 1 -noshell -noinput -pa "$C4_APP_ROOT"/build/dev/erlang/*/ebin -s c4_supervisor main -extra "$@"
