import json,sys
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text())
assert len(x["commits"])==7
assert x["tuple"]["kogen-executor"].startswith("2f13bd4")
assert x["build"]["exit_code"]==1
assert x["build"]["errors"]==["undefined: shape.Init","undefined: shape.InitInput"]
assert x["cells"]==x["model_requests"]==x["paid_screen_usd"]==0
assert x["qualified"] is False
print("UNRESOLVED: candidate does not compile; 0 cells; $0 paid screen cost; not qualified")
