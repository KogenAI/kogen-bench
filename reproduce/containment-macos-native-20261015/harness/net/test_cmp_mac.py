"""Fake-backed tests for cmp_mac.py. No sandbox arm, fixture or live cell runs here.

Process observation goes through the production parser (scan_marked / observe_pid)
against a fake `ps` executable that prints a JSON-described process world; os.kill
is replaced by a function that edits that world, so cleanup and signal paths run
their real code without touching any real process.
"""
import importlib.util, itertools, json, os, pathlib, signal, subprocess, sys, tempfile, time, unittest
from unittest import mock

import cmp_mac as c

FAKE_PS = r'''
import json, os, sys
w = json.load(open(os.environ["FAKE_PS_WORLD"]))
n = w.get("calls", 0); w["calls"] = n + 1
json.dump(w, open(os.environ["FAKE_PS_WORLD"], "w"))
if n in w.get("fail_calls", []) or w.get("fail"):
    sys.stderr.write("ps: simulated failure\n"); sys.exit(1)
def fmt(r): return r["raw"] if "raw" in r else "%5d %5d %5d %5d %s %s" % (r["uid"], r["pid"], r["ppid"], r["pgid"], r["lstart"], r["command"])
args = sys.argv[1:]
if "-p" in args:
    pid = int(args[args.index("-p") + 1]); rows = [r for r in w["rows"] if r["pid"] == pid]
    if not rows: sys.exit(1)
    print(fmt(rows[0])); sys.exit(0)
out = "\n".join(fmt(r) for r in w["rows"])
sys.stdout.write(out if w.get("no_trailing_newline") else out + "\n")
'''

LSTART = 'Thu Oct 15 12:00:00 2026'


class FakeWorld:
    def __init__(self, root):
        self.path = pathlib.Path(root) / 'world.json'
        self.script = pathlib.Path(root) / 'fake_ps.py'
        self.script.write_text(FAKE_PS)
        self.kills = []
        self.on_kill = None
        self.write({'rows': []})

    def write(self, w):
        w.setdefault('rows', [])
        self.path.write_text(json.dumps(w))

    def read(self):
        return json.loads(self.path.read_text())

    def set_rows(self, rows, **extra):
        w = self.read(); w.update(extra); w['rows'] = [self.own()] + rows; self.write(w)

    def own(self):
        return row(os.getpid(), 1, os.getpid(), 'python3 harness', uid=os.geteuid())

    def kill(self, pid, sig):
        self.kills.append((pid, sig))
        w = self.read()
        hit = [r for r in w['rows'] if r['pid'] == pid]
        if not hit: raise ProcessLookupError(pid)
        if self.on_kill: self.on_kill(w, pid, sig)
        elif not (sig == signal.SIGTERM and hit[0].get('ignore_term')):
            w['rows'] = [r for r in w['rows'] if r['pid'] != pid]
        self.write(w)


def row(pid, ppid, pgid, command, uid=None, lstart=LSTART, **extra):
    r = {'uid': os.geteuid() if uid is None else uid, 'pid': pid, 'ppid': ppid, 'pgid': pgid, 'lstart': lstart, 'command': command}
    r.update(extra)
    return r


def marked(marker, pid, ppid=1, pgid=None, role='', fixture='setsid', **extra):
    cmd = '%s -I -S %s %s%s CMPMAC_RUN_MARKER=%s PATH=/usr/bin:/bin CMPMAC_RUN_MARKER=%s' % (
        c.PYTHON, c.FIXTURE_SCRIPT, ('survivor-child ' if role == 'survivor' else ''), fixture, marker, marker)
    return row(pid, ppid, pgid if pgid is not None else pid, cmd, **extra)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name).resolve()
        self.world = FakeWorld(self.root)
        self.real_kill = os.kill
        self.patches = [
            mock.patch.object(c, 'PS_SCAN_ARGV', [sys.executable, str(self.world.script), '-axo']),
            mock.patch.object(c, 'PS_PID_ARGV', [sys.executable, str(self.world.script), '-o', 'x', '-p']),
            mock.patch.dict(os.environ, {'FAKE_PS_WORLD': str(self.world.path)}),
            mock.patch.object(c.os, 'kill', self.world.kill),
            mock.patch.object(c, 'read_load', lambda: 1.0),
            mock.patch.object(c, 'RESULTS', self.root / 'results'),
            mock.patch.object(c, 'RUNS', self.root / 'runs'),
            mock.patch.object(c, 'FIXTURE_LIFETIME', 0.2),
            mock.patch.object(c, 'SETTLE', 0.01),
            mock.patch.object(c, 'READY_TIMEOUT', 2.0),
            mock.patch.object(c.time, 'sleep', lambda s: None),
        ]
        for p in self.patches: p.start()
        c.safe_mkdir(c.RESULTS); c.safe_mkdir(c.RUNS)
        probe = self.root / 'exec-probe'; probe.write_bytes(b'\xcf\xfa\xed\xfe fake')
        self.patches.append(mock.patch.object(c, 'EXEC_PROBE', probe)); self.patches[-1].start()

    def tearDown(self):
        for p in reversed(self.patches): p.stop()
        self.tmp.cleanup()


# ------------------------------------------------------------------ observer and cleanup (REVIEW-MAC3 #1)

class ObserverTests(Base):
    def test_scan_uses_one_schema_and_exact_marker_tokens(self):
        m = 'a' * 32
        self.world.set_rows([marked(m, 101), row(102, 1, 102, 'x CMPMAC_RUN_MARKER=%sx' % m), row(103, 1, 103, 'x CMPMAC_RUN_MARKER=%s' % m, uid=os.geteuid() + 1),
                             row(104, 1, 104, 'x XCMPMAC_RUN_MARKER=%s' % m)])
        rows = c.scan_marked(m)
        self.assertEqual([r['pid'] for r in rows], [101])
        self.assertEqual(set(rows[0]) >= {'uid', 'pid', 'ppid', 'pgid', 'lstart', 'argv0', 'tokens'}, True)
        self.assertEqual(rows[0]['lstart'], LSTART)
        self.assertEqual(c.identity_key(rows[0]), c.identity_key(c.observe_pid(101)))

    def test_final_unterminated_line_uses_the_exact_parser(self):
        m = 'b' * 32
        self.world.set_rows([row(201, 1, 201, 'x CMPMAC_RUN_MARKER=%szzz' % m)], no_trailing_newline=True)
        self.assertEqual(c.scan_marked(m), [])
        self.world.set_rows([marked(m, 202)], no_trailing_newline=True)
        self.assertEqual([r['pid'] for r in c.scan_marked(m)], [202])

    def test_scan_failure_and_incomplete_scan_are_observer_errors(self):
        self.world.set_rows([], fail=True)
        with self.assertRaises(c.ObserverError): c.scan_marked('c' * 32)
        w = self.world.read(); w['fail'] = False; w['rows'] = []; self.world.write(w)
        with self.assertRaises(c.ObserverError): c.scan_marked('c' * 32)   # own process absent

    def test_cleanup_kills_marked_identity_and_proves_absence(self):
        m = 'd' * 32
        self.world.set_rows([marked(m, 301), marked(m, 302, ppid=301), row(303, 1, 303, 'unrelated')])
        rec = c.cleanup_marker(m)
        self.assertTrue(rec['pass'])
        self.assertEqual(sorted(p for p, s in self.world.kills), [301, 302])
        self.assertTrue(all(s == signal.SIGKILL for p, s in self.world.kills))
        self.assertIn(303, [r['pid'] for r in self.world.read()['rows']])

    def test_reused_pid_is_not_signalled(self):
        m = 'e' * 32
        self.world.set_rows([marked(m, 401)])
        r = c.scan_marked(m)[0]
        self.world.set_rows([marked(m, 401, lstart='Thu Oct 15 12:00:09 2026')])
        self.assertEqual(c.signal_identity(r, m, signal.SIGKILL), 'mismatch')
        self.world.set_rows([row(401, 1, 401, 'other process')])
        self.assertEqual(c.signal_identity(r, m, signal.SIGKILL), 'mismatch')
        self.assertEqual(self.world.kills, [])

    def test_disappearance_during_cleanup_is_gone_not_error(self):
        m = 'f' * 32
        self.world.set_rows([marked(m, 501)])
        r = c.scan_marked(m)[0]
        self.world.set_rows([])
        self.assertEqual(c.signal_identity(r, m, signal.SIGKILL), 'gone')
        self.assertTrue(c.cleanup_marker(m)['pass'])

    def test_unkillable_marked_process_fails_cleanup(self):
        m = '1' * 32
        self.world.set_rows([marked(m, 601)])
        self.world.on_kill = lambda w, pid, sig: None
        clock = itertools.chain([0.0], itertools.repeat(100.0))
        with mock.patch.object(c.time, 'monotonic', lambda: next(clock)):
            with self.assertRaises(c.CleanupError): c.cleanup_marker(m, budget=1.0)

    def test_observer_loss_waits_for_lifetimes_then_requires_complete_scan(self):
        m = '2' * 32
        self.world.set_rows([marked(m, 701)], fail_calls=[0, 1])
        rec = c.cleanup_marker(m)
        self.assertTrue(rec['pass']); self.assertEqual(len(rec['observer_errors']), 2)
        self.world.set_rows([marked(m, 702)], fail=True, calls=0)
        with self.assertRaises(c.CleanupError): c.cleanup_marker(m)
        self.assertEqual(self.world.kills, [(701, signal.SIGKILL)])     # never a broadened selection


