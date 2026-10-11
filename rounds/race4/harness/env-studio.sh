# env-studio.sh — race 3 pinned toolchains (Studio, mise installs, no shims) + equal per-arm CPU caps (2 cores)
I=$HOME/.local/share/mise/installs
export PATH=$I/node/24.21.0/bin:$I/go/1.27.1/bin:$I/bun/1.4.2/bin:$I/elixir/1.20.4-otp-29/bin:$I/erlang/29.1.1/bin:$I/gleam/1.19.1/bin:$I/gleam/1.19.1:$HOME/.cargo/bin:/usr/bin:/bin:/usr/sbin:/opt/homebrew/bin
export GOTOOLCHAIN=local RUSTUP_TOOLCHAIN=1.97.1
export LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export CARGO_BUILD_JOBS=2 GOMAXPROCS=2 GOFLAGS=-p=2 ERL_FLAGS="+S 2:2 +SDcpu 2:2" ELIXIR_ERL_OPTIONS="+S 2:2" UV_THREADPOOL_SIZE=2 RAYON_NUM_THREADS=2

# Agent shells may fetch packages and read web documentation. Arm setup supplies
# private repository caches; never inherit a scorer's offline switches.
unset CARGO_NET_OFFLINE HEX_OFFLINE npm_config_offline NPM_CONFIG_OFFLINE BUN_INSTALL_OFFLINE BUN_CONFIG_OFFLINE
export GOPROXY=https://proxy.golang.org,direct GOSUMDB=sum.golang.org GOFLAGS=-p=2

# Drop only inherited scorer proxies; preserve ordinary host proxy configuration.
for race4_proxy_name in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy; do
  eval 'race4_proxy_value=${'"$race4_proxy_name"'-}'
  if [ "$race4_proxy_value" = http://localhost:9 ]; then unset "$race4_proxy_name"; fi
done
unset race4_proxy_name race4_proxy_value
