#!/usr/bin/env python3
"""Recompute every number on the review-value-2 pages from the published records and bundles.

Usage, from the repository root:  python3 -I rounds/review-value-2/analyze.py [--write]

It reads only files under rounds/review-value-2*/ (records.jsonl, PLAN.json and the bundle's attempt.json and
evaluation.json of every cell), uses the Python standard library, makes no model call and needs no private data.
Without --write it prints the tables; with --write it also writes results.json and results.txt next to itself.
The bootstrap resamples whole cases (or whole tasks) 10,000 times with the fixed seed 20261026.
"""
import glob
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = os.path.dirname(HERE)
SEED, B = 20261026, 10000
ROUND = {"A": "review-value-2", "B": "review-value-2-clean", "Coff": "review-value-2-natural-off",
         "Crev": "review-value-2-natural-reviewed", "Sol": "review-value-2-openai"}
ARMS = ["r-now", "r-low", "r-haiku"]
OUT = []


def say(text=""):
    OUT.append(text)
    print(text)


# ---------------------------------------------------------------- statistics
def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def cp_upper(k, n, conf=0.95):
    """One-sided exact (Clopper-Pearson) upper bound; 0 of 84 gives 3.50%."""
    if n == 0:
        return float("nan")
    if k >= n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        cdf = sum(math.comb(n, i) * mid ** i * (1 - mid) ** (n - i) for i in range(k + 1))
        if cdf > 1 - conf:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def quant(xs, q):
    xs = sorted(xs)
    i = q * (len(xs) - 1)
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return float("nan")
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def pct(x, d=1):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:.{d}f}%"


def rng():
    return random.Random(SEED)


# ---------------------------------------------------------------- loading
def load(part):
    rid = ROUND[part]
    base = os.path.join(ROUNDS, rid)
    cells = []
    for f in sorted(glob.glob(os.path.join(base, "bundles", rid, "attempts", "*", "*", "*", "a1", "attempt.json"))):
        d = os.path.dirname(f)
        task, rep, lane = d.split(os.sep)[-4:-1]
        a = json.load(open(f))
        e = json.load(open(os.path.join(d, "evaluation.json")))
        st = {s["stage"]: s for s in a["stages"]}
        totals = a.get("totals") or {}
        cells.append(dict(
            part=part, task=task, rep=rep, lane=lane, outcome=a["outcome"], passed=bool(e.get("all_passed")),
            cost=totals.get("cost_usd") or 0.0, wall=a.get("wall_s"), final_tree=a.get("final_tree"),
            build_requests=(st.get("build") or {}).get("requests") or 0,
            review_requests=(st.get("review") or {}).get("requests") or 0,
            review_cost=(st.get("review") or {}).get("cost_usd") or 0.0,
            review_wall=(st.get("review") or {}).get("wall_s") or 0.0,
            requests=totals.get("requests") or 0))
    return cells


def by(cells, **kw):
    return [c for c in cells if all(c[k] == v for k, v in kw.items())]


def seeded_class(c):
    """seed_red (acceptance caught the planted tree: the builder ran, so the cell is not a test of review),
    infra (the build stopped or timed out), escaped (committed, hidden tests fail), or ok (committed, pass)."""
    if c["build_requests"] > 0:
        return "seed_red"
    if c["outcome"] != "landed":
        return "infra"
    return "ok" if c["passed"] else "escaped"