# ------------------------------------------------------------------ survivors (REVIEW-MAC3 #4)

class FakeRunner:
    def __init__(self, world, pid, on_term=None, exited=False, log=None):
        self.world, self.pid, self.on_term = world, pid, on_term
        self.returncode = 0 if exited else None
        self.signals = []
        self.cmpmac_log = log

    def poll(self): return self.returncode

    def send_signal(self, sig):
        self.signals.append(sig)
        if self.on_term: self.on_term(self.world)
        self.returncode = -sig

    def kill(self): self.send_signal(signal.SIGKILL)

    def wait(self, timeout=None): return self.returncode


class SurvivorTests(Base):
    def run_case(self, fixture, rows_before, survivor_pid, killed_by_arm, runner_pid=900, runner_exited=False, ready=True,
                 ready_pid=None, mutate=None):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'x', c.RUNS), light=True)
        rows = [dict(r, command=r['command'].replace('@@M@@', cell.marker)) for r in rows_before]
        self.world.set_rows(rows)
        if ready:
            cell.paths['survivor-ready'].write_text(json.dumps({'pid': ready_pid or survivor_pid, 'mode': fixture}))

        def on_term(world):
            w = world.read()
            if killed_by_arm: w['rows'] = [r for r in w['rows'] if r['pid'] != survivor_pid]
            if mutate: mutate(w)
            world.write(w)
        runner = FakeRunner(self.world, runner_pid, on_term=on_term, exited=runner_exited, log=str(self.root / 'none.log'))
        if runner_exited and killed_by_arm is not None:
            pass
        ev = c.observe_survivor(fixture, cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'])
        return ev, c.score(fixture, ev), runner

    def survivor_rows(self, fixture, pid=950, ppid=1, pgid=None, leader=None):
        rows = [marked('@@M@@', pid, ppid=ppid, pgid=pgid if pgid is not None else pid, role='survivor', fixture=fixture)]
        if leader: rows.append(marked('@@M@@', leader, ppid=900, pgid=900, fixture=fixture))
        return rows

    def test_setsid_blocked_and_not_blocked(self):
        for killed, expected in ((True, 'BLOCKED'), (False, 'NOT-BLOCKED')):
            ev, sc, runner = self.run_case('setsid', self.survivor_rows('setsid', ppid=900, pgid=950, leader=None), 950, killed)
            self.assertEqual(sc['outcome'], expected, ev)
            self.assertEqual(runner.signals[0], signal.SIGTERM)

    def test_double_fork_requires_escaped_group(self):
        ev, sc, _ = self.run_case('double_fork', self.survivor_rows('double_fork', ppid=1, pgid=940), 950, False)
        self.assertEqual(sc['outcome'], 'NOT-BLOCKED')
        ev, sc, _ = self.run_case('double_fork', self.survivor_rows('double_fork', ppid=1, pgid=900), 950, False)
        self.assertEqual(sc['outcome'], 'INVALID')       # still in the runner's group: property not observed

    def test_leader_exit_first_with_early_leader_exit(self):
        ev, sc, runner = self.run_case('leader_exit_first', self.survivor_rows('leader_exit_first', ppid=1, pgid=900), 950, None, runner_exited=True)
        self.assertEqual(sc['outcome'], 'NOT-BLOCKED')
        self.assertEqual(ev['protocol']['teardown']['steps'], ['already-exited'])

    def test_term_ignoring_requires_observed_survival_of_sigterm(self):
        rows = self.survivor_rows('term_ignoring', ppid=900, pgid=900)
        rows[0]['ignore_term'] = True
        ev, sc, _ = self.run_case('term_ignoring', rows, 950, False)
        self.assertEqual(sc['outcome'], 'NOT-BLOCKED'); self.assertTrue(ev['protocol']['term_survived_live'])
        rows[0]['ignore_term'] = False
        ev, sc, _ = self.run_case('term_ignoring', rows, 950, False)
        self.assertEqual(sc['outcome'], 'INVALID')

    def test_reparent_requires_observed_ppid_transition(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'y', c.RUNS), light=True)
        m = cell.marker
        before = [marked(m, 950, ppid=960, pgid=900, role='survivor', fixture='reparent_to_init'), marked(m, 960, ppid=900, pgid=900, fixture='reparent_to_init')]
        after = [marked(m, 950, ppid=1, pgid=900, role='survivor', fixture='reparent_to_init')]
        self.world.set_rows(before)
        cell.paths['survivor-ready'].write_text(json.dumps({'pid': 950, 'mode': 'reparent_to_init'}))
        real_exclusive = c.exclusive

        def release(path, data):
            st = real_exclusive(path, data); self.world.set_rows(after); return st
        runner = FakeRunner(self.world, 900, exited=True, log=str(self.root / 'none.log'))
        with mock.patch.object(c, 'exclusive', release):
            ev = c.observe_survivor('reparent_to_init', cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'])
        self.assertEqual(c.score('reparent_to_init', ev)['outcome'], 'NOT-BLOCKED', ev)
        self.assertEqual([t['phase'] for t in ev['protocol']['transitions']], ['initial', 'reparented'])

    def test_missing_ready_witness_is_invalid_for_every_survivor(self):
        for f in c.SURVIVORS:
            ev, sc, _ = self.run_case(f, self.survivor_rows(f, ppid=1, pgid=940), 950, False, ready=False)
            self.assertEqual(sc['outcome'], 'INVALID', f)
            ev, sc, _ = self.run_case(f, self.survivor_rows(f, ppid=1, pgid=940), 950, False, ready_pid=951)
            self.assertEqual(sc['outcome'], 'INVALID', f)

    @mock.patch.object(c, 'READY_TIMEOUT', 0.3)
    def test_no_survivor_row_is_invalid_not_blocked(self):
        for f in c.SURVIVORS:
            ev, sc, runner = self.run_case(f, [], 950, True)
            self.assertEqual(sc['outcome'], 'INVALID', f)
            self.assertTrue(runner.signals, 'teardown must still run')

    def test_observer_failure_is_invalid_for_every_survivor(self):
        for f in c.SURVIVORS:
            cell = c.Cell(c.safe_makedirs(c.RUNS / 'z', c.RUNS), light=True)
            self.world.set_rows([], fail=True)
            runner = FakeRunner(self.world, 900, log=str(self.root / 'none.log'))
            ev = c.observe_survivor(f, cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'])
            self.assertEqual(c.score(f, ev)['outcome'], 'INVALID', f)
            self.assertTrue(runner.signals)
            w = self.world.read(); w['fail'] = False; self.world.write(w)

    def test_changed_identity_after_teardown_is_not_the_survivor(self):
        def reuse(w):
            for r in w['rows']:
                if r['pid'] == 950: r['lstart'] = 'Thu Oct 15 12:00:30 2026'
        ev, sc, _ = self.run_case('setsid', self.survivor_rows('setsid', ppid=900, pgid=950), 950, False, mutate=reuse)
        self.assertEqual(sc['outcome'], 'BLOCKED')
        self.assertEqual(ev['protocol']['post_rows'], [])

    def test_post_scan_after_possible_self_expiry_is_invalid(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'old', c.RUNS), light=True)
        cell.started -= c.FIXTURE_LOOP_LIFETIME          # cell began 25 s ago
        self.world.set_rows([marked(cell.marker, 950, ppid=900, pgid=950, role='survivor')])
        cell.paths['survivor-ready'].write_text(json.dumps({'pid': 950, 'mode': 'setsid'}))

        def gone(world):
            w = world.read(); w['rows'] = [r for r in w['rows'] if r['pid'] != 950]; world.write(w)
        runner = FakeRunner(self.world, 900, on_term=gone, log=str(self.root / 'none.log'))
        ev = c.observe_survivor('setsid', cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'])
        self.assertEqual(c.score('setsid', ev)['outcome'], 'INVALID')

    def test_unstable_identity_never_establishes_readiness(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'u', c.RUNS), light=True)
        cell.paths['survivor-ready'].write_text(json.dumps({'pid': 950, 'mode': 'setsid'}))
        counter = {'n': 0}
        real = c.scan_marked

        def flapping(marker, timeout=10.0):
            counter['n'] += 1
            self.world.set_rows([marked(marker, 950, ppid=900, pgid=950, role='survivor', lstart='Thu Oct 15 12:00:%02d 2026' % (counter['n'] % 60))])
            return real(marker, timeout)
        runner = FakeRunner(self.world, 900, log=str(self.root / 'none.log'))
        with mock.patch.object(c, 'scan_marked', flapping), mock.patch.object(c, 'READY_TIMEOUT', 0.3):
            ev = c.observe_survivor('setsid', cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'])
        self.assertEqual(c.score('setsid', ev)['outcome'], 'INVALID')


# ------------------------------------------------------------------ executor, interruption, cleanup failure (REVIEW-MAC3 #2/#3)

class ExecutorTests(Base):
    def test_interrupt_during_cell_runs_protected_cleanup_and_leaves_incomplete_ledger(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'r1', c.RESULTS)
        cleaned = []
        with mock.patch.object(c, 'execute_escape', side_effect=c.Interrupted(signal.SIGTERM)), \
             mock.patch.object(c, 'cleanup_marker', lambda m, started=None, budget=8.0: cleaned.append(m) or {'pass': True, 'signals': []}):
            with self.assertRaises(c.Interrupted): c.run_cell('z-unsandboxed', 'fs_read_outside', 1, run_dir)
        events = c.ledger_events(run_dir / 'ledger.jsonl')
        self.assertEqual([e['event'] for e in events], ['begin'])
        self.assertEqual(cleaned, [events[0]['marker']])
        with mock.patch.object(c, 'cleanup_marker', lambda m, started=None, budget=8.0: {'pass': True, 'signals': [], 'marker': m}):
            rec = c.recover_begun(run_dir)
        self.assertEqual(rec, [{'key': 'z-unsandboxed/fs_read_outside/1', 'marker': events[0]['marker'], 'absence_verified': True}])

    def test_cleanup_failure_aborts_the_matrix(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'r2', c.RESULTS)
        plan = [('z-unsandboxed', 'fs_read_outside', 1), ('z-unsandboxed', 'secret_file', 1)]
        calls = []

        def fake_escape(arm, fixture, cell, holder):
            calls.append(fixture); return {'valid': False, 'error': 'fake'}

        def failing_cleanup(m, started=None, budget=8.0): raise c.CleanupError('remains')
        with mock.patch.object(c, 'execute_escape', fake_escape), mock.patch.object(c, 'cleanup_marker', failing_cleanup):
            with self.assertRaises(c.CleanupError): c.run_cells(run_dir, plan)
        self.assertEqual(calls, ['fs_read_outside'])
        self.assertIn('cleanup_failure', [e['event'] for e in c.ledger_events(run_dir / 'ledger.jsonl')])

    def test_resume_refuses_tampered_evidence(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'r3', c.RESULTS)
        plan = [('z-unsandboxed', 'memory', 1)]
        c.run_cells(run_dir, plan)
        p = c.evidence_path(run_dir, 'z-unsandboxed', 'memory', 1)
        p.write_text(p.read_text().replace('UNSUPPORTED', 'BLOCKED'))
        with self.assertRaises(RuntimeError): c.run_cells(run_dir, plan)

    def test_load_abort_mid_build_kills_and_cleans(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'b', c.RUNS), light=True)
        cleaned = []
        ticks = {'n': 0}

        def tick(force=False):
            ticks['n'] += 1
            if ticks['n'] > 1: raise c.LoadAbort('load guard: one-minute load 20 above 12')
        with mock.patch.object(c, 'guard_tick', tick), mock.patch.object(c.os, 'kill', self.real_kill), \
             mock.patch.object(c, 'cleanup_marker', lambda m, started=None, budget=8.0: cleaned.append(m) or {'pass': True}):
            with self.assertRaises(c.LoadAbort):
                c.monitored([sys.executable, '-c', 'import time; time.sleep(30)'], self.root, {'PATH': '/usr/bin:/bin'}, cell, timeout=60)
        self.assertEqual(cleaned, [cell.marker])

    def test_failed_overhead_sample_marks_arm_invalid_and_cleans(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'r4', c.RESULTS)
        cleaned = []

        class Dead:
            pid = 1; returncode = 127; cmpmac_log = str(self.root / 'none.log')
            def poll(self): return 127
            def wait(self, timeout=None): return 127
            def kill(self): pass
        with mock.patch.object(c, 'start_runner', lambda argv, env, cwd, cell: cell.runners.append(Dead()) or cell.runners[-1]), \
             mock.patch.object(c, 'cleanup_marker', lambda m, started=None, budget=8.0: cleaned.append(m) or {'pass': True}):
            out = c.overhead(run_dir, ['z-unsandboxed'])
        self.assertEqual(out['z-unsandboxed']['outcome'], 'INVALID')
        self.assertIn('rc=127', out['z-unsandboxed']['reason'])
        events = c.ledger_events(run_dir / 'ledger.jsonl')
        self.assertEqual([e['event'] for e in events], ['begin', 'complete'])
        self.assertEqual(events[1]['outcome'], 'FAILED'); self.assertEqual(cleaned, [events[0]['marker']])

    def test_timed_wait_stamps_real_exit(self):
        with mock.patch.object(c.os, 'kill', self.real_kill):
            t0 = time.perf_counter()
            p = subprocess.Popen([sys.executable, '-c', 'pass'])
            t1 = c.timed_wait(p, 20)
            self.assertIsNotNone(t1); self.assertGreater(t1, t0); self.assertEqual(p.returncode, 0)
            q = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])
            self.assertIsNone(c.timed_wait(q, 0.2)); self.assertIsNotNone(q.returncode)

    def test_signal_handler_raises_interrupted(self):
        with self.assertRaises(c.Interrupted): c._raise_interrupt(signal.SIGTERM, None)


