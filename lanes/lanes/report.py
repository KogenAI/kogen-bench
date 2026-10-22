"""Lane report: per-lane quality, cost and time, witness checks and the fixed decision rule.

`report(run_dir)` reads `experiment.json`, `plan.jsonl` and each cell's `result.json`,
`evaluation.json` and run log; `write(run_dir)` writes `report.json` and `report.md`.
Outcome classes and rule arithmetic follow the Lab's scoring exactly (`DECISION-RULES.md`).
"""

import collections
import os
import re
import sys
from fractions import Fraction
from math import comb

from . import common, experiment, usage

RULE_KINDS = ("paired_sign", "task_sign", "cost_at_quality", "descriptive")
SHAPE_KEYS = ("scenarios", "pass_on_reference", "fail_on_start", "wrong_caught", "wrong_total")
COUNTED = ("correct", "incorrect", "workflow_failure")  # the Lab's Outcome.counted?
THRESHOLDS = ("min_gain_points", "max_p", "max_loss_points", "min_saving_pct")
STAGE_ORDER = ("shape", "approve", "build") + usage.INNER  # other stages follow in first-seen order
SUMS = ("requests",) + usage.TOKENS + ("cost_usd", "wall_s")
DECIMAL = re.compile(r"[+-]?\d+(\.\d+)?([eE][+-]?\d+)?")

# Differences from the Lab's scoring (internal/scoring, lab-go-final-20261022), all deliberate:
# - the default `cost_at_quality` metric is `wall_s` (the Lab: `wall_seconds`);
# - `ratio` accepts "n/d" strings and reads inf/nan as 0, where the Lab's decimal pattern rejects
#   "n/d" and `decimalBound` treats inf as beyond every ratio and nan as always false; `check_rule`
#   admits only numbers and decimal strings, so neither case reaches a rule;
# - Kogen's endings are not the Lab's workflow-end strings: `classify` maps them.


class ReportError(Exception):
    pass


# ---- exact arithmetic (the Lab's Decision helpers) ---------------------------------------

def ratio(value):
    """A number or decimal string as a Fraction (floats by shortest repr); anything else 0."""
    try:
        return Fraction(0) if isinstance(value, bool) else Fraction(str(value).strip())
    except (ValueError, ZeroDivisionError):
        return Fraction(0)


