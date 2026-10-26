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
from math import comb, exp, lgamma, log, sqrt

from . import common, costguard, experiment, usage

RULE_KINDS = ("paired_sign", "task_sign", "cost_at_quality", "keep_revert", "descriptive")
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
# - Kogen's endings are not the Lab's workflow-end strings: `classify` maps them;
# - climb reports leave plumbing cells (timeouts, truncations, provider and harness failures) out of the
#   quality rates, where the Lab counts timeouts and context exhaustion as `workflow_failure`.


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


# ---- confidence intervals (floats; they inform the climb verdict, see DECISION-RULES.md) ---

Z95 = 1.959964


def wilson(k, n, z=Z95):
    """Wilson score interval of k successes in n; None without trials."""
    if n <= 0:
        return None
    p, z2 = k / n, z * z
    centre = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = z * sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def _binom_ge(k, n, p):
    """P(X >= k), X ~ Binomial(n, p), 0 < p < 1."""
    return min(1.0, sum(exp(lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) + i * log(p) + (n - i) * log(1 - p))
                        for i in range(k, n + 1)))


def _solve(f, target, rising):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (f(mid) < target) == rising:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def clopper_pearson(k, n, alpha=0.05):
    """Exact two-sided (1 - alpha) interval of k successes in n; None without trials."""
    if n <= 0:
        return None
    tail = alpha / 2
    lower = 0.0 if k == 0 else _solve(lambda p: _binom_ge(k, n, p), tail, True)
    upper = 1.0 if k == n else _solve(lambda p: 1 - _binom_ge(k + 1, n, p), tail, False)
    return lower, upper


def paired_difference_ci(candidate_only, baseline_only, pairs, alpha=0.05):  # `pairs`: the units (tasks)
    """Exact, conservative interval of the paired pass-rate difference (candidate - baseline).

    Each pair is a candidate-only win (p+), a baseline-only win (p-) or a tie; d = p+ - p-.
    Clopper-Pearson intervals of p+ and p- at level 1 - alpha/2 each (Bonferroni) give
    [lo+ - hi-, hi+ - lo-], which holds at level 1 - alpha. Wide for few pairs, on purpose."""
    if pairs <= 0:
        return None
    plus = clopper_pearson(candidate_only, pairs, alpha / 2)
    minus = clopper_pearson(baseline_only, pairs, alpha / 2)
    return max(-1.0, plus[0] - minus[1]), min(1.0, plus[1] - minus[0])


def hoeffding(mean, n, alpha=0.05, low=-1.0, high=1.0):
    """Conservative two-sided (1 - alpha) interval of the mean of n independent values in [low, high]:
    mean +- (high - low) * sqrt(ln(2 / alpha) / (2 n)) (Hoeffding), clipped to the range; None without values."""
    if n <= 0:
        return None
    half = (high - low) * sqrt(log(2 / alpha) / (2 * n))
    return max(low, float(mean) - half), min(high, float(mean) + half)


def _ci_text(ci):
    return "n/a" if ci is None else f"[{ci[0]:.2f}, {ci[1]:.2f}]"


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


def _shape_class(shape):
    """The class of the Intent an e2e cell shaped: correct, incorrect or infrastructure (as `classify` names them)."""
    state = _eval_state(shape, "shape")
    return {"all_passed": "correct", "failed": "incorrect"}.get(state, "infrastructure")


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
    if ending.startswith("interrupted") or ending in ("controller_lost", "signal", "cost_cap"):
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


