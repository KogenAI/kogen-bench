#!/bin/sh
set -eu
APP_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ERL_INETRC="$APP_ROOT/scripts/inetrc"
export ERL_INETRC
exec /opt/bench/mise/installs/erlang/29.0.3/bin/erl +S 1:1 +SDcpu 1 +SDio 1 +A 1 -noshell -noinput -pa "$APP_ROOT"/build/dev/erlang/*/ebin -eval 'nil=runtime_cleanup:quiesce(), refstore:main(), halt().' -extra "$@"