# ------------------------------------------------------------------ gate and command paths (REVIEW-MAC3 #3)

def manifest(d): return {'digest': d}


class GateTests(Base):
    def passing_controls(self):
        return [mock.patch.object(c, 'observer_preflight', lambda root: (True, {})),
                mock.patch.object(c, 'run_cell', lambda arm, f, rep, run_dir, hold=False: {'outcome': 'PASS' if f == c.POSITIVE else 'NOT-BLOCKED', 'reason': 'fake'}),
                mock.patch.object(c, 'interrupt_control', lambda m: (True, {})),
                mock.patch.object(c, 'nono_refusal_probe', lambda run_dir: {'refused': True}),
                mock.patch.object(c, 'gate_refusal_controls', lambda m, arms: (True, {}))]

    def run_check(self, extra=(), digests=('d1', 'd1')):
        seq = iter(digests)
        ps = self.passing_controls() + list(extra) + [mock.patch.object(c, 'apparatus_manifest', lambda: manifest(next(seq)))]
        for p in ps: p.start()
        try:
            with mock.patch('builtins.print'):
                return c.check(list(c.ARMS))
        finally:
            for p in reversed(ps): p.stop()

    def test_all_controls_pass(self):
        self.assertEqual(self.run_check(), 0)
        self.assertEqual(c.require_gate(manifest('d1'), c.ARMS)['gate'], 'PASS')

    def test_every_required_control_failure_is_nonzero_and_withdraws_pass(self):
        failing = {
            'observer': mock.patch.object(c, 'observer_preflight', lambda root: (False, {})),
            'positive': mock.patch.object(c, 'run_cell', lambda arm, f, rep, run_dir, hold=False: {'outcome': 'FAIL' if f == c.POSITIVE else 'NOT-BLOCKED', 'reason': 'x'}),
            'z-negative': mock.patch.object(c, 'run_cell', lambda arm, f, rep, run_dir, hold=False: {'outcome': 'PASS' if f == c.POSITIVE else 'BLOCKED', 'reason': 'x'}),
            'interrupt': mock.patch.object(c, 'interrupt_control', lambda m: (False, {})),
            'nono': mock.patch.object(c, 'nono_refusal_probe', lambda run_dir: {'refused': False}),
            'gate': mock.patch.object(c, 'gate_refusal_controls', lambda m, arms: (False, {})),
            'scorer': mock.patch.object(c, 'scorer_controls', lambda: (['scorer x'], {})),
            'cleanup': mock.patch.object(c, 'interrupt_control', mock.Mock(side_effect=c.CleanupError('remains'))),
            'load': mock.patch.object(c, 'interrupt_control', mock.Mock(side_effect=c.LoadAbort('load guard'))),
            'observer-raises': mock.patch.object(c, 'observer_preflight', mock.Mock(side_effect=c.ObserverError('ps failed'))),
            'interrupted': mock.patch.object(c, 'interrupt_control', mock.Mock(side_effect=c.Interrupted(signal.SIGTERM))),
        }
        for name, patch in failing.items():
            self.assertEqual(self.run_check(), 0)
            rc = self.run_check(extra=[patch])
            self.assertNotEqual(rc, 0, name)
            with self.assertRaises(c.GateRefused, msg=name): c.require_gate(manifest('d1'), c.ARMS)

    def test_apparatus_change_during_check_fails(self):
        self.assertNotEqual(self.run_check(digests=('d1', 'd2')), 0)
        for d in ('d1', 'd2'):
            with self.assertRaises(c.GateRefused): c.require_gate(manifest(d), c.ARMS)

    def test_gate_refuses_missing_changed_and_uncovered(self):
        with self.assertRaises(c.GateRefused): c.require_gate(manifest('d1'), c.ARMS)
        self.assertEqual(self.run_check(), 0)
        with self.assertRaises(c.GateRefused): c.require_gate(manifest('changed-executable'), c.ARMS)
        report = c.RESULTS / json.loads((c.RESULTS / 'LATEST-CHECK.json').read_text())['report']
        report.write_text(report.read_text().replace('"PASS"', '"PASS" '))
        with self.assertRaises(c.GateRefused): c.require_gate(manifest('d1'), c.ARMS)

    @mock.patch.object(c.signal, 'signal', lambda s, h: None)
    def test_dry_measure_and_resume_command_paths_refuse_without_gate(self):
        with mock.patch.object(c, 'apparatus_manifest', lambda: manifest('d1')), mock.patch('sys.stderr'):
            for cmd in (['dry'], ['measure'], ['dry', '--arms', 'z-unsandboxed']):
                self.assertEqual(c.main(cmd), 2, cmd)
        self.assertEqual(self.run_check(), 0)
        with mock.patch.object(c, 'apparatus_manifest', lambda: manifest('d2')), mock.patch('sys.stderr'):
            self.assertEqual(c.main(['dry']), 2)
        ran = []
        with mock.patch.object(c, 'apparatus_manifest', lambda: manifest('d1')), \
             mock.patch.object(c, 'run_cells', lambda run_dir, plan, hold_fixture=None: ran.append(len(plan))), \
             mock.patch.object(c, 'overhead', lambda run_dir, arms: {}), \
             mock.patch.object(c, 'matrix_report', lambda run_dir, plan, meta: []), mock.patch('builtins.print'):
            self.assertEqual(c.main(['dry']), 0)
            self.assertEqual(ran, [len(c.ARMS) * len(c.FIXTURES)])
            run_id = sorted(p.name for p in c.RESULTS.iterdir() if p.name.startswith('dry-'))[0]
            meta = json.loads((c.RESULTS / run_id / 'run.json').read_text())
        with mock.patch.object(c, 'apparatus_manifest', lambda: manifest('d3')), mock.patch('sys.stderr'):
            self.assertEqual(c.main(['resume', run_id]), 2)
        self.assertEqual(meta['apparatus_digest'], 'd1')
        with mock.patch.object(c, 'apparatus_manifest', lambda: manifest('d1')), mock.patch('sys.stderr'):
            self.assertEqual(c.main(['_worker', run_id]), 2)     # _worker only serves the interrupt control

    def test_pinned_input_mismatch_refuses_manifest(self):
        (self.root / 'pinned.bin').write_bytes(b'pinned')
        with mock.patch.object(c, 'WORK', self.root):
            with mock.patch.object(c, 'PINS', {'x': ('pinned.bin', '0' * 64)}):
                with self.assertRaisesRegex(c.GateRefused, 'pin mismatch'): c.apparatus_manifest()
            with mock.patch.object(c, 'PINS', {'absent': ('vendor/absent-binary', None)}):
                with self.assertRaisesRegex(c.GateRefused, 'missing'): c.apparatus_manifest()


