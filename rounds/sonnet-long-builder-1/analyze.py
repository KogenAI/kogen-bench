#!/usr/bin/env python3
"""Recompute every number on the sonnet-long-builder-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/sonnet-long-builder-1/analyze.py [--write]

It reads only rounds/sonnet-long-builder-1/ (each bundle's attempt.json and evaluation.json), uses the Python
standard library, makes no model call and needs no private data. Without --write it prints the tables; with --write
it also writes results.txt next to itself.

Definitions. A cell "passed" when its build landed and every hidden test of its task passed. Lane names are
<review model>-review-<machine>: sonnet-review (Claude Sonnet 5.5 reviews) or opus-review (Claude Opus 5.5 reviews),
then the machine (m3 or m4, two Linux machines that each built Kogen separately). Both models build at medium
effort. The Opus lane on m4 holds repetition 1 and the Opus lane on m3 holds repetition 2 of the same three tasks.
Cost is the list price of Kogen's recorded requests (build and review together).
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def say(text=""):
    OUT.append(text)
    print(text)


def median(xs):
    xs = sorted(xs)
    m = len(xs) // 2
    return None if not xs else xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def load():
    cells = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        ids = e["ids"]
        st = {s["stage"]: s for s in a["stages"]}
        t = a["totals"]
        cells.append({"cell": a["cell"], "task": task, "lane": a["lane"], "rep": int(a["cell"].split("/")[1][1:]),
                      "reviewer": a["lane"].split("-")[0], "outcome": a["outcome"],
                      "pass": a["outcome"] == "landed" and bool(e["all_passed"]), "passed": ids["passed_count"],
                      "total": ids["passed_count"] + ids["failed_count"] + ids["other_count"], "wall": a["wall_s"],
                      "build_wall": st["build"]["wall_s"], "review_wall": st.get("review", {}).get("wall_s"),
                      "in": t["input_tokens"], "out": t["output_tokens"], "cost": t["cost_usd"],
                      "build_req": st["build"]["requests"], "review_req": st.get("review", {}).get("requests")})
    return cells


def cell_text(c):
    return f"{c['outcome']}, {c['passed']}/{c['total']}" + (" (all)" if c["pass"] else "")


def main():
    cells = load()
    tasks = sorted({c["task"] for c in cells})
    say("## Per task and cell")
    say()
    say("| Task | Hidden tests | Sonnet review, rep 1 | Opus review, rep 1 | Opus review, rep 2 |")
    say("| --- | ---: | --- | --- | --- |")
    for t in tasks:
        row = []
        for rev, rep in (("sonnet", 1), ("opus", 1), ("opus", 2)):
            c = [c for c in cells if c["task"] == t and c["reviewer"] == rev and c["rep"] == rep]
            row.append(cell_text(c[0]) if c else "not run")
        say(f"| `{t}` | {max(c['total'] for c in cells if c['task'] == t)} | " + " | ".join(row) + " |")
    say()
    say("## Wall time, tokens and list cost per cell")
    say()
    say("| Task | Cell | Wall s | Build s | Review s | Input tokens | Output tokens | List cost USD | Build / review requests |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for c in sorted(cells, key=lambda c: (c["task"], c["reviewer"] != "sonnet", c["rep"])):
        say(f"| `{c['task']}` | {c['reviewer']} review, rep {c['rep']} | {c['wall']:,.0f} | {c['build_wall']:,.0f} | "
            f"{c['review_wall'] or 0:,.0f} | {c['in']:,} | {c['out']:,} | {c['cost']:.2f} | {c['build_req']} / {c['review_req']} |")
    say()
    three = [t for t in tasks if any(c["reviewer"] == "sonnet" and c["task"] == t for c in cells)]
    say(f"## Per arm, the {len(three)} tasks that ran in every arm")
    say()
    say("| Arm | Cells | Landed | Passed every hidden test | Hidden tests passed | Median wall s | Input / output tokens (sum) | List cost USD (sum) |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |")
    for label, f in (("Sonnet review, rep 1", lambda c: c["reviewer"] == "sonnet"),
                     ("Opus review, rep 1", lambda c: c["reviewer"] == "opus" and c["rep"] == 1),
                     ("Opus review, rep 2", lambda c: c["reviewer"] == "opus" and c["rep"] == 2),
                     ("Opus review, reps 1 and 2", lambda c: c["reviewer"] == "opus")):
        v = [c for c in cells if c["task"] in three and f(c)]
        say(f"| {label} | {len(v)} | {sum(c['outcome'] == 'landed' for c in v)} | {sum(c['pass'] for c in v)} | "
            f"{sum(c['passed'] for c in v)}/{sum(c['total'] for c in v)} | {median([c['wall'] for c in v]):,.0f} | "
            f"{sum(c['in'] for c in v) / 1e6:.2f}M / {sum(c['out'] for c in v) / 1e3:.0f}k | {sum(c['cost'] for c in v):.2f} |")
    say()
    say("## The fourth task (Opus review, rep 1 only)")
    say()
    for c in cells:
        if c["task"] not in three:
            say(f"`{c['task']}`: {cell_text(c)}, {c['wall']:,.0f} s, list cost {c['cost']:.2f} USD.")
    say()
    say("## Hidden-test shortfall of the cells that did not pass every test")
    say()
    say("| Cell | Outcome | Hidden tests passed |")
    say("| --- | --- | ---: |")
    for c in cells:
        if not c["pass"]:
            say(f"| `{c['cell']}` | {c['outcome']} | {c['passed']} of {c['total']} |")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
