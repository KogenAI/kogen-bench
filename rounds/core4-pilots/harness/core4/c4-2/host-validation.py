#!/usr/bin/env python3
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import re
import signal

ROOT=Path('<ROOT>')
PROFILE='/benchmark-root/kits/current/reproduce/sandbox-profile.sh'
LANGS=['rust','go','ts-bun']
ENV={**os.environ,'HOME':'/tmp/bench-home','PYTHONDONTWRITEBYTECODE':'1',
'PATH':'/benchmark-root/toolchains/go-1.27.1/bin:/benchmark-root/toolchains/rust-1.97.1/bin:/benchmark-root/toolchains/bun-1.4.2/bin:/benchmark-root/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/mise/installs/ruby/3.4.8/bin:/benchmark-root/toolchains/python-3.14.7/bin:/usr/bin:/bin',
'PYTHONPATH':'/benchmark-root/toolchains/python-3.14.7/lib/python3.14/site-packages',
'RUSTUP_HOME':'/opt/bench/rustup','CARGO_NET_OFFLINE':'true','GOTOOLCHAIN':'local','GOPROXY':'off'}

def run(lang,kind,command,label):
    work=ROOT/kind/lang
    task=ROOT/f'taskdir-{lang}'
    start=time.monotonic()
    is_suite = label == 'grade' or label.startswith('loaded-') or label in ['hang', 'deadline', 'cleanup', 'storage']
    p=subprocess.run([PROFILE,'grade',str(work),str(task),'--','python3',
                     '/task/validation-probe.py', 'suite' if is_suite else 'command',
                     *command],env=ENV,capture_output=True,text=True,timeout=330)
    elapsed=round(time.monotonic()-start,3)
    logs=ROOT/'validation-logs';logs.mkdir(exist_ok=True)
    (logs/f'{kind}-{lang}-{label}.log').write_text(p.stdout+'\n'+p.stderr)
    verdict=None
    process_check=None
    author_result=None
    for line in reversed(p.stdout.splitlines()):
        try:
            value=json.loads(line)
            if isinstance(value,dict) and 'pass_' in value:verdict=value
            if isinstance(value,dict) and 'sandbox_process_check' in value:process_check=value['sandbox_process_check']
            if isinstance(value,dict) and 'checks' in value:author_result=value
        except ValueError:pass
    suite_times=re.findall(r'Ran \d+ tests? in ([\d.]+)s',p.stderr)
    result=dict(rc=p.returncode,elapsed_seconds=elapsed,suite_seconds=float(suite_times[-1]) if suite_times else None,verdict=verdict)
    if author_result is not None:
        result['author_result']=author_result
    if is_suite:
        snapshot=subprocess.check_output(['ps','-eo','stat,ppid,args'],text=True)
        (logs/f'{kind}-{lang}-{label}-host-ps.txt').write_text(snapshot)
        rows=[line.split(None,2) for line in snapshot.splitlines()[1:]]
        zombies=[row for row in rows if row[0].startswith('Z')]
        # Other jobs may be running in separate PID namespaces on this host.
        # The sandbox assertion covers every process in our namespace; its
        # remaining host-side bwrap processes must also be absent.
        leftovers=[row for row in rows if
                   (row[2].startswith('/usr/bin/bwrap ') and str(ROOT) in row[2])
                   or row[2].startswith(str(ROOT)+'/')]
        result['sandbox_process_check']=process_check
        result['<SERVER_ID>']=dict(rc=0 if not zombies and not leftovers else 1,
                                         zombies=len(zombies),leftovers=len(leftovers))
        assert process_check == dict(rc=0,leftovers=0,zombies=0), (label,process_check)
        assert not zombies and not leftovers, (label,zombies,leftovers)
    return result

mode=sys.argv[1]
selected = sys.argv[2:] or LANGS
assert all(lang in LANGS for lang in selected)
result_path = ROOT/f'{mode}-results.json'
results=json.loads(result_path.read_text()) if sys.argv[2:] and result_path.exists() else {}
burners=[]
if mode=='loaded':
    for _ in range(os.cpu_count()):
        burners.append(subprocess.Popen(['yes'],stdout=subprocess.DEVNULL,start_new_session=True))
    assert len(burners)==os.cpu_count() and all(p.poll() is None for p in burners)
    (ROOT/'burner-count.json').write_text(json.dumps(dict(cores=os.cpu_count(),burners=len(burners)))+'\n')

