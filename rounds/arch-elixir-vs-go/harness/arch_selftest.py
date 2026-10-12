#!/usr/bin/env python3
"""Offline self-checks with synthetic receipts/process tables; no model sessions."""
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import copy
import json
import os
import shutil
import signal
import subprocess
import stat
import sys
import tempfile
import time
import unittest
import uuid

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
from arch_config import (ARMS, STUDIO_ARMS, MACBOOK_ARMS, STUDIO_WAVES, PAIRS, CONSTRAINTS,
                         MODEL, EFFORT, PHASE_SECONDS, CORES, render, dump, digest, pair_for_arm)
from arch_fs import safe_chmod, safe_rmtree
from arch_budget import ArmBudget, Process
from arch_cpu import Supervisor
from arch_tokens import collect_phase
from arch_loc import count, code_lines
from arch_repairs import count as repairs, affirmative
from arch_snapshot import capture, tree_hash, writable_copy
from arch_score import normalize, score
from arch_report import decide, report, markdown
from arch_audit import audit_events, actual_model_receipts, outside_reads
from arch_install import environment, install, mise_config
from arch_gates import freeze, verify, contract_hash, check_freeze
from arch_run import Arm, InfraLaunchError, argv, flag_infrastructure
from arch_finalize import finalize
from arch_tooltimer import collect as times
from arch_evidence import build as build_evidence
from arch_run import production_schedule
from arch_run import score_arms, capture_arm, score_reference_snapshots
from arch_cpu import kill_arm_orphans

def now():
    return datetime.now(timezone.utc).isoformat()

def events(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))

def token(at, value):
    return dict(type='event_msg', timestamp=at, payload=dict(type='token_count', info=dict(total_token_usage=dict(
        input_tokens=value, cached_input_tokens=1, output_tokens=value, reasoning_output_tokens=1, total_tokens=2 * value))))

def raw_score(groups=('B', 'F'), reps=2):
    rows = [dict(id=g + '01', group=g, passed=True, k_ids=['K-07'], clauses=[dict(number=1, text='fixture')],
                 repetitions=[dict(repetition=i + 1, passed=True) for i in range(reps)]) for g in groups]
    counters = dict(overall=dict(passed=2, total=2), repetitions=[
        dict(repetition=i + 1, passed=1, total=1) for i in range(reps)])
    priority = dict(overall=dict(passed=0, total=0), repetitions=[
        dict(repetition=i + 1, passed=0, total=0) for i in range(reps)])
    hashes = {'SPEC.md': 'fixture-spec', 'PROTOCOL.md': 'fixture-protocol'}
    return dict(schema_version=2, reps=reps, spec_sha256=hashes, suite_sha256='fixture-suite',
                spec_sha256_end=hashes, cases=rows,
                groups={g: dict(passed=1, total=1) for g in groups},
                k_ids=counters, priority_k_ids=priority, spec_changed_during_run=False)

class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.selfcheck-', dir=HERE)
        self.root = Path(self.temp.name)
    def tearDown(self):
        # Captures are read-only, so restore only test-owned files for cleanup.
        try:
            for base, dirs, files in os.walk(self.root, followlinks=False):
                if Path(base).is_symlink():
                    continue
                safe_chmod(self.root, Path(base), 0o755)
                for name in files:
                    path = Path(base) / name
                    if not path.is_symlink():
                        safe_chmod(self.root, path, path.stat().st_mode | 0o600)
        finally:
            self.temp.cleanup()

def clean_selfcheck_roots():
    for candidate in HERE.glob('.selfcheck-*'):
        if candidate.is_symlink() or not candidate.is_dir():
            continue
        for base, dirs, files in os.walk(candidate, followlinks=False):
            base_path = Path(base)
            if base_path.is_symlink():
                continue
            safe_chmod(candidate, base_path, 0o755)
            for name in files:
                path = base_path / name
                if not path.is_symlink():
                    safe_chmod(candidate, path, path.stat().st_mode | 0o600)
        safe_rmtree(HERE, candidate)

class Collectors(Base):
    def rollout(self, identity='t1'):
        cwd = self.root / 'workspace'; cwd.mkdir(exist_ok=True)
        turns = self.root / 'turn-1.jsonl'
        events(turns, [dict(type='thread.started', thread_id=identity)])
        sessions = self.root / 'sessions'; sessions.mkdir(exist_ok=True)
        rollout = sessions / ('rollout-' + identity + '.jsonl')
        events(rollout, [dict(type='session_meta', payload=dict(id=identity, cwd=str(cwd))),
                         token('2026-10-11T01:00:00Z', 10), token('2026-10-11T01:00:01Z', 20),
                         token('2026-10-11T01:00:02Z', 30)])
        return cwd, turns, sessions, rollout

    def test_cumulative_cutoff_inclusive_not_turn_sum(self):
        cwd, turns, sessions, _ = self.rollout()
        events(self.root / 'turn-2.jsonl', [dict(type='thread.started', thread_id='t1'),
                                          dict(type='turn.completed', usage={'total_tokens': 999})])
        result = collect_phase([turns, self.root / 'turn-2.jsonl'], sessions, cwd, '2026-10-11T01:00:01+00:00')
        self.assertEqual(result['usage']['total_tokens'], 40)
        self.assertEqual(result['n_threads'], 1)
        self.assertEqual(result['threads'][0]['later_token_events'], 1)

    def test_usage_missing_never_becomes_zero(self):
        cwd, turns, sessions, _ = self.rollout()
        with self.assertRaises(ValueError):
            collect_phase([turns], sessions, cwd, '2026-10-10T00:00:00Z')

    def test_rollout_metadata_and_order_must_agree(self):
        cwd, turns, sessions, path = self.rollout()
        events(path, [dict(type='session_meta', payload=dict(id='wrong', cwd=str(cwd))), token(now(), 10)])
        with self.assertRaises(ValueError):
            collect_phase([turns], sessions, cwd, now())
        events(path, [dict(type='session_meta', payload=dict(id='t1', cwd=str(cwd))),
                      token('2026-10-11T01:00:01Z', 10), token('2026-10-11T01:00:00Z', 20)])
        with self.assertRaises(ValueError):
            collect_phase([turns], sessions, cwd, now())

    def test_multiple_sessions_add_cumulative_counts(self):
        cwd, turns, sessions, _ = self.rollout()
        events(sessions / 'rollout-t2.jsonl', [dict(type='session_meta', payload=dict(id='t2', cwd=str(cwd))),
                                               token('2026-10-11T01:00:00Z', 10)])
        events(self.root / 'turn-2.jsonl', [dict(type='thread.started', thread_id='t2')])
        result = collect_phase([turns, self.root / 'turn-2.jsonl'], sessions, cwd, '2026-10-11T01:00:01Z')
        self.assertEqual(result['usage']['total_tokens'], 60)

    def test_actual_model_receipts_are_not_requested_flags(self):
        cwd, turns, sessions, path = self.rollout()
        at = now()
        events(path, [dict(type='session_meta', payload=dict(id='t1', cwd=str(cwd))),
                      dict(type='turn_context', timestamp=at, payload=dict(cwd=str(cwd), model=MODEL, effort='low'))])
        with self.assertRaises(ValueError):
            actual_model_receipts(sessions, {'t1'}, cwd, now())

    def test_loc_ignores_comments_deps_and_generated(self):
        (self.root / 'main.go').write_text('package main\n// comment\n/* block\n comment */\nvar s = "// string" // tail\nvar r = `# raw`\n\n')
        (self.root / 'a.ex').write_text('@moduledoc """\nDocs\n"""\ndefmodule X do # tail\n s = "# string"\nend\n')
        for folder in ('deps', '_build', 'vendor', 'generated'):
            (self.root / folder).mkdir(); (self.root / folder / 'x.go').write_text('package ignored\n')
        (self.root / 'gen.go').write_text('// Code generated by fake. DO NOT EDIT.\npackage generated\n')
        result = count(self.root)
        self.assertEqual(result['by_language'], {'Go': 3, 'Elixir': 3})
        self.assertEqual(result['excluded_generated'], ['gen.go'])

    def test_repairs_count_only_later_started_turns(self):
        for n, text in enumerate(['Not all tests pass yet.', 'ALL TESTS PASS', 'Fix one more edge.', 'ALL TESTS PASS'], 1):
            events(self.root / ('turn-' + str(n) + '.jsonl'), [dict(type='thread.started', thread_id='t1'),
                    dict(item=dict(type='agent_message', text=text))])
        result = repairs(sorted(self.root.glob('turn-*.jsonl')))
        self.assertEqual(result['repair_turns'], 2)
        self.assertFalse(affirmative('When all tests pass, stop.'))

    def test_tool_timing_includes_interrupted_tail(self):
        path = self.root / 'timings.jsonl'
        events(path, [dict(id='a', phase='build', event='start', category='build', at=1),
                      dict(id='a', phase='build', event='end', category='build', at=3),
                      dict(id='b', phase='build', event='start', category='test', at=5),
                      dict(id='c', phase='maintenance', event='start', category='test', at=5)])
        result = times(path, 'build', 10)
        self.assertEqual(result['total_seconds'], 7)
        self.assertEqual(result['incomplete_at_kill'], 1)

