#!/usr/bin/env python3
import collections,json
from pathlib import Path
rows=json.loads(Path(__file__).with_name("results.json").read_text())
pairs=collections.defaultdict(dict)
for r in rows: pairs[r["input"]][r["arm"]]=r
for key,pair in sorted(pairs.items()):
 b=pair["baseline"]; c=pair["candidate"]
 print(f"{key}\t{b['ready']}\t{b['exit_code']}\t{b['refusal']}\t{c['ready']}\t{c['exit_code']}\t{c['refusal']}")
controls=[p for k,p in pairs.items() if k.startswith("c")]
print("control ready:",sum(p["baseline"]["ready"] for p in controls),sum(p["candidate"]["ready"] for p in controls),"of",len(controls))
print("wall seconds, including failed and timed-out cells:",*(round(sum(r["wall_s"] for r in rows if r["arm"]==a),2) for a in ("baseline","candidate")))
