#!/usr/bin/env python3
"""Compile-only reference timing worker. Invoked by the control window.

The worker stages no grader material, runs no tests/checks, and emits numeric
receipts only. Private project copies and logs are removed before it exits.
"""
import datetime
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(os.environ.get('BENCH_ROOT', pathlib.Path(__file__).resolve().parents[2]))
TOOLCHAINS = pathlib.Path(os.environ.get('TOOLCHAINS_ROOT', ROOT.parent / 'toolchains'))
sys.path.insert(0, str(ROOT / 'probe-kgn/runner'))
sys.path.insert(0, str(ROOT / 'levers/r70'))
from sandbox_linux import base_args
from dispatch import active

FILES = {
    'rust': 'src/core.rs',
    'go': 'core.go',
    'ts-bun': 'src/core.ts',
    'elixir': 'lib/core.ex',
}
COMMENT = {
    'rust': b'\n// compile timing neutral comment\n',
    'go': b'\n// compile timing neutral comment\n',
    'ts-bun': b'\n// compile timing neutral comment\n',
    'elixir': b'\n# compile timing neutral comment\n',
}


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def public_host_id():
    return {'hostname': os.environ.get('BENCH_HOST_ID', 'not recorded')}


def load_average():
    try:
        one, five, fifteen = os.getloadavg()
        return {'1m': one, '5m': five, '15m': fifteen}
    except (AttributeError, OSError):
        return None


def tree_size(path):
    path = pathlib.Path(path)
    if not path.exists():
        return {'exists': False, 'bytes': 0, 'files': 0}
    if path.is_file():
        try:
            return {'exists': True, 'bytes': path.stat().st_size, 'files': 1}
        except OSError:
            return {'exists': True, 'bytes': None, 'files': None}
    total = 0
    files = 0
    for current, dirs, names in os.walk(path, followlinks=False):
        dirs[:] = [d for d in dirs if not pathlib.Path(current, d).is_symlink()]
        for name in names:
            item = pathlib.Path(current, name)
            if item.is_symlink():
                continue
            try:
                total += item.stat().st_size
                files += 1
            except OSError:
                pass
    return {'exists': True, 'bytes': total, 'files': files}


def tsbuildinfo_paths(project):
    return [p for p in pathlib.Path(project).rglob('*.tsbuildinfo') if p.is_file()]


def remove_path(path):
    path = pathlib.Path(path)
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.exists():
        shutil.rmtree(path)


def cache_paths(context, project, go_cache, output):
    result = {
        'target': project / 'target',
        '_build': project / '_build',
        'build': project / 'build',
        'node_modules_cache': project / 'node_modules/.cache',
        'go_cache': go_cache,
        'compiler_output': output,
    }
    for path in tsbuildinfo_paths(project):
        result['tsbuildinfo:' + str(path.relative_to(project))] = path
    result['tsbuildinfo:compile-window'] = project / '.compile-window.tsbuildinfo'
    return result


def snapshot(paths):
    return {name: tree_size(path) for name, path in paths.items()}


def is_empty(state):
    return all(item['bytes'] == 0 for item in state.values())


def build_commands(stack, project, output):
    if stack == 'rust':
        cmd = ['cargo', 'build', '--offline', '--release']
        return [('cargo_build', cmd, 'target')]
    if stack == 'go':
        cmd = ['go', 'build', '-trimpath', '-o', str(output), '.']
        return [('go_build', cmd, 'go_cache')]
    if stack == 'ts-bun':
        tsc = [
            'bun', './node_modules/typescript/bin/tsc', '--strict', '--noEmit',
            '--incremental', '--tsBuildInfoFile',
            str(project / '.compile-window.tsbuildinfo'),
        ]
        bun = ['bun', 'build', '--compile', '--outfile', str(output), 'src/main.ts']
        return [('tsc_noemit', tsc, 'tsbuildinfo:compile-window'),
                ('bun_compile_bundle', bun, 'compiler_output')]
    if stack == 'elixir':
        return [('mix_compile', ['mix', 'compile', '--warnings-as-errors'], '_build')]
    raise ValueError('unknown stack')


