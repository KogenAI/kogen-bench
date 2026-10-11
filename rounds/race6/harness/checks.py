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
from condition import ARMS,condition,language
from validity import codex_home, tree_hash
from scoring_config import counts, scored_ids
from mode_policy import read_mode, brief_template, DENYLIST_RULE

R = Path(__file__).resolve().parent
KIT = Path(os.environ.get('RACE3_KIT_DIR', str(R.parent/'race3-kit'))).resolve()
NAMES = {a: ('Elixir' if language(a)=='ex' else 'Go') for a in ARMS}

CACHE_VARS = ('CARGO_HOME', 'GOPATH', 'GOMODCACHE', 'GOCACHE', 'MIX_HOME',
              'HEX_HOME', 'BUN_INSTALL_CACHE_DIR', 'XDG_CACHE_HOME', 'npm_config_cache')
GIT_PREFIXES = ('https://github.com/KogenAI/', 'http://github.com/KogenAI/',
                '[email omitted]:KogenAI/', 'ssh://[email omitted]/KogenAI/')
OFFLINE = {'UV_OFFLINE': '1', 'CARGO_NET_OFFLINE': 'true', 'HEX_OFFLINE': '1', 'npm_config_offline': 'true',
           'NPM_CONFIG_OFFLINE': 'true', 'BUN_INSTALL_OFFLINE': '1', 'BUN_CONFIG_OFFLINE': '1'}


def disk_admission(root, arms, env=None, free_bytes=None, host=None):
    """Portable admission on every host, using conservative race 4 measurements."""
    root = Path(root)
    env = os.environ if env is None else env
    if not arms or len(arms) != len(set(arms)) or not set(arms) <= set(NAMES):
        raise ValueError('ARMS must contain unique registered race 6 conditions')
    host = host or platform.system()
    if host == 'Linux' and (len(arms) != 1 or arms[0] not in ('ex-a', 'ex-d')):
        raise ValueError('Linux hosts run one A or D arm only')
    defaults = json.loads((root / 'DISK-DEFAULTS.json').read_text())
    def positive(key, fallback):
        value = int(env.get(key, fallback))
        if value <= 0:
            raise ValueError(f'{key} must be a positive integer')
        return value
    prefix = 'linux_' if host == 'Linux' else ''
    working = positive('RACE_PER_ARM_WORKING_BYTES', defaults.get(prefix+'per_arm_working_bytes', defaults['per_arm_working_bytes']))
    snapshot = positive('RACE_SNAPSHOT_BYTES_PER_ARM', defaults.get(prefix+'snapshot_bytes_per_arm', defaults['snapshot_bytes_per_arm']))
    cap = positive('RACE_CAP_MIN', 60)
    interval = positive('RACE_SNAPSHOT_MIN', 5)
    snapshots = 5 if host == 'Linux' else (cap + interval - 1) // interval + 1
    base = len(arms) * (working + snapshots * snapshot + (working if host != 'Linux' else 0))  # Hourly builds survive pruning.
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
        if env.get('GOPROXY') != 'https://proxy.golang.org,direct' or env.get('GOSUMDB') != 'sum.golang.org' or '-mod=' in env.get('GOFLAGS', '') or '-modcacherw' not in env.get('GOFLAGS',''):
            raise ValueError('REAL-WORKFLOW Go environment must allow normal fetching')
        for key in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy'):
            if env.get(key) == 'http://127.0.0.1:9':
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
    if env.get('GOPROXY') != 'https://proxy.golang.org,direct' or '-mod=' in env.get('GOFLAGS', '') or '-modcacherw' not in env.get('GOFLAGS',''):
        raise ValueError('agent Go environment must allow normal module fetching')
    for name in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy'):
        if env.get(name) == 'http://127.0.0.1:9':
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
    if 'PATH' in result:
        result['PATH']=':'.join(p for p in result['PATH'].split(':') if not p.endswith('/race6-kit/quint'))
    return ''.join('%s=%s\n' % item for item in sorted(result.items()))



def quint_gate(root,arm,env):
    kit=Path(os.environ.get('RACE6_KIT_DIR',str(Path(root).parent/'race6-kit')))
    actual=shutil.which('quint',path=env['PATH'])
    if condition(arm) in ('a','c'):
        assert actual is None, f'{arm} must not have quint on PATH: {actual}'
    else:
        assert actual and Path(actual).resolve()==(kit/'quint/quint').resolve(),f'{arm} missing pinned Quint'
        got=subprocess.check_output([actual,'--version'],env=env,text=True,timeout=30).strip()
        assert got=='0.33.0',got
    return True

