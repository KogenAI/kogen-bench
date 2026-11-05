#!/usr/bin/env python3
"""Stage 0 replay for lab-loops-collide-s0-20261105. Reads only data/*.json (no logs, no model). Deterministic.
Usage: python3 -I report.py [--json]"""
import json, os, sys, collections, statistics, datetime as dt
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
STATUS_ONLY = ("OVERLOAD", "EXPERIMENTS_LOW", "UNDERSPEND")      # ops-tick never relays these
def ep(t): return dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()
OWNER = {}
for k in "REPO_STALL REPO_IDLE ADOPTION_RED SCREEN_DEBT GREEN_UNLANDED BUILD_HOST_BLOCKED BUILD_STALL BUILD_FUTILE ROADMAP_DRY HOLD_UNSOURCED BLOCKED STUDIO_NEW GUARD_HOLD SWAP_HIGH".split(): OWNER[k] = "delivery"
for k in "SHELF_LOW UNDERUSED LOW_RUNNABLE EXP_NO_CELLS FINDING_UNROUTED FINDINGS_QUIET OVERPACE IDLE_WITH_BACKLOG WORKER_DEAD LANES_UNPUBLISHED".split(): OWNER[k] = "research"
def coarse(l):                      # ops-tick key(): the key arm D0 uses today
    p = l.split()
    return " ".join(p[:3] if p[:2] == ["PUBLISH_STALE", "finding"] else p[:2]) if len(p) > 1 else l.strip()
def fine(l):                        # D1 key: kind + subject
    p = l.split(); k = p[0]
    if k == "EXP_NO_CELLS" and len(p) > 2: return k + " " + p[1] + " " + p[2].rstrip(":")
    if k == "BUILD_STALL" and len(p) > 4: return k + " " + p[4]
    if k == "STUDIO_NEW" and len(p) > 4: return k + " " + p[4]
    if k == "BUILD_FUTILE" and len(p) > 2: return k + " " + p[1] + " " + p[2]
    return coarse(l)
def owner(l): return OWNER.get(l.split()[0], "main")

ticks_all = json.load(open(os.path.join(D, "ticks.json")))
T = [t for t in ticks_all if t["in_line_window"]]
for t in T:
    t["e"] = ep(t["t"]); t["L"] = [l for l in t["lines"] if l.split()[0] not in STATUS_ONLY]

def d0_replay():
    """ops-tick: relay a key when new, again when open > 20 min and last relayed > 1 h ago; a key absent for one tick is forgotten."""
    seen = {}; rel = []              # rel: (tick index, coarse key, fine key of the shown line)
    for i, t in enumerate(T):
        keys = {coarse(l): l for l in t["L"]}
        for k in keys: seen.setdefault(k, {"first": t["e"], "rel": 0})
        for k in list(seen):
            if k not in keys: del seen[k]
        due = [k for k, v in seen.items() if v["rel"] == 0 or (t["e"] - v["first"] > 1200 and t["e"] - v["rel"] > 3600)]
        if due and not t["failed"]:
            for k in due: seen[k]["rel"] = t["e"]; rel.append((i, k, fine(keys[k])))
    return rel

def events(H):
    """Events = fine key; a key absent for more than H minutes (H=0: any missed tick) and seen again opens a new event."""
    ev = []; open_ev = {}
    for i, t in enumerate(T):
        for l in t["L"]:
            k = fine(l); e = open_ev.get(k)
            if e is not None and (i == e["last"] + 1 or (H > 0 and t["e"] - T[e["last"] + 1]["e"] <= H * 60)):
                e["last"] = i; e["occ"] += 1
            else:
                e = {"key": k, "first": i, "last": i, "occ": 1, "owner": owner(l)}; open_ev[k] = e; ev.append(e)
    return ev

