#!/usr/bin/env python3
"""Compose RESULTS.md (and replay data) from sample.json + eu-runs/ . python3 -I gen_results.py"""
import json, os, re, statistics, glob
D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(D + "/sample.json"))
R = D + "/eu-runs/runs/"
EXPECT = {  # what broke, from the adoption step outputs (ADOPTION-FAILURES) -- not used to decide anything
    "8852812": "go: consumes/kogen-build TestRecover* (4 windows)", "10f190b": "acceptance: stop scenarios / no_progress (not a go test)",
    "91d0a32": "go: consumes/kogen-shaping TestPreflight... 'title names the Git user'", "f04edce": "go vet: undefined shape.ShapeBatchTool",
    "aeeb5be": "go: consumes/kogen-setup TestInitUses...", "f4b7f54": "go (05T070119Z step): review-side break",
    "1e795ed": "acceptance suite (decision check); go test passed", "bc5b726": "go: consumes/kogen-coordinator TestShapeWorkers..."}


def load(p):
    try: return json.load(open(p))
    except Exception: return None


def stage(r):
    if r is None: return "not run"
    d = r["detail"]
    if r["status"] == "green": return "green"
    if d.startswith("PIN") or d.startswith("clone"): return "pin"
    if d.startswith("gofmt"): return "gofmt"
    if d.startswith("go build"): return "build"
    if d.startswith("go vet"): return "vet"
    if d.startswith("go test"): return "test"
    return r["status"]


def base_fact(main12, tid):
    """pass/fail/None for one test id on the unpinned kogen main, from a full base run or targeted base-test runs"""
    f = load(f"{R}base-{main12}/result.json")
    if f and f.get("failed_ids") is not None and f["mode"] == "base" and stage(f) in ("test", "green"):
        return "fail" if tid in f["failed_ids"] else "pass"
    for g in glob.glob(f"{R}basetests-{main12}-*/result.json"):
        t = (load(g) or {}).get("tested", {})
        if tid in t: return t[tid]
    return None


HARDPIN = "kogen.TestAssemblyUsesThePinnedComponents"
def classify(prefix, i, L):
    r = load(f"{R}{prefix}-{i}/result.json"); m12 = L["kogen_main"][:12]
    bv = load(f"{R}basevet-{m12}/result.json") or load(f"{R}base-{m12}/result.json")
    row = dict(n=i, role=L["role"], repo=L["repo"], sha7=L["sha7"], kogen=L["kogen_main"][:8], log=L["log"], A=L["consumer_check"].replace("consumer check", "cc"),
               r=r, stage=stage(r), new=[], old=[], unknown=[], hardpin=False, why="")
    if r is None: row.update(verdict="not run", adj="not run")
    elif r["status"] == "green": row.update(verdict="pass", adj="pass")
    else:
        st = row["stage"]
        if st == "test":
            for tid in r["failed_ids"]:
                f = base_fact(m12, tid)
                (row["old"] if f == "fail" else row["unknown"] if f is None else row["new"]).append(tid)
            txt = open(f"{R}{prefix}-{i}/go-test.out", errors="replace").read() if os.path.exists(f"{R}{prefix}-{i}/go-test.out") else ""
            row["hardpin"] = HARDPIN in row["new"] and bool(re.search(r"assembly_test\.go:\d+: .*want v0\.0\.0-\d+-[0-9a-f]+ unreplaced", txt))
            adjnew = [t for t in row["new"] if not (t == HARDPIN and row["hardpin"])]
            row["verdict"] = "REFUSE" if row["new"] else ("unknown (no base fact)" if row["unknown"] else "pre-existing only")
            row["adj"] = "REFUSE" if adjnew else ("unknown (no base fact)" if row["unknown"] else "pass")
            row["why"] = r["detail"]
        else:
            same = bv is not None and bv["status"] == "red" and stage(bv) == st and bv["detail"][:60] == r["detail"][:60]
            row["new"] = [] if same else [r["detail"][:160]]
            row["verdict"] = "pre-existing" if same else ("REFUSE" if bv is not None else "REFUSE (no base run)")
            row["adj"] = row["verdict"]; row["why"] = r["detail"]
    # cause class of a refusal: hardpin (obsolete test), skew (kogen main still vendors the bare kogen-loop while the pinned
    # component requires github.com/KogenAI/kogen-loop: mixed module paths), behaviour (anything else)
    if row["r"] is not None and row["verdict"].startswith("REFUSE"):
        txt = ""
        for fn in ("build.out", "vet.out", "tidy.out", "goget.out", "sync.out"):
            q = f"{R}{prefix}-{i}/{fn}"
            if os.path.exists(q): txt += open(q, errors="replace").read()
        skew = row["stage"] in ("build", "vet", "pin") and re.search(r'"kogen-loop/[a-z]+"[^\n]*"github\.com/KogenAI/kogen-loop/|"github\.com/KogenAI/kogen-loop/[a-z]+"[^\n]*"kogen-loop/|kogen-loop', txt) is not None
        nonhard = [t for t in row["new"] if not (t == HARDPIN and row["hardpin"])]
        row["cause"] = "skew" if skew else ("behaviour" if nonhard else "hardpin")
        if row["stage"] == "test" and nonhard: row["cause"] = "behaviour"
    else: row["cause"] = ""
    d = ""
    if row["cause"] == "hardpin": d = "obsolete test: hard-coded component versions in assembly_test.go"
    elif row["cause"] == "skew": d = "loop-module path mix: kogen main vendors the bare kogen-loop, the pinned component needs github.com/KogenAI/kogen-loop"
    elif row["cause"] == "behaviour":
        if row["stage"] in ("build", "vet", "pin"): d = "API coupling: an unmoved component fails to build/vet against the pinned one"
        elif row["new"] and all(re.search(r"Deadline|Timeout|Hung|Timing", t) for t in row["new"]): d = "timing test that reports host load (not re-run on the pin)"
        else: d = "kogen test fails on the pin only"
    row["cause_detail"] = d
    return row


