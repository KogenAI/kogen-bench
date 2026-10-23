"""Run-to-run noise of one lane: two runs of the same baseline on the same tasks, compared, or the two
halves of one run with twice the reps (`split_half`).

`noise(run_a, run_b)` and `split_half(run)` return the noise record `lanes-noise` writes; `check_gate(exp,
exp_path)` is the climb gate of `lanes-plan`: the experiment's `noise_ref` must name a record for the same
baseline and task set whose `spread` is smaller than the experiment's `min_effect`. When the climb screens with
the task sign test, the floor is what that test can resolve (`sign_floor`) instead of the Hoeffding floor.
"""

import argparse
import os
import sys
from math import sqrt

from . import common, experiment, plan_hashes, report

# two-sided 95% Student t quantiles, df 1..30 (the normal 1.96 beyond)
T95 = (12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145,
       2.131, 2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048,
       2.045, 2.042)
METRICS = ("pass_rate", "cost_usd", "tokens", "wall_s")


class NoiseError(ValueError):
    pass


def t95(df):
    return T95[df - 1] if df <= len(T95) else 1.96


def floor(tasks):
    """The least pass-rate difference the keep/revert rule can resolve over this many tasks: the half-width of
    its Hoeffding interval (report.climb_report), whatever the runs showed. Reps do not lower it: the task is the unit."""
    return report.hoeffding(0, tasks)[1]


def sign_floor(max_p, reps, tasks):
    """The least pass-rate difference the task sign test can resolve: k_min / (reps * tasks), k_min the least k with
    0.5 ** k <= max_p (k tasks better, none worse, reach p <= max_p)."""
    k = 1
    while 0.5 ** k > max_p:
        k += 1
    return k, k / (reps * tasks)


def _load(run_dir):
    try:
        exp = experiment.load(os.path.join(run_dir, "experiment.json"))
        plan = common.read_json(os.path.join(run_dir, "PLAN.json"))
        cells = report._load_cells(run_dir, exp["phase"])
    except (experiment.ExperimentError, report.ReportError, OSError, ValueError) as e:
        raise NoiseError(f"{run_dir}: {e}") from None
    named = [x for x in exp["lanes"] if x["name"] == "baseline"]
    if named:
        lane = named[0]
    elif len(exp["lanes"]) == 1:
        lane = exp["lanes"][0]
    else:
        raise NoiseError(f"{run_dir}: more than one lane and none named baseline")
    return exp, plan, lane, [c for c in cells if c["plan"]["lane"] == lane["name"]]


def _same_plan(a, b):
    """Both runs must be one plan under two ids."""
    (ea, pa, la, _), (eb, pb, lb, _) = a, b
    drop = lambda e: {k: v for k, v in e.items() if k not in ("id", "hosts", "parent", "round")}
    if ea["id"] == eb["id"]:
        raise NoiseError("the two runs have the same experiment id")
    if drop(pa["experiment"]) != drop(pb["experiment"]) or pa["hashes"] != pb["hashes"]:
        raise NoiseError("the two runs differ in more than the run id (experiment or PLAN.json hashes)")
    art = lambda p: p["lock"].get("artifacts", {}).get(la["name"])
    if art(pa) != art(pb):
        raise NoiseError("the two runs built different baseline artifacts")


def _values(cells):
    """`{task: {metric: mean over usable reps}}`; plumbing cells are left out, a null leaves the metric out."""
    seen = {}
    for c in cells:
        t = c["plan"]["task"]
        row = seen.setdefault(t, {m: [] for m in METRICS})
        if report.plumbing(c):
            continue
        totals = (c["result"] or {}).get("totals") or {}
        row["pass_rate"].append(int(c["class"] == "correct"))
        toks = [totals.get("input_tokens"), totals.get("output_tokens")]
        for m, v in (("cost_usd", totals.get("cost_usd")), ("wall_s", totals.get("wall_s")),
                     ("tokens", None if None in toks else sum(toks))):
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                row[m].append(v)
    return {t: {m: sum(v) / len(v) for m, v in row.items() if v} for t, row in seen.items()}


def _interval(diffs, metric):
    """Interval of the mean difference over tasks: Hoeffding for a pass rate, Student t otherwise."""
    n = len(diffs)
    mean = sum(diffs) / n
    if metric == "pass_rate":
        lo, hi = report.hoeffding(mean, n)
    elif n < 2:
        return None
    else:
        sd = sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
        lo, hi = mean - t95(n - 1) * sd / sqrt(n), mean + t95(n - 1) * sd / sqrt(n)
    return [round(lo, 6), round(hi, 6)]


