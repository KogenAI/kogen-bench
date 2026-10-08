#!/usr/bin/env python3
"""Explicit historical gap audit. Run after reviewing a new evidence snapshot.
This writes declarations; validate_round.py itself never waives or writes gaps.
"""
import json, re
from pathlib import Path
from validate_round import ROOT, records, gaps, validate, group_completeness, gap_sources

SUPPLEMENTAL_COHORTS = {
    'r70-rve-ext': ('r70-rve-ext',),
    'r70-rve-rerun': ('r70-rve-rerun',),
    'r70-task8': ('r70-task8-v1-smoke', 'r70-task8-v2-smoke'),
}
SUPPLEMENTAL_CONTROL_COHORTS = {
    'r70-rve-ext': ('r70-rve-ext',),
    'r70-rve-rerun': ('r70-rve-rerun',),
    'r70-task8': ('r70-task8-v1', 'r70-task8-v2'),
}

def supplemental_evidence(round_id):
    cohorts=SUPPLEMENTAL_COHORTS.get(round_id)
    if not cohorts:return None
    tests=[json.loads(line) for line in (ROOT/'results/test-counts.jsonl').read_text().splitlines() if line.strip()]
    controls=[json.loads(line) for line in (ROOT/'results/controls.jsonl').read_text().splitlines() if line.strip()]
    grades=[row for row in tests if row.get('cohort') in cohorts]
    control_cohorts=SUPPLEMENTAL_CONTROL_COHORTS.get(round_id,cohorts)
    control_rows=[row for row in controls if row.get('cohort') in control_cohorts]
    unscored_smokes=sum(row.get('scored') is False for row in grades)
    if round_id=='r70-task8':
        grade_label=f'{len(grades)} unscored smokes' if unscored_smokes==len(grades) else f'{len(grades)} official grades, {unscored_smokes} unscored smokes'
    else:
        grade_label=f'{len(grades)} official grades'
    resource_note=''
    if round_id in {'r70-rve-ext','r70-rve-rerun'}:
        resource_note=(' A supplemental cost/time ledger covers 44 official rerun and extension cells with uncached/cached/output token counters and wall seconds; per-cell cost, reasoning counters, effective model/effort receipts, and verified harness version remain unavailable and null. '
                       'This does not add rows to the Standard run-record completeness denominator.')
    return {'grade_label':grade_label,'controls':len(control_rows),'resource_note':resource_note}

def impact(path):
    if path.startswith(('itt.','outcome','stop_reason','grade.')):return 'Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.'
    if path.startswith(('timing.','host.')):return 'Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.'
    if path.startswith(('cost.','tokens.')):return 'Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.'
    return 'Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.'

def group_lines(rows):
    lines=['Per-group completeness:', '', '| Group | Required leaves | Missing | Complete |','| --- | ---: | ---: | ---: |']
    for g,c in group_completeness(rows).items():lines.append(f"| `{g}` | {c['fields']} | {c['missing']} | {c['completeness']:.1f}% |")
    if not rows:lines.append('| All groups | 0 | 0 | N/A |')
    return lines+['',*gap_lines(rows)]

def gap_lines(rows):
    lines=[]
    for category, fields in gap_sources(rows).items():
        if category=='reconstructable':
            lines += ['Potentially reconstructable from identified sources:', '', 'These values remain missing in this snapshot; the listed sources are candidates for reconstruction.', '', '| Field | Missing occurrences | Reconstruction source |','| --- | ---: | --- |']
        else:
            lines += ['Lost or unavailable in inspected surviving sources:', '', '| Field | Missing occurrences | Reconstruction source |','| --- | ---: | --- |']
        for p,c in fields.items():lines.append(f"| `{p}` | {sum(c.values())} | "+'; '.join(f'{s} ({n})' for s,n in c.items())+' |')
        if not fields:lines.append('| None | 0 | None |')
        lines.append('')
    return lines

