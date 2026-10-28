#!/usr/bin/env python3
"""Recompute every number on the shape-flawed-requests-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/shape-flawed-requests-1/analyze.py [--write]

It reads only this round's files: the bundle (attempt.json and evaluation.json of every cell), grades.json (the blind
grader's label counts per cell), grader-agreement.json (a second grader's labels on a sample) and shape-usage.json.
Standard library only, no model call, no private data. Without --write it prints the tables; with --write it also
writes results.txt next to this file.

Definitions. A "defect-cell" is one known defect of a case in one cell. The grader gives each defect-cell one label:
RESOLVED-STATED (the Intent states a result for the exposing input and nothing contradicts it), ASKED (the shaper
asked a question naming both conflicting statements and an example), SILENT (carried through unresolved) or NEW
(resolved to something that is neither accepted nor a named alternative). "Caught" = RESOLVED-STATED or ASKED. An
new-flaw hit (an "N-test" of the grader) is a new defect the grader found in the shaper's own output (beyond the known ones). Cells with status
infra-excluded (a memory cap stopped the cell before any output) are left out; a cell with no output counts every
defect as SILENT. The climb rule is the frozen one: per case, caught-rate of the lever minus caught-rate of the
baseline (both arms pooled over the case's repetitions, train half); sign test one-sided over cases with a non-zero
difference; "better" needs p <= 0.10, mean gain > 0.15 and mean change in new-flaw hits per cell <= 1; "worse" when the mean
gain is below zero or the new-flaw hits per cell rose; otherwise no change. Shape matrix: scenarios passing on the
reference solution, scenarios failing on the unchanged starting code, known-wrong variants caught by some scenario.
"""
import glob
import json
import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
ARMS = [("Baseline (Sonnet medium)", ("sonnet-medium-train", "sonnet-medium-test")),
        ("L1 (checklist)", ("sonnet-medium-checklist-train",)),
        ("L2 (Opus medium)", ("opus-medium-train",)),
        ("Sol low (reference)", ("sol-low-reference",))]
LANE_ARM = {lane: name for name, lanes in ARMS for lane in lanes}
CAUGHT = ("RESOLVED-STATED", "ASKED")


def say(text=""):
    OUT.append(text)
    print(text)


