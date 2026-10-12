#!/usr/bin/env python3
"""Create a new ARCH harness from read-only lever helpers and this overlay."""
from pathlib import Path
import argparse
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
from arch_config import ARMS, CORES, MODEL, EFFORT, treatment, arms_for_host, render, dump, digest
from arch_fs import safe_chmod, safe_rmtree

OVERLAY = Path(__file__).resolve().parent

def clone(source, destination):
    if os.uname().sysname == 'Darwin':
        subprocess.run(['/bin/cp', '-c', '-p', '-R', str(source), str(destination)], check=True)
    else:
        shutil.copytree(source, destination, symlinks=False)

def aid(text):
    text = re.sub(r'^## Offline rules\n.*?(?=^## |\Z)', '', text, flags=re.M | re.S)
    text = re.sub(r'\. "[^"\n]+/env-aids\.sh"', '. ./.kit-env.sh', text)
    text = text.replace(' --offline', '')
    text = text.replace('Its online installation examples are reference material; use this kit’s offline commands and pins.',
                        'Documentation and package installation may be used in REAL-WORKFLOW mode.')
    text = text.replace('Available offline libraries', 'Seeded libraries')
    return text

def environment(root, arm, config):
    workspace = root / arm
    stack = config['toolchains']
    # Codex may be a Node CLI with an /usr/bin/env node shebang. Keep the
    # executable's install bin on the arm PATH even when the caller's PATH is
    # replaced by this controlled toolchain environment.
    codex_bin = Path(config['codex_executable']).expanduser().absolute().parent
    mise_shims = Path.home() / '.local/share/mise/shims'
    mise = config.get('mise_executable') or shutil.which('mise')
    paths = [str(workspace / '.kit-tools'), str(codex_bin), str(mise_shims)]
    if mise:
        paths.append(str(Path(mise).expanduser().absolute().parent))
    paths.append(str(Path(stack['go']) / 'bin'))
    if treatment(arm) == 'E':
        paths += [str(Path(stack['elixir']) / 'bin'), str(Path(stack['erlang']) / 'bin')]
    paths += ['/usr/bin', '/bin', '/usr/sbin', '/sbin']
    cache = workspace / '.kitcache'
    cores = CORES[config['host']]
    threads = 3  # Studio's fractional cap is enforced in the shared sampled supervisor.
    values = dict(PATH=':'.join(paths), GOTOOLCHAIN='local', GOWORK='off',
                  GOMAXPROCS=str(threads), GOFLAGS='-p=3 -modcacherw',
                  GOPATH=str(cache / 'go'), GOMODCACHE=str(cache / 'go/pkg/mod'),
                  GOCACHE=str(cache / 'go-build'), GOPROXY='https://proxy.golang.org,direct',
                  GOSUMDB='sum.golang.org', GOLANGCI_LINT_CACHE=str(cache / 'golangci'),
                  GOPLSCACHE=str(cache / 'gopls'), TEST_TELEMETRY_DIR=str(cache / 'go-telemetry'),
                  XDG_CACHE_HOME=str(cache / 'xdg'), XDG_CONFIG_HOME=str(cache / 'config'),
                  XDG_DATA_HOME=str(cache / 'data'), TMPDIR=str(cache / 'tmp'),
                  MISE_CACHE_DIR=str(cache / 'mise'), MISE_TRUSTED_CONFIG_PATHS=str(workspace),
                  MISE_DATA_DIR=str(Path.home() / '.local/share/mise'),
                  MISE_OFFLINE='1', MISE_AUTO_INSTALL='0',
                  GIT_CONFIG_GLOBAL=str(workspace / '.gitconfig-global'),
                  RACE_MODE='real-workflow', RACE3_KIT=config['kit'], ARCH_SOFT_CORES=str(cores), NO_COLOR='1',
                  LC_ALL='C', LANG='C')
    if treatment(arm) == 'E':
        values.update(MIX_HOME=str(cache / 'mix'), HEX_HOME=str(cache / 'hex'),
                      MIX_XDG='true', HEX_OFFLINE='0', MIX_ENV='test',
                      ERL_FLAGS='+S 3:3 +SDcpu 3:3', ELIXIR_ERL_OPTIONS='+S 3:3',
                      ERL_CRASH_DUMP=str(cache / 'tmp/erl_crash.dump'))
    return values

def mise_config(arm):
    tools = ['go = "1.27.1"', 'node = "24.21.0"']
    if treatment(arm) == 'E':
        tools += ['elixir = "1.20.4-otp-29"', 'erlang = "29.1.1"']
    return '[tools]\n' + '\n'.join(tools) + '\n'

