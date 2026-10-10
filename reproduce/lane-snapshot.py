#!/usr/bin/env python3
"""Record launch-time public host/tool snapshots without host identity or credentials."""
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def run(command):
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT,
                                       text=True, timeout=8).strip().splitlines()[0][:240]
    except Exception:
        return None


def sha(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except Exception:
        return None


SPECS = {
    'python': (['python3', '--version'], 'PYTHON_VERSION'),
    'ruby': (['ruby', '--version'], 'RUBY_VERSION'),
    'elixir': (['elixir', '--version'], 'ELIXIR_VERSION'),
    'erlang': (['erl', '-noshell', '-eval', 'io:format("~s",[erlang:system_info(otp_release)]),halt().'], 'ERLANG_VERSION'),
    'rust': (['rustc', '--version'], 'RUST_VERSION'),
    'node': (['node', '--version'], 'NODE_VERSION'),
    'go': (['go', 'version'], 'GO_VERSION'),
    'bun': (['bun', '--version'], 'BUN_VERSION'),
    'gleam': (['gleam', '--version'], 'GLEAM_VERSION'),
}


def collect(kit, allowfile='', venue='', account='', planfile='', *, command_runner=run,
            file_sha=sha, host_platform=platform, core_count=None,
            proc_root=Path('/proc'), codex_path='/opt/bench/tools/bin/codex'):
    kit = str(kit)
    if planfile:
        try:
            plan = json.loads(Path(planfile).read_text(encoding='utf-8'))
            venue = plan.get('venue', venue)
            account = plan.get('account_class', account)
        except (OSError, ValueError):
            pass
    pins = {}
    for line in Path(kit + '/reproduce/host-pins.lock').read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            pins[key] = value

    versions, hashes = {}, {}
    for name, (cmd, _pin) in SPECS.items():
        executable = shutil.which(cmd[0])
        versions[name] = command_runner(cmd) if executable else None
        hashes[name] = file_sha(executable) if executable else None

    allow = ['chatgpt.com', 'ab.chatgpt.com']
    # Hash the canonical default list, including its newline format.
    allow_hash = hashlib.sha256(b'chatgpt.com\nab.chatgpt.com\n').hexdigest()
    if allowfile:
        path = Path(allowfile)
        try:
            allow_hash = file_sha(path)
            for line in path.read_text().splitlines():
                value = line.split('#', 1)[0].strip()
                if value and '=' in value:
                    value = value.split('=', 1)[1].strip()
                if value:
                    allow.append(value)
        except OSError:
            allow_hash = None
    allow = sorted(set(x for x in allow if x and '/' not in x and '\\' not in x))

    try:
        mem = round(int(next(x.split()[1] for x in (proc_root / 'meminfo').read_text().splitlines()
                             if x.startswith('MemTotal:'))) / 1048576, 3)
    except Exception:
        mem = None
    try:
        cpu = next(x.split(':', 1)[1].strip() for x in (proc_root / 'cpuinfo').read_text().splitlines()
                   if x.startswith('model name'))
    except Exception:
        cpu = host_platform.machine()
    cores = core_count if core_count is not None else os.cpu_count()
    system_name = host_platform.system()
    if hasattr(host_platform, 'freedesktop_os_release'):
        try:
            os_name = host_platform.freedesktop_os_release().get('PRETTY_NAME', system_name)
        except Exception:
            os_name = system_name
    else:
        os_name = system_name

    other_names = ('go', 'bun', 'gleam')
    environment_inventory = '; '.join(f'{name}={versions[name] or "unavailable"}'
                                      for name in other_names)
    tools_inventory = '; '.join(
        f'{name}={versions[name] or "unavailable"}; sha256={hashes[name] or "unavailable"}'
        for name in other_names)
    environment_toolchains = {
        key: versions.get(key) or {'missing': 'm54'}
        for key in ('python', 'ruby', 'elixir', 'erlang', 'rust', 'node')
    }
    environment_toolchains['other_inventory'] = environment_inventory
    tools_toolchains = {
        key: (f'{version}; sha256={hashes[key]}' if version and hashes[key]
              else version or {'missing': 'm54'})
        for key, version in versions.items()
        if key in ('python', 'ruby', 'elixir', 'erlang', 'rust', 'node')
    }
    tools_toolchains['other_inventory'] = tools_inventory

    codex_version = command_runner([codex_path, '--version'])
    data = {
        'environment': {
            'os': os_name, 'kernel': host_platform.release(), 'cpu_model': cpu,
            'cores': cores, 'ram_gib': mem, 'toolchains': environment_toolchains,
            'network': {'profile': 'per-cell CONNECT allowlist proxy', 'allowlist_hosts': allow},
            'account_class': account if account in ('billing', 'owner') else {'missing': 'm100'},
        },
        'host': {
            'id': f'kogen-bench-{venue}' if venue in ('eu', 'us') else {'missing': 'm32'},
            'cpu': cpu, 'vcpu': cores, 'ram_gib': mem, 'os': system_name,
            'kernel': host_platform.release(), 'spec_ref': 'sanitized launch snapshot',
        },
        'sandbox': {
            'profile': 'bubblewrap network namespace',
            'profile_sha256': file_sha(Path(kit + '/reproduce/sandbox-profile.sh')),
            'egress_profile': f'per-cell CONNECT allowlist proxy; allowlist_sha256={allow_hash}',
            'egress_allow': allow,
        },
        'tools': {
            'harness': {'missing': 'm17'},
            'codex_cli': (f'{codex_version} sha256={file_sha(codex_path)}'
                          if codex_version and file_sha(codex_path) else {'missing': 'm18'}),
            'runner': f'kit runner sha256={file_sha(Path(kit + "/reproduce/run-lane.sh"))}',
            'grader': {'missing': 'm77'},
            'toolchains': tools_toolchains,
        },
        'tool_hashes': hashes,
        'allowlist_sha256': allow_hash,
        'tool_versions': versions,
    }
    return data


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) not in (5, 6):
        raise SystemExit('usage: lane-snapshot.py OUT KIT ALLOWFILE VENUE ACCOUNT [PLANFILE]')
    out, kit, allowfile, venue, account = argv[:5]
    planfile = argv[5] if len(argv) == 6 else ''
    Path(out).write_text(json.dumps(collect(kit, allowfile, venue, account, planfile), sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
