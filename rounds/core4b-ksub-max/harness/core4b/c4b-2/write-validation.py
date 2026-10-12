from pathlib import Path
import hashlib
import json
import subprocess
rows=[json.loads(l) for l in Path('evidence/validation-counts.jsonl').read_text().splitlines()]
lines=['# Validation','', 'Host: eu. Official grade sandbox; pinned control-worker environment. Plain runs only.', 'loaded runs pending — user requested deferral while pilot units are running.', '', '| Stack | Base check rc | Base tests/failures/errors | Reference check rc | Reference tests/failures/errors (3 runs) | Leftovers/zombies, every suite run |', '| --- | --- | --- | --- | --- | --- |']
for lang in ['rust','go','ts-bun']:
    r=[x for x in rows if x['lang']==lang]
    bc=next(x['check_rc'] for x in r if x['variant']=='bases' and 'check_rc'in x)
    rc=next(x['check_rc'] for x in r if x['variant']=='reference' and 'check_rc'in x)
    base=next(x['grade'] for x in r if x['variant']=='bases' and 'grade'in x)
    runs=[x for x in r if x['variant']=='reference' and 'grade'in x]
    assert len(runs)==3 and all(x['grade']==runs[0]['grade'] for x in runs)
    assert all(x['grade']['pass_'] for x in runs)
    lines.append(f"| {lang} | {bc} | {base['tests']}/{base['failures']}/{base['errors']} | {rc} | "+', '.join(f"{x['grade']['tests']}/{x['grade']['failures']}/{x['grade']['errors']}" for x in runs)+' | 0/0 |')
lines+=['','Suite seconds (3 reference runs, plain):']
for lang in ['rust','go','ts-bun']:
    lines.append('- '+lang+': '+', '.join(str(x['suite_seconds']) for x in rows if x['lang']==lang and x['variant']=='reference' and 'grade'in x))
lines+=['','Total suite runtime: '+str(round(sum(x.get('suite_seconds') or 0 for x in rows),3))+' seconds; total grade invocation runtime: '+str(round(sum(x.get('seconds',0) for x in rows),3))+' seconds.', 'All grade invocations rc 0; no skips. Reference outcomes identical across 3 runs.', 'Reference pre-cleanup candidate survivors: 0 on every test; post-cleanup leftovers/zombies: 0/0.', '', 'Harness per stack: rc 0; 20 planted rejections; 2 clean acceptances; 1 chunked marker; 3 escaped descendants; 0 leftovers; 0 zombies.', 'Evidence: evidence/harness-counts.jsonl (counts/rc only).', 'No measured pilots launched by this author. Loaded determinism and measured pass rate pending.', '', 'Git repositories (signed initial base commit; reference has base + solution commit):']
for lang in ['rust','go','ts-bun']:
    for v in ['bases','reference']:
        rev=subprocess.check_output(['git','-C',f'{v}/{lang}','rev-parse','HEAD'],text=True).strip()
        count=subprocess.check_output(['git','-C',f'{v}/{lang}','rev-list','--count','HEAD'],text=True).strip()
        lines.append(f'- {v}/{lang}: {rev}; commits {count}.')
lines+=['','All six commit signatures verified locally with the configured public key;', 'verification uses a task-local trust database because the home trust database', 'is read-only in this sandbox. Nothing was pushed.', '', 'SHA-256 (every prompt and hidden file; SPEC included):']
files=[Path('SPEC.md'),*sorted(Path('.').glob('prompt-*.md')),*sorted(p for p in Path('hidden').rglob('*') if p.is_file())]
for p in files:
    lines.append('- '+str(p)+': '+hashlib.sha256(p.read_bytes()).hexdigest())
Path('VALIDATION.md').write_text('\n'.join(lines)+'\n')
files=[Path('SPEC.md'),Path('LEVERS.md'),Path('VALIDATION.md'),*sorted(Path('.').glob('prompt-*.md'))]
for top in ['bases','reference','hidden']:
    files+=sorted(p for p in Path(top).rglob('*') if p.is_file() and '.git' not in p.parts)
Path('REVISION.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files))
print(hashlib.sha256(Path('REVISION.sha256').read_bytes()).hexdigest())
