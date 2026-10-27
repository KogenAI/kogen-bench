#!/usr/bin/env python3
"""Recompute every number on the executor-lineup-dry-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/executor-lineup-dry-1/analyze.py [--write]

It reads only rounds/executor-lineup-dry-1/ (each bundle's attempt.json and evaluation.json, plumbing.json and
executor-usage.json), uses the Python standard library, makes no model call and needs no private data. Without
--write it prints the tables; with --write it also writes results.txt next to itself.
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


def main():
    plumb = json.load(open(os.path.join(HERE, "plumbing.json")))["cells"]
    usage = json.load(open(os.path.join(HERE, "executor-usage.json")))["cells"]
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        rows.append((a, e, plumb[a["cell"]], usage[a["cell"]]))
    say("## Per cell")
    say()
    say("| Machine | Task | Outcome | Hidden tests passed | Cell wall, s | Shape, s | Build, s | Executor started in shape, build, review | Native calls in shape, in build and review |")
    say("| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |")
    for a, e, p, u in rows:
        st = {s["stage"]: s for s in a["stages"]}
        ids = e["ids"]
        say(f"| {a['lane'].replace('cc-lineup-', '')} | `{a['cell'].split('/')[0]}` | {a['outcome']} | {ids['passed_count']} of {ids['passed_count'] + ids['failed_count'] + ids['other_count']} | "
            f"{a['wall_s']:.0f} | {st['shape']['wall_s']:.0f} | {st['build']['wall_s']:.0f} | {p['shape_executor_started']}, {p['build_executor_started']}, {p['review_executor_started']} | "
            f"{p['shape_native_provider_calls']}, {p['build_review_native_requests']} |")
    say()
    say("## Grade of the shaped Intent")
    say()
    say("| Machine | Scenarios | Holding on the reference solution | Failing on the starting code | Known-wrong solutions caught |")
    say("| --- | ---: | ---: | ---: | ---: |")
    for a, e, p, u in rows:
        i = p["intent"]
        say(f"| {a['lane'].replace('cc-lineup-', '')} | {i['scenarios']} | {i['pass_on_reference']} | {i['fail_on_start']} | {i['wrong_caught']} of {i['wrong_total']} |")
    say()
    say("## Claude Code usage as reported by Kogen (not a bill)")
    say()
    say("| Machine | Role | Input tokens | of which cached | Output tokens | Claude Code's own cost estimate, USD |")
    say("| --- | --- | ---: | ---: | ---: | ---: |")
    for a, e, p, u in rows:
        for role in ("build", "review"):
            x = u[role]
            say(f"| {a['lane'].replace('cc-lineup-', '')} | {role} | {x['input_tokens']:,} | {x['cached_input_tokens']:,} | {x['output_tokens']:,} | {x['estimate_usd']:.4f} |")
    say()
    say(f"Cells: {len(rows)}; landed: {sum(a['outcome'] == 'landed' for a, *_ in rows)}; every hidden test passed: {sum(bool(e['all_passed']) for _, e, *_ in rows)}; "
        f"native model calls in any role: {sum(p['shape_native_provider_calls'] + p['build_review_native_requests'] for _, _, p, _ in rows)}.")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
