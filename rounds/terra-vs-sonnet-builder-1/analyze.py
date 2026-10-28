#!/usr/bin/env python3
"""Recompute every number on the terra-vs-sonnet-builder-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/terra-vs-sonnet-builder-1/analyze.py [--write] [--check-comparator]

It reads only this round's files: the T-arm bundles (attempt.json and evaluation.json per cell), void-cells.json and
comparator.json. comparator.json holds one row per partner cell of the S arm, copied from the cc lane of
rounds/loop-vs-executor-1 (already published). --check-comparator rebuilds those rows from that round's bundles and
fails if they differ; it needs the whole repository. No model call, standard library only. --write also writes
results.txt next to this file.

Definitions. T = Terra at high effort as the builder (lane terra-high-<machine>); S = Claude Sonnet 5.5 at medium
effort as the builder, run through the Claude Code executor (lane cc-<machine> of loop-vs-executor-1). Review is
Claude Opus 5.5 medium in both arms. A cell "passed" when the build landed and every hidden test of its task passed.
A "pair" is a task, a repetition number and a machine for which both arms have a graded cell. Sign test (registered
rule): per task count the pair passes of each arm; the arm with more passes on a task is favoured there; ties are
dropped; p is the exact one-sided binomial P(X >= k) with n = k + m, in both directions. The rule calls one arm better
when p <= 0.10 and the pass-rate gap over pairs is above 0.15. A "plumbing" cell (void-cells.json of each arm) stopped
for a reason outside the model's work: the start check failed, a memory cap stopped it, or the provider rejected the
review request. Readings are shown as run and without the pairs that have a plumbing cell on either side.
"""
import glob
import json
import os
import sys
from collections import defaultdict
from math import comb

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


def fmt(x, d=0):
    return "n/a" if x is None else f"{x:,.{d}f}"


def total(xs):
    return sum(x for x in xs if isinstance(x, (int, float)))


