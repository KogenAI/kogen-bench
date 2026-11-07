import json, pathlib
r = json.loads((pathlib.Path(__file__).parent / "data.json").read_text())
for x in r: print(x["case"], int(x["baseline_ready"]), int(x["candidate_ready"]))
print("ready", sum(x["baseline_ready"] for x in r), sum(x["candidate_ready"] for x in r), "of", len(r))
