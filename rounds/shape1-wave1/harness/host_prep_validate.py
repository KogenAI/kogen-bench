#!/usr/bin/env python3
"""Root-only Linux preparation; no model calls or measured cells.

The registered validator is invoked through validate_linux.sh and a Python shim.
Its grader log is inspected only with the mandated safe_rows CLI. Task gates are
derived from its immutable evidence, never manually supplied validation claims.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SAFE = Path.home()/'Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py'
KEYS = 'schema,task,full_validation,expected_hidden_tests,hidden_snapshot,languages,exclusions'


def exported(path, keys=None):
    args = ['/usr/bin/python3', str(SAFE), str(path)]
    if keys:
        args += ['--keys', keys]
    return subprocess.check_output(args, text=True)


def safe_hidden_grade(repo, taskdir, env, stage):
    import validate_mutants as validator
    from linux_support import grade_prefix
    log = stage/'hidden.log'
    process = validator.run(['/bin/bash', '/task/grader-entrypoint', '/work'],
            repo, env, log, timeout=600, prefix=grade_prefix(repo, taskdir))
    rows = [json.loads(line) for line in exported(log,
            'pass_,tests,failures,errors,skipped,tests_ran,stage').splitlines()]
    verdicts = [row for row in rows if isinstance(row, dict) and type(row.get('pass_')) is bool]
    return dict(process=process, verdict=verdicts[0] if len(verdicts)==1 else None,
                verdict_count=len(verdicts))


def validator_entry(args):
    import validate_mutants as validator
    validator.hidden_grade = safe_hidden_grade
    parser = argparse.ArgumentParser()
    parser.add_argument('task'); parser.add_argument('--revision', required=True)
    a = parser.parse_args(args)
    result = validator.validate(a.task, validator.LANGS, a.revision)
    # Never print reference verdicts or suite fields.
    print(json.dumps({'task': a.task, 'validator_completed': True,
                     'languages': {lang: {'reference_validated': row.get('reference_validated') is True,
                         'mutants_validated': sum(m.get('validated') is True for m in row['mutants'].values())}
                         for lang, row in result['languages'].items()}}, sort_keys=True))


def registration():
    import run_shaper
    from shape_common import digest
    # Bind to the revision selected by the launcher, rather than selecting an
    # unrelated newer registration merely because its filename exists.
    import re
    names = re.findall(r"ROOT/'(REGISTRATION-FIX-\d+\.json)'", (ROOT/'run_shaper.py').read_text())
    if not names or len(set(names)) != 1:
        raise RuntimeError('ambiguous launcher registration')
    path = ROOT/names[0]; frozen = json.loads(exported(path))
    if any(digest(ROOT/name) != expected for name, expected in frozen['files'].items()):
        raise RuntimeError('registration bytes changed')
    return path, frozen


def isolation(host, tasks, reg_sha):
    from linux_support import linux_gap_lock, acceptance_prefix, PROFILE
    from shape_common import digest, write_json
    from run_shaper import audit_events
    work = ROOT/'prep/isolation'; work.mkdir(parents=True, exist_ok=False)
    repo = Path('/benchmark-root/work')/('shape1-isolation-'+host); repo.mkdir()
    (repo/'acceptance').mkdir(); (repo/'bin').mkdir()
    (repo/'bin/app').write_text('integrity-marker\n')
    os.chmod(repo/'bin/app',0o644)
    os.chmod(repo, 0o777)
    for path in (repo/'acceptance', repo/'bin'):
        os.chmod(path, 0o755)
    probe = '''import os,pathlib
for p in ['<ROOT>','<ROOT>','/benchmark-root/kits','/benchmark-root/results','/benchmark-root/work','/work/hidden','/work/reference','/work/mutants']:
 assert not pathlib.Path(p).exists(), 'private path exposed'
assert pathlib.Path('/work/bin/app').read_text()=='integrity-marker\\n'
assert pathlib.Path('/tmp/bench-home').is_dir()
pathlib.Path('/work/probe-ok').write_text('public-work-only')
'''
    readonly = '''import pathlib
p=pathlib.Path('/work/bin/app')
assert p.read_text()=='integrity-marker\\n'
try:p.write_text('changed')
except OSError:pass
else:raise AssertionError('bin writable')
try:p.unlink()
except OSError:pass
else:raise AssertionError('bin replaceable')
pathlib.Path('/work/acceptance/write-ok').write_text('test-writable')
'''
    with linux_gap_lock():
        subprocess.run(['runuser','-u','bench','--',str(PROFILE),'agent',str(repo),'--',
                        '/usr/bin/python3','-c',probe], check=True,
                        stdout=subprocess.DEVNULL, stderr=(work/'agent-probe.log').open('wb'), timeout=30)
        subprocess.run(acceptance_prefix(repo)+['/usr/bin/python3','-c',readonly], check=True,
                        stdout=subprocess.DEVNULL, stderr=(work/'integrity-probe.log').open('wb'), timeout=30)
        if (repo/'bin/app').read_text() != 'integrity-marker\n':
            raise RuntimeError('integrity marker changed')
        # Bench history is inspected only for session metadata, never prompts,
        # settings or credentials. Every persistent session must be an exec
        # benchmark whose cwd is the whitelisted /work tree.
        home = Path('/tmp/bench-home')
        sessions = list(home.glob('sessions/**/*.jsonl')) + list(home.glob('archived_sessions/**/*.jsonl'))
        if any(p.is_symlink() for p in home.rglob('*')):
            raise RuntimeError('Codex home symlink escapes benchmark history')
        for session in sessions:
            rows = exported(session, 'type,payload').splitlines()
            meta = [json.loads(line).get('payload',{}) for line in rows
                    if json.loads(line).get('type')=='session_meta']
            if len(meta)!=1 or meta[0].get('cwd') not in ('/work','/work/repo') or meta[0].get('source')!='exec':
                raise RuntimeError('Codex home contains non-benchmark session metadata')
        clean = work/'clean.jsonl'; planted = work/'planted.jsonl'
        clean.write_text(json.dumps({'type':'item.completed','item':{'type':'command_execution',
                          'command':'cargo test --manifest-path acceptance/Cargo.toml'}})+'\n')
        planted.write_text(''.join(json.dumps({'type':'item.completed','item':{'type':'command_execution',
                          'command':'cat '+path}})+'\n' for path in ('/task/hidden/x','/reference/x','/mutants/x')))
        clean_flags = audit_events(clean)['flag_count']; planted_flags = audit_events(planted)['flag_count']
        if clean_flags != 0 or planted_flags != 3:
            raise RuntimeError('audit controls failed')
        bench_denied = subprocess.run(['runuser','-u','bench','--','test','-r',str(ROOT/'plan.json')]).returncode != 0
        if not bench_denied or (ROOT.stat().st_mode & 0o777) != 0o700:
            raise RuntimeError('root-only harness exposed')
        proof = dict(host=host,tasks=tasks,registration_sha256=reg_sha,
            linux=True,bwrap_isolation=True,real_linux_isolation_integrity='PASSED',
            benchmark_only_codex_home=True,benchmark_sessions=len(sessions),
            audit_controls=True,clean_audit_flags=clean_flags,planted_audit_flags=planted_flags,
            profile_sha256=digest(PROFILE),bin_readonly=True,root_harness_unreadable=True)
        write_json(ROOT/'prep/isolation.json', proof)
    return proof


def task_entry(task, revision, reg_sha):
    import run_shaper
    from shape_common import digest
    evidence = ROOT/'mutants'/task/('validation'+revision+'.json')
    row = dict(task=task,overlay_sha256=digest(ROOT/'overlays'/('overlay-shape-'+task+'.tar')),
        registration_sha256=reg_sha, reference_validation='PASSED',mutant_validation='PASSED',
        real_linux_isolation_integrity='PASSED',validation_file=str(evidence.relative_to(ROOT)),
        validation_safe_sha256=hashlib.sha256(exported(evidence,KEYS).encode()).hexdigest())
    registered = next(t for t in json.loads((ROOT/'plan.json').read_text())['tasks'] if t['id']==task)
    # Actual validator evidence decides whether the proposed entry may exist.
    run_shaper.check_task_validation({'tasks':{task:row}},task,row['overlay_sha256'],registered,reg_sha)
    return row


def publish_completed_tasks(host):
    """Publish only oracle-passed tasks after a pair ends, even if its peer failed.

