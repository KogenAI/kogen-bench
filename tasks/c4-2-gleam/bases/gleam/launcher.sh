#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(dirname "$SCRIPT_DIR")
export ERL_FLAGS="+S 1:1 +SDcpu 1 +SDio 1 +A 1 +sbwt none +sbwtdcpu none +sbwtdio none"
exec /opt/bench/mise/installs/erlang/29.0.3/bin/erl \
  +S 1:1 +SDcpu 1 +SDio 1 +A 1 +sbwt none +sbwtdcpu none +sbwtdio none \
  -noshell -noinput \
  -pa "$ROOT/build/dev/erlang/durable_queue/ebin" \
  -pa "$ROOT/build/dev/erlang/gleam_stdlib/ebin" \
  -pa "$ROOT/build/dev/erlang/gleam_json/ebin" \
  -pa "$ROOT/build/dev/erlang/gleam_erlang/ebin" \
  -pa "$ROOT/build/dev/erlang/gleeunit/ebin" \
  -eval 'app:main().' -extra "$@"
