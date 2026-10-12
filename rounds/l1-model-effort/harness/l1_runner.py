#!/usr/bin/env python3
"""Root supervision of frozen L1 harness copies. Never open authentication files."""
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

RULE_SHA = '5fea4b24d6fe41c64d0312072d9464e86fcacb4d606bee9eb4a6d0b9730c02ce'
CONFIG = {
    'eu': ('ex', '[path omitted]', ['sol61-high','luna-max','sol61-medium','luna-medium']),
    'us': ('go', '[path omitted]', ['sol61-medium','luna-max','sol61-high','luna-medium']),
}
PAIRS = {'sol61-high':('gpt-6.1-sol','high'), 'sol61-medium':('gpt-6.1-sol','medium'),
         'luna-max':('gpt-6-luna','max'), 'luna-medium':('gpt-6-luna','medium')}
QUOTA = re.compile(r'\b429\b|rate.?limit|quota|usage limit|too many requests|limit reached', re.I)
PROVIDER = re.compile(r'connection (?:failed|reset)|server error|\b50[0234]\b|provider unavailable|stream disconnected', re.I)
BUILD = re.compile(r'\b(mix\s+(compile|test)|go\s+(build|test))\b')
FIELDS = ('input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens','total_tokens')

def utc(epoch=None):
    return dt.datetime.fromtimestamp(time.time() if epoch is None else epoch, dt.timezone.utc).isoformat().replace('+00:00','Z')

def epoch(value):
    try: return dt.datetime.fromisoformat(value.replace('Z','+00:00')).timestamp()
    except (ValueError,TypeError,AttributeError): return None

def append(path, row):
    row = dict(recorded_at=utc(), **row)
    with path.open('a') as f:
        f.write(json.dumps(row,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps(row,sort_keys=True),flush=True)

def save(path, row):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(row,indent=2,sort_keys=True)+'\n'); tmp.replace(path)

def tree_sha(root, exclude_inputs=False):
    command='set -o pipefail; export LC_ALL=C; find . -type f'
    if exclude_inputs: command += " -not -path './inputs/*'"
    command += ' -print0 | sort -z | xargs -0 sha256sum | sha256sum'
    return subprocess.check_output(['/bin/bash','-c',command],cwd=root,text=True).split()[0]

def events(path):
    try:
        with path.open(errors='replace') as f:
            for line in f:
                try: yield json.loads(line)
                except ValueError: pass
    except OSError: return

def quota(home):
    # Metadata only: auth.json is never opened, copied, or parsed.
    try: login=(home/'auth.json').stat().st_mtime
    except OSError: login=None
    now=time.time(); best=None
    files=sorted((home/'sessions').glob('*/*/*/rollout-*.jsonl'),key=lambda p:p.stat().st_mtime,reverse=True)
    for path in files[:60]:
        with path.open(errors='replace') as stream:
            rows=[]
            for line in stream:
                if '"rate_limits"' not in line: continue
                try: rows.append(json.loads(line))
                except ValueError: pass
        for row in rows:
            when=epoch(row.get('timestamp')); limits=(row.get('payload') or {}).get('rate_limits')
            if not isinstance(limits,dict) or when is None or login is None or when<login: continue
            if best is None or when>best[0]: best=(when,limits)
    result=dict(account='billing@',codex_home=str(home),checked_at=utc(now),login_boundary=utc(login) if login else 'NA',
                used_percent='NA',as_of='NA',available='NA',source='post-login session rate_limits')
    if best:
        when,limits=best; primary=limits.get('primary') or {}; reset=primary.get('resets_at')
        result.update(as_of=utc(when),resets_at=utc(reset) if isinstance(reset,(int,float)) else 'NA',
                      plan_type=limits.get('plan_type'),secondary=limits.get('secondary'))
        if isinstance(reset,(int,float)) and reset>now:
            used=primary.get('used_percent')
            result.update(used_percent=used if isinstance(used,(int,float)) else 'NA',
                          available=used<100 if isinstance(used,(int,float)) else 'NA')
        else: result['freshness']='window reset; current usage unavailable'
    return result

def thread(root, arm):
    path=root/'out'/arm/'thread'
    tid=path.read_text().strip() if path.exists() else ''
    if not tid:
        tid=next((r.get('thread_id') for r in events(root/'out'/arm/'turn-0.jsonl') if r.get('thread_id')),'')
    return tid if re.fullmatch(r'[A-Za-z0-9_-]+',tid or '') else ''

