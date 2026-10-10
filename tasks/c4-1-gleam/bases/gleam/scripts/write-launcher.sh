#!/bin/sh
set -eu
mkdir -p bin
cat > bin/app <<'APP'
#!/bin/sh
set -eu
app_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec /opt/bench/mise/installs/erlang/29.0.3/bin/erl +fnu +S 1:1 +A 1 +SDcpu 1 +SDio 1 \
    -noshell -noinput -boot no_dot_erlang \
    -pa "$app_dir"/build/erlang-shipment/*/ebin \
    -eval 'landing:main(), halt().' -extra "$@"
APP
chmod 755 bin/app