# ---------------------------------------------------------------- Part A
def part_a(A):
    cases = sorted({c["task"] for c in A})
    res = {"cases": len(cases), "arms": {}}
    pc = {}
    for arm in ARMS:
        cs = by(A, lane=arm)
        cls = Counter(seeded_class(c) for c in cs)
        valid = [c for c in cs if seeded_class(c) in ("ok", "escaped")]
        k, n = cls["escaped"], len(valid)
        per = {t: (sum(1 for c in valid if c["task"] == t and not c["passed"]), sum(1 for c in valid if c["task"] == t))
               for t in cases}
        pc[arm] = per
        r = rng()
        boot = []
        for _ in range(B):
            sel = [r.choice(cases) for _ in cases]
            kk, nn = sum(per[t][0] for t in sel), sum(per[t][1] for t in sel)
            boot.append(kk / nn if nn else 0.0)
        res["arms"][arm] = dict(
            cells=len(cs), seed_red=cls["seed_red"], infra=cls["infra"],
            infra_outcomes=dict(Counter(c["outcome"] for c in cs if seeded_class(c) == "infra")),
            valid=n, escaped=k, rescued_or_passed=cls["ok"], E=k / n, wilson=wilson(k, n),
            case_boot95=(quant(boot, 0.025), quant(boot, 0.975)),
            cost_mean=mean(c["cost"] for c in cs), cost_sum=sum(c["cost"] for c in cs),
            review_cost_mean=mean(c["review_cost"] for c in cs),
            review_wall_median=median(c["review_wall"] for c in cs if c["outcome"] == "landed"),
            review_requests_mean=mean(c["review_requests"] for c in cs),
            reach_review=(len(cs) - cls["seed_red"]) / len(cs), per_case=per)
    # paired per-case differences against r-now (reps averaged inside case and arm)
    res["pairs"] = {}
    for arm in ("r-low", "r-haiku"):
        diffs = {}
        for t in cases:
            a, b = pc[arm][t], pc["r-now"][t]
            if a[1] and b[1]:
                diffs[t] = a[0] / a[1] - b[0] / b[1]
        ts = list(diffs)
        r = rng()
        boot = [mean(diffs[r.choice(ts)] for _ in ts) for _ in range(B)]
        res["pairs"][arm] = dict(n_cases=len(ts), mean=mean(diffs.values()), nonzero_cases=sum(1 for x in diffs.values() if x),
                                 boot95=(quant(boot, 0.025), quant(boot, 0.975)), upper95=quant(boot, 0.95),
                                 nonzero={t: round(x, 4) for t, x in diffs.items() if x})
    # sensitivity: the cells Haiku lost to a review that could not be filed
    h = ARMS[2]
    cs = by(A, lane=h)
    inval = [c for c in cs if c["outcome"] == "review_invalid"]
    tmo = [c for c in cs if c["outcome"] == "timeout"]
    k, n = res["arms"][h]["escaped"], res["arms"][h]["valid"]
    res["haiku_sensitivity"] = {
        "protocol (all lost cells excluded)": (k, n),
        "review_invalid kept as not escaped": (k, n + len(inval)),
        "review_invalid counted as escaped": (k + len(inval), n + len(inval)),
        "review_invalid and timeouts counted as escaped": (k + len(inval) + len(tmo), n + len(inval) + len(tmo))}
    res["escape_cases"] = {arm: {t: v for t, v in pc[arm].items() if v[0]} for arm in ARMS}
    return res


# ---------------------------------------------------------------- Part B
def part_b(Bc):
    out = {}
    for arm in ARMS:
        cs = by(Bc, lane=arm)
        out[arm] = dict(cells=len(cs), landed=sum(1 for c in cs if c["outcome"] == "landed"),
                        hidden_fail=sum(1 for c in cs if not c["passed"]), builder_requests=sum(c["build_requests"] for c in cs),
                        cost_mean=mean(c["cost"] for c in cs), review_cost_mean=mean(c["review_cost"] for c in cs),
                        review_wall_mean=mean(c["review_wall"] for c in cs), review_wall_median=median(c["review_wall"] for c in cs),
                        review_requests_mean=mean(c["review_requests"] for c in cs), wall_mean=mean(c["wall"] for c in cs))
        out[arm]["upper95_hidden_fail"] = cp_upper(out[arm]["hidden_fail"], len(cs))
    return out


# ---------------------------------------------------------------- Part C
def saving(sel):
    sx, sy = sum(x for x, _ in sel), sum(y for _, y in sel)
    return 1 - sx / sy if sy else float("nan")


