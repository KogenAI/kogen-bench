#!/usr/bin/env python3
"""CCMAC analysis-side cost reader: requests and list-price USD per cell and per arm, the same way for both arms.

lanes' result.json/report/cost guard show the Kogen arm with 0 requests and null cost, and the bare arm with null
cost (ccmac.md, "Witness reader fix"). This reads what Claude Code itself wrote instead and prices it with
ccmac-prices-v1.json. It reads run dirs only; it changes nothing.

Per Claude Code session (bare arm: claude-code-alone/events.jsonl; Kogen: shape, build and review sessions):
- tokens split into fresh input, 5m and 1h cache writes, cache reads and output. Source, in order:
  the stream-json `result` events' `modelUsage` (bare events.jsonl, Kogen run-log/executor*/**/round-N.jsonl),
  else the session transcript `<claude projects dir>/*/<session>.jsonl` (assistant usage, last line per message id),
  else Kogen's executor usage with the uncached part taken as 1h cache writes (`split: inferred`);
- requests = distinct assistant message ids (not `<synthetic>`) in the stream or transcript (else Kogen's num_turns, `requests_source`);
- usd = tokens x list price; client_usd = Claude Code's own `costUSD` / Kogen's executor `cost_usd`.
For Kogen sessions the split must add up to Kogen's executor_round_ended totals (input incl. cache, cached = reads),
else the session is flagged `mismatch`.

Usage: ccmac-cost.py [--prices P] [--claude-projects DIR] [--json] <run dir>...
"""

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYNTHETIC = "<synthetic>"  # assistant lines Claude Code writes itself, not model requests
KEYS = ("input", "cache_write_5m", "cache_write_1h", "cache_read", "output")