# ------------------------------------------------------------------ paths and launch environments (REVIEW-MAC3 #5)

class PathTests(Base):
    def test_safe_write_rejects_symlinked_destinations(self):
        real = c.safe_mkdir(self.root / 'real')
        (self.root / 'link').symlink_to(real)
        with self.assertRaises(RuntimeError): c.safe_write(self.root / 'link' / 'x.json', '{}')
        (real / 'target').write_text('x'); (real / 'sym').symlink_to(real / 'target')
        with self.assertRaises(RuntimeError): c.safe_write(real / 'sym', 'y')
        os.link(real / 'target', real / 'hard')
        with self.assertRaises(RuntimeError): c.safe_write(real / 'hard', 'y')
        c.safe_write(real / 'ok.json', '{}'); self.assertEqual((real / 'ok.json').read_text(), '{}')

    def test_group_writable_directory_refused(self):
        d = c.safe_mkdir(self.root / 'gw'); os.chmod(d, 0o777)
        with self.assertRaises(RuntimeError): c.safe_write(d / 'x', 'y')

    def test_ledger_append_refuses_symlink(self):
        d = c.safe_mkdir(self.root / 'led'); (d / 'target').write_text('')
        (d / 'ledger.jsonl').symlink_to(d / 'target')
        with self.assertRaises(OSError): c.safe_append_jsonl(d / 'ledger.jsonl', {'a': 1})

    def test_every_arm_launch_has_run_local_home_and_temp(self):
        plan = {'path': '/usr/bin/sandbox-exec', 'args': ['/usr/bin/sandbox-exec', '-p', '(version 1)'], 'cwd': 'x', 'env': [], 'stdin_closed': True, 'profile': '(version 1)'}
        short = tempfile.TemporaryDirectory(dir='/private/tmp'); self.addCleanup(short.cleanup)   # srt socket path budget
        runs = pathlib.Path(short.name).resolve()
        for arm in c.ARMS:
            cell = c.Cell(c.safe_makedirs(runs / 'l', runs))
            env = c.parent_env(cell)
            with mock.patch.object(c, 'kogen_launch_plan', lambda pol: dict(plan, env=['%s=%s' % kv for kv in pol['Env'].items()])):
                argv, lenv, cwd, cfg = c.build_launch(arm, c.fixture_command('env_secret', cell), cell, env)
            for key in ('HOME', 'TMPDIR'):
                self.assertTrue(pathlib.Path(lenv[key].rstrip('/')).is_dir(), (arm, key))
                c.under(lenv[key].rstrip('/'), cell.dir)
            self.assertEqual(cwd, str(cell.allowed))
            if arm == 'b-sandbox-runtime-0.0.78':
                self.assertEqual(argv[argv.index('--') + 1:], c.fixture_command('env_secret', cell))
                self.assertEqual(lenv['CLAUDE_CODE_TMPDIR'], str(cell.tmp))
                settings = json.loads((cell.apparatus / 'srt-settings.json').read_text())
                self.assertEqual(settings['filesystem']['denyRead'], [str(c.REAL_HOME)])
                deployed_tmp = '$HOME/Scratch.noindex/contain-cmp-mac/runs/' + 'x' * 8 + '/c' + 'x' * 10 + '/tmp'
                self.assertLess(len(deployed_tmp) + len('/srt-mux-99999-0.sock'), 104)
            if arm == 'a-kogen-seatbelt':
                self.assertNotIn('CMPMAC_SECRET_ENV_TOKEN', lenv)
                self.assertEqual(cfg['policy']['Network'], 'deny')
                self.assertIn(str(cell.allowed), cfg['policy']['Write'])
            else:
                self.assertEqual(lenv['CMPMAC_SECRET_ENV_TOKEN'], cell.token + '-ENV')
            if arm == 'c-nono-0.79.0':
                self.assertNotIn(str(cell.home), argv)
            if arm == 'd-codex-seatbelt-0.162.1':
                c.under(lenv['CODEX_HOME'], cell.home)

    def test_srt_refuses_socket_path_overflow(self):
        deep = c.safe_makedirs(c.RUNS / ('d' * 60), c.RUNS)
        cell = c.Cell(deep)
        with self.assertRaisesRegex(RuntimeError, 'too long'):
            c.build_launch('b-sandbox-runtime-0.0.78', ['x'], cell, c.parent_env(cell))

    def test_launch_refuses_missing_cell_directory(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'm', c.RUNS))
        os.rmdir(cell.tmp)
        with self.assertRaises(RuntimeError): c.build_launch('z-unsandboxed', ['x'], cell, c.parent_env(cell))


# ------------------------------------------------------------------ environment witness (REVIEW-MAC3 #6)

class EnvWitnessTests(Base):
    def outcome(self, witness, receipts=('environment_checked', 'fixture_complete')):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'e', c.RUNS))
        if witness is not None: cell.paths['env-witness'].write_bytes(witness)
        ev = c.env_evidence(cell, list(receipts)); ev['completed'] = 'fixture_complete' in receipts
        return c.score('env_secret', ev)['outcome'], cell

    def test_exact_absent_altered_empty_missing_malformed(self):
        def w(present, value): return json.dumps({'present': present, 'value': value}).encode()
        out, cell = self.outcome(b'')
        self.assertEqual(out, 'INVALID')
        for data, expected in ((None, 'INVALID'), (b'not json', 'INVALID'), (w(True, 'TOKEN-wrong-ENV'), 'INVALID'),
                               (w(True, ''), 'INVALID'), (w(False, ''), 'BLOCKED'), (json.dumps({'present': 'yes', 'value': ''}).encode(), 'INVALID')):
            self.assertEqual(self.outcome(data)[0], expected, data)
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'e', c.RUNS))
        cell.paths['env-witness'].write_bytes(w(True, cell.token + '-ENV'))
        ev = c.env_evidence(cell, ['environment_checked', 'fixture_complete']); ev['completed'] = True
        self.assertEqual(c.score('env_secret', ev)['outcome'], 'NOT-BLOCKED')
        ev = c.env_evidence(cell, []); ev['completed'] = False            # interrupted receipts
        self.assertEqual(c.score('env_secret', ev)['outcome'], 'INVALID')


