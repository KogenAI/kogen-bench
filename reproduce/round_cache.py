#!/usr/bin/env python3
"""Off-repo cache of per-round checks, keyed by the round's git tree sha.

A round passes once per (validator code, round id, tree sha). Rounds with any
uncommitted, untracked or ignored file are never cached, so the cache only ever
vouches for committed content. KOGEN_VALIDATE_CACHE=off, a missing git tree or
an unwritable cache directory all mean a full check.
"""
import hashlib, json, os, subprocess
from pathlib import Path


class RoundCache:
    def __init__(self, root):
        self.root = Path(root)
        self.dir = self._cache_dir()
        self.trees = self._clean_round_trees() if self.dir else {}
        self.key_prefix = self._validator_hash() if self.trees else ''
        self.cached = self.checked = 0

    def _cache_dir(self):
        setting = os.environ.get('KOGEN_VALIDATE_CACHE')
        if setting == 'off':
            return None
        try:
            base = Path(setting) if setting else Path(os.environ.get('XDG_CACHE_HOME') or Path.home() / '.cache') / 'kogen-bench-validate'
            base.mkdir(parents=True, exist_ok=True)
            probe = base / f'.probe-{os.getpid()}'
            probe.write_text('')
            probe.unlink()
            return base
        except (OSError, RuntimeError):
            return None

    def _git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, capture_output=True, check=True).stdout.decode('utf-8', 'surrogateescape')

    def _clean_round_trees(self):
        try:
            if self._git('rev-parse', '--show-prefix').strip():
                return {}
            trees = {}
            for entry in self._git('ls-tree', '-z', 'HEAD', 'rounds/').split('\0'):
                meta, _, path = entry.partition('\t')
                parts = meta.split()
                if len(parts) == 3 and parts[1] == 'tree' and path.startswith('rounds/'):
                    trees[path[len('rounds/'):]] = parts[2]
            status = self._git('status', '--porcelain=v1', '-z', '--ignored', '--untracked-files=all', '--', 'rounds').split('\0')
            renamed_old = False
            for item in status:
                # With -z a rename/copy is "XY new" followed by a bare "old" path.
                path = item if renamed_old else item[3:]
                renamed_old = not renamed_old and item[:1] in ('R', 'C')
                parts = path.split('/')
                if len(parts) > 1 and parts[0] == 'rounds':
                    trees.pop(parts[1], None)
            return trees
        except (OSError, subprocess.CalledProcessError):
            return {}

    def _validator_hash(self):
        digest = hashlib.sha256()
        for path in sorted((self.root / 'reproduce').glob('*.py')):
            digest.update(path.name.encode() + b'\0' + path.read_bytes() + b'\0')
        return digest.hexdigest()

    def _entry(self, round_id):
        tree = self.trees.get(round_id)
        if not tree:
            return None
        return self.dir / hashlib.sha256(f'{self.key_prefix}\0{round_id}\0{tree}'.encode()).hexdigest()

    def lookup(self, round_id):
        """Return the stored result dict for a round that already passed, else None."""
        entry = self._entry(round_id)
        if entry is None:
            return None
        try:
            return json.loads(entry.read_text())
        except (OSError, ValueError):
            return None

    def record_pass(self, round_id, result):
        entry = self._entry(round_id)
        if entry is None:
            return
        try:
            temp = entry.with_name(f'.{entry.name}.{os.getpid()}')
            temp.write_text(json.dumps(result))
            os.replace(temp, entry)
        except OSError:
            pass

    def note(self):
        return f'ROUND CACHE: {self.cached} rounds cached, {self.checked} checked'
