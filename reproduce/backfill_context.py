#!/usr/bin/env python3
"""Offline context reconstruction from sanitized host metadata and public receipts.
No deployment, grading, transcript, credential, remote Git or sealed readers.
"""
import argparse, copy, hashlib, json, re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from build_records import ROOT, PHASES, safe
from export_results import round_tag
from missing_reasons import compact_value, expand_value, load_legend, load_marker_to_code
from partitioned_jsonl import read_partitions, write_partitions

GROUPS=('timestamps','circumstances','environment','setup')
MISSING_CODES=load_legend()
def missing(reason,source='none'):return {'missing':reason,'reconstructable_from':source}
def upgrade(v):
    expanded=expand_value(v,MISSING_CODES)
    def walk(value):
        if isinstance(value,dict):
            if 'missing' in value:return {**value,'reconstructable_from':value.get('reconstructable_from','none')}
            return {k:walk(x) for k,x in value.items()}
        if isinstance(value,list):return [walk(x) for x in value]
        return value
    return walk(expanded)
def utc(v):
    try:
        if isinstance(v,(int,float)):return datetime.fromtimestamp(v/1000,timezone.utc).isoformat().replace('+00:00','Z')
        d=datetime.fromisoformat(v.replace('Z','+00:00'))
        if d.tzinfo is None:return missing('Timestamp has no timezone receipt')
        return d.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
    except (ValueError,TypeError,AttributeError):return missing('Absolute UTC boundary was not emitted')
def number(v,reason):return v if isinstance(v,(int,float)) and not isinstance(v,bool) and v>=0 else missing(reason)
def blank_boundary():return {k:missing('Absolute phase boundary not retained') for k in ('start_utc','end_utc')}
def withheld(reason):return {'withheld':reason}
def hide_if_reported(value,reason):
    return value if isinstance(value,dict) and ('missing' in value or 'not_applicable' in value or 'withheld' in value) else withheld(reason)
def defaults(r):
    r=upgrade(r);r['schema_version']='1.2'
    for key,reason in {
        'spec_ref':'Host specification references are withheld from public records',
        'cpu':'Host CPU model is withheld from public records',
        'vcpu':'Host CPU allocation is withheld from public records',
        'ram_gib':'Host memory capacity is withheld from public records',
        'os':'Host operating-system details are withheld from public records',
        'kernel':'Host kernel details are withheld from public records',
    }.items():r['host'][key]=hide_if_reported(r['host'].get(key),reason)
    r.setdefault('timestamps',{'cell':blank_boundary(),'phases':{p:blank_boundary() for p in PHASES},'attempts':missing('Attempt boundary receipts unavailable')})
    r.setdefault('circumstances',{**{k:missing('Boundary telemetry not retained') for k in ['load1_start','load1_end','concurrent_cells_start','concurrent_cells_end','cap_start','cap_end']},'queue':missing('Queue receipt unavailable'),'dispatcher_id':missing('Dispatcher receipt unavailable'),'incidents':missing('Cell interval unavailable for incident overlap audit'),'load_samples':missing('No matching controller samples retained')})
    r.setdefault('environment',{'os':copy.deepcopy(r['host']['os']),'kernel':copy.deepcopy(r['host']['kernel']),'cpu_model':copy.deepcopy(r['host']['cpu']),'cores':copy.deepcopy(r['host']['vcpu']),'ram_gib':copy.deepcopy(r['host']['ram_gib']),'toolchains':copy.deepcopy(r['tools']['toolchains']),'network':{'profile':copy.deepcopy(r['sandbox']['egress_profile']),'allowlist_hosts':copy.deepcopy(r['sandbox']['egress_allow'])},'account_class':missing('No dated account-class receipt')})
    for key,reason in {
        'os':'Host operating-system details are withheld from public records',
        'kernel':'Host kernel details are withheld from public records',
        'cpu_model':'Host CPU model is withheld from public records',
        'cores':'Host core count is withheld from public records',
        'ram_gib':'Host memory capacity is withheld from public records',
    }.items():r['environment'][key]=hide_if_reported(r['environment'].get(key),reason)
    r.setdefault('setup',{'task_base':copy.deepcopy(r['task']['base_revision']),'adapter_harness_sha':copy.deepcopy(r['tools']['harness']),'sandbox_mode':copy.deepcopy(r['sandbox']['profile']),'sandbox_profile_sha256':copy.deepcopy(r['sandbox']['profile_sha256']),'deps_source':missing('Dependency source not pinned per cell'),'kogen_sha':copy.deepcopy(r['tools']['kogen'])})
    return r

