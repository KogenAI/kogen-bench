# report.py <pack dir>: prints the finding's tables from data/cells.json (one record per cell) and data/replay.json.
import json, os, sys, collections
d = sys.argv[1] if len(sys.argv) > 1 else '.'
cells = json.load(open(os.path.join(d, 'data/cells.json')))
def grp(c): return (c['set'], c['lineup'], c['arm'])
G = collections.defaultdict(list)
for c in cells: G[grp(c)].append(c)
print('| set | lineup | arm | cells | ready | questions asked | mean per cell | cells asking | follow-ups of answers | non-UX after round 2 | refusals by gate |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for k in sorted(G):
    cs = G[k]; q = sum(c['questions_asked'] for c in cs)
    gates = collections.Counter(r['gate'] for c in cs for r in c['refusals'])
    print(f"| {k[0]} | {k[1]} | {k[2]} | {len(cs)} | {sum(c['ready'] for c in cs)} | {q} | {q/len(cs):.2f} | {sum(c['questions_asked'] > 0 for c in cs)} | "
          f"{sum(c['follow_ups_of_answers'] for c in cs)} | {sum(c['nonux_questions_after_round_2'] for c in cs)} | "
          + ', '.join(f'{g} {n}' for g, n in gates.most_common()) + ' |')
print()
print('| row | arm | ready | questions per session | session exits | answer rounds | refusals (attempt: gate) | wall s |')
print('|---|---|---|---|---|---|---|---|')
for c in sorted((c for c in cells if c['set'] == 'rows'), key=lambda c: (int(c['task'].split()[1]), c['arm'])):
    print(f"| {c['task']} | {c['arm']} | {'yes' if c['ready'] else 'no'} | {c['questions_per_session']} | {c['session_exit_codes']} | {c['answer_rounds']} | "
          + '; '.join(f"{r['attempt']}: {r['gate']}" for r in c['refusals']) + f" | {c['wall_s']:.0f} |")
rp = os.path.join(d, 'data/replay.json')
if os.path.exists(rp):
    r = json.load(open(rp)); print(); print('Replay of the recorded questions (no model call):', json.dumps(r['counts']))
