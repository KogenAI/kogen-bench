#!/usr/bin/env python3
"""Phase 2 per-arm table. usage: analyze2.py <cell dir>...
Definitions (phase 1's, plus):
  ref hook          the reference SessionStart(compact) hook from --settings (paired on every compaction)
  signal detected   the FIRST studio_note after a compaction had a missing/stale/flagged signal, counted only if the
                    last studio_note before it carried a valid signal (phase 1 definition). Guide arms: the receipt
                    fallback, counted only where the agent used it.
  hook installed    a settings file in the cell (project .claude/settings*.json or the cell home's user settings)
                    that holds a SessionStart hook running "brief --loop"
  agent hook fired  a cli_brief call with source=compact inside a compaction turn (the agent's own hook)
  agent hook other  cli_brief calls outside compactions: source startup/resume (session start), or no hook event
                    (the agent ran the command by hand, e.g. to test it)
  false alarm       phase 1 definition, per 100 steady turns
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stub2  # noqa: E402  (brief text per cell, for the "brief intact in the summary" check)
from collections import defaultdict


def jl(p):
    out = []
    if os.path.exists(p):
        for l in open(p):
            try:
                out.append(json.loads(l))
            except ValueError:
                pass
    return out


def arm_of(c):
    return c["mode"] + ("+rs" if c.get("reserve") else "") + ("/live" if c.get("drive") == "live" else "") + \
        ("/" + c["perm"] if c.get("perm", "default") != "default" else "")


def installed(d):
    hits = []
    for f in [os.path.join(d, "installed", x) for x in (os.listdir(d + "/installed") if os.path.isdir(d + "/installed") else [])]:
        try:
            j = json.load(open(f))
        except ValueError:
            continue
        for g in (j.get("hooks", {}) or {}).get("SessionStart", []) or []:
            for h in g.get("hooks", []):
                if "brief --loop" in h.get("command", ""):
                    hits.append((os.path.basename(f), g.get("matcher")))
    return hits


A = defaultdict(lambda: defaultdict(float))
rows = []
for d in sys.argv[1:]:
    c = json.load(open(os.path.join(d, "cell.json")))
    ev, calls, hooks, summ = jl(d + "/events.jsonl"), jl(d + "/calls.jsonl"), jl(d + "/hooks.jsonl"), jl(d + "/summaries.jsonl")
    notes = [x for x in calls if x["tool"] == "studio_note"]
    clis = [x for x in calls if x["tool"] == "cli_brief"]
    comps = [e for e in ev if e["kind"] == "compact"]
    k = arm_of(c)
    a = A[k]
    a["cells"] += 1
    a["turns_fail"] += sum(1 for e in ev if e["rc"] != 0)
    stub2.setup(d)
    brief_lines = stub2.brief().split("\n")
    inst = installed(d)
    a["installed"] += bool(inst)
    first_after = set()
    for e in comps:
        a["compactions"] += 1
        inwin = lambda t: e["t0"] <= t <= e["t1"] + 2
        a["hook_det"] += any(inwin(h["t"]) and h.get("source") == "compact" for h in hooks)
        a["agent_hook_det"] += any(inwin(x["t"]) and x.get("source") == "compact" for x in clis)
        before = [x for x in notes if x["t"] < e["t0"]]
        after = [x for x in notes if x["t"] > e["t1"]]
        if after:
            first_after.add(id(after[0]))
        if c["mode"] != "none" and before and after and before[-1]["signal"] in ("ok", "baseline"):
            a["sig_events"] += 1
            a["sig_det"] += bool(after[0]["detected"])
            ci = comps.index(e)
            if ci < len(summ):  # brief intact = every brief line verbatim in this compaction's summary
                intact = all(l in summ[ci]["summary"] for l in brief_lines)
                a["x_%s_%s" % ("intact" if intact else "lost", "flag" if after[0]["detected"] else "quiet")] += 1
    for x in clis:
        if any(e["t0"] <= x["t"] <= e["t1"] + 2 for e in comps) and x.get("source") == "compact":
            continue
        a["cli_other_" + str(x.get("source") or "manual")] += 1
    for s in summ:
        a["summaries"] += 1
        a["sum_kept_marker"] += s["kept_marker"]
        a["sum_kept_rules"] += s["kept_ticket"] and s["kept_tag"]
        a["sum_kept_last_receipt"] += bool(s.get("receipts_kept"))
    prev = None
    for x in notes:
        if id(x) not in first_after:
            a["steady"] += 1
            between = prev is not None and any(prev["t"] < e["t0"] and e["t1"] < x["t"] for e in comps)
            if prev is not None and prev["signal"] in ("ok", "baseline") and not between and x["detected"]:
                a["false_alarm"] += 1
        prev = x
    for h in hooks:
        if not any(e["t0"] <= h["t"] <= e["t1"] + 2 for e in comps):
            a["hook_false"] += 1
    a["steady_turns"] += len([e for e in ev if e["kind"] != "compact"])
    t_first = comps[0]["t1"] if comps else float("inf")
    for x in notes:
        p = "post" if x["t"] > t_first else "pre"
        a[p + "_calls"] += 1
        a[p + "_viol"] += not (x["r1"] and x["r2"])
        a[p + "_reserved"] += x.get("reserved", False)
        a["fallback_used"] += bool(x["args"].get("receipt"))
        for f in ("marker", "receipt", "brief_seen", "first"):
            if f in x["args"]:
                a["sig_field_tok"] += len(json.dumps({f: x["args"][f]})) / 4.0
    for e in ev:
        if e["kind"] != "step":
            continue
        try:
            r = json.load(open(os.path.join(d, "turns", e["file"])))
        except (ValueError, OSError):
            continue
        u = r.get("usage", {}) or {}
        a["step_turns"] += 1
        a["out_tok"] += u.get("output_tokens", 0)
        a["in_tok"] += u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        a["cost"] += r.get("total_cost_usd", 0) or 0
    seat_ok = open(d + "/seat-settings.before").read() == open(d + "/seat-settings.after").read() \
        if os.path.exists(d + "/seat-settings.after") else None
    rows.append((os.path.basename(d), k, "compactions=%d" % len(comps), "notes=%d" % len(notes), "cli=%d" % len(clis),
                 "installed=%s" % (inst or "no"), "seat_settings_untouched=%s" % seat_ok,
                 "signals=" + ",".join(x["signal"] for x in notes)))


def pct(n, d):
    return "%d/%d" % (n, d) if d else "n/a"


print("| arm | cells | compactions | ref hook | hook-free signal detected | agent hook installed (cells) | agent hook fired on compaction | agent CLI runs outside compaction | summary kept marker / a receipt | summary kept both rules | false alarms / steady calls | signal tok/call | fallback field used (calls) | out tok/step | in tok/step | violations pre | violations post |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(A):
    a = A[k]
    calls = a["pre_calls"] + a["post_calls"]
    other = ", ".join("%s %d" % (x[10:], a[x]) for x in sorted(a) if x.startswith("cli_other_")) or "0"
    guide = k.startswith("guide")
    print("| %s | %d | %d | %s | %s | %s | %s | %s | %s / %s | %s | %s | %.1f | %s | %.0f | %.0f | %s | %s |" % (
        k, a["cells"], a["compactions"], pct(a["hook_det"], a["compactions"]),
        pct(a["sig_det"], a["sig_events"]) if a["sig_events"] or not guide else "n/a (fallback unused)",
        pct(a["installed"], a["cells"]) if guide else "n/a", pct(a["agent_hook_det"], a["compactions"]) if guide else "n/a",
        other if guide else "n/a",
        pct(a["sum_kept_marker"], a["summaries"]) if k.split("+")[0].split("/")[0] in ("marker", "hash", "nonce") else "n/a",
        pct(a["sum_kept_last_receipt"], a["summaries"]) if k.startswith(("rolling", "guide")) else "n/a",
        pct(a["sum_kept_rules"], a["summaries"]),
        "%d/%d" % (a["false_alarm"], a["steady"]),
        a["sig_field_tok"] / calls if calls else 0, pct(a["fallback_used"], calls) if guide else "n/a",
        a["out_tok"] / a["step_turns"] if a["step_turns"] else 0, a["in_tok"] / a["step_turns"] if a["step_turns"] else 0,
        pct(a["pre_viol"], a["pre_calls"]), pct(a["post_viol"], a["post_calls"])))
print()
print("Brief intact in the summary (all brief lines verbatim) x hook-free signal on the first call after it (counted events):")
for k in sorted(A):
    a = A[k]
    if a["sig_events"]:
        print("  %s: brief NOT verbatim -> flagged %d, missed %d; brief verbatim -> flagged %d, quiet %d" % (
            k, a["x_lost_flag"], a["x_lost_quiet"], a["x_intact_flag"], a["x_intact_quiet"]))
print()
print("failed turns:", {k: int(A[k]["turns_fail"]) for k in A}, " notional seat cost USD:", {k: round(A[k]["cost"], 2) for k in A})
for r in rows:
    print("cell", *r)