def cluster_boot(by_task, stat):
    ts = list(by_task)
    r = rng()
    outs = []
    for _ in range(B):
        sel = [x for t in (r.choice(ts) for _ in ts) for x in by_task[t]]
        outs.append(stat(sel))
    return outs


def part_c(Co, Cr):
    arms = {"r-off": Co, **{a: by(Cr, lane=a) for a in ARMS}}
    out = {}
    for arm, cs in arms.items():
        landed = [c for c in cs if c["outcome"] == "landed"]
        infra = [c for c in cs if c["outcome"] != "landed"]
        out[arm] = dict(cells=len(cs), landed=len(landed), infra=len(infra),
                        infra_outcomes=dict(Counter(c["outcome"] for c in infra)),
                        infra_tasks=dict(Counter(c["task"] for c in infra)),
                        final_fail=sum(1 for c in landed if not c["passed"]),
                        final_fail_cells=[f"{c['task']}/{c['rep']}" for c in landed if not c["passed"]],
                        cost_mean=mean(c["cost"] for c in landed), wall_mean=mean(c["wall"] for c in landed),
                        review_cost_mean=mean(c["review_cost"] for c in landed),
                        review_wall_mean=mean(c["review_wall"] for c in landed),
                        review_requests_mean=mean(c["review_requests"] for c in landed),
                        review_requests_total=sum(c["review_requests"] for c in cs),
                        build_cost_mean=mean(c["cost"] - c["review_cost"] for c in landed),
                        cost_sum=sum(c["cost"] for c in cs))
    # r-off has no review, so its first green tree is its final tree
    o = out["r-off"]
    k, n = o["final_fail"], o["landed"]
    o["first_green_wrong"] = (k, n, cp_upper(k, n), wilson(k, n))
    o["first_green_wrong_if_lost_cells_clean"] = (k, o["cells"], cp_upper(k, o["cells"]))
    # paired whole-pipeline cost against r-now (same host, same task and repetition, both landed)
    now = {(c["task"], c["rep"]): c for c in by(Cr, lane="r-now") if c["outcome"] == "landed"}
    pairs = {}
    for arm in ARMS[1:]:
        oth = {(c["task"], c["rep"]): c for c in by(Cr, lane=arm) if c["outcome"] == "landed"}
        ks = sorted(set(now) & set(oth))
        row = {}
        for metric in ("cost", "review_cost", "wall", "review_wall"):
            bt = defaultdict(list)
            for kk in ks:
                bt[kk[0]].append((oth[kk][metric], now[kk][metric]))
            sel = [x for v in bt.values() for x in v]
            boot = cluster_boot(bt, saving)
            row[metric] = dict(saving=saving(sel), boot95=(quant(boot, 0.025), quant(boot, 0.975)), blocks=len(ks))
        pairs[arm] = row
    out["paired_vs_r_now"] = pairs
    # r-off against r-now: same 14 tasks, different host, per-task means
    tn, to = defaultdict(list), defaultdict(list)
    for c in by(Cr, lane="r-now"):
        if c["outcome"] == "landed":
            tn[c["task"]].append(c["cost"])
    for c in Co:
        if c["outcome"] == "landed":
            to[c["task"]].append(c["cost"])
    tasks = sorted(set(tn) & set(to))
    bt = {t: [(mean(to[t]), mean(tn[t]))] for t in tasks}
    boot = cluster_boot(bt, saving)
    out["off_vs_now"] = dict(tasks=len(tasks), saving=saving([x for v in bt.values() for x in v]),
                             boot95=(quant(boot, 0.025), quant(boot, 0.975)))
    return out


