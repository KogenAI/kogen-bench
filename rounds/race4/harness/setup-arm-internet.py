#!/usr/bin/env python3
"""Adapt copied kit aids and AGENTS.md; never modify the kit."""
from pathlib import Path
import re
import shlex
import sys

arm, kit = map(Path, sys.argv[1:])
env = (kit / 'env-aids.sh').read_text()
env = env.replace('all writable caches stay in the kit', 'all writable caches stay in this arm')
env = re.sub(r'if \[ -n "\$\{BASH_SOURCE:-\}" \]; then\n.*?\nfi\n', '', env, count=1, flags=re.S)
env = env.replace('$RACE3_KIT/cache/', '${RACE4_ARM_ROOT}/.kitcache/')
env = env.replace('$RACE3_KIT/logs/erl_crash.dump', '${RACE4_ARM_ROOT}/.kitcache/tmp/erl_crash.dump')
env = '\n'.join(line for line in env.splitlines()
                if not line.startswith(('export CARGO_NET_OFFLINE=', 'export GOPROXY=', 'export GOFLAGS=')))
header = '''# Private build caches; runtime dependencies belong in snapshot build output.
if [ -n "${BASH_SOURCE:-}" ]; then
  export RACE4_ARM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  export RACE4_ARM_ROOT="$(cd "$(dirname "${(%):-%x}")" && pwd)"
fi
'''
tail = '''
unset CARGO_NET_OFFLINE HEX_OFFLINE npm_config_offline NPM_CONFIG_OFFLINE BUN_INSTALL_OFFLINE BUN_CONFIG_OFFLINE
export GOPROXY=https://proxy.golang.org,direct GOSUMDB=sum.golang.org GOFLAGS=-p=2
export MIX_ENV=test NO_COLOR=1 CARGO_TERM_COLOR=never CARGO_TERM_PROGRESS_WHEN=never

# Drop only inherited scorer proxies; preserve ordinary host proxy configuration.
for race4_proxy_name in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy; do
  eval 'race4_proxy_value=${'"$race4_proxy_name"'-}'
  if [ "$race4_proxy_value" = http://localhost:9 ]; then unset "$race4_proxy_name"; fi
done
unset race4_proxy_name race4_proxy_value
mkdir -p "$CARGO_HOME" "$GOPATH" "$GOMODCACHE" "$GOCACHE" "$MIX_HOME" "$HEX_HOME" "$BUN_INSTALL_CACHE_DIR" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$npm_config_cache" "$TEST_TELEMETRY_DIR" "$GOPLSCACHE" "$GOLANGCI_LINT_CACHE" "$BUN_RUNTIME_TRANSPILER_CACHE_PATH" "$TMPDIR"
'''
(arm / '.kit-env.sh').write_text(header + 'export RACE3_KIT=' + shlex.quote(str(kit)) + '\n' + env + '\n' + tail)
agents = (arm / 'AGENTS.md').read_text()
agents = re.sub(r'\. "[^"\n]+/env-aids\.sh"', '. ./.kit-env.sh', agents)
agents = re.sub(r'^## Offline rules\n.*?(?=^## |\Z)', '', agents, flags=re.M | re.S)
agents = agents.replace(' --offline', '')
agents = agents.replace('Its online installation examples are reference material; use this kit’s offline commands and pins.',
                        'Online installation examples and documentation may be used; start from the supplied toolchain and libraries.')
agents += '''
## Race 4 internet and scoring policy

This section supersedes inherited kit restrictions on fetching, offline resolution,
and changing dependency pins. You may install packages with your ecosystem's
package manager and read documentation on the web, as a developer normally would.
Never call real model providers; the suite uses a local fake.

Source `. ./.kit-env.sh` for private writable caches seeded from the kit. Scoring
runs with NO network: `./kogen` must be prebuilt and fully offline. Vendor or
bundle every runtime dependency inside this repository, using relative paths.
Snapshots include build output but exclude `.kitcache/`; runtime dependencies
must therefore be embedded or copied outside that build cache before scoring.
'''
(arm / 'AGENTS.md').write_text(agents)
