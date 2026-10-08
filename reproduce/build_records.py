#!/usr/bin/env python3
"""Build standard records offline; --probe captures allowlisted public metadata read-only.
Never opens transcripts, patches, sealed files, caches, credentials or grader code.
"""
import argparse, hashlib, json, re
from pathlib import Path
from export_results import round_tag
from privacy import contains_private_path
from missing_reasons import expand_value, load_legend, load_marker_to_code, compact_value
from partitioned_jsonl import read_partitions, write_partitions
ROOT = Path(__file__).resolve().parents[1]
PHASES = ('setup','shape','plan','develop','review','gate','grade')
TOKENS = ('input','cached_input','output','reasoning')

def digest(data): return hashlib.sha256(data).hexdigest()
def missing(reason): return {'missing':reason}
def na(reason): return {'not_applicable':reason}
def read(path): return json.loads(path.read_text()) if path.is_file() else {}
def safe(value):
    if not isinstance(value,str) or not value: return missing('Not recorded in available public metadata')
    if re.search(r'@|/Users/|/home/|/tmp/|~\/|\b(?:\d{1,3}\.){3}\d{1,3}\b|resp_|[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}',value) or contains_private_path(value):
        return missing('Value withheld by PRIVATE.md')
    return value

def num(value): return value if isinstance(value,(int,float)) and not isinstance(value,bool) and value>=0 else missing('Numeric counter not recorded')
def boolean(value): return value if isinstance(value,bool) else missing('Boolean receipt not recorded')
def vector(source): return {t:num(source.get(t)) for t in TOKENS}

