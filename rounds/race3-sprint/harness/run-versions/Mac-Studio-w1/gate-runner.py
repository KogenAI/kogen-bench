#!/usr/bin/python3
# Run every gate on private copies of an existing dry cell. No start/arm launch.
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from selftest import FILES

R = Path(__file__).resolve().parent
METRICS = {'cold_ready_s', 'incremental_ready_s', 'startup_median_s', 'own_tests_s',
           'lint_findings', 'artifact_bytes', 'invocation_median_s', 'peak_rss_kb'}


def clone(source, dest):
    subprocess.run(['/bin/cp', '-c', '-p', '-R', str(source), str(dest)], check=True)


def rewrite(tree, old, new):
    for base, dirs, files in os.walk(tree):
        dirs[:] = [d for d in dirs if d not in ('.kitcache', '.git', 'target', '_build', 'build', 'deps', 'node_modules')]
        for name in files:
            file = Path(base) / name
            if file.is_symlink(): continue
            try:
                text = file.read_text()
                if '\0' not in text and old in text:
                    file.write_text(text.replace(old, new))
            except (UnicodeError, OSError):
                pass


def stage(source, dest):
    for name in FILES:
        shutil.copy2(R / name, dest / name)
    for name in ('BRIEF.tmpl', 'TARGET.md', 'SPEC-BUG-CASES.txt', 'EXCLUDED-V2.txt', 'COUNTS.txt', 'inputs.sha', 'env.sh'):
        shutil.copy2(R / name, dest / name)
    for name in ('BRIEF-rust.md', 'BRIEF-go.md', 'BRIEF-ts.md', 'BRIEF-gleam.md', 'BRIEF-ex.md'):
        shutil.copy2(R / name, dest / name)
    clone(R / 'inputs', dest / 'inputs')
    for name in ('ARMS', 'START', 'DEADLINE', 'CODEX_HOME', 'KIT-SHA256', 'CODEX-VERSION'):
        if (source / name).is_file(): shutil.copy2(source / name, dest / name)
    clone(source / 'out', dest / 'out')
    clone(source / 'snapshots', dest / 'snapshots')
    arms = (dest / 'ARMS').read_text().split()
    if not arms or not set(arms) <= {'rust', 'go', 'ts', 'gleam', 'ex'}:
        raise ValueError('ARMS must list registered race 3 arms')
    for arm in arms:
        live = source / arm
        clone(live if live.is_dir() else source / 'snapshots/FINAL' / arm, dest / arm)
        for name in ('spec', 'conformance'):
            if not (dest / arm / name).is_dir(): clone(dest / 'inputs' / name, dest / arm / name)
        if not (dest / arm / 'TARGET.md').is_file(): shutil.copy2(dest / 'TARGET.md', dest / arm / 'TARGET.md')
        rewrite(dest / arm, str(source), str(dest))
    rewrite(dest / 'snapshots', str(source), str(dest))
    return arms


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: test-gates.sh DRY_CELL_ROOT (or its out directory)')
    source = Path(sys.argv[1]).resolve()
    if source.name == 'out' and (source.parent / 'ARMS').is_file(): source = source.parent
    for name in ('ARMS', 'START', 'out', 'snapshots/FINAL'):
        if not (source / name).exists(): raise SystemExit('missing dry-cell input: %s' % (source / name))
    rows = []
    with tempfile.TemporaryDirectory(prefix='.gates-', dir=str(R)) as tmp:
        dest = Path(tmp); arms = stage(source, dest)
        def command(name, *args, root=dest):
            cmd = ['/bin/bash' if name.endswith('.sh') else '/usr/bin/python3', str(root / name)] + list(args)
            p = subprocess.run(cmd, cwd=str(dest), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            if p.returncode: raise AssertionError('%s (rc=%s): %s' % (name, p.returncode, p.stdout[-1500:]))
            return p.stdout
        def gate(name, fn):
            try:
                reason = fn() or 'ok'; rows.append((name, 'PASS', reason))
            except Exception as e:
                rows.append((name, 'FAIL', str(e).replace('\n', ' ')[:1600]))
            print('%s\t%s\t%s' % rows[-1], flush=True)
        print('gate\tresult\tdetail', flush=True)
        for test in ('checks', 'audit', 'receipts', 'scoring'):
            gate(test + '-selftest', lambda test=test: command('test-%s.sh' % test, root=R).strip())
        gate('checks', lambda: command('checks.sh') and 'pre-clock equality checks')
        gate('audit', lambda: command('audit.py') and 'dry-cell commands, hashes and receipts')
        def locks():
            d = dest / 'lock-fixture'; d.mkdir(); d.chmod(0o751)
            try:
                for host in ('macbook', 'studio'):
                    command('lock-%s.sh' % host, '--test-dir', str(d))
                    assert d.stat().st_mode & 0o777 == 0, 'lock did not set 000'
                    command('unlock.sh')
                    assert d.stat().st_mode & 0o777 == 0o751, 'unlock changed original mode'
                command('lock.sh', str(d), str(d))
                assert len((dest / 'locks.tsv').read_text().splitlines()) == 1, 'duplicate lock receipt'
                command('unlock.sh')
                assert not any((p.stat().st_mode & 0o777) == 0 for p in dest.iterdir() if p.is_dir()), 'directory left at 000'
            finally:
                d.chmod(0o751)
            return 'both host locks: 000 then exact 751 restore; duplicates checked'
        gate('lock-unlock', locks)
        def snap():
            command('snap.sh', 'GATE')
            text = (dest / 'out/snap-times.log').read_text().splitlines()[-1]
            seconds = float(text.split('copy_s=')[1])
            for arm in arms:
                for name in ('.spec.sha', '.conformance.sha', '.target.sha'):
                    assert (dest / 'snapshots/GATE' / arm / name).read_text().strip(), 'missing snapshot hash'
            assert seconds <= 20, 'snapshot took %ss (>20s; use 10-minute interval per PLAN)' % seconds
            return 'copy_s=%s (20s gate)' % seconds
        gate('snapshot', snap)
        def scoring():
            # Remove previous standalone FINAL row to avoid duplicate reporting.
            scores = dest / 'out/scores.tsv'
            old = scores.read_text() if scores.exists() else ''
            try:
                command('score-arm.sh', 'FINAL', arms[0])
                command('validate-results.py', str(dest / ('out/results/FINAL-%s.jsonl' % arms[0])))
            finally:
                scores.write_text(old)
            return 'one FINAL, complete frozen case inventory'
        gate('score-arm', scoring)
        def metrics():
            command('metrics.py'); command('final-metrics.sh')
            report = json.loads((dest / 'out/metrics.json').read_text())
            required = {'curve', 'final_total', 'final_scored', 't75', 't90', 't_target', 't100', 'ended', 'turns', 'cpu_s',
                        'tokens', 'cmd_time_s', 'turn_wall_s', 'model_wait_s', 'build_output_kb', 'loc', 'test_defs',
                        'stall_waits', 't_target_adj', 't75_adj', 't90_adj', 't100_adj', 'audit_flags', 'quota_points'}
            def present(value):
                if isinstance(value, dict): return all(present(v) for v in value.values())
                if isinstance(value, (list, tuple)): return all(present(v) for v in value)
                if value is None or value == '': return False
                if isinstance(value, str) and value.startswith('n/a'): return value.startswith('n/a (') and value.endswith(')')
                return True
            for arm in arms:
                assert required <= set(report[arm]) and present(report[arm]), 'missing/unexplained metric: ' + arm
            table = [line.split('\t') for line in (dest / 'out/final-metrics.tsv').read_text().splitlines()]
            for arm in arms:
                arm_rows = [row for row in table if row[0] == arm]
                assert {row[1] for row in arm_rows} == METRICS and len(arm_rows) == len(METRICS), 'missing FINAL metric: ' + arm
                assert all(len(row) == 4 and row[2] and row[3] for row in arm_rows), 'missing value/method/reason'
            markdown = (dest / 'out/METRICS.md').read_text()
            assert 'None' not in markdown and len([l for l in markdown.splitlines() if l.startswith('|')]) == len(arms) + 2
            return 'all fields present or n/a with reason in both tables'
        gate('metrics', metrics)
        def receipts():
            command('receipts.py')
            rows = (dest / 'out/receipts.tsv').read_text().splitlines()[1:]
            turns = sum(len(list((dest / 'out' / a).glob('turn-*.jsonl'))) for a in arms)
            assert len(rows) == turns and all(len(row.split('\t')) == 4 for row in rows)
            return '%s turn receipts' % turns
        gate('receipts', receipts)
    return any(status == 'FAIL' for _, status, _ in rows)


if __name__ == '__main__':
    sys.exit(main())