def stop_burners():
    for p in burners:
        if p.poll() is None:
            os.killpg(p.pid,signal.SIGKILL)
        p.wait(timeout=3)

import atexit
atexit.register(stop_burners)
def terminate(_sig, _frame):
    stop_burners()
    sys.exit(1)
signal.signal(signal.SIGTERM,terminate)
signal.signal(signal.SIGINT,terminate)
for lang in selected:
    task=ROOT/f'taskdir-{lang}';task.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'hidden',task/'hidden',dirs_exist_ok=True)
    shutil.copyfile(ROOT/'validation-probe.py',task/'validation-probe.py')
    for helper in ['cleanup_audit.py','reference-storage-audit.py']:
        shutil.copyfile(ROOT/helper,task/helper)
    for kind in ['bases','reference']:
        if mode=='format':
            results[f'{kind}/{lang}']=run(lang,kind,['make','format'],'format')
            if lang=='rust':results[f'{kind}/{lang}-lock']=run(lang,kind,['cargo','generate-lockfile','--offline'],'lock')
        elif mode=='validate':
            results[f'{kind}/{lang}-check']=run(lang,kind,['make','check'],'check')
            results[f'{kind}/{lang}-grade']=run(lang,kind,['/bin/bash','/task/grader-entrypoint','/work'],'grade')
        elif mode=='runtime' and kind=='reference':
            results[f'{kind}/{lang}-flock']=run(lang,kind,['/bin/sh','-c','command -v flock >/dev/null && flock /work/.runtime-flock /bin/true'],'flock')
        elif mode=='audit' and kind=='reference' and lang=='rust':
            helper=ROOT/kind/lang/'suite-contract-check.py'
            shutil.copyfile(ROOT/'suite-contract-check.py',helper)
            try:
                results['suite-contract']=run(lang,kind,['python3','/work/suite-contract-check.py'],'suite-contract')
            finally:
                helper.unlink()
        elif mode=='storage' and kind=='reference':
            results[f'{kind}/{lang}-storage']=run(lang,kind,['python3','/task/reference-storage-audit.py'],'storage')
        elif mode=='guards' and kind=='reference' and lang=='rust':
            results['cleanup']=run(lang,kind,['python3','/task/cleanup_audit.py','cleanup'],'cleanup')
            print(json.dumps(results['cleanup']),flush=True)
            results['deadline']=run(lang,kind,['python3','/task/cleanup_audit.py','deadline'],'deadline')
            print(json.dumps(results['deadline']),flush=True)
            hang=task/'hang-app.py'
            hang.write_text('#!/usr/bin/env python3\nimport time\ntime.sleep(600)\n')
            hang.chmod(0o755)
            try:
                results['hang']=run(lang,kind,['python3','/task/hidden/suite/run.py','/task/hang-app.py'],'hang')
            finally:
                hang.unlink()
        elif mode=='loaded' and kind=='reference':
            for i in range(5):
                assert all(p.poll() is None for p in burners)
                results[f'{kind}/{lang}-{i+1}']=run(lang,kind,['python3','/task/hidden/suite/run.py','/work/bin/app'],f'loaded-{i+1}')
                assert all(p.poll() is None for p in burners)
                print(f'{lang} loaded run {i+1}: '+json.dumps(results[f'{kind}/{lang}-{i+1}']),flush=True)
stop_burners()
if mode=='loaded':
    assert all(p.returncode is not None for p in burners)
    rows=subprocess.check_output(['ps','-eo','stat,ppid,args'],text=True).splitlines()[1:]
    assert not any(line.split()[0].startswith('Z') for line in rows)
    (ROOT/'burner-count.json').write_text(json.dumps(dict(cores=os.cpu_count(),burners=len(burners),
                                                        stopped=True,zombies=0))+'\n')
(ROOT/f'{mode}-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