def version_commands(stack):
    if stack == 'rust':
        return {'rustc': ['rustc', '--version'], 'cargo': ['cargo', '--version']}
    if stack == 'go':
        return {'go': ['go', 'version']}
    if stack == 'ts-bun':
        return {
            'bun': ['bun', '--version'],
            'tsc': ['bun', './node_modules/typescript/bin/tsc', '--version'],
        }
    if stack == 'elixir':
        return {'elixir_otp': ['elixir', '--version'], 'mix': ['mix', '--version']}
    raise ValueError('unknown stack')


def run_sandbox(scratch, project, env, argv, label, timeout=600, timed=False,
                caches=None, expected_cache=None):
    if active():
        raise RuntimeError('benchmark runner became active')
    args = base_args() + [
        '--ro-bind', str(TOOLCHAINS), str(TOOLCHAINS),
        '--bind', str(scratch), str(scratch),
        '--remount-ro', '/', '--chdir', str(project),
    ]
    load = load_average() if timed else None
    before = snapshot(caches) if timed else None
    if timed and not is_empty(before) and label.endswith(':cold'):
        return {'seconds': None, 'exit_code': None, 'error_type': 'cold_cache_not_empty',
                'load_average_before': load, 'cache_before': before, 'cache_after': None}
    started_utc = utc_now() if timed else None
    started = time.monotonic() if timed else None
    log_path = pathlib.Path(scratch) / 'logs' / (label.replace('/', '_') + '.log')
    log_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        with log_path.open('wb') as log:
            proc = subprocess.run(
                args + argv, env=env, stdin=subprocess.DEVNULL,
                stdout=log, stderr=subprocess.STDOUT, timeout=timeout,
            )
        rc = proc.returncode
        error_type = None
    except subprocess.TimeoutExpired:
        rc = 124
        error_type = 'timeout'
    except Exception as exc:
        rc = None
        error_type = type(exc).__name__
    elapsed = round(time.monotonic() - started, 6) if timed else None
    ended_utc = utc_now() if timed else None
    after = snapshot(caches) if timed else None
    if timed and rc == 0 and expected_cache:
        if after.get(expected_cache, {}).get('bytes', 0) <= 0:
            error_type = 'expected_output_missing'
            rc = 125
    return {
        'seconds': elapsed,
        'exit_code': rc,
        'error_type': error_type,
        'started_at_utc': started_utc,
        'ended_at_utc': ended_utc,
        'load_average_before': load,
        'cache_before': before,
        'cache_after': after,
    }


