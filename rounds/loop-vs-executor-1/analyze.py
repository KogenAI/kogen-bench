#!/usr/bin/env python3
"""Recompute every number on the loop-vs-executor-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/loop-vs-executor-1/analyze.py [--write]

It reads only rounds/loop-vs-executor-1/ (each bundle's attempt.json and evaluation.json, and executor-usage.json),
uses the Python standard library, makes no model call and needs no private data. Without --write it prints the
tables; with --write it also writes results.txt next to itself.

Definitions. A cell "passed" when its build landed and every hidden test of its task passed. Lane names are
<arm>-<machine>: arm native (Kogen's own build loop) or cc (the Claude Code executor), machine m1 to m4 (four
machines, see README.md). A "pair" is a task, a machine and a repetition number for which both arms have a graded
cell; the comparison uses pairs only, so a cell whose partner never finished does not tilt it. The sign test follows
the registered rule: per task, count the pair passes of each arm (all machines pooled); the arm with more passes on a
task is favoured there; ties are dropped; p is the exact one-sided binomial P(X >= k) with n = k + m, reported in
both directions. The same test is also run on each machine alone.
A "plumbing" cell (listed with its reason in void-cells.json) stopped for a reason outside the model's work: the start
check failed before any build, or a memory cap stopped the cell. The tables show cells as run and again without them; a pair with a plumbing cell on either side is
left out of the second reading. "Extra executor repetitions" are executor cells run without a native partner by
design (unpaired-cells.json); they are never part of the pairs or the sign test and are reported apart.
"""
import glob
import json
import os
import sys
from math import comb
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
MACHINES = ("m1", "m2", "m3", "m4")


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
    global PLUMB, EXTRA
    PLUMB = json.load(open(os.path.join(HERE, "void-cells.json")))["cells"]
    EXTRA = set(json.load(open(os.path.join(HERE, "unpaired-cells.json")))["cells"])
    cells = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        arm, machine = a["lane"].split("-", 1)
        st = {s["stage"]: s for s in a["stages"]}
        ids = e.get("ids") or {"passed_count": 0, "failed_count": 0, "other_count": 0}
        c = {"cell": a["cell"], "task": task, "arm": arm, "machine": machine, "rep": int(a["cell"].split("/")[1][1:]),
             "outcome": a["outcome"],
             "pass": a["outcome"] == "landed" and bool(e["all_passed"]), "passed": ids["passed_count"],
             "total": ids["passed_count"] + ids["failed_count"] + ids["other_count"], "wall": a.get("wall_s"),
             "plumbing": PLUMB.get(a["cell"]), "extra": a["cell"] in EXTRA,
             "build_wall": st.get("build", {}).get("wall_s"), "review_wall": st.get("review", {}).get("wall_s"),
             "review_cost": st.get("review", {}).get("cost_usd"), "review_in": st.get("review", {}).get("input_tokens"),
             "review_out": st.get("review", {}).get("output_tokens")}
        if arm == "native":
            b = st.get("build") or {}
            c.update(b_in=b.get("input_tokens"), b_out=b.get("output_tokens"), b_cost=b.get("cost_usd"), b_req=b.get("requests"))
        else:
            u = usage.get(a["cell"])
            u = u and u.get("build")
            c.update(b_in=u and u["input_tokens"], b_out=u and u["output_tokens"], b_cost=u and u["estimate_usd"], b_req=None)
        cells.append(c)
    return cells


def tot(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs)


def fmt(x, d=0):
    return "n/a" if x is None else f"{x:,.{d}f}"


def pairs_of(cells):
    """(task, machine, rep) -> {arm: cell} for keys where both arms have a cell."""
    by = defaultdict(dict)
    for c in cells:
        if not c["extra"]:
            by[(c["task"], c["machine"], c["rep"])][c["arm"]] = c
    return {k: v for k, v in by.items() if len(v) == 2}


