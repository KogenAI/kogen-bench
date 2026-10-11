# env-studio.sh — race 3 pinned toolchains (Studio, mise installs, no shims) + equal per-arm CPU caps (2 cores)
I=$HOME/.local/share/mise/installs
export PATH=$I/node/24.21.0/bin:$I/go/1.27.1/bin:$I/bun/1.4.2/bin:$I/elixir/1.20.4-otp-29/bin:$I/erlang/29.1.1/bin:$I/gleam/1.19.1/bin:$I/gleam/1.19.1:$HOME/.cargo/bin:/usr/bin:/bin:/usr/sbin:/opt/homebrew/bin
export GOTOOLCHAIN=local RUSTUP_TOOLCHAIN=1.97.1
export LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export CARGO_BUILD_JOBS=2 GOMAXPROCS=2 GOFLAGS=-p=2 ERL_FLAGS="+S 2:2 +SDcpu 2:2" ELIXIR_ERL_OPTIONS="+S 2:2" UV_THREADPOOL_SIZE=2 RAYON_NUM_THREADS=2

# Apply the benchmark's declared mode after toolchain and CPU caps.
if [ -n "${BASH_SOURCE:-}" ]; then
  race5_env_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  race5_env_root="$(cd "$(dirname "${(%):-%x}")" && pwd)"
fi
source "$race5_env_root/mode-env.sh" "$race5_env_root" || return $?
unset race5_env_root
