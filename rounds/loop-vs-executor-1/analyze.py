#!/usr/bin/env python3
"""Recompute every number on the loop-vs-executor-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/loop-vs-executor-1/analyze.py [--write]

It reads only rounds/loop-vs-executor-1/ (each bundle's attempt.json and evaluation.json, and executor-usage.json),
uses the Python standard library, makes no model call and needs no private data. Without --write it prints the
tables; with --write it also writes results.txt next to itself.

Definitions. A cell "passed" when its build landed and every hidden test of its task passed. Lane names are
<arm>-<machine>: arm native (Kogen's own build loop) or cc (the Claude Code executor), machine mac, linux-a or
linux-b. The sign test follows the registered rule: per task, count the cells each arm passed; the arm with more
passes on a task is favoured there; ties are dropped; p is the exact one-sided binomial P(X >= k) with n = k + m,
reported in both directions. A task whose own start check failed before the
build in every cell of both arms (found by the script) is void and is also shown excluded.
"""
import glob
import json
import os
import sys
from math import comb
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def say(text=""):
    OUT.append(text)
    print(text)


def median(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    m = len(xs) // 2
    return None if not xs else xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def p_upper(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def load():
    usage = json.load(open(os.path.join(HERE, "executor-usage.json")))["cells"]
    cells = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        arm, machine = a["lane"].split("-", 1)
        st = {s["stage"]: s for s in a["stages"]}
        ids = e["ids"]
        c = {"cell": a["cell"], "task": task, "arm": arm, "machine": machine, "outcome": a["outcome"],
             "pass": a["outcome"] == "landed" and bool(e["all_passed"]), "passed": ids["passed_count"],
             "total": ids["passed_count"] + ids["failed_count"] + ids["other_count"], "wall": a["wall_s"],
             "build_wall": st["build"]["wall_s"], "review_wall": st.get("review", {}).get("wall_s"),
             "review_cost": st.get("review", {}).get("cost_usd"), "review_in": st.get("review", {}).get("input_tokens"),
             "review_out": st.get("review", {}).get("output_tokens")}
        if arm == "native":
            b = st["build"]
            c.update(b_in=b["input_tokens"], b_out=b["output_tokens"], b_cost=b["cost_usd"], b_req=b["requests"])
        else:
            u = usage.get(a["cell"])
            u = u and u["build"]
            c.update(b_in=u and u["input_tokens"], b_out=u and u["output_tokens"], b_cost=u and u["estimate_usd"], b_req=None)
        cells.append(c)
    return cells


def tot(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs)


def fmt(x, d=0):
    return "n/a" if x is None else f"{x:,.{d}f}"


def main():
    cells = load()
    tasks = sorted({c["task"] for c in cells})
    mach = {t: next(c["machine"] for c in cells if c["task"] == t) for t in tasks}
    total = {t: next(c["total"] for c in cells if c["task"] == t and c["total"]) for t in tasks}
    VOID = {t for t in tasks if all(c["outcome"] == "check_failing" for c in cells if c["task"] == t)}
    say("## Cells and passes, as run")
    say()
    say("| Machine | Arm | Cells | Passed every hidden test |")
    say("| --- | --- | ---: | ---: |")
    for m in ("mac", "linux-a", "linux-b"):
        for arm in ("native", "cc"):
            cs = [c for c in cells if c["machine"] == m and c["arm"] == arm]
            say(f"| {m} | {arm} | {len(cs)} | {sum(c['pass'] for c in cs)} |")
    for arm in ("native", "cc"):
        cs = [c for c in cells if c["arm"] == arm]
        say(f"| all | {arm} | {len(cs)} | {sum(c['pass'] for c in cs)} |")
    say()
    say(f"Tasks whose start check failed before the build in every cell (void for both arms): {', '.join(sorted(VOID)) or 'none'}.")
    say()
    say("## Per task")
    say()
    say("| Task | Machine | Hidden tests | Reps | native passed | cc passed | Favours |")
    say("| --- | --- | ---: | ---: | ---: | ---: | --- |")
    fav = {}
    for t in tasks:
        n = sum(c["pass"] for c in cells if c["task"] == t and c["arm"] == "native")
        k = sum(c["pass"] for c in cells if c["task"] == t and c["arm"] == "cc")
        reps = sum(1 for c in cells if c["task"] == t and c["arm"] == "cc")
        fav[t] = "cc" if k > n else "native" if n > k else "tie"
        say(f"| `{t}` | {mach[t]} | {total[t]} | {reps} | {n} | {k} | {fav[t]} |")
    say()
    for label, keep in (("all 21 tasks, as run", tasks), ("without the void task", [t for t in tasks if t not in VOID])):
        k = sum(fav[t] == "cc" for t in keep)
        m = sum(fav[t] == "native" for t in keep)
        ties = sum(fav[t] == "tie" for t in keep)
        cn = [c for c in cells if c["task"] in keep and c["arm"] == "native"]
        cc = [c for c in cells if c["task"] in keep and c["arm"] == "cc"]
        rn, rc = sum(c["pass"] for c in cn) / len(cn), sum(c["pass"] for c in cc) / len(cc)
        say(f"Sign test, {label}: cc favoured on {k} tasks, native on {m}, ties {ties}; pass rate native {sum(c['pass'] for c in cn)}/{len(cn)} = {rn:.3f}, "
            f"cc {sum(c['pass'] for c in cc)}/{len(cc)} = {rc:.3f}; one-sided p (cc better) {p_upper(k, k + m):.4f}, (native better) {p_upper(m, k + m):.4f}.")
    say()
    say("## Cells that did not pass every hidden test")
    say()
    say("| Cell | Outcome | Hidden tests passed |")
    say("| --- | --- | ---: |")
    for c in cells:
        if not c["pass"]:
            say(f"| `{c['cell']}` | {c['outcome']} | {c['passed']} of {c['total']} |")
    say()
    say("## Wall time (seconds per cell; build stage is the build command)")
    say()
    say("| Set | Arm | Cells | Median cell | Sum, cell | Median build | Sum, build |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    sets = [("all cells", lambda c: True), ("without the void task", lambda c: c["task"] not in VOID),
            ("short tasks (mac, linux-a)", lambda c: c["machine"] != "linux-b"), ("linux-b tasks, without the void task", lambda c: c["machine"] == "linux-b" and c["task"] not in VOID)]
    for name, f in sets:
        for arm in ("native", "cc"):
            cs = [c for c in cells if f(c) and c["arm"] == arm]
            say(f"| {name} | {arm} | {len(cs)} | {fmt(median([c['wall'] for c in cs]))} | {fmt(tot([c['wall'] for c in cs]))} | "
                f"{fmt(median([c['build_wall'] for c in cs]))} | {fmt(tot([c['build_wall'] for c in cs]))} |")
    say()
    say("Per-task median cell wall time ratio, cc over native (tasks with every cell built, void task left out):")
    ratios = []
    for t in tasks:
        if t in VOID:
            continue
        a = median([c["wall"] for c in cells if c["task"] == t and c["arm"] == "cc"])
        b = median([c["wall"] for c in cells if c["task"] == t and c["arm"] == "native"])
        ratios.append(a / b)
    say(f"median {median(ratios):.2f}, cc faster on {sum(r < 1 for r in ratios)} of {len(ratios)} tasks, slower on {sum(r > 1 for r in ratios)}.")
    say()
    say("## Build tokens and cost (build stage only; the Opus review is native in both arms)")
    say()
    say("Native: Kogen's own request log, list prices. cc: harness-reported tokens from Kogen's executor line, and Claude Code's own cost estimate, which is an estimate and not a bill. Input tokens include cached input and are summed over requests (native) or turns (cc), so they are comparable only roughly.")
    say()
    say("| Set | Arm | Cells | Median input | Median output | Sum input | Sum output | Sum cost, USD | Median cost, USD |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, f in [("all cells with a build", lambda c: True)]:
        for arm in ("native", "cc"):
            cs = [c for c in cells if f(c) and c["arm"] == arm and c["b_in"] is not None]
            say(f"| {name} | {arm} | {len(cs)} | {fmt(median([c['b_in'] for c in cs]))} | {fmt(median([c['b_out'] for c in cs]))} | "
                f"{fmt(tot([c['b_in'] for c in cs]))} | {fmt(tot([c['b_out'] for c in cs]))} | {fmt(tot([c['b_cost'] for c in cs]), 2)} | {fmt(median([c['b_cost'] for c in cs]), 3)} |")
    say()
    rin, rout = [], []
    for t in tasks:
        a = [c for c in cells if c["task"] == t and c["arm"] == "cc" and c["b_in"] is not None]
        b = [c for c in cells if c["task"] == t and c["arm"] == "native" and c["b_in"] is not None]
        if a and b:
            rin.append(median([c["b_in"] for c in a]) / median([c["b_in"] for c in b]))
            rout.append(median([c["b_out"] for c in a]) / median([c["b_out"] for c in b]))
    say(f"Per-task ratio of median build tokens, cc over native ({len(rin)} tasks): input median {median(rin):.2f}, cc higher on {sum(r > 1 for r in rin)}; "
        f"output median {median(rout):.2f}, cc higher on {sum(r > 1 for r in rout)}.")
    say()
    say("## Review (Opus 5.5 medium, native in both arms), list price")
    say()
    say("| Arm | Cells reviewed | Sum input | Sum output | Sum cost, USD | Median cost, USD |")
    say("| --- | ---: | ---: | ---: | ---: | ---: |")
    for arm in ("native", "cc"):
        cs = [c for c in cells if c["arm"] == arm and c["review_cost"] is not None]
        say(f"| {arm} | {len(cs)} | {fmt(tot([c['review_in'] for c in cs]))} | {fmt(tot([c['review_out'] for c in cs]))} | {fmt(tot([c['review_cost'] for c in cs]), 2)} | {fmt(median([c['review_cost'] for c in cs]), 3)} |")
    say()
    say("## Native arm, list-price cost per cell (build plus review)")
    say()
    cs = [c for c in cells if c["arm"] == "native"]
    allc = [(c["b_cost"] or 0) + (c["review_cost"] or 0) for c in cs]
    say(f"{len(cs)} cells: sum {sum(allc):.2f} USD, median {median(allc):.3f} USD, mean {sum(allc) / len(allc):.3f} USD.")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
