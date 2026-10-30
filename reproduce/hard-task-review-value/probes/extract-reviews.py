#!/usr/bin/env python3 -I
"""Rebuild reviews.csv from Kogen cell run directories (standard library only).

usage: extract-reviews.py ANNOTATIONS.csv RUN_DIR [RUN_DIR ...] > reviews.csv

RUN_DIR is a lanes run directory (its basename is the cohort id, for example hk3-mb) holding
cells/<task>/r1/kogen/{evaluation.json, run-log/log.jsonl, run-log/review-*.json}.
One row per review attempt: every `review` event in run-log/log.jsonl. The reviewer is
counted as having edited the tree when a `pass` event follows the review (Kogen re-verifies
only a changed tree). A review is a regression when that next pass is red.
Cells that never reached a review (no review event) get no row.
"""
import csv, glob, json, os, sys

INSTRUMENT = {'kogen-loop-tool-cut', 'kogen-loop-read-ledger', 'kogen-loop-parallel-calls'}
COLS = ['cohort', 'task', 'task_group', 'model', 'effort', 'review_no', 'attempt', 'pass_reviewed',
        'verdict', 'findings', 'blocking', 'reviewer_edited_tree', 'post_review_pass_green',
        'cell_outcome', 'cell_passed', 'cell_hidden_or_regression_failed', 'note_covers_failing_area']


def jl(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def main(ann_path, runs):
    ann = {(r['cohort'], r['task'], r['review_no'], r['attempt']): r for r in csv.DictReader(open(ann_path, newline=''))}
    out = csv.DictWriter(sys.stdout, COLS, lineterminator='\n')
    out.writeheader()
    for run in runs:
        cohort = os.path.basename(os.path.normpath(run))
        for cell in sorted(glob.glob(os.path.join(run, 'cells', '*', 'r1', 'kogen'))):
            task = cell.split(os.sep)[-3]
            log = os.path.join(cell, 'run-log', 'log.jsonl')
            if not os.path.exists(log):
                continue
            events = jl(log)
            ev = json.load(open(os.path.join(cell, 'evaluation.json')))
            res = {}
            if os.path.exists(os.path.join(cell, 'result.json')):
                res = json.load(open(os.path.join(cell, 'result.json')))
            hidden_failed = [f for f in (ev.get('failed') or []) if not f.startswith('acceptance:')]
            meta = {}
            for f in glob.glob(os.path.join(cell, 'run-log', 'review-*.json')):
                meta = json.load(open(f))
            for i, e in enumerate(events):
                if e.get('event') != 'review':
                    continue
                nxt = next((x for x in events[i + 1:] if x.get('event') == 'pass'), None)
                key = (cohort, task, str(e.get('review')), str(e.get('attempt')))
                out.writerow({
                    'cohort': cohort, 'task': task,
                    'task_group': 'instrument' if task in INSTRUMENT else 'discriminating',
                    'model': meta.get('model', ''), 'effort': meta.get('effort', ''),
                    'review_no': e.get('review'), 'attempt': e.get('attempt'), 'pass_reviewed': e.get('pass'),
                    'verdict': e.get('verdict'), 'findings': len(e.get('findings') or []),
                    'blocking': sum(1 for x in (e.get('findings') or []) if x.get('severity') != 'note'),
                    'reviewer_edited_tree': int(nxt is not None),
                    'post_review_pass_green': '' if nxt is None else int(bool(nxt.get('green'))),
                    'cell_outcome': res.get('outcome', ''), 'cell_passed': int(bool(ev.get('all_passed'))),
                    'cell_hidden_or_regression_failed': int(bool(hidden_failed)),
                    'note_covers_failing_area': ann[key]['note_covers_failing_area'] if key in ann else 0,
                })


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
