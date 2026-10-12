#!/usr/bin/env python3
"""Four arms: shared 90-minute build, independent fresh 30-minute maintenance."""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from arch_config import (CORES, MODEL, EFFORT, PHASE_SECONDS, CONTINUATION, STUDIO_WAVES,
                         STUDIO_ARMS, MACBOOK_ARMS, load, dump)
from arch_cpu import Supervisor
from arch_budget import observe
from arch_snapshot import capture, tree_hash, copy_reference_snapshot
from arch_score import score, score_snapshot
from arch_config import treatment

ARM_SANDBOX_OVERRIDES = (
    'features.multi_agent=false',
    'features.unified_exec=false',
    'sandbox_workspace_write.network_access=true',
    'approval_policy="never"',
)

class InfraLaunchError(RuntimeError):
    """A launcher failed before emitting any Codex event."""

def flag_infrastructure(root, phase, arm, reason, category, **details):
    record = dict(arm=arm.arm, phase=phase, reason=str(reason), category=category,
                  classified='infrastructure', **details)
    local = arm.output / 'INFRA-FAILURE.json'
    global_path = Path(root) / ('INFRA-FAILURE-' + phase + '-' + arm.arm + '.json')
    for path in (local, global_path):
        if path.is_file():
            prior = json.loads(path.read_text())
            if isinstance(prior, dict):
                prior.update(record)
                record = prior
        dump(path, record)
    (Path(root) / 'STOP').touch()

def utc(epoch=None):
    return datetime.fromtimestamp(time.time() if epoch is None else epoch, timezone.utc).isoformat()

def check_hold(root):
    hold = Path(root) / 'HOLD'
    if hold.exists():
        detail = hold.read_text(errors='replace').strip()
        raise RuntimeError('HOLD file blocks launch' + (': ' + detail if detail else ''))

def capture_arm(arm, destination, label, phase):
    try:
        return capture(arm.workspace, destination, arm.barrier, label, phase)
    except Exception as error:
        message = f'{label} capture failed: {error}'
        arm.errors.append(message)
        arm.capture_errors.append(dict(label=label, phase=phase, error=str(error)))
        return None