# ---------------------------------------------------------------- confirmation with a different provider
def part_sol(S, A):
    cs = S
    cls = Counter(seeded_class(c) for c in cs)
    valid = [c for c in cs if seeded_class(c) in ("ok", "escaped")]
    k, n = cls["escaped"], len(valid)
    cases = sorted({c["task"] for c in cs})
    per = {t: (sum(1 for c in valid if c["task"] == t and not c["passed"]), sum(1 for c in valid if c["task"] == t)) for t in cases}
    return dict(cells=len(cs), seed_red=cls["seed_red"], infra=cls["infra"], valid=n, escaped=k, upper95=cp_upper(k, n),
                wilson=wilson(k, n), cost_mean=mean(c["cost"] for c in cs), cost_sum=sum(c["cost"] for c in cs),
                review_cost_mean=mean(c["review_cost"] for c in cs), review_requests_mean=mean(c["review_requests"] for c in cs),
                review_wall_median=median(c["review_wall"] for c in cs), wall_median=median(c["wall"] for c in cs),
                per_case=per)


# ---------------------------------------------------------------- tasks
def task_table():
    rows = {}
    for part in ("A", "B", "Coff"):
        plan = json.load(open(os.path.join(ROUNDS, ROUND[part], "PLAN.json")))
        for t, h in plan["hashes"]["tasks"].items():
            rows.setdefault(t, {"task": h["task"], "tree": h["tree"], "hidden_tests": h["hidden_tests"]})
    return rows


# ---------------------------------------------------------------- printing
def ci(t):
    return f"{pct(t[0])} to {pct(t[1])}"