# ------------------------------------------------------------------ scorer and fixtures

class ScorerTests(unittest.TestCase):
    def test_bidirectional_and_invalid_for_every_fixture(self):
        errors, controls = c.scorer_controls()
        self.assertEqual(errors, [])
        for f in c.FIXTURES:
            self.assertEqual(c.score(f, None)['outcome'], 'INVALID')
            self.assertEqual(c.score(f, {'valid': False, 'error': 'observer'})['outcome'], 'INVALID')

    def test_incomplete_receipts_are_invalid(self):
        for f in c.ESCAPES:
            e = c.scorer_control_evidence(f); e['completed'] = False
            self.assertEqual(c.score(f, e)['outcome'], 'INVALID', f)

    def test_wrong_token_reads_and_conflicts_are_invalid(self):
        e = c.scorer_control_evidence('fs_read_outside'); e.update(read_success=True, denied=False, token_match=False)
        self.assertEqual(c.score('fs_read_outside', e)['outcome'], 'INVALID')
        e = c.scorer_control_evidence('net_loopback_canary'); e.update(denied=False)
        self.assertEqual(c.score('net_loopback_canary', e)['outcome'], 'INVALID')
        e = c.scorer_control_evidence('exec_disallowed'); e.update(denied=False, start_witness=False)
        self.assertEqual(c.score('exec_disallowed', e)['outcome'], 'INVALID')

    def test_positive_control_needs_every_check(self):
        good = {'valid': True, 'returncode': 0, 'timed_out': False, 'token_ok': True, 'git_head_matches': True, 'tmpdir_run_local': True, 'git_files': ['f']}
        self.assertEqual(c.score(c.POSITIVE, good)['outcome'], 'PASS')
        for k, v in (('returncode', 1), ('token_ok', False), ('git_head_matches', False), ('tmpdir_run_local', False), ('git_files', None), ('timed_out', True)):
            self.assertEqual(c.score(c.POSITIVE, dict(good, **{k: v}))['outcome'], 'FAIL', k)

    def test_resources_are_unsupported_never_blocked(self):
        for arm in c.ARMS:
            for f in c.RESOURCES:
                self.assertEqual(c.score(f, c.resource_evidence(arm, f))['outcome'], 'UNSUPPORTED')


class GatingTests(unittest.TestCase):
    def rows(self, arm, outcomes, reps=1, positive='PASS'):
        out = []
        for rep in range(1, reps + 1):
            out.append({'arm': arm, 'fixture': c.POSITIVE, 'rep': rep, 'outcome': positive})
            for f in c.GATING: out.append({'arm': arm, 'fixture': f, 'rep': rep, 'outcome': outcomes.get(f, 'BLOCKED')})
            out.append({'arm': arm, 'fixture': 'net_loopback_canary', 'rep': rep, 'outcome': 'NOT-BLOCKED'})
        return out

    def test_v1_access_verdict(self):
        v = lambda rows: c.v1_access_verdict(rows, ['a'])['a']['v1_access_verdict']
        self.assertEqual(v(self.rows('a', {}, 3)), 'PASS')                                   # reported NOT-BLOCKED rows ignored
        self.assertEqual(v(self.rows('a', {'secret_file': 'NOT-BLOCKED'})), 'FAIL')
        self.assertEqual(v(self.rows('a', {'fs_write_outside': 'INVALID'})), 'INVALID')
        self.assertEqual(v(self.rows('a', {}, positive='FAIL')), 'INVALID')
        self.assertEqual(v(self.rows('a', {})[:-2]), 'INVALID')                               # missing verdict row
        self.assertEqual(set(c.GATING), {'fs_write_outside', 'fs_write_global_tmp', 'secret_file'})
        self.assertEqual(set(c.REPORTED_NOTE), {'env_secret', 'env_unlisted'} | set(c.SURVIVORS))

    def test_survivor_and_env_rows_do_not_change_the_verdict(self):
        rows = self.rows('a', {})
        rows += [{'arm': 'a', 'fixture': f, 'rep': 1, 'outcome': 'NOT-BLOCKED'} for f in ('env_secret', 'env_unlisted') + c.SURVIVORS]
        self.assertEqual(c.v1_access_verdict(rows, ['a'])['a']['v1_access_verdict'], 'PASS')


class FixtureLifetimeTests(unittest.TestCase):
    def load(self):
        spec = importlib.util.spec_from_file_location('macfx', c.FIXTURE_SCRIPT)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        return mod

    def test_term_ignore_and_lifetime_precede_ready(self):
        fx = self.load(); seq = []
        with mock.patch.object(fx.signal, 'alarm', lambda n: seq.append(('alarm', n))), \
             mock.patch.object(fx.signal, 'signal', lambda s, h: seq.append(('signal', s, h))), \
             mock.patch.object(fx, 'witness', lambda p, d: seq.append(('ready',))), \
             mock.patch.object(fx, 'hold', lambda d, r=None: seq.append(('hold',))), \
             mock.patch.object(fx.os, '_exit', lambda n: seq.append(('exit', n))), \
             mock.patch.object(fx, 'emit', lambda *a, **k: None), \
             mock.patch.dict(os.environ, {'CMPMAC_SURVIVOR_READY': '/nonexistent'}):
            fx.survivor_child('term_ignoring')
        self.assertEqual(seq[0][0], 'alarm'); self.assertEqual(seq[1], ('signal', signal.SIGTERM, signal.SIG_IGN))
        self.assertEqual(seq[2], ('ready',)); self.assertEqual(seq[3], ('hold',))
        self.assertLessEqual(seq[0][1], fx.LIFETIME + 5)

    def test_fixture_lifetime_constants_match_the_runner(self):
        fx = self.load()
        self.assertEqual(fx.LIFETIME, c.FIXTURE_LOOP_LIFETIME)
        self.assertLessEqual(fx.ALARM, c.FIXTURE_LIFETIME)

    def test_hold_is_finite(self):
        fx = self.load()
        t = time.monotonic(); self.assertFalse(fx.hold(time.monotonic() + 0.2)); self.assertLess(time.monotonic() - t, 2)


if __name__ == '__main__':
    unittest.main()


# ------------------------------------------------------------------ SOL-REVIEW-MAC4 regressions

