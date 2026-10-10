#!/usr/bin/env python3
"""Generate a frozen one-cell host dry plan from the installed task kit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

EMAIL = re.compile(r'(?i)\b[a-z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-z0-9.-]+\.[a-z]{2,}\b')
HOME_PATH = re.compile(r'(?i)(?<![a-z0-9])(?:~(?:[/\\][^\s,;)]*)?|/(?:Users|home)/[^\s,;)]*|/root(?:[/\\][^\s,;)]*)?|[a-z]:[/\\]Users[/\\][^\s,;)]*)')
SHA40 = re.compile(r'[0-9a-f]{40}\Z')
SHA64 = re.compile(r'[0-9a-f]{64}\Z')
ITT_CLASSES = ('counted', 'excluded-env-fault')
ITT_COHORTS = ('scored', 'smoke-control', 'unresolved')


def read_regular(path: Path, limit: int = 4 * 1024 * 1024) -> bytes:
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError(f'{path.name} is not a bounded regular file')
        parts, total = [], 0
        while True:
            chunk = os.read(fd, min(1024 * 1024, limit - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > limit:
                raise ValueError(f'{path.name} exceeds the size limit')
            parts.append(chunk)
        return b''.join(parts)
    finally:
        os.close(fd)


def public_ref(value: str) -> str:
    value = public_label(value)
    if not value:
        raise ValueError('reference must be public, relative and email-free')
    ssh = re.fullmatch(r'(?:ssh://)?git@([^:/]+)[:/]([^\s]+)', value)
    if ssh:
        value = ssh.group(1).lower() + '/' + ssh.group(2)
    elif '://' in value:
        parsed = urlsplit(value)
        if not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('reference URL must not contain credentials')
        value = parsed.hostname.lower() + '/' + unquote(parsed.path).lstrip('/')
    if value.startswith(('/', '~')) or re.match(r'^[a-z]:[/\\]', value, re.I) or '\\' in value:
        raise ValueError('reference must not be a local path')
    if any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('reference must not contain traversal components')
    return value


def public_label(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    value = ' '.join(value.strip().split())
    if EMAIL.search(value) or HOME_PATH.search(value):
        return None
    if value.startswith(('/', '~', '\\')) or re.match(r'^[a-z]:[/\\]', value, re.I):
        return None
    if any(ord(ch) < 32 for ch in value):
        return None
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(read_regular(path, 128 * 1024 * 1024)).hexdigest()


def kit_revision(kit: Path) -> str:
    raw = read_regular(kit / '.complete', 128).decode('ascii').strip()
    if not SHA40.fullmatch(raw):
        raise ValueError('kit .complete marker is not a full revision')
    return raw


def task_metadata(kit: Path, task_id: str) -> tuple[dict, Path]:
    tasks = (kit / 'tasks').resolve(strict=True)
    metadata_path = kit / 'tasks' / task_id / 'task.json'
    metadata = json.loads(read_regular(metadata_path).decode('utf-8'))
    if metadata.get('id', task_id) != task_id:
        raise ValueError('task metadata id does not match the requested task')
    bundle_rel = metadata.get('base_bundle')
    if (not isinstance(bundle_rel, str) or not bundle_rel.startswith('_bases/')
            or any(part in ('', '.', '..') for part in bundle_rel.split('/'))
            or '\\' in bundle_rel):
        raise ValueError('task metadata has no bundled base under _bases/')
    bundle_path = kit / 'tasks' / bundle_rel
    if bundle_path.is_symlink():
        raise ValueError('task base bundle must be a regular file, not a symlink')
    resolved_bundle = bundle_path.resolve(strict=True)
    try:
        resolved_bundle.relative_to(tasks)
    except ValueError as error:
        raise ValueError('task base bundle escapes the installed task tree') from error
    bundle_sha = metadata.get('base_bundle_sha256')
    if not isinstance(bundle_sha, str) or not SHA64.fullmatch(bundle_sha):
        raise ValueError('task metadata has no valid base bundle SHA-256')
    if digest(resolved_bundle) != bundle_sha:
        raise ValueError('task base bundle SHA-256 does not match task metadata')
    base_sha = metadata.get('base_sha')
    if not isinstance(base_sha, str) or not SHA40.fullmatch(base_sha):
        raise ValueError('task metadata has no valid base commit')
    base_repo = public_label(metadata.get('base_repo'))
    if not base_repo:
        raise ValueError('task metadata has no public base_repo label')
    return metadata, resolved_bundle


def command_version(command: str) -> str:
    result = subprocess.run([command, '--version'], capture_output=True, text=True,
                            timeout=8, check=True, env={'PATH': '/usr/bin:/bin', 'HOME': '/nonexistent'})
    value = result.stdout.strip() or result.stderr.strip()
    value = value.splitlines()[0][:200] if value else ''
    if not value or not public_label(value):
        raise ValueError('Codex --version did not return a safe pinned version')
    return value


def harness_fingerprint(kit: Path) -> str:
    paths = ('reproduce/run-lane.sh', 'reproduce/lane-plan.py', 'reproduce/sandbox-profile.sh',
             'reproduce/lane-patch.sh', 'reproduce/control-worker.py', 'reproduce/host-pins.lock')
    digest_state = hashlib.sha256()
    for relative in paths:
        digest_state.update(relative.encode('utf-8') + b'\0')
        digest_state.update(bytes.fromhex(digest(kit / relative)))
    return digest_state.hexdigest()


def make_plan(args: argparse.Namespace) -> dict:
    kit = Path(args.kit)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', args.task):
        raise ValueError('task id must be a simple public identifier')
    revision = kit_revision(kit)
    task, _bundle = task_metadata(kit, args.task)
    if args.venue not in ('eu', 'us'):
        raise ValueError('venue must be eu or us')
    if args.account_class not in ('billing', 'owner'):
        raise ValueError('account class must be billing or owner')
    if args.itt_class not in ITT_CLASSES:
        raise ValueError('ITT class is not in the Standard 1.2 enum')
    if args.itt_cohort not in ITT_COHORTS:
        raise ValueError('ITT cohort is not in the Standard 1.2 enum')
    if args.effort not in ('low', 'medium', 'high', 'xhigh', 'max'):
        raise ValueError('effort is not supported by the lane runner')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', args.model):
        raise ValueError('model must be a simple model identifier')
    effective_model = public_label(args.effective_model)
    if not effective_model:
        raise ValueError('effective model must be supplied as a public model identifier')
    queue = public_label(args.queue_position)
    if not queue:
        raise ValueError('queue position must be a public identifier')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', args.round_id):
        raise ValueError('round id must be a short public identifier')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', args.audit_round):
        raise ValueError('audit round must be a short public identifier')
    if args.repetition < 1:
        raise ValueError('repetition must be positive')
    if args.deps_source not in ('task-derived', 'shared'):
        raise ValueError('dependency source must be task-derived or shared')
    launcher_sha = digest(kit / 'reproduce/run-lane.sh')
    bundle_path = kit / 'tasks' / task['base_bundle']
    ledger_sha = digest(Path(args.ledger_file))
    cell = {
        'round_id': args.round_id,
        'audit_round': args.audit_round,
        'cell_id': args.cell,
        'task': args.task,
        'model': args.model,
        'effective_model': effective_model,
        'effort': args.effort,
        'effective_effort': args.effort,
        'arm': public_label(args.arm),
        'harness': 'codex',
        'harness_version': command_version(args.codex),
        'recipe': public_label(args.recipe),
        'itt': {
            'class': public_label(args.itt_class),
            'cohort': public_label(args.itt_cohort),
            'evidence_ref': public_ref(args.itt_evidence_ref),
        },
        'repetition': args.repetition,
        'base_repo': public_label(task.get('base_repo')),
        'base_revision': {'kind': 'git-commit', 'hash': task['base_sha']},
        'base_bundle_sha256': digest(bundle_path),
        'launcher_sha256': launcher_sha,
        'adapter_harness_sha': harness_fingerprint(kit),
        'deps_source': args.deps_source,
        'ledger_sha256': ledger_sha,
        'source_ref': public_ref(args.source_ref),
        'venue': args.venue,
        'account_class': args.account_class,
        'queue_position': queue,
        'kogen_sha': revision,
    }
    for key in ('cell_id', 'arm', 'recipe', 'itt_class', 'itt_cohort'):
        value = cell['itt']['class' if key == 'itt_class' else 'cohort'] if key in ('itt_class', 'itt_cohort') else cell[key]
        if not value:
            raise ValueError(f'{key.replace("_", " ")} must be a public identifier')
    return {'cells': [cell], 'source_ref': cell['source_ref'], 'launcher_sha256': launcher_sha}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kit', default='/srv/bh/bench/kits/current')
    p.add_argument('--task', required=True)
    p.add_argument('--cell', required=True)
    p.add_argument('--round-id', required=True)
    p.add_argument('--audit-round', required=True)
    p.add_argument('--arm', required=True)
    p.add_argument('--model', required=True)
    p.add_argument('--effective-model', required=True)
    p.add_argument('--effort', required=True)
    p.add_argument('--recipe', default='standard-1.2-host-dry-v1')
    p.add_argument('--itt-class', choices=ITT_CLASSES, required=True)
    p.add_argument('--itt-cohort', choices=ITT_COHORTS, required=True)
    p.add_argument('--itt-evidence-ref', required=True)
    p.add_argument('--ledger-file', required=True)
    p.add_argument('--source-ref', default='reproduce/RERUN.md')
    p.add_argument('--deps-source', choices=('task-derived', 'shared'), default='task-derived')
    p.add_argument('--repetition', type=int, default=1)
    p.add_argument('--queue-position', required=True)
    p.add_argument('--venue', choices=('eu', 'us'), required=True)
    p.add_argument('--account-class', choices=('billing', 'owner'), required=True)
    p.add_argument('--codex', default='/opt/bench/tools/bin/codex')
    p.add_argument('--output', help='write a new plan file; omit to print JSON on stdout')
    return p


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        plan = make_plan(args)
        rendered = json.dumps(plan, sort_keys=True, indent=2) + '\n'
        if args.output:
            fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, 'O_NOFOLLOW', 0), 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8') as target:
                target.write(rendered)
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError,
            subprocess.SubprocessError) as error:
        print(f'cannot generate dry-cell plan: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
