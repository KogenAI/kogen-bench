#!/usr/bin/env python3
"""check.py: rerun the C9 reader over the published log skeletons and compare with the hand-assigned truth.
usage: python3 -I check.py      (run from this directory; stdlib only, no network, no model)"""
import csv, glob, importlib.util, json, os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ro', os.path.join(here, 'read-outcome.py')); ro = importlib.util.module_from_spec(spec); spec.loader.exec_module(ro)
t0 = time.time()
rows = list(csv.DictReader(open(os.path.join(here, 'data/truth.tsv')), delimiter='\t'))
def agree(truth_class, truth_code, got):
    return got[0] == truth_class and (truth_code == '*' or got[1] == truth_code)
v2 = v1 = base = interim = 0; green = 0; green_fail_v2 = green_fail_v1 = green_fail_interim = 0; failed_green = 0
unrefined_v1 = unrefined_v2 = 0
for r in rows:
    p = os.path.join(here, 'data/skeletons', r['id'] + '.log')
    g2 = ro.read(p); g1 = ro.read(p, approval_marker=False)
    tc, tk = r['truth_class'], r['truth_code']
    v2 += agree(tc, tk, g2); v1 += agree(tc, tk, g1)
    if tc == 'green':
        green += 1; green_fail_v2 += g2[0] != 'green'; green_fail_v1 += g1[0] != 'green'; green_fail_interim += r['interim_class'] != 'green'
        interim += r['interim_class'] == 'green'
    else:
        failed_green += g2[0] == 'green'
        interim += (r['interim_code'] == 'unknown') if tc == 'none' else (r['interim_code'] == tk)
        base += (r['baseline_code'] == 'unknown') if tc == 'none' else (r['baseline_code'] == tk)
ctl = sorted(glob.glob(os.path.join(here, 'data/control/*.log')))
ctl_green = sum(ro.read(p)[0] == 'green' for p in ctl)
res = dict(rows=len(rows), baseline_first_line_agree=base, interim_agree=interim, reader_v1_agree=v1, reader_v2_agree=v2,
           refined_rows=sum(r['refined_from_hand_text'] == '1' for r in rows),
           green_rows=green, green_read_as_failed_baseline_as_recorded_by_delivery=3, green_read_as_failed_interim=green_fail_interim,
           green_read_as_failed_v1=green_fail_v1, green_read_as_failed_v2=green_fail_v2, failed_read_as_green_v2=failed_green,
           control_landed_logs=len(ctl), control_read_green=ctl_green, duration_s=round(time.time() - t0, 3))
print(json.dumps(res, indent=1))
print('%d rows, %d agree (v2); %d green read as failed (v2); %d of %d control logs read green' % (len(rows), v2, green_fail_v2, ctl_green, len(ctl)))
json.dump(res, open(os.path.join(here, 'data/results.json'), 'w'), indent=1)