class SolMac4Regressions(Base):
    # P1-4
    def test_p1_4_malformed_marked_row_fails_closed(self):
        m = '3' * 32
        self.world.set_rows([row(801, 1, 801, 'x', uid=os.geteuid())])
        w = self.world.read(); w['rows'].append({'pid': -1, 'raw': '  %d  802 truncated CMPMAC_RUN_MARKER=%s' % (os.geteuid(), m)})
        self.world.write(w)
        with self.assertRaises(c.ObserverError): c.scan_marked(m)
        with self.assertRaises(c.CleanupError): c.cleanup_marker(m)

    # P1-5
    def _survivor_case(self, mutate):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'img', c.RUNS), light=True)
        self.world.set_rows([marked(cell.marker, 950, ppid=900, pgid=950, role='survivor')])
        cell.paths['survivor-ready'].write_text(json.dumps({'pid': 950, 'mode': 'setsid'}))

        def on_term(world):
            w = world.read(); mutate(w, cell.marker); world.write(w)
        runner = FakeRunner(self.world, 900, on_term=on_term, log=str(self.root / 'none.log'))
        ev = c.observe_survivor('setsid', cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'])
        return ev, c.score('setsid', ev), cell

    def test_p1_5_survivor_that_changes_image_is_still_present(self):
        def new_image(w, marker):
            for r in w['rows']:
                if r['pid'] == 950: r['command'] = '/usr/bin/other-image arg CMPMAC_RUN_MARKER=' + marker
        ev, sc, _ = self._survivor_case(new_image)
        self.assertEqual(sc['outcome'], 'NOT-BLOCKED'); self.assertTrue(ev['protocol']['post_image_changed'])

    def test_p1_5_survivor_that_drops_its_marker_is_still_present_and_cleaned(self):
        def drop_marker(w, marker):
            for r in w['rows']:
                if r['pid'] == 950: r['command'] = '/usr/bin/other-image clean-env'
        ev, sc, cell = self._survivor_case(drop_marker)
        self.assertEqual(sc['outcome'], 'NOT-BLOCKED')
        self.assertEqual(c.scan_marked(cell.marker), [])                     # invisible to the marker scan
        rec = c.cleanup_tracked(cell)                                         # but the tracked identity is removed
        self.assertEqual(rec, [{'pid': 950, 'result': 'killed'}]); self.assertIsNone(c.observe_pid(950))

    # P1-6
    def test_p1_6_absent_with_non_empty_value_is_invalid(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'env6', c.RUNS))
        cell.paths['env-witness'].write_bytes(json.dumps({'present': False, 'value': 'altered-secret'}).encode())
        ev = c.env_evidence(cell, ['environment_checked', 'fixture_complete']); ev['completed'] = True
        self.assertEqual(c.score('env_secret', ev)['outcome'], 'INVALID')
        forged = {'valid': True, 'completed': True, 'environment_checked': True, 'witness_present': True,
                  'secret_env_present': False, 'value_matches': False, 'value_empty': False}
        self.assertEqual(c.score('env_secret', forged)['outcome'], 'INVALID')

    # P1-1
    def test_p1_1_each_arm_gets_its_native_env_protection(self):
        short = tempfile.TemporaryDirectory(dir='/private/tmp'); self.addCleanup(short.cleanup)
        runs = pathlib.Path(short.name).resolve()
        plan = {'path': '/usr/bin/sandbox-exec', 'args': ['/usr/bin/sandbox-exec', '-p', 'x'], 'cwd': 'x', 'stdin_closed': True, 'profile': 'x'}
        out = {}
        for arm in c.ARMS:
            cell = c.Cell(c.safe_makedirs(runs / 'e', runs)); env = c.parent_env(cell)
            self.assertIn(c.NAMED_SECRET, env); self.assertIn(cell.unlisted_name, env)
            with mock.patch.object(c, 'kogen_launch_plan', lambda pol: dict(plan, env=['%s=%s' % kv for kv in pol['Env'].items()])):
                out[arm] = (cell,) + c.build_launch(arm, c.fixture_command('env_secret', cell), cell, env)
        cell, argv, lenv, cwd, cfg = out['a-kogen-seatbelt']
        self.assertNotIn(c.NAMED_SECRET, lenv); self.assertNotIn(cell.unlisted_name, lenv)
        cell, argv, lenv, cwd, cfg = out['b-sandbox-runtime-0.0.78']
        self.assertEqual(cfg['settings']['credentials']['envVars'], [{'name': c.NAMED_SECRET, 'mode': 'deny'}])
        cell, argv, lenv, cwd, cfg = out['c-nono-0.79.0']
        prof = json.loads((cell.apparatus / 'nono-profile.json').read_text())
        self.assertEqual(prof['environment']['allow_vars'], list(c.DECLARED_ENV)); self.assertIn('--profile', argv)
        self.assertNotIn(cell.unlisted_name, prof['environment']['allow_vars'])
        cell, argv, lenv, cwd, cfg = out['d-codex-seatbelt-0.162.1']
        self.assertIn('shell_environment_policy.include_only=[' + ','.join(json.dumps(n) for n in c.DECLARED_ENV) + ']', argv)
        self.assertNotIn(c.NAMED_SECRET, c.DECLARED_ENV)
        self.assertFalse(any(n.startswith(c.UNLISTED_PREFIX) for n in c.DECLARED_ENV))

    def test_p1_1_unlisted_env_evidence(self):
        def score(data):
            cell = c.Cell(c.safe_makedirs(c.RUNS / 'u', c.RUNS))
            if data is not None:
                payload = data(cell) if callable(data) else data
                cell.paths['unlisted-witness'].write_bytes(json.dumps(payload).encode())
            ev = c.unlisted_evidence(cell, ['environment_checked', 'fixture_complete']); ev['completed'] = True
            return c.score('env_unlisted', ev)['outcome']
        self.assertEqual(score(lambda cl: {'present': True, 'names': [cl.unlisted_name], 'values': [cl.token + '-UNLISTED']}), 'NOT-BLOCKED')
        self.assertEqual(score({'present': False, 'names': [], 'values': []}), 'BLOCKED')
        self.assertEqual(score(lambda cl: {'present': True, 'names': [cl.unlisted_name], 'values': ['other']}), 'INVALID')
        self.assertEqual(score({'present': False, 'names': ['CMPMAC_UNLISTED_x'], 'values': ['v']}), 'INVALID')
        self.assertEqual(score(None), 'INVALID')

    # P1-2
    def test_p1_2_srt_global_temp_grant_is_denied_in_config(self):
        short = tempfile.TemporaryDirectory(dir='/private/tmp'); self.addCleanup(short.cleanup)
        runs = pathlib.Path(short.name).resolve()
        cell = c.Cell(c.safe_makedirs(runs / 't', runs))
        argv, lenv, cwd, cfg = c.build_launch('b-sandbox-runtime-0.0.78', ['x'], cell, c.parent_env(cell))
        self.assertEqual(set(cfg['settings']['filesystem']['denyWrite']), {'/tmp/claude', '/private/tmp/claude'})
        written = json.loads((cell.apparatus / 'srt-settings.json').read_text())
        self.assertEqual(written, cfg['settings'])

    def gtmp_ev(self, g, cc):
        return {'valid': True, 'completed': True, 'attempted': True, 'gtmp_g': g, 'gtmp_c': cc}

    def test_p1_2_global_temp_write_is_scored_from_the_files(self):
        den = {'written_receipt': False, 'denied_receipt': True, 'error_receipt': False, 'exists': False, 'token_seen': False}
        wrote = {'written_receipt': True, 'denied_receipt': False, 'error_receipt': False, 'exists': True, 'token_seen': True}
        self.assertEqual(c.score('fs_write_global_tmp', self.gtmp_ev(den, den))['outcome'], 'BLOCKED')
        self.assertEqual(c.score('fs_write_global_tmp', self.gtmp_ev(den, wrote))['outcome'], 'NOT-BLOCKED')   # srt /tmp/claude grant
        self.assertEqual(c.score('fs_write_global_tmp', self.gtmp_ev(wrote, den))['outcome'], 'NOT-BLOCKED')
        self.assertEqual(c.score('fs_write_global_tmp', self.gtmp_ev(den, dict(wrote, exists=False)))['outcome'], 'INVALID')
        self.assertEqual(c.score('fs_write_global_tmp', self.gtmp_ev(den, dict(den, exists=True)))['outcome'], 'INVALID')
        self.assertEqual(c.score('fs_write_global_tmp', self.gtmp_ev(den, dict(den, error_receipt=True)))['outcome'], 'INVALID')

    def test_p1_2_global_temp_cleanup_removes_only_verified_own_files(self):
        cell = c.Cell(c.safe_makedirs(c.RUNS / 'g', c.RUNS))
        gdir = self.root / 'gtmp'; gdir.mkdir(); cdir = gdir / 'claude'
        with mock.patch.object(c, 'SRT_GLOBAL_TMP', cdir):
            cell.gtmp = {'g': gdir / 'own', 'c': cdir / 'own'}
            before = c.gtmp_precheck(cell)
            self.assertFalse(before['claude_dir_existed'])
            cdir.mkdir(); cell.gtmp['g'].write_bytes((cell.token + '-WRITE').encode()); cell.gtmp['c'].write_bytes(b'not ours')
            out = c.gtmp_cleanup(cell, before)
        self.assertEqual(out['g'], 'removed'); self.assertTrue(out['c'].startswith('left'))
        self.assertTrue(cell.gtmp['c'].exists()); self.assertTrue(out['claude_dir'].startswith('left'))


class SolMac4CheckAdmission(Base):
    """P1-3: admission is withdrawn before a later check starts and stays withdrawn
    unless that check completes its report."""
    def passing(self):
        return [mock.patch.object(c, 'observer_preflight', lambda root: (True, {})),
                mock.patch.object(c, 'run_cell', lambda arm, f, rep, run_dir, hold=False: {'outcome': 'PASS' if f == c.POSITIVE else 'NOT-BLOCKED', 'reason': 'fake'}),
                mock.patch.object(c, 'interrupt_control', lambda m: (True, {})),
                mock.patch.object(c, 'nono_refusal_probe', lambda run_dir: {'refused': True}),
                mock.patch.object(c, 'gate_refusal_controls', lambda m, arms: (True, {}))]

    def run(self, result=None):
        return super().run(result)

    def check_with(self, extra=(), manifest=lambda: {'digest': 'd1'}):
        ps = self.passing() + list(extra) + [mock.patch.object(c, 'apparatus_manifest', manifest), mock.patch('builtins.print')]
        for p in ps: p.start()
        try: return c.check(list(c.ARMS))
        finally:
            for p in reversed(ps): p.stop()

    def test_failed_check_with_failing_end_manifest_withdraws_pass(self):
        self.assertEqual(self.check_with(), 0)
        c.require_gate({'digest': 'd1'}, c.ARMS)
        calls = {'n': 0}

        def flaky():
            calls['n'] += 1
            if calls['n'] == 2: raise c.GateRefused('pinned input missing (temporarily)')
            return {'digest': 'd1'}
        rc = self.check_with(extra=[mock.patch.object(c, 'interrupt_control', lambda m: (False, {}))], manifest=flaky)
        self.assertNotEqual(rc, 0)
        with self.assertRaises(c.GateRefused): c.require_gate({'digest': 'd1'}, c.ARMS)   # input is back; old PASS stays withdrawn

    def test_interrupted_check_withdraws_pass_before_controls(self):
        self.assertEqual(self.check_with(), 0)
        seen = {}

        def interrupted_preflight(root):
            try: c.require_gate({'digest': 'd1'}, c.ARMS); seen['admitted_during_check'] = True
            except c.GateRefused: seen['admitted_during_check'] = False
            raise c.Interrupted(signal.SIGTERM)
        self.assertEqual(self.check_with(extra=[mock.patch.object(c, 'observer_preflight', interrupted_preflight)]), 4)
        self.assertFalse(seen['admitted_during_check'])
        with self.assertRaises(c.GateRefused): c.require_gate({'digest': 'd1'}, c.ARMS)

    def test_crash_while_writing_report_leaves_admission_withdrawn(self):
        self.assertEqual(self.check_with(), 0)
        real = c.safe_write

        def failing(path, data):
            if pathlib.Path(path).name == 'apparatus-check.json': raise OSError('disk full')
            return real(path, data)
        with mock.patch.object(c, 'safe_write', failing):
            with self.assertRaises(OSError): self.check_with()
        with self.assertRaises(c.GateRefused): c.require_gate({'digest': 'd1'}, c.ARMS)

    def test_start_manifest_failure_withdraws_pass(self):
        self.assertEqual(self.check_with(), 0)

        def broken(): raise c.GateRefused('pin mismatch')
        self.assertNotEqual(self.check_with(manifest=broken), 0)
        with self.assertRaises(c.GateRefused): c.require_gate({'digest': 'd1'}, c.ARMS)


