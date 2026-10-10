#!/usr/bin/python3
# stalls.py — per-arm quota / rate-limit stall log from the timestamped Codex events (*.ts + *.jsonl) and turn stderr:
# every error/retry event mentioning 429, rate limit, quota or usage limit, with time; stall spans = from the first such event
# to the next successful event in that turn. Writes out/STALLS.tsv (arm, start, end, seconds, message) and prints totals per arm.
import json, glob, os, re, datetime
R = os.path.dirname(os.path.abspath(__file__)); O = R + '/out'
PAT = re.compile(r'429|rate.?limit|quota|usage limit|too many requests', re.I)
rows = []; tot = {}
for a in open(R + '/ARMS').read().split():
    tot[a] = 0.0
    for j in sorted(glob.glob(f'{O}/{a}/turn-*.jsonl')):
        ts = [l.rstrip('\n').split('\t') for l in open(j[:-6] + '.ts')] if os.path.exists(j[:-6] + '.ts') else []
        ev = [json.loads(l) for l in open(j, errors='ignore') if l.strip().startswith('{')]
        open_at = None; msg = ''
        for (t, typ, *_), e in zip(ts, ev):
            text = json.dumps(e)
            if PAT.search(text) and (typ in ('error', 'turn.failed') or 'retry' in text.lower()):
                if open_at is None: open_at, msg = float(t), (e.get('message') or text)[:160]
            elif open_at is not None:
                rows.append((a, open_at, float(t), msg)); tot[a] += float(t) - open_at; open_at = None
        err = j[:-6] + '.err'
        if os.path.exists(err):
            for l in open(err, errors='ignore'):
                if PAT.search(l): rows.append((a, None, None, l.strip()[:160]))
with open(O + '/STALLS.tsv', 'w') as w:
    for a, s, e, m in rows:
        f = lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%H:%M:%S') if x else '-'
        w.write(f"{a}\t{f(s)}\t{f(e)}\t{(e - s) if s and e else ''}\t{m}\n")
print({a: round(v) for a, v in tot.items()}, 'stall rows:', len(rows))