def noise(run_a, run_b):
    a, b = _load(run_a), _load(run_b)
    _same_plan(a, b)
    return _record(a, b, [a[0]["id"], b[0]["id"]], a[0]["reps"])


def split_half(run_dir, tasks=None, exclude=()):
    """The noise record of one baseline run with 2r reps: reps 1..r against reps r+1..2r of the same cells.
    `tasks` keeps only those tasks, `exclude` drops those; the record's task set is what remains."""
    a = _load(run_dir)
    exp, plan, lane, cells = a
    unknown = sorted((set(tasks or ()) | set(exclude)) - set(exp["tasks"]))
    if unknown:
        raise NoiseError(f"{run_dir}: not tasks of the run: {', '.join(unknown)}")
    keep = [t for t in exp["tasks"] if (tasks is None or t in tasks) and t not in exclude]
    exp = dict(exp, tasks=keep)
    cells = [c for c in cells if c["plan"]["task"] in keep]
    if exp["reps"] < 2 or exp["reps"] % 2:
        raise NoiseError(f"{run_dir}: --split-half needs an even number of reps, at least 2 (the run has {exp['reps']})")
    r = exp["reps"] // 2
    first = (exp, plan, lane, [c for c in cells if c["plan"]["rep"] <= r])
    second = (exp, plan, lane, [c for c in cells if c["plan"]["rep"] > r])
    rec = _record(first, second, [exp["id"]], r)
    rec["split_half"], rec["r"] = True, r
    return rec


def _record(a, b, runs, reps):
    exp, plan, lane = a[0], a[1], a[2]
    va, vb = _values(a[3]), _values(b[3])
    tasks = sorted(set(exp["tasks"]))
    both = {m: [t for t in tasks if m in va.get(t, {}) and m in vb.get(t, {})] for m in METRICS}
    per_task = {t: {m: {"a": round(va[t][m], 6), "b": round(vb[t][m], 6), "abs_diff": round(abs(va[t][m] - vb[t][m]), 6)}
                    for m in METRICS if t in both[m]} for t in tasks}
    overall = {}
    for m in METRICS:
        diffs = [va[t][m] - vb[t][m] for t in both[m]]
        n = len(diffs)
        overall[m] = n and {
            "tasks": n, "a": round(sum(va[t][m] for t in both[m]) / n, 6), "b": round(sum(vb[t][m] for t in both[m]) / n, 6),
            "difference": round(sum(diffs) / n, 6), "abs_difference": round(abs(sum(diffs) / n), 6),
            "mean_abs_task_difference": round(sum(abs(d) for d in diffs) / n, 6), "interval": _interval(diffs, m)} or None
    rate = overall["pass_rate"]
    if rate is None or rate["tasks"] < 2:
        raise NoiseError("need at least 2 tasks with a usable cell in both runs to estimate noise")
    d = [va[t]["pass_rate"] - vb[t]["pass_rate"] for t in both["pass_rate"]]
    # what these runs show: two lanes that do not differ would differ by this much, 95%
    rms = min(1.0, t95(len(d) - 1) * sqrt(sum(x * x for x in d) / len(d)) / sqrt(len(d)))
    sde = max(rms, floor(len(d)))  # runs that agree by chance must not read as "no noise"
    hashes = plan["hashes"]["lanes"][lane["name"]]
    return {
        "kind": "noise", "runs": runs, "phase": exp["phase"], "intent_form": exp.get("intent_form"),
        "baseline": {"sha": lane["sha"], "patch_sha256": hashes["patch"], "settings_sha256": hashes["settings"]},
        "tasks": tasks, "reps": reps, "per_task": per_task, "overall": overall,
        "rms_effect": round(rms, 6), "floor": round(floor(len(d)), 6), "smallest_detectable_effect": round(sde, 6),
        # the number a climb's min_effect must exceed: the larger of the observed and the expected difference
        "spread": round(max(rate["abs_difference"], sde), 6),
    }


def _ids(text):
    return [x for x in text.split(",") if x]


