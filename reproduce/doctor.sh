#!/usr/bin/env bash
# Read-only, model-free host qualification. Does not inspect login state.
set -euo pipefail
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
# shellcheck disable=SC1091
source "$HERE/host-pins.lock"
ROOT=/srv/bh/bench
TOOLS=/opt/bench
# shellcheck source=/dev/null
source /etc/os-release
fail=0
check() { if "$@"; then printf 'OK: %s\n' "$*"; else printf 'FAIL: %s\n' "$*" >&2; fail=1; fi; }
version() { local out; out=$("$1" --version 2>&1) && [[ $out == *"$2"* ]]; }
go_version() { local out; out=$("$1" version 2>&1) && [[ $out == *"$2"* ]]; }
zig_version() { local out; out=$("$1" version 2>&1) && [[ $out == *"$2"* ]]; }
erlang_version() { local out; out=$("$1" -noshell -eval 'io:format("~s",[erlang:system_info(otp_release)]),halt().' 2>&1) && [[ $out == 29 ]]; }
elixir_version() { local out; out=$(PATH="$TOOLS/mise/installs/erlang/$ERLANG_VERSION/bin:$PATH" "$1" --version 2>&1) && [[ $out == *"$2"* ]]; }
bundler_version() { "$1" list --local --exact bundler | grep -Fq "$2"; }
marker() { [[ -f $1/.kogen-artifact-sha256 && $(cat "$1/.kogen-artifact-sha256") == "$2" ]]; }
sha() { [[ -f $1 && $(sha256sum "$1" | cut -d' ' -f1) == "$2" ]]; }
owner() { [[ $(stat -c '%U:%G' "$1") == "$2" ]]; }
check test "$(uname -m)" = "$ARCH"
check test "$ID" = ubuntu
check test "$VERSION_ID" = "$UBUNTU_VERSION"
check version /usr/bin/bwrap "$BWRAP_VERSION"
check version /usr/local/bin/mise "$MISE_VERSION"
check sha /usr/local/bin/mise "$MISE_SHA256"
check getent passwd benchadmin
check getent passwd bench
check getent group bench
check owner "$ROOT" benchadmin:bench
check marker "$TOOLS/mise/installs/erlang/$ERLANG_VERSION" "$ERLANG_SHA256"
check marker "$TOOLS/mise/installs/elixir/$ELIXIR_VERSION" "$ELIXIR_SHA256"
check marker "$TOOLS/mise/installs/python/$PYTHON_VERSION" "$PYTHON_SHA256"
check marker "$TOOLS/mise/installs/ruby/$RUBY_VERSION" "$RUBY_SHA256"
check marker "$TOOLS/mise/installs/node/$NODE_VERSION" "$NODE_SHA256"
check marker "$TOOLS/rustup/toolchains/$RUST_VERSION-x86_64-unknown-linux-gnu" "$RUST_SHA256"
check marker "$ROOT/toolchains/go-$GO_VERSION" "$GO_SHA256"
check marker "$ROOT/toolchains/bun-$BUN_VERSION" "$BUN_SHA256"
check marker "$ROOT/toolchains/zig-$ZIG_VERSION" "$ZIG_SHA256"
check marker "$ROOT/toolchains/gleam-$GLEAM_VERSION" "$GLEAM_SHA256"
check marker "$TOOLS/tools/codex-$CODEX_VERSION" "$CODEX_SHA256"
check sha "$TOOLS/tools/bin/codex" "$CODEX_BINARY_SHA256"
check version "$TOOLS/tools/bin/codex" "$CODEX_VERSION"
check test -x "$TOOLS/tools/bin/codex-code-mode-host"
check test -x "$TOOLS/tools/codex-$CODEX_VERSION/vendor/$CODEX_TARGET/codex-path/rg"
check test -d "$TOOLS/tools/codex-$CODEX_VERSION/vendor/$CODEX_TARGET/codex-resources"
check go_version "$ROOT/toolchains/go-$GO_VERSION/bin/go" "$GO_VERSION"
check version "$ROOT/toolchains/bun-$BUN_VERSION/bin/bun" "$BUN_VERSION"
check version "$ROOT/toolchains/gleam-$GLEAM_VERSION/bin/gleam" "$GLEAM_VERSION"
check zig_version "$ROOT/toolchains/zig-$ZIG_VERSION/zig" "$ZIG_VERSION"
check version "$TOOLS/rustup/toolchains/$RUST_VERSION-x86_64-unknown-linux-gnu/bin/rustc" "$RUST_VERSION"
check version "$TOOLS/mise/installs/python/$PYTHON_VERSION/bin/python3" "$PYTHON_VERSION"
check env PYTHONPATH="$ROOT/toolchains/python-$PYTHON_VERSION/lib/python3.14/site-packages" "$ROOT/toolchains/python-$PYTHON_VERSION/bin/python3" -m pytest --version
check version "$TOOLS/mise/installs/ruby/$RUBY_VERSION/bin/ruby" "$RUBY_VERSION"
check bundler_version "$TOOLS/mise/installs/ruby/$RUBY_VERSION/bin/gem" "$BUNDLER_WRITEBOOK_VERSION"
check bundler_version "$TOOLS/mise/installs/ruby/$RUBY_VERSION/bin/gem" "$BUNDLER_OTHER_VERSION"
check version "$TOOLS/mise/installs/node/$NODE_VERSION/bin/node" "$NODE_VERSION"
check erlang_version "$TOOLS/mise/installs/erlang/$ERLANG_VERSION/bin/erl"
check elixir_version "$TOOLS/mise/installs/elixir/$ELIXIR_VERSION/bin/elixir" 1.20.2
# Offline dependency snapshots: each template must match the shipped lockfiles.
deps_sha() { (cd "$HERE/deps" && sha256sum "$@") | sha256sum | cut -d' ' -f1; }
lock_marker() { [[ -f $1/.kogen-lock-sha256 && $(cat "$1/.kogen-lock-sha256") == "$2" ]]; }
bench_readable() { runuser -u bench -- test -r "$1" -a -x "$1"; }
ELIXIR_KIT="$ROOT/toolchains/elixir-1.20.2-otp29"
ELIXIR_DEPS_SHA=$(printf '%s hex-%s\n' "$(deps_sha elixir/mix.exs elixir/mix.lock)" "$HEX_VERSION" | sha256sum | cut -d' ' -f1)
DIALYXIR_PLT="dialyxir_erlang-${ERLANG_VERSION}_elixir-1.20.2"
check test -d "$ROOT/toolchains/rust-$RUST_VERSION/cache/cargo-home"
check lock_marker "$ROOT/toolchains/rust-$RUST_VERSION/vendor" "$(deps_sha rust/vendor.tsv rust/build_vendor.py)"
check test "$(find "$ROOT/toolchains/rust-$RUST_VERSION/vendor" -mindepth 1 -maxdepth 1 -type d | wc -l)" = "$(wc -l < "$HERE/deps/rust/vendor.tsv")"
check bench_readable "$ROOT/toolchains/rust-$RUST_VERSION/vendor"
check bench_readable "$ROOT/toolchains/rust-$RUST_VERSION/cache/cargo-home"
check test -d "$ROOT/toolchains/go-$GO_VERSION/cache/gomodcache"
check sha "$ROOT/toolchains/go-$GO_VERSION/bin/golangci-lint" "$GOLANGCI_LINT_BINARY_SHA256"
check version "$ROOT/toolchains/go-$GO_VERSION/bin/golangci-lint" "$GOLANGCI_LINT_VERSION"
check lock_marker "$ELIXIR_KIT/project" "$ELIXIR_DEPS_SHA"
check lock_marker "$ELIXIR_KIT/mix-home" "$ELIXIR_DEPS_SHA"
check lock_marker "$ELIXIR_KIT/hex-home" "$ELIXIR_DEPS_SHA"
check test -d "$ELIXIR_KIT/project/deps"
check test -f "$ELIXIR_KIT/project/_build/test/${DIALYXIR_PLT}_deps-test.plt"
check test -f "$ELIXIR_KIT/project/_build/test/${DIALYXIR_PLT}_deps-test.plt.hash"
check test -f "$ELIXIR_KIT/mix-home/$DIALYXIR_PLT.plt"
check test -d "$ELIXIR_KIT/mix-home/archives/hex-$HEX_VERSION"
check bench_readable "$ELIXIR_KIT/project/deps"
check lock_marker "$ROOT/toolchains/bun-$BUN_VERSION/node-template" "$(deps_sha bun/package.json bun/bun.lock)"
check test -d "$ROOT/toolchains/bun-$BUN_VERSION/node-template/node_modules"
check bench_readable "$ROOT/toolchains/bun-$BUN_VERSION/node-template/node_modules"
check lock_marker "$ROOT/toolchains/gleam-$GLEAM_VERSION/cache/project" "$(deps_sha gleam/gleam.toml gleam/manifest.toml gleam/src/r70_gleam_cache.gleam gleam/test/r70_gleam_cache_test.gleam)"
check test -d "$ROOT/toolchains/gleam-$GLEAM_VERSION/cache/project/build"
check bench_readable "$ROOT/toolchains/gleam-$GLEAM_VERSION/cache/project/build"
check test -L "$ROOT/kits/current"
check test -f "$ROOT/kits/current/.complete"
check test -f "$ROOT/kits/current/tasks/index.json"
check test -f "$ROOT/kits/current/reproduce/run-lane.sh"
check test -x /usr/local/bin/bench-disk-floor
check test -x /usr/local/bin/bench-run-lane
check test -x /usr/local/bin/bench-run-controls
check test -f /etc/sudoers.d/90-kogen-benchadmin
check /usr/local/bin/bench-disk-floor "$ROOT"
check test "$(sysctl -n kernel.unprivileged_userns_clone)" = 1
check test "$(sysctl -n user.max_user_namespaces)" = "$USER_MAX_USER_NAMESPACES"
check test "$(sysctl -n kernel.yama.ptrace_scope)" = 1
check test "$(sysctl -n vm.swappiness)" = 10
check systemctl cat bench.slice
check systemctl is-active --quiet fail2ban.service
check command -v systemd-run
check runuser -u bench -- /usr/bin/bwrap --unshare-user --unshare-pid --ro-bind / / --proc /proc --dev /dev /usr/bin/true
# The bundle manifest can carry protected metadata; qualify its presence without reading it.
check test -f "$ROOT/kits/current/tasks/_bases/MANIFEST.sha256"
if [[ -d /home/bench/.codex ]]; then
  check runuser -u bench -- bash "$HERE/egress-selftest.sh"
else
  printf 'SKIP: egress self-test needs /home/bench/.codex; run codex login as bench first\n'
fi
check timeout --signal=KILL 300 bash "$HERE/selftest-lane-hostile.sh"
if (( fail )); then exit 1; fi
printf 'Host doctor: PASS (no model call)\n'