rows = [classify("pin", i, L) for i, L in enumerate(S["sample"], 1)]
def pick_tuple(i, L):
    cands = [(v, classify(v, i, L)) for v in ("tuple", "tupleNL") if os.path.exists(f"{R}{v}-{i}/result.json")]
    if not cands: return None
    good = [c for c in cands if c[1]["stage"] in ("test", "green", "vet", "gofmt")]
    v, row = (good or cands)[0]; row["variant"] = "with loop" if v == "tuple" else "without loop"
    return row


trows = [x for x in (pick_tuple(i, L) for i, L in enumerate(S["sample"], 1)) if x]
ploop = [classify("pinloop", i, L) for i, L in enumerate(S["sample"], 1) if os.path.exists(f"{R}pinloop-{i}/result.json")]

done = [x for x in rows if x["r"] is not None]
br = [x for x in rows if x["role"] == "breaker"]; gd = [x for x in rows if x["role"] == "good"]
ref = lambda x, k: x[k].startswith("REFUSE")
caught = [x for x in br if ref(x, "verdict")]; caught_adj = [x for x in br if ref(x, "adj")]
fr = [x for x in gd if ref(x, "verdict")]; fr_adj = [x for x in gd if ref(x, "adj")]
ran_b = [x for x in br if x["r"] is not None]; ran_g = [x for x in gd if x["r"] is not None]


def mins(x, wait):
    t = x["r"]["times_s"]; w = x["r"]["wall_s"]
    return (w if wait else w - t.get("lockwait", 0)) / 60


add = [mins(x, False) for x in done if x["r"]["status"] in ("green", "red")]
addw = [mins(x, True) for x in done if x["r"]["status"] in ("green", "red")]
med = statistics.median(add) if add else None; medw = statistics.median(addw) if addw else None


beh = lambda x: x["cause"] == "behaviour"
caught_beh = [x for x in br if beh(x)]; fr_beh = [x for x in gd if beh(x)]