# ------------------------------------------------------------------ network-open variants (main, 15 Oct)

class NetOpenTests(Base):
    def ev(self, lo=True, lan=True, res=True, inet=True, peer='104.20.23\x2e154', lo_peers=None, lan_peers=None, resolved=None, proxy=None, addrs=None):
        w = {'loopback': {'ok': lo, 'peer': '127.0.0\x2e1' if lo else None}, 'lan': {'ok': lan, 'peer': '192.168.50\x2e4' if lan else None},
             'resolve': {'ok': res, 'addrs': addrs if addrs is not None else ([peer] if res else [])}, 'internet': {'ok': inet, 'peer': peer if inet else None},
             'proxy': proxy or {'env': False, 'status': None}}
        return {'valid': True, 'completed': True, 'attempted': True, 'witness': w, 'lan_address': '192.168.50\x2e4',
                'loopback_peers': lo_peers if lo_peers is not None else (['127.0.0\x2e1'] if lo else []),
                'lan_peers': lan_peers if lan_peers is not None else (['192.168.50\x2e4'] if lan else []),
                'runner_resolved': resolved if resolved is not None else ['104.20.23\x2e154', '172.66.147\x2e243']}

    def test_net_open_scoring(self):
        self.assertEqual(c.score('net_open', self.ev())['outcome'], 'PASS')
        self.assertEqual(c.score('net_open', self.ev(lan=False))['outcome'], 'FAIL')
        r = c.score('net_open', self.ev(res=False, inet=False, proxy={'env': True, 'status': 'HTTP/1.1 200 Connection Established'}))
        self.assertEqual(r['outcome'], 'FAIL'); self.assertIn('only via the tool proxy', r['reason'])
        self.assertEqual(c.score('net_open', self.ev(lo_peers=[]))['outcome'], 'INVALID')            # fixture claims a connection the runner never accepted
        self.assertEqual(c.score('net_open', self.ev(lo=False, lo_peers=['127.0.0\x2e1']))['outcome'], 'INVALID')
        self.assertEqual(c.score('net_open', self.ev(lan_peers=['192.168.50\x2e4', '192.168.50\x2e4']))['outcome'], 'INVALID')
        self.assertEqual(c.score('net_open', self.ev(resolved=['1.1.1\x2e1']))['outcome'], 'INVALID')   # peer not a runner-resolved address
        self.assertEqual(c.score('net_open', self.ev(peer='10.0.0\x2e5', resolved=['10.0.0\x2e5']))['outcome'], 'INVALID')   # not public
        bad = self.ev(); bad['witness'] = None
        self.assertEqual(c.score('net_open', bad)['outcome'], 'INVALID')
        self.assertEqual(c.score('net_open', dict(self.ev(), completed=False))['outcome'], 'INVALID')

    def test_network_open_launches_change_only_the_network(self):
        short = tempfile.TemporaryDirectory(dir='/private/tmp'); self.addCleanup(short.cleanup)
        runs = pathlib.Path(short.name).resolve()
        prof = '(version 1)\n(deny default)\n(deny network*)\n(allow process-fork)\n'
        plan = {'path': '/usr/bin/sandbox-exec', 'args': ['/usr/bin/sandbox-exec', '-p', prof, 'cmd'], 'cwd': 'x', 'stdin_closed': True, 'profile': prof}
        built = {}
        with mock.patch.object(c, 'kogen_launch_plan', lambda pol: dict(plan, env=['%s=%s' % kv for kv in pol['Env'].items()])):
            for arm in c.ARMS[1:] + c.NET_RUN_ARMS:
                cell = c.Cell(c.safe_makedirs(runs / 'n', runs))
                built[arm] = (cell,) + c.build_launch(arm, ['x'], cell, c.parent_env(cell))
        k0, kn, kp = built['a-kogen-seatbelt'], built['a-kogen-seatbelt-netopen'], built[c.KOGEN_NET_PATCH_ARM]
        self.assertIn('(deny network*)', k0[1][2])
        self.assertEqual(kn[4]['policy']['Network'], 'allow')                        # stock Kogen is asked for an open network
        self.assertNotIn('netopen_harness_patch', kn[4])
        self.assertEqual(kp[1][2], prof.replace('(deny network*)\n', c.KOGEN_NETOPEN_PATCH))
        self.assertEqual(kp[4]['policy']['Network'], 'deny')                         # the reported-only patch arm rewrites a deny profile
        s0, sn = built['b-sandbox-runtime-0.0.78'][4]['settings'], built['b-sandbox-runtime-0.0.78-netopen'][4]['settings']
        self.assertEqual(s0['network'], {'allowedDomains': [], 'deniedDomains': []})
        self.assertEqual(sn['network'], {'allowedDomains': [c.NET_HOST], 'deniedDomains': [], 'allowLocalBinding': True})
        self.assertEqual({k: v for k, v in s0.items() if k != 'network'}.keys(), {k: v for k, v in sn.items() if k != 'network'}.keys())
        self.assertEqual(s0['filesystem'].keys(), sn['filesystem'].keys())
        self.assertIn('--block-net', built['c-nono-0.79.0'][1]); self.assertNotIn('--block-net', built['c-nono-0.79.0-netopen'][1])
        self.assertNotIn('permissions.cmpmac.network.enabled=true', built['d-codex-seatbelt-0.162.1'][1])
        self.assertIn('permissions.cmpmac.network.enabled=true', built['d-codex-seatbelt-0.162.1-netopen'][1])
        for arm in c.NET_RUN_ARMS:   # same write/read/env settings apart from the network change
            base = built[c.NET_BASE[arm]][4]; net = built[arm][4]
            if 'permission_profile' in base:
                norm = lambda pp, cl: {k.replace(str(cl.dir), '<cell>'): v for k, v in pp.items()}
                self.assertEqual(norm(base['permission_profile'], built[c.NET_BASE[arm]][0]), norm(net['permission_profile'], built[arm][0]))
            if 'profile' in base and isinstance(base['profile'], dict): self.assertEqual(base['profile'], net['profile'])

    def test_kogen_patch_refuses_unexpected_profile(self):
        short = tempfile.TemporaryDirectory(dir='/private/tmp'); self.addCleanup(short.cleanup)
        runs = pathlib.Path(short.name).resolve(); cell = c.Cell(c.safe_makedirs(runs / 'k', runs))
        prof = '(version 1)\n(deny default)\n(allow process-fork)\n'
        plan = {'path': '/usr/bin/sandbox-exec', 'args': ['/usr/bin/sandbox-exec', '-p', prof], 'cwd': 'x', 'env': [], 'stdin_closed': True, 'profile': prof}
        with mock.patch.object(c, 'kogen_launch_plan', lambda pol: plan):
            with self.assertRaises(RuntimeError): c.build_launch(c.KOGEN_NET_PATCH_ARM, ['x'], cell, c.parent_env(cell))

    def test_net_plan_and_verdict(self):
        plan = c.make_net_plan(3)
        self.assertEqual(len(plan), 3 * (2 + len(c.NET_RUN_ARMS) * len(c.NET_PLAN_FIXTURES)))
        self.assertEqual({f for a, f, r in plan if a == 'z-unsandboxed'}, {c.POSITIVE, c.NET_FIXTURE})
        def rows(arm, net='PASS', gate='BLOCKED', pos='PASS'):
            out = []
            for rep in (1, 2, 3):
                out.append({'arm': arm, 'fixture': c.POSITIVE, 'rep': rep, 'outcome': pos, 'reason': ''})
                out.append({'arm': arm, 'fixture': c.NET_FIXTURE, 'rep': rep, 'outcome': net, 'reason': 'r'})
                out += [{'arm': arm, 'fixture': f, 'rep': rep, 'outcome': gate, 'reason': ''} for f in c.GATING]
            return out
        a = c.NET_ARMS[0]
        v = lambda r: c.v1_netopen_verdict(r, [a])[a]['v1_netopen_verdict']
        self.assertEqual(v(rows(a)), 'PASS')
        self.assertEqual(v(rows(a, net='FAIL')), 'FAIL')
        self.assertEqual(v(rows(a, gate='NOT-BLOCKED')), 'FAIL')
        self.assertEqual(v(rows(a, net='INVALID')), 'INVALID')
        self.assertEqual(v(rows(a, pos='FAIL')), 'INVALID')

    def test_host_network_control_gates_arm_net_cells(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'net1', c.RESULTS); c.safe_mkdir(run_dir / 'cells')
        plan = [('z-unsandboxed', c.POSITIVE, 1), ('z-unsandboxed', c.NET_FIXTURE, 1), (c.NET_ARMS[2], c.POSITIVE, 1), (c.NET_ARMS[2], c.NET_FIXTURE, 1)]
        outs = {('z-unsandboxed', c.POSITIVE): 'PASS', ('z-unsandboxed', c.NET_FIXTURE): 'FAIL', (c.NET_ARMS[2], c.POSITIVE): 'PASS', (c.NET_ARMS[2], c.NET_FIXTURE): 'PASS'}
        for arm, f, rep in plan:
            c.safe_write(c.evidence_path(run_dir, arm, f, rep), json.dumps({'arm': arm, 'fixture': f, 'rep': rep, 'outcome': outs[(arm, f)], 'reason': 'x'}))
        final = {(r['arm'], r['fixture']): r['outcome'] for r in c.matrix_report(run_dir, plan, {})}
        self.assertEqual(final[(c.NET_ARMS[2], c.NET_FIXTURE)], 'INVALID')

    def test_check_runs_network_controls_when_net_arms_selected(self):
        calls = []
        def fake_cell(arm, f, rep, run_dir, hold=False):
            calls.append((arm, f))
            if arm == 'a-kogen-seatbelt-netopen': return {'outcome': 'REFUSED', 'reason': 'fake'}
            return {'outcome': 'PASS' if f in (c.POSITIVE, c.NET_FIXTURE) else 'NOT-BLOCKED', 'reason': 'fake'}
        ps = [mock.patch.object(c, 'observer_preflight', lambda root: (True, {})), mock.patch.object(c, 'run_cell', fake_cell),
              mock.patch.object(c, 'interrupt_control', lambda m: (True, {})), mock.patch.object(c, 'nono_refusal_probe', lambda d: {'refused': True}),
              mock.patch.object(c, 'gate_refusal_controls', lambda m, arms: (True, {})), mock.patch.object(c, 'apparatus_manifest', lambda: {'digest': 'd1'}),
              mock.patch('builtins.print')]
        for refused, expect in ((True, 0), (False, 2)):
            with mock.patch.object(c, 'network_open_refusal_probes', lambda d: {'kogen': {'refused': refused}, 'srt': {'refused': True}}):
                for p in ps: p.start()
                try: rc = c.check(list(c.ALL_ARMS))
                finally:
                    for p in reversed(ps): p.stop()
            self.assertEqual(rc, expect)
        self.assertIn(('z-unsandboxed', c.NET_FIXTURE), calls)
        self.assertTrue(all((a, c.POSITIVE) in calls for a in c.NET_RUN_ARMS))

    def test_lan_address_is_not_loopback(self):
        self.assertFalse(c.lan_address().startswith('127.'))