def run():
    from briefs import check as brief_check
    from spec_split import verify,rows,CLASSES
    from freeze import kit_hash,check as freeze_check,validate_inputs
    failed=[]
    def check(name,fn):
        try:ok=bool(fn())
        except Exception as error:print(str(error));ok=False
        print(('PASS ' if ok else 'FAIL ')+name)
        if not ok:failed.append(name)
    arms=(R/'ARMS').read_text().split()
    (R/'out').mkdir(exist_ok=True)
    check('disk-admission',lambda:disk_admission(R,arms))
    if '--disk-only' in sys.argv:return bool(failed)
    check('MODE',lambda:read_mode(R)=='real-workflow')
    check('brief-equality',lambda:(brief_check(R) or True))
    check('frozen-inputs',lambda:validate_inputs(R))
    check('hidden-inventory-closed',lambda:not json.loads((R/'hidden-inventory.json').read_text())['errors'])
    check('split-complete-and-byte-identical',lambda:bool(verify(R)))
    check('target-only-hidden-count',lambda:(R/'TARGET.md').read_text()=='The hidden suite has 106 scored cases.\n')
    check('106-scored',lambda:counts(R)[0]['N_scored']==len((R/'SCORE_CASES.txt').read_text().split())==106 if platform.system()=='Linux' and not os.access(R/'inputs/conformance',os.R_OK) else counts(R)[0]['N_scored']==len(scored_ids(R))==106)
    kit=Path(os.environ.get('RACE6_KIT_DIR',str(R.parent/'race6-kit')))
    check('Quint-kit-hash',lambda:kit_hash(kit/'quint')==(R/'QUINT-KIT-SHA256').read_text().strip())
    if (R/'FREEZE.json').exists():check('freeze',lambda:(freeze_check(R) or True))
    def main_kit():
        output=subprocess.check_output(['bash','kitsum.sh'],cwd=R,text=True,env=dict(os.environ,RACE_KIT_MANIFEST=str(R/'out/kit-manifest.sha256')))
        got=re.search(r'\bhash ([0-9a-f]{64})',output)[1]
        print('Elixir/Go kit hash: '+got)
        return got==(R/'KIT-SHA256').read_text().strip()
    check('race5-Elixir-Go-kit-pin',main_kit)
    # No credential/home contents are read by these build gates.
    print('SKIP live Codex/credential and host process gates: live dry cells waived')
    command='set -e; source "$1/env.sh"; source "$1/$2/.kit-env.sh"; cd "$1/$2"; exec /usr/bin/python3 -c "import os,json;print(json.dumps(dict(os.environ)))"'
    baseline=None
    for arm in arms:
        def environment(arm=arm):
            nonlocal baseline
            env=json.loads(subprocess.check_output(['/bin/bash','-c',command,'checks',str(R),arm],text=True))
            mode_environment(env,'real-workflow',R/arm)
            for key in ('CARGO_BUILD_JOBS','GOMAXPROCS','UV_THREADPOOL_SIZE','RAYON_NUM_THREADS'):
                assert env[key]=='2',key
            assert env['GOFLAGS']=='-modcacherw' and env['ERL_FLAGS']=='+S 2:2 +SDcpu 2:2'
            assert not (R/arm).is_symlink() and not (R/arm/'.kitcache').is_symlink(),'symlinked arm/cache writable roots'
            for key in ('GOMODCACHE','GOCACHE','TMPDIR'):
                raw=Path(env[key]);assert raw==raw.resolve() and not raw.is_symlink(),key+' symlinked writable root'
                assert R/arm in raw.resolve().parents,key
            if language(arm)=='go':
                assert 'go1.27.1' in subprocess.check_output(['go','version'],env=env,text=True,timeout=30)
            else:
                assert 'Elixir 1.20.4' in subprocess.check_output(['elixir','--version'],env=env,text=True,timeout=30)
            quint_gate(R,arm,env)
            normalized=normalise_env(env,arm)
            if baseline is None:baseline=normalized
            else:assert normalized==baseline,'arm environments differ beyond designated Quint PATH'
            assert not (R/arm/'conformance').exists(),'suite supplied to arm'
            assert (R/arm/'INTERFACE.md').read_bytes()==(R/'INTERFACE.md').read_bytes()
            assert (R/arm/'TARGET.md').read_bytes()==(R/'TARGET.md').read_bytes()
            expected={row['path']:row['sha256'] for row in rows(R) if row['class'] in CLASSES[condition(arm)]}
            import hashlib
            actual={p.relative_to(R/arm/'spec').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/arm/'spec').rglob('*') if p.is_file()}
            assert expected==actual,'spec subset differs'
            return True
        check('arm-'+arm+'-env-spec-quint-presence-or-absence',environment)
    return bool(failed)

if __name__=='__main__':raise SystemExit(run())