def decide(c, f, nb, ng, tag):
    if nb < 8 and c < 6 and (8 - nb) + c < 6: return "FAIL (%s: recall %d/8 cannot reach 6)" % (tag, c)
    if f > 2: return "FAIL (%s: %d false refusals of %d good run > 2)" % (tag, f, ng)
    if nb < 8: return "incomplete (%s: %d/8 breakers run, recall so far %d)" % (tag, nb, c)
    if c < 6: return "FAIL (%s: recall %d/8 < 6)" % (tag, c)
    if ng < 40: return "unresolved (%s: recall %d/8 ok, %d false refusals in %d of 40 good run)" % (tag, c, f, ng)
    return "PASS (%s: recall %d/8, false refusals %d/40)" % (tag, c, f)


verdict = decide(len(caught), len(fr), len(ran_b), len(ran_g), "strict, as registered")
verdict_beh = decide(len(caught_beh), len(fr_beh), len(ran_b), len(ran_g), "behaviour only: hard-coded-pin test and bare-loop skew ignored")
verdict_adj = decide(len(caught_adj), len(fr_adj), len(ran_b), len(ran_g), "adjusted: hard-coded-pin test ignored")
out = []
out += ["# Lab lab-prelanding-kogen-check-20261105: results (generated by gen_results.py)", "",
        "Verdict, strict (the registered rule, every new failing test refuses): **%s**" % verdict, "",
        "Verdict, adjusted (post hoc, labelled: the one test that hard-codes the expected pins in kogen before 896ae0c is not counted): **%s**" % verdict_adj, "",
        "Verdict, behaviour only (post hoc: hard-coded-pin test and loop-module skew refusals are not counted as catches or refusals): **%s**" % verdict_beh, "",
        "- Recall on the 8 breakers: strict **%d of %d run**; adjusted **%d of %d run** (A, the gate as it decided: 0 of 8 refused, all landed GREEN)" % (len(caught), len(ran_b), len(caught_adj), len(ran_b)),
        "- False refusals among the known-good: strict **%d of %d run**; adjusted **%d of %d run** (A: 0 of 40, all landed GREEN)" % (len(fr), len(ran_g), len(fr_adj), len(ran_g)),
        "- Minutes added to a landing (median of %d runs, pin+gofmt+build+vet+test, Go-lock wait excluded): **%s**; including lock wait: %s" %
        (len(add), ("%.1f" % med) if med is not None else "n/a", ("%.1f" % medw) if medw is not None else "n/a"), ""]
out += ["## Per commit (B)", "",
        "strict = every new failing test refuses; adjusted = TestAssemblyUsesThePinnedComponents is ignored when its failure is only the hard-coded `want` map (assembly_test.go) not matching the moved pin. 'new' = fails on the pin and passes on the unpinned kogen main of that landing time; 'old' = fails there too.", "",
        "| n | role | commit | kogen main | A: gate as decided (land log) | B stage | strict | adjusted | cause | new failing tests | old (also red on base) | min | what broke (report) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
short = lambda ids: "; ".join(i.replace("kogen/consumes/", "consumes/") for i in ids)
for x in rows:
    m = ("%.1f" % mins(x, False)) if x["r"] else ""
    out.append("| %d | %s | %s@%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (x["n"], x["role"], x["repo"], x["sha7"], x["kogen"], x["A"][:60], x["stage"], x["verdict"], x["adj"], x["cause"],
               (short(x["new"]) if x["new"] else "")[:230].replace("|", "/"), short(x["old"] + x["unknown"])[:80], m, EXPECT.get(x["sha7"], "") if x["role"] == "breaker" else ""))
out += ["", "## False refusals, strict (known-good refused by B)", ""]
out += ["- n=%d %s@%s (kogen %s): stage %s; new: %s" % (x["n"], x["repo"], x["sha7"], x["kogen"], x["stage"], short(x["new"])[:300]) for x in fr] or ["- none so far"]
out += ["", "## False refusals, adjusted", ""]
out += ["- n=%d %s@%s (kogen %s): stage %s; new: %s" % (x["n"], x["repo"], x["sha7"], x["kogen"], x["stage"], short([t for t in x["new"] if t != HARDPIN or not x["hardpin"]])[:300]) for x in fr_adj] or ["- none so far"]
out += ["", "## Breakers B did not refuse (adjusted)", ""]
out += ["- n=%d %s@%s: adjusted %s (stage %s). %s" % (x["n"], x["repo"], x["sha7"], x["adj"], x["stage"], EXPECT.get(x["sha7"], "")) for x in ran_b if x not in caught_adj] or ["- none so far"]

