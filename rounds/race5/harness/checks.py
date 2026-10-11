#!/usr/bin/python3
import difflib
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys
import platform
from importlib import import_module
from pathlib import Path
from validity import codex_home, tree_hash
from scoring_config import counts, scored_ids
from mode_policy import read_mode, brief_template, DENYLIST_RULE

R = Path(__file__).resolve().parent
KIT = Path(os.environ.get('RACE3_KIT_DIR', str(Path.home() / 'retained-run' / 'race3-kit'))).resolve()
NAMES = {'rust': 'Rust', 'go': 'Go', 'ts': 'TypeScript on Bun',
         'ex': 'Elixir', 'py': 'Python'}

CACHE_VARS = ('CARGO_HOME', 'GOPATH', 'GOMODCACHE', 'GOCACHE', 'MIX_HOME',
              'HEX_HOME', 'BUN_INSTALL_CACHE_DIR', 'XDG_CACHE_HOME', 'npm_config_cache')
GIT_PREFIXES = ('https://github.com/KogenAI/', 'http://github.com/KogenAI/',
                'git@github.com:KogenAI/', 'ssh://git@github.com/KogenAI/')
OFFLINE = {'UV_OFFLINE': '1', 'CARGO_NET_OFFLINE': 'true', 'HEX_OFFLINE': '1', 'npm_config_offline': 'true',
           'NPM_CONFIG_OFFLINE': 'true', 'BUN_INSTALL_OFFLINE': '1', 'BUN_CONFIG_OFFLINE': '1'}


def disk_admission(root, arms, env=None, free_bytes=None, host=None):
    """Portable admission on every host, using conservative race 4 measurements."""
    root = Path(root)
    env = os.environ if env is None else env
    if not arms or len(arms) != len(set(arms)) or not set(arms) <= set(NAMES):
        raise ValueError('ARMS must contain unique registered race 5 languages')
    host = host or platform.system()
    if host == 'Linux' and (len(arms) != 1 or arms[0] not in ('rust', 'go')):
        raise ValueError('Linux hosts run one Rust or Go arm only')
    defaults = json.loads((root / 'DISK-DEFAULTS.json').read_text())
    def positive(key, fallback):
        value = int(env.get(key, fallback))
        if value <= 0:
            raise ValueError(f'{key} must be a positive integer')
        return value
    prefix = 'linux_' if host == 'Linux' else ''
    working = positive('RACE_PER_ARM_WORKING_BYTES', defaults.get(prefix+'per_arm_working_bytes', defaults['per_arm_working_bytes']))
    snapshot = positive('RACE_SNAPSHOT_BYTES_PER_ARM', defaults.get(prefix+'snapshot_bytes_per_arm', defaults['snapshot_bytes_per_arm']))
    cap = positive('RACE_CAP_MIN', 180)
    interval = positive('RACE_SNAPSHOT_MIN', 5)
    snapshots = 5 if host == 'Linux' else (cap + interval - 1) // interval + 1
    base = len(arms) * (working + snapshots * snapshot)
    required = (base * 13 + 9) // 10  # ceil(base * 1.30), physical-estimate margin
    free = shutil.disk_usage(root).free if free_bytes is None else free_bytes
    print(f'disk admission: free={free} required={required} bytes; arms={len(arms)} '
          f"working/arm={working} snapshots={snapshots} snapshot/arm={snapshot} margin=30% accounting={defaults.get('accounting', 'fixture')} host={host}")
    return free >= required


