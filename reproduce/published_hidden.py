#!/usr/bin/env python3
"""Hidden-test files of a closed, published round: the one narrow carve-out of the release gate.

A sensitive file (for example test_hidden.py) is allowed only under
rounds/<id>/reproduce/tasks/<task>/evaluator/** and only when the round's PLAN.json
has publication.closed == true, lists the file under publication.files with its sha256,
and the published evaluator/ folder hashes to the pre-run hidden_tests hash of that task.
Only the hidden-test file names below qualify; credentials, transcripts, patches and sealed
or author-private paths are never allowed. The same module exempts, from the publication scan,
the path strings that closed round's PLAN.json lists under publication.files.
"""
import hashlib, json, os, re
from pathlib import Path

HIDDEN_TEST_NAMES = {'test_hidden.py'}
PRIVATE_PARTS = {'sealed', 'author-private', 'author_private'}
PLAN_PATH_RE = re.compile(r'^rounds/[^/]+/PLAN\.json$')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(root, exclude=('.git',)):
    """Same digest as lanes/lanes/common.py sha256_tree (what PLAN.json hidden_tests holds)."""
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in exclude)
        links = [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]
        dirnames[:] = [d for d in dirnames if d not in links]
        for name in sorted(filenames + links):
            if name in exclude:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, '/')
            if os.path.islink(path):
                line = f'l {os.readlink(path)} {rel}\n'
            else:
                mode = 'x' if os.stat(path).st_mode & 0o111 else 'f'
                line = f'{mode} {sha256_file(path)} {rel}\n'
            h.update(line.encode())
    return h.hexdigest()


_cache = {}


def _folder_ok(round_dir, task):
    key = (str(round_dir), task)
    if key not in _cache:
        _cache[key] = False
        try:
            plan = json.loads((round_dir / 'PLAN.json').read_text())
            publication = plan.get('publication')
            want = plan['hashes']['tasks'][task]['hidden_tests']
            evaluator = round_dir / 'reproduce' / 'tasks' / task / 'evaluator'
            _cache[key] = (isinstance(publication, dict) and publication.get('closed') is True
                           and isinstance(want, str) and evaluator.is_dir() and not evaluator.is_symlink()
                           and sha256_tree(evaluator) == want)
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            pass
    return _cache[key]


def allowed(path, root):
    """True when `path` is a hidden-test file the carve-out permits."""
    path = Path(path)
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    if path.name.lower() not in HIDDEN_TEST_NAMES or PRIVATE_PARTS & {p.lower() for p in parts}:
        return False
    if len(parts) < 7 or parts[0] != 'rounds' or parts[2:4] != ('reproduce', 'tasks') or parts[5] != 'evaluator':
        return False
    round_dir = Path(root) / 'rounds' / parts[1]
    if path.is_symlink() or not path.is_file() or not _folder_ok(round_dir, parts[4]):
        return False
    try:
        listed = json.loads((round_dir / 'PLAN.json').read_text())['publication']['files']
        return listed.get('/'.join(parts[2:])) == sha256_file(path)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return False


def plan_publication_spans(text, relative_path):
    """Character spans of `text` the publication scan may skip: in `rounds/<id>/PLAN.json` with
    publication.closed true, each publication.files key under reproduce/tasks/<task>/evaluator/."""
    if not PLAN_PATH_RE.match(relative_path):
        return []
    try:
        publication = json.loads(text)['publication']
        if publication.get('closed') is not True:
            return []
        keys = list(publication['files'])
    except (ValueError, KeyError, TypeError, AttributeError):
        return []
    spans = []
    for key in keys:
        parts = key.split('/') if isinstance(key, str) else []
        if len(parts) < 5 or parts[:2] != ['reproduce', 'tasks'] or parts[3] != 'evaluator' or '..' in parts or '' in parts:
            continue
        needle = '"' + json.dumps(key)[1:-1] + '"'
        start = text.find(needle)
        while start != -1:
            spans.append((start, start + len(needle)))
            start = text.find(needle, start + 1)
    return spans