def events(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if isinstance(e, dict):
                    out.append(e)
    return out


def zero():
    return {k: 0 for k in KEYS}


def add(a, b):
    for k in KEYS:
        a[k] += b[k]


def from_model_usage(mu):
    """`{model: tokens}` and Claude Code's own cost from a result event's modelUsage."""
    out, client = {}, 0.0
    for model, u in (mu or {}).items():
        w1h, w5m = u.get("cacheCreationEphemeral1hInputTokens"), u.get("cacheCreationEphemeral5mInputTokens")
        if w1h is None and w5m is None:  # no split recorded: all writes taken as 5m would undercount; refuse
            raise ValueError(f"modelUsage for {model} has no 5m/1h cache-write split")
        out[model] = {"input": u.get("inputTokens", 0), "cache_write_5m": w5m or 0, "cache_write_1h": w1h or 0,
                      "cache_read": u.get("cacheReadInputTokens", 0), "output": u.get("outputTokens", 0)}
        if (out[model]["cache_write_5m"] + out[model]["cache_write_1h"]) != u.get("cacheCreationInputTokens", 0):
            raise ValueError(f"modelUsage for {model}: 5m+1h writes != cacheCreationInputTokens")
        client += u.get("costUSD") or 0.0
    return out, client


def stream_session(evs):
    """Requests, tool calls, session id and per-model tokens of stream-json events (one or more rounds)."""
    ids, tools, sid, tokens, client, results = set(), 0, None, {}, 0.0, 0
    for e in evs:
        sid = sid or e.get("session_id")
        if e.get("type") == "assistant":
            m = e.get("message") or {}
            if m.get("model") == SYNTHETIC:
                continue
            if m.get("id"):
                ids.add(m["id"])
            tools += sum(1 for c in m.get("content") or [] if isinstance(c, dict) and c.get("type") == "tool_use")
        elif e.get("type") == "result":
            results += 1
            t, c = from_model_usage(e.get("modelUsage"))
            for model, v in t.items():
                add(tokens.setdefault(model, zero()), v)
            client += c
    return {"session_id": sid, "requests": len(ids), "tool_calls": tools, "tokens": tokens,
            "client_usd": client, "results": results}


def transcript_session(path):
    """The same from a Claude Code session transcript (usage on assistant lines; last line per message id wins)."""
    last, tools = {}, {}
    for e in events(path):
        m = e.get("message") or {}
        if e.get("type") == "assistant" and m.get("id") and m.get("model") != SYNTHETIC:
            if m.get("usage"):
                last[m["id"]] = (m.get("model"), m["usage"])
            tools[m["id"]] = tools.get(m["id"], 0) + sum(
                1 for c in m.get("content") or [] if isinstance(c, dict) and c.get("type") == "tool_use")
    tokens = {}
    for model, u in last.values():
        cc = u.get("cache_creation") or {}
        w5m, w1h = cc.get("ephemeral_5m_input_tokens"), cc.get("ephemeral_1h_input_tokens")
        if w5m is None and w1h is None and u.get("cache_creation_input_tokens"):
            raise ValueError(f"{path}: cache writes without a 5m/1h split")
        add(tokens.setdefault(model, zero()), {"input": u.get("input_tokens", 0), "cache_write_5m": w5m or 0,
                                               "cache_write_1h": w1h or 0,
                                               "cache_read": u.get("cache_read_input_tokens", 0),
                                               "output": u.get("output_tokens", 0)})
    return {"requests": len(last), "tool_calls": sum(tools.values()), "tokens": tokens}


def price(tokens, prices):
    """USD of `{model: tokens}`; None (and the unpriced model) when a model has no row."""
    usd = 0.0
    for model, t in tokens.items():
        row = prices.get(model) or prices.get(model.split("/", 1)[-1])
        if row is None:
            return None, model
        usd += sum(t[k] * row[k] for k in KEYS) / 1e6
    return usd, None


def total(tokens):
    t = zero()
    for v in tokens.values():
        add(t, v)
    return t


def bare_arm(arm_dir, prices):
    s = stream_session(events(os.path.join(arm_dir, "events.jsonl")))
    usd, unpriced = price(s["tokens"], prices)
    return {"sessions": {"agent": {**s, "usd": usd, "unpriced": unpriced, "split": "stream",
                                   "requests_source": "stream"}}}


def kogen_rounds(evs):
    """`{(role, session): {"model", "input", "cached", "output", "client_usd", "num_turns", "rounds"}}`."""
    out = {}
    for e in evs:
        if e.get("event") != "executor_round_ended":
            continue
        u = e.get("usage") or {}
        r = out.setdefault((e.get("role"), e.get("session_id")), {"model": u.get("model") or e.get("model"),
                                                                  "input": 0, "cached": 0, "output": 0,
                                                                  "client_usd": 0.0, "num_turns": 0, "rounds": 0,
                                                                  "complete": True})
        r["input"] += u.get("input") or 0
        r["cached"] += u.get("cached") or 0
        r["output"] += u.get("output") or 0
        r["client_usd"] += u.get("cost_usd") or 0.0
        r["num_turns"] += e.get("num_turns") or 0
        r["rounds"] += 1
        r["complete"] = r["complete"] and u.get("state") == "complete"
    return out


def kogen_arm(arm_dir, prices, projects):
    evs = []
    for p in (os.path.join(arm_dir, "shaping-events.ndjson"), os.path.join(arm_dir, "run-log", "log.jsonl")):
        if os.path.isfile(p):
            evs += events(p)
    streams = {}
    for p in sorted(glob.glob(os.path.join(arm_dir, "run-log", "executor*", "**", "round-*.jsonl"), recursive=True)):
        s = stream_session(events(p))
        if s["session_id"]:
            streams.setdefault(s["session_id"], []).append(s)
    sessions = {}
    for (role, sid), k in kogen_rounds(evs).items():
        rec = {"session_id": sid, "num_turns": k["num_turns"], "rounds": k["rounds"], "kogen_usage_complete": k["complete"],
               "client_usd": k["client_usd"], "kogen_tokens": {"input": k["input"], "cached": k["cached"],
                                                               "output": k["output"]}}
        tr = glob.glob(os.path.join(projects, "*", f"{sid}.jsonl")) if projects and sid else []
        if sid in streams:
            ss = streams[sid]
            tokens = {}
            for s in ss:
                for model, v in s["tokens"].items():
                    add(tokens.setdefault(model, zero()), v)
            rec.update(split="stream", requests=sum(s["requests"] for s in ss), requests_source="stream",
                       tool_calls=sum(s["tool_calls"] for s in ss), tokens=tokens,
                       stream_client_usd=sum(s["client_usd"] for s in ss))
        elif tr:
            t = transcript_session(tr[0])
            rec.update(split="transcript", requests=t["requests"], requests_source="transcript",
                       tool_calls=t["tool_calls"], tokens=t["tokens"], transcript=tr[0])
        else:
            rec.update(split="inferred", requests=k["num_turns"], requests_source="num_turns", tool_calls=None,
                       tokens={k["model"]: {"input": 0, "cache_write_5m": 0, "cache_write_1h": k["input"] - k["cached"],
                                            "cache_read": k["cached"], "output": k["output"]}})
        t = total(rec["tokens"])
        rec["mismatch"] = (sum(t[x] for x in ("input", "cache_write_5m", "cache_write_1h", "cache_read")) != k["input"]
                           or t["cache_read"] != k["cached"] or t["output"] != k["output"])
        rec["usd"], rec["unpriced"] = price(rec["tokens"], prices)
        sessions[f"{role}" if role not in sessions else f"{role}:{sid}"] = rec
    return {"sessions": sessions}


def passed(arm_dir):
    p = os.path.join(arm_dir, "evaluation.json")
    if not os.path.isfile(p):
        return None
    ev = json.load(open(p))
    if ev.get("infrastructure") not in (None, False) or not ev.get("complete", True):
        return None
    return ev.get("all_passed") is True


def run(run_dir, prices, projects):
    cells, arms = [], {}
    for arm_dir in sorted(glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*"))):
        if not os.path.isdir(arm_dir):
            continue
        arm = os.path.basename(arm_dir)
        if os.path.isfile(os.path.join(arm_dir, "events.jsonl")):
            rec = bare_arm(arm_dir, prices)
        elif os.path.isfile(os.path.join(arm_dir, "run-log", "log.jsonl")) or \
                os.path.isfile(os.path.join(arm_dir, "shaping-events.ndjson")):
            rec = kogen_arm(arm_dir, prices, projects)
        else:
            continue
        ss = rec["sessions"].values()
        usds = [s["usd"] for s in ss]
        rec.update(cell=os.path.relpath(arm_dir, os.path.join(run_dir, "cells")), arm=arm, passed=passed(arm_dir),
                   requests=sum(s["requests"] for s in ss),
                   usd=None if None in usds else round(sum(usds), 7),
                   client_usd=round(sum(s["client_usd"] for s in ss), 7),
                   flags=sorted({s["split"] for s in ss if s["split"] != "stream"}
                                | {"mismatch" for s in ss if s.get("mismatch")}
                                | {f"unpriced:{s['unpriced']}" for s in ss if s.get("unpriced")}))
        cells.append(rec)
        a = arms.setdefault(arm, {"cells": 0, "graded": 0, "passes": 0, "requests": 0, "usd": 0.0, "client_usd": 0.0,
                                  "unpriced_cells": 0})
        a["cells"] += 1
        a["graded"] += rec["passed"] is not None
        a["passes"] += rec["passed"] is True
        a["requests"] += rec["requests"]
        a["client_usd"] += rec["client_usd"]
        if rec["usd"] is None:
            a["unpriced_cells"] += 1
        else:
            a["usd"] += rec["usd"]
    for a in arms.values():
        a["usd"] = None if a["unpriced_cells"] else round(a["usd"], 6)
        a["client_usd"] = round(a["client_usd"], 6)
        a["usd_per_cell"] = None if a["usd"] is None or not a["cells"] else round(a["usd"] / a["cells"], 6)
        a["usd_per_pass"] = None if a["usd"] is None or not a["passes"] else round(a["usd"] / a["passes"], 6)
    return {"run": os.path.abspath(run_dir), "arms": arms, "cells": cells}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run_dirs", nargs="+")
    ap.add_argument("--prices", default=os.path.join(HERE, "ccmac-prices-v1.json"))
    ap.add_argument("--claude-projects", default=os.path.expanduser("~/.claude-bench/projects"),
                    help="Claude Code projects dir of the cells (CLAUDE_CD/projects); for the shape transcript")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    table = json.load(open(a.prices))
    out = [run(d, table["models"], a.claude_projects) for d in a.run_dirs]
    if a.json:
        json.dump({"prices": {k: table[k] for k in ("version", "source_url", "fetched_utc")}, "runs": out},
                  sys.stdout, indent=2)
        print()
        return
    print(f"prices {table['version']} ({table['source_url']}, fetched {table['fetched_utc']})")
    for r in out:
        print(f"\n{r['run']}")
        print("| cell | arm | session | requests | fresh in | 5m wr | 1h wr | cache rd | out | USD list | client USD | split |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for c in r["cells"]:
            for name, s in c["sessions"].items():
                t = total(s["tokens"])
                usd = "n/a" if s["usd"] is None else f"{s['usd']:.7f}"
                print(f"| {c['cell'].rsplit('/', 1)[0]} | {c['arm']} | {name} | {s['requests']} | {t['input']} | "
                      f"{t['cache_write_5m']} | {t['cache_write_1h']} | {t['cache_read']} | {t['output']} | "
                      f"{usd} | {s['client_usd']:.7f} | "
                      f"{s['split']}{' MISMATCH' if s.get('mismatch') else ''} |")
        print("\n| arm | cells | graded | passes | requests | USD list | client USD | USD/cell | USD/pass |")
        print("|---|---|---|---|---|---|---|---|---|")
        for arm, a in r["arms"].items():
            print(f"| {arm} | {a['cells']} | {a['graded']} | {a['passes']} | {a['requests']} | {a['usd']} | "
                  f"{a['client_usd']} | {a['usd_per_cell']} | {a['usd_per_pass']} |")


if __name__ == "__main__":
    main()
