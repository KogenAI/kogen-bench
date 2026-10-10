#!/bin/sh
set -eu
app_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec /opt/bench/mise/installs/erlang/29.0.3/bin/erl +S 2:2 +A 1 -noshell -pa "$app_root"/build/dev/erlang/*/ebin -eval 'config_migrator:main(), halt().' -extra "$@"