def sign(pairs, keep, label):
    """Sign test over tasks on the pairs whose task is in keep; returns the printed line."""
    n, k = defaultdict(int), defaultdict(int)
    for (t, _, _), v in pairs.items():
        if t in keep:
            n[t] += v["native"]["pass"]
            k[t] += v["cc"]["pass"]
    cc_t = sum(k[t] > n[t] for t in n)
    nat_t = sum(n[t] > k[t] for t in n)
    ties = len(n) - cc_t - nat_t
    pn, pc = sum(n.values()), sum(k.values())
    cnt = sum(1 for (t, _, _) in pairs if t in keep)
    say(f"Sign test, {label}: {len(n)} tasks, {cnt} pairs; cc favoured on {cc_t} tasks, native on {nat_t}, ties {ties}; "
        f"pair passes native {pn}/{cnt} = {pn / cnt:.3f}, cc {pc}/{cnt} = {pc / cnt:.3f}; "
        f"one-sided p (cc better) {p_upper(cc_t, cc_t + nat_t):.4f}, (native better) {p_upper(nat_t, cc_t + nat_t):.4f}.")


def main():
    allcells = load()
    extra = [c for c in allcells if c["extra"]]
    cells = [c for c in allcells if not c["extra"]]
    tasks = sorted({c["task"] for c in cells})
    pairs = pairs_of(cells)
    paired_cells = {c["cell"] for v in pairs.values() for c in v.values()}
    total = {t: max(c["total"] for c in cells if c["task"] == t) for t in tasks}
    voidcells = {c["cell"] for c in cells if c["plumbing"]}
    pairs_nv = {k: v for k, v in pairs.items() if not any(c["plumbing"] for c in v.values())}
    say("## Cells and passes, as run")
    say()
    say("| Machine | Arm | Cells | Passed every hidden test | Cells without plumbing cells | Passed, of those |")
    say("| --- | --- | ---: | ---: | ---: | ---: |")
    for m in MACHINES + ("all",):
        for arm in ("native", "cc"):
            cs = [c for c in cells if (m == "all" or c["machine"] == m) and c["arm"] == arm]
            ok = [c for c in cs if not c["plumbing"]]
            say(f"| {m} | {arm} | {len(cs)} | {sum(c['pass'] for c in cs)} | {len(ok)} | {sum(c['pass'] for c in ok)} |")
    say()
    say(f"Cells without a partner (the other arm's cell with the same task, machine and repetition never finished): "
        f"{', '.join(sorted(c['cell'] for c in cells if c['cell'] not in paired_cells)) or 'none'}. "
        f"Pairs: {len(pairs)}.")
    say()
    reasons = defaultdict(int)
    for c in cells:
        if c["plumbing"]:
            reasons[(c["plumbing"], c["machine"], c["arm"])] += 1
    say("Plumbing cells (stopped outside the model's work; reason, machine, arm: cells): "
        + ("; ".join(f"{r} on {m} ({a}): {n}" for (r, m, a), n in sorted(reasons.items())) or "none")
        + f". Total {len(voidcells)} of {len(cells)} cells; {len(pairs) - len(pairs_nv)} of {len(pairs)} pairs lose a cell to them.")
    say()
    say("Extra executor repetitions (executor cells with no native partner by design): "
        f"{len(extra)} cells, {sum(c['pass'] for c in extra)} passed, "
        f"{sum(1 for c in extra if c['plumbing'])} plumbing.")
    say()
    say("## Per task (pairs only, all machines pooled)")
    say()
    say("| Task | Machines | Hidden tests | Pairs | native passed | cc passed | Favours | Hidden tests passed, native | Hidden tests passed, cc |")
    say("| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |")
    for t in tasks:
        ks = [k for k in pairs if k[0] == t]
        n = sum(pairs[k]["native"]["pass"] for k in ks)
        k_ = sum(pairs[k]["cc"]["pass"] for k in ks)
        fav = "cc" if k_ > n else "native" if n > k_ else "tie"
        ms = "+".join(sorted({k[1] for k in ks}))
        tn = sum(pairs[k]["native"]["passed"] for k in ks)
        tc = sum(pairs[k]["cc"]["passed"] for k in ks)
        tt = sum(pairs[k]["cc"]["total"] for k in ks)
        sh = (lambda x: f"{x / tt:.1%}" if tt else "n/a")
        say(f"| `{t}` | {ms or 'none'} | {total[t]} | {len(ks)} | {n} | {k_} | {fav} | {sh(tn)} | {sh(tc)} |")
    say()
    say("## Sign test over tasks")
    say()
    keep_all = set(tasks)
    sign(pairs, keep_all, "all tasks, as run")
    sign(pairs_nv, keep_all, "without the plumbing cells")
    say()
    say("Per machine (the tasks that ran on that machine, its own pairs only):")
    say()
    for m in MACHINES:
        pm = {k: v for k, v in pairs.items() if k[1] == m}
        sign(pm, {k[0] for k in pm}, f"machine {m}, as run")
    for m in MACHINES:
        pm = {k: v for k, v in pairs_nv.items() if k[1] == m}
        sign(pm, {k[0] for k in pm}, f"machine {m}, without the plumbing cells")
    say()
    say("## Cells that did not pass every hidden test")
    say()
    say("| Cell | Outcome | Plumbing reason | Hidden tests passed |")
    say("| --- | --- | --- | ---: |")
    for c in allcells:
        if not c["pass"]:
            say(f"| `{c['cell']}` | {c['outcome']} | {c['plumbing'] or ''} | {c['passed']} of {c['total']} |")
    say()
    say("## Wall time (seconds per cell; build stage is the build command)")
    say()
    say("| Set | Arm | Cells | Median cell | Sum, cell | Median build | Sum, build |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    sets = [("all cells", lambda c: True), ("without the plumbing cells", lambda c: c["cell"] not in voidcells)]
    sets += [(f"machine {m}, without the plumbing cells", (lambda m: lambda c: c["machine"] == m and c["cell"] not in voidcells)(m)) for m in MACHINES]
    for name, f in sets:
        for arm in ("native", "cc"):
            cs = [c for c in cells if f(c) and c["arm"] == arm]
            say(f"| {name} | {arm} | {len(cs)} | {fmt(median([c['wall'] for c in cs]))} | {fmt(tot([c['wall'] for c in cs]))} | "
                f"{fmt(median([c['build_wall'] for c in cs]))} | {fmt(tot([c['build_wall'] for c in cs]))} |")
    say()
    say("Per-task median cell wall time ratio, cc over native (all cells of the task, plumbing cells left out):")
    ratios = []
    for t in tasks:
        a = median([c["wall"] for c in cells if c["task"] == t and c["arm"] == "cc" and c["cell"] not in voidcells])
        b = median([c["wall"] for c in cells if c["task"] == t and c["arm"] == "native" and c["cell"] not in voidcells])
        if a is not None and b is not None:
            ratios.append(a / b)
    say(f"median {median(ratios):.2f}, cc faster on {sum(r < 1 for r in ratios)} of {len(ratios)} tasks, slower on {sum(r > 1 for r in ratios)}.")
    say()
    say("## Build tokens and cost (build stage only; the Opus review is native in both arms)")
    say()
    say("Native: Kogen's own request log, list prices. cc: harness-reported tokens from Kogen's executor line, and Claude Code's own cost estimate, which is an estimate and not a bill. Input tokens include cached input and are summed over requests (native) or turns (cc), so they are comparable only roughly.")
    say()
    say("| Set | Arm | Cells | Median input | Median output | Sum input | Sum output | Sum cost, USD | Median cost, USD |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, f in [("all cells with a build, plumbing cells left out", lambda c: not c["plumbing"])]:
        for arm in ("native", "cc"):
            cs = [c for c in cells if f(c) and c["arm"] == arm and c["b_in"] is not None]
            say(f"| {name} | {arm} | {len(cs)} | {fmt(median([c['b_in'] for c in cs]))} | {fmt(median([c['b_out'] for c in cs]))} | "
                f"{fmt(tot([c['b_in'] for c in cs]))} | {fmt(tot([c['b_out'] for c in cs]))} | {fmt(tot([c['b_cost'] for c in cs]), 2)} | {fmt(median([c['b_cost'] for c in cs]), 3)} |")
    say()
    rin, rout = [], []
    for t in tasks:
        a = [c for c in cells if c["task"] == t and c["arm"] == "cc" and c["b_in"] is not None and not c["plumbing"]]
        b = [c for c in cells if c["task"] == t and c["arm"] == "native" and c["b_in"] is not None and not c["plumbing"]]
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
        cs = [c for c in cells if c["arm"] == arm and c["review_cost"] is not None and not c["plumbing"]]
        say(f"| {arm} | {len(cs)} | {fmt(tot([c['review_in'] for c in cs]))} | {fmt(tot([c['review_out'] for c in cs]))} | {fmt(tot([c['review_cost'] for c in cs]), 2)} | {fmt(median([c['review_cost'] for c in cs]), 3)} |")
    say()
    say("## Native arm, list-price cost per cell (build plus review)")
    say()
    cs = [c for c in cells if c["arm"] == "native" and not c["plumbing"]]
    allc = [(c["b_cost"] or 0) + (c["review_cost"] or 0) for c in cs]
    say(f"{len(cs)} cells: sum {sum(allc):.2f} USD, median {median(allc):.3f} USD, mean {sum(allc) / len(allc):.3f} USD.")
    say()
    say("## Extra executor repetitions (executor arm only, no native partner; not in the sign test)")
    say()
    say("Per task: the executor cells of the paired design (plumbing cells left out) against the extra repetitions (plumbing cells left out). Wall time is the whole cell.")
    say()
    say("| Task | Paired-design executor cells | Passed | Extra cells | Passed | Plumbing cells among extra | Median cell wall, extra | Median cell wall, paired-design |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    ex_tasks = sorted({c["task"] for c in extra})
    for t in ex_tasks:
        pd = [c for c in cells if c["task"] == t and c["arm"] == "cc" and not c["plumbing"]]
        ex = [c for c in extra if c["task"] == t and not c["plumbing"]]
        say(f"| `{t}` | {len(pd)} | {sum(c['pass'] for c in pd)} | {len(ex)} | {sum(c['pass'] for c in ex)} | "
            f"{sum(1 for c in extra if c['task'] == t and c['plumbing'])} | {fmt(median([c['wall'] for c in ex]))} | {fmt(median([c['wall'] for c in pd]))} |")
    say()
    say("| Machine | Extra cells | Plumbing | Passed (of the rest) | Median cell wall |")
    say("| --- | ---: | ---: | ---: | ---: |")
    for m in MACHINES:
        ex = [c for c in extra if c["machine"] == m]
        if ex:
            ok = [c for c in ex if not c["plumbing"]]
            say(f"| {m} | {len(ex)} | {len(ex) - len(ok)} | {sum(c['pass'] for c in ok)} of {len(ok)} | {fmt(median([c['wall'] for c in ok]))} |")
    ok = [c for c in extra if not c["plumbing"]]
    pd = [c for c in cells if c["arm"] == "cc" and not c["plumbing"] and c["task"] in ex_tasks]
    say()
    pdw = median([c["wall"] for c in pd])
    say(f"Median cell wall time of the extra cells {fmt(median([c['wall'] for c in ok]))} s against {fmt(pdw)} s for the paired-design executor cells on the same tasks. "
        "The machines differ (the extra repetitions ran on three machines at other times), so this is a rough comparison.")
    say()
    say(f"All extra cells: {len(extra)}; plumbing {len(extra) - len(ok)}; passed {sum(c['pass'] for c in ok)} of {len(ok)}. "
        f"The executor cells of the paired design on the same tasks (plumbing left out): {sum(c['pass'] for c in pd)} of {len(pd)}.")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