def main():
    rows=records(); ids=json.loads((ROOT/'rounds/index.json').read_text())
    ids=sorted(set(ids)|{r['audit_round'] for r in rows})
    reports=[]
    for rid in ids:
        folder=ROOT/'rounds'/rid;folder.mkdir(exist_ok=True);readme=folder/'README.md'
        if not readme.exists():readme.write_text(f'# {rid}\n\nSTATUS: **INTERIM**\n\nQuestion: Owning round not recoverable from existing public identifiers.\n\nVerdict: no pooled scientific claim; recover round ownership before analysis.\n')
        text=readme.read_text();subset=[r for r in rows if r['audit_round']==rid];g=gaps(subset)
        question=re.search(r'^(?:Question(?:/design)?|Design):\s*(.+)$',text,re.M)
        question=question.group(1) if question else 'Question not stated in the documentary round stub; consult the linked sources before interpreting this round.'
        fields={p:{'count':sum(c.values()),'reasons':c,'affects_verdict':impact(p)} for p,c in g.items()}
        declaration={'round':rid,'cells':len(subset),'fields':fields,'gap_sources':gap_sources(subset)}
        (folder/'MISSING.md').write_text('# Declared historical data gaps\n\nThis declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.\n\n```json\n'+json.dumps(declaration,indent=2,sort_keys=True)+'\n```\n')
        supplemental=supplemental_evidence(rid)
        if supplemental:
            coverage=(f'Standard run-record capture only: {len(subset)} deliveries; capture grade-flag records: {sum(r.get("graded") is True for r in subset)}. '
                      'Public official-export cross-checks and capture-reported scope are documented in [GRADE-JOIN.md](../../results/GRADE-JOIN.md). '
                      f'Separate supplemental ledgers publish {supplemental["grade_label"]} and {supplemental["controls"]} control receipts; '
                      'these receipts are outside the Standard run-record completeness denominator.'+supplemental['resource_note'])
            scope_note='Coverage and verdict below apply only to the Standard run-record capture.'
        else:
            coverage=(f'Coverage: {len(subset)} captured deliveries; capture grade-flag records: {sum(r.get("graded") is True for r in subset)}. '
                      'The refreshed public official-grade export exact-joins all 5,020 captured grade IDs; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). '
                      'The 128 post-cut additions comprise 84 model passes, 19 model failures, and 25 invalid control_apply rows. Those controls are not model failures and are classified as invalid in the cells export. Ungraded deliveries carry no invented outcomes. '
                      'Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).')
            scope_note=''
        lines=[f'# Measurement contract: {rid}','',f'Question (from [round record](README.md)): {question}','',
            'Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.','',
            scope_note,coverage,'',
            *group_lines(subset),'', 'MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):','', '| Field | Missing occurrences | Reason | Effect on verdict |','| --- | ---: | --- | --- |']
        for p,c in g.items():lines.append(f'| `{p}` | {sum(c.values())} | '+ '; '.join(f'{reason} ({n})' for reason,n in c.items())+' | '+impact(p)+' |')
        if not g:lines+=['| None in captured records | 0 | No graded cells captured; completeness is N/A. | No cell verdict supported by this snapshot. |' if not subset else '| None | 0 | All fields recorded. | None |']
        (folder/'MEASURED.md').write_text('\n'.join(lines)+'\n')
        report=validate(rid,rows);reports.append(report)
        pct=f"{report['completeness']:.1f}%" if report['completeness'] is not None else 'N/A'
        if supplemental:
            line=(f"Data completeness (standard run-record capture): **{pct}** ({len(subset)} deliveries; {report['verdict']}). "
                  f"Supplemental evidence: {supplemental['grade_label']}; {supplemental['controls']} control receipts. "
                  '[Measurement contract](MEASURED.md); [declared gaps](MISSING.md).')
        else:
            line=f"Data completeness: **{pct}** ({len(subset)} deliveries; {report['verdict']}). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md)."
        text=re.sub(r'^Data completeness[^\n]*\n?', '', text,flags=re.M)
        status=re.search(r'^STATUS:.*$',text,re.M)
        if status:text=text[:status.end()]+'\n\n'+line+text[status.end():]
        else:text+='\n'+line+'\n'
        readme.write_text(text)
    out=['# Standard record validation','', 'Leaf-field completeness includes explicit, justified not-applicable values; missing values reduce completeness. Percentages are data coverage, not scientific validity. Historical PASS WITH DECLARED GAPS does not satisfy strict release. No deliveries gives N/A and cannot pass strict validation. Each row was validated using the same validator behind `validate_round.py --round ID`.','', '| Round | Deliveries | Required leaves | Missing leaves | Complete | Validation verdict |','| --- | ---: | ---: | ---: | ---: | --- |']
    for r in reports:
        pct=f"{r['completeness']:.1f}%" if r['completeness'] is not None else 'N/A'
        out.append(f"| [{r['round']}](../rounds/{r['round']}/MEASURED.md) | {r['cells']} | {r['fields']} | {r['missing']} | {pct} | {r['verdict']} |")
    out+=['','Per-group completeness (all required groups; arrays count once and require all nested receipts):','', '| Round | '+ ' | '.join(sorted(group_completeness(rows)))+' |','| --- | '+ ' | '.join('---:' for _ in group_completeness(rows))+' |']
    for report in reports:
        out.append('| '+report['round']+' | '+' | '.join(f"{report['groups'][g]['completeness']:.1f}%" if g in report['groups'] else 'N/A' for g in sorted(group_completeness(rows)))+' |')
    out+=['',*gap_lines(rows)]
    (ROOT/'results/validation-summary.md').write_text('\n'.join(out).rstrip()+'\n')
    errors=[e for r in reports for e in r['errors']]
    print(json.dumps({'rounds':len(reports),'cells':len(rows),'failures':errors},indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