def prepare_context(job, window, version_cache, host):
    task = job['task']
    stack = job['stack']
    context = window / 'contexts' / (task + '-' + stack)
    context.mkdir(mode=0o700, parents=True, exist_ok=False)
    context.chmod(0o700)
    home = context / 'home'
    home.mkdir(mode=0o700)
    project = context / 'project'
    project.mkdir(mode=0o700)
    go_cache = context / 'go-cache'
    output = context / 'artifacts' / stack / 'kogen'
    (context / 'artifacts' / stack).mkdir(mode=0o700, parents=True)
    td = ROOT / 'new-tasks' / task
    meta = json.loads((td / 'task.json').read_text())
    base = job.get('reference_base_sha') or meta['base_sha']
    env = {
        **os.environ,
        **meta.get('env', {}),
        'RUSTUP_HOME': '/opt/bench/rustup',
        'CARGO_NET_OFFLINE': 'true',
        'CARGO_TARGET_DIR': str(project / 'target'),
        'GOTOOLCHAIN': 'local',
        'GOCACHE': str(go_cache),
        'HOME': str(home),
        'MIX_BUILD_PATH': str(project / '_build'),
        'GIT_CONFIG_GLOBAL': '/dev/null',
        'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_COUNT': '1',
        'GIT_CONFIG_KEY_0': 'safe.directory',
        'GIT_CONFIG_VALUE_0': '*',
    }
    archive = subprocess.run(
        ['git', '-C', str(td / 'skeleton'), 'archive', base],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env,
    )
    if archive.returncode != 0:
        raise RuntimeError('public_base_archive_failed')
    subprocess.run(['tar', '-x', '-C', str(project)], input=archive.stdout,
                   check=True, stderr=subprocess.DEVNULL)
    if job.get('reference_source'):
        shutil.copytree(job['reference_source'], project, dirs_exist_ok=True)
    if job.get('patch'):
        subprocess.run(
            ['git', 'apply', '--whitespace=nowarn', job['patch']],
            cwd=project, env=env, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    if stack == 'ts-bun':
        for name in ['package.json', 'tsconfig.json', 'setup.sh']:
            shutil.copy2(td / 'skeleton' / name, project / name)
        (project / 'src/runtime.d.ts').unlink(missing_ok=True)
    setup = project / 'setup.sh'
    if not setup.is_file() or setup.is_symlink():
        raise RuntimeError('setup_script_missing')
    setup.chmod(setup.stat().st_mode | 0o700)
    setup_result = run_sandbox(context, project, env, ['./setup.sh'], 'setup', timed=False, timeout=600)
    if setup_result['exit_code'] != 0:
        raise RuntimeError('dependency_setup_failed')
    version_key = (task, stack)
    if version_key not in version_cache:
        versions = {}
        for name, argv in version_commands(stack).items():
            result = run_sandbox(context, project, env, argv, 'version-' + name, timed=False, timeout=60)
            log = context / 'logs' / ('version-' + name + '.log')
            try:
                body = log.read_text(errors='replace').strip()
            except OSError:
                body = ''
            versions[name] = {'text': body[:500], 'exit_code': result['exit_code']}
        if not all(value['exit_code'] == 0 for value in versions.values()):
            raise RuntimeError('toolchain_version_probe_failed')
        version_cache[version_key] = versions
    return {
        'job': job, 'context': context, 'project': project, 'home': home,
        'go_cache': go_cache, 'output': output, 'env': env, 'task_meta': meta,
        'base_sha': base, 'versions': version_cache[version_key], 'host': host,
    }


def reset_for_cold(ctx, tool):
    project = ctx['project']
    for rel in ['target', '_build', 'build', 'node_modules/.cache']:
        remove_path(project / rel)
    for info in tsbuildinfo_paths(project):
        remove_path(info)
    remove_path(project / '.compile-window.tsbuildinfo')
    remove_path(ctx['go_cache'])
    remove_path(ctx['context'] / 'artifacts')
    (ctx['context'] / 'artifacts' / ctx['job']['stack']).mkdir(mode=0o700, parents=True)
    if ctx['job']['stack'] == 'go':
        ctx['go_cache'].mkdir(mode=0o700)
    # All compiler state and outputs are absent immediately before each cold run.
    if tool == 'tsc_noemit':
        pass


def record_compile(ctx, rep, tool, argv, expected_cache):
    job = ctx['job']
    project = ctx['project']
    task = job['task']
    stack = job['stack']
    source = project / FILES[stack]
    if not source.is_file() or source.is_symlink():
        raise RuntimeError('incremental_source_missing')
    paths = cache_paths(ctx['context'], project, ctx['go_cache'], ctx['output'])
    row_base = {
        'task': task,
        'task_number': int(task.split('-')[1]),
        'stack': stack,
        'tool': tool,
        'rep': rep,
        'incremental_file': FILES[stack],
        'reference_base_sha': ctx['base_sha'],
        'versions': ctx['versions'],
        'host': ctx['host'],
        'dependency_scope': {
            'fetched_dependencies_preserved': True,
            'compiled_dependencies_included_when_cache_cleared': stack in ('rust', 'go', 'elixir'),
            'note': {
                'rust': 'Cargo target/ absent; registry/download cache kept; dependency crates compile as needed.',
                'go': 'Fresh GOCACHE per cold run; module cache kept; standard and module packages compile as needed.',
                'ts-bun': 'node_modules kept; tsc checks source/types with no JS output; Bun bundle includes imported packages.',
                'elixir': 'Mix _build absent; deps source kept; Mix compiles project and any uncached dependencies.',
            }[stack],
        },
        'host_spec': ctx['host'],
    }
    cold_state = snapshot(paths)
    if not is_empty(cold_state):
        row = {**row_base, 'phase': 'cold', 'seconds': None, 'exit_code': None,
               'error_type': 'cold_cache_not_empty', 'cache_before': cold_state,
               'cache_after': None, 'valid': False}
        return [row]
    cold = run_sandbox(
        ctx['context'], project, ctx['env'], argv, f'{task}-{stack}-{tool}-r{rep}:cold',
        timed=True, caches=paths, expected_cache=expected_cache,
    )
    cold_row = {**row_base, 'phase': 'cold', **cold, 'valid': cold['exit_code'] == 0}

    original_size = source.stat().st_size
    comment = COMMENT[stack]
    source.chmod(source.stat().st_mode | 0o600)
    with source.open('ab') as handle:
        handle.write(comment)
        handle.flush()
        os.fsync(handle.fileno())
    if source.stat().st_size != original_size + len(comment):
        raise RuntimeError('comment_append_size_mismatch')
    incremental = run_sandbox(
        ctx['context'], project, ctx['env'], argv,
        f'{task}-{stack}-{tool}-r{rep}:incremental', timed=True,
        caches=paths,
    )
    inc_row = {
        **row_base,
        'phase': 'incremental',
        **incremental,
        'valid': incremental['exit_code'] == 0,
        'edit': 'one neutral line comment appended to the same implementation file',
        'comment_bytes': len(comment),
        'compiler_incremental_mode': (
            'TypeScript --incremental using the .tsbuildinfo produced by the cold run'
            if tool == 'tsc_noemit' else
            'Bun standalone CLI rebuild after source edit; output is regenerated, with no persistent incremental build graph'
            if tool == 'bun_compile_bundle' else
            'same compiler command after source edit with cold-run artifacts retained'
        ),
        'cold_run_cache_after': cold.get('cache_after'),
    }
    # Restore without reading or emitting any source bytes.
    with source.open('r+b') as handle:
        handle.truncate(original_size)
        handle.flush()
        os.fsync(handle.fileno())
    if source.stat().st_size != original_size:
        raise RuntimeError('source_restore_size_mismatch')
    return [cold_row, inc_row]


def main():
    window = pathlib.Path(sys.argv[1])
    if not window.name.startswith('r70-window-') or window.stat().st_mode & 0o777 != 0o700:
        raise SystemExit(2)
    if active():
        raise SystemExit(3)
    jobs = json.loads((window / 'jobs.json').read_text())
    rows = []
    setup_rcs = []
    version_cache = {}
    host = public_host_id()
    started_utc = utc_now()
    start = time.monotonic()
    contexts = {}
    try:
        for item in jobs:
            key = (item['task'], item['stack'])
            if key not in contexts:
                ctx = prepare_context(item, window, version_cache, host)
                contexts[key] = ctx
                setup_rcs.append({'task': item['task'], 'stack': item['stack'], 'exit_code': 0})
            ctx = contexts[key]
            for tool, argv, expected in build_commands(item['stack'], ctx['project'], ctx['output']):
                reset_for_cold(ctx, tool)
                rows.extend(record_compile(ctx, item['rep'], tool, argv, expected))
        ok = len(rows) == 150 and all(row.get('valid') for row in rows)
        reason = None if ok else 'measurement_count_or_exit_code_invalid'
    except Exception as exc:
        ok = False
        reason = type(exc).__name__
    finally:
        shutil.rmtree(window / 'contexts', ignore_errors=True)
    ended_utc = utc_now()
    elapsed = round(time.monotonic() - start, 6)
    measured = round(sum(row.get('seconds') or 0 for row in rows), 6)
    with (window / 'timings.jsonl').open('w') as out:
        for row in rows:
            row['project_scratch_purged'] = not (window / 'contexts').exists()
            out.write(json.dumps(row, sort_keys=True) + '\n')
    summary = {
        'valid': ok,
        'reason': reason,
        'started_at_utc': started_utc,
        'finished_at_utc': ended_utc,
        'worker_elapsed_seconds': elapsed,
        'sum_timed_compile_seconds': measured,
        'timed_command_count': len(rows),
        'expected_timed_command_count': 150,
        'setup_exit_codes': setup_rcs,
        'project_scratch_purged': not (window / 'contexts').exists(),
        'host_spec': host,
    }
    (window / 'worker-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
