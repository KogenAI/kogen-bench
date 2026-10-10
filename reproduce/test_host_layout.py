"""Integration coverage for installing and running a lane kit on host layout."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
INSTALLER = HERE / 'install-lane-kit.sh'
GENERATOR = HERE / 'generate-host-plan.py'
GIT_ENV = os.environ.copy()
GIT_ENV.update({
    'GIT_CONFIG_GLOBAL': '/dev/null',
    'GIT_CONFIG_NOSYSTEM': '1',
    'GIT_AUTHOR_NAME': 'Synthetic fixture',
    'GIT_AUTHOR_EMAIL': 'fixture@' + 'example.invalid',
    'GIT_COMMITTER_NAME': 'Synthetic fixture',
    'GIT_COMMITTER_EMAIL': 'fixture@' + 'example.invalid',
})


class HostLayoutIntegrationTests(unittest.TestCase):
    def git(self, *args):
        return subprocess.check_output(['git', *map(str, args)], env=GIT_ENV, text=True).strip()

    def test_install_plan_and_patch_use_carried_host_task_tree(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'bench'
            kits = root / 'kits'
            prior = kits / 'prior-release'
            tasks = prior / 'tasks'
            task_id = 'c4-1-ts-bun'
            task_dir = tasks / task_id
            bases = tasks / '_bases'
            task_dir.mkdir(parents=True)
            bases.mkdir()
            (prior / '.complete').write_text('1' * 40 + '\n')
            old_task = tasks / 'legacy-task'
            old_task.mkdir()
            (old_task / 'kept.txt').write_text('carried forward\n')

            source = Path(temporary) / 'upstream'
            source.mkdir()
            self.git('init', '-q', str(source))
            self.git('-C', str(source), 'config', 'user.name', 'Synthetic fixture')
            self.git('-C', str(source), 'config', 'user.email', 'fixture@' + 'example.invalid')
            (source / 'tracked.txt').write_text('base\n')
            self.git('-C', str(source), 'add', 'tracked.txt')
            self.git('-C', str(source), 'commit', '-qm', 'synthetic base')
            base_sha = self.git('-C', str(source), 'rev-parse', 'HEAD')
            bundle_rel = f'_bases/{task_id}-{base_sha[:12]}.bundle'
            bundle = tasks / bundle_rel
            self.git('-C', str(source), 'bundle', 'create', str(bundle), '--all')
            task_dir.joinpath('prompt.md').write_text('Synthetic public prompt.\n')
            task_dir.joinpath('task.json').write_text(json.dumps({
                'id': task_id,
                'base_bundle': bundle_rel,
                'base_bundle_sha256': hashlib.sha256(bundle.read_bytes()).hexdigest(),
                'base_sha': base_sha,
                'base_repo': 'Core4 task fixture (checkout bundled)',
            }))
            kits.mkdir(exist_ok=True)
            (kits / 'current').symlink_to('prior-release', target_is_directory=True)

            revision = 'a' * 40
            installed = subprocess.run(
                ['bash', str(INSTALLER), '--root', str(root), '--release-id', revision],
                env=GIT_ENV, text=True, capture_output=True,
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            kit = kits / 'current'
            self.assertEqual((kit / 'tasks' / 'legacy-task' / 'kept.txt').read_text(), 'carried forward\n')
            self.assertTrue((kit / 'tasks').is_symlink())
            self.assertEqual(self.git('-C', str(kit), 'rev-parse', 'HEAD'), revision)

            reinstalled = subprocess.run(
                ['bash', str(INSTALLER), '--root', str(root), '--release-id', revision],
                env=GIT_ENV, text=True, capture_output=True,
            )
            self.assertEqual(reinstalled.returncode, 0, reinstalled.stderr)
            self.assertEqual(os.path.realpath(kit), os.path.realpath(kits / revision))

            codex = Path(temporary) / 'codex'
            codex.write_text('#!/bin/sh\nprintf "codex-cli 0.160.0\\n"\n')
            codex.chmod(0o755)
            ledger = Path(temporary) / 'ledger.md'
            ledger.write_text('synthetic public input ledger\n')
            plan_path = Path(temporary) / 'plan.json'
            generator_args = [
                sys.executable, str(kit / 'reproduce' / 'generate-host-plan.py'),
                '--kit', str(kit), '--task', task_id, '--cell', 'dry-rc-us-1',
                '--round-id', 'dry-rc-us', '--audit-round', 'dry-rc-us',
                '--arm', 'Codex-Luna-high', '--model', 'gpt-6-luna',
                '--effective-model', 'gpt-6-luna', '--effort', 'high',
                '--itt-class', 'counted', '--itt-cohort', 'smoke-control',
                '--itt-evidence-ref', 'rounds/dry-rc-us/ITT.md',
                '--ledger-file', str(ledger), '--source-ref', 'rounds/dry-rc-us/README.md',
                '--queue-position', 'held', '--venue', 'us', '--account-class', 'owner',
                '--codex', str(codex), '--output', str(plan_path),
            ]
            generated = subprocess.run(generator_args, env=GIT_ENV, text=True, capture_output=True)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            rendered_plan = plan_path.read_text()
            self.assertNotIn(str(ledger), rendered_plan)
            self.assertNotIn('@', rendered_plan)
            plan = json.loads(rendered_plan)['cells'][0]
            self.assertEqual(plan['kogen_sha'], revision)
            self.assertEqual(plan['itt'], {
                'class': 'counted', 'cohort': 'smoke-control',
                'evidence_ref': 'rounds/dry-rc-us/ITT.md',
            })
            self.assertEqual(plan['base_repo'], 'Core4 task fixture (checkout bundled)')
            for option, value in (('--itt-class', 'dry-cell'), ('--itt-cohort', 'host-layout')):
                invalid_args = generator_args.copy()
                invalid_args[invalid_args.index(option) + 1] = value
                invalid_plan = Path(temporary) / f'invalid-{option[2:]}.json'
                invalid_args[invalid_args.index('--output') + 1] = str(invalid_plan)
                invalid = subprocess.run(invalid_args, env=GIT_ENV, text=True, capture_output=True)
                self.assertNotEqual(invalid.returncode, 0)
                self.assertFalse(invalid_plan.exists())
            resolved = subprocess.run([
                sys.executable, str(kit / 'reproduce' / 'lane-plan.py'),
                '--plan', str(plan_path), '--cell', 'dry-rc-us-1', '--task', task_id,
                '--model', 'gpt-6-luna', '--effort', 'high',
            ], env=GIT_ENV, text=True, capture_output=True)
            self.assertEqual(resolved.returncode, 0, resolved.stderr)
            normalized = json.loads(resolved.stdout)
            self.assertEqual(normalized['queue_position'], 'held')
            self.assertEqual(normalized['venue'], 'us')
            self.assertEqual(normalized['account_class'], 'owner')

            work = Path(temporary) / 'work' / 'repo'
            work.parent.mkdir()
            self.git('clone', '-q', str(bundle), str(work))
            self.git('-C', str(work), 'checkout', '-q', base_sha)
            (work / 'tracked.txt').write_text('changed by synthetic agent\n')
            result = Path(temporary) / 'patch.diff'
            bundle.chmod(0o600)
            patch_runtime = Path(temporary) / 'patch-runtime'
            patch_runtime.mkdir()
            wrapper_text = (kit / 'reproduce' / 'lane-patch.sh').read_text()
            wrapper_text = wrapper_text.replace(
                'if (( EUID == 0 )); then',
                'if [[ ${LANE_PATCH_TEST_ROOT:-0} == 1 ]] || (( EUID == 0 )); then', 1,
            )
            wrapper_text = wrapper_text.replace(
                'bench_uid=$(id -u bench); bench_gid=$(id -g bench)',
                'bench_uid=$(id -u); bench_gid=$(id -g)', 1,
            )
            wrapper_text = wrapper_text.replace(
                '/usr/sbin/runuser -u bench --', '"$RUNUSER_BIN" -u bench --', 1,
            )
            (patch_runtime / 'lane-patch.sh').write_text(wrapper_text)
            (patch_runtime / 'lane-patch.sh').chmod(0o755)
            profile_text = (kit / 'reproduce' / 'sandbox-profile.sh').read_text()
            profile_text = profile_text.replace('exec /usr/bin/bwrap', 'exec "$BWRAP_BIN"', 1)
            (patch_runtime / 'sandbox-profile.sh').write_text(profile_text)
            (patch_runtime / 'sandbox-profile.sh').chmod(0o755)
            bindir = Path(temporary) / 'bin'
            bindir.mkdir()
            timeout = bindir / 'timeout'
            timeout.write_text('#!/bin/sh\n[ "$1" = --signal=KILL ] && shift\nshift\nexec "$@"\n')
            timeout.chmod(0o755)
            fake_bwrap = Path(temporary) / 'fake-bwrap'
            fake_bwrap.write_text('''#!/usr/bin/env python3
import os, subprocess, sys
args=sys.argv[1:]
mounts={}
i=0
while i < len(args):
    if args[i] in ('--bind','--ro-bind'):
        mounts[args[i+2]]=args[i+1]; i+=3
    elif args[i]=='--chdir':
        cwd=args[i+1]; i+=2; command=args[i:]; break
    elif args[i] in ('--proc','--dev','--tmpfs','--dir'):
        i+=2
    elif args[i]=='--symlink':
        i+=3
    else:
        i+=1
assert os.path.realpath(mounts['/input']) == os.environ['EXPECTED_INPUT']
staged_bundle=os.path.realpath(mounts['/base.bundle'])
assert staged_bundle != os.environ['EXPECTED_BUNDLE']
assert os.path.dirname(staged_bundle) == os.path.realpath(mounts['/scratch'])
assert os.path.basename(staged_bundle) == 'base.bundle'
assert os.stat(staged_bundle).st_mode & 0o777 == 0o444
with open(staged_bundle,'rb') as staged, open(os.environ['EXPECTED_BUNDLE'],'rb') as source:
    assert staged.read() == source.read()
assert os.path.basename(os.path.realpath(mounts['/scratch'])).startswith('lane-patch.')
assert os.path.isdir(mounts['/scratch'])
assert cwd == '/scratch'
assert command[:3] == ['/bin/bash','/lane-patch.sh','--inside']
translated=[mounts.get(value,value) for value in command]
raise SystemExit(subprocess.call(translated,cwd=mounts.get(cwd,cwd)))
''')
            fake_bwrap.chmod(0o755)
            fake_runuser = Path(temporary) / 'fake-runuser'
            fake_runuser.write_text('''#!/usr/bin/env python3
import subprocess,sys
args=sys.argv[1:]
if args[:3] != ['-u','bench','--']:
    raise SystemExit('unexpected runuser arguments')
raise SystemExit(subprocess.call(args[3:]))
''')
            fake_runuser.chmod(0o755)
            env = GIT_ENV.copy()
            env['PATH'] = str(bindir) + os.pathsep + env.get('PATH', '')
            env['BWRAP_BIN'] = str(fake_bwrap)
            env['RUNUSER_BIN'] = str(fake_runuser)
            env['LANE_PATCH_TEST_ROOT'] = '1'
            env['EXPECTED_INPUT'] = str(work.resolve())
            env['EXPECTED_BUNDLE'] = str(bundle.resolve())
            env['TMPDIR'] = temporary
            extracted = subprocess.run([
                str(patch_runtime / 'lane-patch.sh'), base_sha,
                str(kit / 'tasks' / bundle_rel), str(work), str(result),
            ], env=env, text=True, capture_output=True)
            self.assertEqual(extracted.returncode, 0, extracted.stderr)
            patch = result.read_text()
            self.assertIn('tracked.txt', patch)
            verify = Path(temporary) / 'verify'
            self.git('clone', '-q', str(bundle), str(verify))
            self.git('-C', str(verify), 'checkout', '-q', base_sha)
            self.git('-C', str(verify), 'apply', '--index', str(result))
            self.assertEqual((verify / 'tracked.txt').read_text(), 'changed by synthetic agent\n')


if __name__ == '__main__':
    unittest.main()
