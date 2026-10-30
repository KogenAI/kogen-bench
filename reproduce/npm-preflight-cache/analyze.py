"""Summarise the npm-preflight-cache fault tests and test runs from runs.csv and tests.csv.
usage: python3 analyze.py   (standard library only)"""
import csv, pathlib

H = pathlib.Path(__file__).resolve().parent
runs = list(csv.DictReader(open(H / 'runs.csv')))
tests = list(csv.DictReader(open(H / 'tests.csv')))
f = float

print('== npm-stage-once: preflight under a stalled npm (the stall is 600 s; the approval deadline is 120 s) ==')
print('harness    host   task          preflight s  deadline s  npm calls  result')
for x in runs:
    if x['change'] == 'npm-stage-once' and x['fault'].startswith('npm stalls'):
        print('%-10s %-6s %-13s %-12s %-11s %-10s %s' % (x['harness'], x['host'], x['task'], x['elapsed_s'], x['deadline_s'], x['npm_calls'], x['outcome']))
new = [x for x in runs if x['change'] == 'npm-stage-once' and x['harness'] == 'patched' and x['fault'].startswith('npm stalls')]
old = [x for x in runs if x['change'] == 'npm-stage-once' and x['harness'] == 'unpatched']
print('patched: %d/%d approved, %.3f-%.3f s, npm calls %d' % (sum(x['passed'] == 'true' for x in new), len(new), min(f(x['elapsed_s']) for x in new), max(f(x['elapsed_s']) for x in new), sum(int(x['npm_calls']) for x in new)))
print('unpatched: %d/%d refused at the %s s deadline, npm calls %d' % (sum(x['passed'] == 'false' for x in old), len(old), old[0]['deadline_s'], sum(int(x['npm_calls']) for x in old)))
for x in runs:
    if x['change'] == 'npm-stage-once' and not x['fault'].startswith('npm stalls'):
        print('%s: %s, %s s, %s' % (x['fault'], x['task'], x['elapsed_s'], x['outcome']))

print('\n== defer-approval-timeouts: setup stalled 125 s for task-tags-go (low-effort lane a0) ==')
for x in runs:
    if x['change'] == 'defer-approval-timeouts':
        print('%-34s %-12s %-6s %-9s %s' % (x['stage'], x['task'], x['lane'], x['elapsed_s'], x['outcome']))
d = [x for x in runs if x['change'] == 'defer-approval-timeouts']
print('deadline failures: %d (both task-tags-go a0); approved on the later invocation: %s' % (
    sum(x['timed_out'] == 'true' for x in d),
    ', '.join('%s/%s' % (x['task'], x['lane']) for x in d if x['stage'] == 'later-invocation')))

print('\n== test runs ==')
for t in tests:
    print('%-24s %-6s %-48s tests=%-3s skipped=%s %.3f s  %s' % (t['change'], t['host'], t['suite'], t['tests'], t['skipped'], f(t['seconds']), t['result'][:60]))