def mode_environment(env, mode, root=None):
    if env.get('RACE_MODE') != mode:
        raise ValueError('environment MODE differs from MODE file')
    if env.get('CODEX_WEB_SEARCH') != ('live' if mode == 'real-workflow' else 'disabled'):
        raise ValueError('web search environment differs from MODE')
    if env.get('RACE_NETWORK_ACCESS') != ('true' if mode == 'real-workflow' else 'false'):
        raise ValueError('sandbox network environment differs from MODE')
    if mode == 'sealed':
        for key, value in OFFLINE.items():
            if env.get(key) != value:
                raise ValueError(f'SEALED requires {key}={value}')
        if env.get('GOPROXY') != 'off' or env.get('GOSUMDB') != 'off' or '-mod=readonly' not in env.get('GOFLAGS', ''):
            raise ValueError('SEALED Go environment must be offline')
    else:
        for key in OFFLINE:
            if key in env:
                raise ValueError(f'REAL-WORKFLOW retains offline switch {key}')
        if env.get('GOPROXY') != 'https://proxy.golang.org,direct' or env.get('GOSUMDB') != 'sum.golang.org' or '-mod=' in env.get('GOFLAGS', ''):
            raise ValueError('REAL-WORKFLOW Go environment must allow normal fetching')
        for key in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy'):
            if env.get(key) == 'http://localhost:9':
                raise ValueError(f'REAL-WORKFLOW retains scorer proxy {key}')
    if root is not None:
        root = Path(root).resolve()
        if env.get('RACE_ARM_MODE') != mode:
            raise ValueError('arm setup MODE differs from MODE file')
        for key in CACHE_VARS:
            cache = Path(env.get(key, '/missing')).resolve()
            if root not in cache.parents or not cache.is_dir():
                raise ValueError(f'{key} must be a private directory inside {root}')
            with tempfile.TemporaryFile(dir=cache) as probe:
                probe.write(b'private cache write probe')
        if root.name == 'py':
            for key in ('UV_CACHE_DIR', 'MYPY_CACHE_DIR', 'RUFF_CACHE_DIR', 'RACE5_PY_CACHE_ROOT'):
                cache = Path(env.get(key, '/missing')).resolve()
                if root not in cache.parents or not cache.is_dir():
                    raise ValueError(f'{key} must be a private Python cache inside the arm')
                with tempfile.TemporaryFile(dir=cache) as probe:
                    probe.write(b'private Python cache probe')
            if env.get('UV_PYTHON_DOWNLOADS') != 'never' or env.get('UV_LINK_MODE') != 'copy':
                raise ValueError('Python must use supplied interpreter and copied venv dependencies')
            for key in ('UV_CONCURRENT_BUILDS', 'UV_CONCURRENT_INSTALLS', 'UV_CONCURRENT_DOWNLOADS',
                        'RAYON_NUM_THREADS', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                        'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
                if env.get(key) != '2':
                    raise ValueError(f'Python requires {key}=2')
            py_kit = Path(env.get('RACE5_PY_KIT', '/missing')).resolve()
            if not (py_kit/'templates/py').is_dir() or not Path(env.get('UV_PYTHON_INSTALL_DIR', '/missing')).is_dir():
                raise ValueError('Python kit/toolchain pending')
        config = Path(env.get('GIT_CONFIG_GLOBAL', '/missing')).resolve()
        if config != root / '.gitconfig-global' or not config.is_file():
            raise ValueError('GIT_CONFIG_GLOBAL must be the private arm config')
        for scope in (['--file', str(config)], ['--local']):
            prefixes = subprocess.check_output(['git', 'config', *scope, '--get-all',
                                               'url.https://invalid.invalid/blocked/.insteadOf'],
                                              cwd=root, text=True).splitlines()
            if set(prefixes) != set(GIT_PREFIXES):
                raise ValueError('arm git Kogen denylist differs from policy')
        agents = (root / 'AGENTS.md').read_text()
        if f'MODE: {mode}' not in agents or DENYLIST_RULE not in agents:
            raise ValueError('arm AGENTS.md differs from MODE or denylist')
    return True


def internet_environment(env, root):
    """Require private writable caches and fetching enabled in an agent shell."""
    root = Path(root).resolve()
    for name in CACHE_VARS:
        cache = Path(env.get(name, '/missing')).resolve()
        if root not in cache.parents or not cache.is_dir():
            raise ValueError(f'{name} must be a directory inside {root}: {cache}')
        with tempfile.TemporaryFile(dir=cache) as probe:
            probe.write(b'private cache write probe')
    for name in ('CARGO_NET_OFFLINE', 'HEX_OFFLINE', 'npm_config_offline',
                 'NPM_CONFIG_OFFLINE', 'BUN_INSTALL_OFFLINE', 'BUN_CONFIG_OFFLINE'):
        if name in env:
            raise ValueError(f'agent environment retains {name}')
    if env.get('GOPROXY') != 'https://proxy.golang.org,direct' or '-mod=' in env.get('GOFLAGS', ''):
        raise ValueError('agent Go environment must allow normal module fetching')
    for name in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy'):
        if env.get(name) == 'http://localhost:9':
            raise ValueError(f'agent environment retains scorer proxy {name}')
    return True


def diff(want, got, left, right):
    print(''.join(difflib.unified_diff(want.splitlines(True), got.splitlines(True),
                                       fromfile=left, tofile=right)), end='')
    return want == got


def normalise_env(env, arm):
    # Preserve variable names, flags, and PATH order. Only known path roots and
    # shell bookkeeping vary; arbitrary variables (including caps) stay checked.
    result = {}
    for key, value in env.items():
        if key in ('_', 'SHLVL', 'OLDPWD'):
            continue
        value = value.replace(str(R / arm), '<ARM>').replace(str(KIT), '<KIT>')
        value = re.sub(r'/Users/[^/]+/\.local/share/mise/installs/([^/]+)/[^/:]+',
                       r'<TOOLCHAIN>/\1', value)
        result[key] = value
    return ''.join('%s=%s\n' % item for item in sorted(result.items()))


def run():
    failed = []
    def check(name, fn):
        try:
            ok = fn()
        except Exception as e:
            print(str(e)); ok = False
        print(('PASS ' if ok else 'FAIL ') + name)
        if not ok:
            failed.append(name)

    arms = (R / 'ARMS').read_text().split()
    check('disk-admission', lambda: disk_admission(R, arms))
    if '--disk-only' in sys.argv:
        return bool(failed)
    if 'py' in arms:
        check('Python-Mac-only', lambda: platform.system() == 'Darwin')
        check('python-kit', lambda: import_module('py-kit').check(R))
    check('MODE', lambda: read_mode(R) in ('sealed', 'real-workflow'))
    if 'MODE' in failed:
        return True
    mode = read_mode(R)
    def briefs():
        template = brief_template(R)
        values, _ = counts(R)
        template = template.replace('{TARGET}', str(values['target'])).replace('{N}', str(values['N_scored']))
        ok = True
        for arm, name in NAMES.items():
            # Replace only placeholder positions. A global replacement could
            # conceal edits to unrelated mentions of the language/arm name.
            pattern = re.escape(template).replace('LANGNAME', re.escape(name)).replace('LANGID', re.escape(arm))
            text = (R / ('BRIEF-%s.md' % arm)).read_text()
            expected = template.replace('LANGNAME', name).replace('LANGID', arm)
            if not re.fullmatch(pattern, text):
                normal = text.replace(name, 'LANGNAME').replace('/tmp/kc-' + arm, '/tmp/kc-LANGID')
                diff(template, normal, 'BRIEF.tmpl', 'BRIEF-%s.md (normalised)' % arm)
                ok = False
        return ok
    check('briefs', briefs)
    def mode_env():
        command = 'set -e; source "$1/env.sh"; exec /usr/bin/python3 -c "import json,os;print(json.dumps(dict(os.environ)))"'
        env = json.loads(subprocess.check_output(['/bin/bash', '-c', command, 'checks', str(R)], text=True))
        return mode_environment(env, mode)
    check('MODE-environment', mode_env)
    # Assembly mode requires no race directory, kit or credential paths.
    if '--assembly' in __import__('sys').argv or not any((R / arm).is_dir() for arm in arms):
        check('frozen-inputs', lambda: tree_hash(R / 'inputs', frozen=True) == (R / 'inputs.sha').read_text().strip())
        def assembly_counts():
            values, bugs = counts(R)
            text = (R / 'TARGET.md').read_text()
            listed = re.findall(r'^- (\S+)$', text, re.M)
            return (len(scored_ids(R)) == values['N_scored']
                    and set(listed) == bugs and len(listed) == len(bugs)
                    and f"{values['target']}/{values['N_scored']}" in text)
        check('target-spec-bugs', assembly_counts)
        check('suite-checks', lambda: subprocess.call([__import__('sys').executable, str(R/'suite-checks.py')]) == 0)
        print('SKIP host checks: kit, version, arm environments and auth require a prepared race directory')
        return bool(failed)

    def kit():
        output = subprocess.check_output(['bash', 'kitsum.sh'], cwd=str(R), text=True,
                                         env=dict(os.environ, RACE_KIT_MANIFEST=str(R/'out/kit-manifest.sha256')))
        match = re.search(r'\bhash ([0-9a-fA-F]{64})\b', output)
        if match is None:
            raise ValueError('kitsum.sh did not print a valid hash: ' + output.strip())
        sha = match.group(1).lower()
        if (R / 'out').is_dir():
            (R / 'out/kit.sha256').write_text(sha + '\n')
        print('kit sha256:', sha)
        pin = R / 'KIT-SHA256'
        return not pin.exists() or pin.read_text().strip() == sha
    check('kit', kit)
    def inputs():
        sha = tree_hash(R / 'inputs', frozen=True); print('inputs sha:', sha)
        return sha == (R / 'inputs.sha').read_text().strip()
    check('frozen-inputs', inputs)

    def version():
        got = subprocess.check_output(['/bin/bash', '-c', 'source "$1/env.sh"; codex --version',
                                       'checks', str(R)], cwd=str(R), text=True).strip()
        (R / 'out/codex-version.txt').write_text(got + '\n'); print(got)
        pin = R / 'CODEX-VERSION'
        return bool(got) and (not pin.exists() or pin.read_text().strip() == got)
    check('codex-version', version)

    def environments():
        baseline = None; baseline_env = None; python_env = None; ok = bool(arms)
        command = ('set -e; source "$1/env.sh"; source "$1/$2/.kit-env.sh"; '
                   'if [ -s "$1/CODEX_HOME" ]; then export CODEX_HOME=$(cat "$1/CODEX_HOME"); fi; '
                   'cd "$1/$2"; exec /usr/bin/python3 -c "import json,os;print(json.dumps(dict(os.environ)))"')
        for arm in arms:
            env = json.loads(subprocess.check_output(['/bin/bash', '-c', command, 'checks', str(R), arm],
                                                     cwd=str(R), text=True))
            mode_environment(env, mode, R / arm)
            raw = ''.join('%s=%s\n' % item for item in sorted(env.items()))
            (R / ('out/env-%s.txt' % arm)).write_text(raw)
            normal = normalise_env(env, arm)
            (R / ('out/env-%s.normalised.txt' % arm)).write_text(normal)
            if arm == 'py':
                python_env = env
                continue
            if baseline is None:
                baseline = (arm, normal)
                baseline_env = env
            else:
                ok = diff(baseline[1], normal, 'env-' + baseline[0], 'env-' + arm) and ok
        if python_env is not None and baseline_env is not None:
            for key in ('LC_ALL', 'LANG', 'CARGO_BUILD_JOBS', 'GOMAXPROCS', 'GOFLAGS',
                        'ERL_FLAGS', 'ELIXIR_ERL_OPTIONS', 'UV_THREADPOOL_SIZE', 'RAYON_NUM_THREADS',
                        'RACE_MODE', 'CODEX_WEB_SEARCH', 'RACE_NETWORK_ACCESS'):
                if python_env.get(key) != baseline_env.get(key):
                    print('Python common environment differs: ' + key); ok = False
        return ok
    check('arm-environments', environments)
    check('codex-auth', lambda: codex_home(R).is_dir() and (codex_home(R) / 'auth.json').is_file())

    def target():
        values, bugs = counts(R)
        text = (R / 'TARGET.md').read_text()
        listed = re.findall(r'^- (\S+)$', text, re.M)
        return (set(listed) == bugs and len(listed) == len(bugs)
                and len(scored_ids(R)) == values['N_scored']
                and f"{values['target']}/{values['N_scored']}" in text)
    check('target-spec-bugs', target)
    return bool(failed)


if __name__ == '__main__':
    raise SystemExit(run())
