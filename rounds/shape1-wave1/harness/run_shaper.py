#!/usr/bin/env python3
"""Linux lane adapter. Default emits a command; launch requires explicit gates."""
import argparse
import hashlib
from datetime import datetime, timezone
import json
import platform
import re
import shlex
import subprocess
import time
import tarfile
from pathlib import Path
from shape_common import ROOT, LANGS, digest, fence, reserve_json, write_json
from linux_support import require_linux_gap

SAFE_ROWS=Path.home()/'Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py'
OLD_LANE='pre-RC old-descriptive'


def safe_json(path,keys=None):
    command=['python3',str(SAFE_ROWS),str(path)]
    if keys:command+=['--keys',','.join(keys)]
    return json.loads(subprocess.check_output(command,text=True))


def record_labels(lane):
    old=lane in ('old-descriptive',OLD_LANE)
    if lane not in ('strict','old-descriptive',OLD_LANE):raise ValueError('unknown lane')
    return {'lane':OLD_LANE if old else 'strict','strict_eligible':not old}


def required_host_gates(lane):
    if lane=='strict':
        return ('core4b_rep1_complete','ksub_complete','targeted_recheck_accepted',
            'bwrap_isolation','benchmark_only_codex_home','audit_controls',
            'strict_standard_dry','quiet_window','disk_admission','lane_watchdog_1800_600')
    if lane=='old-descriptive':
        return ('targeted_recheck_accepted','bwrap_isolation','benchmark_only_codex_home',
                'audit_controls','quiet_window','disk_admission')
    raise ValueError('unknown lane')


class TranscriptWatch:
    """Follow complete transcript events, retaining unfinished command IDs."""
    def __init__(self,path,now):
        self.path=Path(path);self.offset=0;self.pending=b'';self.last_event=now
        self.open_commands=set()

    def poll(self,now):
        if not self.path.exists():return
        if self.path.stat().st_size<self.offset:raise RuntimeError('transcript truncated')
        with self.path.open('rb') as stream:
            stream.seek(self.offset);chunk=stream.read();self.offset=stream.tell()
        self.pending+=chunk
        lines=self.pending.split(b'\n');self.pending=lines.pop()
        for line in lines:
            if not line.strip():continue
            event=json.loads(line)
            if not isinstance(event,dict) or not isinstance(event.get('type'),str):
                raise ValueError('malformed transcript event')
            self.last_event=now
            item=event.get('item') or {}
            if item.get('type')=='command_execution':
                key=item.get('id')
                if not key:raise ValueError('command event missing identity')
                if event['type']=='item.started':self.open_commands.add(key)
                elif event['type']=='item.completed':self.open_commands.discard(key)


def stop_old_unit(run_id):
    subprocess.run(['sudo','-n','systemctl','stop','bench-'+run_id],stdin=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,timeout=30)


