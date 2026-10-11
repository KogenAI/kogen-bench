# Supervisor installs native pinned Bun/Node/Codex; no credentials inspected here.
export PATH=${RACE6_LINUX_PATH:-${HOME}/.local/bin:/usr/local/bin:/usr/bin:/bin}
export LANG=C.UTF-8 LC_ALL=C.UTF-8
export CARGO_BUILD_JOBS=2 GOMAXPROCS=2 GOFLAGS=-p=2
export ERL_FLAGS='+S 2:2 +SDcpu 2:2' ELIXIR_ERL_OPTIONS='+S 2:2'
export UV_THREADPOOL_SIZE=2 RAYON_NUM_THREADS=2
