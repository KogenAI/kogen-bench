#!/usr/bin/env python3
"""Recompute every number on the round page from the files in this folder.

    python3 -I analysis.py

Reads records.jsonl (one Standard record per graded cell), request-usage.jsonl (token counts per
request), single-call-probe.jsonl (the single-request probe). The usage-meter part (Part 3) is not recomputable here:
its ledger and meter readings are account activity and stay private. Standard library only; prints plain text.
"""
import datetime
import json
import os
import statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def rows(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def pct(x):
    return f"{100 * x:.1f}%"


def comparison():
    recs = rows("records.jsonl")
    reqs = rows("request-usage.jsonl")
    lanes = ("baseline", "session-id")
    cell = {}
    for r in recs:
        rep = r["cell_id"].split(f"-{r['task']['id']}-")[1].split("-")[0]  # r1, r2
        cell[(r["task"]["id"], rep, r["arm"])] = r

    print("== Build and review, two lanes (24 graded cells) ==")
    for lane in lanes:
        cs = [r for k, r in cell.items() if k[2] == lane]
        correct = sum(r["outcome"] == "pass" for r in cs)
        print(f"{lane}: cells {len(cs)}, correct {correct}")
        for stage, phase in (("build", "develop"), ("review", "review")):
            rq = [x for x in reqs if x["lane"] == lane and x["stage"] == stage]
            inp = sum(x["input_tokens"] for x in rq)
            cached = sum(x["cached_tokens"] for x in rq)
            # the same share from the records: their `input` excludes the cached part
            rec_cached = sum(r["tokens"]["phases"][phase]["cached_input"] for r in cs)
            rec_input = sum(r["tokens"]["phases"][phase]["input"] for r in cs) + rec_cached
            assert (inp, cached) == (rec_input, rec_cached), (lane, stage)
            # follow-up requests: every request but the first of its conversation
            by_cell = defaultdict(list)
            for x in rq:
                by_cell[(x["task"], x["rep"])].append(x)
            full = part = miss = 0
            ratios = []
            for xs in by_cell.values():
                xs.sort(key=lambda x: x["n"])
                for prev, cur in zip(xs, xs[1:]):
                    assert cur["conversation"] == prev["conversation"]
                    ratios.append(cur["cached_tokens"] / prev["input_tokens"])
                    if cur["cached_tokens"] >= prev["input_tokens"] - 1024:
                        full += 1
                    elif cur["cached_tokens"] > 0:
                        part += 1
                    else:
                        miss += 1
            print(f"  {stage}: requests {len(rq)}, input {inp}, cached {cached}, cached share {pct(cached / inp)}; "
                  f"follow-ups {full + part + miss} (full {full}, partial {part}, none {miss}), "
                  f"median cached / previous input {statistics.median(ratios):.3f}")
        unc = [r["tokens"]["total"]["input"] for r in cs]
        cost = [r["cost"]["usd"] for r in cs]
        wall = [r["timing"]["total_wall_s"] for r in cs]
        nreq = [sum(1 for x in reqs if (x["task"], x["rep"], x["lane"]) == (k[0], int(k[1][1:]), k[2]))
                for k in cell if k[2] == lane]
        print(f"  uncached input per cell: mean {statistics.mean(unc):,.0f}; cost total ${sum(cost):.2f}, mean ${statistics.mean(cost):.3f}; "
              f"requests per cell {statistics.mean(nreq):.1f}; wall per cell {statistics.mean(wall):.0f} s")
        print(f"  total input {sum(r['tokens']['total']['input'] + r['tokens']['total']['cached_input'] for r in cs):,}, "
              f"uncached {sum(unc):,}, cached {sum(r['tokens']['total']['cached_input'] for r in cs):,}, "
              f"output {sum(r['tokens']['total']['output'] for r in cs):,}")
    share = {}
    for lane in lanes:
        for stage in ("build", "review"):
            rq = [x for x in reqs if x["lane"] == lane and x["stage"] == stage]
            share[(lane, stage)] = sum(x["cached_tokens"] for x in rq) / sum(x["input_tokens"] for x in rq)
    for stage in ("build", "review"):
        print(f"{stage} cached share, session-id minus baseline: {100 * (share[('session-id', stage)] - share[('baseline', stage)]):+.1f} points")
    # paired by task and repetition
    pairs = sorted({(k[0], k[1]) for k in cell})
    dc = [cell[(t, r, "session-id")]["cost"]["usd"] - cell[(t, r, "baseline")]["cost"]["usd"] for t, r in pairs]
    du = [cell[(t, r, "session-id")]["tokens"]["total"]["input"] - cell[(t, r, "baseline")]["tokens"]["total"]["input"] for t, r in pairs]
    dw = [cell[(t, r, "session-id")]["timing"]["total_wall_s"] - cell[(t, r, "baseline")]["timing"]["total_wall_s"] for t, r in pairs]
    lower = sum(d < 0 for d in dc)
    tot_g = sum(cell[(t, r, "baseline")]["cost"]["usd"] for t, r in pairs)
    tot_c = sum(cell[(t, r, "session-id")]["cost"]["usd"] for t, r in pairs)
    ug = sum(cell[(t, r, "baseline")]["tokens"]["total"]["input"] for t, r in pairs)
    uc = sum(cell[(t, r, "session-id")]["tokens"]["total"]["input"] for t, r in pairs)
    print(f"paired ({len(pairs)} pairs): cost lower with the header in {lower} of {len(pairs)}; median cost difference ${statistics.median(dc):.3f}; "
          f"median uncached-input difference {statistics.median(du):,.0f}; median wall difference {statistics.median(dw):.0f} s")
    print(f"cost change {pct(tot_c / tot_g - 1)} (${tot_g:.2f} to ${tot_c:.2f}); uncached input change {pct(uc / ug - 1)} ({ug:,} to {uc:,})")
    k = lower
    n = len(pairs)
    from math import comb
    p = 2 * sum(comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n
    print(f"two-sided sign test on the cost direction: p = {p:.4f}")
    print("per task, mean cost per cell (baseline, session-id):")
    for t in sorted({k[0] for k in cell}):
        g = statistics.mean(cell[(t, r, "baseline")]["cost"]["usd"] for tt, r in pairs if tt == t)
        c = statistics.mean(cell[(t, r, "session-id")]["cost"]["usd"] for tt, r in pairs if tt == t)
        print(f"  {t}: {g:.3f} -> {c:.3f}")


def probe():
    print("\n== Single-request probe ==")
    rs = rows("single-call-probe.jsonl")
    groups = defaultdict(list)
    for r in rs:
        groups[(r["run"], r["model"], r["shape"])].append(r)
    for key, xs in groups.items():
        xs.sort(key=lambda x: x["turn"])
        ref = [x for x in xs if x["refusal"]]
        if ref:
            print(f"{key[0]:6} {key[1]:12} {key[2]:50} refused: {ref[0]['refusal']}")
            continue
        hits, full = [], 0
        for prev, cur in zip(xs, xs[1:]):
            hits.append(cur["cached_tokens"] / prev["input_tokens"])
            full += cur["cached_tokens"] >= prev["input_tokens"] - 1024
        print(f"{key[0]:6} {key[1]:12} {key[2]:50} median share of previous input served from cache {statistics.median(hits):.2f}, full {full} of {len(hits)}")


def meter():
    import os
    if not os.path.exists(os.path.join(HERE, "meter-ledger.jsonl")) if "HERE" in globals() else not os.path.exists("meter-ledger.jsonl"):
        print("\n== Usage meter: data not published (account activity); see README Part 3 ==")
        return
    print("\n== Usage meter against work done (descriptive) ==")
    led = rows("meter-ledger.jsonl")
    reads = rows("meter-readings.jsonl")

    def cum(t):
        s = [x for x in led if x["ended"] < t]
        return (len(s), sum(x["input_tokens"] for x in s), sum(x["cached_tokens"] for x in s),
                sum(x["output_tokens"] for x in s), sum(x["cost_usd"] for x in s))

    shown = {"2026-10-25T17:51", "2026-10-25T18:21", "2026-10-25T19:22", "2026-10-25T19:52", "2026-10-25T20:53",
             "2026-10-25T22:54", "2026-10-26T01:56", "2026-10-26T03:57"}
    print("reading (UTC), meter %, items ended, input M, cached M, output M, list $, $ per meter point")
    for r in reads:
        if r["read_at"][:16] in shown:
            n, i, c, o, k = cum(r["read_at"])
            print(f"{r['read_at'][:16]} {r['used_pct']:3d} {n:3d} {i / 1e6:6.2f} {c / 1e6:6.2f} {o / 1e6:5.2f} {k:6.2f} {k / r['used_pct']:5.2f}")
    # windows used in the first look; each reading is taken at its own time
    def reading(t):
        return next(r for r in reads if r["read_at"][:16] == t)

    def window(a, b):
        ra, rb = reading(a), reading(b)
        na, ia, ca, oa, ka = cum(ra["read_at"])
        nb, ib, cb, ob, kb = cum(rb["read_at"])
        print(f"window {a[11:]} to {b[11:]}: +{rb['used_pct'] - ra['used_pct']} points, list ${kb - ka:.1f}, "
              f"input {(ib - ia) / 1e6:.1f}M of which cached {100 * (cb - ca) / (ib - ia):.0f}%")

    first = reading("2026-10-25T17:51")
    na, ia, ca, oa, ka = cum(first["read_at"])
    print(f"window reset (15:46) to 17:51: +{first['used_pct']} points, list ${ka:.1f}, input {ia / 1e6:.1f}M of which cached {100 * ca / ia:.0f}%")
    window("2026-10-25T17:51", "2026-10-25T19:22")
    last = led[-1]["ended"]
    print(f"last item ended {last}; meter {reading('2026-10-25T19:52')['used_pct']} points at 19:52 and {reads[-1]['used_pct']} at {reads[-1]['read_at']}")
    print(f"whole evening: list ${cum(reads[-1]['read_at'])[4]:.2f} for {reads[-1]['used_pct']} points, ${cum(reads[-1]['read_at'])[4] / reads[-1]['used_pct']:.2f} per point")


if __name__ == "__main__":
    comparison()
    probe()
    meter()