def _lane(lane, cells, phase, part=None):
    """`part`: task -> split of a climb experiment. Then the rates leave plumbing cells out, and the
    outcome, class, plumbing and witness details cover train cells only (test details stay out)."""
    own = [c for c in cells if c["plan"]["lane"] == lane["name"]]
    finished = [c for c in own if c["result"]]
    counted = [c for c in own if c["class"] in COUNTED and not (part and plumbing(c))]  # the Lab's denominator
    shown = [c for c in own if not part or part.get(c["plan"]["task"]) == "train"]
    graded = [c["evaluation"] for c in own if c["evaluation"] is not None]
    totals = [c["result"].get("totals") or {} for c in finished]
    stages = collections.defaultdict(list)
    for c in finished:
        for s in c["result"].get("stages") or []:
            stages[s["stage"]].append(s)
    found = [(c, f) for c in finished  # a cell that never ran has no log
             for f in check_witnesses(lane.get("expect"), c["log"])]
    witness = [f"{c['plan']['cell']}: {f}" for c, f in found if c in shown]
    hidden = sum(1 for c, _ in found if c not in shown)
    shaped = [e for e in graded if all(isinstance(e.get(k), int) for k in SHAPE_KEYS)]
    shapes = [e["shape"] for e in graded if phase == "e2e" and isinstance(e.get("shape"), dict)]
    if phase == "e2e":  # an e2e cell's evaluation holds the grade of the Intent it shaped under `shape`
        shaped = [e for e in shapes if all(isinstance(e.get(k), int) for k in SHAPE_KEYS)]
    rate = lambda n: round(n / len(counted), 4) if counted else None
    return {
        "name": lane["name"], "sha": lane.get("sha"), "patch": lane.get("patch"),
        "valid": not found, "witness_failures": witness, "witness_failures_test": hidden,
        "cells": {"planned": len(own), "finished": len(finished), "graded": len(graded)},
        "outcomes": dict(collections.Counter(str(c["result"].get("outcome")) for c in finished if c in shown)),
        "classes": dict(sorted(collections.Counter(c["class"] for c in shown).items())),
        "pass_rate": rate(sum(1 for c in counted if c["class"] == "correct")),
        "pass_rate_ci": wilson(sum(1 for c in counted if c["class"] == "correct"), len(counted)),
        "first_green_pass_rate": rate(sum(1 for c in counted if _green_pass(c["evaluation"]))),
        "first_green_pass_rate_ci": wilson(sum(1 for c in counted if _green_pass(c["evaluation"])), len(counted)),
        "plumbing": dict(sorted(collections.Counter(p for p in map(plumbing, shown) if p).items())),
        # usage.py read totals.models from the run log
        "models": sorted({m for t in totals for m in t.get("models") or []}),
        "totals": _sums(totals),
        "cost_reasons": sorted({t["cost_reason"] for t in totals if t.get("cost_reason")}),
        "model_sources": sorted({m for t in totals for m in t.get("model_sources") or []}),
        "stages": [{"stage": k, "cells": len(v), **_sums(v)} for k, v in sorted(
            stages.items(), key=lambda kv: STAGE_ORDER.index(kv[0]) if kv[0] in STAGE_ORDER else len(STAGE_ORDER))],
        "shape": {k: _sum([e[k] for e in shaped]) for k in SHAPE_KEYS} if phase == "shape" or shapes else None,
        **({"shape_classes": dict(sorted(collections.Counter(_shape_class(e) for e in shapes).items()))} if shapes else {}),
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
    if kind == "keep_revert":
        return out("invalid_rule", "keep_revert needs a climb experiment (kind: climb)")
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


# ---- plumbing and the climb rule ---------------------------------------------------------

PLUMBING = ("timeout", "provider_error", "truncation", "harness", "cost_cap")
TRUNCATION = re.compile(r"truncat\w*|context_exhausted")  # Kogen's endings (build.ex); anchored with fullmatch


def plumbing(cell):
    """The plumbing category of a cell (not a task failure), or None."""
    ending = (cell["result"] or {}).get("outcome")
    if isinstance(ending, str) and ending not in ("landed", "ok"):
        if ending == "cost_cap":  # the cost guard stopped the cell: not a task failure
            return "cost_cap"
        if ending.startswith("timeout"):
            return "timeout"
        if TRUNCATION.fullmatch(ending):
            return "truncation"
        if ending.startswith("provider_failure") or any(
                e.get("provider_failure") for e in cell["log"] if e.get("event") == "outcome"):
            return "provider_error"
    return "harness" if cell["class"] in ("infrastructure", "incomplete") else None


def _split_of(exp):
    return {t: part for part in ("train", "test") for t in exp["split"][part]}


def _rate(k, n):
    return {"correct": k, "n": n, "rate": round(k / n, 4) if n else None, "ci": wilson(k, n)}


def climb_report(cells, exp):
    """Per split: Wilson rates of both lanes and the paired difference, over cells without plumbing."""
    part = _split_of(exp)
    out = {"min_effect": exp["min_effect"], "plumbing": [], "splits": {}, "train_failures": []}
    usable = {}
    for c in cells:
        cat = plumbing(c)
        key = (c["plan"]["lane"], c["plan"]["task"], c["plan"]["rep"])
        if cat:
            out["plumbing"].append({"cell": c["plan"]["cell"], "lane": key[0], "split": part.get(key[1]),
                                    "category": cat, "outcome": (c["result"] or {}).get("outcome")
                                    if part.get(key[1]) == "train" else None})
        elif key[1] in part:
            usable[key] = c["class"] == "correct"
            if part[key[1]] == "train" and c["class"] != "correct":
                out["train_failures"].append({"cell": c["plan"]["cell"], "lane": key[0], "class": c["class"],
                                              "outcome": (c["result"] or {}).get("outcome")})
    for name in ("train", "test"):
        res = {}
        for lane in ("baseline", "candidate"):
            v = [ok for (l, t, _), ok in usable.items() if l == lane and part[t] == name]
            res[lane] = _rate(sum(v), len(v))
        # the task is the unit: its reps (usable on both lanes) average into one difference
        per_task = collections.defaultdict(list)
        for (l, t, r) in sorted(usable):
            if l == "candidate" and part[t] == name and ("baseline", t, r) in usable:
                per_task[t].append(int(usable[(l, t, r)]) - int(usable[("baseline", t, r)]))
        mean = {t: Fraction(sum(d), len(d)) for t, d in per_task.items()}
        b = sum(1 for m in mean.values() if m > 0)
        o = sum(1 for m in mean.values() if m < 0)
        pairs = sum(len(d) for d in per_task.values())
        # the pass-rate difference: the mean over tasks of each task's mean rep difference
        diff = sum(mean.values(), Fraction(0)) / len(mean) if mean else None
        res.update({"unit": "task", "tasks": len(mean), "pairs": pairs, "candidate_better": b, "baseline_better": o,
                    "tied": len(mean) - b - o,
                    "difference": None if diff is None else round(float(diff), 4),
                    "difference_exact": None if diff is None else ratio_decimal(diff),
                    "pair_difference": round(sum(sum(d) for d in per_task.values()) / pairs, 4) if pairs else None,
                    "difference_ci": hoeffding(diff, len(mean)) if mean else None})
        out["splits"][name] = res
    out["plumbing"].sort(key=lambda r: r["cell"])
    out["plumbing_counts"] = {lane: {cat: sum(1 for r in out["plumbing"] if r["lane"] == lane and r["category"] == cat)
                                     for cat in PLUMBING} for lane in ("baseline", "candidate")}
    return out


def task_sign_p(split):
    """`(k, n, p)` of a split: k candidate-better of n untied tasks, p = P(X >= k), X ~ Binomial(n, 1/2), exact."""
    k = split["candidate_better"]
    n = k + split["baseline_better"]
    return k, n, binomial_tail(k, n)


def keep_revert(splits, min_effect, improves=None):
    """`splits`: {train, test: {tasks, difference_exact, difference_ci, candidate_better, baseline_better}};
    decision and case. The pass-rate difference is exact (`difference_exact`, a decimal or n/d); the interval
    is float. `improves` (`{"test": "task_sign", "max_p": p}`) swaps the interval for the exact sign test over tasks."""
    if any(s["tasks"] == 0 for s in splits.values()):
        return {"decision": "incomplete", "case": "no_pairs"}
    diff = {n: ratio(s["difference_exact"]) for n, s in splits.items()}
    if improves:
        gains = {n: diff[n] > ratio(min_effect) and task_sign_p(splits[n])[2] <= ratio(improves["max_p"])
                 for n in splits}
    else:
        gains = {n: diff[n] > ratio(min_effect) and splits[n]["difference_ci"][0] > 0  # beats min_effect, interval excludes zero
                 for n in splits}
    if any(d < 0 for d in diff.values()):
        return {"decision": "revert", "case": "drop"}
    if gains["train"] and gains["test"]:
        return {"decision": "keep", "case": "improved_both"}
    if gains["train"] and diff["test"] <= ratio(min_effect):  # test flat; a larger gain with a wide interval is noise
        return {"decision": "revert", "case": "overfit"}
    return {"decision": "within_noise", "case": "within_noise"}


def _climb_verdict(rep, exp, lanes):
    res = {"kind": "keep_revert", "baseline": "baseline", "candidate": "candidate", "params": {}}
    bad = [l["name"] for l in lanes if not l["valid"]]
    if bad:
        return {**res, "decision": "invalid", "line": f"Rule keep_revert: INVALID: lane {', '.join(bad)} failed a witness"}
    improves = exp["decision_rule"].get("improves")
    r = keep_revert(rep["splits"], exp["min_effect"], improves)
    if improves:
        return _sign_verdict(res, r, rep, exp, improves)
    nums = "; ".join(
        f"{n} {_diff_text(s)} ({s['tasks']} tasks, {s['pairs']} pairs, candidate-better {s['candidate_better']}, "
        f"baseline-better {s['baseline_better']})"
        for n, s in rep["splits"].items())
    words = {"improved_both": "train and test both improved by more than min_effect with intervals above zero",
             "overfit": "train improved, test flat (at most min_effect): overfit, revert",
             "drop": "a split dropped: revert",
             "within_noise": "within noise; don't merge",
             "no_pairs": "a split has no task with a usable pair of cells (plumbing excluded)"}[r["case"]]
    shown = {"within_noise": "WITHIN NOISE"}.get(r["decision"], r["decision"].upper())
    res.update(r)
    res["line"] = (f"Rule keep_revert (candidate vs baseline, min_effect {exp['min_effect']}): {shown} "
                   f"[{r['case']}]: {words}; pass-rate differences (task unit, Hoeffding 95%) vs min_effect "
                   f"{exp['min_effect']}: {nums}")
    return res


def _sign_verdict(res, r, rep, exp, improves):
    """The task_sign flavour of the climb verdict line: k/n and p of each split instead of the interval."""
    def split_text(n, s):
        k, m, p = task_sign_p(s)
        return (f"{n} {float(s['difference']):+.2f} (sign test {k}/{m} tasks candidate-better, p {float(p):.4f}; "
                f"{s['tasks']} tasks, {s['pairs']} pairs)") if s["difference"] is not None else f"{n} n/a"
    nums = "; ".join(split_text(n, s) for n, s in rep["splits"].items())
    words = {"improved_both": "train and test both improved by more than min_effect with a sign test p at most max_p",
             "overfit": "train improved, test flat (at most min_effect): overfit, revert",
             "drop": "a split dropped: revert",
             "within_noise": "within noise; don't merge",
             "no_pairs": "a split has no task with a usable pair of cells (plumbing excluded)"}[r["case"]]
    shown = {"within_noise": "WITHIN NOISE"}.get(r["decision"], r["decision"].upper())
    res.update(r)
    res["params"] = {"improves": improves}
    res["sign"] = {n: dict(zip(("k", "n", "p"), (k, m, float(p)))) for n, (k, m, p) in
                   ((n, task_sign_p(s)) for n, s in rep["splits"].items())}
    res["line"] = (f"Rule keep_revert (candidate vs baseline, min_effect {exp['min_effect']}, improves task_sign "
                   f"max_p {improves['max_p']}): {shown} [{r['case']}]: {words}; pass-rate differences (task unit, "
                   f"exact one-sided sign test over tasks) vs min_effect {exp['min_effect']}: {nums}")
    return res


def _diff_text(s):
    d = s["difference"]
    return "n/a" if d is None else f"{float(d):+.2f} {_ci_text(s['difference_ci'])}"


# ---- report -----------------------------------------------------------------------------

def check_rule(rule):
    """ReportError unless every threshold of `rule` is a number or a decimal string."""
    for k in THRESHOLDS:
        v = rule.get(k)
        if k in rule and (isinstance(v, bool) or not (
                isinstance(v, (int, float)) or (isinstance(v, str) and DECIMAL.fullmatch(v.strip())))):
            raise ReportError(f"decision_rule.{k}: must be a number or a decimal string")


def cost_section(run_dir, exp, cells):
    """Spend against the caps: total and per lane, and which cap stopped the run (cost-stop.json)."""
    spent, lanes = costguard.estimate(run_dir, per_lane=True)
    cap = exp.get("cost_cap_usd")
    stop = os.path.join(run_dir, costguard.STOP)
    capped = sorted(c["plan"]["cell"] for c in cells if (c["result"] or {}).get("outcome") == "cost_cap")
    names, started, limits = costguard.lane_providers(exp), costguard.started_cells(run_dir, exp), costguard.rate_limited(run_dir)
    by_provider, usd = costguard.provider_spend(run_dir, exp), costguard.usd_caps(exp)
    providers = {}
    for p in sorted(set(names.values()) | set(by_provider)):
        providers[p] = {"spent_usd": by_provider.get(p, 0.0), "usd_cap": usd[p][0] if p in usd else None,
                        "hard_cap_usd": usd[p][1] if p in usd else None, "cells_started": len(started.get(p, ())),
                        "cells_cap": ((exp.get("provider_caps") or {}).get(p) or {}).get("cells"),
                        "rate_limited": limits.get(p)}
    return {"providers": providers, "lane_providers": names, "cost_cap_usd": cap, "hard_cap_usd": None if cap is None else cap * costguard.HARD_FACTOR,
            "spent_usd": spent, "lanes": {l["name"]: lanes.get(l["name"], 0.0) for l in exp["lanes"]},
            "cost_cap_cells": capped,
            "not_started": sum(1 for c in cells if not os.path.isdir(common.cell_dir(run_dir, c["plan"]["cell"]))),
            # a cost_cap cell is a hard stop whatever the note says (a remote cell's note stays on its host)
            "stopped": "hard" if capped else (common.read_json(stop)["cap"] if os.path.isfile(stop) else None)}


def report(run_dir):
    try:
        exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    except experiment.ExperimentError as e:
        raise ReportError(f"experiment error: {e}") from None
    check_rule(exp["decision_rule"])
    if exp["phase"] == "probe":
        from . import probe  # probe imports this module
        return probe.report_probe(run_dir, exp)
    cells = _load_cells(run_dir, exp["phase"])
    part = _split_of(exp) if exp.get("kind") == "climb" else None
    lanes = [_lane(l, cells, exp["phase"], part) for l in exp["lanes"]]
    rep = {"experiment": exp["id"], "phase": exp["phase"], "decision_rule": exp["decision_rule"], "lanes": lanes,
           "cost": cost_section(run_dir, exp, cells)}
    if exp.get("kind") == "climb":
        rep["climb"] = climb_report(cells, exp)
        rep["verdict"] = _climb_verdict(rep["climb"], exp, lanes)
    else:
        rep["verdict"] = apply_rule(exp["decision_rule"], cells, lanes)
    return rep


COLS = [("requests", "requests"), ("input_tokens", "input"), ("cached_input_tokens", "cached"),
        ("output_tokens", "output"), ("reasoning_tokens", "reasoning"), ("cache_hit_share", "cache hit"),
        ("cost_usd", "cost USD"), ("wall_s", "wall s")]


def _row(cells):
    return "| " + " | ".join("n/a" if v is None else str(v) for v in cells) + " |"


def _table(heads, rows):
    return [_row(heads), "|" + "---|" * len(heads)] + [_row(r) for r in rows]


def _rate_text(rate, ci):
    return None if rate is None else f"{rate} {_ci_text(ci)}"


def _render_cost(c):
    cap, hard = c["cost_cap_usd"], c["hard_cap_usd"]
    out = ["", "## Spend vs cost cap", "",
           "Spend counts finished cells and unpriced requests at the guard's fallback price, so it is an upper "
           "estimate (lanes/FORMATS.md, Cost cap).", ""]
    share = lambda v, limit: "n/a" if not limit else f"{100 * v / limit:.0f}%"
    gpt_spent = c["providers"].get("chatgpt", {}).get("spent_usd", 0.0)
    gpt = lambda n: c["lane_providers"].get(n, "chatgpt") == "chatgpt"  # the cap covers ChatGPT lanes only
    out += _table(["lane", "provider", "spend USD", "of soft cap", "of hard cap"],
                  [[n, c["lane_providers"].get(n, "chatgpt"), f"{v:.4f}", share(v, cap) if gpt(n) else "n/a",
                    share(v, hard) if gpt(n) else "n/a"] for n, v in c["lanes"].items()]
                  + [["total", "", f"{c['spent_usd']:.4f}", share(gpt_spent, cap), share(gpt_spent, hard)]])
    out += ["", "`cost_cap_usd` covers ChatGPT-priced spend only; other providers' dollars are estimates and stop a run "
            "only through their own `provider_caps`.", ""]
    out += _table(["provider", "est. spend USD", "$ cap (soft / hard)", "cells started", "cell cap", "rate limited"],
                  [[p, f"{v['spent_usd']:.4f}",
                    "none" if v["usd_cap"] is None else f"{v['usd_cap']:g} / {v['hard_cap_usd']:g}"
                    + f" ({100 * v['spent_usd'] / v['usd_cap']:.0f}%)",
                    v["cells_started"], "none" if v["cells_cap"] is None else v["cells_cap"],
                    "no" if not v["rate_limited"] else f"{v['rate_limited']['reason']} ({v['rate_limited']['cell']})"]
                   for p, v in c["providers"].items()])
    out += ["", "- soft cap: " + ("none set" if cap is None else f"${cap:g}") + "; hard cap: "
            + ("none set" if hard is None else f"${hard:g}")]
    if c["stopped"] == "hard":
        out.append(f"- COST CAP STOPPED THE RUN: the hard cap ended {len(c['cost_cap_cells'])} cell(s) "
                   f"as cost_cap ({', '.join(c['cost_cap_cells']) or 'none recorded'}); {c['not_started']} cell(s) were not started")
    elif c["stopped"] == "soft":
        out.append(f"- COST CAP STOPPED THE RUN: the soft cap was reached; {c['not_started']} cell(s) were not started")
    return out


def _render_climb(c):
    out = ["", "## Climb", "", "Rates are Wilson 95% over cells. The unit of the difference is the task: each task's "
           "difference is the mean over its reps of candidate minus baseline (cells with plumbing failures "
           "excluded); the difference is the pass-rate difference, the mean of those over tasks, compared with "
           "min_effect, with a conservative Hoeffding 95% interval over tasks (values in [-1, 1]). "
           f"min_effect {c['min_effect']}.", ""]
    rows = [[n, s["baseline"]["n"], _rate_text(s["baseline"]["rate"], s["baseline"]["ci"]), s["candidate"]["n"],
             _rate_text(s["candidate"]["rate"], s["candidate"]["ci"]), s["tasks"], s["pairs"], _diff_text(s)]
            for n, s in c["splits"].items()]
    out += _table(["split", "baseline cells", "baseline rate", "candidate cells", "candidate rate", "tasks",
                   "pairs", "difference (task unit)"], rows)
    out += ["", "### Plumbing failures (excluded from the rates above)", ""]
    out += _table(["cell", "lane", "split", "category", "outcome"],
                  [[r["cell"], r["lane"], r["split"], r["category"], r["outcome"]] for r in c["plumbing"]]) \
        if c["plumbing"] else ["none"]
    out += ["", "### Train failures for the next round", ""]
    out += _table(["cell", "lane", "class", "outcome"],
                  [[r["cell"], r["lane"], r["class"], r["outcome"]] for r in c["train_failures"]]) \
        if c["train_failures"] else ["none"]
    return out


def render(rep):
    if rep["phase"] == "probe":
        from . import probe
        return probe.render(rep)
    out = [f"# Report: {rep['experiment']} ({rep['phase']})", "", f"**Verdict:** {rep['verdict']['line']}", "",
           "## Lanes", ""]
    note = " (plumbing excluded)" if "climb" in rep else ""
    out += _table(["lane", "valid", "cells planned/finished/graded", "pass rate" + note, "first-green-pass rate" + note]
                  + [h for _, h in COLS],
                  [[l["name"], "yes" if l["valid"] else "INVALID", "/".join(str(v) for v in l["cells"].values()),
                    _rate_text(l["pass_rate"], l["pass_rate_ci"]),
                    _rate_text(l["first_green_pass_rate"], l["first_green_pass_rate_ci"])] + [l["totals"][k] for k, _ in COLS]
                   for l in rep["lanes"]])
    if "climb" in rep:
        out += _render_climb(rep["climb"])
    out += _render_cost(rep["cost"])
    scope = " (train cells)" if "climb" in rep else ""
    for l in rep["lanes"]:
        out += ["", f"### {l['name']}", "", f"- sha `{l['sha']}`, patch {l['patch'] or 'none'}",
                f"- models (run log): {', '.join(l['models']) or 'none logged'}"
                + (f" (name source: {', '.join(l['model_sources'])})" if l["model_sources"] else ""),
                f"- outcomes{scope}: {', '.join(f'{k} {v}' for k, v in sorted(l['outcomes'].items())) or 'none'}",
                f"- classes{scope}: {', '.join(f'{k} {v}' for k, v in l['classes'].items()) or 'none'}",
                f"- plumbing{scope}: {', '.join(f'{k} {v}' for k, v in l['plumbing'].items()) or 'none'}"]
        out += [f"- cost notes: {'; '.join(l['cost_reasons'])}"] if l["cost_reasons"] else []
        out += [f"- WITNESS FAILED: {w}" for w in l["witness_failures"]]
        out += [f"- WITNESS FAILED on {l['witness_failures_test']} test cells (not listed)"] if l["witness_failures_test"] else []
        if l["shape"]:
            out.append("- shape: " + ", ".join(f"{k} {'n/a' if v is None else v}" for k, v in l["shape"].items()))
        if l.get("shape_classes"):
            out.append("- shape classes: " + ", ".join(f"{k} {v}" for k, v in l["shape_classes"].items()))
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
