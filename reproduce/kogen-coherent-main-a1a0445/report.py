"""Replay the result summary from the pack; no model or network access."""
import json
from pathlib import Path
d=json.loads((Path(__file__).parent/"data.json").read_text())
print("verdict",d["metadata"]["verdict"],"finished_at",d["metadata"]["finished_at"])
for r in d["rows"]:
 print(r["task"],"Intent",int(r["candidate"]["valid_intent"]),"landed",int(r["candidate"]["landed"]),"hidden",int(r["candidate"]["hidden_all_pass"]),"stored",None if r["stored"] is None else r["stored"]["valid_intents"],"/",None if r["stored"] is None else r["stored"]["attempts"])
print("timeout_sensitivity_disagrees",d["metadata"]["timeout_sensitivity_disagrees"])
print("tokens",json.dumps(d["metadata"]["tokens"],sort_keys=True))
print("cell_wall_s",d["metadata"]["cell_wall_s"])
print("cost_usd",d["metadata"]["cost_usd"],d["metadata"]["cost_reason"])