def capture(probe):
    """Snapshot derived facts only. Raw official grade files remain untouched."""
    raw=(probe/'grades/grades.final.jsonl').read_bytes()
    latest={}
    for line in raw.splitlines():
        if not line.strip():continue
        g=json.loads(line); cid=g['cell_id']
        if cid not in latest or str(g.get('graded_at',''))>=str(latest[cid].get('graded_at','')):latest[cid]=g
    meta=read(ROOT/'reproduce/inputs/cell-metadata.json'); tasks={t['id']:t for t in read(ROOT/'tasks/index.json')}
    evidence=[]
    for cid,g in sorted(latest.items()):
        # Exact pulled alias owns identity; never fuzzy-match a different repetition.
        d=probe/'results'/cid; mf=d/'manifest.json'; m=read(mf); md=meta.get(cid,{})
        requested=m.get('requested') or {}; observed=m.get('observed') or {}; extra=m.get('extra') or {}; usage=m.get('usage') or {}
        ku=extra.get('kogen_usage') or {}; report={}
        # COMPLETE is read only for public artifact integrity metadata; no listed file is opened.
        complete=read(d/'COMPLETE.json')
        if m.get('harness','').startswith(('kogen','kgn')):
            attempt_numbers=[int(p.name.split('-')[1]) for p in d.glob('attempt-*') if p.name.split('-')[-1].isdigit()]
            if attempt_numbers:
                out=d/f'attempt-{max(attempt_numbers)}'/'kogen-out'
                ku=read(out/'usage.json') or ku
                report=read(out/'report.json')
        harness=m.get('harness') or md.get('harness'); parts=cid.split('__')
        if not harness and len(parts)>=6:harness=parts[0]
        rid=round_tag(cid,m.get('experiment') or md.get('experiment',''))
        task_id=g.get('task'); task=tasks.get(task_id,{})
        # base_sha is the original git base. fresh_base_commit is a runner snapshot, not provenance.
        base=(m.get('workdir') or {}).get('base_sha')
        host={'us':'kogen-bench-us','eu':'kogen-bench-eu','studio':'studio','orchestrator-control':'orchestrator-control','us-worker':'kogen-bench-us','eu-worker':'kogen-bench-eu'}.get(str(g.get('host','')).lower())
        sandbox=m.get('sandbox') or {}; egress=sandbox.get('egress') or {}
        reqmodel=requested.get('model') or (parts[1] if len(parts)>=6 else None)
        reqeff=requested.get('effort') or (parts[2] if len(parts)>=6 else None)
        effmodel=','.join(sorted(observed.get('models',{}))) or None
        r={'schema_version':'1.0','audit_round':rid,'round_id':rid if rid!='unmapped' else missing('No unambiguous owning round tag'), 'cell_id':safe(cid),
           'task':{'id':safe(task_id),'base_repo':safe(task.get('base_repo')),'base_revision':{'kind':'git-commit' if base else missing('Original base revision type not recorded per cell'),'hash':safe(base) if base else missing('Original base commit/tree hash absent; fresh_base_commit is not a base hash')}},
           'arm':safe(g.get('arm')),'harness':safe(harness),'model':{'requested':safe(reqmodel),'effective':safe(effmodel)},'effort':{'requested':safe(reqeff),'effective':safe(observed.get('effort')),'runner_requested':safe(reqeff)},'recipe':safe(ku.get('recipe') or extra.get('kogen_recipe')),
           'host':{'id':safe(host),'spec_ref':missing('Host specifications are withheld from the public record'), 'cpu':missing('Host CPU model is withheld from the public record'),'vcpu':missing('Host CPU allocation is withheld from the public record'),'ram_gib':missing('Host memory capacity is withheld from the public record'),'os':missing('Host operating-system details are withheld from the public record'),'kernel':missing('Host kernel details are withheld from the public record')},
           'tools':{k:missing('Historical tool version not pinned in cell artifacts') for k in ['harness','kogen','codex_cli','runner','grader']},
           'sandbox':{'profile':safe(sandbox.get('mode')),'profile_sha256':missing('Sandbox profile hash not exported'),'egress_profile':safe(egress.get('mode')),'egress_allow':[s for s in egress.get('allow',[]) if isinstance(safe(s),str)] if isinstance(egress.get('allow'),list) else missing('Egress allowlist not recorded')},
           'timing':{'phases_s':{p:missing('Phase wall not emitted or not separable') for p in PHASES},'total_wall_s':num(m.get('total_wall_s_all_attempts',m.get('wall_s',md.get('wall_s')))),'timeout_cap_s':num((m.get('runner') or {}).get('timeout_s'))},
           'tokens':{'phases':{p:{t:missing('Per-phase token counter not emitted') for t in TOKENS} for p in PHASES},'total':vector(usage)},
           'cost':{'usd':missing('Cost calculation is not re-derivable from the public record'),'price_table_version':missing('Price table unavailable in the public record'),'calculator_version':missing('Calculator unavailable in the public record'),'accounting':'Source-reported values are not independently re-derived; complete all-attempt usage and pricing inputs are unavailable','long_context_reconciled':False},
           'outcome':g.get('outcome') if g.get('outcome') in ['pass','fail','invalid'] else missing('Official result outside standard outcome classes'),'stop_reason':missing('Runner status does not establish normalized stop cause'),'graded':True,
           'itt':{'class':missing('Invalid/environment cause requires evidence audit') if g.get('kind') in ['env_invalid','env_suspect','infra','control_apply'] else 'counted','evidence_ref':missing('No evidence-backed ITT classification') if g.get('kind') in ['env_invalid','env_suspect','infra','control_apply'] else 'STANDARD.md#intention-to-treat','cohort':'smoke-control' if 'smoke' in cid.lower() or re.search(r'(^|[-_])(noop|reference|control)([-_]|$)',cid) else 'scored'},
           'kogen':{'landed':missing('Kogen landing receipt absent'),'best_candidate':missing('Kogen candidate receipt absent')},
           'grade':{'grader':missing('Grading-host details are withheld from the public record'),'tests_ran':boolean(g.get('tests_ran')),'timestamp':safe(g.get('graded_at'))},
           'provenance':{'ledger_sha256':digest(raw),'manifest_sha256':digest(mf.read_bytes()) if mf.exists() else missing('Exact pulled manifest unavailable'),'source_ref':'reproduce/inputs/run-evidence/index.json'}}
        r['tools']['toolchains']={k:missing('Toolchain version/inventory not recorded') for k in ['python','ruby','elixir','erlang','rust','node','other_inventory']}
        r['tools']['toolchains']['python']=safe((m.get('host') or {}).get('python'))
        r['tools']['harness']=safe((m.get('wrapper') or {}).get('sha256'))
        if harness=='codex':r['tools']['codex_cli']=safe(m.get('cli_version'))
        if harness and not harness.startswith(('kogen','kgn')):
            r['kogen']={k:na('Harness does not use Kogen') for k in r['kogen']};r['tools']['kogen']=na('Harness does not use Kogen')
        else:
            # A root suffix is a hint, not a verified SHA. Do not promote it to version evidence.
            r['kogen']['landed']=boolean(report.get('status')=='landed') if report.get('status') else missing('Kogen report status absent')
            r['kogen']['best_candidate']=safe(report.get('best_candidate') or report.get('candidate'))
        # A Kogen pipeline may override the outer runner effort. Only its explicit
        # native clamp receipt establishes the operation's requested max.
        effort_note=(m.get('runtime_reported') or {}).get('effort_note','')
        if harness and harness.startswith('kh') and observed.get('effort')=='xhigh' and isinstance(effort_note,str) and re.search(r'max unsupported; clamped to xhigh',effort_note):
            r['effort']['requested']='max'
        status=m.get('status')
        if status=='ok':r['stop_reason']='completed'
        elif status=='timeout':r['stop_reason']='timeout'
        # Only explicit native recipe is used; a kh arm label is not a pinned recipe.
        if harness=='codex':r['recipe']='direct'
        if isinstance(g.get('grade_wall_s'),(int,float)):r['timing']['phases_s']['grade']=num(g['grade_wall_s'])
        r['tokens']['phases']['grade']={t:na('Official grading makes no contestant model call') for t in TOKENS}
        # Token stages own their counters; never add attempt totals to their stage rollups.
        stages=report.get('model_stages') or ku.get('stages') or []
        mapped={'build':'develop','develop':'develop','plan':'plan','shape':'shape','review':'review'}
        for p in PHASES:
            rows=[s for s in stages if mapped.get(s.get('stage'))==p]
            if rows:
                walls=[s.get('wall_ms') for s in rows]
                if all(isinstance(x,(int,float)) for x in walls):r['timing']['phases_s'][p]=sum(walls)/1000
                for t in TOKENS:
                    counts=[(s.get('tokens') or {}).get(t) for s in rows]
                    if all(isinstance(x,int) and not isinstance(x,bool) and x>=0 for x in counts):r['tokens']['phases'][p][t]=sum(counts)
        # Phases can nest. Use only named outer receipts, never check+gate sums.
        phases=ku.get('phases') or report.get('phase_timings') or []
        for p,name in [('setup','setup:task-setup'),('gate','gate_run')]:
            rows=[x for x in phases if x.get('name')==name]
            if rows and all(isinstance(x.get('wall_ms'),(int,float)) for x in rows):r['timing']['phases_s'][p]=sum(x['wall_ms'] for x in rows)/1000
        shape=ku.get('shape') or {}
        if isinstance(shape.get('wall_ms'),(int,float)):r['timing']['phases_s']['shape']=shape['wall_ms']/1000
        if harness and harness.startswith('kh'):
            r['tokens']['total']={t:missing('Captured runner counters do not establish complete all-stage usage') for t in TOKENS}
        if rid in ['r62b','r65','r65b'] and g.get('kind')=='control_apply':r['itt'].update({'class':'counted','evidence_ref':'METHOD.md'})
        # Keep exact per-cell observations, not modern host values projected backward.
        evidence.append(r)
    write_partitions(
        evidence,
        ROOT/'reproduce/inputs/run-evidence',
        round_for=lambda row: row.get('round_id') if isinstance(row.get('round_id'),str) else None,
    )
    (ROOT/'reproduce/inputs/run-evidence-provenance.json').write_text(json.dumps({'ledger_sha256':digest(raw),'input_rows':len(raw.splitlines()),'unique_cells':len(latest),'latest_grade':max(g.get('graded_at','') for g in latest.values()),'cost_source_status':'Source-reported; calculator, price table and analysis inputs are absent from this snapshot and values are not independently re-derived.','analysis_input_status':'not re-derivable from the public record','scope':'All latest official graded identities; ungraded deliveries absent. Exact-alias manifests only. Public metadata allowlist; no diagnostic grade fields, raw paths, identities or transcripts.'},indent=2)+'\n')

