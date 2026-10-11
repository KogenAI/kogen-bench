#!/usr/bin/env python3
"""Offline checks of public aggregate arithmetic; no scorer or network access."""
import csv
import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]

def check(ok, label):
    if not ok:
        raise AssertionError(label)

def median(xs):
    return statistics.median(xs)

def verify_manifest():
    path = ROOT/'SHA256SUMS'
    if not path.exists():
        return 'not present yet (assembly mode)'
    covered=set()
    for line in path.read_text().splitlines():
        expected,name=line.split('  ',1)
        p=ROOT/name
        check(not p.is_symlink() and p.is_file(), 'manifest regular file')
        check(hashlib.sha256(p.read_bytes()).hexdigest()==expected,'checksum '+name)
        covered.add(p.relative_to(ROOT).as_posix())
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
    check(covered==actual,'complete checksum coverage')
    return f'{len(covered)} entries verified'

def main():
    d=json.loads((ROOT/'results/results.json').read_text())
    intervals=json.loads((ROOT/'results/change-intervals.json').read_text())
    ix={(x['host'],x['wave'],x['arm']):x['seconds'] for x in intervals}
    cells=d['cells']
    check(len(cells)==26,'26 completed cells')
    check(len(ix)==26,'26 numeric interval inventories')
    check(sum(c['valid_y_n']=='n' for c in cells)==4,'four invalid cells')
    check(all(not c['full_compliance_certified'] for c in cells),'audit qualifications')
    with (ROOT/'results/cells.tsv').open() as f:
        table=list(csv.DictReader(f,delimiter='\t'))
    check(len(table)==26,'TSV count')
    for c,row in zip(cells,table):
        key=(c['host'],c['wave'],c['arm'])
        xs=ix[key]
        check(all(isinstance(x,(int,float)) and x>=0 for x in xs),'nonnegative intervals')
        t=c['timing']
        check(len(xs)==t['change_interval_count'],'interval count')
        check(median(xs)==t['buildtest_per_change_median_s'],'per-cell J1')
        check(sum(x>0 for x in xs)==t['change_interval_with_buildtest_count'],'positive intervals')
        check(row['host']==c['host'] and row['wave']==c['wave'] and row['language']==c['language'],'cell identity')
        check(row['FINAL/106']==f"{c['final']}/106",'cell score')
        check(row['valid_y_n']==c['valid_y_n'] and row['validity_reason']==c['validity_reason'],'cell validity')
        check(row['decision_scope']==c['scope'],'cell scope')
        check(float(row['J1_build_test_seconds_per_change'])==t['buildtest_per_change_median_s'],'cell timing')
        u=c['tokens']['usage']
        check(int(row['tokens'])==u['total_tokens'],'cell tokens')
        check(u['total_tokens']==u['input_tokens']+u['output_tokens'],'token subsets not double counted')
        check(c['tokens']['method']=='session cumulative total_token_usage','cumulative tokens')
        receipt=c['official_score_receipt']
        check(receipt['combined_scored']==c['final'] and receipt['N_scored']==106,'recorded score receipt')
    primary=[c for c in cells if c['scope']=='PRIMARY as-scored']
    repaired=[c for c in cells if c['scope']=='REPAIRED-only']
    linux=[c for c in cells if c['scope']=='Linux robustness (nondeciding)']
    check((len(primary),len(repaired),len(linux))==(20,2,4),'scope counts')
    def validate_sample(sample,expected):
        for arm in ['rust','go','ts','ex','py']:
            group=[c for c in sample if c['arm']==arm]
            scores=[c['final'] for c in group]
            xs=[x for c in group for x in ix[(c['host'],c['wave'],c['arm'])]]
            e=expected['scores'][arm]
            check(scores==e['values'],'sample scores')
            check(median(scores)==e['median'] and min(scores)==e['min'] and max(scores)==e['max'] and max(scores)-min(scores)==e['spread'],'sample statistics')
            t=expected['timing'][arm]
            check(len(xs)==t['change_interval_count'] and median(xs)==t['buildtest_per_change_median_s'],'pooled J1')
            positive=[x for x in xs if x>0]
            check(median(positive)==t['buildtest_per_active_change_median_s'],'positive-only pooled timing')
    validate_sample(primary,d['primary'])
    replacement=[c for c in primary if not(c['host']=='Mac Studio' and c['arm']=='go')]+repaired
    validate_sample(replacement,d['repaired'])
    medians=d['primary']['scores']
    top=sorted(medians,key=lambda a:medians[a]['median'],reverse=True)[:2]
    check(top==['ts','go'] and abs(medians['ts']['median']-medians['go']['median'])<=3,'top two tie zone')
    check(d['primary']['timing']['go']['buildtest_per_change_median_s']<d['primary']['timing']['ts']['buildtest_per_change_median_s'],'Go J1 faster')
    check(d['primary']['winner']=='Go' and d['repaired']['winner']=='Go','reported winners')
    receipts=json.loads((ROOT/'results/source-receipts.json').read_text())
    check(len(receipts)==22,'22 private-source aggregate verifications')
    for r in receipts:
        check(all(r['checks'].values()),'source numerical checks')
        for kind in ['official','combined']:
            q=r[kind]
            check(q['rows']==106 and q['duplicates']==0 and q['invalid_rows']==0,'aggregate source inventory')
            check(sum(q['status_counts'].values())==106 and q['status_counts']['pass']==r['final'],'source count arithmetic')
        check(r['official']['status_counts']==r['combined']['status_counts'],'first/combined aggregates agree')
    rule=ROOT/'harness/DECISION-RULE-v5.md'
    check(hashlib.sha256(rule.read_bytes()).hexdigest()==d['rule_sha256'],'governing rule bytes')
    check((ROOT/'harness/MODE').read_text().strip()=='real-workflow','MODE')
    check(not (ROOT/'inputs/conformance').exists(),'withheld conformance boundary')
    check(not any(ROOT.rglob('turn-*.jsonl')),'transcript boundary')
    print('PASS: 26 cells; 4 invalid; PRIMARY and REPAIRED score/J1 arithmetic; token components; 22 aggregate source receipts; rule/MODE; withholding boundaries.')
    print('SHA256SUMS: '+verify_manifest())
    print('Limits: public arithmetic only; official score/token derivation, classifier replay and historical perfect-score searches require private evidence.')

if __name__=='__main__':
    main()