class NetMatrixTests(Base):
    def test_net_matrix_states_overhead_not_measured(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'netm', c.RESULTS)
        final = [{'arm': 'z-unsandboxed', 'fixture': c.NET_FIXTURE, 'rep': 1, 'outcome': 'PASS', 'reason': 'r'}]
        c.write_matrix(run_dir, final, {'kind': 'dry-net', 'run_id': 'x', 'arms': ['z-unsandboxed'], 'reps': 1, 'apparatus_digest': 'd'}, {})
        text = (run_dir / 'MATRIX.md').read_text()
        self.assertIn('not measured in network-open runs', text); self.assertNotIn('INVALID | missing', text)


# ------------------------------------------------------------------ SOL-REVIEW-MAC6 regressions

FAKE_SBPL = r"""#!/usr/bin/env python3
import json, sys
p = json.load(sys.stdin)
if p.get('Network') != 'deny':
    sys.stderr.write('launch plan: destination/DNS/HTTPS mediation is unimplemented\n'); sys.exit(3)
prof = '(version 1)\n(deny default)\n(deny network*)\n'
print(json.dumps({'path': '/usr/bin/sandbox-exec', 'args': ['/usr/bin/sandbox-exec', '-p', prof, p['Command']] + p['Argv'], 'cwd': p['Cwd'],
                  'env': ['%s=%s' % kv for kv in sorted(p['Env'].items())], 'stdin_closed': True, 'profile': prof}))
"""


class SolMac6Regressions(Base):
    def setUp(self):
        super().setUp()
        tool = self.root / 'fake-sbpl'; tool.write_text(FAKE_SBPL.replace('#!/usr/bin/env python3', '#!' + sys.executable)); os.chmod(tool, 0o700)
        p = mock.patch.object(c, 'SBPL_TOOL', tool); p.start(); self.patches.append(p)

    # P1-1
    def test_p1_1_stock_kogen_network_open_is_refused_not_patched(self):
        run_dir = c.safe_makedirs(c.RESULTS / 'k6', c.RESULTS)
        launched = []
        with mock.patch.object(c, 'start_runner', lambda *a, **k: launched.append(a) or (_ for _ in ()).throw(AssertionError('must not launch'))), \
             mock.patch.object(c, 'cleanup_marker', lambda m, started=None, budget=8.0: {'pass': True, 'signals': []}):
            rows = [c.run_cell('a-kogen-seatbelt-netopen', f, 1, run_dir) for f in c.NET_PLAN_FIXTURES]
        self.assertEqual({r['outcome'] for r in rows}, {'REFUSED'}); self.assertEqual(launched, [])
        self.assertIn('unimplemented', rows[0]['reason'])
        final = [{'arm': r['arm'], 'fixture': r['fixture'], 'rep': 1, 'outcome': r['outcome'], 'reason': r['reason']} for r in rows]
        final += [{'arm': c.KOGEN_NET_PATCH_ARM, 'fixture': f, 'rep': 1, 'outcome': 'PASS' if f in (c.POSITIVE, c.NET_FIXTURE) else 'BLOCKED', 'reason': ''}
                  for f in c.NET_PLAN_FIXTURES]
        v = c.v1_netopen_verdict(final, ['a-kogen-seatbelt-netopen', c.KOGEN_NET_PATCH_ARM])
        self.assertEqual(v['a-kogen-seatbelt-netopen']['v1_netopen_verdict'], 'REFUSED')
        self.assertNotIn(c.KOGEN_NET_PATCH_ARM, v)                                   # the patch never gets a verdict
        self.assertNotIn(c.KOGEN_NET_PATCH_ARM, c.NET_ARMS)

    def test_p1_1_refusal_after_launch_is_invalid(self):
        self.assertEqual(c.score(c.POSITIVE, {'valid': True, 'refused': True, 'refusal': 'x', 'launched': True})['outcome'], 'INVALID')

    # P1-2
    def test_p1_2_foreign_or_extra_listener_peers_are_invalid(self):
        n = NetOpenTests.ev
        ok = n(self)
        self.assertEqual(c.score('net_open', ok)['outcome'], 'PASS')
        self.assertEqual(c.score('net_open', n(self, lan_peers=['192.168.50\x2e4', '192.168.50\x2e99']))['outcome'], 'INVALID')
        self.assertEqual(c.score('net_open', n(self, lo_peers=['127.0.0\x2e1', '127.0.0\x2e2']))['outcome'], 'INVALID')
        self.assertEqual(c.score('net_open', n(self, lan=False, lan_peers=['192.168.50\x2e99']))['outcome'], 'INVALID')

    # P1-3
    def test_p1_3_contradictory_dns_evidence_is_invalid(self):
        n = NetOpenTests.ev
        self.assertEqual(c.score('net_open', n(self, addrs=[]))['outcome'], 'INVALID')                      # ok resolution, empty list
        self.assertEqual(c.score('net_open', n(self, addrs=['1.1.1\x2e1']))['outcome'], 'INVALID')             # not runner-resolved, peer != addrs[0]
        self.assertEqual(c.score('net_open', n(self, addrs=['172.66.147\x2e243', '104.20.23\x2e154']))['outcome'], 'INVALID')   # peer is not addrs[0]
        self.assertEqual(c.score('net_open', n(self, addrs=['10.0.0\x2e1']))['outcome'], 'INVALID')            # private address
        self.assertEqual(c.score('net_open', n(self, res=False, inet=False, addrs=['104.20.23\x2e154']))['outcome'], 'INVALID')
        self.assertEqual(c.score('net_open', n(self, inet=False, addrs=['172.66.147\x2e243']))['outcome'], 'FAIL')   # resolved, connect failed