def usage_rows(rows):
    # Differences of cumulative receipts count each increment once. If a
    # resume resets a counter, start a new segment rather than discard usage.
    sums={key:0 for key in FIELDS}; previous={}; seen=set(); count=0
    for when,values in sorted(rows,key=lambda r:r[0]):
        key=(when,json.dumps(values,sort_keys=True))
        if key in seen: continue
        seen.add(key); count+=1
        for field in FIELDS:
            value=values.get(field)
            if type(value) is not int or value<0: continue
            prior=previous.get(field)
            sums[field]+=value if prior is None or value<prior else value-prior
            previous[field]=value
    return {key:sums[key] if key in previous else 'NA' for key in FIELDS},count

def usage(root,arm,home,cutoff):
    tid=thread(root,arm); rows=[]
    if tid:
        for path in (home/'sessions').glob('*/*/*/rollout-*'+tid+'*.jsonl'):
            for row in events(path):
                when=epoch(row.get('timestamp')); p=row.get('payload') or {}
                if when is None or when>cutoff or p.get('type')!='token_count': continue
                values=(p.get('info') or {}).get('total_token_usage')
                if isinstance(values,dict): rows.append((when,values))
    totals,count=usage_rows(rows)
    return dict(thread_id=tid or 'NA',totals=totals,cumulative_receipts=count,cutoff=utc(cutoff),
                method='sum cumulative increments once; new segment on counter reset; missing fields NA')

def stream_stats(root,arm,cutoff):
    commands={}; errors=[]; exit_codes=[]; completed=0; successful=0
    for path in sorted((root/'out'/arm).glob('turn-*.jsonl')):
        ts=path.with_suffix('.ts')
        timings=ts.read_text().splitlines() if ts.exists() else []
        for i,row in enumerate(events(path)):
            when=float(timings[i].split('\t')[0]) if i<len(timings) else None
            item=row.get('item') or {}; kind=row.get('type')
            if kind in ('error','turn.failed'):
                message=json.dumps(row.get('error') or row.get('message') or row)
                errors.append(message)
            if item.get('type')!='command_execution': continue
            key=(path.name,item.get('id'))
            if kind=='item.started': commands[key]=dict(command=item.get('command',''),start=when,end=None)
            if kind=='item.completed':
                completed+=1; successful+=item.get('exit_code')==0
                record=commands.setdefault(key,dict(command=item.get('command',''),start=None,end=None))
                record['end']=when
        err=path.with_suffix('.err')
        if err.exists():
            text=err.read_text(errors='replace')
            exit_codes.extend(int(x) for x in re.findall(r'Exit status:\s*(-?[0-9]+)',text))
            errors.extend(line for line in text.splitlines() if QUOTA.search(line) or PROVIDER.search(line))
    matches=[c for c in commands.values() if BUILD.search(c['command']) and c['start'] is not None and c['start']<=cutoff]
    return dict(completed_commands=completed,successful_commands=successful,model_errors=errors,
                build_test_proxy=dict(regex=BUILD.pattern,count=len(matches),
                    duration_seconds=round(sum(max(0,min(c['end'] or cutoff,cutoff)-c['start']) for c in matches),3),
                    unfinished_clipped=sum(c['end'] is None or c['end']>cutoff for c in matches)),
                process_exit_codes=exit_codes)

def driver_processes(root):
    processes={}; drivers=set()
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit(): continue
        try:
            stat=(entry/'stat').read_text(); ppid=int(stat[stat.rfind(')')+2:].split()[1])
            args=(entry/'cmdline').read_bytes().split(b'\0'); args=[a.decode(errors='replace') for a in args if a]
            pid=int(entry.name); processes[pid]=ppid
            if any(a==str(root/'arm.sh') or a==str(root/'arm-cont.sh') for a in args): drivers.add(pid)
        except (OSError,ValueError): pass
    found=set(drivers)
    while True:
        extra={pid for pid,ppid in processes.items() if ppid in found}
        if extra<=found: break
        found|=extra
    return found

def send(pids,sig):
    for pid in pids:
        try: os.kill(pid,sig)
        except ProcessLookupError: pass

def refusal(root,arm,offsets):
    messages=[]
    for path in (root/'out'/arm).glob('turn-*'):
        if path.suffix not in ('.jsonl','.err'): continue
        try:
            with path.open(errors='replace') as f:
                f.seek(offsets.get(str(path),0)); text=f.read(); offsets[str(path)]=f.tell()
            for line in text.splitlines():
                if path.suffix=='.err':
                    if QUOTA.search(line): messages.append(line[:500])
                else:
                    try: row=json.loads(line)
                    except ValueError: continue
                    if row.get('type') in ('error','turn.failed') and QUOTA.search(json.dumps(row)):
                        messages.append(str(row.get('message') or row.get('error') or row)[:500])
        except OSError: pass
    return messages