tb = [x for x in trows if x["role"] == "breaker"]; tg = [x for x in trows if x["role"] == "good"]
out += ["", "## Diagnostic arm B-tuple (post hoc, not the registered arm B)", "",
        "The adoption windows pinned a tuple of components at once, not one commit. B-tuple pins, on the same landing-time kogen main, the landed commit plus the main head of every other component kogen requires at that time (loop first, as `pins()` does). Same steps and same new-vs-base rule. A good commit whose tuple holds a sample breaker is flagged: its refusal belongs to that breaker.", "",
        "- Breakers refused (strict / adjusted / behaviour): %d / %d / %d of %d run" % (sum(ref(x, "verdict") for x in tb), sum(ref(x, "adj") for x in tb), sum(beh(x) for x in tb), len(tb)),
        "- Good refused (strict / adjusted / behaviour): %d / %d / %d of %d run" % (sum(ref(x, "verdict") for x in tg), sum(ref(x, "adj") for x in tg), sum(beh(x) for x in tg), len(tg)), "",
        "| n | role | commit | kogen main | tuple | stage | strict | adjusted | cause | new failing tests / first error | old | min |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for x in trows:
    out.append("| %d | %s | %s@%s | %s | %s | %s | %s | %s | %s | %s | %s | %.1f |" % (x["n"], x["role"], x["repo"], x["sha7"], x["kogen"], x["variant"], x["stage"], x["verdict"], x["adj"], x["cause"],
               (short(x["new"]) if x["new"] else x["why"][:160] if x["verdict"] != "pass" else "")[:260].replace("|", "/"), short(x["old"] + x["unknown"])[:60], mins(x, False)))
out += ["", "## Diagnostic: loop-aligned single pin (negative)", "",
        "Pinning only the vendored loop to the version the pinned component requires does not build: the other components in kogen main still import the bare `kogen-loop`, so `go mod tidy` fails. Rows: " + (", ".join("n=%d %s" % (x["n"], x["why"][:140].replace("|", "/")) for x in ploop) or "none run"), ""]
open(D + "/RESULTS.generated.md", "w").write("\n".join(out) + "\n")
json.dump(dict(verdict=verdict, verdict_adjusted=verdict_adj, verdict_behaviour=verdict_beh, caught_behaviour=len(caught_beh), false_refusals_behaviour=len(fr_beh), tuple_rows=[dict(n=x["n"], role=x["role"], sha7=x["sha7"], stage=x["stage"], verdict=x["verdict"], adjusted=x["adj"], cause=x["cause"], new=x["new"], old=x["old"], wall_s=(x["r"] or {}).get("wall_s")) for x in trows], caught=len(caught), caught_adjusted=len(caught_adj), breakers_run=len(ran_b), false_refusals=len(fr),
               false_refusals_adjusted=len(fr_adj), good_run=len(ran_g), median_min=med, median_min_with_wait=medw,
               rows=[dict(n=x["n"], role=x["role"], repo=x["repo"], sha7=x["sha7"], kogen=x["kogen"], verdict=x["verdict"], adjusted=x["adj"], cause=x["cause"], cause_detail=x["cause_detail"], stage=x["stage"], new=x["new"], old=x["old"],
                          unknown=x["unknown"], hardpin=x["hardpin"], wall_s=(x["r"] or {}).get("wall_s"), times=(x["r"] or {}).get("times_s")) for x in rows]),
          open(D + "/summary.json", "w"), indent=1)
print(verdict); print(verdict_adj); print(verdict_beh); print(len(done), "runs collected")
