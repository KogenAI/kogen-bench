#!/usr/bin/env python3
"""Recompute every number on the claude-code-fix-rechecks-1 page from its published files.

Usage, from the repository root:  python3 -I rounds/claude-code-fix-rechecks-1/analyze.py [--write]

It reads only rounds/claude-code-fix-rechecks-1/ (each bundle's attempt.json and evaluation.json, and cell-facts.json),
uses the Python standard library, makes no model call and needs no private data. Without --write it prints the
tables; with --write it also writes results.txt next to itself.
"""
import glob
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def say(text=""):
    OUT.append(text)
    print(text)


def main():
    facts = json.load(open(os.path.join(HERE, "cell-facts.json")))["cells"]
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        rows.append((a, e, facts[a["cell"]]))
    builds = [r for r in rows if r[0]["phase"] == "build"]
    shapes = [r for r in rows if r[0]["phase"] == "shape"]

    say("## Build cells (the two stop rules)")
    say()
    say("| Lane | Task id | Outcome | Executor rounds | Blocker reports | Repeated-failure stops | Verification runs | Cell wall time, s | Hidden tests passed | failed | not reported |")
    say("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for a, e, x in builds:
        b, ids = x["build"], e["ids"]
        say(f"| {a['lane']} | `{a['cell'].split('/')[0]}` | {a['outcome']} | {b['executor_rounds']} | {b['builder_blocker_events']} | {b['no_progress_events']} | "
            f"{b['verification_passes']} | {a['wall_s']:.0f} | {ids['passed_count']} of {e['expected']['requested_count']} | {ids['failed_count']} | {ids['other_count']} |")
    say()
    say("## Shape cells (the step-file self-check)")
    say()
    say("| Rep | Outcome | Cell wall time, s | Self-check runs | Checks run | Checks failed | Step files | go run, npm run or npx in step files | Scenarios | Passing on the reference | Failing on the start | Wrong variants caught |")
    say("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for a, e, x in shapes:
        s = x["shape"]
        say(f"| {a['cell'].split('/')[1]} | {a['outcome']} | {a['wall_s']:.0f} | {s['selfcheck_events']} | {s['selfcheck_items']} | {s['selfcheck_items_failed']} | "
            f"{s['step_files']} | {s['go_run_npm_run_npx_matches']} | {e['scenarios']} | {e['pass_on_reference']} | {e['fail_on_start']} | {e['wrong_caught']} of {e['wrong_total']} |")
    tot = lambda k: sum(e[k] for _, e, _ in shapes)
    say()
    say(f"Shape cells: {len(shapes)}; ended ok: {sum(a['outcome'] == 'ok' for a, _, _ in shapes)}; "
        f"self-check runs: {sum(x['shape']['selfcheck_events'] for _, _, x in shapes)} ({min(x['shape']['selfcheck_events'] for _, _, x in shapes)} to {max(x['shape']['selfcheck_events'] for _, _, x in shapes)} per cell); "
        f"checks run: {sum(x['shape']['selfcheck_items'] for _, _, x in shapes)}, failed: {sum(x['shape']['selfcheck_items_failed'] for _, _, x in shapes)}; "
        f"step-file matches for go run, npm run or npx: {sum(x['shape']['go_run_npm_run_npx_matches'] for _, _, x in shapes)}.")
    kinds = {}
    for _, _, x in shapes:
        for k, v in x["shape"]["selfcheck_kinds"].items():
            kinds[k] = kinds.get(k, 0) + v
    say(f"Checks run by kind: {', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))}.")
    say(f"Scenarios {tot('scenarios')}; passing on the reference {tot('pass_on_reference')}; failing on the starting code {tot('fail_on_start')}; "
        f"wrong variants caught {tot('wrong_caught')} of {tot('wrong_total')}.")
    full = [a["cell"].split("/")[1] for a, e, _ in shapes if e["pass_on_reference"] == e["scenarios"]]
    say(f"Cells where every scenario passes on the reference: {len(full)} ({', '.join(full)}). Cells where every scenario fails on the start: "
        f"{sum(e['fail_on_start'] == e['scenarios'] for _, e, _ in shapes)}. Cells that catch every wrong variant: {sum(e['wrong_caught'] == e['wrong_total'] for _, e, _ in shapes)}.")
    walls = sorted(a["wall_s"] for a, _, _ in shapes)
    say(f"Shape wall time, s: min {walls[0]:.0f}, median {statistics.median(walls):.1f}, max {walls[-1]:.0f}.")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
