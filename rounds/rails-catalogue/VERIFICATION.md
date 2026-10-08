# rails-catalogue verification

Recomputed 6 October 2026 from the public [`results/cells.jsonl`](../../results/cells.jsonl) export. This check uses the public cell export only; it does not read an external grade ledger.

## Reproduction code

```python
import json, re
from collections import Counter
from decimal import Decimal
from pathlib import Path

EXPORT = Path("results/cells.jsonl")
README = Path("rounds/rails-catalogue/README.md")
POOL_ROUNDS = {"r60", "r60b", "r63", "r63b", "r64", "r64b", "r64c"}
COHORTS = {
    "Plan-shell": {("r64", "kh-plan-shell"), ("r64b", "kh-plan-shell")},
    "Sol high": {("r60", "Codex-Sol-high"), ("r60b", "Codex-Sol-high"), ("r64b", "Codex-Sol-high")},
    "Luna max": {("r60", "Codex-Luna-max"), ("r60b", "Codex-Luna-max")},
}

tasks = set(re.findall(r"\(\.\./\.\./tasks/([^/]+)/task\.json\)", README.read_text()))
rows = [json.loads(s) for s in EXPORT.read_text().splitlines()]
for name, keys in COHORTS.items():
    selected = [r for r in rows
                if r.get("round") in POOL_ROUNDS
                and r.get("task") in tasks
                and (r["round"], r.get("arm", "").split(":")[-1]) in keys]
    outcomes = Counter(r.get("ITT outcome") for r in selected)
    costs = [Decimal(str(r["usd_est"])) for r in selected
             if isinstance(r.get("usd_est"), (int, float))]
    total_cost = sum(costs, Decimal("0"))
    passes = outcomes.get("pass", 0)
    n = len(selected)
    print(name, "rows", n, "outcomes", dict(sorted(outcomes.items())))
    print(name, "recorded USD", f"{total_cost:.6f}",
          "export USD/pass", f"{total_cost / passes:.6f}" if passes else "N/A")
```

## Output

```text
Plan-shell rows 65 outcomes {'fail': 11, 'pass': 52, 'unresolved': 2}
Plan-shell recorded USD 6.192018 export USD/pass 0.119077
Sol high rows 81 outcomes {'fail': 31, 'pass': 50}
Sol high recorded USD 34.019188 export USD/pass 0.680384
Luna max rows 64 outcomes {'fail': 37, 'pass': 27}
Luna max recorded USD 1.919042 export USD/pass 0.071076
```

The historical denominators 85/85/68 are source-reported, not reproducible from public data. The corresponding historical API-equivalent USD/pass values 0.176370/0.793775/0.122729 are also source-reported, not reproducible from public data. The public export arithmetic shown above can be recomputed from `usd_est`, but the historical price table and calculator are not included. The source-reported p-values 0.403743 and 0.000329 are not reproducible because the test method and comparison family are not recorded.
