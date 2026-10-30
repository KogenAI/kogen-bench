"""Print the goose-labels-go approval-deadline measurements from runs.csv and the ratios the finding relies on.
usage: python3 analyze.py   (standard library only)"""
import csv, pathlib

H = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(H / 'runs.csv')))
DEADLINE = 120.0
get = lambda step, cond: next(r for r in rows if r['step'] == step and r['condition'].startswith(cond))
f = float

print('tree: %s files, %s MB; node_modules: %s files, %s MB (ignored)' % (
    get('tree', 'task start')['files'], get('tree', 'task start')['megabytes'],
    get('tree', 'node_modules')['files'], get('tree', 'node_modules')['megabytes']))
ga0, ga1 = get('git_add', 'fresh GIT_INDEX_FILE; no node'), get('git_add', 'fresh GIT_INDEX_FILE; with node')
print('git add, 2,373 files staged: %s s without node_modules, %s s with (%.2f%% of the %d s deadline)' % (ga0['wall_s'], ga1['wall_s'], 100 * f(ga0['wall_s']) / DEADLINE, DEADLINE))
cold, warm = get('go_build', 'cold'), get('go_build', 'warm')
print('go build: cold %s s wall / %s CPU-s, warm %s s (cold/warm wall %.1fx, CPU/wall %.1fx)' % (
    cold['wall_s'], cold['cpu_s'], warm['wall_s'], f(cold['wall_s']) / f(warm['wall_s']), f(cold['cpu_s']) / f(cold['wall_s'])))
print('npm ci from a warm npm cache: %s s' % get('npm_ci', 'warm')['wall_s'])
for r in rows:
    if r['step'] == 'preflight':
        print('preflight: %-70s %s s, %s' % (r['condition'][:70], r['wall_s'] or 'n/a', r['outcome']))
print('reading: git add is not slow (largest measured value %.2f s); the CPU-heavy step is the cold build (%.1f CPU-s).' % (max(f(ga0['wall_s']), f(ga1['wall_s'])), f(cold['cpu_s'])))