def cells_of(root, plumb):
    """Cells of one round directory: cell id -> record."""
    out = {}
    for f in sorted(glob.glob(os.path.join(root, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        ids = e.get("ids") or {"passed_count": 0, "failed_count": 0, "other_count": 0}
        st = {s["stage"]: s for s in a["stages"]}
        b = st.get("build") or {}
        out[a["cell"]] = {"cell": a["cell"], "outcome": a["outcome"], "pass": a["outcome"] == "landed" and bool(e["all_passed"]),
                          "passed": ids["passed_count"], "total": ids["passed_count"] + ids["failed_count"] + ids["other_count"],
                          "wall": a.get("wall_s"), "build_wall": b.get("wall_s"), "plumbing": plumb.get(a["cell"]),
                          "b_in": b.get("input_tokens"), "b_cached": b.get("cached_input_tokens"), "b_out": b.get("output_tokens"),
                          "b_req": b.get("requests")}
    return out


def partner_id(cell):
    task, rep, lane = cell.split("/")
    return f"{task}/{rep}/cc-{lane.rsplit('-', 1)[1]}"


def build_comparator(t_cells):
    root = os.path.join(HERE, "..", "loop-vs-executor-1")
    plumb = json.load(open(os.path.join(root, "void-cells.json")))["cells"]
    s = cells_of(root, plumb)
    rows = {}
    for c in t_cells:
        sid = partner_id(c)
        if sid in s:
            r = s[sid]
            rows[sid] = {k: r[k] for k in ("cell", "outcome", "pass", "passed", "total", "wall", "build_wall", "plumbing")}
    return {"note": "Partner cells of the S arm (Claude Sonnet 5.5 medium through the Claude Code executor, review Opus 5.5 medium): one row per cell of the cc lane of rounds/loop-vs-executor-1 with the same task, repetition and machine as a Terra cell of this round. Copied from that round's bundles and void-cells.json; python3 -I rounds/terra-vs-sonnet-builder-1/analyze.py --check-comparator rebuilds them.",
            "cells": dict(sorted(rows.items()))}


def sign(pairs, label):
    n, k = defaultdict(int), defaultdict(int)
    for (t, _, _), (tc, sc) in pairs.items():
        n[t] += sc["pass"]
        k[t] += tc["pass"]
    t_t = sum(k[t] > n[t] for t in n)
    s_t = sum(n[t] > k[t] for t in n)
    ties = len(n) - t_t - s_t
    cnt = len(pairs)
    pt, ps = sum(k.values()), sum(n.values())
    gap = (pt - ps) / cnt if cnt else 0.0
    pT, pS = p_upper(t_t, t_t + s_t), p_upper(s_t, t_t + s_t)
    rule = "T better" if pT <= 0.10 and gap > 0.15 else "S better" if pS <= 0.10 and -gap > 0.15 else "on par (rule does not fire)"
    say(f"Sign test, {label}: {len(n)} tasks, {cnt} pairs; T favoured on {t_t} tasks, S on {s_t}, ties {ties}; "
        f"pair passes T {pt}/{cnt} = {pt / cnt:.3f}, S {ps}/{cnt} = {ps / cnt:.3f}, gap (T - S) {gap:+.3f}; "
        f"one-sided p (T better) {pT:.4f}, (S better) {pS:.4f}; reading: {rule}.")


def main():
    plumb_t = json.load(open(os.path.join(HERE, "void-cells.json")))["cells"]
    t_all = cells_of(HERE, plumb_t)
    comp = json.load(open(os.path.join(HERE, "comparator.json")))["cells"]
    if "--check-comparator" in sys.argv:
        want = build_comparator(t_all)["cells"]
        if want != comp:
            sys.exit("comparator.json differs from rounds/loop-vs-executor-1")
        print("comparator.json matches rounds/loop-vs-executor-1")
    pairs, s_only = {}, []
    for c, t in t_all.items():
        s = comp.get(partner_id(c))
        if s:
            task, rep, lane = c.split("/")
            pairs[(task, rep, lane.rsplit("-", 1)[1])] = (t, s)
        else:
            s_only.append(c)
    tasks = sorted({k[0] for k in pairs})
    tl = list(t_all.values())
    sl = [s for _, s in pairs.values()]
    pairs_nv = {k: v for k, v in pairs.items() if not (v[0]["plumbing"] or v[1]["plumbing"])}
    say("## Cells and passes")
    say()
    say(f"T cells graded: {len(tl)}; with an S partner: {len(pairs)}; without: {', '.join(s_only) or 'none'}.")
    say()
    say("| Machine | Pairs | T passed | S passed | Pairs without plumbing | T passed, of those | S passed, of those |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for m in ("m2", "m3", "m4", "all"):
        ps = [v for k, v in pairs.items() if m == "all" or k[2] == m]
        pn = [v for k, v in pairs_nv.items() if m == "all" or k[2] == m]
        say(f"| {m} | {len(ps)} | {sum(a['pass'] for a, _ in ps)} | {sum(b['pass'] for _, b in ps)} | {len(pn)} | "
            f"{sum(a['pass'] for a, _ in pn)} | {sum(b['pass'] for _, b in pn)} |")
    say()
    reasons = defaultdict(int)
    for c in tl:
        if c["plumbing"]:
            reasons[("T", c["plumbing"])] += 1
    for s in sl:
        if s["plumbing"]:
            reasons[("S", s["plumbing"])] += 1
    say("Plumbing cells in the pairs (arm, reason: cells): " + "; ".join(f"{a} {r}: {n}" for (a, r), n in sorted(reasons.items()))
        + f". {len(pairs) - len(pairs_nv)} of {len(pairs)} pairs lose a cell to them.")
    say()
    say("## Per task (pairs only)")
    say()
    say("| Task | Machine | Hidden tests | Pairs | T passed | S passed | Favours | Hidden tests passed, T | Hidden tests passed, S |")
    say("| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |")
    for t in tasks:
        ks = sorted(k for k in pairs if k[0] == t)
        a = sum(pairs[k][0]["pass"] for k in ks)
        b = sum(pairs[k][1]["pass"] for k in ks)
        tt = sum(pairs[k][1]["total"] for k in ks)
        hid = max(pairs[k][1]["total"] for k in ks)
        sh = lambda x: f"{x / tt:.1%}" if tt else "n/a"
        say(f"| `{t}` | {'+'.join(sorted({k[2] for k in ks}))} | {hid} | {len(ks)} | {a} | {b} | "
            f"{'T' if a > b else 'S' if b > a else 'tie'} | {sh(sum(pairs[k][0]['passed'] for k in ks))} | {sh(sum(pairs[k][1]['passed'] for k in ks))} |")
    say()
    say("## Sign test over tasks")
    say()
    sign(pairs, "as run")
    sign(pairs_nv, "without the pairs with a plumbing cell")
    for m in ("m2", "m3", "m4"):
        sign({k: v for k, v in pairs.items() if k[2] == m}, f"machine {m} alone, as run")
    say()
    say("## Cells that did not pass every hidden test (T arm, with the S partner)")
    say()
    say("| T cell | T outcome | T plumbing | T hidden tests passed | S partner outcome | S passed every test | S plumbing |")
    say("| --- | --- | --- | ---: | --- | --- | --- |")
    for k in sorted(pairs):
        t, s = pairs[k]
        if not t["pass"] or not s["pass"]:
            say(f"| `{t['cell']}` | {t['outcome']} | {t['plumbing'] or ''} | {t['passed']} of {t['total']} | {s['outcome']} | {'yes' if s['pass'] else 'no'} | {s['plumbing'] or ''} |")
    say()
    say("## Wall time (seconds per cell; build stage is the build command)")
    say()
    say("| Set | Arm | Cells | Median cell | Sum, cell | Median build | Sum, build |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for name, ps in (("all pairs", pairs), ("pairs without plumbing", pairs_nv)):
        for i, arm in ((0, "T"), (1, "S")):
            cs = [v[i] for v in ps.values()]
            say(f"| {name} | {arm} | {len(cs)} | {fmt(median([c['wall'] for c in cs]))} | {fmt(total([c['wall'] for c in cs]))} | "
                f"{fmt(median([c['build_wall'] for c in cs]))} | {fmt(total([c['build_wall'] for c in cs]))} |")
    for m in ("m2", "m3", "m4"):
        ps = {k: v for k, v in pairs_nv.items() if k[2] == m}
        for i, arm in ((0, "T"), (1, "S")):
            cs = [v[i] for v in ps.values()]
            say(f"| machine {m}, without plumbing | {arm} | {len(cs)} | {fmt(median([c['wall'] for c in cs]))} | {fmt(total([c['wall'] for c in cs]))} | "
                f"{fmt(median([c['build_wall'] for c in cs]))} | {fmt(total([c['build_wall'] for c in cs]))} |")
    say()
    ratios = []
    for t in tasks:
        a = median([v[0]["wall"] for k, v in pairs_nv.items() if k[0] == t])
        b = median([v[1]["wall"] for k, v in pairs_nv.items() if k[0] == t])
        if a is not None and b is not None:
            ratios.append(a / b)
    say(f"Per-task median cell wall time ratio, T over S (pairs without plumbing, {len(ratios)} tasks): median {median(ratios):.2f}, "
        f"T faster on {sum(r < 1 for r in ratios)} tasks, slower on {sum(r > 1 for r in ratios)}.")
    say()
    say("## T build tokens (Kogen's request log for the build stage; Terra has no list price, so no cost)")
    say()
    say("Input tokens include cached input and are summed over requests. S's own tokens (Claude Code's usage line) are in rounds/loop-vs-executor-1 and are measured differently, so no ratio is given.")
    say()
    say("| Set | Cells | Requests | Median input | Median cached | Median output | Sum input | Sum cached | Sum output |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    sets = [("all T cells with a build", [c for c in tl if c["b_in"] is not None]),
            ("without plumbing", [c for c in tl if c["b_in"] is not None and not c["plumbing"]])]
    for m in ("m2", "m3", "m4"):
        sets.append((f"machine {m}, without plumbing", [c for c in tl if c["b_in"] is not None and not c["plumbing"] and c["cell"].endswith(m)]))
    for name, cs in sets:
        say(f"| {name} | {len(cs)} | {fmt(total([c['b_req'] for c in cs]))} | {fmt(median([c['b_in'] for c in cs]))} | {fmt(median([c['b_cached'] for c in cs]))} | "
            f"{fmt(median([c['b_out'] for c in cs]))} | {fmt(total([c['b_in'] for c in cs]))} | {fmt(total([c['b_cached'] for c in cs]))} | {fmt(total([c['b_out'] for c in cs]))} |")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
