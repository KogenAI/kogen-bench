"""Read the frozen scoring arithmetic and exclusion inventory."""
from pathlib import Path
import math

def counts(root=None):
    root = Path(root or Path(__file__).resolve().parent)
    values = dict(line.split("=", 1) for line in (root / "COUNTS.txt").read_text().splitlines() if line.strip())
    values = {key: int(value) for key, value in values.items()}
    exclusions = set((root / "SPEC-BUG-CASES.txt").read_text().split())
    assert values["excluded"] == len(exclusions)
    assert values["N_scored"] == values["N_total"] - len(exclusions)
    assert values["target"] == math.ceil(0.88 * values["N_scored"])
    return values, exclusions