def build():
    # Evidence snapshot contains only derived allowlisted facts. Rebuild is host-independent.
    codes=load_legend()
    rows=read_partitions(ROOT/'reproduce/inputs/run-evidence')[1]
    rows=[expand_value(row,codes) for row in rows]
    from backfill_context import defaults
    context_dir=ROOT/'reproduce/inputs/context-evidence'
    context={r['cell_id']:expand_value(r,codes) for r in read_partitions(context_dir)[1]} if (context_dir/'index.json').exists() else {}
    rows=[defaults({**r,**context.get(r['cell_id'],{})}) for r in rows]
    extra_dir=ROOT/'reproduce/inputs/ungraded-evidence'
    if (extra_dir/'index.json').exists():
        rows += [defaults(expand_value(row,codes)) for row in read_partitions(extra_dir)[1]]
    rows.sort(key=lambda r:r['cell_id'])
    for row in rows:
        row['schema_version']='1.2'
        row['provenance']['source_ref']=(
            'reproduce/inputs/run-evidence/index.json'
            if row.get('graded') is True
            else 'reproduce/inputs/ungraded-evidence/index.json'
        )
    marker_to_code=load_marker_to_code()
    index=write_partitions(
        rows,
        ROOT/'results/run-records',
        round_for=lambda row: row.get('round_id') if isinstance(row.get('round_id'),str) else None,
        schema_field='schema_version',
        transform=lambda row: compact_value(row,marker_to_code),
    )
    (ROOT/'results/run-records.jsonl').unlink(missing_ok=True)
    print(f'Built {len(rows)} standard records across {len(index["files"])} files')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--probe',type=Path)
    a=ap.parse_args()
    if a.probe:
        capture(a.probe)
    build()
