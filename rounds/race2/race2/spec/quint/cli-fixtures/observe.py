#!/usr/bin/env python3
"""Read-only black-box observations, invoked by IO schema 1 GitCommand.

Never calls Rust APIs, produces receipts, stages the real index, or fixes outputs.
Raw snapshots live in the runner's control directory, outside the project.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})


def snapshot(repo):
    repo = Path(repo)
    files = {}
    for root, dirs, names in os.walk(repo):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for name in sorted(names):
            p = Path(root) / name
            files[str(p.relative_to(repo))] = ['symlink', os.readlink(p)] if p.is_symlink() else ['file', p.read_bytes().hex(), p.stat().st_mode & 0o777]
    index = repo / '.git/index'
    return {'files': files, 'index': index.read_bytes().hex() if index.exists() else None,
            'refs': git(repo, 'for-each-ref', '--format=%(refname) %(objectname)').decode(),
            'head': (repo / '.git/HEAD').read_bytes().hex()}


def main(argv):
    op, *args = argv
    if op == 'pulse':
        assert not args
    elif op == 'duration':
        seconds = max(0, int(args[0])) // 1000
        print(str(seconds) + 's' if seconds < 60 else str(seconds // 60) + 'm' if seconds < 3600 else str(seconds // 3600) + 'h' + str((seconds % 3600) // 60).zfill(2) + 'm')
    elif op == 'delta':
        later, earlier = map(int, args)
        print(json.dumps({'delta_ms': later - earlier}))
    elif op == 'wait-pid':
        pid = int(args[0])
        deadline = time.monotonic() + 25
        while True:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            assert time.monotonic() < deadline, 'detached trace-owned daemon did not exit'
            time.sleep(.01)
    elif op == 'log':
        sys.stdout.buffer.write(Path(args[0]).read_bytes())
    elif op == 'snapshot':
        repo, dest = args
        Path(dest).write_text(json.dumps(snapshot(repo), sort_keys=True))
    elif op == 'unchanged':
        repo, dest = args
        assert snapshot(repo) == json.loads(Path(dest).read_text()), 'command mutated worktree, index, or refs'
    elif op == 'unchanged-except-ref':
        repo, dest, ref = args
        before = json.loads(Path(dest).read_text())
        after = snapshot(repo)
        for state in (before, after):
            state['refs'] = '\n'.join(line for line in state['refs'].splitlines() if not line.startswith(ref + ' '))
        assert before == after, 'publication failure partially changed worktree, index, HEAD, or unrelated refs'
    elif op == 'approval':
        repo, slug, caller, payload = args
        ref = 'refs/kogen/intents/' + slug
        doc = json.loads(git(repo, 'show', ref + ':.kogen/intents/' + slug + '/approval.json'))
        intent = Path(repo, '.kogen/intents', slug, 'intent.md').read_bytes()
        assert intent == Path(payload).read_bytes(), 'approved payload differs from fixture'
        assert doc['schema'] == 1 and doc['slug'] == slug and doc['by'] == caller
        assert doc['target_branch'] == 'main'
        assert doc['intent_sha256'] == hashlib.sha256(intent).hexdigest()
        binding = b'kogen:criteria-only-approval\0' + len(intent).to_bytes(8, 'big') + intent
        assert doc['approval_sha256'] == hashlib.sha256(binding).hexdigest()
        assert doc['protected_manifest']['.kogen/intents/' + slug + '/intent.md'] == hashlib.sha256(intent).hexdigest()
        assert doc['acceptance_paths'] == [], 'criteria-only approval must bind absence'
        assert git(repo, 'show', ref + ':.kogen/intents/' + slug + '/intent.md') == intent
        # Identity is checked by bytes in the owner's document, not a captured OID.
    elif op == 'credential':
        home, label = args
        doc = json.loads(Path(home, '.kogen/credentials/chatgpt-' + label + '.json').read_text())
        assert doc['subject'] == 'cli-' + label
        assert doc['expires_at'] == 4102444800
        assert doc['access_token'] == 'cli-' + label + '-access'
        assert doc['refresh_token'] == 'cli-' + label + '-refresh'
        assert 'chatgpt.tokens.use.direct' in doc['scopes']
    elif op == 'accounts':
        home, repo, default, project = args
        # Machine-local schema adapter; fixed owner format, never an oracle
        # derived from provider use's output or a digest of arbitrary new bytes.
        text = Path(home, '.kogen/accounts.yaml').read_text()
        expected = 'chatgpt:\n'
        if default != '-':
            expected += '  default: ' + default + '\n'
        if project != '-':
            expected += '  projects:\n    - path: ' + json.dumps(repo) + '\n      account: ' + project + '\n'
        expected += 'selection:\n'
        if default != '-':
            expected += '  default: chatgpt\n'
        if project != '-':
            expected += '  projects:\n    - path: ' + json.dumps(repo) + '\n      provider: chatgpt\n'
        assert text == expected, (text, expected)
        assert not Path(repo, '.kogen/accounts.yaml').exists()
        assert not Path(repo, '.kogen/credentials').exists()
        assert not any('access_token' in git(repo, 'show', f'HEAD:{p.decode()}').decode(errors='replace')
                       for p in git(repo, 'ls-tree', '-r', '--name-only', 'HEAD').splitlines())
    elif op == 'history':
        repo, base, *pairs = args
        assert len(pairs) % 2 == 0
        commits = git(repo, 'rev-list', '--reverse', base + '..HEAD').decode().splitlines()
        assert len(commits) == len(pairs) // 2, 'each landed Build must produce exactly one commit'
        for oid, slug, run in zip(commits, pairs[::2], pairs[1::2]):
            assert git(repo, 'diff-tree', '--no-commit-id', '--name-only', '-r', oid).decode().splitlines() == [slug + '.txt']
            assert git(repo, 'show', oid + ':' + slug + '.txt') == b'Hello.\n'
            assert ('Kogen-Intent: ' + slug) in git(repo, 'show', '-s', '--format=%B', oid).decode()
            tree = git(repo, 'show', '-s', '--format=%T', oid).decode().strip()
            main(['verification', repo, run, 'green', tree])
    elif op == 'verification':
        repo, build_id, result, tree = args
        events = Path(repo, '.kogen/local/runs', build_id, 'events.jsonl')
        records = [json.loads(line) for line in events.read_text().splitlines()]
        checks = [r for r in records if r.get('event') == 'verification']
        assert checks, 'printing success cannot replace durable verification evidence'
        last = checks[-1]
        assert last['result'] == result
        assert last['tree'] == tree, 'receipt must describe the published candidate tree'
        if result == 'green':
            assert last['checks'] and all(c['status'] == 'passed' for c in last['checks'])
    else:
        raise ValueError(op)


if __name__ == '__main__':
    main(sys.argv[1:])