def prelaunch_gate(arm, runner=subprocess.run):
    tools = ('codex', 'go', 'elixir', 'erl', 'mix', 'node', 'git')
    script = 'printf "__ARCH_MISE_BEGIN__\\n"; mise current; ms=$?; printf "__ARCH_MISE_END__%s\\n" "$ms"; '
    script += 'status=0; for tool in ' + ' '.join(tools) + '; do '
    script += 'found=$(command -v "$tool" 2>/dev/null) || found=""; '
    script += 'printf "__ARCH_COMMAND__%s=%s\\n" "$tool" "$found"; '
    script += '[ -n "$found" ] || status=1; done; exit "$status"'
    workspace = arm.workspace.resolve()
    codex = arm.config['codex_executable']
    command = [codex, 'sandbox', '-c', 'sandbox_workspace_write.network_access=true',
               '--', 'sh', '-c', script]
    result = runner(command, cwd=str(workspace),
                    env=arm.env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    current, command_v, in_mise, mise_status = [], {}, False, None
    for line in result.stdout.splitlines():
        if line == '__ARCH_MISE_BEGIN__':
            in_mise = True
        elif line.startswith('__ARCH_MISE_END__'):
            in_mise = False
            try: mise_status = int(line.removeprefix('__ARCH_MISE_END__'))
            except ValueError: mise_status = -1
        elif line.startswith('__ARCH_COMMAND__'):
            key, _, value = line.removeprefix('__ARCH_COMMAND__').partition('=')
            command_v[key] = value or None
        elif in_mise:
            current.append(line)
    record = dict(argv=command, cwd=str(workspace), sandbox='codex sandbox', mise_current='\n'.join(current),
                  mise_exit_code=mise_status, command_v=command_v,
                  exit_code=result.returncode, stderr_head=result.stderr[:4096])
    receipt_path = arm.root / 'out' / arm.arm / 'environment-check.json'
    prior = json.loads(receipt_path.read_text()) if receipt_path.is_file() else dict(arm=arm.arm, checks=[])
    record['launch_number'] = len(prior.get('checks', [])) + 1
    prior.setdefault('checks', []).append(record)
    dump(receipt_path, prior)
    missing = sorted(set(tools) - {name for name, value in command_v.items() if value})
    if result.returncode or mise_status != 0 or missing:
        raise RuntimeError('arm environment gate failed; missing=' + ','.join(missing) +
                           '; mise_exit=' + str(mise_status) + '; command_exit=' + str(result.returncode) +
                           '; stderr=' + result.stderr[:512])
    return record

def argv(config, workspace, thread=None):
    command = [config['codex_executable'], 'exec', '-C', str(workspace), '-m', MODEL,
               '-c', 'model_reasoning_effort="high"']
    for override in ARM_SANDBOX_OVERRIDES:
        command += ['-c', override]
    command += [
               '-c', 'web_search="live"',
               '--ignore-user-config', '--skip-git-repo-check', '--json']
    return command + (['resume', thread, '-'] if thread else ['-s', 'workspace-write', '-'])

class Arm:
    def __init__(self, root, arm, phase, config, clock):
        self.root, self.arm, self.phase = root, arm, phase
        self.workspace = root / arm
        self.output = root / 'out' / arm / ('phase-' + phase)
        self.output.mkdir(parents=True, exist_ok=False)
        self.home = self.output / 'codex-home'
        self.home.mkdir(mode=0o700)
        auth = Path(config['source_codex_home']) / 'auth.json'
        if auth.is_file():
            (self.home / 'auth.json').symlink_to(auth.absolute())
        self.env = dict(os.environ)
        # Do not inherit frozen lever clocks, role stores or launch switches.
        for key in list(self.env):
            if key.startswith(('LEVER_', 'RACE_', 'KOGEN_')):
                self.env.pop(key)
        self.env.update(json.loads((root / 'out' / arm / 'environment.json').read_text()))
        self.env.update(CODEX_HOME=str(self.home), PYTHONDONTWRITEBYTECODE='1', ARCH_PHASE=phase)
        self.cpu = Supervisor(SimpleNamespace(arm=arm, root=str(root), private=str(self.output / 'cpu'),
                                             cores=CORES[config['host']], t0=clock['t0'], deadline=clock['deadline']))
        self.lock = threading.RLock()
        self.frozen = False
        self.config, self.clock = config, clock
        self.thread, self.invocation, self.turn, self.first_start = None, None, 0, None
        self.history, self.errors = [], []
        self.capture_errors = []
        self.stdout_bytes = 0
        self.launch_record = None
        self.completed = False
        self.kill_monotonic = None

    def launch(self):
        check_hold(self.root)
        prelaunch_gate(self)
        self.turn += 1
        prompt = CONTINUATION if self.thread else (self.root / (
            'MAINTENANCE-ARCH.md' if self.phase == 'maintenance' else 'BRIEF-' + self.arm + '.md')).read_text()
        invocation = dict(operation='launch', arm=self.arm, role='builder',
                          argv=argv(self.config, self.workspace, self.thread), cwd=str(self.workspace),
                          env=self.env, stdin=prompt)
        with self.lock:
            reply = self.cpu.request(invocation)
        self.invocation = dict(**reply, launched_monotonic=time.monotonic(),
                               event_path=str(self.output / ('turn-' + str(self.turn) + '.jsonl')))
        if self.first_start is None:
            self.first_start = max(self.clock['t0'], self.invocation['launched_monotonic'])
        self.launch_record = dict(arm=self.arm, phase=self.phase, turn=self.turn, argv=invocation['argv'],
                  prompt_sha256=__import__('hashlib').sha256(prompt.encode()).hexdigest(),
                  resumed_thread=self.thread, requested_model=MODEL, requested_effort=EFFORT,
                  deadline_monotonic=self.clock['deadline'], **self.invocation,
                  exit_code=None, signal_number=None, signal_name=None, stderr_first_4kb='')
        dump(self.output / ('launch-' + str(self.turn) + '.json'), self.launch_record)

    def sync(self, force=False):
        if not self.invocation:
            return None
        source = Path(self.invocation['output'])
        destination = Path(self.invocation['event_path'])
        code = self.cpu.children[self.invocation['handle']].poll()
        if force or code is not None:
            shutil.copyfile(source / 'stdout', destination)
            stderr_path = self.output / ('turn-' + str(self.turn) + '.stderr')
            shutil.copyfile(source / 'stderr', stderr_path)
            self.stdout_bytes = (source / 'stdout').stat().st_size
            if self.launch_record is not None:
                with stderr_path.open('rb') as stderr_stream:
                    stderr_data = stderr_stream.read(4096)
                self.launch_record.update(exit_code=code,
                    signal_number=(-code if code is not None and code < 0 else None),
                    signal_name=(signal.Signals(-code).name if code is not None and code < 0 else None),
                    stderr_first_4kb=stderr_data.decode('utf-8', errors='replace'),
                    stderr_sample_bytes=len(stderr_data),
                    stderr_truncated=stderr_path.stat().st_size > len(stderr_data))
                dump(self.output / ('launch-' + str(self.turn) + '.json'), self.launch_record)
        # thread.started is an initial CLI record. Avoid recopying/parsing the
        # growing transcript ten times a second throughout a two-hour run.
        with (source / 'stdout').open() as stream:
            initial = stream.read(65536)
        for line in initial.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get('type') == 'thread.started':
                thread = event['thread_id']
                if self.thread is not None and thread != self.thread:
                    raise ValueError('Continuation changed the phase thread')
                self.thread = thread
        return code

    def poll(self):
        if self.completed or self.cpu.stopped:
            return
        code = self.sync()
        if code is None:
            if self.thread is None and time.monotonic() > self.invocation['launched_monotonic'] + 60:
                raise RuntimeError('Missing thread.started after 60 seconds')
            return
        self.history.append(dict(turn=self.turn, exit_code=code,
                                 started_monotonic=self.invocation['launched_monotonic'],
                                 completed_monotonic=time.monotonic(), thread_id=self.thread))
        if self.thread is None and self.stdout_bytes == 0:
            reason = f'Infrastructure launch failure: zero events and early exit (exit code {code})'
            flag_infrastructure(self.root, self.phase, self, reason, 'zero-events-early-exit',
                turn=self.turn, exit_code=code,
                signal_number=(-code if code is not None and code < 0 else None),
                stderr_first_4kb=(self.launch_record or {}).get('stderr_first_4kb', ''))
            raise InfraLaunchError(reason)
        if code != 0:
            raise RuntimeError('Builder client failed: exit ' + str(code))
        if not self.thread:
            raise RuntimeError('Builder completed without session ID')
        if time.monotonic() < self.clock['deadline']:
            self.launch()

    def tick(self, rows=None):
        with self.lock:
            if self.cpu.stopped:
                return
            original = self.cpu.observer
            if rows is not None:
                self.cpu.observer = lambda: rows
            try:
                if self.frozen and time.monotonic() < self.clock['deadline'] and not (self.root / 'STOP').exists():
                    self.cpu.budget.sample(self.cpu.observer(), time.monotonic())
                else:
                    self.cpu.tick()
            finally:
                self.cpu.observer = original

    @contextmanager
    def barrier(self):
        with self.lock:
            self.frozen = True
            self.cpu.budget.sample(self.cpu.observer(), time.monotonic())
            self.cpu.signal_members(signal.SIGSTOP)
        try:
            yield dict(enforcement='race5-level', membership='sampled retained process identities',
                       all_observed_writers_quiesced=True, kernel_complete_membership=False)
        finally:
            with self.lock:
                self.frozen = False
                if not self.cpu.stopped and not self.cpu.paused:
                    self.cpu.signal_members(signal.SIGCONT)

    def stop(self):
        with self.lock:
            if self.kill_monotonic is None:
                self.kill_monotonic = min(time.monotonic(), self.clock['deadline'])
            if not self.cpu.stopped:
                self.cpu.stop()
        self.sync(force=True)

    def finish(self):
        self.stop()
        if self.invocation and not any(row['turn'] == self.turn for row in self.history):
            self.history.append(dict(turn=self.turn,
                                     exit_code=self.cpu.children[self.invocation['handle']].poll(),
                                     started_monotonic=self.invocation['launched_monotonic'],
                                     completed_monotonic=min(time.monotonic(), self.clock['deadline']),
                                     thread_id=self.thread))
        snapshot_error = None
        try:
            capture(self.workspace, self.root / 'snapshots' / self.phase / 'FINAL' / self.arm,
                    self.barrier, 'FINAL', self.phase)
        except Exception as error:
            snapshot_error = str(error)
            self.errors.append('FINAL capture failed: ' + snapshot_error)
            self.capture_errors.append(dict(label='FINAL', phase=self.phase, error=snapshot_error))
        final = dict(arm=self.arm, phase=self.phase, cwd=str(self.workspace),
                     sessions=str(self.home / 'sessions'), thread_id=self.thread,
                     epoch_utc=self.clock['epoch_utc'], kill_utc=utc(
                         datetime.fromisoformat(self.clock['epoch_utc']).timestamp() + self.kill_monotonic - self.clock['t0']),
                     stopped_utc=utc(), cap_seconds=self.clock['duration'],
                     t0=self.clock['t0'], deadline=self.kill_monotonic, scheduled_deadline=self.clock['deadline'], history=self.history,
                     agent_wall_seconds=sum(max(0, min(row['completed_monotonic'], self.clock['deadline']) -
                                                max(row['started_monotonic'], self.clock['t0'])) for row in self.history),
                     errors=self.errors, capture_errors=self.capture_errors, snapshot_error=snapshot_error,
                     cpu=dict(self.cpu.budget.report(),
                              orphan_kills=getattr(self.cpu, 'orphan_kills', []),
                              orphan_cleanup_errors=getattr(self.cpu, 'orphan_cleanup_errors', [])))
        dump(self.output / 'PHASE.json', final)
        self.completed = True
        return final

def run_phase(root, config, phase, selected, dry=False):
    duration = 600 if dry else PHASE_SECONDS[phase]
    setup_started = time.monotonic()
    epoch = time.time() + 30
    t0 = time.monotonic() + (epoch - time.time())
    clock = dict(epoch_utc=utc(epoch), kill_utc=utc(epoch + duration),
                 t0=t0, deadline=t0 + duration, duration=duration)
    dump(root / ('CLOCK-' + phase + '.json'), clock)
    arms = [Arm(root, arm, phase, config, clock) for arm in selected]
    ending = threading.Event()
    def monitor():
        while not ending.is_set():
            try:
                rows = observe()
            except Exception as error:
                for arm in arms:
                    arm.errors.append('Process observation failed: ' + str(error))
                    flag_infrastructure(root, phase, arm, error, 'process-observation')
                    arm.stop()
                return
            for arm in arms:
                try:
                    arm.tick(rows)
                except Exception as error:
                    arm.errors.append('CPU supervisor failure: ' + str(error))
                    flag_infrastructure(root, phase, arm, error, 'cpu-supervisor')
                    arm.stop()
            ending.wait(.2)
    watcher = threading.Thread(target=monitor, daemon=True)
    watcher.start()
    try:
        setup_seconds = time.monotonic() - setup_started
        lead = max(30.0, setup_seconds + 15.0)
        epoch = time.time() + lead
        t0 = time.monotonic() + lead
        clock.update(epoch_utc=utc(epoch), kill_utc=utc(epoch + duration),
                     t0=t0, deadline=t0 + duration, setup_seconds=setup_seconds,
                     epoch_lead_seconds=lead)
        for arm in arms:
            arm.cpu.args.t0 = t0
            arm.cpu.args.deadline = t0 + duration
            arm.cpu.budget.t0 = t0
        for arm in arms:
            arm.launch()
        if time.monotonic() >= t0:
            raise RuntimeError('Prelaunch missed shared start; wave must be voided, never extended')
        next_snapshot = t0 + config['snapshot_interval_seconds']
        while time.monotonic() < clock['deadline'] and not (root / 'STOP').exists():
            if time.monotonic() >= t0:
                for arm in arms:
                    try:
                        arm.poll()
                    except Exception as error:
                        arm.errors.append(str(error)); arm.stop()
                        if isinstance(error, InfraLaunchError):
                            flag_infrastructure(root, phase, arm, error, 'zero-events-early-exit')
                if time.monotonic() >= next_snapshot:
                    elapsed = int(round((next_snapshot - t0) / 60))
                    label = 'T+' + str(elapsed).zfill(3) + 'm'
                    for arm in arms:
                        capture_arm(arm, root / 'snapshots' / phase / label / arm.arm, label, phase)
                    next_snapshot += config['snapshot_interval_seconds']
            time.sleep(.1)
        if (root / 'STOP').exists():
            clock['kill_utc'] = utc()
            for arm in arms:
                arm.errors.append('External STOP: incomplete phase')
        for arm in arms:
            arm.finish()
        return arms
    except BaseException as error:
        (root / 'STOP').touch()
        for arm in arms:
            arm.errors.append('Phase driver failure: ' + str(error))
            try:
                if not arm.completed:
                    arm.finish()
            except Exception:
                arm.stop()
        return arms
    finally:
        ending.set(); watcher.join(timeout=3)

def score_arms(root, arms, phases, dry=False):
    results = []
    failures = []
    for arm in arms:
        for phase in phases:
            result = score(root, arm, phase)
            results.append(result)
            if dry and result.get('scoring_error'):
                failures.append(arm + '/' + phase + ': ' + result['scoring_error'])
    if failures:
        raise RuntimeError('Dry cell scoring failed: ' + '; '.join(failures))
    return results

def score_reference_snapshots(root, references, allowed_roots=None):
    root = Path(root).resolve()
    if allowed_roots is None:
        allowed_roots = [Path('<scratch-dir>') / 'arch-r2/arch-harness/snapshots']
    metadata, scores = [], []
    for index, source in enumerate(references, 1):
        source = Path(source).expanduser()
        arm = next((part for part in source.parts if part in
                    ('arch-e1','arch-e2','arch-e3','arch-e4','arch-e5','arch-e6',
                     'arch-g1','arch-g2','arch-g3','arch-g4','arch-g5','arch-g6')), None)
        if arm is None:
            raise ValueError('Reference snapshot path must identify its source arm')
        label = 'ref-%02d-%s' % (index, arm)
        destination = root / 'out' / 'reference-snapshots' / label
        destination.parent.mkdir(parents=True, exist_ok=True)
        copied = copy_reference_snapshot(source, destination, allowed_roots)
        result_path = root / 'out' / 'reference-scores' / (label + '.json')
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result = score_snapshot(root, arm, 'build', destination, result_path)
        if result.get('scoring_error'):
            raise RuntimeError('Reference scoring failed: ' + result['scoring_error'])
        wall = result.get('scoring_wall_seconds', 0)
        count = result.get('scoring_case_count', 0)
        if not isinstance(wall, (int, float)) or wall <= 0 or not isinstance(count, int) or count <= 0:
            raise RuntimeError('Reference scoring produced no scored cases')
        metadata.append(dict(source_path=copied['source_path'], sha256=copied['sha256'],
                             arm_kind=treatment(arm)))
        scores.append(dict(scoring_wall_seconds=wall, scored_case_count=count))
    receipt = dict(reference_snapshots=metadata, scored_reference=bool(metadata),
                   scoring_wall_seconds=sum(item['scoring_wall_seconds'] for item in scores),
                   scored_case_count=sum(item['scored_case_count'] for item in scores))
    dump(root / 'out' / 'ARCH-REFERENCE-SCORING.json', receipt)
    return receipt

def production_schedule(host, dry=False):
    if dry:
        if host != 'studio': raise ValueError('Dry cell runs only on Studio')
        return [('A', ('arch-e1', 'arch-g1'))]
    if host == 'studio':
        return list(STUDIO_WAVES.items())
    if host == 'macbook':
        return [('optional', MACBOOK_ARMS)]
    raise ValueError('Unknown ARCH host: ' + host)

def main():
    from arch_gates import verify
    from arch_finalize import finalize
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--evidence', type=Path, required=True)
    p.add_argument('--dry', action='store_true', help='Separate disposable harness: E1/G1, ten-minute build only')
    p.add_argument('--reference-snapshot', type=Path, action='append', default=[],
                   help='Read-only reference FINAL snapshot for dry scoring when dry arms have no candidate')
    args = p.parse_args()
    if args.reference_snapshot and not args.dry:
        p.error('--reference-snapshot is available only with --dry')
    root = args.root.resolve(); config = load(root)
    check_hold(root)
    if (root / 'ARCH-START.json').exists():
        raise ValueError('One prescribed schedule per prepared harness; never overwrite or reset a launch')
    verify(root, args.evidence, dry=args.dry)
    schedule = production_schedule(config['host'], args.dry)
    selected = tuple(arm for _, arms in schedule for arm in arms)
    for arm in selected:
        dump(root / 'out' / arm / 'baseline.json', dict(spec_hash=tree_hash(root / arm / 'spec')))
    dump(root / 'ARCH-START.json', dict(host=config['host'], mode='dry' if args.dry else 'production',
                                      model=MODEL, effort=EFFORT, arms=selected,
                                      deciding=config['host'] == 'studio' and not args.dry,
                                      wave_schedule=[dict(wave=wave, arms=arms) for wave, arms in schedule],
                                      started_utc=utc()))
    for wave, arms in schedule:
        phases = ('build',) if args.dry else ('build', 'maintenance')
        for phase in phases:
            run_phase(root, config, phase, arms, args.dry)
            if (root / 'STOP').exists(): break
        # Reserve scoring between waves; Wave B cannot overlap Wave A scoring.
        own_scores = score_arms(root, arms, phases, dry=args.dry)
        if args.dry and any(item.get('candidate_missing') for item in own_scores):
            if not args.reference_snapshot:
                raise RuntimeError('Dry cell has no candidate; pass --reference-snapshot')
            score_reference_snapshots(root, args.reference_snapshot)
        if (root / 'STOP').exists():
            break
    dump(root / 'AGENT-PHASES-DONE.json', dict(completed_utc=utc(), scoring_pending=False))
    dump(root / 'SCORING-DONE.json', dict(completed_utc=utc()))
    finalize(root)
    print(str(root / 'out/ARCH-SUMMARY.json'))

if __name__ == '__main__':
    main()