def public_manifest(p,venue):
    m=json.loads(p.read_text());keep={k:m.get(k) for k in ['cell_id','experiment','harness','requested','observed','started_at','ended_at','timestamps','host','sandbox','workdir','wrapper','cli_version','runner','status','usage','wall_s','total_wall_s_all_attempts']}
    keep.update(alias=p.parent.name,venue=venue,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source='pulled-manifests/'+p.parent.name,attempt_boundaries=[])
    # Read native public timing receipts only, never a model transcript.
    keep['phase_boundaries']=defaultdict(list)
    for a in p.parent.glob('attempt-*/attempt.json'):
        z=json.loads(a.read_text());keep['attempt_boundaries'].append({k:z.get(k) for k in ['n','started_at','ended_at']})
    for e in p.parent.glob('attempt-*/kogen-out/events.jsonl'):
        for line in e.read_text().splitlines():
            try:z=json.loads(line)
            except ValueError:continue
            if z.get('event')!='phase_timing':continue
            phase={'setup:task-setup':'setup','gate_run':'gate'}.get(z.get('name'))
            if phase and z.get('started_at') is not None and z.get('finished_at') is not None:keep['phase_boundaries'][phase].append({'start_utc':utc(z['started_at']),'end_utc':utc(z['finished_at'])})
    # Profile is a public isolation artifact. Only retain its fingerprint.
    profiles=list(p.parent.glob('attempt-*/sandbox.sb'))
    if profiles:keep['profile_sha256']=hashlib.sha256(profiles[-1].read_bytes()).hexdigest()
    return keep

def empty_record(template,m,cid,task,arm,round_hint=None):
    def clear(v):
        if isinstance(v,dict) and not ('missing' in v or 'not_applicable' in v):return {k:clear(x) for k,x in v.items()}
        return missing('Not available for ungraded delivery')
    r=clear(template)
    owning_alias=re.sub(r'-r[0-9]+(?=-(?:r|lr)[0-9])','',cid) if m['venue']=='studio' else cid
    rid=round_tag(round_hint or owning_alias,m.get('experiment') or '')
    # Alias carries round suffix for Studio deliveries, even when native cell_id does not.
    if rid=='unmapped':rid=round_tag(m.get('alias',''),m.get('experiment') or '')
    r.update(schema_version='1.2',audit_round=rid,round_id=rid if rid!='unmapped' else missing('No unambiguous owning round tag'),cell_id=cid,graded=False)
    r['task']['id']=task if task else missing('Task identity not retained');r['arm']=arm if arm else missing('Arm label not retained')
    r['harness']=m.get('harness') or missing('Harness not retained');req=m.get('requested') or {};obs=m.get('observed') or {}
    r['model']={'requested':safe(req.get('model')),'effective':safe(','.join(sorted(obs.get('models',{}))))}
    r['effort']={'requested':safe(req.get('effort')),'runner_requested':safe(req.get('effort')),'effective':safe(obs.get('effort'))}
    r['host']['id']=m['venue'];r['host']['os']=safe((m.get('host') or {}).get('platform'))
    r['tools']['harness']=safe((m.get('wrapper') or {}).get('sha256'));r['tools']['toolchains']['python']=safe((m.get('host') or {}).get('python'))
    if m.get('harness')=='codex':r['recipe']='direct';r['tools']['codex_cli']=safe(m.get('cli_version'))
    kogen=str(m.get('harness','')).startswith(('kogen','kgn'))
    if not kogen:
        r['tools']['kogen']={'not_applicable':'Harness does not use Kogen'};r['kogen']={k:{'not_applicable':'Harness does not use Kogen'} for k in r['kogen']}
    r['outcome']=missing('No official grade in the public snapshot','not re-derivable from the public record')
    r['grade']={k:missing('No official grade in the public snapshot','not re-derivable from the public record') for k in r['grade']}
    r['itt']={'class':missing('Ungraded delivery needs evidence audit'),'evidence_ref':missing('No audited ITT receipt'),'cohort':'smoke-control' if re.search(r'smoke|control|noop',cid) else missing('No captured cohort launch receipt')}
    r['stop_reason']={'ok':'completed','timeout':'timeout'}.get(m.get('status'),missing('No normalized stop receipt'))
    r['timing']['total_wall_s']=number(m.get('total_wall_s_all_attempts',m.get('wall_s')),'Wall counter unavailable');r['timing']['timeout_cap_s']=number((m.get('runner') or {}).get('timeout_s'),'Timeout receipt unavailable')
    for k in r['tokens']['total']:r['tokens']['total'][k]=number((m.get('usage') or {}).get(k),'Usage counter unavailable')
    r['provenance']={'ledger_sha256':template['provenance']['ledger_sha256'],'manifest_sha256':m.get('sha256') or missing('Manifest unavailable'),'source_ref':'reproduce/inputs/ungraded-evidence/index.json'}
    return upgrade(r)

