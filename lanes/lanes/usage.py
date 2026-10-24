"""Per-stage cost, token and time records from a Kogen run log (`result.json` `stages`, `totals`).

Sources: the build run log (`request` events) and the shaping events
(`.kogen/local/shaping/<slug>/events.ndjson`, `provider_call` events).
Fields the logs lack are None with the field named in `missing`; nothing is invented.
"""

import importlib.util
import os

from . import common

STAGES = ("shape", "approve", "build")
INNER = ("verify", "review", "repair")  # request roles Kogen names that get their own record
TOKENS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")
RATES = ("input", "cached_input", "output")
USAGE_KEYS = dict(zip(TOKENS, ("input", "cached", "output", "reasoning")))
ZERO_USAGE = "usage all zero (b45ba32b logs unknown usage as 0)"
COST_CALC = os.path.join(os.path.dirname(__file__), "..", "..", "reproduce", "cost_calc.py")


def _cost_calc():
    spec = importlib.util.spec_from_file_location("cost_calc", COST_CALC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def model_of(event):
    """`(model, source)` of a shaping or build event: its `effective_model` (or build `model`), else its
    `configured_model` (Kogen leaves `effective_model` null for some providers); `(None, None)` when
    neither is named. A model name is never made up."""
    for key, source in (("effective_model", "effective"), ("model", "effective"), ("configured_model", "configured")):
        if event.get(key):
            return event[key], source
    return None, None


def top_rates(table):
    """The highest input, cached-input and output rate of the price table: the guard's fallback rates."""
    rows = list(table["models"].values())
    return {k: max(float(r[k]) for r in rows if r.get(k) is not None) for k in RATES}


def request_cost(model, usage, table=None, calc=None):
    """`(usd or None, reason or None)` for one request; `usage` has the TOKENS keys.

    A price that cost_calc flags as an estimate keeps its usd and returns the status as reason. A row
    whose rate for one component is null (the provider's page does not state it) prices that component at
    the table's highest rate, the reason `fallback_rate: <component>`; the other components keep their rows.
    """
    calc = calc or _cost_calc()
    if any(usage.get(k) is None for k in ("input_tokens", "cached_input_tokens", "output_tokens")):
        return None, "usage missing"
    if not model:
        return None, "model missing"
    table = table if table is not None else calc.load_table()
    for name in (model, (model or "").split("/", 1)[-1]):
        if name in table.get("models", {}):
            model = name
            break
    row = table.get("models", {}).get(model)
    gaps = sorted(k for k in RATES if isinstance(row, dict) and row.get(k) is None and k in row)
    if gaps:
        top = top_rates(table)
        table = {**table, "models": {**table["models"], model: {**row, **{k: top[k] for k in gaps}}}}
    try:
        r = calc.calculate(model, usage["input_tokens"], usage["cached_input_tokens"],
                           usage["output_tokens"], table)
    except ValueError as e:
        return None, str(e)
    if r["usd"] is None:
        return None, f"{r['status']}: {model}"
    if gaps:
        return float(r["usd"]), "fallback_rate: " + ", ".join(gaps)
    return float(r["usd"]), (r["status"] if r["status"] != "priced" else None)


def _record(stage, command, requests, table, calc):
    """One record from a command-level `command` (or None for an inner stage) and its requests."""
    missing = []
    rec = {"stage": stage, "started": None, "ended": None, "wall_s": None, "exit_code": None,
           "outcome": None, "requests": len(requests),
           "models": sorted({r["model"] for r in requests if r.get("model")}),
           "model_sources": sorted({r["model_source"] for r in requests if r.get("model_source")})}
    if command:
        for k in ("started", "ended", "wall_s", "exit_code"):
            rec[k] = command.get(k)
    else:
        rec["wall_s"] = round(sum(r.get("wall_ms") or 0 for r in requests) / 1000, 3)
        missing += ["started", "ended", "exit_code"]
    for k in TOKENS:
        vals = [r["usage"].get(k) for r in requests]
        rec[k] = None if (not requests and stage != "approve") or any(v is None for v in vals) else sum(vals)
    if stage != "approve" and not requests:
        missing += list(TOKENS)
    else:
        missing += [k for k in TOKENS if rec[k] is None]
    costs = [(None, ZERO_USAGE) if r.get("zero_is_unknown") else
             request_cost(r.get("model"), r["usage"], table, calc) for r in requests]
    if any(r.get("zero_is_unknown") for r in requests):
        missing.append("usage_zero_is_unknown")
    if stage == "approve" and not requests:
        rec["cost_usd"], rec["cost_reason"] = 0.0, None
    elif not requests:
        rec["cost_usd"], rec["cost_reason"] = None, "no request in the log"
    elif any(c[0] is None for c in costs):
        rec["cost_usd"] = None
        rec["cost_reason"] = "; ".join(sorted({c[1] for c in costs if c[0] is None}))
    else:
        rec["cost_usd"] = round(sum(c[0] for c in costs), 8)
        rec["cost_reason"] = "; ".join(sorted({c[1] for c in costs if c[1]})) or None
    rec["missing"] = sorted(set(missing))
    return rec


def shape_requests(events):
    """Requests from shaping events: each `provider_call`, nulls kept as null."""
    out = []
    for e in events or []:
        if e.get("event") == "provider_call":
            u = e.get("usage") or {}
            model, source = model_of(e)
            out.append({"role": "shape", "model": model, "model_source": source, "wall_ms": e.get("wall_ms"),
                        "usage": {k: u.get(v) for k, v in USAGE_KEYS.items()}})
    return out


def parse_run_log(events, commands, table=None, shape_events=None):
    """Stage records and totals.

    `events`: the build run log's event dicts (or None when the cell has no log).
    `shape_events`: the shaping events (`events.ndjson`), or None; the `shape` record sums
    their `provider_call`s.
    `commands`: one dict per Kogen command the cell ran, in order: `stage` (shape | approve |
    build), `started`, `ended`, `wall_s`, `exit_code`, and optionally `timed_out`.
    Requests with role verify, review or repair become an inner record after their command's;
    every other request belongs to its command's stage (a `shape` request to shape).
    Returns `{"stages": [...], "totals": {...}}`.
    """
    calc = _cost_calc()
    table = table if table is not None else calc.load_table()
    events = events or []
    reqs = []
    for e in events:
        if e.get("event") == "request":
            u = e.get("usage") or {}
            usage = {k: u.get(v) for k, v in USAGE_KEYS.items()}
            model, source = model_of(e)
            reqs.append({"role": e.get("role"), "model": model, "model_source": source, "wall_ms": e.get("wall_ms"),
                         "usage": usage, "zero_is_unknown": all(v == 0 for v in usage.values())})
    outcomes = [e.get("outcome") for e in events if e.get("event") == "outcome"]
    stages = []
    for c in commands:
        name = c["stage"]
        if name == "shape":
            own = shape_requests(shape_events)
        elif name == "build":
            own = [r for r in reqs if r["role"] not in INNER]
        else:
            own = []
        rec = _record(name, c, own, table, calc)
        if c.get("timed_out"):
            rec["outcome"] = "timeout"
        elif name == "build":
            rec["outcome"] = outcomes[-1] if outcomes else ("no_outcome" if c.get("exit_code") else "ok")
        else:
            rec["outcome"] = "ok" if c.get("exit_code") in (0, 5) else f"exit_{c.get('exit_code')}"
        stages.append(rec)
        if name == "build":
            for role in INNER:
                inner = [r for r in reqs if r["role"] == role]
                if inner:
                    irec = _record(role, None, inner, table, calc)
                    irec["outcome"] = None
                    irec["missing"] = sorted(set(irec["missing"]) | {"outcome"})
                    stages.append(irec)
    return {"stages": stages, "totals": totals(stages)}


def totals(stages):
    """Sums over all records; wall time sums only command-level stages (inner ones overlap them)."""
    t = {"requests": sum(s["requests"] for s in stages), "models": sorted({m for s in stages for m in s["models"]}),
         "model_sources": sorted({m for s in stages for m in s["model_sources"]})}
    for k in TOKENS:
        vals = [s[k] for s in stages]
        t[k] = None if any(v is None for v in vals) else sum(vals)
    walls = [s["wall_s"] for s in stages if s["stage"] in STAGES]
    t["wall_s"] = None if not walls or any(w is None for w in walls) else round(sum(walls), 3)
    costs = [s["cost_usd"] for s in stages]
    t["cost_usd"] = None if any(c is None for c in costs) else round(sum(costs), 8)
    t["cost_reason"] = "; ".join(sorted({s["cost_reason"] for s in stages if s["cost_reason"]})) or None
    t["missing"] = sorted({m for s in stages for m in s["missing"] if m in TOKENS or m == "usage_zero_is_unknown"})
    return t


def read_log(path):
    """Events of a run's `log.jsonl` or a shaping `events.ndjson`, or None when absent."""
    return common.read_jsonl(path) if os.path.isfile(path) else None
