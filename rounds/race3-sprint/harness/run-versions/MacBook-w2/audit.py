#!/usr/bin/python3
# audit.py — scan every arm's Codex events for downloads/installs and reads of ~/.codex*, ~/Library, iCloud, or ~/Areas (outside the arm workspace)
import json, glob, os, re, sys
from pathlib import Path
from validity import tree_hash, file_hash, events
from receipts import collect
R = os.path.dirname(os.path.abspath(__file__)); home = os.path.expanduser('~')
bad = re.compile(r'(\b(curl|wget)\b|git (clone|fetch|pull)|cargo (fetch|install)|go (get|install) |bun (add|install)|npm (install|add|ci)|mix deps.get|mix hex|\.codex|Mobile Documents|CloudDocs|' + re.escape(home) + r'/Library|~/Library|\$(?:HOME|\{HOME\})/Library|' + re.escape(home) + r'/Areas|~/Areas|\$(?:HOME|\{HOME\})/Areas|\.\./\.\./Areas|Areas/Kogen)')
flags = []
for f in sorted(glob.glob(R + '/out/*/turn-*.jsonl')):
    lang = f.split('/')[-2]
    for line in open(f, errors='ignore'):
        try: e = json.loads(line)
        except Exception: continue
        it = e.get('item') or {}
        cmd = it.get('command') or ''
        if isinstance(cmd, list): cmd = ' '.join(cmd)
        if cmd and bad.search(cmd): flags.append('FLAG %s %s %s' % (lang, os.path.basename(f), cmd[:200]))
root = Path(R)
frozen = {name: tree_hash(root / 'inputs' / name) for name in ('spec', 'conformance')}
frozen['target'] = file_hash(root / 'TARGET.md')
for snapshot in sorted((root / 'snapshots').glob('*')):
    if not snapshot.is_dir(): continue
    for arm in (root / 'ARMS').read_text().split():
        for name, sha in frozen.items():
            marker = snapshot / arm / ('.%s.sha' % name)
            got = marker.read_text().strip() if marker.is_file() else 'missing'
            if got != sha:
                flags.append('FLAG %s %s %s hash expected=%s actual=%s' % (arm, snapshot.name, name, sha, got))
            if name == 'target':
                target = snapshot / arm / 'TARGET.md'
                if not target.is_file() or file_hash(target) != sha:
                    flags.append('FLAG %s %s TARGET.md content changed or missing' % (arm, snapshot.name))
flags.extend(collect(root))
for flag in flags: print(flag)
print('audit done')
sys.exit(bool(flags))
