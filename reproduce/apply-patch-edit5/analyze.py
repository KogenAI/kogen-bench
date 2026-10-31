#!/usr/bin/env python3
"""Reproduce the apply-patch-edit5 numbers from runs.csv (standard library only)."""
import csv, math, pathlib

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
ARMS = ['loop-default', 'apply-patch', 'codex']
LABEL = {'loop-default': 'loop default', 'apply-patch': 'loop + apply_patch', 'codex': 'Codex CLI'}
NUM = ('wall_s', 'requests', 'output_tokens', 'reasoning_tokens', 'edit_turns', 'edit_turn_output',
       'write_file_calls', 'apply_patch_calls', 'shell_edit_calls', 'apply_patch_errors', 'cost_usd')
for r in ROWS:
    r['passed'] = r['passed'] == '1'
    r['rep'] = int(r['rep'])
    for k in NUM:
        r[k] = float(r[k])
COUNTED = [r for r in ROWS if r['stratum'] == 'counted']
CELL = {(r['task'], r['rep'], r['arm']): r for r in COUNTED}
BLOCKS = sorted({(r['task'], r['rep']) for r in COUNTED}, key=lambda b: (b[1], list(dict.fromkeys(r['task'] for r in COUNTED)).index(b[0])))
DONE = [b for b in BLOCKS if all((*b, a) in CELL for a in ARMS)]


def test(w, l, n):
    m = w + l
    k = min(w, l)
    p = 1.0 if m == 0 else min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)
    return w, l, n - m, p


def sign(a, b):
    return test(sum(x < y for x, y in zip(a, b)), sum(x > y for x, y in zip(a, b)), len(a))


def cpp(r):  # cost per pass of one cell; a failed cell is worse than any pass, two failures tie
    return r['cost_usd'] if r['passed'] else math.inf


def p90(v):
    v = sorted(v)
    return v[max(0, math.ceil(.9 * len(v)) - 1)]


