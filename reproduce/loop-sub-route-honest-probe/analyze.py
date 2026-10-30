#!/usr/bin/env python3
"""Reproduce the loop-sub-route-honest-probe numbers from probes.csv (standard library only).

Rates are output tokens divided by an interval of the response stream:
  first->last  = output / (last body byte - first body byte)
  delta->last  = output / (last body byte - first text delta)
Medians with the interquartile range use statistics.quantiles (exclusive method), n=10 per variant per block.
"""
import csv
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = {
    'A': 'A: HTTP SSE, empty User-Agent (loop today)',
    'B': 'B: HTTP SSE, honest User-Agent',
    'E': 'E: WebSocket response.create, honest User-Agent',
    'D': 'D: ChatGPT Codex backend with loop token, honest User-Agent',
}


def summary(values):
    q1, _, q3 = st.quantiles(values, n=4)
    return f'{st.median(values):.1f} [{q1:.1f}, {q3:.1f}]'


def main():
    with open(os.path.join(HERE, 'probes.csv'), newline='') as f:
        rows = list(csv.DictReader(f))
    ok = [r for r in rows if r['status'] in ('200', '101')]
    for r in ok:
        out = int(r['output_tokens'])
        first, delta, last = (float(r[k]) for k in ('first_byte_s', 'first_delta_s', 'last_byte_s'))
        r['first_last'] = out / (last - first)
        r['delta_last'] = out / (last - delta)
        r['delta'] = delta
    print(f'successful requests: {len(ok)}; output tokens {sorted({r["output_tokens"] for r in ok})}; '
          f'reasoning tokens {sorted({r["reasoning_tokens"] for r in ok})}; tiers {sorted({r["tier"] for r in ok})}')
    for block in ('B', 'E'):
        rs = [r for r in ok if r['block'] == block]
        for variant in (block, 'A'):
            v = [r for r in rs if r['variant'] == variant]
            print(f'block {block} {LABELS[variant]}: n={len(v)} first->last {summary([r["first_last"] for r in v])} '
                  f'delta->last {summary([r["delta_last"] for r in v])} tok/s; '
                  f'median time to first delta {st.median(r["delta"] for r in v):.2f} s')
    rates = [r['delta_last'] for r in ok]
    print(f'all {len(rates)} successful requests, three variants: delta->last median {st.median(rates):.1f} tok/s')
    for r in rows:
        if r['status'] not in ('200', '101'):
            print(f'{LABELS[r["variant"]]}: HTTP {r["status"]} {r["error"]} (single check, not retried)')


if __name__ == '__main__':
    main()
