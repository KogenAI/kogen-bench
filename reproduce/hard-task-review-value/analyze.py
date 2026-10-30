#!/usr/bin/env python3
"""Count what Kogen's independent reviews did across the hard-task cohorts (standard library only)."""
import csv, pathlib

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('reviews.csv'), newline='')))
GROUPS = [('discriminating', 'tasks that can separate the setups'),
          ('instrument', 'three tasks whose acceptance scenarios no setup could pass')]


def n(rows, f):
    return sum(1 for r in rows if f(r))


def show(label, rows):
    cells = len({(r['cohort'], r['task']) for r in rows})
    edited = [r for r in rows if r['reviewer_edited_tree'] == '1']
    regress = [r for r in edited if r['post_review_pass_green'] == '0']
    failing = [r for r in rows if r['cell_hidden_or_regression_failed'] == '1']
    print(f'{label}: {len(rows)} reviews in {cells} cells')
    print(f'  verdict approve: {n(rows, lambda r: r["verdict"] == "approve")}; blocking findings: {sum(int(r["blocking"]) for r in rows)}; '
          f'note-level findings: {sum(int(r["findings"]) for r in rows)} in {n(rows, lambda r: int(r["findings"]) > 0)} reviews')
    print(f'  reviewer changed the tree (a verification pass followed): {len(edited)}; that pass red (regression): {len(regress)}'
          + (' (' + ', '.join(f'{r["cohort"]} {r["task"]} attempt {r["attempt"]}' for r in regress) + ')' if regress else ''))
    print(f'  reviews of a cell whose final tree fails a hidden or regression test: {len(failing)}, all approved: '
          f'{n(failing, lambda r: r["verdict"] == "approve")}')
    print(f'  of those, notes that cover the failing area: {n(failing, lambda r: r["note_covers_failing_area"] == "1")}'
          + (' (' + ', '.join(f'{r["cohort"]} {r["task"]}' for r in failing if r['note_covers_failing_area'] == '1') + ')'
             if any(r['note_covers_failing_area'] == '1' for r in failing) else ''))
    print(f'  blocking findings in those reviews: {sum(int(r["blocking"]) for r in failing)}')


print(f'review attempts: {len(ROWS)}; cohorts: {sorted({r["cohort"] for r in ROWS})}')
print()
show('All reviews', ROWS)
for g, text in GROUPS:
    print()
    show(f'{g} ({text})', [r for r in ROWS if r['task_group'] == g])
print()
print('Per cohort (model, effort): reviews | changed tree | regressions')
for c in dict.fromkeys(r['cohort'] for r in ROWS):
    rs = [r for r in ROWS if r['cohort'] == c]
    ed = [r for r in rs if r['reviewer_edited_tree'] == '1']
    print(f'{c} ({rs[0]["model"]}, {rs[0]["effort"]}): {len(rs)} | {len(ed)} | {n(ed, lambda r: r["post_review_pass_green"] == "0")}')
