import json, pathlib
d = json.loads((pathlib.Path(__file__).parent / "data" / "results.json").read_text())
print(d["finding"], d["model"], d["effort"])
for p in d["pairs"]:
    print(f'{p["task"]:28} release {p["release"]}  candidate {p["candidate"]}  of {p["total"]}  valid_pair={p["valid_pair"]}')
valid = [p for p in d["pairs"] if p["valid_pair"]]
for k in ("release", "candidate"):
    print(k, "hidden mean over valid pairs:", round(sum(p[k] / p["total"] for p in valid) / len(valid), 4))