def main(argv=None):
    p = argparse.ArgumentParser(description="Run-to-run noise of a baseline lane from two runs of one plan, "
                                            "or from one run with 2r reps (--split-half).")
    p.add_argument("run_a")
    p.add_argument("run_b", nargs="?", help="the second run (not with --split-half)")
    p.add_argument("--split-half", action="store_true", help="compare reps 1..r with reps r+1..2r of the one run")
    p.add_argument("--tasks", type=_ids, help="with --split-half: only these tasks (comma-separated ids)")
    p.add_argument("--exclude", type=_ids, default=[], help="with --split-half: leave these tasks out (comma-separated ids)")
    p.add_argument("--out", required=True, help="noise record to write (JSON)")
    a = p.parse_args(argv)
    if a.split_half == (a.run_b is not None):
        p.error("give two run directories, or one run directory with --split-half")
    if (a.tasks is not None or a.exclude) and not a.split_half:
        p.error("--tasks and --exclude go with --split-half")
    try:
        rec = split_half(a.run_a, a.tasks, a.exclude) if a.split_half else noise(a.run_a, a.run_b)
        common.write_json(a.out, rec)
    except (NoiseError, OSError) as e:
        print(f"noise: {e}", file=sys.stderr)
        return 2
    print(f"pass-rate spread {rec['spread']} (smallest detectable effect {rec['smallest_detectable_effect']}, "
          f"observed difference {rec['overall']['pass_rate']['abs_difference']}) over {len(rec['tasks'])} tasks",
          file=sys.stderr)
    return 0


def check_gate(exp, exp_path):
    """Refuse a climb whose noise record is missing, for another baseline or task set, or too noisy."""
    ref = exp["noise_ref"]
    path = ref if os.path.isabs(ref) else os.path.join(os.path.dirname(os.path.abspath(exp_path)), ref)
    try:
        rec = common.read_json(path)
        spread, base = rec["spread"], rec["baseline"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise NoiseError(f"noise_ref {ref}: not a readable noise record ({type(e).__name__})") from None
    lane = exp["lanes"][0]
    patch = experiment.patch_path(exp_path, lane)
    want = {"sha": lane["sha"], "patch_sha256": common.sha256_file(patch) if patch else None,
            "settings_sha256": plan_hashes.sha256_json(lane["settings"])}
    if not isinstance(spread, (int, float)) or isinstance(spread, bool) or not isinstance(base, dict):
        raise NoiseError(f"noise_ref {ref}: not a noise record")
    for k, v in want.items():
        if base.get(k) != v:
            raise NoiseError(f"noise_ref {ref}: recorded for another baseline ({k} differs)")
    if rec.get("kind") != "noise":
        raise NoiseError(f"noise_ref {ref}: not a noise record (kind is not noise)")
    if rec.get("reps") != exp["reps"]:
        raise NoiseError(f"noise_ref {ref}: recorded with reps {rec.get('reps')}, the climb has reps {exp['reps']}")
    if rec.get("phase") != exp["phase"] or rec.get("intent_form") != exp.get("intent_form"):
        raise NoiseError(f"noise_ref {ref}: recorded for another phase or Intent form")
    if sorted(rec.get("tasks") or []) != sorted(exp["tasks"]):
        raise NoiseError(f"noise_ref {ref}: recorded for another task set")
    # keep_revert decides on each split alone: the smaller split's floor applies as well
    small = min(len(exp["split"]["train"]), len(exp["split"]["test"]))
    improves = (exp.get("decision_rule") or {}).get("improves")
    if isinstance(improves, dict) and improves.get("test") == "task_sign":
        _sign_gate(exp, rec, ref, small, improves["max_p"])
        return
    spread = round(max(spread, floor(small)), 6)
    if not spread < exp["min_effect"]:
        raise NoiseError(f"noise_ref {ref}: run-to-run spread {spread} (at least the floor for the smaller split, "
                         f"{small} tasks) is not smaller than min_effect {exp['min_effect']}; "
                         "the climb cannot tell such an effect from noise")


def _sign_gate(exp, rec, ref, small, max_p):
    """Under the task sign test the floor is what the test can resolve; the record's own Hoeffding floor does not apply."""
    try:  # the measured part of the record's spread: the observed difference and the t-bound, without the floor
        measured = max(rec["overall"]["pass_rate"]["abs_difference"], rec["rms_effect"])
    except (KeyError, TypeError):
        measured = rec["spread"]  # a record without those fields: its whole spread
    k, f = sign_floor(max_p, exp["reps"], small)
    if small < k:  # even every task better gives p = 0.5 ** small > max_p: the split can never improve
        raise NoiseError(f"noise_ref {ref}: the smaller split has {small} tasks; the sign test at max_p {max_p} "
                         f"needs at least {k}, or no task can show an improvement")
    need = round(max(measured, f), 6)
    if not need < exp["min_effect"]:
        raise NoiseError(f"noise_ref {ref}: min_effect {exp['min_effect']} is not above the larger of the measured "
                         f"run-to-run spread {round(measured, 6)} and the sign-test floor {round(f, 6)} "
                         f"(k_min {k} at max_p {max_p}, / ({exp['reps']} reps x {small} tasks in the smaller split)); "
                         "the climb cannot tell such an effect from noise")