def median(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    m = len(xs) // 2
    return None if not xs else xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def p_upper(k, n):
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def fmt(x, d=0):
    return "n/a" if x is None else f"{x:,.{d}f}"


def load():
    g = json.load(open(os.path.join(HERE, "grades.json")))
    usage = json.load(open(os.path.join(HERE, "shape-usage.json")))["cells"]
    cells = {}
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        cid = a["cell"]
        case, rep, lane = cid.split("/")
        gr = g["cells"][cid]
        lab = gr.get("labels") or {}
        cells[cid] = {"cell": cid, "case": case, "rep": rep, "lane": lane, "arm": LANE_ARM[lane], "outcome": a["outcome"],
                      "wall": a.get("wall_s"), "status": gr["status"], "n": gr["known_defects"],
                      "caught": sum(lab.get(k, 0) for k in CAUGHT), "labels": lab, "nhits": gr.get("n_test_hits", 0),
                      "questions": gr.get("questions_asked", 0), "eval": e, "usage": usage.get(cid),
                      "half": g["cases"][case]["half"]}
    return g, cells


def graded(cells):
    return [c for c in cells if c["status"] in ("graded", "empty")]


def main():
    g, cells = load()
    cl = list(cells.values())
    cases = sorted(g["cases"])
    say("## Cells and grading")
    say()
    say("| Arm | Cells | Graded or empty | Excluded (memory cap) | Defect-cells | Caught | Caught rate | RESOLVED-STATED | ASKED | SILENT | NEW | new-flaw hits | new-flaw hits per cell | Cells with a question |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, lanes in ARMS:
        cs = [c for c in cl if c["arm"] == name]
        gc = graded(cs)
        n = sum(c["n"] for c in gc)
        cau = sum(c["caught"] for c in gc)
        lab = Counter()
        for c in gc:
            lab.update(c["labels"])
        nh = sum(c["nhits"] for c in gc)
        say(f"| {name} | {len(cs)} | {len(gc)} | {len(cs) - len(gc)} | {n} | {cau} | {cau / n:.2f} | {lab['RESOLVED-STATED']} | {lab['ASKED']} | {lab['SILENT']} | {lab['NEW']} | {nh} | {nh / len(gc):.2f} | "
            f"{sum(c['questions'] > 0 for c in gc)} |")
    say()
    for name, lanes in ARMS:
        for lane in lanes:
            cs = graded([c for c in cl if c["lane"] == lane])
            say(f"- {lane}: {len(cs)} cells, caught {sum(c['caught'] for c in cs)} of {sum(c['n'] for c in cs)}")
    say()
    say("## Per case and arm: caught defects over defect-cells (new-flaw hits)")
    say()
    say("| Case | Half | Known defects | " + " | ".join(n for n, _ in ARMS) + " |")
    say("| --- | --- | ---: | " + " | ".join("---:" for _ in ARMS) + " |")
    for case in cases:
        row = []
        for name, _ in ARMS:
            gc = graded([c for c in cl if c["case"] == case and c["arm"] == name])
            row.append(f"{sum(c['caught'] for c in gc)} of {sum(c['n'] for c in gc)} (new flaws {sum(c['nhits'] for c in gc)}, {len(gc)} cells)" if gc else "not graded")
        say(f"| `{case}` | {g['cases'][case]['half']} | {g['cases'][case]['known_defects']} | " + " | ".join(row) + " |")
    say()
    say("## Halves")
    say()
    say("| Arm | Train: caught of defect-cells | Test: caught of defect-cells |")
    say("| --- | ---: | ---: |")
    for name, _ in ARMS:
        r = []
        for h in ("train", "test"):
            gc = graded([c for c in cl if c["arm"] == name and c["half"] == h])
            r.append(f"{sum(c['caught'] for c in gc)} of {sum(c['n'] for c in gc)} ({len(gc)} cells)" if gc else "not run")
        say(f"| {name} | {r[0]} | {r[1]} |")
    say()
    say("## Shape outcomes (cells)")
    say()
    outs = sorted({c["outcome"] for c in cl})
    say("| Arm | " + " | ".join(outs) + " |")
    say("| --- | " + " | ".join("---:" for _ in outs) + " |")
    for name, _ in ARMS:
        cs = [c for c in cl if c["arm"] == name]
        say(f"| {name} | " + " | ".join(str(sum(c["outcome"] == o for c in cs)) for o in outs) + " |")
    say()
    say("## Shape matrix (cells that produced a graded Intent; sums over cells)")
    say()
    say("| Arm | Cells with scenarios | Scenarios | Passing on the reference | Failing on the starting code | Wrong variants caught | Wrong variants | Cells with every scenario passing on the reference |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, _ in ARMS:
        cs = [c for c in cl if c["arm"] == name and c["eval"].get("scenarios")]
        t = lambda k: sum(c["eval"].get(k, 0) for c in cs)
        say(f"| {name} | {len(cs)} | {t('scenarios')} | {t('pass_on_reference')} ({t('pass_on_reference') / t('scenarios'):.1%}) | {t('fail_on_start')} ({t('fail_on_start') / t('scenarios'):.1%}) | "
            f"{t('wrong_caught')} | {t('wrong_total')} ({t('wrong_caught') / t('wrong_total'):.1%}) | {sum(c['eval']['pass_on_reference'] == c['eval']['scenarios'] for c in cs)} |")
    say()
    say("Train half only, the cases the climb rule compares:")
    say()
    say("| Arm | Cells with scenarios | Scenarios | Passing on the reference | Failing on the starting code | Wrong variants caught | Wrong variants |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, _ in ARMS[:3]:
        cs = [c for c in cl if c["arm"] == name and c["half"] == "train" and c["eval"].get("scenarios")]
        t = lambda k: sum(c["eval"].get(k, 0) for c in cs)
        say(f"| {name} | {len(cs)} | {t('scenarios')} | {t('pass_on_reference')} | {t('fail_on_start')} | {t('wrong_caught')} | {t('wrong_total')} |")
    say()
    say("## Wall time and Claude Code tokens (shape stage; per cell)")
    say()
    say("| Arm | Cells | Median cell wall, s | Median input tokens (cached included) | Median output tokens |")
    say("| --- | ---: | ---: | ---: | ---: |")
    for name, _ in ARMS:
        cs = [c for c in cl if c["arm"] == name and c["status"] != "infra-excluded"]
        us = [c["usage"] for c in cs if c["usage"]]
        say(f"| {name} | {len(cs)} | {fmt(median([c['wall'] for c in cs]))} | {fmt(median([u['input'] for u in us])) if us else 'in bundle'} | {fmt(median([u['output'] for u in us])) if us else 'in bundle'} |")
    say()
    say("## Frozen climb rule, train half (per case, pooled over repetitions)")
    say()
    train = [c for c in cases if g["cases"][c]["half"] == "train"]
    base = "Baseline (Sonnet medium)"
    for lev in ("L2 (Opus medium)", "L1 (checklist)"):
        say(f"### {lev} against {base}")
        say()
        say("| Case | Baseline caught | Lever caught | Difference in caught rate | new-flaw hits per cell, baseline to lever |")
        say("| --- | ---: | ---: | ---: | --- |")
        diffs, dnew, floor = [], [], 0
        for case in train:
            b = graded([c for c in cl if c["case"] == case and c["arm"] == base])
            l = graded([c for c in cl if c["case"] == case and c["arm"] == lev])
            bc, bn, lc, ln = sum(c["caught"] for c in b), sum(c["n"] for c in b), sum(c["caught"] for c in l), sum(c["n"] for c in l)
            d = lc / ln - bc / bn
            diffs.append(d)
            bnh, lnh = sum(c["nhits"] for c in b) / len(b), sum(c["nhits"] for c in l) / len(l)
            dnew.append(lnh - bnh)
            floor += bc == 0 and lc == 0
            say(f"| `{case}` | {bc} of {bn} | {lc} of {ln} | {d:+.2f} | {bnh:.2f} to {lnh:.2f} |")
        pos, neg = sum(d > 0 for d in diffs), sum(d < 0 for d in diffs)
        p = p_upper(pos, pos + neg)
        mean, mnew = sum(diffs) / len(diffs), sum(dnew) / len(dnew)
        verdict = "better (replicate on test)" if p <= 0.10 and mean > 0.15 and mnew <= 1 else ("worse" if mean < 0 or mnew > 0 else "no change")
        say()
        say(f"{len(diffs)} cases: {pos} up, {neg} down, {len(diffs) - pos - neg} unchanged; one-sided sign test p = {p:.3f}; mean gain in caught rate {mean:+.3f}; "
            f"mean change in new-flaw hits per cell {mnew:+.2f}; cases at zero in both arms {floor}. Verdict under the frozen rule: **{verdict}**.")
        say()
    say("Pooled over all train cells: " + "; ".join(
        f"{n} caught {sum(c['caught'] for c in graded([c for c in cl if c['arm'] == n and c['half'] == 'train']))} of "
        f"{sum(c['n'] for c in graded([c for c in cl if c['arm'] == n and c['half'] == 'train']))}, new-flaw hits "
        f"{sum(c['nhits'] for c in graded([c for c in cl if c['arm'] == n and c['half'] == 'train']))} over "
        f"{len(graded([c for c in cl if c['arm'] == n and c['half'] == 'train']))} cells" for n in (base, "L1 (checklist)", "L2 (Opus medium)")) + ".")
    say()
    say("## Grader agreement")
    say()
    ag = json.load(open(os.path.join(HERE, "grader-agreement.json")))["cells"]
    A = [p[0] for v in ag.values() for p in v]
    B = [p[1] for v in ag.values() for p in v]
    n = len(A)
    po = sum(a == b for a, b in zip(A, B)) / n
    pe = sum((A.count(k) / n) * (B.count(k) / n) for k in set(A) | set(B))
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    cb = lambda L: ["C" if x in CAUGHT else "M" for x in L]
    A2, B2 = cb(A), cb(B)
    po2 = sum(a == b for a, b in zip(A2, B2)) / n
    pe2 = sum((A2.count(k) / n) * (B2.count(k) / n) for k in set(A2) | set(B2))
    k2 = (po2 - pe2) / (1 - pe2) if pe2 < 1 else 1.0
    say(f"A second blind grader re-labelled {len(ag)} cells ({n} labels): raw agreement {po:.2f}, Cohen's kappa {kappa:.2f} over the four labels; "
        f"caught against not caught: agreement {po2:.2f}, kappa {k2:.2f}. Disagreements: {n - round(po * n)} of {n}.")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