class ScoringAndBudgets(Base):
    def test_two_concurrent_trampoline_launches_reach_fake_codex(self):
        from concurrent.futures import ThreadPoolExecutor
        script = self.root / 'fake-codex'
        script.write_text('#!' + sys.executable + '\nimport json,sys\nsys.stdin.read()\n'
                          'print(json.dumps({"type":"thread.started","thread_id":"fake"}),flush=True)\n'
                          'print(json.dumps({"type":"turn.completed"}),flush=True)\n')
        safe_chmod(self.root, script, 0o755)
        t0 = time.monotonic() + .5
        supervisors, requests = [], []
        for arm in ('arch-e1', 'arch-g1'):
            private = self.root / arm
            private.mkdir()
            holder = {}
            stopped = set()
            def observer(holder=holder, t0=t0):
                supervisor = holder.get('supervisor')
                if supervisor is None:
                    return {}
                rows = {}
                for proc in supervisor.children.values():
                    if proc.poll() is not None:
                        continue
                    try:
                        waited, status = os.waitpid(proc.pid, os.WNOHANG | os.WUNTRACED)
                        if waited == proc.pid and os.WIFSTOPPED(status):
                            stopped.add(proc.pid)
                    except ChildProcessError:
                        pass
                    if proc.pid in stopped:
                        state = 'T' if time.monotonic() < t0 else 'R'
                        rows[proc.pid] = Process(proc.pid, os.getpid(), proc.pid, .01, state,
                                                 'fixture-' + str(proc.pid))
                return rows
            cpu = Supervisor(SimpleNamespace(arm=arm, root=str(self.root), private=str(private),
                                             cores=3., t0=t0, deadline=t0 + 5), observer=observer)
            holder['supervisor'] = cpu
            supervisors.append(cpu)
            requests.append(dict(operation='launch', arm=arm, role='builder', argv=[str(script), 'exec'],
                                 cwd=str(self.root), env=dict(os.environ), stdin='fake prompt'))

        try:
            with ThreadPoolExecutor(max_workers=2) as pool:
                replies = list(pool.map(lambda pair: pair[0].request(pair[1]), zip(supervisors, requests)))
            limit = time.monotonic() + 4
            codes = [None, None]
            while time.monotonic() < limit:
                for supervisor in supervisors:
                    supervisor.tick()
                codes = [supervisor.children[reply['handle']].poll()
                         for supervisor, reply in zip(supervisors, replies)]
                if all(code is not None for code in codes):
                    break
                time.sleep(.02)
            self.assertEqual(codes, [0, 0])
            for reply in replies:
                output = (Path(reply['output']) / 'stdout').read_text()
                self.assertIn('"type": "thread.started"', output)
                self.assertIn('"type": "turn.completed"', output)
        finally:
            for supervisor in supervisors:
                supervisor.stop()

    def test_every_repetition_required(self):
        result = raw_score(); result['cases'][1]['repetitions'][1]['passed'] = False
        result['cases'][1]['passed'] = False; result['groups']['F']['passed'] = 0
        scored = normalize(result, ['B', 'F'], {'B01': 'B', 'F01': 'F', 'M01': 'M'})
        self.assertEqual(scored['groups']['F']['passed'], 0)

    def test_v1_rejected_v2_accepted_and_missing_case_rejected(self):
        report = raw_score()
        self.assertEqual(normalize(report, ['B', 'F'], {'B01': 'B', 'F01': 'F'})['groups']['B']['total'], 1)
        no_clauses = copy.deepcopy(report)
        for case in no_clauses['cases']:
            case.pop('clauses', None)
        self.assertEqual(normalize(no_clauses, ['B', 'F'], {'B01': 'B', 'F01': 'F'})['groups']['F']['total'], 1)
        bad_tags = copy.deepcopy(report); bad_tags['cases'][0]['k_ids'] = 'K-07'
        with self.assertRaisesRegex(ValueError, 'k_ids must be a list of strings'):
            normalize(bad_tags, ['B', 'F'], {'B01': 'B', 'F01': 'F'})
        old = copy.deepcopy(report); old['schema_version'] = 1
        with self.assertRaisesRegex(ValueError, 'schema_version 2'):
            normalize(old, ['B', 'F'], {'B01': 'B', 'F01': 'F'})
        missing = copy.deepcopy(report); missing['cases'].pop()
        with self.assertRaisesRegex(ValueError, 'inventory'):
            normalize(missing, ['B', 'F'], {'B01': 'B', 'F01': 'F'})

    def test_partial_duplicate_or_inconsistent_scores_rejected(self):
        original = raw_score()
        for changed in ('partial', 'duplicate', 'inconsistent'):
            result = copy.deepcopy(original)
            if changed == 'partial': result['cases'].pop()
            if changed == 'duplicate': result['cases'].append(copy.deepcopy(result['cases'][0]))
            if changed == 'inconsistent': result['groups']['F']['passed'] = 0
            with self.assertRaises(ValueError):
                normalize(result, ['B', 'F'], {'B01': 'B', 'F01': 'F'})

    def test_cpu_caps_and_detached_identity_retained(self):
        self.assertEqual(CORES, {'macbook': 3., 'studio': 2.5})
        budget = ArmBudget('arch-e1', 2.5, 0)
        root = Process(100, 1, 100, 0, 'T', 'start1')
        budget.register(root, 'builder', 'arch-e1')
        budget.sample({100: root, 101: Process(101, 100, 101, 1, 'R', 'start2')}, 1)
        result = budget.sample({101: Process(101, 1, 101, 8, 'R', 'start2')}, 2)
        self.assertEqual(result['active_pids'], [101])
        self.assertGreater(result['pause_seconds'], 0)
        result = budget.sample({101: Process(101, 1, 101, 99, 'R', 'reused')}, 3)
        self.assertEqual(result['active_pids'], [])
        self.assertFalse(budget.report()['kernel_complete_membership'])

    def test_pid_reuse_within_ps_start_resolution_is_a_gap_not_supervisor_crash(self):
        budget = ArmBudget('arch-e1', 2.5, 0)
        original = Process(321, 1, 321, .20, 'R', 'Sun Oct 11 14:10:35 2026')
        budget.register(original, 'builder', 'arch-e1')
        reused = Process(321, 1, 321, .01, 'R', 'Sun Oct 11 14:10:35 2026')
        result = budget.sample({321: reused}, 1)
        self.assertEqual(result['active_pids'], [])
        self.assertIn('PID identity reused', budget.report()['attribution_gaps'][-1]['reason'])

    def test_snapshots_keep_runtime_builds_exclude_cache_and_relocate(self):
        source = self.root / 'source'; source.mkdir()
        for folder in ('deps', '_build', '.kitcache'):
            (source / folder).mkdir(); (source / folder / 'file').write_text('data')
        (source / 'kogen').write_text('#!/bin/sh\nexit 0\n'); safe_chmod(self.root, source / 'kogen', 0o755)
        destination = self.root / 'snap'
        result = capture(source, destination, lambda: nullcontext({'sampled': True}), 'FINAL', 'build')
        self.assertTrue((destination / '_build/file').exists())
        self.assertFalse((destination / '.kitcache').exists())
        self.assertEqual(tree_hash(destination), result['source_hash'])
        writable_copy(destination, self.root / 'score')
        (self.root / 'score/kogen').write_text('changed')
        self.assertEqual(tree_hash(destination), result['source_hash'])

    def test_hardlinked_files_capture_content_and_link_counts(self):
        source = self.root / 'hardlink-source'; source.mkdir()
        (source / 'object').write_text('git object bytes')
        os.link(source / 'object', source / 'object-alias')
        receipt = capture(source, self.root / 'hardlink-snapshot',
                          lambda: nullcontext({'sampled': True}), 'FINAL', 'build')
        self.assertEqual(tree_hash(source), tree_hash(self.root / 'hardlink-snapshot'))
        self.assertEqual(receipt['hardlink_counts'], {'object': 2, 'object-alias': 2})

    def test_one_arm_capture_failure_does_not_abort_another(self):
        arms = [SimpleNamespace(workspace=self.root / name, errors=[], capture_errors=[], arm=name,
                                 barrier=lambda: nullcontext({})) for name in ('arch-e1', 'arch-g1')]
        calls = []
        def fake_capture(workspace, destination, barrier, label, phase):
            calls.append(workspace.name)
            if workspace.name == 'arch-e1': raise OSError('fixture capture failure')
            return dict(label=label)
        with patch('arch_run.capture', side_effect=fake_capture):
            self.assertIsNone(capture_arm(arms[0], self.root / 'snap/e1', 'T+001m', 'build'))
            self.assertEqual(capture_arm(arms[1], self.root / 'snap/g1', 'T+001m', 'build')['label'], 'T+001m')
        self.assertEqual(calls, ['arch-e1', 'arch-g1'])
        self.assertEqual(len(arms[0].capture_errors), 1)
        self.assertEqual(arms[1].capture_errors, [])

    def test_scorer_profile_only_adds_ps_exec_and_process_observation(self):
        from arch_score import PROFILE
        self.assertIn('(allow process-exec (literal "/bin/ps") (with no-sandbox))', PROFILE)
        self.assertIn('(allow process-info*)', PROFILE)
        self.assertIn('(deny network-outbound)', PROFILE)

    def test_scorer_profile_allows_real_ps_observation(self):
        from arch_score import PROFILE
        sandbox = shutil.which('sandbox-exec')
        self.assertIsNotNone(sandbox, 'sandbox-exec is required for the scorer ps integration check')
        proc = subprocess.run([sandbox, '-p', PROFILE, '/bin/ps', '-p', str(os.getpid()),
                               '-o', 'pid=,ppid=,command='], text=True, capture_output=True, timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(proc.stdout.strip(), 'sandboxed ps returned no process observation')

    def test_dry_cell_fails_when_real_scorer_reports_error(self):
        with patch('arch_run.score', return_value=dict(scoring_error='ps denied')) as scorer:
            with self.assertRaisesRegex(RuntimeError, 'Dry cell scoring failed.*ps denied'):
                score_arms(self.root, ['arch-e1'], ('build',), dry=True)
        scorer.assert_called_once_with(self.root, 'arch-e1', 'build')

    def test_reference_snapshot_is_copied_hashed_and_scored_separately(self):
        root = self.root / 'dry-harness'; root.mkdir()
        allowed = self.root / 'allowed'; source = allowed / 'build/FINAL/arch-e1'
        source.mkdir(parents=True)
        (source / 'kogen').write_text('#!/bin/sh\necho fixture\n')
        safe_chmod(source, source / 'kogen', 0o755)
        calls = []
        def fake_score(target_root, arm, phase, snapshot, receipt):
            calls.append((target_root, arm, phase, Path(snapshot), Path(receipt)))
            self.assertTrue((Path(snapshot) / 'kogen').is_file())
            self.assertEqual(tree_hash(snapshot), tree_hash(source))
            return dict(scoring_error=None, scoring_wall_seconds=1.25, scoring_case_count=6)
        with patch('arch_run.score_snapshot', side_effect=fake_score):
            result = score_reference_snapshots(root, [source], allowed_roots=[allowed])
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1:3], ('arch-e1', 'build'))
        self.assertEqual(result['reference_snapshots'][0]['sha256'], tree_hash(source))
        self.assertEqual(result['reference_snapshots'][0]['arm_kind'], 'E')
        self.assertEqual(result['scored_case_count'], 6)
        self.assertTrue(result['scored_reference'])
        self.assertFalse(os.stat(calls[0][3] / 'kogen').st_mode & 0o222)

    def test_reference_scoring_error_fails(self):
        root = self.root / 'dry-harness'; root.mkdir()
        allowed = self.root / 'allowed'; source = allowed / 'build/FINAL/arch-e1'
        source.mkdir(parents=True); (source / 'kogen').write_text('candidate')
        with patch('arch_run.score_snapshot', return_value=dict(scoring_error='fixture scorer failure')):
            with self.assertRaisesRegex(RuntimeError, 'Reference scoring failed'):
                score_reference_snapshots(root, [source], allowed_roots=[allowed])

    def test_reference_outside_allowed_root_and_escaping_symlink_rejected(self):
        allowed = self.root / 'allowed'; allowed.mkdir()
        outside = self.root / 'outside/build/FINAL/arch-e1'; outside.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'outside allowed roots'):
            score_reference_snapshots(self.root / 'harness', [outside], allowed_roots=[allowed])
        source = allowed / 'build/FINAL/arch-e1'; source.mkdir(parents=True)
        external = self.root / 'secret'; external.write_text('outside')
        (source / 'escape').symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'escapes workspace'):
            score_reference_snapshots(self.root / 'harness', [source], allowed_roots=[allowed])

    def test_term_ignoring_detached_child_is_killed_and_recorded(self):
        workspace = self.root / 'detached-arm'; workspace.mkdir()
        child = subprocess.Popen(['/bin/sh', '-c', 'trap "" TERM; while :; do sleep 0.1; done'],
                                 cwd=workspace, start_new_session=True, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        try:
            time.sleep(.15)
            os.killpg(child.pid, signal.SIGTERM)
            time.sleep(.1)
            self.assertIsNone(child.poll(), 'test child should ignore the initial group TERM')
            proc_rows = f'{child.pid} sh -c trap "" TERM; while :; do sleep 0.1; done\n'
            killed, errors = kill_arm_orphans(workspace, proc_rows, {child.pid: str(workspace)})
            child.wait(timeout=5)
            self.assertIn(child.pid, [row['pid'] for row in killed])
            self.assertTrue(all(row['signal'] == 'SIGKILL' for row in killed))
            self.assertEqual(errors, [])
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait(timeout=5)
    def test_escaping_or_absolute_snapshot_links_rejected(self):
        source = self.root / 'source'; source.mkdir()
        (source / 'escape').symlink_to(self.root)
        with self.assertRaises(ValueError): tree_hash(source)

    def test_briefs_only_differ_by_constraint(self):
        template = (HERE / 'BRIEF-ARCH.tmpl').read_text()
        values = [render(template, arm).replace(CONSTRAINTS['E' if arm.startswith('arch-e') else 'G'], '{CONSTRAINT}') for arm in ARMS]
        self.assertEqual(len(set(values)), 1)
        self.assertEqual(PHASE_SECONDS, {'build': 5400, 'maintenance': 1800})

    def test_fresh_maintenance_cli_and_explicit_resume(self):
        config = dict(codex_executable='codex')
        fresh = argv(config, self.root)
        resumed = argv(config, self.root, 'exact-thread')
        self.assertNotIn('resume', fresh)
        self.assertEqual(resumed[-3:], ['resume', 'exact-thread', '-'])
        self.assertIn('features.multi_agent=false', fresh)

    def test_audit_never_treats_assistant_provider_prose_as_a_call(self):
        path = self.root / 'events.jsonl'
        events(path, [dict(item=dict(type='agent_message', text='api.openai.com is forbidden.')),
                      dict(item=dict(type='command_execution', command='curl https://api.openai.com/v1/responses')),
                      dict(item=dict(type='command_execution', command='cat ../tests/cases.py')),
                      dict(item=dict(type='command_execution', command='mix deps.get'))])
        result = audit_events([path], self.root / 'arch-e1')
        self.assertEqual({flag['reason'] for flag in result['flags']}, {'real model-provider call', 'protected outside read'})

    def test_audit_allows_system_toolchain_but_flags_private_and_other_arm_reads(self):
        workspace = self.root / 'arch-e1'
        workspace.mkdir()
        self.assertEqual(outside_reads('ls /Library/Developer/CommandLineTools/SDKs', workspace), [])
        self.assertTrue(outside_reads('ls ~/Library/Keychains', workspace))
        self.assertTrue(outside_reads('ls ' + str(self.root / 'arch-g1'), workspace))
        self.assertEqual(outside_reads('ls <scratch-dir>/race3-kit/bin', workspace), [])

    def test_audit_detects_patch_of_frozen_spec_even_if_restored(self):
        path = self.root / 'events.jsonl'
        events(path, [dict(type='response_item', payload=dict(type='function_call', name='apply_patch',
                       arguments='*** Begin Patch\n*** Update File: spec/SPEC.md\n@@\n-old\n+new\n*** End Patch'))])
        self.assertEqual(audit_events([path], self.root)['flags'][0]['reason'], 'frozen spec modification')

class Decisions(Base):
    def test_studio_wave_order_and_pairing_are_fixed(self):
        self.assertEqual(production_schedule('studio'), list(STUDIO_WAVES.items()))
        self.assertEqual(STUDIO_WAVES, {
            'A': ('arch-e1', 'arch-e2', 'arch-g1', 'arch-g2'),
            'B': ('arch-e3', 'arch-e4', 'arch-g3', 'arch-g4')})
        self.assertEqual(PAIRS[:4], (('arch-e1', 'arch-g1'), ('arch-e2', 'arch-g2'),
                                    ('arch-e3', 'arch-g3'), ('arch-e4', 'arch-g4')))
        self.assertEqual(pair_for_arm('arch-g3'), 'pair-3')

    def rows(self, e_fault=8, g_fault=5, e_tokens=150, g_tokens=100):
        return [dict(host=host, arm=arm, treatment='E' if arm.startswith('arch-e') else 'G',
                     valid=True, invalid_reasons=[], B={'passed': 1, 'total': 1},
                     F={'passed': e_fault if arm.startswith('arch-e') else g_fault, 'total': 12},
                     M={'passed': 1, 'total': 1},
                     total_tokens=e_tokens if arm.startswith('arch-e') else g_tokens,
                     agent_wall_seconds=100, build_test_seconds=5, repair_turns=1, loc={'build': {'Go': 4}})
                for host in ('studio',) for arm in STUDIO_ARMS]

    def test_boundary_E_win_and_cost_failure(self):
        self.assertEqual(decide(self.rows())['outcome'], 'E')
        self.assertEqual(decide(self.rows(e_tokens=151))['outcome'], 'G')
        self.assertEqual(decide(self.rows(e_fault=7))['outcome'], 'G')
        self.assertEqual(decide(self.rows(e_fault=5))['outcome'], 'G')

    def test_invalid_runs_excluded_three_valid_and_half_medians(self):
        rows = self.rows(); rows[0]['valid'] = False
        result = decide(rows)
        self.assertEqual(result['valid_runs']['E'], 3)
        self.assertEqual(result['outcome'], 'E')
        rows[1]['valid'] = False
        self.assertEqual(decide(rows)['outcome'], 'inconclusive')
        rows = self.rows()
        for row, value in zip([r for r in rows if r['treatment'] == 'E'], (6, 8, 9, 12)):
            row['F']['passed'] = value
        self.assertEqual(decide(rows)['medians']['E']['F'], 8.5)

    def test_missing_tokens_inconclusive_not_zero(self):
        rows = self.rows(); rows[0]['total_tokens'] = None
        self.assertEqual(decide(rows)['outcome'], 'inconclusive')

class Integration(Base):
    def test_arm_environment_uses_c_locale(self):
        config = dict(host='studio', kit='/kit', codex_executable='/tools/node/bin/codex',
                      toolchains=dict(go='/tools/go', elixir='/tools/elixir', erlang='/tools/erlang'))
        values = environment(self.root, 'arch-g1', config)
        self.assertEqual(values['LC_ALL'], 'C')
        self.assertEqual(values['LANG'], 'C')
        self.assertIn('/tools/node/bin', values['PATH'].split(os.pathsep))
        self.assertIn(str(Path.home() / '.local/share/mise/shims'), values['PATH'].split(os.pathsep))
        self.assertEqual(values['MISE_DATA_DIR'], str(Path.home() / '.local/share/mise'))
        self.assertEqual(values['MISE_TRUSTED_CONFIG_PATHS'], str(self.root / 'arch-g1'))
        self.assertEqual(values['MISE_OFFLINE'], '1')
        self.assertEqual(values['MISE_AUTO_INSTALL'], '0')
        self.assertIn('go = "1.27.1"', mise_config('arch-g1'))
        self.assertIn('node = "24.21.0"', mise_config('arch-g1'))
        self.assertNotIn('elixir =', mise_config('arch-g1'))
        self.assertIn('elixir = "1.20.4-otp-29"', mise_config('arch-e1'))
        self.assertIn('erlang = "29.1.1"', mise_config('arch-e1'))

    def test_tool_version_check_uses_arm_cwd_from_elsewhere(self):
        from arch_install import environment
        from arch_gates import check_tool_version
        workspace = self.root / 'arch-e1'; workspace.mkdir()
        (workspace / 'mise.toml').write_text(mise_config('arch-e1'))
        config = dict(host='studio', kit=str(self.root / 'kit'), codex_executable='/usr/bin/true',
                      mise_executable=shutil.which('mise') or '/opt/homebrew/bin/mise',
                      toolchains=dict(go=str(Path.home() / '.local/share/mise/installs/go/1.27.1'),
                                      elixir=str(Path.home() / '.local/share/mise/installs/elixir/1.20.4-otp-29'),
                                      erlang=str(Path.home() / '.local/share/mise/installs/erlang/29.1.1')))
        env = dict(os.environ, **environment(self.root, 'arch-e1', config))
        elsewhere = self.root / 'different-process-cwd'; elsewhere.mkdir()
        original = Path.cwd()
        try:
            os.chdir(elsewhere)
            output = check_tool_version('go', 'version', 'go1.27.1', env, workspace, timeout=15)
        finally:
            os.chdir(original)
        self.assertIn('go1.27.1', output)

    def test_prelaunch_gate_records_resolution_inside_arm_context(self):
        from arch_run import prelaunch_gate
        workspace = self.root / 'arch-e1'
        workspace.mkdir()
        bindir = self.root / 'bin'; bindir.mkdir()
        capture = self.root / 'codex-sandbox-call.json'
        names = ('codex', 'go', 'elixir', 'erl', 'mix', 'node', 'git')
        codex = bindir / 'codex'
        codex.write_text('#!' + sys.executable + '\n' +
            'import json, os, subprocess, sys\n'
            'args=sys.argv[1:]\n'
            'with open(os.environ["STUB_CAPTURE"], "w") as f: json.dump({"argv":args,"cwd":os.getcwd(),"arm_value":os.environ.get("ARM_VALUE"),"path":os.environ.get("PATH")},f)\n'
            'i=args.index("--")+1\n'
            'p=subprocess.run(args[i:],cwd=os.getcwd(),env=os.environ.copy(),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)\n'
            'sys.stdout.write(p.stdout);sys.stderr.write(p.stderr);sys.exit(p.returncode)\n')
        safe_chmod(self.root, codex, 0o755)
        for name in ('go', 'elixir', 'erl', 'mix', 'node', 'git'):
            executable = bindir / name
            executable.write_text('#!/bin/sh\nexit 0\n'); safe_chmod(self.root, executable, 0o755)
        mise = bindir / 'mise'
        mise.write_text('#!/bin/sh\nprintf "go 1.27.1\\nelixir 1.20.4-otp-29\\nnode 24.21.0\\n"\n')
        safe_chmod(self.root, mise, 0o755)
        arm_path = str(bindir) + os.pathsep + '/bin'
        arm = SimpleNamespace(workspace=workspace, root=self.root, arm='arch-e1',
                              env=dict(PATH=arm_path, ARM_VALUE='same-env', STUB_CAPTURE=str(capture)),
                              config=dict(codex_executable=str(codex)))
        record = prelaunch_gate(arm)
        observed = json.loads(capture.read_text())
        self.assertEqual(observed['cwd'], str(workspace.resolve()))
        self.assertEqual(observed['arm_value'], 'same-env')
        self.assertEqual(observed['path'], arm_path)
        script = ('printf "__ARCH_MISE_BEGIN__\\n"; mise current; ms=$?; '
                  'printf "__ARCH_MISE_END__%s\\n" "$ms"; status=0; '
                  'for tool in codex go elixir erl mix node git; do '
                  'found=$(command -v "$tool" 2>/dev/null) || found=""; '
                  'printf "__ARCH_COMMAND__%s=%s\\n" "$tool" "$found"; '
                  '[ -n "$found" ] || status=1; done; exit "$status"')
        expected = ['sandbox', '-c', 'sandbox_workspace_write.network_access=true',
                    '--', 'sh', '-c', script]
        self.assertEqual(observed['argv'], expected)
        self.assertEqual(record['argv'], [str(codex), *expected])
        self.assertEqual(record['exit_code'], 0)
        self.assertEqual(record['stderr_head'], '')
        self.assertEqual(record['mise_current'], 'go 1.27.1\nelixir 1.20.4-otp-29\nnode 24.21.0')
        self.assertEqual(set(record['command_v']), set(names))
        self.assertTrue((self.root / 'out/arch-e1/environment-check.json').is_file())

    def test_runner_hold_blocks_arm_launch(self):
        target, _, _ = self.fixture()
        from arch_config import load
        (target / 'HOLD').write_text('operator hold\n')
        arm = Arm(target, 'arch-g1', 'build', load(target),
                  dict(t0=time.monotonic(), deadline=time.monotonic() + 60,
                       epoch_utc=now(), kill_utc=now(), duration=5400))
        with self.assertRaisesRegex(RuntimeError, 'HOLD file blocks launch'):
            arm.launch()
        self.assertIsNone(arm.invocation)

    def fixture(self, external_link=None):
        inputs, source, kit = self.root / 'arch', self.root / 'lever', self.root / 'kit'
        for directory in (inputs / 'spec/quint', inputs / 'spec/features', inputs / 'tests', source, kit / 'bin',
                          kit / 'templates/go/docs', kit / 'templates/ex/docs', kit / 'cache', kit / 'templates/ex/deps',
                          kit / 'templates/ex/_build'):
            directory.mkdir(parents=True, exist_ok=True)
        for name in ('DESIGN-ARCH.md', 'DECISION-RULE-ARCH.md'):
            (inputs / name).write_text('Synthetic harness fixture; no kogen implementation.\n')
        (inputs / 'RULE-SHA256.txt').write_text(digest(inputs / 'DECISION-RULE-ARCH.md'))
        for name in ('SPEC.md', 'PROTOCOL.md', 'STEPS.md'):
            (inputs / 'spec' / name).write_text('Synthetic contract fixture.\n')
        (inputs / 'spec/quint/a.qnt').write_text('module fixture {}\n')
        (inputs / 'spec/features/a.feature').write_text('Feature: fixture\n')
        target = self.root / 'arch-harness'
        if external_link is not None:
            relative_target = os.path.relpath(external_link, target / 'arch-e1/spec/features')
            (inputs / 'spec/features/planted-link').symlink_to(relative_target)
        (inputs / 'tests/run_hidden.py').write_text('print("B01 [B] fixture\\nF01 [F] fixture\\nM01 [M] fixture")\n')
        (kit / 'env-aids.sh').write_text('# synthetic kit fixture\n')
        for language in ('go', 'ex'):
            (kit / 'templates' / language / 'AGENTS.md').write_text('# fixture language aid\n')
        (kit / 'templates/go/go.mod').write_text('module fixture\n')
        (kit / 'templates/ex/mix.exs').write_text('# fixture\n')
        for name in ('golangci-lint', 'goimports', 'gofumpt', 'gopls', 'gotestsum'):
            (kit / 'bin' / name).write_text('#!/bin/sh\nexit 0\n')
        pins = dict(env_aids_sha256=digest(kit / 'env-aids.sh'), race5_full_kit_manifest_sha256='fixture')
        dump(source / 'KIT-PINS-v2.json', pins)
        (source / 'CODEX-VERSION').write_text('fixture\n')
        (source / 'kitsum.sh').write_text('#!/bin/sh\nexit 0\n')
        fake_mise = self.root / 'mise'; fake_mise.write_text('#!/bin/sh\nexit 0\n'); safe_chmod(self.root, fake_mise, 0o755)
        args = SimpleNamespace(target=str(target), source_harness=str(source), arch_input=str(inputs), kit=str(kit),
                               host='studio', go=str(self.root / 'go'), elixir=str(self.root / 'elixir'),
                               erlang=str(self.root / 'erlang'), codex_home=str(self.root / 'auth'),
                               mise_executable=str(fake_mise))
        install(args)
        if external_link is not None:
            return target, None, None
        frozen = freeze(target)
        evidence = dict(mode='analysis', drop_list=[], analysis=dict(per_case={case: dict.fromkeys(
            ('spec_lint', 'contradictions', 'quint', 'mechanics'), True) for case in frozen['cases']},
            checks={}, input_hashes={p: sha for p, sha in frozen['files'].items() if p.startswith(('spec/', 'tests/'))}))
        for name in ('spec_lint', 'contradictions', 'quint', 'mechanics'):
            proof = self.root / (name + '.json'); dump(proof, dict(passed=True, scope='synthetic gate fixture',
                inputs={p: sha for p, sha in frozen['files'].items() if p.startswith(('spec/', 'tests/'))}))
            evidence['analysis']['checks'][name] = dict(path=str(proof), sha256=digest(proof))
        evidence_path = self.root / 'evidence.json'; dump(evidence_path, evidence)
        verify(target, evidence_path, dry=True, platform_checks=False)
        return target, frozen, evidence_path

    def test_install_gate_score_missing_binary_and_freeze_tamper(self):
        target, frozen, proof = self.fixture()
        self.assertTrue((target / 'arch-e1/mix.exs').is_file())
        self.assertTrue((target / 'arch-e1/go.mod').is_file())
        self.assertIn('.local/share/mise/shims/go', (target / 'arch-e1/.kit-tools/go').read_text())
        self.assertIn('.local/share/mise/shims/mix', (target / 'arch-e1/.kit-tools/mix').read_text())
        self.assertEqual(json.loads((target / 'out/arch-e1/environment.json').read_text())['MISE_TRUSTED_CONFIG_PATHS'],
                         str(target / 'arch-e1'))
        self.assertFalse((target / 'arch-g1/mix.exs').exists())
        self.assertTrue((target / 'spec/SPEC.md').is_file())
        kit_env = target / 'arch-e1/.kit-env.sh'
        kit_tools = target / 'arch-e1/.kit-tools'
        self.assertFalse(stat.S_IMODE(kit_env.stat().st_mode) & 0o222)
        self.assertFalse(stat.S_IMODE(kit_tools.stat().st_mode) & 0o222)
        for path in kit_tools.iterdir():
            if not path.is_symlink(): self.assertFalse(stat.S_IMODE(path.stat().st_mode) & 0o222)
        snapshot = target / 'snapshots/build/FINAL/arch-g1'
        capture(target / 'arch-g1', snapshot, lambda: nullcontext({'sampled': True}), 'FINAL', 'build')
        result = score(target, 'arch-g1', 'build')
        self.assertIsNone(result['scoring_error'])
        self.assertEqual(result['groups']['F'], dict(passed=0, total=1))
        (target / 'BRIEF-ARCH.tmpl').write_text('tampered')
        with self.assertRaises(ValueError): check_freeze(target)

    def test_arm_frozen_input_change_is_scoped_to_its_arm(self):
        target, _, _ = self.fixture()
        path = target / 'arch-e1/.kit-env.sh'
        safe_chmod(target, path, 0o644)
        path.write_text(path.read_text() + '# simulated agent edit\n')
        check_freeze(target, skip_arm_files=True)
        check_freeze(target, only_arm='arch-g1')
        with self.assertRaisesRegex(ValueError, 'arch-e1/.kit-env.sh'):
            check_freeze(target, only_arm='arch-e1')
        with self.assertRaisesRegex(ValueError, 'arch-e1/.kit-env.sh'):
            check_freeze(target)

    def test_external_symlink_mode_is_untouched_by_install_snapshot_and_copy(self):
        outside = self.root / 'outside-venv-python'
        outside.write_text('external target\n')
        safe_chmod(self.root, outside, 0o640)
        before = stat.S_IMODE(outside.stat().st_mode)
        target, _, _ = self.fixture(external_link=outside)
        workspace = target / 'arch-e1'
        planted = workspace / 'spec/features/planted-link'
        self.assertTrue(planted.is_symlink())
        self.assertEqual(planted.resolve(), outside.resolve())
        self.assertEqual(stat.S_IMODE(outside.stat().st_mode), before)
        with self.assertRaisesRegex(ValueError, 'outside target root'):
            safe_chmod(target, planted, 0o600)
        self.assertEqual(stat.S_IMODE(outside.stat().st_mode), before)

        snapshot = target / 'snapshots/build/FINAL/arch-e1'
        with self.assertRaisesRegex(ValueError, 'Snapshot link escapes workspace'):
            capture(workspace, snapshot, lambda: nullcontext({'sampled': True}), 'FINAL', 'build')
        self.assertEqual(stat.S_IMODE(outside.stat().st_mode), before)

        copy = target / 'arch-e1-copy'
        writable_copy(workspace, copy)
        self.assertTrue((copy / 'spec/features/planted-link').is_symlink())
        self.assertEqual(stat.S_IMODE(outside.stat().st_mode), before)

    def test_analysis_stale_or_missing_checks_block(self):
        target, frozen, path = self.fixture()
        evidence = json.loads(path.read_text())
        evidence['analysis']['per_case']['B01']['mechanics'] = False
        dump(path, evidence)
        with self.assertRaises(ValueError): verify(target, path, dry=True, platform_checks=False)

    def test_phase_manager_fresh_stores_and_continuation_history(self):
        target, frozen, evidence = self.fixture()
        from arch_config import load
        class FakeProcess:
            def poll(self): return 0
        class FakeSupervisor:
            def __init__(self, args):
                self.args, self.stopped, self.paused = args, False, set()
                self.children = {}; self.private = Path(args.private); self.private.mkdir()
                self.observer = lambda: {}
                self.budget = SimpleNamespace(sample=lambda *args: {}, report=lambda: dict(cores=args.cores))
            def request(self, request):
                identity = uuid.uuid4().hex; output = self.private / identity; output.mkdir()
                command = request['argv']
                thread = command[command.index('resume') + 1] if 'resume' in command else str(uuid.uuid4())
                events(output / 'stdout', [dict(type='thread.started', thread_id=thread),
                    dict(item=dict(type='agent_message', text='ALL TESTS PASS'))])
                (output / 'stderr').write_text('')
                self.children[identity] = FakeProcess()
                return dict(handle=identity, pid=0, identity=identity, output=str(output))
            def stop(self): self.stopped = True
            def signal_members(self, sig): pass
        config = load(target)
        source_auth_home = Path(config['source_codex_home'])
        source_auth_home.mkdir(parents=True, exist_ok=True)
        source_auth = source_auth_home / 'auth.json'
        source_auth.touch()
        clock = dict(t0=time.monotonic(), deadline=time.monotonic() + 60, epoch_utc=now(), kill_utc=now(), duration=5400)
        with patch('arch_run.Supervisor', FakeSupervisor), patch('arch_run.prelaunch_gate'):
            build = Arm(target, 'arch-e1', 'build', config, clock)
            build_auth = build.home / 'auth.json'
            self.assertTrue(build_auth.is_symlink())
            self.assertFalse(stat.S_ISREG(build_auth.lstat().st_mode))
            self.assertTrue(Path(os.readlink(build_auth)).is_absolute())
            build.launch(); build.poll(); build.finish()
            maintenance = Arm(target, 'arch-e1', 'maintenance', config, dict(clock, duration=1800))
            maintenance_auth = maintenance.home / 'auth.json'
            self.assertTrue(maintenance_auth.is_symlink())
            self.assertFalse(stat.S_ISREG(maintenance_auth.lstat().st_mode))
            self.assertEqual(os.readlink(maintenance_auth), str(source_auth.absolute()))
            maintenance.launch(); maintenance.finish()
        self.assertNotEqual(build.thread, maintenance.thread)
        self.assertNotEqual(build.home, maintenance.home)
        self.assertEqual(build.workspace, maintenance.workspace)
        self.assertEqual(len(build.history), 2)
        self.assertEqual(repairs(sorted(build.output.glob('turn-*.jsonl')))['repair_turns'], 1)

    def test_empty_early_codex_exit_is_flagged_with_exit_status(self):
        target, _, _ = self.fixture()
        from arch_config import load
        config = load(target)
        fake = self.root / 'fake-codex'
        fake.write_text('#!/bin/sh\nexit 23\n')
        safe_chmod(self.root, fake, 0o755)
        config['codex_executable'] = str(fake)

        class Exited:
            def __init__(self, status): self.status = status
            def poll(self): return self.status

        class FakeSupervisor:
            def __init__(self, args):
                self.args, self.children, self.stopped = args, {}, False
                self.private = Path(args.private); self.private.mkdir(parents=True)
            def request(self, request):
                handle = 'fake-child'; output = self.private / handle; output.mkdir()
                with (output / 'stdout').open('wb') as stdout, (output / 'stderr').open('wb') as stderr:
                    result = subprocess.run(request['argv'], cwd=request['cwd'], env=request['env'],
                                            input=request['stdin'].encode(), stdout=stdout, stderr=stderr)
                self.children[handle] = Exited(result.returncode)
                return dict(handle=handle, pid=123, identity='123@fixture', output=str(output))

        clock = dict(t0=time.monotonic(), deadline=time.monotonic() + 60,
                     epoch_utc=now(), kill_utc=now(), duration=60)
        with patch('arch_run.Supervisor', FakeSupervisor), patch('arch_run.prelaunch_gate'):
            arm = Arm(target, 'arch-e1', 'build', config, clock)
            arm.launch()
            with self.assertRaisesRegex(InfraLaunchError, 'exit code 23'):
                arm.poll()
        receipt = json.loads((arm.output / 'launch-1.json').read_text())
        flag = json.loads((arm.output / 'INFRA-FAILURE.json').read_text())
        flag_infrastructure(target, 'build', arm, flag['reason'], 'zero-events-early-exit')
        flag = json.loads((arm.output / 'INFRA-FAILURE.json').read_text())
        self.assertEqual(receipt['exit_code'], 23)
        self.assertIsNone(receipt['signal_number'])
        self.assertEqual(receipt['stderr_first_4kb'], '')
        self.assertEqual(flag['exit_code'], 23)

    def test_evidence_generator_does_not_bless_stale_analysis(self):
        target, frozen, evidence = self.fixture()
        directory = self.root / 'analysis'; directory.mkdir()
        from arch_evidence import FILES
        for name in FILES.values():
            dump(directory / name, dict(passed=True, inputs={p: sha for p, sha in frozen['files'].items()
                                                           if p.startswith(('spec/', 'tests/'))}))
        ledger = self.root / 'ledger.json'
        dump(ledger, dict(per_case={case: dict.fromkeys(('spec_lint', 'contradictions', 'quint', 'mechanics'), True)
                                  for case in frozen['cases']}, drop_list=[]))
        studio = self.root / 'ledger-dry-studio.json'
        dump(studio, dict(host='studio', mode='dry', passed=True, contract_sha256=contract_hash(frozen),
                          arms=['arch-e1', 'arch-g1'], cap_seconds=600,
                          scoring_wall_seconds=1.0, scored_case_count=1, audit_runs=1, analyzer_runs=1))
        result = build_evidence(target, directory, ledger, dry_studio=studio, production=True)
        self.assertEqual(result['mode'], 'analysis')
        proof = json.loads((directory / 'spec-lint.json').read_text())
        proof['inputs']['spec/SPEC.md'] = 'stale'
        dump(directory / 'spec-lint.json', proof)
        with self.assertRaises(ValueError): build_evidence(target, directory, ledger, dry_studio=studio, production=True)

    def test_production_gate_requires_studio_dry_only(self):
        target, frozen, _ = self.fixture()
        directory = self.root / 'production-analysis'; directory.mkdir()
        from arch_evidence import FILES
        per_case = {case: dict.fromkeys(('spec_lint', 'contradictions', 'quint', 'mechanics'), True)
                    for case in frozen['cases']}
        for name in FILES.values():
            dump(directory / name, dict(passed=True, inputs={p: sha for p, sha in frozen['files'].items()
                                                            if p.startswith(('spec/', 'tests/'))}))
        ledger = self.root / 'production-ledger.json'
        dump(ledger, dict(per_case=per_case, drop_list=[]))
        studio = self.root / 'DRY-studio.json'
        dry_receipt = dict(host='studio', mode='dry', passed=True,
                           contract_sha256=contract_hash(frozen), arms=['arch-e1', 'arch-g1'], cap_seconds=600,
                           scoring_wall_seconds=1.25, scored_case_count=1, audit_runs=1, analyzer_runs=1)
        dump(studio, dry_receipt)
        evidence = self.root / 'production-evidence.json'
        # Dry evidence uses reviewed analysis but does not yet have a dry receipt.
        dry_result = build_evidence(target, directory, ledger)
        self.assertNotIn('studio', dry_result['dry'])
        dry_evidence = self.root / 'dry-evidence.json'; dump(dry_evidence, dry_result)
        verify(target, dry_evidence, dry=True, platform_checks=False)

        with self.assertRaisesRegex(ValueError, 'passing Studio dry receipt'):
            build_evidence(target, directory, ledger, production=True)
        failed_studio = self.root / 'DRY-studio-failed.json'
        dump(failed_studio, dict(host='studio', mode='dry', passed=False,
                                 contract_sha256=contract_hash(frozen), arms=['arch-e1', 'arch-g1'], cap_seconds=600))
        with self.assertRaisesRegex(ValueError, 'passing one-wave Studio dry receipt'):
            build_evidence(target, directory, ledger, dry_studio=failed_studio, production=True)
        for field, value in (('scoring_wall_seconds', 0), ('scored_case_count', 0)):
            invalid = dict(dry_receipt, **{field: value})
            path = self.root / ('DRY-zero-' + field + '.json'); dump(path, invalid)
            with self.assertRaisesRegex(ValueError, 'scoring, audit, and analyzer metrics'):
                build_evidence(target, directory, ledger, dry_studio=path, production=True)
        result = build_evidence(target, directory, ledger, dry_studio=studio, production=True)
        self.assertEqual(set(result['dry']), {'studio'})
        dump(evidence, result)
        verify(target, evidence, dry=False, platform_checks=False)

        from arch_evidence import reference
        for field, value in (('scoring_wall_seconds', 0), ('scored_case_count', 0)):
            invalid_path = self.root / ('DRY-gate-zero-' + field + '.json')
            dump(invalid_path, dict(dry_receipt, **{field: value}))
            invalid_evidence = copy.deepcopy(result)
            invalid_evidence['dry']['studio'] = reference(invalid_path)
            invalid_evidence_path = self.root / ('gate-zero-' + field + '.json')
            dump(invalid_evidence_path, invalid_evidence)
            with self.assertRaisesRegex(ValueError, 'scoring, audit, and analyzer metrics'):
                verify(target, invalid_evidence_path, dry=False, platform_checks=False)

        reference_receipt = dict(dry_receipt, arm_scoring_wall_seconds=0, arm_scored_case_count=0,
                                  scoring_wall_seconds=2.0, scored_case_count=8,
                                  reference_scoring_wall_seconds=2.0, reference_scored_case_count=8,
                                  scored_reference=True,
                                  reference_snapshots=[dict(source_path='/fixture/arch-e1', sha256='abc', arm_kind='E')])
        ref_dry = self.root / 'DRY-reference.json'; dump(ref_dry, reference_receipt)
        result = build_evidence(target, directory, ledger, dry_studio=ref_dry, production=True)
        dump(evidence, result)
        verify(target, evidence, dry=False, platform_checks=False)

        # A failed optional MacBook receipt may be described but cannot gate.
        macbook = self.root / 'DRY-macbook.json'
        dump(macbook, dict(host='macbook', mode='dry', passed=False))
        result = build_evidence(target, directory, ledger, dry_macbook=macbook, dry_studio=studio, production=True)
        dump(evidence, result)
        verify(target, evidence, dry=False, platform_checks=False)
        self.assertEqual(set(result['dry']), {'studio', 'macbook'})
        self.assertFalse(build_evidence(target, directory, ledger, dry_macbook=self.root / 'absent.json',
                                        dry_studio=studio, production=True)['dry'].get('macbook'))

    def test_incomplete_phase_produces_invalid_rows(self):
        target, frozen, evidence = self.fixture()
        dump(target / 'ARCH-START.json', dict(host='studio', mode='production', arms=list(STUDIO_ARMS)))
        result = finalize(target)
        self.assertEqual(len(result['runs']), len(STUDIO_ARMS))
        self.assertTrue(all(not row['valid'] for row in result['runs']))
        self.assertTrue(all(row['total_tokens'] is None for row in result['runs']))

    def test_full_phase_accounting_and_two_host_report(self):
        target, frozen, evidence = self.fixture()
        from arch_config import load
        config = load(target)
        dump(target / 'ARCH-START.json', dict(host='studio', mode='production', arms=list(STUDIO_ARMS)))
        for arm in STUDIO_ARMS:
            for phase in ('build', 'maintenance'):
                directory = target / 'out' / arm / ('phase-' + phase)
                directory.mkdir()
                sessions = directory / 'sessions'; sessions.mkdir()
                thread = str(uuid.uuid4())
                at = now(); cwd = str(target / arm)
                events(directory / 'turn-1.jsonl', [dict(type='thread.started', thread_id=thread),
                    dict(item=dict(type='agent_message', text='ALL TESTS PASS'))])
                events(sessions / ('rollout-' + thread + '.jsonl'), [dict(type='session_meta', payload=dict(id=thread, cwd=cwd)),
                    dict(type='turn_context', timestamp=at, payload=dict(cwd=cwd, model=MODEL, effort=EFFORT)), token(at, 10)])
                dump(directory / 'PHASE.json', dict(arm=arm, phase=phase, cwd=cwd, sessions=str(sessions),
                     kill_utc=now(), deadline=10, agent_wall_seconds=1, cpu={}, errors=[]))
                capture(target / arm, target / 'snapshots' / phase / 'FINAL' / arm,
                        lambda: nullcontext({'sampled': True}), 'FINAL', phase)
                groups = {'B': dict(passed=1, total=1), 'F': dict(passed=1, total=1)} if phase == 'build' else {'M': dict(passed=1, total=1)}
                dump(target / 'out' / arm / ('score-' + phase + '.json'), dict(groups=groups, scoring_error=None))
        result = finalize(target)
        self.assertTrue(all(row['valid'] for row in result['runs']))
        self.assertEqual({row['wave'] for row in result['runs']}, {'A', 'B'})
        self.assertTrue(all(row['deciding'] for row in result['runs']))
        self.assertTrue(all(row['total_tokens'] == 40 for row in result['runs']))
        optional = dict(host='macbook', mode='production', optional_status='interrupted', runs=[],
                        drop_list=['optional host unavailable'], evidence_sha256=None)
        decision = report([result, optional])
        self.assertEqual(decision['decision']['outcome'], 'G')
        self.assertEqual(decision['decision']['valid_runs'], {'E': 4, 'G': 4})
        self.assertEqual(len(decision['runs']), 8)
        self.assertEqual(len(decision['optional_runs']), 4)
        self.assertEqual(decision['optional_host_status'], 'interrupted: optional host unavailable')
        self.assertTrue(all('interrupted: optional host unavailable' in row['invalid_reasons']
                            for row in decision['optional_runs']))
        without_optional = report([result])
        self.assertEqual(without_optional['decision'], decision['decision'])
        self.assertEqual(without_optional['optional_host_status'], 'interrupted: optional host unavailable')
        observed_mac = dict(host='macbook', mode='production', optional_status='descriptive',
                            drop_list=[], evidence_sha256='fixture', runs=[
            dict(host='macbook', arm=arm, treatment='E' if arm.startswith('arch-e') else 'G',
                 valid=True, invalid_reasons=[], total_tokens=1, F={'passed': 0 if arm.startswith('arch-e') else 12,
                 'total': 12}, B={'passed': 1, 'total': 12}, M={'passed': 1, 'total': 1})
            for arm in MACBOOK_ARMS])
        descriptive = report([result, observed_mac])
        self.assertEqual(descriptive['decision'], without_optional['decision'])
        self.assertEqual(len(descriptive['optional_runs']), 4)
        self.assertTrue(all(not row['deciding'] for row in descriptive['optional_runs']))
        rows = copy.deepcopy(result['runs'])
        rows[0]['valid'] = False
        rows[0]['invalid_reasons'] = ['fixture invalid']
        result_without_pair = dict(result, runs=rows)
        filtered = report([result_without_pair])
        self.assertNotIn('pair-1', filtered['decision']['included_pairs'])
        self.assertIn('pair-1', [row['pair'] for row in filtered['decision']['excluded_pairs']])
        self.assertIn('Criterion (ii)', markdown(decision))
        with self.assertRaises(ValueError): report([dict(result, runs=result['runs'][:-1])])

def main():
    clean_selfcheck_roots()
    result = None
    try:
        suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        dump(HERE / 'SELF-CHECK.json', dict(passed=result.wasSuccessful(), tests_run=result.testsRun,
                                            failures=len(result.failures), errors=len(result.errors),
                                            scope='offline synthetic receipts and sampled process tables; no live model, no host launch, no passability claim'))
        return 0 if result.wasSuccessful() else 1
    finally:
        clean_selfcheck_roots()

if __name__ == '__main__':
    raise SystemExit(main())
