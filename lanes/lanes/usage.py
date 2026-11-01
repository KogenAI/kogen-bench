"""Per-stage cost, token and time records from a Kogen run log (`result.json` `stages`, `totals`).

Sources: the build run log (`request` events) and the shaping events
(`.kogen/local/shaping/<slug>/events.ndjson`, `provider_call` events). When Kogen drives an executor
(claude-code) it logs neither; a stage without them takes its executor's `executor_round_ended` events.
Fields the logs lack are None with the field named in `missing`; nothing is invented.
"""

import datetime
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


def _record(stage, command, requests, table, calc, zero_ok=False):
    """One record from a command-level `command` (or None for an inner stage) and its requests."""
    missing = []
    rec = {"stage": stage, "started": None, "ended": None, "wall_s": None, "exit_code": None,
           "outcome": None, "requests": sum(r.get("count", 1) for r in requests),
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
        rec[k] = None if (not requests and stage != "approve" and not zero_ok) or any(v is None for v in vals) else sum(vals)
    if stage != "approve" and not requests and not zero_ok:
        missing += list(TOKENS)
    else:
        missing += [k for k in TOKENS if rec[k] is None]
    costs = [(None, ZERO_USAGE) if r.get("zero_is_unknown") else
             request_cost(r.get("model"), r["usage"], table, calc) for r in requests]
    if any(r.get("zero_is_unknown") for r in requests):
        missing.append("usage_zero_is_unknown")
    if stage == "approve" and not requests:
        rec["cost_usd"], rec["cost_reason"] = 0.0, None
    elif zero_ok and not requests:  # a declared seed replaced the builder, or Kogen stopped before its executor
        rec["cost_usd"], rec["cost_reason"] = 0.0, (zero_ok if isinstance(zero_ok, str) else
                                                     "seeded: no builder request by design")
    elif not requests:
        rec["cost_usd"], rec["cost_reason"] = None, "no request in the log"
    elif any(c[0] is None for c in costs):
        rec["cost_usd"] = None
        rec["cost_reason"] = "; ".join(sorted({c[1] for c in costs if c[0] is None}))
    else:
        rec["cost_usd"] = round(sum(c[0] for c in costs), 8)
        rec["cost_reason"] = "; ".join(sorted({c[1] for c in costs if c[1]})) or None
    if requests and all(r.get("client_cost_usd") is not None for r in requests):  # the executor's own figure
        rec["client_cost_usd"] = round(sum(r["client_cost_usd"] for r in requests), 8)
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


def _ms(start, end):
    try:
        t0, t1 = (datetime.datetime.fromisoformat(t.replace("Z", "+00:00")) for t in (start, end))
    except (AttributeError, TypeError, ValueError):
        return None
    return round((t1 - t0).total_seconds() * 1000)


def executor_requests(events):
    """Requests of an executor Kogen drives (claude-code), counted the way the agent-alone lane counts Claude
    Code's: one record per `executor_round_ended`, worth its `num_turns` requests, its usage as Kogen logs it
    (input with cache reads and writes, cached = cache reads), the executor's `cost_usd` as `client_cost_usd`.
    Kogen logs no `request` or `provider_call` events for these executors (ccs3-lm, rpfix 31 Oct)."""
    out, started = [], {}
    for e in events or []:
        key = (e.get("role"), e.get("session_id"), e.get("round"))
        if e.get("event") == "executor_round_started":
            started[key] = e.get("at")
        if e.get("event") != "executor_round_ended":
            continue
        u = e.get("usage") or {}
        usage = {k: u.get(v) for k, v in USAGE_KEYS.items()}
        model, source = model_of({"model": u.get("model") or e.get("model")})
        turns = e.get("num_turns")
        out.append({"role": e.get("role"), "model": model, "model_source": source,
                    "wall_ms": _ms(started.get(key), e.get("at")), "usage": usage,
                    "count": turns if isinstance(turns, int) and not isinstance(turns, bool) else 1,
                    "client_cost_usd": u.get("cost_usd"),
                    "zero_is_unknown": all(v == 0 for v in usage.values())})
    return out


def parse_run_log(events, commands, table=None, shape_events=None):
    """Stage records and totals.

    `events`: the build run log's event dicts (or None when the cell has no log).
    `shape_events`: the shaping events (`events.ndjson`), or None; the `shape` record sums
    their `provider_call`s.
    `commands`: one dict per Kogen command the cell ran, in order: `stage` (shape | approve |
    build), `started`, `ended`, `wall_s`, `exit_code`, and optionally `timed_out`.
    A build stage with no request counts as zero, not as missing, when the log has a `seeded` event: a
    declared seed replaced the builder, so it has no builder request by design. It also counts as zero when Kogen
    drives an executor (its shaping or build events show one) and the build log ended with an `outcome` before
    any executor round started: Kogen stopped before building (ccs3-lm revive-baseline-go, check_failing).
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
    if not reqs:  # Kogen driving an executor: its rounds are the requests
        reqs = executor_requests(events)
    outcomes = [e.get("outcome") for e in events if e.get("event") == "outcome"]
    seeded = any(e.get("event") == "seeded" for e in events)
    executor = any(str(e.get("event", "")).startswith("executor_") for e in events + (shape_events or []))
    unstarted = bool(executor and not reqs and outcomes
                     and not any(e.get("event") == "executor_round_started" for e in events))
    stages = []
    for c in commands:
        name = c["stage"]
        if name == "shape":
            own = shape_requests(shape_events) or executor_requests(shape_events)
        elif name == "build":
            own = [r for r in reqs if r["role"] not in INNER]
        else:
            own = []
        zero = (name == "build" and seeded) or (
            name == "build" and unstarted and "no executor round: Kogen stopped before building")
        rec = _record(name, c, own, table, calc, zero_ok=zero)
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
    # Never zero a total because one stage is unpriced: sum the priced stages, list the unpriced ones (cap7, 30 Oct).
    priced = [s["cost_usd"] for s in stages if s["cost_usd"] is not None]
    unpriced = [{"stage": s["stage"], "reason": s["cost_reason"]} for s in stages if s["cost_usd"] is None]
    t["priced_usd"] = round(sum(priced), 8) if priced else None
    t["unpriced_stages"] = unpriced
    t["cost_complete"] = not unpriced
    t["cost_usd"] = t["priced_usd"]  # a lower bound whenever unpriced_stages is not empty
    t["cost_reason"] = "; ".join(sorted({s["cost_reason"] for s in stages if s["cost_reason"]})) or None
    t["missing"] = sorted({m for s in stages for m in s["missing"] if m in TOKENS or m == "usage_zero_is_unknown"})
    return t


def read_log(path):
    """Events of a run's `log.jsonl` or a shaping `events.ndjson`, or None when absent."""
    return common.read_jsonl(path) if os.path.isfile(path) else None