def analyse(H):
    rel = d0_replay(); ev = events(H); by = collections.defaultdict(list)
    for e in ev: by[e["key"]].append(e)
    seen_ev = set(); first = dup = 0
    for i, ck, fk in rel:
        c = [x for x in by.get(fk, []) if x["first"] <= i <= x["last"]]
        if not c: continue
        e = c[0]; e.setdefault("relays", []).append(i)
        if id(e) in seen_ev: dup += 1
        else: seen_ev.add(id(e)); first += 1
    never = sum(1 for e in ev if id(e) not in seen_ev)
    d0_msgs = len({i for i, _, _ in rel})
    d1_msgs = len({e["first"] for e in ev})
    res = {"H_min": H, "events": len(ev), "D0_lines": len(rel), "D0_msgs": d0_msgs, "D0_first_lines": first, "D0_duplicate_lines": dup,
           "D0_duplicate_pct": round(100 * dup / len(rel), 1), "D0_events_never_relayed": never,
           "D1_lines": len(ev), "D1_msgs": d1_msgs, "D1_duplicate_lines": 0,
           "D1_dup_removed_pct": 100.0, "D1_line_cut_pct": round(100 * (1 - len(ev) / len(rel)), 1), "D1_wake_cut_pct": round(100 * (1 - d1_msgs / d0_msgs), 1)}
    ivl = 600; sweep = {}
    for a in (0, 0.25, 0.5, 0.75, 0.9, 1.0):
        main = esc = po = role = 0.0; mt = collections.Counter()
        for e in ev:
            t0 = T[e["first"]]["e"]; tl = T[e["last"]]["e"]
            a1 = tl - t0 >= ivl * 0.8; a2 = tl - t0 >= 2 * ivl * 0.8
            if e["owner"] == "main":
                main += 1; mt[e["first"]] += 1
                p = (1 - a) if a1 else 0; po += p; esc += p
            else:
                role += 1
                p = (1 - a) if a1 else 0; main += p; esc += p
                if p:
                    j = e["first"] + 1
                    while j < len(T) - 1 and T[j]["e"] - t0 < ivl: j += 1
                    mt[j] += p
                p2 = (1 - a) ** 2 if a2 else 0; po += p2; esc += p2
        sweep[str(a)] = {"main_lines": round(main, 1), "main_msgs": round(sum(min(1.0, w) for w in mt.values()), 1), "role_lines": role,
                         "escalations_added": round(esc, 1), "owner_alerts": round(po, 1), "all_lines": round(len(ev) + esc, 1)}
    res["D2_by_ack_rate"] = sweep
    return res, ev

def hazard(ev):
    last = len(T) - 1
    def end_in(e, t0): return None if e["last"] >= last - 1 else T[e["last"]]["e"] - t0 <= 3600
    f, r, cf, cr = [], [], [], []
    for e in ev:
        for k, i in enumerate(e.get("relays", [])):
            t0 = T[i]["e"]; v = end_in(e, t0)
            if v is None: continue
            (f if k == 0 else r).append(v)
            if T[e["last"]]["e"] > t0 + 1800:
                v2 = end_in(e, t0 + 1800)
                if v2 is not None: (cr if k else cf).append(v2)
    pc = lambda x: [round(100 * sum(x) / len(x), 1), len(x)] if x else None
    dur = [(T[e["last"]]["e"] - T[e["first"]]["e"]) / 3600 for e in ev]
    rep_chronic = sum(len(e.get("relays", [])) - 1 for e, d in zip(ev, dur) if d >= 6 and e.get("relays"))
    rep_total = sum(max(0, len(e.get("relays", [])) - 1) for e in ev)
    top = collections.Counter()
    for e in ev:
        if len(e.get("relays", [])) > 1: top[e["key"]] += len(e["relays"]) - 1
    return {"end_within_60min_after_first_relay_pct_n": pc(f), "end_within_60min_after_repeat_relay_pct_n": pc(r),
            "control_window_relay_plus_30min_after_first_pct_n": pc(cf), "control_window_relay_plus_30min_after_repeat_pct_n": pc(cr),
            "events_open_over_1h": sum(1 for d in dur if d > 1), "events_open_over_6h": sum(1 for d in dur if d >= 6),
            "repeat_lines_total": rep_total, "repeat_lines_from_events_open_6h_or_more": rep_chronic, "top_repeat_keys": top.most_common(8)}

