# python3 -I timeline.py <dir with cell dirs> > cells-timeline.json
# Rebuilds, per cell, the time split of a shape-only cell from its shaping-events.ndjson and result.json.
# A cell dir is any dir holding shaping-events.ndjson and result.json (searched recursively).
import json, os, sys, collections

def cell_dirs(root):
    for d, _, fs in os.walk(root):
        if "shaping-events.ndjson" in fs and "result.json" in fs:
            yield d

def analyse(d):
    ev = [json.loads(l) for l in open(os.path.join(d, "shaping-events.ndjson"))]
    res = json.load(open(os.path.join(d, "result.json")))
    deadline_ms = None
    rounds, tools, cur = [], collections.Counter(), None
    refusals, checks = [], []
    shape_time, phases = None, {}
    n_tools = 0
    started = {}          # session_id -> executor_started event
    for e in ev:
        k = e["event"]
        if k == "response_budget":
            deadline_ms = e["budget_ms"]
        elif k == "executor_started":
            started[e["session_id"]] = e
        elif k == "executor_round_started":
            cur = {"session_id": e["session_id"], "round": e["round"], "resume": e["resume"], "tools": 0,
                   "tool_names": collections.Counter(), "tool_errors": 0}
            rounds.append(cur)
        elif k == "executor_tool":
            n_tools += 1
            if cur is not None:
                cur["tools"] += 1
                cur["tool_names"][e["name"]] += 1
                cur["tool_errors"] += bool(e.get("result_error"))
        elif k == "executor_round":
            cur["session"] = e["session"]
            cur["started_s"] = round(e["started_ms"] / 1000, 1)
            cur["wall_s"] = round(e["wall_ms"] / 1000, 1)
            cur["model_s"] = round(e["model_ms"] / 1000, 1)
            cur["ending"] = e["ending"]
            cur["cost_usd"] = e["usage"]["cost_usd"]
        elif k == "executor_round_ended":
            cur["turns"] = e.get("num_turns")
            cur["max_line_gap_s"] = round(e.get("max_line_gap_ms", 0) / 1000, 1)
        elif k == "executor_round_failed":
            cur["session"] = "executor-shape (interrupted at the deadline)" if cur["tools"] or cur["round"] > 1 or cur["resume"] else "interrupted at the deadline"
            cur["wall_s"] = round(e["wall_ms"] / 1000, 1)
            cur["ending"] = "interrupted:" + e.get("interrupt_cause", "")
            cur["max_line_gap_s"] = round(e.get("max_line_gap_ms", 0) / 1000, 1)
        elif k == "submission_refused":
            refusals.append({"attempt": e["attempt"], "gate": e["gate"], "problem_lines": len(e["problems"])})
        elif k in ("decision_check", "literal_check", "step_selfcheck", "static_checks", "unpassable_check",
                   "contract_review", "property_check", "wrong_implementation_check"):
            c = {"event": k}
            if k == "decision_check":
                c.update(follows=e["follows"], contradicts=e["contradicts"],
                         unsupported=sum(i["verdict"] == "unsupported" for i in e["items"]))
            if k == "contract_review":
                c.update(findings=e.get("findings"), confirmed=e.get("confirmed"), result=e.get("result"))
            if k == "wrong_implementation_check":
                c.update(result=e["result"], problems=len(e["problems"]))
            if k == "static_checks":
                c.update(checks=[(x["name"], x["exit"]) for x in e["checks"]])
            checks.append(c)
        elif k == "phase_duration":
            phases[e["phase"]] = e["wall_ms"]
        elif k == "shape_time":
            shape_time = {x: e[x] for x in ("elapsed_ms", "checks_ms", "readiness_ms", "shaper_ms", "gap_ms")}
    for r in rounds:
        r["tool_names"] = dict(r["tool_names"])
        r.setdefault("session", "?")
    # the round that was cut off by the deadline has no start time: place it after the last recorded round end
    ends = [r["started_s"] + r["wall_s"] for r in rounds if "started_s" in r]
    for r in rounds:
        if "started_s" not in r:
            r["started_s"] = round(shape_time["elapsed_ms"] / 1000 - r["wall_s"], 1)
    st = res["stages"][0]
    shaper = [r for r in rounds if str(r["session"]).startswith("executor-shape") or r["session"] == "?"]
    checker = [r for r in rounds if r not in shaper]
    return {
        "outcome": res["outcome"], "wall_s": res["wall_s"], "started": res["started"], "ended": res["ended"],
        "cost_usd_list_equivalent": round(st["client_cost_usd"], 2) if st.get("client_cost_usd") is not None else None,
        "requests": st["requests"], "output_tokens": st["output_tokens"],
        "tool_calls": n_tools, "rounds_total": len(rounds),
        "shaper_rounds": len(shaper), "shaper_wall_s": round(sum(r["wall_s"] for r in shaper), 1),
        "first_shaper_round_wall_s": shaper[0]["wall_s"] if shaper else None,
        "checker_sessions": len(checker), "checker_wall_s": round(sum(r["wall_s"] for r in checker), 1),
        "refusals": refusals, "checks": checks, "phases_ms": phases, "shape_time": shape_time,
        "rounds": rounds,
    }

if __name__ == "__main__":
    out = {}
    for d in sorted(cell_dirs(sys.argv[1])):
        out[os.path.relpath(d, sys.argv[1])] = analyse(d)
    json.dump(out, sys.stdout, indent=1)
