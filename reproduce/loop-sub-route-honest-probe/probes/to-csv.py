#!/usr/bin/env python3
"""Convert subroute-probe.py JSON lines to probes.csv rows.

usage: to-csv.py BLOCK=FILE.jsonl [BLOCK=FILE.jsonl ...] > probes.csv
Each BLOCK is the candidate of a paired block (B, E) or of a single check (D).
Error records keep only the HTTP status and the provider's error code.
"""
import csv
import json
import sys

FIELDS = ['block', 'variant', 'rep', 'transport', 'status', 'error', 'output_tokens', 'reasoning_tokens', 'tier',
          'first_byte_s', 'first_delta_s', 'last_byte_s']
w = csv.writer(sys.stdout, lineterminator='\n')
w.writerow(FIELDS)
for arg in sys.argv[1:]:
    block, path = arg.split('=', 1)
    for line in open(path):
        d = json.loads(line)
        if 'error' in d:
            try:
                err = json.loads(d.get('detail') or '{}').get('error', {})
                code = '/'.join(x for x in (err.get('code'), err.get('type')) if x) if isinstance(err, dict) else ''
            except ValueError:
                code = ''
            w.writerow([block, d['cand'], d['rep'], 'websocket' if d['cand'] == 'E' else 'http-sse', d.get('http_status'),
                        code or d['error'], '', '', '', '', '', ''])
        else:
            w.writerow([block, d['cand'], d['rep'], d['transport'], d['status'], '', d['output'], d['reasoning'], d['tier'],
                        repr(d['first_s']), repr(d['first_delta_s']), repr(d['last_s'])])
