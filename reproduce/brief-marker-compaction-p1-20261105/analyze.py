#!/usr/bin/env python3
"""Per-arm table from cell dirs. usage: analyze.py <cell dir>... (prints markdown + writes nothing)
Definitions:
  compaction event  one forced /compact turn. Hook detected = a SessionStart(source=compact) hook log inside that turn.
                    Marker/first-message detected = the FIRST studio_note after the compaction had a missing/stale/changed
                    signal, counted only if the last studio_note before it carried a valid signal (state intact).
  false alarm       a studio_note that is not the first after a compaction, flagged although the previous call was ok
                    and no compaction happened in between; hook: a hook log during a non-compact turn. Per 100 steady turns.
  violation         a studio_note breaking R-ticket or R-tag (stub-checked). Reported pre-compaction and post-compaction.
  tokens/turn       from the client's result JSON of each step turn (output tokens; total input incl. cache reads).
"""
import glob, json, os, sys
from collections import defaultdict


def jl(p):
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def arm_of(c):
    if c["mode"] == "none":
        return "hook" + ("+reserve" if c["hook_reserve"] else "")
    return c["mode"] + ("+reserve" if c["reserve"] else "")


A = defaultdict(lambda: defaultdict(float))
rows = []
for d in sys.argv[1:]:
    c = json.load(open(os.path.join(d, "cell.json")))
    ev, calls, hooks, summ = jl(d + "/events.jsonl"), jl(d + "/calls.jsonl"), jl(d + "/hooks.jsonl"), jl(d + "/summaries.jsonl")
    notes = [x for x in calls if x["tool"] == "studio_note"]
    comps = [e for e in ev if e["kind"] == "compact"]
    a = A[arm_of(c)]
    a["cells"] += 1
    a["turns_fail"] += sum(1 for e in ev if e["rc"] != 0)
    first_after = set()
    for e in comps:
        a["compactions"] += 1
        a["hook_det"] += any(e["t0"] <= h["t"] <= e["t1"] + 2 and h.get("source") == "compact" for h in hooks)
        before = [x for x in notes if x["t"] < e["t0"]]
        after = [x for x in notes if x["t"] > e["t1"]]
        if after:
            first_after.add(id(after[0]))
        if c["mode"] != "none" and before and after and before[-1]["signal"] in ("ok", "baseline"):
            a["sig_events"] += 1
            a["sig_det"] += bool(after[0]["detected"])
    for s in summ:
        a["summaries"] += 1
        a["sum_kept_marker"] += s["kept_marker"]
        a["sum_kept_rules"] += s["kept_ticket"] and s["kept_tag"]
    # steady calls: not first after a compaction; false alarm if flagged while previous call was ok and no compaction between
    prev = None
    for x in notes:
        if id(x) not in first_after:
            a["steady"] += 1
            between = prev is not None and any(prev["t"] < e["t0"] and e["t1"] < x["t"] for e in comps)
            if c["mode"] != "none" and prev is not None and prev["signal"] in ("ok", "baseline") and not between and x["detected"]:
                a["false_alarm"] += 1
        prev = x
    steady_turns = [e for e in ev if e["kind"] != "compact"]
    for h in hooks:
        if not any(e["t0"] <= h["t"] <= e["t1"] + 2 for e in comps):
            a["hook_false"] += 1
    a["steady_turns"] += len(steady_turns)
    t_first = comps[0]["t1"] if comps else float("inf")
    for x in notes:
        k = "post" if x["t"] > t_first else "pre"
        a[k + "_calls"] += 1
        a[k + "_viol"] += not (x["r1"] and x["r2"])
        a[k + "_reserved"] += x.get("reserved", False)
        if k == "post":
            a["post_marker_field_tok"] += (len(json.dumps({"marker": x["args"].get("marker")})) / 4.0 if "marker" in x["args"] else 0)
            a["post_first_field_tok"] += (len(json.dumps({"first": x["args"].get("first")})) / 4.0 if "first" in x["args"] else 0)
    for x in notes:
        a["sig_field_tok"] += (len(json.dumps({"marker": x["args"]["marker"]})) / 4.0 if "marker" in x["args"] else 0) + \
                              (len(json.dumps({"first": x["args"]["first"]})) / 4.0 if "first" in x["args"] else 0)
    for e in ev:
        if e["kind"] != "step":
            continue
        try:
            r = json.load(open(os.path.join(d, "turns", e["file"])))
        except (ValueError, OSError):
            continue
        u = r.get("usage", {})
        a["step_turns"] += 1
        a["out_tok"] += u.get("output_tokens", 0)
        a["in_tok"] += u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        a["cost"] += r.get("total_cost_usd", 0) or 0
    rows.append((os.path.basename(d), arm_of(c), len(comps), len(notes)))


def pct(n, d):
    return "%d/%d (%.0f%%)" % (n, d, 100.0 * n / d) if d else "n/a"


print("| arm | cells | compactions | hook detected | hook-free signal detected | summary kept marker | summary kept both rules | false alarms /100 steady turns (signal; hook) | signal field tok/call | out tok/step turn | in tok/step turn | violations pre | violations post | re-serves |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(A):
    a = A[k]
    calls = a["pre_calls"] + a["post_calls"]
    print("| %s | %d | %d | %s | %s | %s | %s | %.1f; %.1f | %.1f | %.0f | %.0f | %s | %s | %d |" % (
        k, a["cells"], a["compactions"], pct(a["hook_det"], a["compactions"]),
        pct(a["sig_det"], a["sig_events"]) if "hook" not in k else "n/a",
        pct(a["sum_kept_marker"], a["summaries"]) if k.startswith("marker") else "n/a",
        pct(a["sum_kept_rules"], a["summaries"]),
        100.0 * a["false_alarm"] / a["steady_turns"] if a["steady_turns"] else 0, 100.0 * a["hook_false"] / a["steady_turns"] if a["steady_turns"] else 0,
        a["sig_field_tok"] / calls if calls else 0,
        a["out_tok"] / a["step_turns"] if a["step_turns"] else 0, a["in_tok"] / a["step_turns"] if a["step_turns"] else 0,
        pct(a["pre_viol"], a["pre_calls"]), pct(a["post_viol"], a["post_calls"]), a["post_reserved"] + a["pre_reserved"]))
print()
print("failed turns:", {k: int(A[k]["turns_fail"]) for k in A}, " notional subscription cost USD:", {k: round(A[k]["cost"], 2) for k in A})
for r in rows:
    print("cell", *r)
