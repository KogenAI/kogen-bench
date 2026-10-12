"""Rebuild author evidence from grade-sandbox counts and payload digests."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
langs = ['rust', 'go', 'ts-bun']
read = lambda name: json.loads((root / name).read_text())
validate, loaded = read('validate-results.json'), read('loaded-results.json')
runtime, audit = read('runtime-results.json'), read('audit-results.json')
guards, storage = read('guards-results.json'), read('storage-results.json')
burners = read('burner-count.json')
assert burners == dict(cores=2, burners=2, stopped=True, zombies=0)
for lang in langs:
    for kind in ['bases', 'reference']:
        check, grade = validate[f'{kind}/{lang}-check'], validate[f'{kind}/{lang}-grade']
        assert check['rc'] == grade['rc'] == 0
        verdict = grade['verdict']
        assert verdict == dict(pass_=kind == 'reference', tests=29,
                               failures=29 if kind == 'bases' else 0, errors=0,
                               skipped=0, tests_ran=True, stage='suite')
    repeats = [loaded[f'reference/{lang}-{i}'] for i in range(1, 6)]
    assert all(r['rc'] == 0 and r['verdict'] == validate[f'reference/{lang}-grade']['verdict'] for r in repeats)
    assert runtime[f'reference/{lang}-flock']['rc'] == 0
    assert storage[f'reference/{lang}-storage']['rc'] == 0
    assert storage[f'reference/{lang}-storage']['author_result'] == dict(rc=0, checks=1)
assert audit['suite-contract']['rc'] == 0
assert audit['suite-contract']['author_result'] == dict(checks=79, rc=0)
assert guards['cleanup']['verdict'] == dict(pass_=True, tests=4, failures=0,
    errors=0, skipped=0, tests_ran=True, stage='suite')
assert guards['deadline']['verdict'] == dict(pass_=False, tests=1, failures=0,
    errors=1, skipped=0, tests_ran=True, stage='suite')
assert guards['deadline']['elapsed_seconds'] < 45
assert guards['hang']['verdict'] == dict(pass_=False, tests=29, failures=0,
    errors=29, skipped=0, tests_ran=True, stage='suite')
assert guards['hang']['elapsed_seconds'] < 300
process_runs = [r for group in [validate, loaded, guards, storage] for r in group.values()
                if 'sandbox_process_check' in r]
for r in process_runs:
    assert r['rc'] == 0
    assert r['sandbox_process_check'] == r['<SERVER_ID>'] == dict(rc=0, leftovers=0, zombies=0)
files = [Path('SPEC.md'), Path('FAIRNESS.md')]
files += [Path(name) for name in ['<SERVER_ID>.py', 'write-validation.py',
          'suite-contract-check.py', 'validation-probe.py', 'cleanup_audit.py',
          'reference-storage-audit.py']]
files += sorted(root.glob('prompt-*.md'))
files += [p for p in (root/'hidden').rglob('*') if p.is_file()]
for kind in ['bases', 'reference']:
    for lang in langs:
        directory = Path(kind)/lang
        tracked = subprocess.check_output(['git', '-C', str(root/directory), 'ls-files'], text=True).splitlines()
        files += [directory/name for name in tracked]
files = sorted({str(p.relative_to(root) if p.is_absolute() else p) for p in files})
hashes = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files}
(root/'validated-payload-sha256.json').write_text(json.dumps(hashes, indent=2)+'\n')
all_runs = [r for group in [validate, loaded, runtime, audit, guards, storage] for r in group.values()]
total = round(sum(r['elapsed_seconds'] for r in all_runs), 3)
suite_total = round(sum(r['suite_seconds'] or 0 for r in all_runs), 3)
counts = dict(host='eu', validation=validate, loaded_runs=loaded, cpu_load=burners,
              runtime=runtime, suite_contract=dict(rc=0, checks=79), guards=guards,
              storage=storage, process_checks=dict(runs=len(process_runs),
              sandbox_rc=0,host_rc=0,leftovers=0,zombies=0),
              deadlines=dict(test_seconds=45,suite_seconds=240),
              total_elapsed_seconds=total, total_suite_seconds=suite_total)
(root/'validation-counts.json').write_text(json.dumps(counts, indent=2)+'\n')
lines = ['# Validation', '', 'Host: eu. Official grade sandbox; pinned offline environment.', '',
'| Stack | Base check rc | Base grader rc | Base tests / failures / errors / skipped | Reference check rc | Reference grader rc | Reference tests / failures / errors / skipped |',
'| --- | ---: | ---: | --- | ---: | ---: | --- |']
def fmt_counts(r):
    v = r['verdict']
    return ' / '.join(str(v[k]) for k in ['tests', 'failures', 'errors', 'skipped'])
for lang in langs:
    b, r = validate[f'bases/{lang}-grade'], validate[f'reference/{lang}-grade']
    lines.append(f'| {lang} | 0 | {b["rc"]} | {fmt_counts(b)} | 0 | {r["rc"]} | {fmt_counts(r)} |')
lines += ['', 'Loaded repeats: 2 cores; 2 CPU burners; 5 identical results per reference; burner cleanup rc 0.', '',
          '| Stack | Loaded 1 rc; tests / failures / errors / skipped | Loaded 2 rc; counts | Loaded 3 rc; counts | Loaded 4 rc; counts | Loaded 5 rc; counts |',
          '| --- | --- | --- | --- | --- | --- | --- |']
for lang in langs:
    entries = [loaded[f'reference/{lang}-{i}'] for i in range(1, 6)]
    lines.append('| '+lang+' | '+' | '.join(f'{r["rc"]}; {fmt_counts(r)}' for r in entries)+' |')
lines += ['', '| Stack | Base suite seconds | Reference suite seconds | Loaded 1 seconds | Loaded 2 seconds | Loaded 3 seconds | Loaded 4 seconds | Loaded 5 seconds |',
          '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
for lang in langs:
    entries = [validate[f'bases/{lang}-grade'], validate[f'reference/{lang}-grade'], *[loaded[f'reference/{lang}-{i}'] for i in range(1, 6)]]
    lines.append('| '+lang+' | '+' | '.join(f'{r["suite_seconds"]:.3f}' for r in entries)+' |')
lines += ['', '| Stack | Grade-sandbox flock lookup and acquisition rc |', '| --- | ---: |']
for lang in langs:
    lines.append(f'| {lang} | {runtime[f"reference/{lang}-flock"]["rc"]} |')
lines += ['', 'Suite framing/integer/duplicate-member audit: 79 rejection checks; rc 0.',
          'Reference storage-member output audits: 1 check per stack; rc 0.', '',
          '| Guard | rc | Tests / failures / errors / skipped | Seconds |',
          '| --- | ---: | --- | ---: |']
for key in ['cleanup','deadline','hang']:
    r=guards[key]
    lines.append(f'| {key} | {r["rc"]} | {fmt_counts(r)} | {r["elapsed_seconds"]:.3f} |')
lines += ['', 'Deadline and hang guards: expected failed verdicts; assertion rc 0.',
          'Hard deadlines: 45 seconds per complete test; 240 seconds per suite.',
          f'Post-run ps -eo stat,ppid,args checks: {len(process_runs)} runs; sandbox rc 0; host rc 0; leftovers 0; zombies 0.', '',
f'Final validation including loaded repeats and guards elapsed total: {total:.3f} seconds.',
f'Suite execution total: {suite_total:.3f} seconds.', '', '| File | SHA-256 |', '| --- | --- |']
for name in files:
    if name.startswith(('prompt-', 'hidden/')) or name in ['SPEC.md', 'FAIRNESS.md']:
        lines.append(f'| {name} | `{hashes[name]}` |')
(root/'VALIDATION.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(dict(elapsed_seconds=total, suite_seconds=suite_total, payload_files=len(hashes))))
