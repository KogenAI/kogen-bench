#!/usr/bin/env python3
"""Freeze a named unlaunched revision; preserve all previous registrations."""
import argparse
from datetime import datetime, timezone
from shape_common import ROOT, digest, snapshot, write_json

def freeze(output):
    if output.exists():raise ValueError('registration already frozen; never overwrite')
    files=[*ROOT.glob('*.py'),*ROOT.glob('*.sh'),ROOT/'plan.json',ROOT/'DECISION-RULE.md',
           ROOT/'README.md',ROOT/'ORDERS.md',ROOT/'REVIEW-LOG.md',ROOT/'FIX-REPORT.md',ROOT/'REPORT.md',ROOT/'behaviour-inventory.json']
    files += [p for p in (ROOT/'mutants').rglob('*') if p.is_file() and 'revisions' not in p.parts and
              (p.suffix=='.patch' or p.name in ('MUTANTS.md','catalog.json'))]
    files += [p for p in (ROOT/'tasks').rglob('*') if p.is_file() and '.git' not in p.parts]
    files += [p for p in (ROOT/'overlays').glob('*') if p.is_file()]
    row={'schema':2,'job':'BM-SHAPE1-FIX-2','revision':'fix-1',
         'frozen_utc':datetime.now(timezone.utc).isoformat(),'measured_launches':0,
         'review':'full review blocked; sole fix round completed; targeted recheck pending',
         'launch_readiness':'blocked','previous_registration_sha256':digest(ROOT/'REGISTRATION.json'),
         'files':{str(p.relative_to(ROOT)):digest(p) for p in sorted(set(files))}}
    write_json(output,row);return digest(output)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='REGISTRATION-FIX-1.json');a=p.parse_args()
    target=ROOT/a.output
    if target.parent!=ROOT or target.suffix!='.json':raise ValueError('registration must be a named root JSON file')
    print(freeze(target))
