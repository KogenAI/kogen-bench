#!/usr/bin/env python3
"""Finalize a lane result directory into its Standard 1.2 per-cell record."""
from __future__ import annotations
import argparse, copy, hashlib, json, os, platform, re, stat, subprocess, sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit
from cost_calc import VERSION as CALCULATOR_VERSION, calculate as calculate_cost, table_sha256

ROOT = Path(__file__).resolve().parents[1]
SAFE_ROWS = Path.home() / 'Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py'
SCHEMA = json.loads((ROOT / 'schema/run-record.schema.json').read_text())
CURRENT = SCHEMA['$defs']['current']
MISSING = {'missing': 'm39'}
EMAIL_RE = re.compile(r'(?i)\b[a-z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-z0-9.-]+\.[a-z]{2,}\b')
HOME_PATH_RE = re.compile(r'(?i)(?<![a-z0-9])(?:~(?:[/\\][^\s,;)]*)?|/(?:Users|home)/[^\s,;)]*|/root(?:[/\\][^\s,;)]*)?|[a-z]:[/\\]Users[/\\][^\s,;)]*)')

def utc_now(): return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
def read_regular(path, max_bytes=16*1024*1024):
    fd=None
    try:
        fd=os.open(os.fspath(path),os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
        info=os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size>max_bytes: return None
        chunks=[]; total=0
        while True:
            block=os.read(fd,min(1024*1024,max_bytes-total+1))
            if not block: break
            chunks.append(block); total+=len(block)
            if total>max_bytes: return None
        return b''.join(chunks)
    except OSError:
        return None
    finally:
        if fd is not None: os.close(fd)

def is_regular_file(path, max_bytes=16*1024*1024):
    fd=None
    try:
        fd=os.open(os.fspath(path),os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
        info=os.fstat(fd)
        return stat.S_ISREG(info.st_mode) and info.st_size<=max_bytes
    except OSError:
        return False
    finally:
        if fd is not None: os.close(fd)

def manifest_hash_receipt(out):
    raw=read_regular(Path(out)/'manifest-sha256.txt',256)
    if not raw: return None
    value=raw.decode('ascii','ignore').strip()
    return value if re.fullmatch(r'[0-9a-f]{64}',value) else None

def skeleton(schema, example=False):
    if '$ref' in schema:
        ref=schema['$ref']; node=SCHEMA
        for part in ref[2:].split('/'): node=node[part.replace('~1','/').replace('~0','~')]
        return skeleton(node,example)
    if 'anyOf' in schema:
        if example:
            for branch in schema['anyOf']:
                if '$ref' not in branch or not any(x in branch['$ref'] for x in ('/missing','/withheld','/not_applicable')):
                    return skeleton(branch,example)
        for branch in schema['anyOf']:
            if '$ref' in branch and '/missing' in branch['$ref']: return MISSING.copy()
        return skeleton(schema['anyOf'][0],example)
    if schema.get('const') is not None: return schema['const']
    if 'enum' in schema: return schema['enum'][0] if example else MISSING.copy()
    typ=schema.get('type')
    if typ=='object': return {k:skeleton(v,example) for k,v in schema.get('properties',{}).items()}
    if typ=='array': return [skeleton(schema['items'],example)] if example and 'items' in schema else (MISSING.copy() if not example else [])
    if typ=='string': return ('2026-01-01T00:00:00Z' if schema.get('format')=='date-time' else 'synthetic') if example else MISSING.copy()
    if typ=='boolean': return False if example else MISSING.copy()
    if typ in ('integer','number'): return schema.get('minimum',1 if typ=='integer' else 0.0) if example else MISSING.copy()
    return MISSING.copy()

def set_path(obj,path,value):
    keys=path.split('.'); cur=obj
    for key in keys[:-1]: cur=cur.setdefault(key,{})
    cur[keys[-1]]=value

def overlay(dst,src):
    if isinstance(dst,dict) and isinstance(src,dict):
        if any(x in dst for x in ('missing','not_applicable','withheld')) and not any(x in src for x in ('missing','not_applicable','withheld')):
            dst.clear(); dst.update(src); return dst
        for k,v in src.items():
            if k in dst and isinstance(dst[k],dict) and isinstance(v,dict) and not any(x in v for x in ('missing','not_applicable','withheld')): overlay(dst[k],v)
            else: dst[k]=v
    return dst

def read_json(path):
    path=Path(path)
    if path.name in ('manifest.json','grade.json'):
        if not is_regular_file(path): return {}
        keys=('task,base_repo,base_revision,base_sha,model,effective_model,effort,effective_effort,graded,grade,runner_rc,timeout,stall,patch_error,grader_version,tests_ran,grade_timestamp,candidate_revision,kit_revision,grader_sha256,timeout_cap_s,plan,capture_failures,release_eligible,cell_start_utc,cell_end_utc' if path.name=='manifest.json' else 'pass_,tests_ran')
        try:
            result=subprocess.run([sys.executable,str(SAFE_ROWS),str(path),'--keys',keys],
                                  check=True,capture_output=True,text=True,timeout=8)
            return json.loads(result.stdout)
        except (OSError,ValueError,subprocess.SubprocessError):
            return {}
    raw=read_regular(path)
    try: return json.loads(raw.decode('utf-8')) if raw is not None else {}
    except (UnicodeError,ValueError): return {}

def public_ref(value):
    if not isinstance(value, str) or not value.strip(): return None
    value=value.strip()
    if EMAIL_RE.search(value) or HOME_PATH_RE.search(value): return None
    ssh=re.fullmatch(r'(?:ssh://)?git@([^:/]+)[:/]([^\s]+)',value)
    if ssh: value=ssh.group(1)+'/'+ssh.group(2)
    elif '://' in value:
        try:
            parsed=urlsplit(value)
            if not parsed.hostname or parsed.username or parsed.password: return None
            value=parsed.hostname.lower()+'/'+unquote(parsed.path).lstrip('/')
        except ValueError: return None
    if value.startswith(('/', '~')) or re.match(r'^[a-z]:[/\\]',value,re.I) or '\\' in value:
        return None
    parts=value.split('/')
    if not value or any(part in ('','.','..') for part in parts) or any(ch.isspace() for ch in value):
        return None
    return value

def sanitize_record(value, path=()):
    """Remove private path/email values from any captured record receipt."""
    if isinstance(value, dict):
        return {k:sanitize_record(v,path+(k,)) for k,v in value.items()}
    if isinstance(value, list):
        return [sanitize_record(v,path+(str(i),)) for i,v in enumerate(value)]
    if isinstance(value, str):
        if EMAIL_RE.search(value) or HOME_PATH_RE.search(value):
            if path in (('task','base_repo'),('provenance','source_ref'),('itt','evidence_ref'),
                        ('tools','harness'),('setup','deps_source')):
                return MISSING.copy()
            value=EMAIL_RE.sub('[redacted]',value)
            value=HOME_PATH_RE.sub('[local-path]',value)
    return value

def counter(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0: return None
    return value

def usage_counters(usage):
    details=usage.get('input_tokens_details') or {}
    output_details=usage.get('output_tokens_details') or {}
    cached=counter(usage.get('cached_input_tokens'))
    if cached is None: cached=counter(details.get('cached_tokens'))
    uncached=counter(usage.get('uncached_input_tokens'))
    total_input=counter(usage.get('input_tokens'))
    if uncached is None and total_input is not None and cached is not None:
        uncached=total_input-cached if cached<=total_input else None
    output=counter(usage.get('output_tokens'))
    reasoning=counter(usage.get('reasoning_tokens'))
    if reasoning is None: reasoning=counter(output_details.get('reasoning_tokens'))
    return {'input':uncached,'cached_input':cached,'output':output,'reasoning':reasoning}

def finalize(result_dir):
    out=Path(result_dir); manifest=read_json(out/'manifest.json'); receipts=read_json(out/'standard-receipts.json')
    rec=skeleton(CURRENT)
    rec['schema_version']='1.2'
    # Direct lane facts; identity is intentionally missing without a registered plan.
    rec['task']={'id':manifest.get('task',MISSING.copy()),'base_repo':manifest.get('base_repo',MISSING.copy()),'base_revision':manifest.get('base_revision',MISSING.copy())}
    rec['model']={'requested':manifest.get('model',MISSING.copy()),'effective':manifest.get('effective_model',MISSING.copy())}
    rec['effort']={'requested':manifest.get('effort',MISSING.copy()),'effective':manifest.get('effective_effort',MISSING.copy()),'runner_requested':manifest.get('effort',MISSING.copy())}
    rec['graded']=manifest.get('graded',False)
    gr=manifest.get('grade') or {}
    rec['outcome']=('pass' if gr.get('passed') is True else 'fail' if gr.get('passed') is False else MISSING.copy())
    rec['stop_reason']=('timeout' if manifest.get('timeout') else 'turn_limit' if manifest.get('stall') else 'harness_error' if manifest.get('patch_error') else 'completed' if manifest.get('runner_rc') == 0 else {'missing':'m31'})
    rec['grade']['grader']=manifest.get('grader_version',MISSING.copy())
    rec['grade']['tests_ran']=manifest.get('tests_ran',MISSING.copy())
    rec['grade']['timestamp']=manifest.get('grade_timestamp',MISSING.copy())
    rec['provenance']['manifest_sha256']=manifest_hash_receipt(out) or MISSING.copy()
    rec['timestamps']['cell']['start_utc']=manifest.get('cell_start_utc') or MISSING.copy()
    rec['timestamps']['cell']['end_utc']=manifest.get('cell_end_utc') or MISSING.copy()
    # Coordinator/harness may supply a schema-shaped authoritative receipt object.
    overlay(rec,receipts.get('record',receipts))
    plan=read_json(out/'plan.json') or manifest.get('plan',{})
    for key in ('round_id','audit_round','cell_id','arm','harness','recipe','itt','repetition'):
        if key in plan:
            target={'repetition':None}.get(key,key)
            if target and key=='itt': rec['itt'].update(plan[key])
            elif target: rec[target]=plan[key]
    if not plan:
        for key in ('round_id','audit_round','cell_id','arm','harness','recipe'):
            rec[key]=MISSING.copy()
        rec['itt']={'class':MISSING.copy(),'cohort':MISSING.copy(),'evidence_ref':MISSING.copy()}
    base_repo=public_ref(plan.get('base_repo')) or public_ref(manifest.get('base_repo'))
    rec['task']['base_repo']=base_repo if base_repo else MISSING.copy()
    base_revision=plan.get('base_revision',manifest.get('base_revision'))
    if isinstance(base_revision,str):
        base_revision={'kind':'git-commit','hash':base_revision}
    if not isinstance(base_revision,dict) and manifest.get('base_sha'):
        base_revision={'kind':'git-commit','hash':manifest['base_sha']}
    if isinstance(base_revision,dict) and base_revision.get('kind') in ('git-commit','tree-sha256') and isinstance(base_revision.get('hash'),str) and base_revision['hash']:
        canonical_base={'kind':base_revision['kind'],'hash':base_revision['hash']}
    else:
        canonical_base={'kind':MISSING.copy(),'hash':MISSING.copy()}
    rec['task']['base_revision']=copy.deepcopy(canonical_base)
    rec['setup']['task_base']=copy.deepcopy(canonical_base)
    effective_effort=plan.get('effective_effort') or manifest.get('effective_effort')
    if isinstance(effective_effort,str) and effective_effort:
        rec['effort']['effective']=effective_effort
    elif isinstance(manifest.get('effort'),str):
        # The launcher passes this exact value in the Codex CLI configuration.
        rec['effort']['effective']=manifest['effort']
    if isinstance(plan.get('effective_model'),str):
        rec['model']['effective']=plan['effective_model']
    if plan:
        rec['provenance']['source_ref']=plan.get('source_ref','plan receipt')
        if plan.get('dispatcher_id'): rec['circumstances']['dispatcher_id']=plan['dispatcher_id']
        if 'queue_position' in plan: rec['circumstances']['queue']=str(plan['queue_position'])
    # Kogen state is an explicit post-cell worktree observation.
    rec['kogen']={'landed':False,'best_candidate':manifest.get('candidate_revision') or MISSING.copy()}
    if receipts.get('record',{}).get('kogen'): rec['kogen']=receipts['record']['kogen']
    # Attribute every usage event to its own effective model before aggregating.
    events=[]
    codex_bytes=read_regular(out/'codex.jsonl',max_bytes=64*1024*1024)
    if codex_bytes is not None:
        for line in codex_bytes.decode('utf-8','replace').splitlines():
            try: e=json.loads(line)
            except ValueError: continue
            u=e.get('usage')
            if not isinstance(u,dict):
                response=e.get('response')
                u=response.get('usage') if isinstance(response,dict) else None
            if isinstance(u,dict): events.append((e,u))
    if events:
        per_event=[]
        effective_models=set()
        for event,u in events:
            counts=usage_counters(u)
            response=event.get('response') if isinstance(event.get('response'),dict) else {}
            event_model=u.get('model') or event.get('model') or response.get('model')
            if isinstance(event_model,str) and event_model: effective_models.add(event_model)
            per_event.append((event_model,counts))
        norm={}
        for name in ('input','cached_input','output','reasoning'):
            values=[counts[name] for _model,counts in per_event]
            norm[name]=sum(values) if all(value is not None for value in values) else MISSING.copy()
        rec['tokens']['phases']['develop']=norm
        for phase in ('setup','shape','plan','review','gate','grade'):
            rec['tokens']['phases'][phase]={k:0 for k in norm}
        for k in norm: rec['tokens']['total'][k]=norm[k]
        if len(effective_models)==1: rec['model']['effective']=next(iter(effective_models))
        elif len(effective_models)>1: rec['model']['effective']=MISSING.copy()
    else:
        rec['tokens']['phases']['develop']={k:MISSING.copy() for k in ('input','cached_input','output','reasoning')}
        rec['tokens']['total']={k:MISSING.copy() for k in ('input','cached_input','output','reasoning')}
    # Frozen plan and exact launch-time snapshots are independent receipts.
    snap=read_json(out/'launch-snapshot.json')
    if snap:
        for group in ('host','tools','sandbox','environment'):
            if group in snap: overlay(rec[group],snap[group])
        runner_sha=snap.get('tools',{}).get('runner')
        if runner_sha and manifest.get('kit_revision'):
            rec['tools']['runner']=f"kit={manifest['kit_revision']}; {runner_sha}"
    timing=read_json(out/'lane-timing.json'); phases=timing.get('phases',{})
    for phase in ('setup','shape','plan','develop','review','gate','grade'):
        receipt=phases.get(phase,{})
        if receipt.get('start'): rec['timestamps']['phases'][phase]['start_utc']=receipt['start']['utc']
        if receipt.get('end'): rec['timestamps']['phases'][phase]['end_utc']=receipt['end']['utc']
        if receipt.get('start') and receipt.get('end'):
            seconds=max(0,(receipt['end']['monotonic_ns']-receipt['start']['monotonic_ns'])/1e9)
            rec['timing']['phases_s'][phase]=seconds
    cell_start=phases.get('cell',{}).get('start'); cell_end=phases.get('cell',{}).get('end')
    if cell_start and cell_end:
        rec['timestamps']['cell']={'start_utc':cell_start['utc'],'end_utc':cell_end['utc']}
        rec['timestamps']['attempts']=[{'attempt':1,'start_utc':cell_start['utc'],'end_utc':cell_end['utc']}]
    if phases.get('develop',{}).get('start') and phases.get('develop',{}).get('end'):
        dev=phases['develop']; rec['timing']['total_wall_s']=max(0,(dev['end']['monotonic_ns']-dev['start']['monotonic_ns'])/1e9)
    if manifest.get('timeout_cap_s') is not None: rec['timing']['timeout_cap_s']=manifest['timeout_cap_s']
    # Grading facts identify this shipped path precisely; a grade is not inferred from rc.
    grade_obj=read_json(out/'grade.json')
    if grade_obj:
        rec['graded']=True
        if isinstance(grade_obj.get('pass_'),bool): rec['outcome']='pass' if grade_obj['pass_'] else 'fail'
        tests=grade_obj.get('tests_ran')
        if isinstance(tests,(int,float)): tests=tests>0
        rec['grade']['tests_ran']=tests if isinstance(tests,bool) else MISSING.copy()
        stamp=phases.get('grade',{}).get('end',{}).get('utc')
        if stamp: rec['grade']['timestamp']=stamp
        kitrev=manifest.get('kit_revision'); gradersha=manifest.get('grader_sha256')
        rec['grade']['grader']=f"Kogen task-local official grader via control-worker.py; kit={kitrev}; sha256={gradersha}" if kitrev and gradersha else MISSING.copy()
        rec['tools']['grader']=f"kit={kitrev}; control-worker.py sha256={gradersha}" if kitrev and gradersha else {'missing':'m77'}
    else:
        rec['graded']=False
    # Boundary monitor receipts; missing sensors stay explicit.
    samples=read_json(out/'boundary-samples.json')
    start=samples.get('start',{}); end=samples.get('end',{})
    for key,source in (('load1_start',start),('load1_end',end),('concurrent_cells_start',start),('concurrent_cells_end',end),('cap_start',start),('cap_end',end)):
        name={'load1_start':'load1','load1_end':'load1','concurrent_cells_start':'running_bench_units','concurrent_cells_end':'running_bench_units','cap_start':'cap','cap_end':'cap'}[key]
        value=source.get(name)
        if value is not None: rec['circumstances'][key]=value
    plan=read_json(out/'plan.json')
    if plan.get('queue_position') is not None: rec['circumstances']['queue']=str(plan['queue_position'])
    elif start.get('queue_position') is not None: rec['circumstances']['queue']=str(start['queue_position'])
    dispatcher=plan.get('launcher_sha256',start.get('dispatcher_id'))
    if dispatcher: rec['circumstances']['dispatcher_id']=dispatcher
    if any(k in manifest for k in ('stall','timeout','patch_error')):
        incidents=[]
        if manifest.get('stall'): incidents.append('stall receipt')
        if manifest.get('timeout'): incidents.append('timeout receipt')
        if manifest.get('patch_error'): incidents.append('patch_error receipt')
        rec['circumstances']['incidents']=incidents
    captured_samples=[{'timestamp_utc':x['timestamp_utc'],'load1':x.get('load1') if x.get('load1') is not None else MISSING.copy(),'pressure':x.get('pressure') if x.get('pressure') is not None else MISSING.copy()} for x in (start,end) if x.get('timestamp_utc')]
    if captured_samples: rec['circumstances']['load_samples']=captured_samples
    if snap:
        rec['setup']['sandbox_mode']='bubblewrap'
        rec['setup']['sandbox_profile_sha256']=snap.get('sandbox',{}).get('profile_sha256',MISSING.copy())
    # Public Kogen state is deliberately false until a separate landing receipt exists.
    rec['kogen']['landed']=False
    if manifest.get('candidate_revision'): rec['kogen']['best_candidate']=manifest['candidate_revision']
    # Price each event at its own effective model; output already contains reasoning.
    price_version='sha256:'+table_sha256()
    rec['cost']['calculator_version']=CALCULATOR_VERSION
    rec['cost']['price_table_version']=price_version
    rec['cost']['long_context_reconciled']=False
    cost_total=Decimal(0); cost_complete=bool(events); cost_flagged=False; cost_reasons=[]
    for model,counts in per_event if events else []:
        if not isinstance(model,str) or any(counts[k] is None for k in ('input','cached_input','output')):
            cost_complete=False
            cost_reasons.append('event model or required usage counter missing')
            continue
        result=calculate_cost(model,counts['input']+counts['cached_input'],counts['cached_input'],counts['output'])
        if result['usd'] is None:
            cost_complete=False
            cost_reasons.append(result['reason'] or 'event model is unpriced')
        else:
            cost_total+=result['usd']
            cost_flagged=cost_flagged or result['flagged']
    if cost_complete:
        rec['cost']['usd']=float(cost_total)
        rec['cost']['accounting']=(
            'API-equivalent estimate; Standard short-context rates; each usage event priced at its event model; '
            'reasoning is included in output; long-context status not reconciled'
        )
        if cost_flagged: rec['cost']['accounting']+='; declared third-party estimate flagged'
    else:
        rec['cost']['usd']={'missing':'m70'}
        rec['cost']['accounting']='incomplete: '+('; '.join(sorted(set(cost_reasons))) or 'usage events unavailable')
    if plan.get('round_id'):
        rec['round_id']=plan['round_id']; rec['audit_round']=plan['audit_round']; rec['cell_id']=plan['cell_id']
        rec['arm']=plan['arm']; rec['harness']=plan['harness']; rec['recipe']=plan['recipe']
        rec['itt']=plan['itt']; rec['provenance']['source_ref']=plan.get('source_ref','frozen plan')
        if plan.get('effective_effort'): rec['effort']['effective']=plan['effective_effort']
        if plan.get('ledger_sha256'): rec['provenance']['ledger_sha256']=plan['ledger_sha256']
        if plan.get('deps_source'): rec['setup']['deps_source']=plan['deps_source']
        if plan.get('adapter_harness_sha'): rec['setup']['adapter_harness_sha']=plan['adapter_harness_sha']
        if plan.get('harness_version'): rec['tools']['harness']=plan['harness_version']
        if plan.get('kogen_sha'): rec['tools']['kogen']=plan['kogen_sha']; rec['setup']['kogen_sha']=plan['kogen_sha']
    else:
        rec['provenance']['source_ref']='unplanned invocation; not release eligible'
    rep=plan.get('repetition')
    if rep is not None: rec['provenance']['source_ref']=f"{rec['provenance'].get('source_ref','frozen plan')}; repetition={rep}"
    if manifest.get('candidate_revision'): rec['kogen']['best_candidate']=manifest['candidate_revision']
    capture_failures=manifest.get('capture_failures')
    status=read_json(out/'capture-status.json')
    status_failures=status.get('failed',[]) if isinstance(status,dict) else []
    capture_failures=(capture_failures if isinstance(capture_failures,list) else [])+(
        status_failures if isinstance(status_failures,list) else [])
    if capture_failures:
        incidents=rec['circumstances'].get('incidents')
        if not isinstance(incidents,list): incidents=[]
        incidents.extend('capture_failed:'+str(item) for item in sorted(set(capture_failures)))
        rec['circumstances']['incidents']=incidents
    rec['provenance']['manifest_sha256']=manifest_hash_receipt(out) or MISSING.copy()
    rec=sanitize_record(rec)
    outpath=out/'standard.json'; outpath.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
    return rec

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('result_dir',type=Path); a=p.parse_args(); finalize(a.result_dir)