def operator(root,args,stdout=None,timeout=None):
    return subprocess.run(['runuser','-u','operator','--','/usr/bin/env','PYTHONDONTWRITEBYTECODE=1',
                           '/bin/bash','-c','cd "$1"; shift; exec "$@"','l1',str(root),*args],
                          stdout=stdout,stderr=subprocess.STDOUT,timeout=timeout)

def remove_ephemeral(root,arm):
    removed=[]
    for path in [root/'seed-cache',root/arm/'.kitcache',root/arm/'.cache/go-build']:
        if path.is_symlink(): path.unlink(); removed.append(str(path))
        elif path.is_dir(): shutil.rmtree(path); removed.append(str(path))
    for path in (root/'snapshots').glob('T+*m'):
        if path.name!='T+030m' and path.is_dir() and not path.is_symlink():
            shutil.rmtree(path); removed.append(str(path))
    return removed

def safe_stop(root):
    (root/'STOP').touch()
    with (root/'out/supervisor-stop.json').open('w') as f:
        result=operator(root,['./process-linux.py','stop',str(root)],f,timeout=30)
    return result.returncode

def run_attempt(host,condition,attempt,arm,home,template,ledger,frozen):
    model,effort=PAIRS[condition]
    root=Path('[path omitted]')/(host+'-'+condition+('' if attempt==1 else '-replacement-1'))
    q=quota(home)
    append(ledger,dict(phase='quota',host=host,condition=condition,attempt=attempt,quota=q))
    if tree_sha(template)!=frozen['full_tree_sha256']: raise RuntimeError('frozen template changed')
    if root.exists(): raise RuntimeError('refusing to reuse '+str(root))
    subprocess.run(['cp','-a',str(template),str(root)],check=True)
    (root/'MODEL').write_text(model+'\n'); (root/'EFFORT').write_text(effort+'\n')
    subprocess.run(['chown','-R','operator:operator',str(root)],check=True)
    planned=(int(time.time())//60+3)*60
    record=dict(host=host,condition=condition,attempt=attempt,run_dir=str(root),arm=arm,model=model,effort=effort,
                rule_sha256=RULE_SHA,template_sha=frozen,quota_before=q,planned_start_epoch=planned,
                planned_start_utc=utc(planned),planned_deadline_epoch=planned+3600)
    append(ledger,dict(phase='launch',**record))
    save(Path('/root/l1/current-'+host+'.json'),record)
    with (root/'out/l1-launch.txt').open('w') as log:
        launched=operator(root,['./start.sh','60',arm,'5','NOLOCK',str(planned)],log,timeout=600)
    start=int((root/'START').read_text()) if (root/'START').exists() else None
    deadline=int((root/'DEADLINE').read_text()) if (root/'DEADLINE').exists() else planned+3600
    offsets={}; quota_events=[]; paused=set(); resume_at=None; grace_exceeded=False
    if launched.returncode==0:
        append(ledger,dict(phase='started',start_epoch=start,deadline_epoch=deadline,**record))
        while not (root/'DONE').exists():
            now=time.time()
            messages=refusal(root,arm,offsets)
            if messages:
                quota_events.append(dict(epoch=int(now),messages=messages))
                if resume_at is None:
                    paused=driver_processes(root); send(paused,signal.SIGSTOP); resume_at=now+600
                    append(ledger,dict(phase='quota_refusal',host=host,condition=condition,attempt=attempt,
                                      infrastructure_affected=True,retry_not_before_epoch=int(resume_at),errors=messages))
            if resume_at is not None and now>=min(resume_at,deadline):
                send(paused,signal.SIGCONT); paused=set(); resume_at=None
                append(ledger,dict(phase='quota_retry_released',host=host,condition=condition,attempt=attempt))
            if now>deadline+600:
                grace_exceeded=True; send(paused,signal.SIGCONT); paused=set(); safe_stop(root); break
            time.sleep(2)
    send(paused,signal.SIGCONT)
    leftovers=driver_processes(root)
    if leftovers: safe_stop(root)
    if driver_processes(root): raise RuntimeError('live arm remains; refusing overlap')
    final=root/'snapshots/FINAL'
    final_complete=(final/'SNAPSHOT_COMPLETE').exists() and (final/arm).is_dir()
    taken=float((final/'TAKEN_EPOCH').read_text()) if (final/'TAKEN_EPOCH').exists() else time.time()
    terminal=min(deadline,taken)
    for marker in (root/('STOP-'+arm),root/('ARM-DONE-'+arm)):
        if marker.exists(): terminal=min(terminal,marker.stat().st_mtime)
    stats=stream_stats(root,arm,terminal)
    quota_affected=bool(quota_events) or any(QUOTA.search(m) for m in stats['model_errors'])
    cap_hit=start is not None and taken>=deadline
    abnormal=(launched.returncode!=0 or grace_exceeded or any(code not in (0,130,137,143) for code in stats['process_exit_codes']) or (not cap_hit and not (root/('STOP-'+arm)).exists()
              and (root/('ARM-DONE-'+arm)).exists() and bool(stats['model_errors'])))
    flags=[]; infra=[]
    if not final_complete: flags.append('missing_FINAL_snapshot')
    if abnormal: flags.append('abnormal_process_exit')
    if cap_hit: flags.append('wall_cap_hit')
    if launched.returncode: infra.append('harness_launch_failed')
    if grace_exceeded: infra.append('DONE_grace_exceeded')
    if quota_affected: infra.append('quota_or_rate_limit_refusal')
    if any(PROVIDER.search(m) for m in stats['model_errors']): infra.append('provider_transport_error')
    if launched.returncode==0 and stats['successful_commands']==0: infra.append('agent_executed_no_successful_commands')
    with (root/'out/receipts-check.txt').open('w') as log:
        receipt=operator(root,['./receipts.py'],log,timeout=120)
    receipts=(root/'out/receipts.tsv').read_text().splitlines()[1:] if (root/'out/receipts.tsv').exists() else []
    pair_check=receipt.returncode==0 and bool(receipts) and all(row.split('\t')[2:]==[model,effort] for row in receipts)
    if not pair_check: infra.append('model_effort_receipt_check_failed')
    tokens=usage(root,arm,home,terminal)
    (root/'out'/('tokens-final-'+arm+'.txt')).write_text(' '.join(str(tokens['totals'][k]) for k in FIELDS)+'\n')
    done_epoch=int((root/'DONE').stat().st_mtime) if (root/'DONE').exists() else 'NA'
    summary=dict(record,start_epoch=start or 'NA',deadline_epoch=deadline,DONE_epoch=done_epoch,
                 termination_epoch=terminal,wall_seconds=max(0,terminal-start) if start else 'NA',
                 launch_exit_status=launched.returncode,receipts_pair_check=pair_check,
                 receipt_pairs=[row.split('\t')[2:] for row in receipts],token_usage=tokens,
                 cap_hit=cap_hit,abnormal_exit=abnormal,failure_flags=flags,infrastructure_affected=bool(infra),
                 infrastructure_flags=infra,quota_refusals=quota_events,
                 completed_commands=stats['completed_commands'],successful_commands=stats['successful_commands'],
                 build_test_proxy=stats['build_test_proxy'],missing_or_unscorable_final=not final_complete,
                 process_exit_codes=stats['process_exit_codes'],
                 model_error_count=len(stats['model_errors']),
                 snapshots=[dict(label=p.name,complete=(p/'SNAPSHOT_COMPLETE').exists()) for p in (root/'snapshots').iterdir()] if (root/'snapshots').exists() else [])
    # Classification is committed before any scoring starts.
    save(root/'out/l1-summary.json',summary)
    append(ledger,dict(phase='run_complete',**summary))
    removed=remove_ephemeral(root,arm)
    append(ledger,dict(phase='disk_cleanup',host=host,condition=condition,attempt=attempt,
                       removed=removed,retained_snapshots=['T+030m','FINAL','TARGET if present']))
    return summary

def score_run(summary,ledger):
    root=Path(summary['run_dir']); arm=summary['arm']
    if driver_processes(root): raise RuntimeError('refusing score with live arm')
    results={}; detail={}
    for metric in ('FINAL','T+030m'):
        label=metric; midpoint=root/'snapshots/T+030m'
        if metric=='T+030m' and not (midpoint/'SNAPSHOT_COMPLETE').exists() and summary['wall_seconds']!='NA' and summary['wall_seconds']<1800:
            label='FINAL'
        output=root/'out'/('final-'+arm+'.txt' if metric=='FINAL' else 't030-'+arm+'.txt')
        snapshot=root/'snapshots'/label
        if not (snapshot/'SNAPSHOT_COMPLETE').exists() or not (snapshot/arm).is_dir():
            rc=2; count=0; output.write_text('0\n'); reason='missing snapshot'
        elif metric=='T+030m' and label=='FINAL' and 'FINAL' in results:
            rc=detail['FINAL']['exit_status']; count=results['FINAL']; output.write_text(str(count)+'\n'); reason='early terminal FINAL fallback'
        else:
            with output.open('w') as stream, (root/'out'/('l1-score-'+metric+'-'+arm+'.stderr')).open('w') as err:
                command=['runuser','-u','operator','--','/usr/bin/env','PYTHONDONTWRITEBYTECODE=1','/bin/bash','-c',
                         'cd "$1"; exec ./score-one.sh "$2" "$3"','l1',str(root),label,arm]
                try: rc=subprocess.run(command,stdout=stream,stderr=err,timeout=14400).returncode
                except subprocess.TimeoutExpired: rc=124
            text=output.read_text().strip()
            count=int(text) if rc==0 and text.isdigit() else 0
            if not 0<=count<=106: raise RuntimeError('invalid /106 score')
            reason='offline frozen scorer' if rc==0 else 'unscorable snapshot; rule assigns 0/106'
        results[metric]=count
        detail[metric]=dict(source_snapshot=label,exit_status=rc,passes=count,total=106,reason=reason)
    update=dict(summary,FINAL_passes=results['FINAL'],T030_passes=results['T+030m'],score_denominator=106,score_detail=detail,
                report_cell_as_missing=summary['infrastructure_affected'] and summary['attempt']==2)
    save(root/'out/l1-summary.json',update)
    append(ledger,dict(phase='scored',**update))
    return update

def main(host_short):
    arm,home_raw,order=CONFIG[host_short]; home=Path(home_raw); host='kogen-operator-'+host_short
    state=Path('/root/l1'); state.mkdir(exist_ok=True)
    lock=(state/('runner-'+host+'.lock')).open('w'); fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if hashlib.sha256((state/'L1-RULE.md').read_bytes()).hexdigest()!=RULE_SHA: raise RuntimeError('rule hash mismatch')
    expected_order=('EU-elixir seed=20261011 order: ' if host_short=='eu' else 'US-go seed=20261012 order: ')+' -> '.join(order)
    if expected_order not in (state/'ORDER.txt').read_text().splitlines(): raise RuntimeError('ORDER.txt mismatch')
    ledger=state/('ledger-'+host+'.jsonl')
    if ledger.exists(): raise RuntimeError('ledger exists; refusing duplicate experiment')
    template=Path('[path omitted]')
    assert (template/'ARMS').read_text().strip()==arm and (template/'MODE').read_text().strip()=='sealed'
    assert (template/'CODEX_HOME').read_text().strip()==str(home)
    frozen=dict(full_tree_sha256=tree_sha(template),excluding_inputs_sha256=tree_sha(template,True))
    expected=json.loads((state/('expected-template-'+host_short+'.json')).read_text())['template']
    if frozen['full_tree_sha256']!=expected['full_tree_sha256'] or frozen['excluding_inputs_sha256']!=expected['excluding_inputs_sha256']:
        raise RuntimeError('template differs from frozen preparation record')
    save(state/('template-'+host+'.json'),frozen)
    append(ledger,dict(phase='runner_started',host=host,arm=arm,order=order,template_sha=frozen,rule_sha256=RULE_SHA))
    summaries=[]
    for condition in order:
        first=run_attempt(host,condition,1,arm,home,template,ledger,frozen); summaries.append(first)
        if first['infrastructure_affected']:
            # One replacement maximum. A refused request never causes a usage
            # threshold pause; actual refusals receive the requested 10-min wait.
            if first['quota_refusals']:
                until=first['quota_refusals'][-1]['epoch']+600
                while time.time()<until: time.sleep(min(10,until-time.time()))
            replacement=run_attempt(host,condition,2,arm,home,template,ledger,frozen); summaries.append(replacement)
    append(ledger,dict(phase='all_conditions_finished',host=host,attempts=len(summaries)))
    for summary in summaries: score_run(summary,ledger)
    after=dict(full_tree_sha256=tree_sha(template),excluding_inputs_sha256=tree_sha(template,True))
    assert after==frozen,'frozen template changed during experiment'
    append(ledger,dict(phase='runner_done',host=host,template_unchanged=True))

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in CONFIG: raise SystemExit('usage: l1_runner.py eu|us')
    main(sys.argv[1])
