import json,pathlib
r=json.loads((pathlib.Path(__file__).parent / "data/results.json").read_text())
for group in ("small", "complex"):
 a=[x for x in r if x["group"]==group]; print(group, sum(x["ready"] and not x["questions_asked"] for x in a), "/", len(a))
print("total",sum(x["ready"] and not x["questions_asked"] for x in r),"/",len(r))
