#!/usr/bin/env python3
"""Export outcome-only results. No grader, remote access, or transcript reads."""
import argparse, csv, hashlib, json, re
from pathlib import Path
from privacy import contains_private_path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['round','arm','task','rep','venue','harness','model','effort','outcome','ITT outcome','exclusion reason','wall_s','tokens','usd_est']
SAFE = re.compile(r'^[A-Za-z0-9_. +:/()≥−-]*$')

def label(value):
    if value is None: return ''
    s = str(value)
    # Identities and paths cannot be emitted, even from externally supplied ledgers.
    if '@' in s or re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b|/Users/|/home/|~/',s) or contains_private_path(s): return 'withheld'
    return s if SAFE.fullmatch(s) else 'unmapped'

def round_tag(cid, experiment=''):
    def canonical(n, suffix=''):
        # A single-letter variant or p2 is a round; aj/ac/pr/w7 etc is a block label.
        suffix=suffix.lower()
        return 'r'+str(int(n))+(suffix if len(suffix)==1 or suffix=='p2' else '')
    # These R70 cohorts share native cell IDs with the wider round. Their
    # explicit sanitized experiment tag preserves the separate public cohort.
    if experiment in ('r70-rve-rerun', 'r70-rve-ext'):
        return experiment
    for text in (cid, experiment):
        m=re.match(r'^(?:rec-lever-)?(?:lr|r)(\d{1,2})([a-z]*[0-9]*)(?=[^a-zA-Z0-9]|$)',text)
        if m:return canonical(m[1],m[2])
        # Studio repetition is __rN, so only hyphen-prefixed tags identify a round.
        # Prefer the first owning tag: -r56b-r01-studio is round 56b, not round 01.
        m=re.search(r'-(?:lr|r)(\d{1,2})([a-z]*[0-9]*)(?=-)',text,re.I)
        if m:return canonical(m[1],m[2])
    return 'unmapped'

def number(value):
    return value if isinstance(value,(int,float)) and not isinstance(value,bool) and value>=0 else None

