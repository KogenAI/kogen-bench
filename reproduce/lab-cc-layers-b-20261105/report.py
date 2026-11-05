#!/usr/bin/env python3
"""report.py [cells.tsv]: rebuild every number of this finding's README from data/cells.tsv (no model calls)."""
import csv, math, os, sys
from math import comb

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cells.tsv")
rows = list(csv.DictReader(open(path), delimiter="\t"))
ARMS = ["loop", "claude-kexec", "claude-lean", "claude-c2"]
blocks = {}
for r in rows:
    blocks.setdefault(r["block"], {})[r["arm"]] = r

def toks(r):  # uncached-equivalent tokens: uncached input (incl. cache writes) + 0.1 x cache reads + 5 x output
    i, c, o = int(r["input"]), int(r["cached"]), int(r["output"])
    return (i - c) + 0.1 * c + 5 * o

def med(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

print("Per arm (all counted cells)")
print("arm            cells pass  checks     median_wall_s  mean_requests  list_usd  usd_per_pass  ktok_per_pass")
for a in ARMS:
    rs = [r for r in rows if r["arm"] == a]; p = sum(int(r["all_passed"]) for r in rs)
    ck = sum(int(r["passed"]) for r in rs), sum(int(r["expected"]) for r in rs)
    usd = sum(float(r["list_usd"]) for r in rs)
    print(f"{a:14s} {len(rs):5d} {p:4d}  {ck[0]:3d}/{ck[1]:3d}    {med([float(r['agent_wall_s']) for r in rs]):13.1f}  "
          f"{sum(int(r['requests']) for r in rs) / len(rs):13.1f}  {usd:8.2f}  {usd / p:12.3f}  {sum(toks(r) for r in rs) / p / 1000:13.0f}")

def sign_p(k, n):
    t = min(k, n - k)
    return min(1.0, 2 * sum(comb(n, i) for i in range(t + 1)) / 2 ** n)

def ci(xs, z):
    n = len(xs); m = sum(xs) / n; se = (sum((x - m) ** 2 for x in xs) / (n - 1)) ** 0.5 / n ** 0.5
    return math.exp(m), math.exp(m - z * se), math.exp(m + z * se)

print("\nPaired ratios a/b over blocks holding both arms (geometric means; CI = normal on per-block log ratios)")
PAIRS = [("loop", "claude-kexec", "primary", 2.241), ("loop", "claude-lean", "primary", 2.241),
         ("claude-kexec", "claude-lean", "secondary", 1.96), ("claude-c2", "claude-lean", "secondary", 1.96),
         ("loop", "claude-c2", "secondary", 1.96)]
for a, b, kind, z in PAIRS:
    bs = [k for k in sorted(blocks) if a in blocks[k] and b in blocks[k]]
    w = [math.log(float(blocks[k][a]["agent_wall_s"]) / float(blocks[k][b]["agent_wall_s"])) for k in bs]
    t = [math.log(toks(blocks[k][a]) / toks(blocks[k][b])) for k in bs]
    u = [math.log(float(blocks[k][a]["list_usd"]) / float(blocks[k][b]["list_usd"])) for k in bs]
    rq = sum(int(blocks[k][a]["requests"]) - int(blocks[k][b]["requests"]) for k in bs) / len(bs)
    k = sum(x < 0 for x in w); pc = "97.5%" if kind == "primary" else "95%"
    gw, gt, gu = ci(w, z), ci(t, z), ci(u, z)
    pa = sum(int(blocks[x][a]["all_passed"]) for x in bs); pb = sum(int(blocks[x][b]["all_passed"]) for x in bs)
    print(f"{a}/{b} ({kind}, {pc} CI, n={len(bs)}): wall {gw[0]:.3f} [{gw[1]:.3f}, {gw[2]:.3f}], {a} faster in {k}/{len(bs)}, "
          f"sign p={sign_p(k, len(bs)):.4f}; tokens {gt[0]:.3f} [{gt[1]:.3f}, {gt[2]:.3f}]; list USD {gu[0]:.3f} [{gu[1]:.3f}, {gu[2]:.3f}]; "
          f"requests {rq:+.1f} per block; pass {pa} vs {pb}")
print("\nFailed cells:", ", ".join(f"{r['task']} {r['rep']} {r['arm']} ({r['passed']}/{r['expected']})" for r in rows if r["all_passed"] == "0"))