def run():
    cells = {p: load(p) for p in ROUND}
    A, Bc, Co, Cr, S = (cells[p] for p in ("A", "B", "Coff", "Crev", "Sol"))
    ra, rb, rc, rs = part_a(A), part_b(Bc), part_c(Co, Cr), part_sol(S, A)
    res = dict(A=ra, B=rb, C=rc, Sol=rs, cells={p: len(v) for p, v in cells.items()})

    say("# review-value-2: recomputed from the published records")
    say()
    say("## Cells per round")
    for p, v in cells.items():
        say(f"- {ROUND[p]}: {len(v)} cells, list-price cost ${sum(c['cost'] for c in v):.2f}")
    say(f"- total {sum(len(v) for v in cells.values())} cells, ${sum(c['cost'] for v in cells.values() for c in v):.2f}")

    say()
    say(f"## Seeded defects, Claude models ({ra['cases']} cases x 3 reviewer settings x 3 repetitions)")
    say("| reviewer | cells | acceptance caught the planted tree | build stopped | valid | escaped | escape rate | Wilson 95% | case bootstrap 95% |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |")
    for arm in ARMS:
        a = ra["arms"][arm]
        say(f"| {arm} | {a['cells']} | {a['seed_red']} | {a['infra']} {a['infra_outcomes']} | {a['valid']} | {a['escaped']} | "
            f"{pct(a['E'])} | {ci(a['wilson'])} | {ci(a['case_boot95'])} |")
    say()
    say("Paired per-case difference against r-now (percentage points, reps averaged inside case):")
    for arm, p in ra["pairs"].items():
        say(f"- {arm}: mean {100 * p['mean']:+.1f}, bootstrap 95% {100 * p['boot95'][0]:+.1f} to {100 * p['boot95'][1]:+.1f}, "
            f"one-sided upper 95% {100 * p['upper95']:+.1f}, {p['nonzero_cases']} of {p['n_cases']} cases differ")
    say()
    say("r-haiku sensitivity to the cells it lost:")
    for lab, (k, n) in ra["haiku_sensitivity"].items():
        say(f"- {lab}: {k} of {n} = {pct(k / n)}")
    say()
    say("Cases with at least one escape (escaped / valid cells):")
    for arm in ARMS:
        say(f"- {arm}: " + ", ".join(f"{t} {v[0]}/{v[1]}" for t, v in ra["escape_cases"][arm].items()))
    say(f"- {len([1 for t, v in rs['per_case'].items() if v[0]])} cases escaped with the OpenAI reviewer")
    say()
    say("Review stage per seeded cell:")
    say("| reviewer | cell cost | review cost | review requests | review wall, median |")
    say("| --- | ---: | ---: | ---: | ---: |")
    for arm in ARMS:
        a = ra["arms"][arm]
        say(f"| {arm} | ${a['cost_mean']:.4f} | ${a['review_cost_mean']:.4f} | {a['review_requests_mean']:.1f} | {a['review_wall_median']:.1f} s |")

    say()
    say("## Per-case table (escaped / valid cells)")
    say("| case | r-now | r-low | r-haiku | OpenAI reviewer |")
    say("| --- | --- | --- | --- | --- |")
    for t in sorted(rs["per_case"]):
        say(f"| {t} | " + " | ".join(f"{ra['arms'][a]['per_case'][t][0]}/{ra['arms'][a]['per_case'][t][1]}" for a in ARMS)
            + f" | {rs['per_case'][t][0]}/{rs['per_case'][t][1]} |")

    say()
    say("## Clean controls (15 tasks x 3 reviewer settings x 2 repetitions)")
    say("| reviewer | cells | landed | hidden tests failed | builder requests | cell cost | review cost | review requests | review wall, mean |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for arm in ARMS:
        b = rb[arm]
        say(f"| {arm} | {b['cells']} | {b['landed']} | {b['hidden_fail']} | {b['builder_requests']} | ${b['cost_mean']:.4f} | "
            f"${b['review_cost_mean']:.4f} | {b['review_requests_mean']:.1f} | {b['review_wall_mean']:.1f} s |")

    say()
    say("## Natural builds, Sonnet 5.5 medium builder (14 tasks)")
    say("| setting | cells | landed | build stopped | final tree fails hidden tests | cost per landed cell | review cost | review wall | wall per landed cell |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for arm in ["r-off"] + ARMS:
        c = rc[arm]
        say(f"| {arm} | {c['cells']} | {c['landed']} | {c['infra']} {c['infra_outcomes']} {c['infra_tasks']} | {c['final_fail']} "
            f"{c['final_fail_cells']} | ${c['cost_mean']:.4f} | ${c['review_cost_mean']:.4f} | {c['review_wall_mean']:.1f} s | {c['wall_mean']:.1f} s |")
    k, n, up, wl = rc["r-off"]["first_green_wrong"]
    say()
    say(f"r-off first green wrong: {k} of {n} landed cells = {pct(k / n)}; exact one-sided 95% upper bound {pct(up)}; Wilson 95% {ci(wl)}")
    k, n, up = rc["r-off"]["first_green_wrong_if_lost_cells_clean"]
    say(f"  with the {rc['r-off']['infra']} lost cells counted as correct: {k} of {n}, upper bound {pct(up)}")
    for arm, row in rc["paired_vs_r_now"].items():
        say(f"- {arm} against r-now, {row['cost']['blocks']} matched (task, repetition) blocks: whole-cell cost saving "
            f"{pct(row['cost']['saving'])} ({ci(row['cost']['boot95'])}); review stage cost saving {pct(row['review_cost']['saving'])} "
            f"({ci(row['review_cost']['boot95'])}); wall saving {pct(row['wall']['saving'])} ({ci(row['wall']['boot95'])})")
    o = rc["off_vs_now"]
    say(f"- r-off against r-now, per-task means over {o['tasks']} tasks (different hosts): cost saving {pct(o['saving'])} ({ci(o['boot95'])})")
    d = rc["r-now"]["cost_mean"] - rc["r-off"]["cost_mean"]
    say(f"- review cost per build, r-now minus r-off whole-cell mean: ${d:.4f}; review stage cost in r-now cells: ${rc['r-now']['review_cost_mean']:.4f}; "
        f"review wall per build in r-now cells: {rc['r-now']['review_wall_mean']:.1f} s ({pct(rc['r-now']['review_wall_mean'] / rc['r-now']['wall_mean'])} of the cell)")
    say()
    say("Price of a review that is switched on (break-even), with the escape rate of r-now from the seeded cases:")
    E = ra["arms"]["r-now"]["E"]
    say("| builds wrong on green (p) | escapes prevented per 1000 builds | review cost per 1000 builds | review wall per 1000 builds | cost per prevented escape |")
    say("| ---: | ---: | ---: | ---: | ---: |")
    res["breakeven"] = []
    for p in (0.001, 0.01, 0.02):
        prev = 1000 * p * (1 - E)
        say(f"| {pct(p)} | {prev:.2f} | ${1000 * d:.1f} | {1000 * rc['r-now']['review_wall_mean'] / 3600:.1f} h | ${d / (p * (1 - E)):.2f} |")
        res["breakeven"].append(dict(p=p, prevented=prev, cost=1000 * d, vstar=d / (p * (1 - E))))

    say()
    say("## Confirmation with a different provider (seeded cases, OpenAI reviewer)")
    say(f"- cells {rs['cells']}, acceptance caught the planted tree {rs['seed_red']}, build stopped {rs['infra']}, valid {rs['valid']}, "
        f"escaped {rs['escaped']} ({pct(rs['escaped'] / rs['valid'])}), exact one-sided 95% upper bound {pct(rs['upper95'])}")
    say(f"- cost ${rs['cost_sum']:.2f} in total, ${rs['cost_mean']:.4f} per cell (review stage ${rs['review_cost_mean']:.4f}), "
        f"{rs['review_requests_mean']:.1f} review requests per cell, median cell wall {rs['wall_median']:.0f} s")
    say(f"- Claude r-now on the same cases: {ra['arms']['r-now']['escaped']} of {ra['arms']['r-now']['valid']} escaped "
        f"({pct(ra['arms']['r-now']['E'])}), ${ra['arms']['r-now']['cost_mean']:.4f} per cell")

    say()
    say("## Tasks (ids and content hashes only; the tasks are still in use)")
    tt = task_table()
    res["tasks"] = tt
    say(f"{len(tt)} task ids in the three Claude rounds; the hashes are in each round's PLAN.json.")
    return res


def write_tasks(tt):
    def kind(t):
        return "seeded defect" if t.startswith("seed-") else "clean control" if t.endswith("-c") else "natural build"
    lines = ["# Tasks of review-value-2 (ids and content hashes only)", "",
             "These tasks are still used by running experiments, so their text, Intents, hidden tests, test names and trees are not published. "
             "Each row gives the task id, how this study used it, and sha256 content hashes recorded in the round's `PLAN.json` before the run. "
             "The tasks will be published once the experiments using them finish; the hashes then show they are unchanged. "
             "Kinds: a seeded defect is a correct solution with one planted change; a clean control is the correct solution; "
             "a natural build is an ordinary Kogen build of the task. Seeded ids are opaque (seed-01 to seed-26, numbered in the sorted order of the original ids); "
             "the mapping will be published with the tasks, and the hashes are those of the real task folders.", "",
             "| Task id | Used as | Task hash | Hidden-test hash | Start-tree hash |", "| --- | --- | --- | --- | --- |"]
    for t in sorted(tt):
        lines.append(f"| `{t}` | {kind(t)} | `{tt[t]['task']}` | `{tt[t]['hidden_tests']}` | `{tt[t]['tree']}` |")
    counts = Counter(kind(t) for t in tt)
    lines += ["", f"{len(tt)} tasks: " + ", ".join(f"{n} {k}" for k, n in sorted(counts.items())) + "."]
    with open(os.path.join(HERE, "TASKS.md"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    results = run()
    if "--write" in sys.argv:
        write_tasks(results["tasks"])
        with open(os.path.join(HERE, "results.json"), "w") as f:
            json.dump(results, f, indent=1, sort_keys=True)
            f.write("\n")
        with open(os.path.join(HERE, "results.txt"), "w") as f:
            f.write("\n".join(OUT) + "\n")
