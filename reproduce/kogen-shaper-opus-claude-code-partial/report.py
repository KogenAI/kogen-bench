#!/usr/bin/env python3
"""report.py <pairs.tsv> <g1_time.tsv>: paired hidden pass, three outcomes, refusal causes, censored and one-arm lists, g1 time split, for the Kogen shaper-on-Opus-via-Claude-Code partial result (standard library only)."""
import csv, sys, collections, math, statistics
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
trows = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
def sign(w, l):
    m = w + l
    return 1.0 if m == 0 else min(1.0, 2 * sum(math.comb(m, i) for i in range(min(w, l) + 1)) / 2 ** m)
I = lambda v: int(v) if v in ("0", "1") else 0
def block(title, pp):
    n = len(pp)
    w = sum(r["change"] == "win" for r in pp); l = sum(r["change"] == "loss" for r in pp)
    S = lambda k: sum(I(r[k]) for r in pp)
    print(f"{title}: {n} pairs; hidden pass g0 {S('g0_hidden')} g1 {S('g1_hidden')}; g1 wins {w} losses {l} net {w-l} exact two-sided sign p {sign(w,l):.2f}; "
          f"valid Intent g0 {S('g0_intent_valid')} g1 {S('g1_intent_valid')}; acceptance separating g0 {S('g0_acc_sep')} g1 {S('g1_acc_sep')}")
    cl = collections.Counter((r["class"], r["change"]) for r in pp if r["change"])
    print("   discordant by class (a shape stage, b build, c review, d infrastructure, e unclear):", {f"{c}-{ch}": v for (c, ch), v in sorted(cl.items())})
for c in ("studio", "linux"):
    R = [r for r in rows if r["cohort"] == c]
    print(f"\n== cohort {c}: planned {len(R)} pairs;", dict(sorted(collections.Counter(r["status"] for r in R).items())))
    pp = [r for r in R if r["status"] == "paired"]
    block("all paired", pp)
    clean = [r for r in pp if r["acc120"] == "0" and r["hiload"] == "0"]
    conf = [r for r in pp if not (r["acc120"] == "0" and r["hiload"] == "0")]
    if c == "studio":
        block("paired, load1 mean < 40 and no acceptance-120 s outcome in either cell", clean)
        block("paired, infra-confounded (a cell at load1 >= 40 or set by the 120 s limit)", conf)
        block("paired, no cell outcome set by the 120 s acceptance limit", [r for r in pp if r["acc120"] == "0"])
    else:
        print("   cells with an acceptance 120 s outcome in this cohort:", sum(r["acc120"] == "1" for r in pp))
    print("   refusal / non-landing causes per arm (all started cells with a result, excluding censored):")
    for a in ("g0", "g1"):
        cs = collections.Counter(r[a + "_cause"] for r in R if r["status"] != "censored (seat limit)" and r[a + "_outcome"] not in ("", "no result"))
        print("     ", a, dict(sorted(cs.items(), key=lambda x: -x[1])))
    for a in ("g0", "g1"):
        cc = [r for r in R if r["status"] != "censored (seat limit)" and r[a + "_outcome"] not in ("", "no result")]
        print(f"      {a}: cells {len(cc)}, valid Intent {sum(I(r[a+'_intent_valid']) for r in cc)}, acceptance separating {sum(I(r[a+'_acc_sep']) for r in cc)}, hidden pass {sum(I(r[a+'_hidden']) for r in cc)}")
    print("   censored pairs (both arms excluded):", [(r["run"], r["task"]) for r in R if r["status"] == "censored (seat limit)"])
    for s in ("g0 only", "g1 only", "unfinished (started, no result)"):
        print(f"   {s}:", len([r for r in R if r["status"] == s]), "pairs;", [(r["run"].split('-', 2)[2], r["task"]) for r in R if r["status"] == s])
    print("   not started:", sum(r["status"] == "not started" for r in R), "pairs")
    print("   per task (paired): task, valid Intent g0/g1, acceptance separating g0/g1, hidden g0/g1, wins, losses, pairs")
    for t in sorted({r["task"] for r in pp}):
        rs = [r for r in pp if r["task"] == t]; s = lambda k: sum(I(r[k]) for r in rs)
        print(f"     {t}\t{s('g0_intent_valid')}/{s('g1_intent_valid')}\t{s('g0_acc_sep')}/{s('g1_acc_sep')}\t{s('g0_hidden')}/{s('g1_hidden')}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}\t{len(rs)}")
    print("   discordant pairs: run, task, g0 hidden, g1 hidden, change, class")
    for r in pp:
        if r["change"]: print(f"     {r['run']}\t{r['task']}\t{r['g0_hidden']}\t{r['g1_hidden']}\t{r['change']}\t{r['class']}")
    T = [r for r in trows if r["cohort"] == c]
    print("   g1 time per cell (seconds, from Claude Code transcripts; model time sums request gaps and can exceed shape wall when the example-check session ran in parallel):")
    def tb(name, rs):
        if not rs: print("     ", name, "0 cells"); return
        f = lambda k: [float(r[k]) for r in rs if r[k] not in ("", None)]
        m = lambda k: f"{statistics.median(f(k)):.0f}" if f(k) else "-"
        print(f"      {name}: {len(rs)} cells; median wall {m('wall_s')}, shape wall {m('shape_wall_s')}, model {m('shape_model_s')}, commands {m('shape_cmd_s')} (longest single command median {m('cc_longest_tool_s')}), Kogen-side {m('shape_other_s')}, readiness acceptance runs {m('shape_readiness_s')}")
    if c == "studio":
        for nm, fn in (("load1 < 40", lambda r: float(r["load1_mean"] or 0) < 40), ("load1 >= 40", lambda r: float(r["load1_mean"] or 0) >= 40)):
            tb(nm + ", landed", [r for r in T if fn(r) and r["outcome"] == "landed"])
            tb(nm + ", timeout", [r for r in T if fn(r) and r["outcome"] == "timeout"])
            tb(nm + ", other", [r for r in T if fn(r) and r["outcome"] not in ("landed", "timeout")])
    else:
        tb("landed", [r for r in T if r["outcome"] == "landed"]); tb("other", [r for r in T if r["outcome"] != "landed"])
    print("   descriptive only (different model and executor between arms; no speed or cost-efficiency claim):")
    for a in ("g0", "g1"):
        ws = [float(r[a + "_wall_s"]) for r in R if r["status"] != "censored (seat limit)" and r[a + "_wall_s"] not in ("",)]
        print(f"      {a} cell wall: n {len(ws)}, median {statistics.median(ws):.0f} s, max {max(ws):.0f} s")
    cs = [float(r["cc_api_equiv_usd"]) for r in T if r["cc_api_equiv_usd"] not in ("", "0.0", "0")]
    if cs: print(f"      g1 shape stage, Claude Code API-equivalent estimate (seat, not billed): {len(cs)} cells, median {statistics.median(cs):.2f} USD, total {sum(cs):.1f} USD")
