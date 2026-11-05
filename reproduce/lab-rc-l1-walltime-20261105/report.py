#!/usr/bin/env python3
"""report.py <out> [<out>...] : per-run rows + summary for the wall-time Lab (rc-l1).
Each <out> holds chunks.tsv (cond, round, arm, start, load5, load1, rc) and <cond>-r<round>-<arm>.json from `go test -json`.
Writes rows.tsv (one line per test run) and summary.md next to the first <out>'s parent when --write DIR is given."""
import json, re, sys, os, statistics as S, math

def bucket(l5):
    return "<3" if l5 < 3 else ("3-12" if l5 <= 12 else ">12")

def parse(path):
    runs, cur = [], None
    for line in open(path):
        try:
            e = json.loads(line)
        except Exception:
            continue
        t = e.get("Test")
        if not t:
            continue
        a = e.get("Action")
        if a == "run":
            cur = {"out": [], "res": None, "elapsed": None}
        elif a == "output" and cur is not None:
            cur["out"].append(e.get("Output", ""))
        elif a in ("pass", "fail") and cur is not None:
            cur["res"] = a
            cur["elapsed"] = e.get("Elapsed")
            runs.append(cur)
            cur = None
    return runs

def classify(run):
    txt = "".join(run["out"])
    m = re.search(r"elapsed (-?\d+)", txt)
    if m:
        return "elapsed", int(m.group(1))
    if "results: []" in txt:
        return "never-started", None
    if "unstarted command logged" in txt:
        return "setup-2-logged", None
    m = re.search(r"wall_time_test.go:\d+: (.{0,80})", txt)
    return "other:" + (m.group(1) if m else txt.strip()[:80].replace("\n", " ")), None

def wilson(k, n):
    if n == 0:
        return (0, 0)
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    wr = None
    if "--write" in sys.argv:
        wr = sys.argv[sys.argv.index("--write") + 1]
        args = [a for a in args if a != wr]
    rows = []
    for out in args:
        label = os.path.basename(out.rstrip("/")).replace("out-", "")
        for ln in open(os.path.join(out, "chunks.tsv")):
            cond, r, arm, t0, l5, l1, rc = ln.rstrip("\n").split("\t")
            f = os.path.join(out, f"{cond}-r{r}-{arm}.json")
            runs = parse(f) if os.path.exists(f) else []
            if not runs:
                rows.append(dict(cond=cond, arm=arm, round=r, idx=0, t0=t0, load5=float(l5), load1=float(l1), res="nochunk", kind="no-runs rc=" + rc, ms="", secs=""))
            for i, run in enumerate(runs, 1):
                kind, ms = ("", None) if run["res"] == "pass" else classify(run)
                rows.append(dict(cond=cond, arm=arm, round=r, idx=i, t0=t0, load5=float(l5), load1=float(l1), res=run["res"], kind=kind, ms="" if ms is None else ms, secs=run["elapsed"]))
    hdr = ["cond", "arm", "round", "idx", "chunk_start", "load5", "load1", "result", "failure_kind", "setup1_ms", "test_secs"]
    lines = ["\t".join(hdr)] + ["\t".join(str(x) for x in (r["cond"], r["arm"], r["round"], r["idx"], r["t0"], r["load5"], r["load1"], r["res"], r["kind"], r["ms"], r["secs"])) for r in rows]
    sm = ["| condition | load5 bucket | arm | runs | fails | fail rate (95% CI) | failure kinds | failing setup-1 ms (min/median/max) |", "|---|---|---|---|---|---|---|---|"]
    conds = sorted({r["cond"] for r in rows})
    for c in conds:
        for b in ["<3", "3-12", ">12", "all"]:
            for arm in "AB":
                rs = [r for r in rows if r["cond"] == c and r["arm"] == arm and (b == "all" or bucket(r["load5"]) == b)]
                if not rs:
                    continue
                n = len(rs)
                fl = [r for r in rs if r["res"] != "pass"]
                k = len(fl)
                lo, hi = wilson(k, n)
                kinds = {}
                for r in fl:
                    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
                ms = sorted(r["ms"] for r in fl if r["ms"] != "")
                dist = f"{ms[0]}/{S.median(ms):g}/{ms[-1]}" if ms else "-"
                sm.append(f"| {c} | {b} | {arm} | {n} | {k} | {100*k/n:.1f}% ({100*lo:.1f}-{100*hi:.1f}) | {', '.join(f'{a} x{v}' for a, v in sorted(kinds.items())) or '-'} | {dist} |")
    ch = ["", "Chunk starts (load5 per chunk): " + ", ".join(f"{r['cond']}{r['round']}{r['arm']}={r['load5']}" for r in {(x['cond'], x['round'], x['arm']): x for x in rows}.values())]
    summary = "\n".join(sm + ch) + "\n"
    if wr:
        open(os.path.join(wr, "rows.tsv"), "w").write("\n".join(lines) + "\n")
        open(os.path.join(wr, "summary.md"), "w").write(summary)
    print(summary)

main()