def run_old_descriptive(command,run_id,transcript,result,clock=None,sleep=None,
                        stop_unit=None,popen=None,fence_process=None):
    """Outer old-lane watchdog; no RC watchdog/audit dependency or retry."""
    clock=clock or time.monotonic;sleep=sleep or time.sleep
    stop_unit=stop_unit or stop_old_unit;popen=popen or subprocess.Popen
    fence_process=fence_process or fence
    started=clock();watch=TranscriptWatch(transcript,started);reason='exit';stopped=False
    proc=None;infrastructure_failure=True;labels=record_labels('old-descriptive')
    try:
        with (result/'lane.stdout').open('wb') as out,(result/'lane.stderr').open('wb') as err:
            proc=popen(command,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
            try:
                while proc.poll() is None:
                    now=clock()
                    if (ROOT/'STOP').exists():reason='stop_latch'
                    elif now-started>=1800:reason='timeout'
                    else:
                        try:watch.poll(now)
                        except (OSError,ValueError,TypeError,AttributeError):reason='transcript_failure'
                        if reason=='exit' and now-watch.last_event>=600 and not watch.open_commands:
                            reason='stall'
                    if reason!='exit':
                        stop_unit(run_id);stopped=True;break
                    sleep(min(1,max(0,1800-(clock()-started))))
                try:proc.wait(timeout=120)
                except subprocess.TimeoutExpired:
                    if not stopped:stop_unit(run_id);stopped=True
                    reason='launcher_timeout'
            finally:
                # Always attempt the fence, even when stopping the unit fails.
                try:
                    if proc.poll() is None and not stopped:stop_unit(run_id);stopped=True
                finally:fence_process(proc)
        infrastructure_failure=False
    except Exception:
        reason='infrastructure_failure'
    finally:
        # Audit after cleanup on every path, including failed launch/stop/fence.
        try:
            audit=audit_events(transcript)
            if not Path(transcript).stat().st_size:
                audit={'flag_count':1,'flags':[{'reason':'empty transcript'}]}
        except Exception:
            audit={'flag_count':1,'flags':[{'reason':'missing/malformed transcript or audit failure'}]}
        if infrastructure_failure or audit['flag_count']:
            (ROOT/'STOP').write_text('old-descriptive infrastructure or transcript audit failure\n')
        write_json(result/'harness-audit.json',dict(audit,run_id=run_id,**labels))
        record=dict(labels,run_id=run_id,rc=2 if infrastructure_failure else proc.returncode,
                    stop_reason='infrastructure_failure' if infrastructure_failure else reason,
                    timeout=reason=='timeout',stall=reason=='stall',unit_stopped=stopped,
                    valid=not infrastructure_failure and not audit['flag_count'] and reason=='exit' and proc.returncode==0,
                    wall_seconds=round(clock()-started,3),audit_flags=audit['flag_count'])
        write_json(result/'old-lane-control.json',record)
    return record


def check_task_validation(gate,task,overlay_sha,registered,registration_sha):
    """Require validator evidence for this task, all arms, and these exact bytes."""
    from validate_mutants import completed, grade_complete
    try:
        entry=gate['tasks'][task]
        if (entry['task']!=task or entry['overlay_sha256']!=overlay_sha or
                entry['registration_sha256']!=registration_sha or
                any(entry[k]!='PASSED' for k in ('reference_validation','mutant_validation',
                                               'real_linux_isolation_integrity'))):
            raise ValueError('incomplete/stale task gate')
        evidence=(ROOT/entry['validation_file']).resolve()
        if (not evidence.is_relative_to((ROOT/'mutants'/task).resolve()) or
                not evidence.name.startswith('validation')):
            raise ValueError('missing validator evidence')
        # Never inspect grade-bearing validator receipts without safe_rows.
        exported=subprocess.run(['python3',str(SAFE_ROWS),str(evidence),'--keys',
            'schema,task,full_validation,expected_hidden_tests,hidden_snapshot,languages,exclusions'],
            capture_output=True,text=True,check=True)
        if hashlib.sha256(exported.stdout.encode()).hexdigest()!=entry['validation_safe_sha256']:
            raise ValueError('stale validator evidence')
        proof=json.loads(exported.stdout)
        expected=len(json.loads((ROOT/'behaviour-inventory.json').read_text())[task])
        if (proof['schema']!=2 or proof['task']!=task or proof['full_validation'] is not True or
                proof['expected_hidden_tests']!=expected or proof['hidden_snapshot']!=registered['hidden_snapshot']):
            raise ValueError('not current full Linux validation')
        catalog=json.loads((ROOT/'mutants'/task/'catalog.json').read_text())
        ids={m['id'] for m in catalog}
        for lang in LANGS:
            row=proof['languages'][lang];reference=row['reference']
            if (row['reference_validated'] is not True or not completed(reference['build']) or
                    not completed(reference['check']) or not grade_complete(reference['hidden'],expected,True)):
                raise ValueError('reference not validated in every arm')
            if set(row['mutants'])!=ids:raise ValueError('partial mutant validation')
            for mid in ids:
                mutant=row['mutants'][mid]
                if (mutant['patch_sha256']!=digest(ROOT/'mutants'/task/lang/(mid+'.patch')) or
                        mutant['reference_snapshot']!=registered['source_snapshots']['reference'][lang]):
                    raise ValueError('stale mutant validation')
                if mutant.get('validated') is True:
                    if not (completed(mutant['build']) and completed(mutant['check']) and
                            grade_complete(mutant['hidden'],expected,False)):
                        raise ValueError('incomplete mutant validation')
                else:
                    # Exclusions only count inside the hash-bound validator receipt;
                    # a manually added exclusion in LINUX-GATES is never consulted.
                    excluded=(proof.get('exclusions') or {}).get(lang,{}).get(mid,{})
                    if (excluded.get('by')!='validate_mutants.py' or
                            excluded.get('validator_sha256')!=digest(ROOT/'validate_mutants.py') or
                            not isinstance(excluded.get('reason'),str) or not excluded['reason'].strip()):
                        raise ValueError('mutant neither validated nor validator-excluded')
    except (OSError,ValueError,KeyError,TypeError,AttributeError,subprocess.SubprocessError):
        raise RuntimeError('task Linux validation/isolation gate missing, malformed, partial or stale') from None


def audit_events(path):
    flags=[]; commands=[]; usage=[]
    for number,line in enumerate(Path(path).read_text(errors='replace').splitlines(),1):
        try: event=json.loads(line)
        except ValueError:
            flags.append({'line':number,'reason':'malformed event'}); continue
        if not isinstance(event,dict) or not isinstance(event.get('item',{}),dict):
            flags.append({'line':number,'reason':'malformed event'});continue
        item=event.get('item',{})
        command=item.get('command','')
        if command and item.get('type')=='command_execution':
            commands.append(command)
            if re.search(r'(?i)(?:bench-sealed|(?:^|[/\s])hidden(?:[/\s]|$)|(?:^|[/\s])reference(?:[/\s]|$)|mutants)',command):
                flags.append({'line':number,'reason':'hidden-path command'})
        if event.get('usage'): usage.append(event['usage'])
    return {'flags':flags,'flag_count':len(flags),'flagged':len(flags),'commands':commands,'usage':usage}


def lane_command(task,lang,host):
    tasks={r['id'] for r in json.loads((ROOT/'plan.json').read_text())['tasks']}
    if task not in tasks or lang not in LANGS or host not in ('eu','us'):
        raise ValueError('unregistered task, language or host')
    rid=f's1-{host}-{task}-{lang}'
    return rid,['sudo','-n','/usr/bin/env','BENCH_CELL_SECONDS=1800','BENCH_STALL_SECONDS=600',
        '/usr/local/bin/bench-run-lane',f'shape-{task}-{lang}',rid,'gpt-6.1-sol','high']


def check_gates(host,task,lang,lane='strict'):
    require_linux_gap()
    if (ROOT/'STOP').exists(): raise RuntimeError('STOP latch set')
    registration=ROOT/'REGISTRATION-FIX-4.json'
    frozen=safe_json(registration)
    if any(digest(ROOT/k)!=v for k,v in frozen['files'].items()):
        raise RuntimeError('registration changed')
    gate=json.loads((ROOT/'LINUX-GATES.json').read_text()).get(host,{})
    needed=required_host_gates(lane)
    if gate.get('registration_sha256')!=digest(registration) or not all(gate.get(k) is True for k in needed):
        raise RuntimeError('Linux host gates incomplete; launch disabled')
    if lane=='old-descriptive':
        wave=[c for c in frozen['old_descriptive']['cells'] if c['host']==host]
        next_cell=next((c for c in wave if not (ROOT/'attempts'/f"{c['task']}-{c['language']}.json").exists()),None)
        if next_cell is None or (task,lang)!=(next_cell['task'],next_cell['language']):
            raise RuntimeError('cell is outside the next registered old-descriptive host slot')
    definition=Path('/benchmark-root/kits/current/tasks')/f'shape-{task}-{lang}'
    registered=next(t for t in json.loads((ROOT/'plan.json').read_text())['tasks'] if t['id']==task)
    overlay=ROOT/'overlays'/f'overlay-shape-{task}.tar'
    check_task_validation(gate,task,digest(overlay),registered,digest(registration))
    # Bind the installed public definition/bundle to the approved overlay too.
    with tarfile.open(overlay) as archive:
        expected=json.load(archive.extractfile(f'tasks/shape-{task}-{lang}/task.json'))
    installed=json.loads((definition/'task.json').read_text())
    if any(installed.get(k)!=expected[k] for k in ('base_sha','base_bundle_sha256',
            'prompt_sha256_original','source_snapshot_sha256')):
        raise RuntimeError('installed task does not match the validation-approved overlay')
    if digest(definition/'prompt.md')!=registered['shaping_prompt_sha256'][lang]:
        raise RuntimeError('installed shaping prompt does not match registration')
    from build_shape_tasks import STUB
    if (definition/'grader-entrypoint').read_bytes()!=STUB:
        raise RuntimeError('installed shape grader is not the registered non-scoring stub')


def main():
    p=argparse.ArgumentParser();p.add_argument('host',choices=('eu','us'))
    p.add_argument('task');p.add_argument('language',choices=LANGS)
    p.add_argument('--lane',choices=('strict','old-descriptive'),default='strict')
    p.add_argument('--launch',action='store_true');a=p.parse_args()
    rid,command=lane_command(a.task,a.language,a.host)
    if not a.launch:
        preview=command if a.lane=='strict' else [str(ROOT/'run_shaper.sh'),a.host,a.task,a.language,'--lane',a.lane,'--launch']
        print(shlex.join(preview)); return 0
    check_gates(a.host,a.task,a.language,a.lane)
    labels=record_labels(a.lane)
    result=ROOT/'results'/rid; result.mkdir(parents=True,exist_ok=False)
    # Global task/language latch enforces one replicate across hosts.
    reserve_json(ROOT/'attempts'/f'{a.task}-{a.language}.json',dict(run_id=rid,host=a.host,**labels))
    reserve_json(result/'launch.json',{'run_id':rid,'task':a.task,'language':a.language,
        'host':a.host,'registration_sha256':digest(ROOT/'REGISTRATION-FIX-4.json'),
        'preserved_repo':f'/benchmark-root/work/{rid}/repo','model':'gpt-6.1-sol','effort':'high',**labels})
    logfile=ROOT/'logs/launcher.log'; logfile.parent.mkdir(exist_ok=True)
    def log(phase,**fields):
        with logfile.open('a') as f:
            f.write(f'{phase} utc={datetime.now(timezone.utc).isoformat()} run_id={rid} '+
                    f'lane={labels["lane"]} strict_eligible={labels["strict_eligible"]} '+
                    ' '.join(f'{k}={v}' for k,v in fields.items())+'\n')
    start=time.monotonic();log('START')
    if a.lane=='old-descriptive':
        try:
            control=run_old_descriptive(command,rid,Path('/benchmark-root/results')/rid/'codex.jsonl',result)
        except (OSError,RuntimeError,ValueError,subprocess.SubprocessError):
            (ROOT/'STOP').write_text('old-descriptive launcher/stop/fence infrastructure failure\n')
            control=dict(labels,run_id=rid,rc=2,stop_reason='infrastructure_failure',
                         timeout=False,stall=False,audit_flags=None,unit_stopped=False)
            write_json(result/'old-lane-control.json',control)
        rc=control['rc']
    else:
        with (result/'lane.stdout').open('wb') as out,(result/'lane.stderr').open('wb') as err:
            proc=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        rc=proc.returncode
    elapsed=round(time.monotonic()-start,3);log('END',rc=rc,seconds=elapsed)
    write_json(result/'launcher-timing.json',{'rc':rc,'wall_seconds':elapsed,
        'lane_result':f'/benchmark-root/results/{rid}','preserved_repo':f'/benchmark-root/work/{rid}/repo',**labels})
    return rc if a.lane=='strict' or control['stop_reason']=='exit' and not control['audit_flags'] else 2


if __name__=='__main__': raise SystemExit(main())
