#!/usr/bin/env python3
"""Validate standard records and exact historical missing-field declarations (offline)."""
import argparse, json, re
from collections import Counter, defaultdict
from pathlib import Path
from missing_reasons import load_legend, marker_code
from run_records import indexed_records
ROOT=Path(__file__).resolve().parents[1]
MISSING_CODES=load_legend(ROOT/'results/missing-reasons.json')

def missing_info(value):
    code=marker_code(value,MISSING_CODES)
    if code:
        entry=MISSING_CODES[code]
        return entry['reason'],entry['reconstructable_from']
    return value.get('missing'),value.get('reconstructable_from','none')

def schema_errors(value, schema, root, path='$'):
    """Evaluate the JSON Schema vocabulary used by the committed schema.
    Unsupported keywords fail closed; no optional package is needed.
    """
    supported={'$schema','$id','$defs','title','description','$ref','anyOf','type','const','enum','minLength','minimum','properties','required','additionalProperties','items','format'}
    unknown=set(schema)-supported
    if unknown:return [f'{path}: unsupported schema keywords {sorted(unknown)}']
    if '$ref' in schema:
        ref=schema['$ref']
        if not ref.startswith('#/'):return [f'{path}: external schema reference unsupported']
        target=root
        for part in ref[2:].split('/'):target=target[part.replace('~1','/').replace('~0','~')]
        return schema_errors(value,target,root,path)
    if 'anyOf' in schema:
        if any(not schema_errors(value,s,root,path) for s in schema['anyOf']):return []
        return [f'{path}: no allowed schema branch matches']
    errors=[]
    if 'const' in schema and value!=schema['const']:errors.append(f'{path}: wrong constant')
    if 'enum' in schema and value not in schema['enum']:errors.append(f'{path}: unknown enum value')
    types={'string':lambda x:isinstance(x,str),'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),'number':lambda x:isinstance(x,(int,float)) and not isinstance(x,bool) and __import__('math').isfinite(x),'integer':lambda x:isinstance(x,int) and not isinstance(x,bool),'boolean':lambda x:isinstance(x,bool)}
    if 'type' in schema and not types[schema['type']](value):return errors+[f'{path}: expected {schema["type"]}']
    if schema.get('format')=='date-time' and isinstance(value,str):
        try:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)',value):raise ValueError('not RFC3339 UTC')
            dt=__import__('datetime').datetime.fromisoformat(value.replace('Z','+00:00'))
            if dt.utcoffset()!=__import__('datetime').timedelta(0):raise ValueError('not UTC')
        except ValueError:errors.append(f'{path}: expected UTC timestamp')
    if isinstance(value,str) and len(value)<schema.get('minLength',0):errors.append(f'{path}: empty value')
    if isinstance(value,(int,float)) and not isinstance(value,bool) and value<schema.get('minimum',float('-inf')):errors.append(f'{path}: negative counter')
    if isinstance(value,dict):
        props=schema.get('properties',{})
        for k in schema.get('required',[]):
            if k not in value:errors.append(f'{path}.{k}: silently absent required field')
        if schema.get('additionalProperties') is False:
            for k in value.keys()-props.keys():errors.append(f'{path}.{k}: unexpected field')
        for k in value.keys() & props.keys():errors+=schema_errors(value[k],props[k],root,path+'.'+k)
    if isinstance(value,list) and 'items' in schema:
        for i,item in enumerate(value):errors+=schema_errors(item,schema['items'],root,f'{path}[{i}]')
    return errors

def leaves(value,path=''):
    if isinstance(value,dict) and not any(k in value for k in ('missing','not_applicable','withheld')):
        for k,v in value.items():yield from leaves(v,f'{path}.{k}' if path else k)
    elif isinstance(value,list) and any(isinstance(x,dict) for x in value):
        if not value:yield path,value
        for i,v in enumerate(value):yield from leaves(v,f'{path}[]')
    else:yield path,value

def records(path=None):
    if path is not None:
        return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
    rows=indexed_records(ROOT)
    # Retain the validator's historical aggregate order after merging indexed partitions.
    rows.sort(key=lambda row: row.get('cell_id',''))
    paths=sorted((ROOT/'rounds').glob('*/records.jsonl'))
    rows.extend(json.loads(s) for source in paths for s in source.read_text().splitlines() if s.strip())
    return rows

def gaps(rows):
    result=defaultdict(Counter)
    for r in rows:
        for p,v in leaves(r):
            if isinstance(v,dict) and 'missing' in v:
                reason,_source=missing_info(v)
                result[p][reason]+=1
    return {p:dict(sorted(c.items())) for p,c in sorted(result.items())}

def gap_sources(rows):
    result={'reconstructable':defaultdict(Counter),'lost':defaultdict(Counter)}
    for r in rows:
        for p,v in leaves(r):
            if isinstance(v,dict) and 'missing' in v:
                _reason,src=missing_info(v)
                result['lost' if src in ('none','not re-derivable from the public record') else 'reconstructable'][p][src]+=1
    return {k:{p:dict(c) for p,c in sorted(v.items())} for k,v in result.items()}

def normalize_declared_sources(value):
    """Treat absent internal file references as unavailable in the public snapshot."""
    normalized={'reconstructable':defaultdict(Counter),'lost':defaultdict(Counter)}
    for category,fields in value.items():
        for path,sources in fields.items():
            for source,count in sources.items():
                token=source.split(None,1)[0].split('#',1)[0]
                local=ROOT/token
                if category=='reconstructable' and (source == 'Official poll.py outcome ledger after delivery' or (token.startswith('levers/') and not local.exists())):
                    normalized['lost'][path]['not re-derivable from the public record']+=count
                else:
                    normalized[category][path][source]+=count
    return {k:{p:dict(c) for p,c in sorted(v.items())} for k,v in normalized.items()}