def median(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def fmt(t):
    return f'{t[0]}/{t[1]}, {t[2]} ties, p={t[3]:.4f}'


def arm_total(arm, blocks, key):
    return sum(CELL[(*b, arm)][key] for b in blocks)


def usd_per_pass(arm, blocks):
    n = sum(CELL[(*b, arm)]['passed'] for b in blocks)
    return arm_total(arm, blocks, 'cost_usd') / n if n else None


print('Per arm, gpt-6.1-terra high, counted cells only (dry cells excluded)')
print('arm | pass/launched | edit-turn output total / per run | edit turns per run | edit calls write_file / apply_patch / shell | cells using apply_patch / errors | output total | wall s median / p90 | requests per run | USD total / per pass')
for a in ARMS:
    xs = [CELL[(*b, a)] for b in BLOCKS]
    n = len(xs)
    s = lambda k: sum(x[k] for x in xs)
    passes = sum(x['passed'] for x in xs)
    print(f"{LABEL[a]} | {passes}/{n} | {s('edit_turn_output'):,.0f} / {s('edit_turn_output') / n:,.0f} | {s('edit_turns') / n:.1f} | "
          f"{s('write_file_calls'):.0f} / {s('apply_patch_calls'):.0f} / {s('shell_edit_calls'):.0f} | {sum(x['apply_patch_calls'] > 0 for x in xs)}/{n} / {s('apply_patch_errors'):.0f} | "
          f"{s('output_tokens'):,.0f} | {median([x['wall_s'] for x in xs]):,.3f} / {p90([x['wall_s'] for x in xs]):,.3f} | {s('requests') / n:.1f} | "
          f"${s('cost_usd'):.6f} / ${usd_per_pass(a, BLOCKS):.6f}")

print()
print(f'Paired by block, {len(DONE)} complete blocks (lower is better): first-arm wins / second-arm wins, ties, exact two-sided sign test p')
COMP = [('apply-patch', 'loop-default'), ('apply-patch', 'codex'), ('loop-default', 'codex')]


def geomean(a, b, key, bs):
    v = [math.log(CELL[(*k, a)][key] / CELL[(*k, b)][key]) for k in bs if CELL[(*k, a)][key] > 0 and CELL[(*k, b)][key] > 0]
    return (math.exp(sum(v) / len(v)) if v else None), len(v)


for a, b in COMP:
    print(f'{LABEL[a]} vs {LABEL[b]}')
    for m, name in (('edit_turn_output', 'edit-turn output'), ('cost', 'cost per pass'), ('wall_s', 'wall'), ('requests', 'requests'), ('output_tokens', 'total output')):
        fn = cpp if m == 'cost' else (lambda x, m=m: x[m])
        print(f'  {name}: {fmt(sign([fn(CELL[(*k, a)]) for k in DONE], [fn(CELL[(*k, b)]) for k in DONE]))}')
    da = [CELL[(*k, a)]['passed'] for k in DONE]
    db = [CELL[(*k, b)]['passed'] for k in DONE]
    print(f'  pass (discordant, first-only/second-only): {fmt(test(sum(x and not y for x, y in zip(da, db)), sum(y and not x for x, y in zip(da, db)), len(DONE)))}')
    g, n = geomean(a, b, 'edit_turn_output', DONE)
    print(f'  edit-turn output geomean ratio: {g:.3f} (n={n})')
    print(f"  total output geomean ratio: {geomean(a, b, 'output_tokens', DONE)[0]:.3f}")
    print(f'  USD per pass ratio: {usd_per_pass(a, DONE) / usd_per_pass(b, DONE):.3f}')
    print(f"  wall geomean ratio: {geomean(a, b, 'wall_s', DONE)[0]:.3f}")

print()
print('By task, apply_patch vs loop default (edit-turn output wins / losses; geomean ratio)')
for t in dict.fromkeys(r['task'] for r in COUNTED):
    bs = [b for b in DONE if b[0] == t]
    w = fmt(sign([CELL[(*k, 'apply-patch')]['edit_turn_output'] for k in bs], [CELL[(*k, 'loop-default')]['edit_turn_output'] for k in bs]))
    print(f"  {t}: {w}, ratio {geomean('apply-patch', 'loop-default', 'edit_turn_output', bs)[0]:.3f}")

failed = [b for b in DONE if not all(CELL[(*b, a)]['passed'] for a in ARMS)]
rest = [b for b in DONE if b not in failed]
print()
print(f'Without the failed block(s) {failed} ({len(rest)} blocks; a check made after the results, not registered)')
for a in ARMS:
    print(f"  {LABEL[a]}: edit-turn output {arm_total(a, rest, 'edit_turn_output'):,.0f}, edit turns {arm_total(a, rest, 'edit_turns'):.0f}, requests {arm_total(a, rest, 'requests'):.0f}, USD ${arm_total(a, rest, 'cost_usd'):.4f}, per pass ${usd_per_pass(a, rest):.4f}")
print(f"  apply_patch vs loop default USD per pass ratio {usd_per_pass('apply-patch', rest) / usd_per_pass('loop-default', rest):.3f}")

dry = [r for r in ROWS if r['stratum'] == 'dry']
print()
print(f"Spend: counted ${sum(r['cost_usd'] for r in COUNTED):.6f}, dry ${sum(r['cost_usd'] for r in dry):.6f} (credit probes, $0.001240, are not in runs.csv)")
print()
print('Per cell (task rep arm: edit-turn output / total output / edit calls w,a,s / USD / wall s / requests; outcome)')
for b in BLOCKS:
    for a in ARMS:
        x = CELL[(*b, a)]
        print(f"  {b[0]} r{b[1]} {a}: {x['edit_turn_output']:,.0f} / {x['output_tokens']:,.0f} / {x['write_file_calls']:.0f},{x['apply_patch_calls']:.0f},{x['shell_edit_calls']:.0f} / ${x['cost_usd']:.4f} / {x['wall_s']:,.1f} / {x['requests']:.0f}; {'pass' if x['passed'] else 'fail (' + x['outcome'] + ')'}")
