# Source with the harness root as $1. Invalid/missing MODE fails closed.
race5_mode_root=${1:?mode-env.sh requires the harness root}
if [ ! -f "$race5_mode_root/MODE" ]; then
  echo 'MODE file is required' >&2; return 2
fi
RACE_MODE=$(cat "$race5_mode_root/MODE")
case "$RACE_MODE" in
  sealed)
    export UV_OFFLINE=1
    export CARGO_NET_OFFLINE=true HEX_OFFLINE=1 npm_config_offline=true NPM_CONFIG_OFFLINE=true
    export BUN_INSTALL_OFFLINE=1 BUN_CONFIG_OFFLINE=1
    export GOPROXY=off GOSUMDB=off GOFLAGS='-p=2 -mod=readonly'
    export CODEX_WEB_SEARCH=disabled RACE_NETWORK_ACCESS=false
    ;;
  real-workflow)
    unset UV_OFFLINE CARGO_NET_OFFLINE HEX_OFFLINE npm_config_offline NPM_CONFIG_OFFLINE BUN_INSTALL_OFFLINE BUN_CONFIG_OFFLINE
    export GOPROXY=https://proxy.golang.org,direct GOSUMDB=sum.golang.org GOFLAGS=-p=2
    export CODEX_WEB_SEARCH=live RACE_NETWORK_ACCESS=true
    ;;
  *) echo 'MODE must be sealed or real-workflow' >&2; return 2 ;;
esac
# The Codex client's own model transport must work in either mode. SEALED shell
# networking is disabled separately by its Codex sandbox flag.
for race5_proxy_name in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy; do
  eval 'race5_proxy_value=${'"$race5_proxy_name"'-}'
  if [ "$race5_proxy_value" = http://localhost:9 ]; then unset "$race5_proxy_name"; fi
done
unset race5_proxy_name race5_proxy_value
export RACE_MODE
unset race5_mode_root