def export(grades, metadata, output):
    raw = grades.read_bytes()
    rows = [json.loads(s) for s in raw.splitlines() if s.strip()]
    meta = json.loads(metadata.read_text()) if metadata and metadata.exists() else {}
    # One final observation per identity; official duplicate annotations never create new cells.
    chosen = {}
    duplicates = 0
    for i,g in enumerate(rows):
        cid = g.get('cell_id')
        if not isinstance(cid,str): cid='unmapped-row-'+str(i)
        if cid in chosen:
            duplicates += 1
            old = chosen[cid]
            if str(g.get('graded_at','')) < str(old.get('graded_at','')): continue
        chosen[cid] = g
    # The FE2 rerun is a separate official-grade cohort whose sanitized
    # receipts are in test-counts.jsonl, not the older grade snapshot above.
    # Include those exact identities in the outcome export with the registered
    # base task ID; the round tag carries the FE2 cohort distinction.
    supplemental_path = ROOT/'results/test-counts.jsonl'
    supplemental_raw = supplemental_path.read_bytes() if supplemental_path.exists() else b''
    supplemental_count = 0
    for line in supplemental_raw.splitlines():
        if not line.strip(): continue
        grade = json.loads(line)
        if grade.get('cohort') != 'r70-rve-rerun' or grade.get('scored') is not True: continue
        cid = grade.get('cell_id')
        if not isinstance(cid, str) or cid in chosen: continue
        parts = cid.split('__')
        task = grade.get('task')
        if (len(parts) != 6 or not isinstance(task, str) or not task.endswith('-fe2')
                or parts[4] != task or parts[5] != 'r'+str(grade.get('rep'))
                or not task[:-4].endswith('-'+str(grade.get('stack')))):
            raise ValueError('Malformed public Round 70 FE2 test-count identity')
        chosen[cid] = {
            'cell_id': cid, 'outcome': grade.get('outcome'), 'host': grade.get('host'),
            'arm': grade.get('stack'), 'task': task[:-4], 'rep': grade.get('rep'), 'kind': 'model',
        }
        meta[cid] = {'experiment': 'r70-rve-rerun', 'harness': parts[0], 'model': parts[1], 'effort': parts[2]}
        supplemental_count += 1
    supplemental_round_rows = []
    for round_id in ('r70-rve2', 'r70-rve3', 'r70-spot1'):
        records_path = ROOT/'rounds'/round_id/'records.jsonl'
        if not records_path.exists():
            continue
        for line in records_path.read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get('round_id') != round_id:
                raise ValueError(f'Round record identity mismatch in {records_path}')
            if (record.get('itt') or {}).get('cohort') != 'scored':
                continue
            task = record.get('task') or {}
            model = record.get('model') or {}
            effort = record.get('effort') or {}
            timing = record.get('timing') or {}
            cid = record.get('cell_id')
            if not isinstance(cid, str) or not isinstance(task.get('id'), str):
                raise ValueError(f'Round record lacks a public cell/task identity in {records_path}')
            outcome = record.get('outcome')
            if outcome not in ('pass', 'fail'):
                raise ValueError(f'Round record has unresolved outcome {cid!r}')
            if cid in chosen:
                raise ValueError(f'Round record duplicates an exported grade identity: {cid}')
            venue = 'eu' if '-eu-' in cid else ('us' if '-us-' in cid else 'unmapped')
            cells_row = {
                'round': round_id,
                'arm': label(record.get('arm')),
                'task': label(task.get('id')),
                'rep': '',
                'venue': venue,
                'harness': 'codex',
                'model': label(model.get('effective')),
                'effort': label(effort.get('effective')),
                'outcome': outcome,
                'ITT outcome': outcome,
                'exclusion reason': '',
                'wall_s': number(timing.get('total_wall_s')),
                'tokens': None,
                'usd_est': None,
            }
            supplemental_round_rows.append(cells_row)
    output.mkdir(parents=True,exist_ok=True)
    cells=[];issues=[]
    for cid,g in sorted(chosen.items()):
        m=meta.get(cid,{})
        rid=round_tag(cid,m.get('experiment',''))
        kind=g.get('kind','unknown')
        outcome=g.get('outcome',g.get('result','unknown'))
        # Invalid control applications carry outcome=fail as the run's terminal
        # state, but result=invalid is the official grading classification.
        # Keep them visible as invalid rows so they are never counted as model failures.
        if kind=='control_apply' and g.get('result')=='invalid':
            outcome='invalid'
        if outcome not in ['pass','fail','invalid','grader_error']:outcome='unknown'
        status=m.get('runner_status')
        exclusion=''
        itt=outcome if outcome in ['pass','fail'] else 'unresolved'
        if kind in ['env_invalid','env_suspect','infra']:
            # A label is insufficient proof: no automatic environmental exclusion.
            itt='unresolved';exclusion='environment label requires evidence review; no exclusion asserted'
        if kind=='control_apply':
            if rid in ['r62b','r65','r65b']:
                itt='fail'  # documented R62/R65 audits: internal stops, no proven OURS fault
            else:
                itt='unresolved';exclusion='control_apply cause unresolved; inspect documented audit'
        if kind=='model' and status in ['timeout','error','harness_error','stage_failed','infra_error']:
            itt='fail'
        if 'smoke' in cid.lower() or re.search(r'(^|[-_])(noop|reference|control)([-_]|$)',cid):
            itt='not_scored';exclusion='smoke or control row; retained outside scored denominator'
        host=str(g.get('host','')).lower()
        venue={'us':'kogen-bench-us','eu':'kogen-bench-eu','studio':'studio','us-worker':'kogen-bench-us','eu-worker':'kogen-bench-eu','kogen-bench-us':'kogen-bench-us','kogen-bench-eu':'kogen-bench-eu','orchestrator-control':'orchestrator-control'}.get(host,'unmapped')
        model=m.get('model');effort=m.get('effort');harness=m.get('harness')
        parts=cid.split('__')
        if len(parts)>=6:
            harness=harness or parts[0];model=model or parts[1];effort=effort or parts[2]
        if (harness or '').startswith('kh') and effort=='max':effort='xhigh (requested max)'
        r={'round':rid,'arm':label(g.get('arm')),'task':label(g.get('task')),'rep':label(g.get('rep')),'venue':venue,
           'harness':label(harness),'model':label(model),'effort':label(effort),'outcome':outcome,'ITT outcome':itt,
           'exclusion reason':exclusion,'wall_s':number(m.get('wall_s')),'tokens':number(m.get('tokens')),'usd_est':number(m.get('usd_est'))}
        cells.append(r)
        missing=[k for k in ['round','harness','model','effort','wall_s','tokens','usd_est'] if r[k] in [None,'','unmapped']]
        if missing or itt=='unresolved':issues.append({'round':rid,'arm':r['arm'],'task':r['task'],'rep':r['rep'],'missing_fields':missing,'itt_unresolved':itt=='unresolved'})
    cells.extend(supplemental_round_rows)
    for row in supplemental_round_rows:
        issues.append({
            'round': row['round'], 'arm': row['arm'], 'task': row['task'], 'rep': row['rep'],
            'missing_fields': ['tokens', 'usd_est'], 'itt_unresolved': False,
        })
    with (output/'cells.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(cells)
    (output/'cells.jsonl').write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in cells))
    (output/'unmapped.json').write_text(json.dumps(issues,indent=2,sort_keys=True)+'\n')
    report={'input_rows':len(rows),'exported_cell_rows':len(cells),'duplicate_identity_rows_reconciled':duplicates,'unmapped_or_incomplete_rows':len(issues),
            'supplemental_r70_rerun_rows':supplemental_count,
            'supplemental_round_record_rows':len(supplemental_round_rows),
            'unmapped_round_rows':sum(c['round']=='unmapped' for c in cells),'unresolved_itt_rows':sum(c['ITT outcome']=='unresolved' for c in cells),
            'grades_input_sha256':hashlib.sha256(raw).hexdigest(),'test_counts_input_sha256':hashlib.sha256(supplemental_raw).hexdigest() if supplemental_raw else None,'wall_s_definition':'runner all-attempts wall; no queue or grading; blank if unavailable',
            'cost_note':'Cost estimates are source-reported API equivalents. The calculator and analysis inputs are absent from this snapshot, so the calculation is not re-derivable from the public record; missing usage is null, not zero.',
            'coverage_note':'official grade snapshot plus supplemental scored FE2 rerun grades from test-counts.jsonl and published per-round records for r70-rve2, r70-rve3 and r70-spot1; ungraded deliveries remain absent, so this export alone is not a complete planned ITT cohort'}
    (output/'export-report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grades',type=Path,default=ROOT/'reproduce/inputs/grades.final.jsonl')
    parser.add_argument('--metadata',type=Path,default=ROOT/'reproduce/inputs/cell-metadata.json')
    parser.add_argument('--output',type=Path,default=ROOT/'results')
    args=parser.parse_args();export(args.grades,args.metadata,args.output)