def normalize_declared_reasons(value):
    normalized={}
    for reason,count in value.items():
        if reason == 'qr.py death left stale states; finalization count is not live concurrency':
            reason='Dispatcher termination may leave stale state; finalization counts are not live concurrency'
        if reason == 'No official grade in captured polling ledger':
            reason='No official grade in the public snapshot'
        normalized[reason]=normalized.get(reason,0)+count
    return normalized

def coverage_leaves(value,path=''):
    # Arrays are one required capture slot: extra samples cannot inflate coverage.
    if isinstance(value,list):
        absent=any(isinstance(v,dict) and 'missing' in v for _,v in leaves(value,path))
        yield path,({'missing':'Nested array receipt missing'} if absent else value)
    elif isinstance(value,dict) and not any(k in value for k in ('missing','not_applicable','withheld')):
        for k,v in value.items():yield from coverage_leaves(v,f'{path}.{k}' if path else k)
    else:yield path,value

def group_completeness(rows):
    groups=defaultdict(lambda:[0,0])
    for r in rows:
        for p,v in coverage_leaves(r):
            g=p.split('.')[0];groups[g][0]+=1
            groups[g][1]+=int(isinstance(v,dict) and 'missing' in v)
    return {g:{'fields':n,'missing':m,'completeness':100*(n-m)/n} for g,(n,m) in sorted(groups.items())}

def validate(rid, all_rows, strict=False):
    rows=[r for r in all_rows if r.get('audit_round')==rid or r.get('round_id')==rid]; errors=[]
    schema=json.loads((ROOT/'schema/run-record.schema.json').read_text())
    identities=Counter(r.get('cell_id') if isinstance(r.get('cell_id'),str) else '<missing>' for r in all_rows)
    for r in rows:
        if strict and r.get('schema_version')!='1.2':errors.append('Strict release requires schema 1.2: '+str(r.get('cell_id')))
        current_branch=schema['$defs']['current'] if r.get('schema_version')=='1.2' else (schema['$defs']['previous'] if r.get('schema_version')=='1.1' else schema)
        errors+=schema_errors(r,current_branch,schema,str(r.get('cell_id')))
        cid=r.get('cell_id')
        if isinstance(cid,str) and identities[cid]!=1:errors.append('Duplicate cell identity: '+cid)
        if isinstance(r.get('round_id'),str) and r['round_id']!=rid:errors.append('Round identity mismatch: '+str(cid))
        if r.get('itt',{}).get('class')=='excluded-env-fault':
            ref=r['itt'].get('evidence_ref')
            if not isinstance(ref,str) or not (ROOT/ref.split('#')[0]).is_file():errors.append('Environmental exclusion needs an existing evidence reference: '+str(cid))
    actual=gaps(rows)
    declaration=ROOT/'rounds'/rid/'MISSING.md'
    declared_protocol_deviations=[]
    if not declaration.is_file():
        if actual or not strict:errors.append('Missing MISSING.md declaration')
    else:
        match=re.search(r'```json\n(.*?)\n```',declaration.read_text(),re.S)
        try:d=json.loads(match.group(1)) if match else {}
        except ValueError:d={}
        if d.get('round')!=rid or d.get('cells')!=len(rows):errors.append('Declaration round/cell count mismatch')
        declared=d.get('fields',{})
        declared_protocol_deviations=d.get('protocol_deviations',[])
        if normalize_declared_sources(d.get('gap_sources',{}))!=gap_sources(rows):errors.append('Declaration reconstruction source inventory differs from records')
        for p,reason_counts in actual.items():
            field=declared.get(p,{})
            if normalize_declared_reasons(field.get('reasons',{}))!=reason_counts or field.get('count')!=sum(reason_counts.values()) or not isinstance(field.get('affects_verdict'),str) or not field.get('affects_verdict'):errors.append('Undeclared or stale gap: '+p)
        if set(declared)!=set(actual):errors.append('Declaration field inventory differs from records')
    if strict and not rows:errors.append('No smoke/scored records; empty cohort cannot pass strict validation')
    if strict and (actual or declared_protocol_deviations) and not declared_protocol_deviations:
        errors.append('Strict historical validation with gaps requires explicit protocol deviations in MISSING.md')
    for name in ['README.md','MEASURED.md']:
        if not (ROOT/'rounds'/rid/name).is_file():errors.append('Missing round document '+name)
    total=sum(1 for r in rows for _ in coverage_leaves(r)); absent=sum(isinstance(v,dict) and 'missing' in v for r in rows for _,v in coverage_leaves(r))
    complete=100*(total-absent)/total if total else None
    release_eligible=bool(rows) and not errors and not actual and not declared_protocol_deviations
    verdict='FAIL' if errors else ('PASS WITH DECLARED DEVIATIONS' if actual or declared_protocol_deviations else ('PASS' if rows else 'NO DELIVERED DATA'))
    return {'round':rid,'cells':len(rows),'fields':total,'missing':absent,'completeness':complete,'verdict':verdict,'strict_release_eligible':release_eligible,'protocol_deviations':declared_protocol_deviations,'errors':errors,'groups':group_completeness(rows),'gap_sources':gap_sources(rows),'graded_cells':sum(r.get('graded') is True for r in rows)}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--round',required=True);ap.add_argument('--strict',action='store_true');ap.add_argument('--records',type=Path)
    a=ap.parse_args();report=validate(a.round,records(a.records),a.strict);print(json.dumps(report,indent=2));raise SystemExit(bool(report['errors']))