def per_day(H=60):
    rel = d0_replay(); ev = events(H); out = collections.defaultdict(lambda: collections.Counter())
    for i, t in enumerate(T): out[t["t"][:10]]["obs_lines"] += t["obs_sent"]; out[t["t"][:10]]["obs_msgs"] += 1 if t["obs_sent"] else 0
    for i, _, _ in rel: out[T[i]["t"][:10]]["D0_lines"] += 1
    for d in {T[i]["t"][:10] for i, _, _ in rel}:
        out[d]["D0_msgs"] = len({i for i, _, _ in rel if T[i]["t"][:10] == d})
    for e in ev: out[T[e["first"]]["t"][:10]]["D1_lines"] += 1
    for d in out: out[d]["D1_msgs"] = len({e["first"] for e in ev if T[e["first"]]["t"][:10] == d})
    return {d: dict(c) for d, c in sorted(out.items())}

if __name__ == "__main__":
    out = {}
    all_t = ticks_all
    out["coverage"] = {"ops_tick_ticks": len(all_t), "ops_tick_first": all_t[0]["t"], "ops_tick_last": all_t[-1]["t"],
                       "line_level_ticks": len(T), "line_level_first": T[0]["t"], "line_level_last": T[-1]["t"],
                       "line_level_days": round((T[-1]["e"] - T[0]["e"]) / 86400, 2),
                       "counts_only_ticks_before_lines": sum(1 for t in all_t if not t["in_line_window"]),
                       "observed_relay_msgs_all": sum(1 for t in all_t if t["obs_sent"]), "observed_relay_lines_all": sum(t["obs_sent"] for t in all_t)}
    out["fidelity"] = {"replay_lines": len(d0_replay()), "replay_msgs": len({i for i, _, _ in d0_replay()}),
                       "observed_lines_same_window": sum(t["obs_sent"] for t in T), "observed_msgs_same_window": sum(1 for t in T if t["obs_sent"])}
    out["sensitivity"] = {}
    for H in (0, 30, 60, 120, 360):
        r, ev = analyse(H); out["sensitivity"][str(H)] = r
        if H == 60: out["hazard_H60"] = hazard(ev)
    out["per_day_H60"] = per_day(60)
    out["main_stream_daily"] = json.load(open(os.path.join(D, "main-stream-daily.json")))
    ms = out["main_stream_daily"]; pd = out["per_day_H60"]; full = [d for d in ("2026-11-01", "2026-11-02", "2026-11-03", "2026-11-04")]
    inv = {d: sum(v for k, v in ms[d].items() if k.startswith(("in_", "out_"))) for d in ms}
    relays = sum(ms[d]["in_relay"] for d in full); involved = sum(inv[d] for d in full)
    saved = sum(pd[d]["D0_msgs"] - pd[d]["D1_msgs"] for d in full)
    out["main_wide_1_to_4_nov"] = {"main_sender_or_receiver_messages": involved, "ops_tick_relays_to_main": relays,
        "relay_share_pct": round(100 * relays / involved, 1), "steward_messages_naming_an_alarm_code": sum(ms[d].get("steward_names_alarm_code", 0) for d in full),
        "steward_messages_restating_a_code_seen_6h": sum(ms[d].get("restated_in_6h", 0) for d in full),
        "main_forwards_of_a_just_relayed_code": sum(ms[d].get("forwards_after_relay_same_code", 0) for d in full),
        "wakes_saved_by_D1": saved, "wakes_saved_pct_of_main_traffic": round(100 * saved / involved, 1),
        "ceiling_if_every_relay_removed_pct": round(100 * relays / involved, 1), "main_involved_by_day": {d: inv[d] for d in sorted(inv)}}
    out["admit"] = json.load(open(os.path.join(D, "admit-summary.json")))
    acks = json.load(open(os.path.join(D, "fleet-acks.json")))
    out["acks"] = {"rows": len(acks), "last_until": max(a["until"] for a in acks)}
    if "--json" in sys.argv: print(json.dumps(out, indent=1)); sys.exit(0)
    print(json.dumps(out, indent=1))
