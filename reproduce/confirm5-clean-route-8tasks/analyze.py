#!/usr/bin/env python3
"""Recompute the confirm5 (8-task, both tools on the same OpenAI API key) numbers from runs.csv."""
import csv, math, pathlib, statistics

HERE = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "runs.csv", newline="")))
for r in rows:
    for k in ("cost_usd", "wall_s"):
        r[k] = float(r[k])
    r["passed"] = r["passed"] == "true"
# Corrected comparison: original runs plus the reruns that replaced the
# four budget-censored and two byte-censored attempts.
runs = [r for r in rows if r["disposition"] in ("counted", "counted-rerun")]
tasks = [t.strip() for t in open(HERE / "tasks.txt") if t.strip()]
assert len(runs) == 32 and len({(r["task"], r["tool"], r["effort"]) for r in runs}) == 32


def sign(diffs):
    lo = sum(d < 0 for d in diffs); hi = sum(d > 0 for d in diffs); n = lo + hi
    p = min(1.0, 2 * sum(math.comb(n, k) for k in range(min(lo, hi) + 1)) / 2 ** n) if n else 1.0
    return lo, hi, len(diffs) - n, p


def get(task, tool, effort):
    return next(r for r in runs if (r["task"], r["tool"], r["effort"]) == (task, tool, effort))


print("tool    effort  pass/graded  clean  median/p90 wall s  total USD  USD/pass")
per_pass = {}
for effort in ("medium", "high"):
    for tool in ("loop", "codex"):
        a = [r for r in runs if r["tool"] == tool and r["effort"] == effort]
        walls = sorted(r["wall_s"] for r in a)
        passes = sum(r["passed"] for r in a)
        usd = sum(r["cost_usd"] for r in a)
        per_pass[tool, effort] = usd / passes
        print(f"{tool:<7} {effort:<7} {passes}/{len(a):<10} {sum(r['outcome'] == 'finished' for r in a):<6} "
              f"{statistics.median(walls):.2f} / {walls[math.ceil(.9 * len(walls)) - 1]:.2f}    "
              f"${usd:.6f}  ${usd / passes:.6f}")
print()
for effort in ("medium", "high"):
    pairs = [(get(t, "loop", effort), get(t, "codex", effort)) for t in tasks]
    wall_ratio = sum(l["wall_s"] for l, _ in pairs) / sum(c["wall_s"] for _, c in pairs)
    cost_ratio = per_pass["loop", effort] / per_pass["codex", effort]
    print(f"{effort.upper()}: loop/Codex mean-wall ratio {wall_ratio:.3f}; USD/pass ratio {cost_ratio:.3f} "
          f"(loop {abs(1 - cost_ratio) * 100:.2f}% {'lower' if cost_ratio < 1 else 'higher'})")
    for name, key in (("wall", "wall_s"), ("USD", "cost_usd")):
        lo, hi, ties, p = sign([l[key] - c[key] for l, c in pairs])
        print(f"  {name:<4} loop lower {lo}/8, Codex lower {hi}/8, ties {ties}, exact two-sided sign p={p:.6f}")
    lo, hi, ties, p = sign([int(c["passed"]) - int(l["passed"]) for l, c in pairs])
    print(f"  pass loop {sum(l['passed'] for l, _ in pairs)}/8, Codex {sum(c['passed'] for _, c in pairs)}/8, discordant {lo + hi}, p={p:.6f}")
print()
print(f"corrected comparison USD {sum(r['cost_usd'] for r in runs):.6f}; "
      f"all attempts incl. superseded USD {sum(r['cost_usd'] for r in rows):.6f} over {len(rows)} attempts")
