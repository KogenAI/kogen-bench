#!/usr/bin/env python3
"""Compile timing v3 supplement: project-only full rebuild + sandbox no-op baseline.

Reuses compile_worker_v3 (same directory). Per (task, stack) context:
  1. untimed warm-up build (dependencies / stdlib / node_modules caches populated);
  2. n reps of a timed sandboxed no-op (`true`) = fixed per-command overhead;
  3. n reps of PROJECT-ONLY full rebuild: one neutral comment appended to EVERY
     project source file (dependency caches stay warm), timed build, sources
     restored by truncation. Never reads or emits source bytes.
Emits timings + sizes only; private project copies are purged before exit.
"""
import json
import pathlib
import shutil
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compile_worker_v3 as w  # noqa: E402

GLOBS = {
    'rust': ['src/**/*.rs'],
    'go': ['*.go', '**/*.go'],
    'ts-bun': ['src/**/*.ts'],
    'elixir': ['lib/**/*.ex'],
}
REPS = 5


def project_sources(stack, project):
    found = set()
    for pattern in GLOBS[stack]:
        for path in project.glob(pattern):
            rel = path.relative_to(project).parts
            if not path.is_file() or path.is_symlink():
                continue
            if any(part in ('vendor', 'node_modules', 'deps', '_build', 'target') for part in rel):
                continue
            if stack == 'go' and path.name.endswith('_test.go'):
                continue
            if stack == 'ts-bun' and path.name.endswith('.d.ts'):
                continue
            found.add(path)
    return sorted(found)


def main():
    window = pathlib.Path(sys.argv[1])
    if not window.name.startswith('r70-window-') or window.stat().st_mode & 0o777 != 0o700:
        raise SystemExit(2)
    if w.active():
        raise SystemExit(3)
    jobs = json.loads((window / 'jobs.json').read_text())
    seen, uniq = set(), []
    for job in jobs:
        key = (job['task'], job['stack'])
        if key not in seen:
            seen.add(key)
            uniq.append({**job, 'rep': 0})
    host = w.host_spec()
    version_cache = {}
    rows = []
    started = w.utc_now()
    t0 = time.monotonic()
    ok, reason = True, None
    try:
        for job in uniq:
            ctx = w.prepare_context(job, window, version_cache, host)
            project, stack = ctx['project'], job['stack']
            base = {'task': job['task'], 'task_number': int(job['task'].split('-')[1]),
                    'stack': stack, 'versions': ctx['versions'], 'host_spec': host}
            for tool, argv, _expected in w.build_commands(stack, project, ctx['output']):
                warm = w.run_sandbox(ctx['context'], project, ctx['env'], argv,
                                     f"{job['task']}-{tool}-warmup", timed=True, caches={})
                if warm['exit_code'] != 0:
                    raise RuntimeError('warmup_failed')
                for rep in range(1, REPS + 1):
                    noop = w.run_sandbox(ctx['context'], project, ctx['env'], ['true'],
                                         f"{job['task']}-{tool}-noop-r{rep}", timed=True, caches={})
                    rows.append({**base, 'tool': tool, 'phase': 'sandbox_noop', 'rep': rep,
                                 'seconds': noop['seconds'], 'exit_code': noop['exit_code'],
                                 'load_average_before': noop['load_average_before'],
                                 'valid': noop['exit_code'] == 0})
                    sources = project_sources(stack, project)
                    if not sources:
                        raise RuntimeError('no_project_sources')
                    sizes = {p: p.stat().st_size for p in sources}
                    comment = w.COMMENT[stack]
                    for p in sources:
                        p.chmod(p.stat().st_mode | 0o600)
                        with p.open('ab') as handle:
                            handle.write(comment)
                    res = w.run_sandbox(ctx['context'], project, ctx['env'], argv,
                                        f"{job['task']}-{tool}-projfull-r{rep}", timed=True, caches={})
                    for p, size in sizes.items():
                        with p.open('r+b') as handle:
                            handle.truncate(size)
                        if p.stat().st_size != size:
                            raise RuntimeError('restore_failed')
                    rows.append({**base, 'tool': tool, 'phase': 'project_full_rebuild', 'rep': rep,
                                 'seconds': res['seconds'], 'exit_code': res['exit_code'],
                                 'project_source_files': len(sources),
                                 'project_source_bytes': sum(sizes.values()),
                                 'load_average_before': res['load_average_before'],
                                 'valid': res['exit_code'] == 0})
            shutil.rmtree(ctx['context'], ignore_errors=True)
        expected = 2 * REPS * sum(len(w.build_commands(j['stack'], pathlib.Path('/x'), pathlib.Path('/y'))) for j in uniq)
        ok = len(rows) == expected and all(r['valid'] for r in rows)
        reason = None if ok else 'count_or_exit_invalid'
    except Exception as exc:  # noqa: BLE001
        ok, reason = False, type(exc).__name__ + ':' + str(exc)[:200]
    finally:
        shutil.rmtree(window / 'contexts', ignore_errors=True)
    with (window / 'timings-supplement.jsonl').open('w') as out:
        for row in rows:
            out.write(json.dumps(row, sort_keys=True) + '\n')
    summary = {'valid': ok, 'reason': reason, 'started_at_utc': started,
               'finished_at_utc': w.utc_now(), 'worker_elapsed_seconds': round(time.monotonic() - t0, 3),
               'rows': len(rows), 'project_scratch_purged': not (window / 'contexts').exists(),
               'host_spec': host}
    (window / 'supplement-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
