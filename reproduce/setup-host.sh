#!/usr/bin/env bash
# Provision an Ubuntu 24.04 x86_64 benchmark worker from this checkout.
set -euo pipefail

HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd -- "$HERE/.." && pwd)
# shellcheck disable=SC1091
source "$HERE/host-pins.lock"
DRY=0
if [[ ${1:-} == --dry-run && $# == 1 ]]; then DRY=1
elif (( $# )); then echo 'usage: sudo ./reproduce/setup-host.sh [--dry-run]' >&2; exit 2
fi
say() { printf '%s\n' "$*"; }
action() { if (( DRY )); then printf 'DRY RUN: %s\n' "$*"; else say "$*"; fi; }
run() { action "$(printf '%q ' "$@")"; if (( ! DRY )); then "$@"; fi; }

if (( ! DRY )); then
  [[ $EUID == 0 ]] || { echo 'Run with sudo' >&2; exit 1; }
  [[ $(uname -m) == "$ARCH" ]] || { echo "Requires $ARCH" >&2; exit 1; }
  # shellcheck source=/dev/null
  source /etc/os-release
  [[ $ID == ubuntu && $VERSION_ID == "$UBUNTU_VERSION" ]] || { echo "Requires Ubuntu $UBUNTU_VERSION" >&2; exit 1; }
  if [[ -n $(git -c "safe.directory=$REPO" -C "$REPO" status --porcelain -- tasks reproduce) ]]; then
    echo 'Commit task and reproduce changes before installing a versioned kit' >&2; exit 1
  fi
fi

CACHE=/var/cache/kogen-bench/artifacts
TMP=/var/tmp/kogen-bench-setup
ROOT=/srv/bh/bench
TOOLS=/opt/bench
mkdir_owned() { run install -d -m "$1" -o "$2" -g "$3" "$4"; }
fetch() {
  local key=$1 url=$2 sha=$3 dest="$CACHE/$1" actual
  [[ $sha =~ ^[0-9a-f]{64}$ ]] || { echo "Invalid SHA-256 for $key" >&2; exit 1; }
  if (( DRY )); then action "download $url -> $dest; verify SHA-256 $sha"; return; fi
  mkdir -p "$CACHE"
  if [[ ! -f $dest ]]; then
    curl --fail --location --retry 3 --output "$dest.part" "$url"
    mv -f "$dest.part" "$dest"
  fi
  actual=$(sha256sum "$dest" | cut -d' ' -f1)
  if [[ $actual != "$sha" ]]; then rm -f "$dest"; echo "SHA-256 mismatch: $key" >&2; exit 1; fi
}
ready() { [[ -f $1/.kogen-artifact-sha256 && $(cat "$1/.kogen-artifact-sha256") == "$2" ]]; }
mark() { if (( ! DRY )); then printf '%s\n' "$2" > "$1/.kogen-artifact-sha256"; rm -f "$1/.kogen-installing"; fi; }
reset_partial() {
  if (( ! DRY )) && [[ -e $1 ]] && ! ready "$1" "$2"; then
    [[ -f $1/.kogen-installing ]] || { echo "Unmanaged existing installation: $1" >&2; exit 1; }
    rm -rf -- "$1"
  fi
}
begin_install() { if (( ! DRY )); then touch "$1/.kogen-installing"; fi; }

# Accounts and SSH protection come first: Ubuntu starts fail2ban's sshd jail as soon as the package is installed,
# so the operator account and its key, and the operator's ignore list, must exist before that happens.
if (( DRY )); then action 'Ensure groups benchadmin and bench, users benchadmin and bench'; else
  getent group benchadmin >/dev/null || groupadd benchadmin
  getent passwd benchadmin >/dev/null || useradd -m -s /bin/bash -g benchadmin benchadmin
  getent group bench >/dev/null || groupadd bench
  getent passwd bench >/dev/null || useradd -m -s /bin/bash -g bench bench
  usermod -aG bench benchadmin
fi
ADMIN_KEYS=${BENCHADMIN_AUTHORIZED_KEYS:-/root/.ssh/authorized_keys}
action "Seed benchadmin SSH keys from $ADMIN_KEYS if benchadmin has none"
ADMIN_HOME=$(getent passwd benchadmin | cut -d: -f6 || true)
if (( ! DRY )) && [[ -s $ADMIN_KEYS && ! -s $ADMIN_HOME/.ssh/authorized_keys ]]; then
  install -d -m 0700 -o benchadmin -g benchadmin "$ADMIN_HOME/.ssh"
  install -m 0600 -o benchadmin -g benchadmin "$ADMIN_KEYS" "$ADMIN_HOME/.ssh/authorized_keys"
fi
action 'Write /etc/fail2ban/jail.d/90-kogen-bench.conf (ignoreself plus BENCH_FAIL2BAN_IGNOREIP)'
if (( ! DRY )); then
  install -d -m 0755 /etc/fail2ban/jail.d
  printf '[DEFAULT]\nignoreself = true\nignoreip = %s\n' "${BENCH_FAIL2BAN_IGNOREIP:-}" > /etc/fail2ban/jail.d/90-kogen-bench.conf
  if systemctl is-active --quiet fail2ban; then systemctl reload fail2ban; fi
fi

action 'Update Ubuntu APT package indexes'
action "Install Ubuntu $UBUNTU_VERSION packages: bubblewrap=$BWRAP_APT_VERSION sudo fail2ban ca-certificates curl git rsync jq zstd unzip xz-utils zip build-essential autoconf m4 bison libssl-dev libreadline-dev libncurses-dev libffi-dev libxml2-dev libsqlite3-dev libyaml-dev libgdbm-dev libdb-dev libbz2-dev liblzma-dev zlib1g-dev libexpat1-dev uuid-dev libcrypt-dev pkg-config perl make python3 (APT verifies hashes from signed metadata)"
if (( ! DRY )); then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y --no-install-recommends "bubblewrap=$BWRAP_APT_VERSION" sudo fail2ban ca-certificates curl git rsync jq zstd unzip xz-utils zip \
    build-essential autoconf m4 bison libssl-dev libreadline-dev libncurses-dev libffi-dev libxml2-dev \
    libsqlite3-dev libyaml-dev libgdbm-dev libdb-dev libbz2-dev liblzma-dev zlib1g-dev \
    libexpat1-dev uuid-dev libcrypt-dev pkg-config perl make python3
fi

mkdir_owned 0755 benchadmin bench "$ROOT"
for d in tools tools-next toolchains tasks runner results work recovery-2026-10-02; do mkdir_owned 0755 benchadmin bench "$ROOT/$d"; done
mkdir_owned 0755 root root "$TOOLS"
mkdir_owned 0755 root root "$TOOLS/mise"
mkdir_owned 0755 root root "$TOOLS/mise/installs"
mkdir_owned 0755 root root "$TOOLS/tools/bin"
mkdir_owned 0755 root root "$CACHE"
mkdir_owned 0755 root root "$TMP"

fetch mise "$MISE_URL" "$MISE_SHA256"
if (( DRY )) || [[ ! -x /usr/local/bin/mise || $(sha256sum /usr/local/bin/mise | cut -d' ' -f1) != "$MISE_SHA256" ]]; then
  run install -m 0755 "$CACHE/mise" /usr/local/bin/mise
fi

# Prebuilt toolchains: each archive is checked before extraction.
install_tar() {
  local key=$1 url=$2 sha=$3 dest=$4 member=$5
  fetch "$key" "$url" "$sha"
  if (( DRY )); then action "extract $key ($member) -> $dest"; return; fi
  if ready "$dest" "$sha"; then return; fi
  reset_partial "$dest" "$sha"; mkdir -p "$dest"
  begin_install "$dest"
  tar -xf "$CACHE/$key" -C "$dest" "$member" --strip-components=1
  mark "$dest" "$sha"
}

install_tar node "$NODE_URL" "$NODE_SHA256" "$TOOLS/mise/installs/node/$NODE_VERSION" "node-v$NODE_VERSION-linux-x64"
install_tar zig "$ZIG_URL" "$ZIG_SHA256" "$ROOT/toolchains/zig-$ZIG_VERSION" "zig-x86_64-linux-$ZIG_VERSION"
fetch go "$GO_URL" "$GO_SHA256"
GO_DIR="$ROOT/toolchains/go-$GO_VERSION"
if (( DRY )); then action "extract Go -> $GO_DIR/go and link $GO_DIR/bin/go"; elif ! ready "$GO_DIR" "$GO_SHA256"; then
  reset_partial "$GO_DIR" "$GO_SHA256"; mkdir -p "$GO_DIR/bin"
  begin_install "$GO_DIR"
  tar -xf "$CACHE/go" -C "$GO_DIR"
  ln -s ../go/bin/go "$GO_DIR/bin/go"
  ln -s ../go/bin/gofmt "$GO_DIR/bin/gofmt"
  mark "$GO_DIR" "$GO_SHA256"
fi
fetch bun "$BUN_URL" "$BUN_SHA256"
if (( DRY )); then action "extract bun -> $ROOT/toolchains/bun-$BUN_VERSION"; elif ! ready "$ROOT/toolchains/bun-$BUN_VERSION" "$BUN_SHA256"; then
  reset_partial "$ROOT/toolchains/bun-$BUN_VERSION" "$BUN_SHA256"
  mkdir -p "$ROOT/toolchains/bun-$BUN_VERSION/bin"
  begin_install "$ROOT/toolchains/bun-$BUN_VERSION"
  unzip -qo "$CACHE/bun" -d "$TMP/bun"
  install -m 0755 "$TMP/bun/bun-linux-x64/bun" "$ROOT/toolchains/bun-$BUN_VERSION/bin/bun"
  mark "$ROOT/toolchains/bun-$BUN_VERSION" "$BUN_SHA256"
fi
fetch gleam "$GLEAM_URL" "$GLEAM_SHA256"
GLEAM_DIR="$ROOT/toolchains/gleam-$GLEAM_VERSION"
if (( DRY )); then action "extract Gleam -> $GLEAM_DIR/bin"; elif ! ready "$GLEAM_DIR" "$GLEAM_SHA256"; then
  reset_partial "$GLEAM_DIR" "$GLEAM_SHA256"; mkdir -p "$GLEAM_DIR/bin"
  begin_install "$GLEAM_DIR"
  tar -xf "$CACHE/gleam" -C "$GLEAM_DIR/bin"
  mark "$GLEAM_DIR" "$GLEAM_SHA256"
fi

# Rust's official component installer writes to the final prefix. A completed
# marker makes this safe to repeat; interrupted installs are replaced.
fetch rust "$RUST_URL" "$RUST_SHA256"
RUST_DIR="$TOOLS/rustup/toolchains/$RUST_VERSION-x86_64-unknown-linux-gnu"
if (( DRY )); then action "install Rust $RUST_VERSION -> $RUST_DIR"; elif ! ready "$RUST_DIR" "$RUST_SHA256"; then
  reset_partial "$RUST_DIR" "$RUST_SHA256"
  mkdir -p "$TMP/rust" "$RUST_DIR"
  begin_install "$RUST_DIR"
  tar -xf "$CACHE/rust" -C "$TMP/rust"
  "$TMP/rust/rust-$RUST_VERSION-x86_64-unknown-linux-gnu/install.sh" --prefix="$RUST_DIR" --disable-ldconfig
  mark "$RUST_DIR" "$RUST_SHA256"
fi

# Source builds use checked upstream source archives; no build step downloads.
build_source() {
  local key=$1 url=$2 sha=$3 dest=$4 extracted=$5; shift 5
  fetch "$key" "$url" "$sha"
  if (( DRY )); then action "build $key from verified source -> $dest ($*)"; return; fi
  if ready "$dest" "$sha"; then return; fi
  reset_partial "$dest" "$sha"
  rm -rf "$TMP/$key-src"; mkdir -p "$TMP/$key-src" "$dest"
  begin_install "$dest"
  tar -xf "$CACHE/$key" -C "$TMP/$key-src"
  ( cd "$TMP/$key-src/$extracted"; ./configure --prefix="$dest" "$@"; make -j "$(nproc)"; make install )
  mark "$dest" "$sha"
}
build_source erlang "$ERLANG_URL" "$ERLANG_SHA256" "$TOOLS/mise/installs/erlang/$ERLANG_VERSION" "otp_src_$ERLANG_VERSION" --without-javac --without-wx
fetch elixir "$ELIXIR_URL" "$ELIXIR_SHA256"
ELIXIR_DIR="$TOOLS/mise/installs/elixir/$ELIXIR_VERSION"
if (( DRY )); then action "extract Elixir -> $ELIXIR_DIR"; elif ! ready "$ELIXIR_DIR" "$ELIXIR_SHA256"; then
  reset_partial "$ELIXIR_DIR" "$ELIXIR_SHA256"; mkdir -p "$ELIXIR_DIR"
  begin_install "$ELIXIR_DIR"
  unzip -qo "$CACHE/elixir" -d "$ELIXIR_DIR"
  mark "$ELIXIR_DIR" "$ELIXIR_SHA256"
fi
build_source python "$PYTHON_URL" "$PYTHON_SHA256" "$TOOLS/mise/installs/python/$PYTHON_VERSION" "Python-$PYTHON_VERSION" --with-ensurepip=install --with-system-libmpdec=no
build_source ruby "$RUBY_URL" "$RUBY_SHA256" "$TOOLS/mise/installs/ruby/$RUBY_VERSION" "ruby-$RUBY_VERSION" --disable-install-doc
for gem in BUNDLER_WRITEBOOK BUNDLER_OTHER; do
  url_name="${gem}_URL"; sha_name="${gem}_SHA256"; version_name="${gem}_VERSION"
  fetch "${gem,,}" "${!url_name}" "${!sha_name}"
  if (( DRY )); then action "install Bundler ${!version_name} from verified gem"; else
    if ! "$TOOLS/mise/installs/ruby/$RUBY_VERSION/bin/gem" list --local --exact bundler | grep -q "${!version_name}"; then
      cp "$CACHE/${gem,,}" "$TMP/bundler-${!version_name}.gem"
      "$TOOLS/mise/installs/ruby/$RUBY_VERSION/bin/gem" install --local "$TMP/bundler-${!version_name}.gem" --no-document
    fi
  fi
done

for wheel in PYTEST PLUGGY PYGMENTS PACKAGING INICONFIG; do
  url_name="${wheel}_URL"; sha_name="${wheel}_SHA256"
  fetch "${wheel,,}" "${!url_name}" "${!sha_name}"
done
PYTHON_KIT="$ROOT/toolchains/python-$PYTHON_VERSION"
if (( DRY )); then action "install SHA-verified pytest wheels -> $PYTHON_KIT"; elif ! ready "$PYTHON_KIT" "$PYTEST_SHA256"; then
  reset_partial "$PYTHON_KIT" "$PYTEST_SHA256"
  mkdir -p "$PYTHON_KIT/bin" "$PYTHON_KIT/lib/python3.14/site-packages"
  begin_install "$PYTHON_KIT"
  ln -s "$TOOLS/mise/installs/python/$PYTHON_VERSION/bin/python3" "$PYTHON_KIT/bin/python3"
  cp "$CACHE/pytest" "$TMP/pytest-9.0.2-py3-none-any.whl"
  cp "$CACHE/pluggy" "$TMP/pluggy-1.6.0-py3-none-any.whl"
  cp "$CACHE/pygments" "$TMP/pygments-2.21.0-py3-none-any.whl"
  cp "$CACHE/packaging" "$TMP/packaging-26.3-py3-none-any.whl"
  cp "$CACHE/iniconfig" "$TMP/iniconfig-2.3.0-py3-none-any.whl"
  "$PYTHON_KIT/bin/python3" -m pip install --no-index --no-deps --target "$PYTHON_KIT/lib/python3.14/site-packages" \
    "$TMP/pytest-9.0.2-py3-none-any.whl" "$TMP/pluggy-1.6.0-py3-none-any.whl" \
    "$TMP/pygments-2.21.0-py3-none-any.whl" "$TMP/packaging-26.3-py3-none-any.whl" "$TMP/iniconfig-2.3.0-py3-none-any.whl"
  cat > "$PYTHON_KIT/bin/pytest" <<EOF
#!/bin/sh
export PYTHONPATH="$PYTHON_KIT/lib/python3.14/site-packages"
exec "$PYTHON_KIT/bin/python3" -m pytest "\$@"
EOF
  chmod 0755 "$PYTHON_KIT/bin/pytest"
  mark "$PYTHON_KIT" "$PYTEST_SHA256"
fi
for item in "rust-$RUST_VERSION:$RUST_DIR" "elixir-1.20.2-otp29:$ELIXIR_DIR"; do
  name=${item%%:*}; target=${item#*:}
  if (( DRY )); then action "link $ROOT/toolchains/$name/bin -> $target/bin"; else
    mkdir -p "$ROOT/toolchains/$name"
    ln -sfnT "$target/bin" "$ROOT/toolchains/$name/bin"
  fi
done

# Offline dependency snapshots for the r70 task kits. Each template is rebuilt
# from the lockfiles in reproduce/deps/ (the package managers verify their
# checksums) and is bound to those exact bytes by a .kogen-lock-sha256 marker.
# Graders read these trees through the sandbox's read-only bind of $ROOT.
deps_sha() { (cd "$HERE/deps" && sha256sum "$@") | sha256sum | cut -d' ' -f1; }
lock_ready() { [[ -f $1/.kogen-lock-sha256 && $(cat "$1/.kogen-lock-sha256") == "$2" ]]; }
lock_mark() { chown -R root:root "$1"; chmod -R a+rX,go-w "$1"; printf '%s\n' "$2" > "$1/.kogen-lock-sha256"; chmod 0644 "$1/.kogen-lock-sha256"; }
ERLANG_BIN="$TOOLS/mise/installs/erlang/$ERLANG_VERSION/bin"
ELIXIR_KIT="$ROOT/toolchains/elixir-1.20.2-otp29"
BUN_TEMPLATE="$ROOT/toolchains/bun-$BUN_VERSION/node-template"
GLEAM_PROJECT="$GLEAM_DIR/cache/project"
ELIXIR_DEPS_SHA=$(deps_sha elixir/mix.exs elixir/mix.lock)
ELIXIR_DEPS_SHA=$(printf '%s hex-%s\n' "$ELIXIR_DEPS_SHA" "$HEX_VERSION" | sha256sum | cut -d' ' -f1)
BUN_DEPS_SHA=$(deps_sha bun/package.json bun/bun.lock)
GLEAM_DEPS_SHA=$(deps_sha gleam/gleam.toml gleam/manifest.toml gleam/src/r70_gleam_cache.gleam gleam/test/r70_gleam_cache_test.gleam)

# Rust kits resolve crates offline from a vendored directory source (their
# .cargo/config.toml replaces crates-io with toolchains/rust-*/vendor). The Rust
# and Go module caches only need to exist (read-only in the sandbox).
RUST_VENDOR="$ROOT/toolchains/rust-$RUST_VERSION/vendor"
RUST_DEPS_SHA=$(deps_sha rust/vendor.tsv rust/build_vendor.py)
mkdir_owned 0755 root root "$ROOT/toolchains/rust-$RUST_VERSION/cache"
mkdir_owned 0755 root root "$ROOT/toolchains/rust-$RUST_VERSION/cache/cargo-home"
if (( DRY )); then action "rebuild $RUST_VENDOR from deps/rust/vendor.tsv ($(wc -l < "$HERE/deps/rust/vendor.tsv") crates, each verified against its crates.io SHA-256); marker $RUST_DEPS_SHA"
elif ! lock_ready "$RUST_VENDOR" "$RUST_DEPS_SHA"; then
  "$TOOLS/mise/installs/python/$PYTHON_VERSION/bin/python3" "$HERE/deps/rust/build_vendor.py" "$RUST_VENDOR" "$CACHE/crates"
  lock_mark "$RUST_VENDOR" "$RUST_DEPS_SHA"
fi
mkdir_owned 0755 root root "$GO_DIR/cache"
mkdir_owned 0755 root root "$GO_DIR/cache/gomodcache"

fetch golangci-lint "$GOLANGCI_LINT_URL" "$GOLANGCI_LINT_SHA256"
if (( DRY )); then action "install golangci-lint $GOLANGCI_LINT_VERSION -> $GO_DIR/bin/golangci-lint; verify binary SHA-256 $GOLANGCI_LINT_BINARY_SHA256"
elif [[ ! -x $GO_DIR/bin/golangci-lint || $(sha256sum "$GO_DIR/bin/golangci-lint" | cut -d' ' -f1) != "$GOLANGCI_LINT_BINARY_SHA256" ]]; then
  rm -rf "$TMP/golangci-lint"; mkdir -p "$TMP/golangci-lint"
  tar -xzf "$CACHE/golangci-lint" -C "$TMP/golangci-lint" --strip-components=1 "golangci-lint-$GOLANGCI_LINT_VERSION-linux-amd64/golangci-lint"
  [[ $(sha256sum "$TMP/golangci-lint/golangci-lint" | cut -d' ' -f1) == "$GOLANGCI_LINT_BINARY_SHA256" ]] || { echo 'golangci-lint binary SHA-256 mismatch' >&2; exit 1; }
  install -m 0755 -o root -g root "$TMP/golangci-lint/golangci-lint" "$GO_DIR/bin/golangci-lint"
fi

fetch hex-src "$HEX_SRC_URL" "$HEX_SRC_SHA256"
if (( DRY )); then action "build $ELIXIR_KIT/{mix-home,hex-home,project} from deps/elixir: Hex $HEX_VERSION built from verified source, deps.get --check-locked, deps.compile and Dialyzer PLTs (MIX_ENV=test); marker $ELIXIR_DEPS_SHA"
elif ! lock_ready "$ELIXIR_KIT/project" "$ELIXIR_DEPS_SHA"; then
  rm -rf -- "$ELIXIR_KIT/mix-home" "$ELIXIR_KIT/hex-home" "$ELIXIR_KIT/project"
  mkdir -p "$ELIXIR_KIT/project/lib" "$ELIXIR_KIT/project/test"
  install -m 0644 "$HERE/deps/elixir/mix.exs" "$HERE/deps/elixir/mix.lock" "$ELIXIR_KIT/project/"
  (
    export PATH="$ERLANG_BIN:$ELIXIR_DIR/bin:/usr/bin:/bin" MIX_HOME="$ELIXIR_KIT/mix-home" HEX_HOME="$ELIXIR_KIT/hex-home" MIX_ENV=test
    cd "$ELIXIR_KIT/project"
    # Hex is built from its pinned source tag with this host's OTP; the published
    # prebuilt archives target older OTP releases and do not load on OTP 29.
    rm -rf "$TMP/hex-src"; mkdir -p "$TMP/hex-src"
    tar -xzf "$CACHE/hex-src" -C "$TMP/hex-src" --strip-components=1
    (cd "$TMP/hex-src" && MIX_ENV=prod mix archive.build -o "$TMP/hex-$HEX_VERSION.ez")
    mix archive.install "$TMP/hex-$HEX_VERSION.ez" --force
    mix deps.get --check-locked
    mix deps.compile
    mix dialyzer --plt
  )
  lock_mark "$ELIXIR_KIT/mix-home" "$ELIXIR_DEPS_SHA"
  lock_mark "$ELIXIR_KIT/hex-home" "$ELIXIR_DEPS_SHA"
  lock_mark "$ELIXIR_KIT/project" "$ELIXIR_DEPS_SHA"
fi

if (( DRY )); then action "build $BUN_TEMPLATE from deps/bun with bun install --frozen-lockfile; marker $BUN_DEPS_SHA"
elif ! lock_ready "$BUN_TEMPLATE" "$BUN_DEPS_SHA"; then
  rm -rf -- "$BUN_TEMPLATE" "$TMP/bun-cache"; mkdir -p "$BUN_TEMPLATE"
  install -m 0644 "$HERE/deps/bun/package.json" "$HERE/deps/bun/bun.lock" "$BUN_TEMPLATE/"
  ( cd "$BUN_TEMPLATE" && BUN_INSTALL_CACHE_DIR="$TMP/bun-cache" "$ROOT/toolchains/bun-$BUN_VERSION/bin/bun" install --frozen-lockfile )
  lock_mark "$BUN_TEMPLATE" "$BUN_DEPS_SHA"
fi

if (( DRY )); then action "build $GLEAM_PROJECT from deps/gleam with gleam deps download and gleam build; marker $GLEAM_DEPS_SHA"
elif ! lock_ready "$GLEAM_PROJECT" "$GLEAM_DEPS_SHA"; then
  rm -rf -- "$GLEAM_PROJECT" "$TMP/gleam-home"; mkdir -p "$GLEAM_PROJECT" "$TMP/gleam-home"
  cp -R "$HERE/deps/gleam/." "$GLEAM_PROJECT/"
  ( cd "$GLEAM_PROJECT" && export PATH="$ERLANG_BIN:$GLEAM_DIR/bin:/usr/bin:/bin" HOME="$TMP/gleam-home" XDG_CACHE_HOME="$TMP/gleam-home/.cache" && gleam deps download && gleam build )
  cmp -s "$HERE/deps/gleam/manifest.toml" "$GLEAM_PROJECT/manifest.toml" || { echo 'gleam changed the locked manifest' >&2; exit 1; }
  lock_mark "$GLEAM_DIR/cache" "$GLEAM_DEPS_SHA"
  printf '%s\n' "$GLEAM_DEPS_SHA" > "$GLEAM_PROJECT/.kogen-lock-sha256"
fi

fetch codex "$CODEX_URL" "$CODEX_SHA256"
CODEX_DIR="$TOOLS/tools/codex-$CODEX_VERSION"
CODEX_VENDOR="$CODEX_DIR/vendor/$CODEX_TARGET/bin"
if (( DRY )); then action "verify npm SRI $CODEX_NPM_INTEGRITY; install complete Codex vendor directory and verify binary $CODEX_BINARY_SHA256 -> $CODEX_DIR"; elif ! ready "$CODEX_DIR" "$CODEX_SHA256"; then
  reset_partial "$CODEX_DIR" "$CODEX_SHA256"; mkdir -p "$CODEX_DIR"
  begin_install "$CODEX_DIR"
  npm_integrity="sha512-$(openssl dgst -sha512 -binary "$CACHE/codex" | openssl base64 -A)"
  [[ $npm_integrity == "$CODEX_NPM_INTEGRITY" ]] || { echo 'Codex npm integrity mismatch' >&2; exit 1; }
  tar -xf "$CACHE/codex" -C "$CODEX_DIR" --strip-components=1 "package/vendor/$CODEX_TARGET"
  for vendor_file in codex codex-code-mode-host; do
    [[ -x $CODEX_VENDOR/$vendor_file ]] || { echo "Missing Codex vendor executable: $vendor_file" >&2; exit 1; }
  done
  [[ -x $CODEX_DIR/vendor/$CODEX_TARGET/codex-path/rg ]] || { echo 'Missing Codex vendor path search executable' >&2; exit 1; }
  [[ -d $CODEX_DIR/vendor/$CODEX_TARGET/codex-resources ]] || { echo 'Missing Codex vendor resources directory' >&2; exit 1; }
  [[ $(sha256sum "$CODEX_VENDOR/codex" | cut -d' ' -f1) == "$CODEX_BINARY_SHA256" ]] || { echo 'Codex binary SHA-256 mismatch' >&2; exit 1; }
  ln -s "vendor/$CODEX_TARGET/bin/codex" "$CODEX_DIR/codex"
  mark "$CODEX_DIR" "$CODEX_SHA256"
fi
run ln -sfn "$CODEX_DIR/codex" "$TOOLS/tools/bin/codex"
run ln -sfn "$CODEX_VENDOR/codex-code-mode-host" "$TOOLS/tools/bin/codex-code-mode-host"

action "Write $TOOLS/mise/config.toml (Elixir $ELIXIR_VERSION, Erlang $ERLANG_VERSION, Node $NODE_VERSION, Python $PYTHON_VERSION, Ruby $RUBY_VERSION)"
action "Write /etc/sysctl.d/90-kogen-bench.conf (user namespaces on, max $USER_MAX_USER_NAMESPACES, ptrace scope 1, swappiness 10) and apply it"
action 'Write /etc/systemd/system/bench.slice (CPU 180%, memory high 5G/max 6G, swap max 2G, tasks 4096) and daemon-reload'
action 'Write /etc/apparmor.d/bwrap (unconfined, userns) and load it: Ubuntu 24.04 restricts unprivileged user namespaces'
action 'Enable and start fail2ban.service'
if (( ! DRY )); then
  cat > "$TOOLS/mise/config.toml" <<EOF
[tools]
elixir = "$ELIXIR_VERSION"
erlang = "$ERLANG_VERSION"
node = "$NODE_VERSION"
python = "$PYTHON_VERSION"
ruby = "$RUBY_VERSION"
EOF
  cat > /etc/sysctl.d/90-kogen-bench.conf <<EOF
kernel.unprivileged_userns_clone=1
user.max_user_namespaces=$USER_MAX_USER_NAMESPACES
kernel.yama.ptrace_scope=1
vm.swappiness=10
EOF
  sysctl -p /etc/sysctl.d/90-kogen-bench.conf
  cat > /etc/systemd/system/bench.slice <<'EOF'
[Unit]
Description=Benchmark contestant jobs
[Slice]
CPUAccounting=yes
MemoryAccounting=yes
TasksAccounting=yes
CPUQuota=180%
MemoryHigh=5G
MemoryMax=6G
MemorySwapMax=2G
TasksMax=4096
EOF
  systemctl daemon-reload
  printf 'profile bwrap /usr/bin/bwrap flags=(unconfined) {\n  userns,\n}\n' > /etc/apparmor.d/bwrap
  apparmor_parser -r /etc/apparmor.d/bwrap
  systemctl enable --now fail2ban.service
fi

RELEASE=$(git -c "safe.directory=$REPO" -C "$REPO" rev-parse --verify HEAD)
action "Verify tasks/_bases/MANIFEST.sha256 and install immutable tasks, grader, lane runner, sandbox profile under $ROOT/kits/$RELEASE"
action 'Point /srv/bh/bench/kits/current at this release and link bench-disk-floor, bench-run-lane, bench-run-controls, bench-doctor into /usr/local/bin'
action 'Install narrow benchadmin sudo access for bench-run-lane, bench-run-controls, and bench-doctor'
if (( ! DRY )); then
  KIT="$ROOT/kits/$RELEASE"
  if [[ ! -f $KIT/.complete ]]; then
    mkdir -p "$KIT/tasks" "$KIT/reproduce"
    rsync -a "$REPO/tasks/" "$KIT/tasks/"
    rsync -a --include='*.sh' --include='*.py' --include='host-pins.lock' --include='deps/***' --exclude='*' "$HERE/" "$KIT/reproduce/"
    ( cd "$KIT/tasks/_bases" && sha256sum -c MANIFEST.sha256 >/dev/null )
    find "$KIT/tasks" -type d \( -name hidden -o -name grader \) -prune -exec chmod 0700 {} +
    find "$KIT/tasks" -type f -path '*/hidden/*' -exec chmod go-rwx {} +
    chown -R root:root "$KIT"
    touch "$KIT/.complete"
  fi
  ln -sfnT "$KIT" "$ROOT/kits/current"
  ln -sfnT "$ROOT/kits/current/reproduce/disk-floor.sh" /usr/local/bin/bench-disk-floor
  ln -sfnT "$ROOT/kits/current/reproduce/run-lane.sh" /usr/local/bin/bench-run-lane
  ln -sfnT "$ROOT/kits/current/reproduce/run-controls.sh" /usr/local/bin/bench-run-controls
  ln -sfnT "$ROOT/kits/current/reproduce/doctor.sh" /usr/local/bin/bench-doctor
  cat > /etc/sudoers.d/90-kogen-benchadmin <<'EOF'
benchadmin ALL=(root) NOPASSWD: /usr/local/bin/bench-run-lane, /usr/local/bin/bench-run-controls, /usr/local/bin/bench-doctor
EOF
  chmod 0440 /etc/sudoers.d/90-kogen-benchadmin
  visudo -cf /etc/sudoers.d/90-kogen-benchadmin
fi
action 'Run model-free doctor'
if (( ! DRY )); then "$HERE/doctor.sh"; fi
say 'Manual login: run codex login --device-auth as the bench user.'