def enrich(r,m,state,events,samples,round_docs):
    r=defaults(r);c=r['circumstances'];ts=r['timestamps'];env=r['environment'];setup=r['setup'];h=m.get('host') or {};sb=m.get('sandbox') or {};eg=sb.get('egress') or {}
    start=m.get('started_at') or state.get('start');end=m.get('ended_at') or state.get('end')
    ts['cell']={'start_utc':utc(start),'end_utc':utc(end) if end else missing('End boundary absent; delivery may be active or receipt lost','Completion manifest or dispatcher END')}
    attempts=m.get('attempt_boundaries') or []
    if attempts:ts['attempts']=[{'attempt':a.get('n') or missing('Attempt number unavailable'),'start_utc':utc(a.get('started_at')),'end_utc':utc(a.get('ended_at'))} for a in attempts]
    for phase,bs in m.get('phase_boundaries',{}).items():
        if bs and all(isinstance(b[k],str) for b in bs for k in ('start_utc','end_utc')):ts['phases'][phase]={'start_utc':min(b['start_utc'] for b in bs),'end_utc':max(b['end_utc'] for b in bs)}
    if m.get('harness')=='codex':
        native=m.get('timestamps') or {};ts['phases']['develop']={'start_utc':utc(native.get('run_started_at')),'end_utc':utc(native.get('run_ended_at'))}
    # Grade timestamp alone supplies neither grade start nor exact end receipt.
    c['load1_start']=number(h.get('load_avg'),'Manifest start load unavailable')
    for key,skey in [('concurrent_cells_start','conc_start'),('concurrent_cells_end','conc_end'),('cap_start','cap_start')]:
        if isinstance(state.get(skey),int):c[key]=state[skey]
    def distance(t):
        try:return abs((datetime.fromisoformat(t.replace('Z','+00:00'))-datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds())
        except (ValueError,AttributeError):return 1e20
    starts=[e for e in events if e['event'] in ('START','start','launch') and distance(e['timestamp'])<=120]
    if starts:
        event=min(starts,key=lambda x:distance(x['timestamp']));v=event['values']
        for key,k in [('cap_start','cap'),('concurrent_cells_start','conc')]:
            if k in v:c[key]=int(float(v[k]))
        # running/active count is sampled BEFORE adding this cell; scope is stated below.
        if 'conc' not in v:
            n=v.get('running',v.get('active'))
            if n is not None:
                c['concurrent_cells_start']=missing('Launch running/active counter is block-scoped; host concurrency not emitted')
                if event['source'].startswith(('dispatch:r71:host-','dispatch:r67b:','dispatch:r65:','dispatch:r65b:')):c['concurrent_cells_start']=int(float(n))+1
        if 'load' in v:c['load1_start']=float(v['load'])
        c['queue']=state.get('block') or event['source'].split(':',1)[0]
        c['dispatcher_id']='studio-dispatcher' if m['venue']=='studio' else ('worker-r53b-dispatcher' if event['source'].startswith('dispatch:r53b:') and event['timestamp']>='2026-10-04T10:40' else 'worker-block-dispatcher')
    if starts and event['source'].startswith('dispatch:r71:host-'):c['dispatcher_id']='worker-r71-host-dispatcher'
    if starts and event['source'].startswith('dispatch:r67b:'):c['dispatcher_id']='worker-r67b-host-dispatcher'
    if starts and event['source'].startswith(('dispatch:r65:','dispatch:r65b:')):c['dispatcher_id']='worker-r65-host-dispatcher'
    if state:
        c['queue']=state.get('block') or 'studio queue';c['dispatcher_id']='studio-dispatcher'
    endevents=[e for e in events if e['event']=='END']
    if endevents and 'conc_at_end' in endevents[-1]['values']:c['concurrent_cells_end']=int(endevents[-1]['values']['conc_at_end'])
    # Periodic controller samples are exported with their times, never substituted at boundaries.
    if m['venue']=='studio' and isinstance(start,str):
        matches=[x for x in samples if start[:19]<=x['timestamp_utc'][:19]<=(end or '2026-10-05T23:59:59')[:19]]
        if matches:c['load_samples']=matches
    # Public records keep venue IDs and tool versions; machine and OS specifications are withheld.
    env['toolchains']=copy.deepcopy(r['tools']['toolchains']);env['network']={'profile':safe(eg.get('mode')),'allowlist_hosts':[x for x in eg.get('allow',[]) if isinstance(safe(x),str)] if isinstance(eg.get('allow'),list) else missing('Allowlist unavailable')}
    r['sandbox']['profile']=safe(sb.get('mode'));r['sandbox']['egress_profile']=env['network']['profile'];r['sandbox']['egress_allow']=env['network']['allowlist_hosts']
    setup['sandbox_mode']=r['sandbox']['profile'];setup['adapter_harness_sha']=r['tools']['harness']
    if m.get('sha256') and m.get('source') and not str(m['source']).startswith('pulled-manifests') and not m.get('profile_sha256'):
        setup['sandbox_profile_sha256']=missing('Public sandbox profile fingerprint not yet captured','Delivery attempt sandbox.sb on '+m['venue'])
        r['sandbox']['profile_sha256']=copy.deepcopy(setup['sandbox_profile_sha256'])
    base=(m.get('workdir') or {}).get('base_sha')
    if base:r['task']['base_revision']={'kind':'git-commit','hash':base}
    setup['task_base']=copy.deepcopy(r['task']['base_revision'])
    if m.get('profile_sha256'):setup['sandbox_profile_sha256']=m['profile_sha256'];r['sandbox']['profile_sha256']=m['profile_sha256']
    # Dated deployment receipts pin these exact adapters, not arbitrary root suffixes.
    pins={'kogen-plan-shell-ce7':'ce7b9dc7642b39d2a14c053a3814a7a5e2ca628d','kogen-escalate-shell-ce7':'ce7b9dc7642b39d2a14c053a3814a7a5e2ca628d','kogen-plan-shell-6e82':'6e826320bb4874a994d2a799b3d737f9b5400851','kogen-escalate-shell-6e82':'6e826320bb4874a994d2a799b3d737f9b5400851','kogen-planshell-provided':'1adf1bce16ad76e2a1a54d50ad081c587aeb6935','kogen-planshell-shaped':'1adf1bce16ad76e2a1a54d50ad081c587aeb6935'}
    if m.get('harness') in ('kogen-plan-shell','kogen-escalate-shell') and r['audit_round']=='r65':pins[m['harness']]='61514154b271f27296f6bd6538a4f810383942d2'
    if m.get('harness') in pins:
        r['tools']['kogen']=pins[m['harness']];setup['kogen_sha']=pins[m['harness']];setup['deps_source']='task-derived';env['toolchains']['elixir']='1.20.4';env['toolchains']['erlang']='29.1.1'
    # Account class is never inferred from a timestamp or a withheld operations source.
    incidents=[]
    incident_file=ROOT/'reproduce/inputs/incident-evidence.json'
    incident_data=json.loads(incident_file.read_text()) if incident_file.exists() else {}
    if r['cell_id'] in incident_data.get('r53b_excluded_first_attempts',[]):incidents.append('r53b-worker-overload (source not independently verifiable)')
    if incidents:c['incidents']=incidents
    return upgrade(r)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--metadata-dir',type=Path,required=True);ap.add_argument('--probe',type=Path,required=True);ap.add_argument('--controller-log',type=Path,required=True);a=ap.parse_args()
    rows=read_partitions(ROOT/'reproduce/inputs/run-evidence')[1];template=rows[0]
    hosts=[json.loads(p.read_text()) for p in sorted(a.metadata_dir.glob('*worker.json'))]+[json.loads((a.metadata_dir/'studio.json').read_text())]
    manifests={};states={};events=defaultdict(list);sources=[]
    for h in hosts:
        sources+=h['sources']
        for m in h['manifests']:
            parts=m.get('source','').split('/')
            if len(parts)==5 and parts[0]=='results':m['alias']=parts[2]
            if len(parts)==4 and parts[0]=='results':m['alias']=(m.get('cell_id') or parts[-2])+'-delivery-'+hashlib.sha256(m['source'].encode()).hexdigest()[:12]
            manifests[(h['venue'],m['alias'])]=m
        for st in h['states']:states[st['name']]=st
        for e in h['events']:events[(h['venue'],e['cell'])].append(e)
    samples=[]
    for s in a.controller_log.read_text().splitlines():
        t=re.match(r'(\S+)',s);v=dict(re.findall(r'(load1|pressure)=([0-9.]+)',s))
        if t and 'load1' in v:samples.append({'timestamp_utc':utc(t[1]),'load1':float(v['load1']),'pressure':int(v['pressure']) if 'pressure' in v else missing('Pressure not in controller sample')})
    samples.sort(key=lambda x:x['timestamp_utc']);used=set();facts=[];extras=[]
    # A surviving START is a delivery receipt even if its manifest was deleted.
    for (venue,alias),evs in events.items():
        starts=[e for e in evs if e['event'] in ('START','start','launch') and '2026-09-28'<=e['timestamp']<'2026-10-06']
        if starts and (venue,alias) not in manifests:
            manifests[(venue,alias)]={'alias':alias,'venue':venue,'started_at':starts[0]['timestamp'],'ended_at':next((e['timestamp'] for e in reversed(evs) if e['event']=='END'),None),'source':starts[0]['source'],'cell_id':states.get(alias,{}).get('cell_id'),'harness':states.get(alias,{}).get('harness')}
    for alias,st in states.items():
        if st.get('start') and '2026-09-28'<=st['start']<'2026-10-06' and ('studio',alias) not in manifests:
            manifests[('studio',alias)]={'alias':alias,'venue':'studio','started_at':st['start'],'ended_at':st.get('end'),'source':'maclane/state','harness':st.get('harness'),'cell_id':st.get('cell_id')}
    for r in rows:
        cid=r['cell_id'];p=a.probe/'results'/cid/'manifest.json';venue=r['host']['id']
        m=public_manifest(p,venue) if p.is_file() else {}
        # Remote alias comes from the sandbox profile, not fuzzy task/rep matching.
        if p.is_file():
            original=json.loads(p.read_text());profile=(original.get('sandbox') or {}).get('profile','');z=re.search(r'/results/([^/]+)/',profile)
            alias=z[1] if z and venue=='studio' else cid;m['alias']=alias
        else:alias=cid
        remote=manifests.get((venue,alias))
        if not remote and not p.is_file():
            candidates=[v for (host,_),v in manifests.items() if host==venue and v.get('cell_id')==cid]
            if len(candidates)==1:remote=candidates[0];alias=remote['alias']
        if remote:
            used.add((venue,alias));m={**remote,**m,'source':remote['source'],'phase_boundaries':m.get('phase_boundaries') or remote.get('phase_boundaries',{}),'attempt_boundaries':m.get('attempt_boundaries') or remote.get('attempt_boundaries',[])}
        if m:
            used.add((venue,alias));out=enrich(r,m,states.get(alias,{}),events.get((venue,alias),events.get((venue,cid),[])),samples,'')
        else:out=defaults(r)
        facts.append({'cell_id':cid,**{k:out[k] for k in ['timestamps','circumstances','environment','setup','task','host','tools','sandbox']}})
    known=set(r['cell_id'] for r in rows)
    for (venue,alias),m in sorted(manifests.items()):
        if (venue,alias) in used or alias in known:continue
        cid=alias.replace('kogen-bench-us','us-worker').replace('kogen-bench-eu','eu-worker')
        if cid in known:continue
        st=states.get(alias,{});parts=(m.get('cell_id') or '').split('__');task=st.get('task') or (parts[4] if len(parts)>=6 else None)
        r=empty_record(template,m,cid,task,st.get('arm'),st.get('suffix'));r=enrich(r,m,st,events.get((venue,alias),[]),samples,'');extras.append(r);known.add(cid)
    folder=ROOT/'reproduce/inputs'
    round_by_cell={row.get('cell_id'):row.get('round_id') for row in rows if isinstance(row.get('cell_id'),str)}
    marker_to_code=load_marker_to_code()
    write_partitions(facts,folder/'context-evidence',round_for=lambda row:round_by_cell.get(row.get('cell_id')),transform=lambda row:compact_value(row,marker_to_code))
    write_partitions(extras,folder/'ungraded-evidence',round_for=lambda row:row.get('round_id') if isinstance(row.get('round_id'),str) else None,schema_field='schema_version',transform=lambda row:compact_value(row,marker_to_code))
    provenance={'date_window_start':'2026-09-28T00:00:00Z','date_window_end_exclusive':'2026-10-06T00:00:00Z','captured_at_utc':datetime.now(timezone.utc).isoformat(),'graded_records_enriched':len(facts),'additional_deliveries':len(extras),'host_inventory':{h['venue']:{'manifests':len(h['manifests']),'events':len(h['events']),'latest_manifest_start_utc':max((m.get('started_at') or '' for m in h['manifests']),default='unavailable')} for h in hosts},'sources':sources,'controller_log_sha256':hashlib.sha256(a.controller_log.read_bytes()).hexdigest(),'scope':'Read-only manifests at bounded public results depths, Studio status/state/queue and worker launch events. Retained and pulled artifacts only; deleted deliveries without logs cannot be recreated. Hardware spot checks are not projected backward. No raw egress, identities, private paths, model transcripts or grader material exported.'}
    controller_state=a.controller_log.parent/'ctl_state.json'
    if controller_state.is_file():provenance['controller_state_sha256']=hashlib.sha256(controller_state.read_bytes()).hexdigest()
    provenance['controller_state_note']='Inspected controller state; current cap/break receipts do not establish historical boundary load or all external cap changes.'
    provenance['evidence_indexes']=['reproduce/inputs/context-evidence/index.json','reproduce/inputs/ungraded-evidence/index.json']
    (folder/'context-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');print(json.dumps({k:provenance[k] for k in ['graded_records_enriched','additional_deliveries']}))
if __name__=='__main__':main()