def format_points(r):
    """Two places, half away from zero."""
    n = int((abs(r) * 200 + 1) // 2)
    return f"{'-' if r < 0 and n else ''}{n // 100}.{n % 100:02d}"


def ratio_decimal(r):
    """An integer, a finite decimal, or `n/d`."""
    n, d = r.numerator, r.denominator
    places = next((k for k in range(d.bit_length() + 1) if 10 ** k % d == 0), None)
    if places is None:
        return f"{n}/{d}"
    if places == 0:
        return str(n)
    digits = str(abs(n) * 10 ** places // d).rjust(places + 1, "0")
    return ("-" if n < 0 else "") + digits[:-places] + "." + digits[-places:].rstrip("0")


def binomial_tail(successes, trials):
    """P(X >= successes) for X ~ Binomial(trials, 1/2); 1 without trials."""
    if trials <= 0:
        return Fraction(1)
    return Fraction(sum(comb(trials, k) for k in range(successes, trials + 1)), 2 ** trials)


def rate_difference(a, a_total, b, b_total):
    return (Fraction(a, max(a_total, 1)) - Fraction(b, max(b_total, 1))) * 100


def median(values):
    s = sorted(ratio(v) for v in values)
    if not s:
        return Fraction(0)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


# ---- rule kinds (the Lab's Decision.decide) ---------------------------------------------

def _sign(wins, losses, gain, min_gain_points, max_p):
    """keep / reject / unresolved and both tails, shared by paired_sign and task_sign."""
    p_c, p_b = binomial_tail(wins, wins + losses), binomial_tail(losses, wins + losses)
    gmin, pmax = ratio(min_gain_points), ratio(max_p)
    decision = ("keep" if gain >= gmin and p_c <= pmax else
                "reject" if -gain >= gmin and p_b <= pmax else "unresolved")
    return {"decision": decision, "gain_points": format_points(gain),
            "p": ratio_decimal(p_c), "p_reverse": ratio_decimal(p_b)}


def paired_sign(blocks, min_gain_points=0, max_p=1):
    """`blocks`: [{candidate: bool, baseline: bool}]."""
    c_only = sum(1 for b in blocks if b["candidate"] and not b["baseline"])
    b_only = sum(1 for b in blocks if b["baseline"] and not b["candidate"])
    both = sum(1 for b in blocks if b["candidate"] and b["baseline"])
    total = len(blocks)
    res = _sign(c_only, b_only, Fraction(c_only - b_only, max(total, 1)) * 100, min_gain_points, max_p)
    if total == 0:
        res["decision"] = "unresolved"
    return {**res, "candidate_only": c_only, "baseline_only": b_only, "both": both,
            "neither": total - c_only - b_only - both, "blocks": total}


def task_sign(tasks, min_gain_points=0, max_p=1):
    """`tasks`: [{candidate_correct, baseline_correct, candidate_total, baseline_total}]."""
    cw = sum(1 for t in tasks if t["candidate_correct"] > t["baseline_correct"])
    bw = sum(1 for t in tasks if t["baseline_correct"] > t["candidate_correct"])
    gain = rate_difference(*(sum(t[k] for t in tasks) for k in (
        "candidate_correct", "candidate_total", "baseline_correct", "baseline_total")))
    res = _sign(cw, bw, gain, min_gain_points, max_p)
    if cw + bw == 0:
        res["decision"] = "unresolved"
    return {**res, "candidate_favored": cw, "baseline_favored": bw, "ties": len(tasks) - cw - bw,
            "tasks": len(tasks)}


def cost_at_quality(baseline, candidate, max_loss_points=0, min_saving_pct=0, metric="wall_s"):
    """`baseline`/`candidate`: {correct, total, metrics: [numbers]}."""
    loss = rate_difference(baseline["correct"], baseline["total"], candidate["correct"], candidate["total"])
    holds = loss <= ratio(max_loss_points)
    bm, cm = median(baseline["metrics"]), median(candidate["metrics"])
    saving = (bm - cm) * 100 / bm if bm != 0 else Fraction(0)
    decision = "unresolved"
    if not holds:
        decision = "reject"
    elif saving >= ratio(min_saving_pct) and baseline["metrics"] and candidate["metrics"]:
        decision = "keep"
    return {"decision": decision, "quality_holds": holds, "loss_points": format_points(loss),
            "saving_pct": format_points(saving), "metric": metric, "baseline_median": ratio_decimal(bm),
            "candidate_median": ratio_decimal(cm)}


# ---- cells ------------------------------------------------------------------------------

def _eval_state(evaluation, phase):
    """The Lab's evaluation state: all_passed, failed, infrastructure or incomplete (no grade)."""
    if not isinstance(evaluation, dict):
        return "incomplete"
    if evaluation.get("infrastructure") not in (None, False):  # the Lab's evaluationState, before all_passed
        return "infrastructure"
    if evaluation.get("state") in ("infrastructure", "incomplete"):
        return evaluation["state"]
    if isinstance(evaluation.get("all_passed"), bool):
        return "all_passed" if evaluation["all_passed"] else "failed"
    if phase == "shape" and all(isinstance(evaluation.get(k), int) for k in SHAPE_KEYS):
        e = evaluation  # scenarios hold on the reference, fail on the start, catch every wrong tree
        good = (e["scenarios"] > 0 and e["pass_on_reference"] == e["scenarios"] == e["fail_on_start"]
                and e["wrong_caught"] == e["wrong_total"])
        return "all_passed" if good else "failed"
    return "incomplete"


def classify(result, log, evaluation, phase):
    """The Lab's outcome class (Outcome.classify) for a Kogen cell; the table is in DECISION-RULES.md."""
    ending = (result or {}).get("outcome")
    if not isinstance(ending, str):  # never ran, or a result without an ending: a harness fault
        return "incomplete"
    if ending in ("landed", "ok"):  # submitted
        state = _eval_state(evaluation, phase)
        if state in ("infrastructure", "incomplete"):
            return "infrastructure"
        return "correct" if state == "all_passed" else "incorrect"
    if (any(e.get("provider_failure") for e in log if e.get("event") == "outcome")
            or ending.startswith("provider_failure") or ending in ("host_lost", "environment", "usage")):
        return "infrastructure"
    if ending.startswith("interrupted") or ending in ("controller_lost", "signal"):
        return "incomplete"
    return "workflow_failure"  # build_blocked, no_outcome, refused, internal, timeout, questions_pending, ...


def _load_cells(run_dir, phase):
    path = os.path.join(run_dir, "plan.jsonl")
    if not os.path.isfile(path):
        raise ReportError(f"{path}: not found (the plan is part of the run directory)")
    cells = []
    for p in common.read_jsonl(path):
        d = common.cell_dir(run_dir, p["cell"])
        read = lambda name: common.read_json(os.path.join(d, name)) if os.path.isfile(os.path.join(d, name)) else None
        c = {"plan": p, "result": read("result.json"), "evaluation": read("evaluation.json"),
             "log": usage.read_log(os.path.join(d, "run-log", "log.jsonl")) or []}
        c["class"] = classify(c["result"], c["log"], c["evaluation"], phase)
        cells.append(c)
    return cells


def check_witnesses(expect, log):
    """Failures of `expect` assertions on one cell's events: `{"event", "count" | "min" | "max",
    "where"?: {field: value}}`."""
    failures = []
    for w in expect or []:
        n = sum(1 for e in log if e.get("event") == w.get("event")
                and all(e.get(k) == v for k, v in (w.get("where") or {}).items()))
        if ("count" in w and n != w["count"]) or ("min" in w and n < w["min"]) or ("max" in w and n > w["max"]):
            want = {k: w[k] for k in ("count", "min", "max") if k in w}
            failures.append(f"event {w.get('event')!r} seen {n} times, expected {want}")
    return failures


# ---- lanes ------------------------------------------------------------------------------

def _sum(values):
    return None if not values or any(v is None for v in values) else sum(values)


def _sums(records):
    t = {k: _sum([r.get(k) for r in records]) for k in SUMS}
    t["cache_hit_share"] = (None if t["cached_input_tokens"] is None or not t["input_tokens"]
                            else round(t["cached_input_tokens"] / t["input_tokens"], 4))
    return t


def _green_pass(evaluation):
    return any(isinstance(t, dict) and t.get("all_passed") is True for t in (evaluation or {}).get("pass_trees") or [])


def _lane(lane, cells, phase):
    own = [c for c in cells if c["plan"]["lane"] == lane["name"]]
    finished = [c for c in own if c["result"]]
    counted = [c for c in own if c["class"] in COUNTED]  # the Lab's denominator
    graded = [c["evaluation"] for c in own if c["evaluation"] is not None]
    totals = [c["result"].get("totals") or {} for c in finished]
    stages = collections.defaultdict(list)
    for c in finished:
        for s in c["result"].get("stages") or []:
            stages[s["stage"]].append(s)
    witness = [f"{c['plan']['cell']}: {f}" for c in finished  # a cell that never ran has no log
               for f in check_witnesses(lane.get("expect"), c["log"])]
    shaped = [e for e in graded if all(isinstance(e.get(k), int) for k in SHAPE_KEYS)]
    rate = lambda n: round(n / len(counted), 4) if counted else None
    return {
        "name": lane["name"], "sha": lane.get("sha"), "patch": lane.get("patch"),
        "valid": not witness, "witness_failures": witness,
        "cells": {"planned": len(own), "finished": len(finished), "graded": len(graded)},
        "outcomes": dict(collections.Counter(str(c["result"].get("outcome")) for c in finished)),
        "classes": dict(sorted(collections.Counter(c["class"] for c in own).items())),
        "pass_rate": rate(sum(1 for c in counted if c["class"] == "correct")),
        "first_green_pass_rate": rate(sum(1 for c in counted if _green_pass(c["evaluation"]))),
        # usage.py read totals.models from the run log
        "models": sorted({m for t in totals for m in t.get("models") or []}),
        "totals": _sums(totals),
        "cost_reasons": sorted({t["cost_reason"] for t in totals if t.get("cost_reason")}),
        "stages": [{"stage": k, "cells": len(v), **_sums(v)} for k, v in sorted(
            stages.items(), key=lambda kv: STAGE_ORDER.index(kv[0]) if kv[0] in STAGE_ORDER else len(STAGE_ORDER))],
        "shape": {k: _sum([e[k] for e in shaped]) for k in SHAPE_KEYS} if phase == "shape" else None,
    }


# ---- the rule ---------------------------------------------------------------------------

def _metric(cell, name):
    """`(present, value)` of a `totals` or top-level `result.json` field."""
    r = cell["result"] or {}
    for src in (r.get("totals") or {}, r):
        if name in src:
            return True, src[name]
    return False, None


def apply_rule(rule, cells, lanes):
    """The verdict: `decision`, the numbers, and a `line` naming the rule."""
    kind = rule.get("kind")
    out = lambda decision, line, **kw: {"kind": kind, "decision": decision, "line": f"Rule {kind}: {line}", **kw}
    if kind not in RULE_KINDS:
        return out("invalid_rule", "unknown kind")
    if kind == "descriptive":
        return out("none", "no decision, results only")
    base, cand = rule.get("baseline"), rule.get("candidate")
    by_name = {l["name"]: l for l in lanes}
    if base not in by_name or cand not in by_name or base == cand:
        return out("invalid_rule", f"baseline {base!r} and candidate {cand!r} must be two lanes of the experiment")
    bad = [n for n in (base, cand) if not by_name[n]["valid"]]
    if bad:
        return out("invalid", f"lane {', '.join(bad)} is invalid (witness failed)")
    by = {n: {(c["plan"]["task"], c["plan"]["rep"]): c for c in cells if c["plan"]["lane"] == n} for n in (base, cand)}
    keys = sorted(set(by[base]) | set(by[cand]))
    ungraded = [f"{t}/r{r}" for t, r in keys if not all(
        (t, r) in by[n] and by[n][(t, r)]["class"] in COUNTED for n in (base, cand))]
    if ungraded:
        return out("incomplete", f"{len(ungraded)} task/rep infrastructure, incomplete or missing on a lane",
                   ungraded=ungraded)
    ok = {n: {k: c["class"] == "correct" for k, c in by[n].items()} for n in (base, cand)}
    params = {k: rule[k] for k in THRESHOLDS if k in rule}
    sign = (params.get("min_gain_points", 0), params.get("max_p", 1))
    if kind == "paired_sign":
        res = paired_sign([{"candidate": ok[cand][k], "baseline": ok[base][k]} for k in keys], *sign)
        nums = (f"gain {res['gain_points']} points, p {res['p']}, candidate-only {res['candidate_only']}, "
                f"baseline-only {res['baseline_only']}, blocks {res['blocks']}")
    elif kind == "task_sign":
        tasks = [{f"{who}_{k}": v for who, n in (("candidate", cand), ("baseline", base))
                  for k, v in (("correct", sum(ok[n][k] for k in keys if k[0] == t)),
                               ("total", sum(1 for k in keys if k[0] == t)))}
                 for t in sorted({t for t, _ in keys})]
        res = task_sign(tasks, *sign)
        nums = (f"gain {res['gain_points']} points, p {res['p']}, candidate-favored {res['candidate_favored']}, "
                f"baseline-favored {res['baseline_favored']}, ties {res['ties']}")
    else:
        metric = rule.get("metric", "wall_s")
        found = [_metric(c, metric) for c in cells]
        vals = {n: [_metric(by[n][k], metric)[1] for k in keys] for n in (base, cand)}
        if not any(p for p, _ in found) or any(
                v is not None and (isinstance(v, bool) or not isinstance(v, (int, float))) for _, v in found):
            return out("invalid_rule", f"metric {metric!r} is not a numeric result or totals field", metric=metric)
        if any(v is None for vs in vals.values() for v in vs):
            return out("incomplete", f"metric {metric} is missing in some cells", metric=metric)
        side = lambda n: {"correct": sum(ok[n][k] for k in keys), "total": len(keys), "metrics": vals[n]}
        res = cost_at_quality(side(base), side(cand), params.get("max_loss_points", 0),
                              params.get("min_saving_pct", 0), metric)
        nums = (f"quality loss {res['loss_points']} points (holds: {str(res['quality_holds']).lower()}), "
                f"{metric} saving {res['saving_pct']}% (median {res['baseline_median']} -> {res['candidate_median']})")
    res.update({"kind": kind, "baseline": base, "candidate": cand, "params": params})
    res["line"] = (f"Rule {kind} ({cand} vs {base}" + "".join(f", {k} {v}" for k, v in params.items())
                   + f"): {res['decision'].upper()}: {nums}")
    return res


# ---- report -----------------------------------------------------------------------------

def check_rule(rule):
    """ReportError unless every threshold of `rule` is a number or a decimal string."""
    for k in THRESHOLDS:
        v = rule.get(k)
        if k in rule and (isinstance(v, bool) or not (
                isinstance(v, (int, float)) or (isinstance(v, str) and DECIMAL.fullmatch(v.strip())))):
            raise ReportError(f"decision_rule.{k}: must be a number or a decimal string")


def report(run_dir):
    try:
        exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    except experiment.ExperimentError as e:
        raise ReportError(f"experiment error: {e}") from None
    check_rule(exp["decision_rule"])
    cells = _load_cells(run_dir, exp["phase"])
    lanes = [_lane(l, cells, exp["phase"]) for l in exp["lanes"]]
    return {"experiment": exp["id"], "phase": exp["phase"], "decision_rule": exp["decision_rule"],
            "verdict": apply_rule(exp["decision_rule"], cells, lanes), "lanes": lanes}


COLS = [("requests", "requests"), ("input_tokens", "input"), ("cached_input_tokens", "cached"),
        ("output_tokens", "output"), ("reasoning_tokens", "reasoning"), ("cache_hit_share", "cache hit"),
        ("cost_usd", "cost USD"), ("wall_s", "wall s")]


def _row(cells):
    return "| " + " | ".join("n/a" if v is None else str(v) for v in cells) + " |"


def _table(heads, rows):
    return [_row(heads), "|" + "---|" * len(heads)] + [_row(r) for r in rows]


def render(rep):
    out = [f"# Report: {rep['experiment']} ({rep['phase']})", "", f"**Verdict:** {rep['verdict']['line']}", "",
           "## Lanes", ""]
    out += _table(["lane", "valid", "cells planned/finished/graded", "pass rate", "first-green-pass rate"]
                  + [h for _, h in COLS],
                  [[l["name"], "yes" if l["valid"] else "INVALID", "/".join(str(v) for v in l["cells"].values()),
                    l["pass_rate"], l["first_green_pass_rate"]] + [l["totals"][k] for k, _ in COLS]
                   for l in rep["lanes"]])
    for l in rep["lanes"]:
        out += ["", f"### {l['name']}", "", f"- sha `{l['sha']}`, patch {l['patch'] or 'none'}",
                f"- models (run log): {', '.join(l['models']) or 'none logged'}",
                f"- outcomes: {', '.join(f'{k} {v}' for k, v in sorted(l['outcomes'].items())) or 'none'}",
                f"- classes: {', '.join(f'{k} {v}' for k, v in l['classes'].items()) or 'none'}"]
        out += [f"- cost notes: {'; '.join(l['cost_reasons'])}"] if l["cost_reasons"] else []
        out += [f"- WITNESS FAILED: {w}" for w in l["witness_failures"]]
        if l["shape"]:
            out.append("- shape: " + ", ".join(f"{k} {'n/a' if v is None else v}" for k, v in l["shape"].items()))
        if l["stages"]:
            out += [""] + _table(["stage", "cells"] + [h for _, h in COLS],
                                 [[s["stage"], s["cells"]] + [s[k] for k, _ in COLS] for s in l["stages"]])
    return "\n".join(out) + "\n"


def write(run_dir):
    rep = report(run_dir)
    common.write_json(os.path.join(run_dir, "report.json"), rep)
    with open(os.path.join(run_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write(render(rep))
    return rep


def main(argv):
    if len(argv) != 1 or argv[0].startswith("-"):
        print("usage: lanes-report <run-dir>", file=sys.stderr)
        return 2
    try:
        rep = write(argv[0])
    except (ReportError, OSError, KeyError, ValueError) as e:
        print(f"lanes-report: {e}", file=sys.stderr)
        return 2
    print(rep["verdict"]["line"])
    return 0
