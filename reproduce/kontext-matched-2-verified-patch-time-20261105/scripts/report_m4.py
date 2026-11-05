#!/usr/bin/env python3
"""report_m4.py: the kontext-matched-2 r4 screen rule (time to an independently verified patch), model-free.

    python3 -I report_m4.py CELLS_DIR [--out report.json]

CELLS_DIR holds one directory per unit (kxm4-screen-<case>-r<rep>[-x]) with the harness's summary.json
(rows: case, arm direct|assisted, outcome green|green_after_followup|red|None, total_s, first_attempt_s,
counts_for_model, attempts[].usage). An <id>-x directory (infrastructure rerun) replaces <id>.
Rule (plan PLAN-kontext-matched-2.md, amendment r4, fixed before any r4 cell):
  matched pairs only (both rows counts_for_model); T = total_s if verified else C = 1200 s;
  per case ratio = median T_B / median T_A over matched reps (both arms red in every rep: uninformative);
  CLEAR LOSS: >=2 cases with B red both reps and A green both, or B verified <= A verified - 2,
              or median ratio over informative cases >= 1.15 with B verified <= A verified;
  PROMISING: B verified >= A verified; no case B red both & A green both; on Crane AND on Rust:
             median per-case ratio <= 0.85 and B verified >= A verified in that stack;
  otherwise UNRESOLVED.  A = direct (no Context), B = assisted (Context packet).
"""
import argparse, json, re, statistics, sys
from pathlib import Path

C = 1200.0
STACK = lambda case: 'crane' if case.startswith('crane-') else ('rust' if case.startswith(('bat', 'tokio', 'rg', 'ripgrep')) else 'other')
VERIFIED = ('green', 'green_after_followup')


def tokens(row):
    t = 0
    for a in row.get('attempts') or []:
        u = a.get('usage') or {}
        t += sum(u.get(k) or 0 for k in ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens'))
    return t


def load(cells):
    units = {}
    for d in sorted(Path(cells).iterdir()):
        m = re.match(r'^kxm4-screen-(.+)-r(\d+)(-x)?$', d.name)
        if not m or not (d / 'summary.json').is_file():
            continue
        key = (m.group(1), int(m.group(2)))
        if key in units and not m.group(3):
            continue  # the -x rerun replaces the original
        units[key] = (d.name, json.loads((d / 'summary.json').read_text()))
    return units


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('cells')
    ap.add_argument('--out')
    a = ap.parse_args(argv)
    units = load(a.cells)
    pairs, dropped = [], []
    for (case, rep), (uid, s) in sorted(units.items()):
        rows = {r['arm']: r for r in s.get('rows', []) if r.get('case') == case}
        A, B = rows.get('direct'), rows.get('assisted')
        if not (A and B and A.get('counts_for_model') and B.get('counts_for_model')):
            dropped.append(dict(case=case, rep=rep, unit=uid, direct=A and A.get('excluded'), assisted=B and B.get('excluded')))
            continue
        p = dict(case=case, rep=rep, unit=uid, stack=STACK(case))
        for arm, r in (('A', A), ('B', B)):
            v = r.get('outcome') in VERIFIED
            p[arm] = dict(outcome=r.get('outcome'), verified=v, total_s=r.get('total_s'), T=r['total_s'] if v else C,
                          first_attempt_s=r.get('first_attempt_s'), tokens=tokens(r),
                          packet_bytes=sum((x.get('packet_bytes') or 0) for x in r.get('attempts') or []) or None)
        pairs.append(p)
    cases = {}
    for p in pairs:
        cases.setdefault(p['case'], []).append(p)
    per_case = {}
    for case, ps in sorted(cases.items()):
        va = sum(p['A']['verified'] for p in ps); vb = sum(p['B']['verified'] for p in ps)
        info = va + vb > 0
        mA = statistics.median(p['A']['T'] for p in ps); mB = statistics.median(p['B']['T'] for p in ps)
        per_case[case] = dict(stack=STACK(case), pairs=len(ps), A_verified=va, B_verified=vb, informative=info,
                              median_T_A=mA, median_T_B=mB, ratio=(mB / mA) if info else None,
                              B_red_both_A_green_both=len(ps) >= 2 and vb == 0 and va == len(ps),
                              A_red_both_B_green_both=len(ps) >= 2 and va == 0 and vb == len(ps),
                              median_tokens_A=statistics.median(p['A']['tokens'] for p in ps),
                              median_tokens_B=statistics.median(p['B']['tokens'] for p in ps))
    VA = sum(c['A_verified'] for c in per_case.values()); VB = sum(c['B_verified'] for c in per_case.values())
    ratios = [c['ratio'] for c in per_case.values() if c['ratio'] is not None]
    med_all = statistics.median(ratios) if ratios else None
    stacks = {}
    for st in ('crane', 'rust'):
        cs = [c for c in per_case.values() if c['stack'] == st]
        rs = [c['ratio'] for c in cs if c['ratio'] is not None]
        sa = sum(c['A_verified'] for c in cs); sb = sum(c['B_verified'] for c in cs)
        med = statistics.median(rs) if rs else None
        stacks[st] = dict(cases=len(cs), A_verified=sa, B_verified=sb, median_ratio=med,
                          holds=med is not None and med <= 0.85 and sb >= sa)
    losses = sum(c['B_red_both_A_green_both'] for c in per_case.values())
    clear_loss = losses >= 2 or VB <= VA - 2 or (med_all is not None and med_all >= 1.15 and VB <= VA)
    promising = (not clear_loss) and VB >= VA and losses == 0 and all(s['holds'] for s in stacks.values())
    verdict = 'CLEAR LOSS' if clear_loss else ('PROMISING' if promising else 'UNRESOLVED')
    rep = dict(rule='kontext-matched-2 r4', censor_s=C, verdict=verdict, matched_pairs=len(pairs), dropped_pairs=dropped,
               A_verified=VA, B_verified=VB, median_ratio_all=med_all, b_red_both_a_green_both_cases=losses,
               stacks=stacks, per_case=per_case, pairs=pairs)
    text = json.dumps(rep, indent=1)
    if a.out:
        Path(a.out).write_text(text + '\n')
    print(f"verdict {verdict}: matched pairs {len(pairs)} (dropped {len(dropped)}), verified A {VA} B {VB}, "
          f"median per-case T_B/T_A {med_all if med_all is None else round(med_all, 3)}; "
          + '; '.join(f"{k}: ratio {v['median_ratio'] if v['median_ratio'] is None else round(v['median_ratio'], 3)} "
                      f"verified A {v['A_verified']} B {v['B_verified']} holds={v['holds']}" for k, v in stacks.items()))
    for case, c in per_case.items():
        print(f"  {case:16s} {c['stack']:5s} pairs={c['pairs']} verified A={c['A_verified']} B={c['B_verified']} "
              f"T_A={c['median_T_A']:.1f} T_B={c['median_T_B']:.1f} ratio={'-' if c['ratio'] is None else round(c['ratio'], 3)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