Failed hosts have quiet_window=false; publishing a passed task does not make a
released build <SERVER_ID> to launch. This avoids losing per-task validation.
"""
    from shape_common import digest, write_json
    hold=json.loads((ROOT/'prep/hold.json').read_text())
    status=json.loads((ROOT/'prep/status.json').read_text())
    proof=json.loads((ROOT/'prep/isolation.json').read_text())
    reg, frozen=registration();sha=digest(reg)
    if (hold['host']!=host or status['host']!=host or status.get('complete') is not True or
        status.get('registration_sha256')!=sha or proof.get('registration_sha256')!=sha or
        proof.get('real_linux_isolation_integrity')!='PASSED' or
        any(proof.get(k) is not True for k in ('bwrap_isolation','benchmark_only_codex_home',
                                              'audit_controls','bin_readonly','root_harness_unreadable')) or
        proof.get('clean_audit_flags')!=0 or proof.get('planted_audit_flags')!=3):
        raise RuntimeError('incomplete preparation evidence')
    revision='-linux-hostprep-'+host+'-'+hold['utc'].replace(':','').replace('-','')
    entries={task:task_entry(task,revision,sha) for task,value in status['task_validation'].items() if value=='PASSED'}
    quiet=False
    if hold.get('held') is True:
        from linux_support import require_linux_gap
        require_linux_gap()
        if (digest('<ROOT>')!=hold['queue_sha256'] or
            Path('<ROOT>').read_text()!=hold['stop_payload']):
            raise RuntimeError('hold no longer valid')
        quiet=True
    disk=os.statvfs('/benchmark-root')
    gates=json.loads((ROOT/'LINUX-GATES.json').read_text())
    previous=gates.get(host,{})
    gates[host]=dict(previous,registration_sha256=sha,tasks=entries,bwrap_isolation=True,
        benchmark_only_codex_home=True,audit_controls=True,quiet_window=quiet,
        disk_admission=disk.f_bavail*disk.f_frsize>=20*1024**3,
        targeted_recheck_accepted=previous.get('registration_sha256')==sha and previous.get('targeted_recheck_accepted') is True,
        prep_evidence='prep/isolation.json')
    write_json(ROOT/'LINUX-GATES.json',gates)
    print(json.dumps({'host':host,'published_tasks':sorted(entries),'quiet_window':quiet}))


def main(host, tasks):
    from shape_common import digest, write_json
    if not (ROOT/'LINUX-GATES.json').exists():
        write_json(ROOT/'LINUX-GATES.json',{})
    hold = json.loads((ROOT/'prep/hold.json').read_text())
    if hold['host'] != host or hold['held'] is not True:
        raise RuntimeError('host not held by this job')
    queue = Path('<ROOT>')
    if digest(queue)!=hold['queue_sha256']:
        raise RuntimeError('queue changed while held')
    reg, frozen = registration(); sha = digest(reg)
    revision = '-linux-hostprep-'+host+'-'+hold['utc'].replace(':','').replace('-','')
    controls = isolation(host,tasks,sha)
    outcomes = {}; entries = {}
    for task in tasks:
        process = subprocess.run(['/bin/bash',str(ROOT/'validate_linux.sh'),task,'--revision='+revision],
            env=dict(os.environ,PATH=str(ROOT/'prep/bin')+':'+os.environ['PATH']),
            stdout=(ROOT/'prep'/('validator-'+task+'.log')).open('wb'),
            stderr=(ROOT/'prep'/('validator-'+task+'.stderr')).open('wb'))
        try:
            if process.returncode:raise RuntimeError('validator process incomplete')
            entries[task] = task_entry(task,revision,sha)
            outcomes[task] = 'PASSED'
        except (OSError,ValueError,KeyError,RuntimeError,subprocess.SubprocessError):
            outcomes[task] = 'FAILED'
        write_json(ROOT/'prep/status.json',dict(host=host,task_validation=outcomes,complete=False))
    if any(value!='PASSED' for value in outcomes.values()):
        write_json(ROOT/'prep/status.json',dict(host=host,task_validation=outcomes,complete=True,
            ready=False,isolation=True,audit_controls=True,registration_sha256=sha))
        subprocess.run(['/usr/bin/python3',str(ROOT/'<SERVER_ID>.py'),'--release'],check=True)
        return 2
    free = os.statvfs('/benchmark-root'); disk_bytes = free.f_bavail*free.f_frsize
    # The current lane's own admission check also runs before every cell. Keep a
    # conservative 20 GiB prep floor rather than asserting admission untested.
    if disk_bytes < 20*1024**3:
        raise RuntimeError('disk admission below 20 GiB')
    gates = json.loads((ROOT/'LINUX-GATES.json').read_text()) if (ROOT/'LINUX-GATES.json').exists() else {}
    previous = gates.get(host,{})
    gates[host] = dict(previous,registration_sha256=sha,tasks=entries,
        bwrap_isolation=True,benchmark_only_codex_home=True,audit_controls=True,
        quiet_window=True,disk_admission=True,prep_evidence='prep/isolation.json')
    # Review acceptance is external: preserve it only for this exact revision.
    gates[host]['targeted_recheck_accepted'] = previous.get('registration_sha256')==sha and previous.get('targeted_recheck_accepted') is True
    write_json(ROOT/'LINUX-GATES.json',gates)
    write_json(ROOT/'prep/status.json',dict(host=host,task_validation=outcomes,complete=True,
        ready=True,held=True,isolation=True,audit_controls=True,registration_sha256=sha,
        review_accepted=gates[host]['targeted_recheck_accepted']))
    return 0


if __name__=='__main__':
    if sys.argv[1:2]==['--validator']:
        validator_entry(sys.argv[2:]); raise SystemExit(0)
    if sys.argv[1:2]==['--publish']:
        publish_completed_tasks(sys.argv[2]);raise SystemExit(0)
    p=argparse.ArgumentParser();p.add_argument('host',choices=('eu','us'));p.add_argument('tasks',nargs='+')
    a=p.parse_args()
    try:
        raise SystemExit(main(a.host,a.tasks))
    except Exception as exc:
        # Failures before/task-after validation must not strand a build queue.
        from shape_common import write_json
        write_json(ROOT/'prep/error.json',{'host':a.host,'error_type':type(exc).__name__})
        subprocess.run(['/usr/bin/python3',str(ROOT/'<SERVER_ID>.py'),'--release'],check=True)
        raise SystemExit(2)