def install(args):
    target, source, inputs, kit = (Path(p).expanduser().resolve() for p in
                                  (args.target, args.source_harness, args.arch_input, args.kit))
    if target.name != 'arch-harness' or target.exists() or target == source or source in target.parents:
        raise ValueError('Target must be a new, nonexistent arch-harness outside the frozen source')
    for name in ('DESIGN-ARCH.md', 'DECISION-RULE-ARCH.md', 'spec/SPEC.md', 'spec/PROTOCOL.md',
                 'spec/STEPS.md', 'tests/run_hidden.py'):
        if not (inputs / name).is_file():
            raise ValueError('Required ARCH input missing: ' + name)
    if not list((inputs / 'spec/quint').glob('*.qnt')) or not list((inputs / 'spec/features').glob('*.feature')):
        raise ValueError('Quint and Gherkin inputs must be complete before installation')
    pins = json.loads((source / 'KIT-PINS-v2.json').read_text())
    if digest(kit / 'env-aids.sh') != pins['env_aids_sha256']:
        raise ValueError('Race 5 kit environment pin differs')
    stack = {'go': str(Path(args.go).expanduser().resolve()),
             'elixir': str(Path(args.elixir).expanduser().resolve()),
             'erlang': str(Path(args.erlang).expanduser().resolve())}
    codex = shutil.which('codex')
    if not codex:
        raise ValueError('codex is not installed')
    mise = getattr(args, 'mise_executable', None) or shutil.which('mise')
    if not mise:
        raise ValueError('mise is not installed')
    mise = str(Path(mise).expanduser().resolve())
    target.mkdir(parents=True)
    for path in OVERLAY.iterdir():
        if path.suffix in ('.py', '.md', '.json', '.tmpl', '.sha256') or path.name == 'ARMS':
            shutil.copy2(path, target / path.name)
    # Selectively derive from the frozen harness; do not copy old arm workspaces or runs.
    for name in ('CODEX-VERSION', 'KIT-PINS-v2.json', 'kitsum.sh'):
        shutil.copy2(source / name, target / name)
    for name in ('DESIGN-ARCH.md', 'DECISION-RULE-ARCH.md'):
        shutil.copy2(inputs / name, target / name)
    for name in ('RULE-SHA256.txt', 'DESIGN-SHA256.txt'):
        if (inputs / name).is_file():
            shutil.copy2(inputs / name, target / name)
    shutil.copytree(inputs / 'spec', target / 'inputs/spec', symlinks=True)
    shutil.copytree(inputs / 'spec', target / 'spec', symlinks=True)
    shutil.copytree(inputs / 'tests', target / 'tests', ignore=shutil.ignore_patterns('__pycache__'))
    (target / 'MODE').write_text('real-workflow\n')
    config = dict(schema=1, host=args.host, model=MODEL, effort=EFFORT, kit=str(kit),
                  source_harness=str(source), codex_executable=codex,
                  mise_executable=mise,
                  source_codex_home=str(Path(args.codex_home).expanduser().resolve()),
                  toolchains=stack, snapshot_interval_seconds=300, score_timeout_seconds=7200,
                  score_network='loopback-only', kit_pins=pins)
    dump(target / 'ARCH-CONFIG.json', config)
    for arm in arms_for_host(args.host):
        workspace = target / arm
        clone(kit / 'templates/go', workspace)
        (workspace / 'mise.toml').write_text(mise_config(arm))
        safe_rmtree(target, workspace / '.cache', ignore_errors=True)
        guides = [('go', (kit / 'templates/go/AGENTS.md').read_text())]
        if treatment(arm) == 'E':
            for path in (kit / 'templates/ex').iterdir():
                if path.name in ('AGENTS.md', 'CLAUDE.md', 'docs'):
                    continue
                destination = workspace / path.name
                clone(path, destination) if path.is_dir() else shutil.copy2(path, destination)
            shutil.copytree(kit / 'templates/ex/docs', workspace / 'docs/elixir', dirs_exist_ok=True)
            guides.append(('Elixir', (kit / 'templates/ex/AGENTS.md').read_text()))
        shutil.copytree(target / 'inputs/spec', workspace / 'spec', symlinks=True)
        caches = ['go', 'go-build', 'go-telemetry', 'golangci', 'gopls', 'xdg', 'config', 'data']
        if treatment(arm) == 'E':
            caches += ['mix', 'hex']
        for name in caches:
            destination = workspace / '.kitcache' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if (kit / 'cache' / name).is_dir():
                clone(kit / 'cache' / name, destination)
            else:
                destination.mkdir()
        (workspace / '.kitcache/tmp').mkdir()
        tools = workspace / '.kit-tools'
        tools.mkdir()
        for name in ('golangci-lint', 'goimports', 'gofumpt', 'gopls', 'gotestsum'):
            shutil.copy2(kit / 'bin' / name, tools / name)
        (tools / 'codex').symlink_to(codex)
        shutil.copy2(target / 'arch_tooltimer.py', tools / 'arch_tooltimer.py')
        for name in (('go', 'mix') if treatment(arm) == 'E' else ('go',)):
            real = str(Path.home() / '.local/share/mise/shims' / name)
            wrapper = tools / name
            wrapper.write_text('#!/bin/sh\nexec /usr/bin/python3 ' + shlex.quote(str(tools / 'arch_tooltimer.py')) +
                               ' ' + shlex.quote(name) + ' ' + shlex.quote(real) + ' "$@"\n')
            safe_chmod(target, wrapper, 0o755)
        values = environment(target, arm, config)
        env_text = '# ARCH private caches and explicitly selected toolchains.\n'
        env_text += '\n'.join('export ' + key + '=' + shlex.quote(value) for key, value in values.items())
        env_text += '\nunset CARGO_NET_OFFLINE FORCE_COLOR\n'
        (workspace / '.kit-env.sh').write_text(env_text)
        safe_chmod(target, workspace / '.kit-env.sh', 0o444)
        for base, dirs, files in os.walk(tools, followlinks=False):
            directory = Path(base)
            safe_chmod(target, directory, stat.S_IMODE(directory.stat().st_mode) & ~0o222)
            for name in files:
                path = directory / name
                if not path.is_symlink():
                    safe_chmod(target, path, stat.S_IMODE(path.stat().st_mode) & ~0o222)
        policy = '\n\n' + render((target / 'BRIEF-ARCH.tmpl').read_text(), arm).replace(
            'You have a 90-minute build cap.',
            'The phase prompt selects a 90-minute build cap or a 30-minute maintenance cap.')
        (workspace / 'AGENTS.md').write_text('\n\n'.join(aid(text) for _, text in guides) + policy)
        (target / ('BRIEF-' + arm + '.md')).write_text(render((target / 'BRIEF-ARCH.tmpl').read_text(), arm))
        gitconfig = '[url "https://invalid.invalid/blocked/"]\n'
        for prefix in ('https://github.com/KogenAI/', 'http://github.com/KogenAI/',
                       '[email omitted]:KogenAI/', 'ssh://[email omitted]/KogenAI/'):
            gitconfig += '\tinsteadOf = ' + prefix + '\n'
        (workspace / '.gitconfig-global').write_text(gitconfig)
        (workspace / '.gitignore').write_text('.git/\n.kitcache/\n.kit-tools/\n.cache/\n')
        # Fresh scratch repos aid the agent; no baseline or real-repository commits.
        subprocess.run(['git', '-c', 'init.defaultBranch=main', 'init', '-q', str(workspace)], check=True)
        for base, dirs, files in os.walk(workspace / 'spec', followlinks=False):
            for name in files:
                path = Path(base) / name
                if not path.is_symlink():
                    safe_chmod(target, path, 0o444)
        dump(target / 'out' / arm / 'environment.json', values)
    print(str(target))
    return target

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target', default='<scratch-dir>/arch-harness')
    p.add_argument('--source-harness', default='<scratch-dir>/lever-harness')
    p.add_argument('--arch-input', default='<scratch-dir>/arch')
    p.add_argument('--kit', default='<scratch-dir>/race3-kit')
    p.add_argument('--host', required=True, choices=CORES)
    p.add_argument('--codex-home', required=True)
    p.add_argument('--go', default='~/.local/share/mise/installs/go/1.27.1')
    p.add_argument('--elixir', default='~/.local/share/mise/installs/elixir/1.20.4-otp-29')
    p.add_argument('--erlang', default='~/.local/share/mise/installs/erlang/29.1.1')
    p.add_argument('--freeze', action='store_true', help='Freeze after completed A/B/E inputs have been installed')
    args = p.parse_args()
    target = install(args)
    if args.freeze:
        from arch_gates import freeze
        freeze(target)

if __name__ == '__main__':
    main()
