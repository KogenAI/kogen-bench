#!/usr/bin/env python3
"""Recompute the published numbers from runs.csv (counted rows only). Usage: python3 analyze.py [runs.csv]"""
import csv, math, statistics, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(sys.argv[1] if len(sys.argv) > 1 else here / "runs.csv")))
tasks = [t for t in (here / "tasks.txt").read_text().split() if t != "ledger-go"]
ARMS = ["overlap", "serial", "codex"]
LABEL = {"overlap": "A overlap", "serial": "B serial", "codex": "C Codex CLI"}
cells = {}
for r in rows:
    if r["stratum"] != "counted":
        continue
    cells[(r["task"], int(r["rep"]), r["arm"])] = dict(
        passed=r["passed"] == "1", wall=float(r["wall_s"]), requests=int(r["requests"]),
        tool_calls=int(r["tool_calls"]), usd=float(r["cost_usd"]),
        early=None if r["early_tool_starts"] == "" else int(r["early_tool_starts"]),
        hidden=None if r["hidden_tool_s"] == "" else float(r["hidden_tool_s"]))
blocks = [(t, k) for k in (1, 2, 3) for t in tasks]
done = [b for b in blocks if all((*b, a) in cells for a in ARMS)]

def p90(v):
    v = sorted(v); return v[max(0, math.ceil(.9 * len(v)) - 1)]

def test(w, l, n):
    m = w + l; k = min(w, l)
    p = 1.0 if m == 0 else min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)
    return w, l, n - m, p

def sign(a, b):
    return test(sum(x < y for x, y in zip(a, b)), sum(x > y for x, y in zip(a, b)), len(a))

def cpp(x):
    return x["usd"] if x["passed"] else math.inf

g = lambda t: f"{t[0]}/{t[1]}, {t[2]} ties, p={t[3]:.4f}"
print(f"Counted cells {len(cells)}, complete blocks {len(done)} ({len(tasks)} tasks x 3 repetitions)")
print()
print("Per arm (counted cells):")
for a in ARMS:
    xs = [cells[(*b, a)] for b in blocks]
    w = [x["wall"] for x in xs]; ps = sum(x["passed"] for x in xs); tot = sum(x["usd"] for x in xs)
    line = (f"{LABEL[a]}: pass {ps}/{len(xs)}, wall median {statistics.median(w):.1f} p90 {p90(w):.1f} mean {statistics.mean(w):.1f}, "
            f"requests/run {statistics.mean(x['requests'] for x in xs):.1f}, tool calls/run {statistics.mean(x['tool_calls'] for x in xs):.1f}, "
            f"USD {tot:.4f}, per pass {tot / ps:.4f}")
    tr = [x for x in xs if x["early"] is not None]
    if tr:
        line += (f", cells with an early tool start {sum(1 for x in tr if x['early'])}/{len(tr)}, early starts/run "
                 f"{statistics.mean(x['early'] for x in tr):.2f}, tool s hidden behind streaming/run {statistics.mean(x['hidden'] for x in tr):.2f}")
    print(line)
print()
print("Paired by block (first wins / second wins; exact two-sided sign test; geometric-mean wall ratio, first over second, with normal 95% CI):")
for a, b in (("overlap", "serial"), ("overlap", "codex"), ("serial", "codex")):
    res = {}
    for m, fn in (("wall", lambda x: x["wall"]), ("requests", lambda x: x["requests"]), ("cost per pass", cpp)):
        res[m] = sign([fn(cells[(*k, a)]) for k in done], [fn(cells[(*k, b)]) for k in done])
    da = [cells[(*k, a)]["passed"] for k in done]; db = [cells[(*k, b)]["passed"] for k in done]
    res["pass"] = test(sum(x and not y for x, y in zip(da, db)), sum(y and not x for x, y in zip(da, db)), len(done))
    lr = [math.log(cells[(*k, a)]["wall"] / cells[(*k, b)]["wall"]) for k in done]
    mu = sum(lr) / len(lr); se = statistics.stdev(lr) / math.sqrt(len(lr))
    print(f"{LABEL[a]} vs {LABEL[b]} ({len(done)} blocks): wall {g(res['wall'])}; ratio {math.exp(mu):.3f} [{math.exp(mu - 1.96 * se):.3f}, {math.exp(mu + 1.96 * se):.3f}]; "
          f"requests {g(res['requests'])}; cost per pass {g(res['cost per pass'])}; pass {g(res['pass'])}")
print()
print("By task, A overlap vs B serial (wall wins / losses, geometric-mean wall ratio):")
for t in tasks:
    ks = [k for k in done if k[0] == t]
    s = sign([cells[(*k, "overlap")]["wall"] for k in ks], [cells[(*k, "serial")]["wall"] for k in ks])
    ratio = math.exp(sum(math.log(cells[(*k, "overlap")]["wall"] / cells[(*k, "serial")]["wall"]) for k in ks) / len(ks))
    print(f"{t}: {g(s)}, ratio {ratio:.3f}")
