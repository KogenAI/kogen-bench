#!/usr/bin/env python3
"""msg.py <report.ndjson> -> per-scenario records [{uri, intent, name, line, wall, status, err}] (Cucumber message format).
wall = testCaseFinished.timestamp - testCaseStarted.timestamp (the readiness run's own report). A scenario's status is the worst of its
steps (FAILED > UNDEFINED > AMBIGUOUS > PENDING > PASSED > SKIPPED); retried attempts are not used (no --retry)."""
import sys, json, re
RANK = {'FAILED':5,'AMBIGUOUS':4,'UNDEFINED':3,'PENDING':2,'UNKNOWN':2,'PASSED':1,'SKIPPED':0}
def ts(t): return t['seconds'] + t['nanos']/1e9
def load(path):
    pk, tc, started, steps, out = {}, {}, {}, {}, []
    gdoc = {}
    for line in open(path, errors='replace'):
        try: m = json.loads(line)
        except Exception: continue
        if 'gherkinDocument' in m:
            d = m['gherkinDocument']; gdoc[d['uri']] = d
        elif 'pickle' in m:
            p = m['pickle']; pk[p['id']] = p
        elif 'testCase' in m:
            t = m['testCase']; tc[t['id']] = t
        elif 'testCaseStarted' in m:
            s = m['testCaseStarted']; started[s['id']] = dict(tc=s['testCaseId'], t=ts(s['timestamp']), attempt=s.get('attempt',0))
        elif 'testStepFinished' in m:
            s = m['testStepFinished']; r = s['testStepResult']
            e = steps.setdefault(s['testCaseStartedId'], [])
            e.append((r['status'], (r.get('message') or '')[:400]))
        elif 'testCaseFinished' in m:
            f = m['testCaseFinished']; s = started.get(f['testCaseStartedId'])
            if not s: continue
            p = pk[tc[s['tc']]['pickleId']]
            st = steps.get(f['testCaseStartedId'], [])
            worst = max((x[0] for x in st), key=lambda z: RANK.get(z, 2), default='PASSED')
            msg = next((x[1] for x in st if x[0] == worst and x[1] and worst != 'PASSED'), '')
            uri = p['uri']; mm = re.search(r'intents/([^/]+)/', uri)
            out.append(dict(uri=uri, intent=mm.group(1) if mm else uri, name=p['name'], wall=ts(f['timestamp']) - s['t'], start=s['t'], end=ts(f['timestamp']), status=worst, err=msg, attempt=s['attempt'], willRetry=f.get('willBeRetried', False)))
    return out
if __name__ == '__main__':
    r = load(sys.argv[1]); print(json.dumps(r))
