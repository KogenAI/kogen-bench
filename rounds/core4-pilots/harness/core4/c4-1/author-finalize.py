"""Record final counts, repository state, canaries and file hashes; no test output."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path('<ROOT>')
counts = json.loads((root / 'validation-counts.json').read_text())
records = counts['records']
gates = [r for r in records if 'cleanup_rc' in r]
assert len(gates) == 24
assert all(r['leftovers'] == r['zombies'] == r['cleanup_rc'] == 0 for r in gates)
cleanup = next(r for r in records if 'cleanup_tests' in r)
contract = next(r for r in records if 'contract_tests' in r)
assert cleanup['cleanup_tests'] == 21 and cleanup['failures'] == cleanup['errors'] == cleanup['rc'] == 0
assert contract['contract_tests'] == 38 and contract['internal_alternates_tests'] == 1
assert contract['failures'] == contract['errors'] == contract['rc'] == 0
langs = ['rust', 'go', 'ts-bun']
summary = {}
repos = []
for lang in langs:
    normal = [r for r in records if r.get('lang') == lang and not r.get('loaded')]
    loaded = [r for r in records if r.get('lang') == lang and r.get('loaded')]
    assert len(normal) == 2 and len(loaded) == 5
    for r in normal:
        log = (root / 'author-logs' / f"grade-{r['variant']}-{lang}.log").read_text()
        r['suite_seconds'] = float(re.search(r'Ran 29 tests in ([0-9.]+)s', log).group(1))
        assert r['check_rc'] == r['grader_rc'] == r['errors'] == r['skipped'] == 0
        assert r['tests'] == 29 and r['failures'] == (29 if r['variant'] == 'bases' else 0)
    assert {tuple(r[k] for k in ['tests', 'failures', 'errors', 'skipped', 'pass_']) for r in loaded} == {(29, 0, 0, 0, True)}
    assert all(r['cpu_burners'] == 2 and r['grader_rc'] == 0 for r in loaded)
    summary[lang] = {'base': normal[0], 'reference': normal[1], 'loaded': loaded}
    for variant, expected in [('bases', 1), ('reference', 2)]:
        path = root / variant / lang
        git = lambda *args: subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()
        n = int(git('rev-list', '--count', 'HEAD'))
        changes = len(git('status', '--porcelain').splitlines())
        assert n == expected and changes == 0
        repos.append({'variant': variant, 'lang': lang, 'commits': n,
                      'head': git('rev-parse', 'HEAD'), 'changes': changes})

canary = (root / 'hidden/CANARY.txt').read_text().splitlines()[-1]
hidden = sorted(p for p in (root / 'hidden').rglob('*') if p.is_file())
assert len(hidden) == 4
assert all('# ' + canary in p.read_text() for p in hidden)
assert 'test_queue.py' not in (root / 'grader-entrypoint').read_text()
spec = (root / 'SPEC.md').read_text()
for lang in langs:
    prompt = (root / f'prompt-{lang}.md').read_text()
    assert prompt.startswith(spec + '\n')
    assert len(prompt[len(spec) + 1:].splitlines()) == 2
paths = hidden + sorted(root.glob('prompt-*.md')) + [root / 'SPEC.md']
hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
assert hashes == json.loads((root / 'host-hashes.json').read_text())
counts.update(summary=summary, repositories=repos, hashes=hashes,
              cleanup_summary={'sandbox_runs': 23, 'gates': 24, 'leftovers': 0, 'zombies': 0, 'rc': 0})
(root / 'validation-counts.json').write_text(json.dumps(counts, indent=2) + '\n')
(root / 'validation-results.json').write_text(json.dumps(records, indent=2) + '\n')

lines = ['# Validation', '', 'Host: `eu`; official grade sandbox; all builds, checks and suites offline.', '',
         '| Language | Base check rc | Base tests / failures / errors / skipped | Reference check rc | Reference tests / failures / errors / skipped | Loaded reference runs with identical counts |',
         '| --- | ---: | --- | ---: | --- | ---: |']
for lang in langs:
    lines.append(f'| {lang} | 0 | 29 / 29 / 0 / 0 | 0 | 29 / 0 / 0 / 0 | 5 |')
lines += ['', 'Loaded runs: `yes > /dev/null` on each of eu\'s 2 cores (2 concurrent burners),',
          'alive throughout all 15 reference suite runs; both burners reaped, rc 0.',
          'Each reference also passes one normal grader suite run. Loaded verdicts and',
          'tests/failures/errors/skipped counts are identical across all five runs per language.', '',
          '| Language | Base suite seconds | Reference normal suite seconds | Loaded suite wall seconds, runs 1 / 2 / 3 / 4 / 5 |',
          '| --- | ---: | ---: | --- |']
for lang in langs:
    r = summary[lang]
    durations = ' / '.join(f"{v['suite_seconds']:.3f}" for v in r['loaded'])
    lines.append(f"| {lang} | {r['base']['suite_seconds']:.3f} | {r['reference']['suite_seconds']:.3f} | {durations} |")
lines += ['', 'Loaded wall seconds include sandbox startup.',
          f"Total final validation runtime (builds, checks, suites, cleanup checks): {counts['total_seconds']:.3f} seconds.",
          'All grader and suite runner exit codes: 0.',
          'Canaries: 4 / 4 files, rc 0; grader-entrypoint comment canary matches CANARY.txt, rc 0.',
          'Process-tree cleanup regressions: 21 tests / 0 failures / 0 errors, rc 0.',
          'Strict JSON/schema/framing regressions: 38 tests / 0 failures / 0 errors, rc 0.',
          'Internal-alternates regression: 1 test / 0 failures / 0 errors, rc 0.',
          'Cleanup gates: 23 sandbox runs, 0 leftovers / 0 zombies after every run, rc 0.',
          'Final burner cleanup: 0 leftovers / 0 zombies, rc 0; total cleanup gates: 24.',
          'Prompt parity: 3 / 3, rc 0.', '',
          '| Language | Base commits | Reference commits | Working tree changes |',
          '| --- | ---: | ---: | ---: |']
for lang in langs:
    lines.append(f'| {lang} | 1 | 2 | 0 |')
lines += ['', '| File | SHA-256 |', '| --- | --- |']
for path, digest in sorted(hashes.items()):
    lines.append(f'| `{path}` | `{digest}` |')
lines += ['', 'Open issues: 0.', '']
(root / 'VALIDATION.md').write_text('\n'.join(lines))
print(json.dumps({'host': 'eu', 'languages': 3, 'loaded_runs': 15,
                  'loaded_tests': 435, 'failures': 0, 'errors': 0,
                  'total_seconds': counts['total_seconds'], 'hashes': len(hashes), 'rc': 0}))
