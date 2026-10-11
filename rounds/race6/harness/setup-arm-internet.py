#!/usr/bin/env python3
"""Adapt copied kit aids and AGENTS.md; never modify the kit."""
from pathlib import Path
import re
import shlex
import sys
from condition import condition
from mode_policy import read_mode, POLICY, DENYLIST_RULE

arm, kit = map(Path, sys.argv[1:3])
py_kit = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
mode = read_mode(arm.parent)
env = (kit / 'env-aids.sh').read_text()
env = env.replace('all writable caches stay in the kit', 'all writable caches stay in this arm')
env = re.sub(r'if \[ -n "\$\{BASH_SOURCE:-\}" \]; then\n.*?\nfi\n', '', env, count=1, flags=re.S)
env = env.replace('$RACE3_KIT/cache/', '${RACE4_ARM_ROOT}/.kitcache/')
env = env.replace('$RACE3_KIT/logs/erl_crash.dump', '${RACE4_ARM_ROOT}/.kitcache/tmp/erl_crash.dump')
if mode == 'real-workflow':
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
source "$RACE4_ARM_ROOT/../mode-env.sh" "$RACE4_ARM_ROOT/.." || return $?
[ "$RACE_MODE" = "$RACE_ARM_MODE" ] || { echo 'arm setup MODE mismatch; rerun setup-arms.sh' >&2; return 2; }
export GIT_CONFIG_GLOBAL="$RACE4_ARM_ROOT/.gitconfig-global"
export MIX_ENV=test NO_COLOR=1 CARGO_TERM_COLOR=never CARGO_TERM_PROGRESS_WHEN=never
mkdir -p "$CARGO_HOME" "$GOPATH" "$GOMODCACHE" "$GOCACHE" "$MIX_HOME" "$HEX_HOME" "$BUN_INSTALL_CACHE_DIR" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$npm_config_cache" "$TEST_TELEMETRY_DIR" "$GOPLSCACHE" "$GOLANGCI_LINT_CACHE" "$BUN_RUNTIME_TRANSPILER_CACHE_PATH" "$TMPDIR"
'''
if py_kit is not None:
    tail += '\nexport RACE5_PY_CACHE_ROOT="$RACE4_ARM_ROOT/.kitcache/py"\n'
    tail += 'race5_common_path=$PATH\nsource ' + shlex.quote(str(py_kit / 'env-py.sh')) + ' || return $?\n'
    tail += 'export PATH="$PATH:$race5_common_path"\nunset race5_common_path\n'
    tail += 'source "$RACE4_ARM_ROOT/../mode-env.sh" "$RACE4_ARM_ROOT/.." || return $?\n'
# Only B and D have the pinned CLI on PATH. Base env.sh deliberately has no Quint.
quint = Path(__import__('os').environ.get('RACE6_KIT_DIR', str(arm.parent.parent/'race6-kit'))) / 'quint'
if condition(arm.name) in ('b','d'):
    tail += '\nexport PATH=' + shlex.quote(str(quint)) + ':"$PATH"\n'
(arm / '.kit-env.sh').write_text(header + 'export RACE_ARM_MODE=' + shlex.quote(mode)
                               + '\nexport RACE3_KIT=' + shlex.quote(str(kit)) + '\n' + env + '\n' + tail)
agents = (arm / 'AGENTS.md').read_text()
agents = re.sub(r'\. "[^"\n]+/env-aids\.sh"', '. ./.kit-env.sh', agents)
if py_kit is not None:
    agents = re.sub(r'\. "[^"\n]+/env-py\.sh"', '. ./.kit-env.sh', agents)
if mode == 'real-workflow':
    agents = re.sub(r'^## Offline rules\n.*?(?=^## |\Z)', '', agents, flags=re.M | re.S)
    agents = agents.replace(' --offline', '')
    agents = agents.replace('Its online installation examples are reference material; use this kit’s offline commands and pins.',
                            'Online installation examples and documentation may be used; start from the supplied toolchain and libraries.')
agents += '\n## Race 6 mode and scoring policy\n\nMODE: ' + mode + '\n\n' + POLICY[mode] + '\n\n' + DENYLIST_RULE + '''

Source `. ./.kit-env.sh` for private writable caches seeded from the kit. Scoring
runs with NO network: `./kogen` must be prebuilt and fully offline. Vendor or
bundle every runtime dependency inside this repository, using relative paths.
Snapshots include build output but exclude `.kitcache/`; runtime dependencies
must therefore be embedded or copied outside that build cache before scoring.
'''
(arm / 'AGENTS.md').write_text(agents)
