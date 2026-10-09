#!/usr/bin/env python3
"""Run validate_round's strict validator against one RESULT directory."""
import argparse, json, shutil, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reproduce'))
import validate_round

def check(result_dir):
    record=Path(result_dir)/'standard.json'
    if not record.is_file(): raise SystemExit(f'missing {record}')
    row=json.loads(record.read_text())
    rid=row.get('audit_round') if isinstance(row.get('audit_round'),str) else row.get('round_id')
    if not isinstance(rid,str): raise SystemExit('standard record has no auditable round id')
    with tempfile.TemporaryDirectory(prefix='standard-cell-check-') as tmp:
        root=Path(tmp); (root/'schema').mkdir(); (root/'results').mkdir(); (root/'rounds'/rid).mkdir(parents=True)
        shutil.copy(ROOT/'schema/run-record.schema.json',root/'schema/run-record.schema.json')
        shutil.copy(ROOT/'results/missing-reasons.json',root/'results/missing-reasons.json')
        for name in ('README.md','MEASURED.md'):
            (root/'rounds'/rid/name).write_text('single-cell strict validation fixture\n')
        old_root,old_codes=validate_round.ROOT,validate_round.MISSING_CODES
        try:
            validate_round.ROOT=root
            from missing_reasons import load_legend
            validate_round.MISSING_CODES=load_legend(root/'results/missing-reasons.json')
            gaps=validate_round.gaps([row])
            deviations=['single-cell capture has declared missing slots'] if gaps else []
            fields={p:{'count':sum(counts.values()),'reasons':counts,'affects_verdict':'strict completion'} for p,counts in gaps.items()}
            declaration={'round':rid,'cells':1,'fields':fields,'gap_sources':validate_round.gap_sources([row]),'protocol_deviations':deviations}
            (root/'rounds'/rid/'MISSING.md').write_text('```json\n'+json.dumps(declaration)+'\n```\n')
            report=validate_round.validate(rid,[row],strict=True)
        finally: validate_round.ROOT,validate_round.MISSING_CODES=old_root,old_codes
    print(f"strict missing count: {report['missing']}")
    for e in report['errors']: print(f'ERROR: {e}')
    return 1 if report['errors'] or report['missing'] or not report['strict_release_eligible'] else 0
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('result_dir',type=Path); a=ap.parse_args(); raise SystemExit(check(a.result_dir))
