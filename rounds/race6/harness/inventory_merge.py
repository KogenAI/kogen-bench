#!/usr/bin/env python3
"""Merge supervisor per-home inventories before freeze; preserve scan evidence."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('reports',type=Path,nargs='+');a=p.parse_args()
reports=[json.loads(r.read_text()) for r in a.reports]
d=dict(reports[0]);found={};types={}
for report in reports:
    found.update({e['path']:e for e in report['found']});types.update(report.get('lock_types',{}))
d['found']=[found[k] for k in sorted(found)];d['locks']=sorted({e['protect'] for e in d['found']});d['lock_types']=types
for key in ('outside_reach','errors','scan_notes','scan_errors_original','quint_wrappers'):
    d[key]=sorted({entry for report in reports for entry in report.get(key,[])})
d['homes']=[report['home'] for report in reports]
(a.root/'hidden-inventory.json').write_text(json.dumps(d,indent=2)+'\n')
text=f"HIDDEN SUITE INVENTORY: {len(d['found'])} discoveries; {len(d['locks'])} protection roots; homes={d['homes']}\n"
text+=d['excluded']+'\n'+''.join(f"{e['path']}\t{e['protect']}\t{e['reason']}\n" for e in d['found'])
text+='SCAN DISCLOSURES:\n'+'\n'.join(d['scan_notes'])+'\nUNRESOLVED ERRORS:\n'+'\n'.join(d['errors'])+'\n'
(a.root/'HIDDEN-SUITE-INVENTORY.txt').write_text(text)
print(f"PASS merged {len(reports)} homes: entries={len(d['found'])} roots={len(d['locks'])} errors={len(d['errors'])}")
