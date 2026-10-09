#!/usr/bin/env python3
"""Complete an r70 grade window whose MacBook controller lost its ssh session (rz1 admission window 2, 8 Oct).
Mirrors grade_window.py lines 106-116 exactly; adds recovery fields to the receipt. Prints aggregate outcomes only."""
import fcntl,json,subprocess,sys,time,pathlib
HERE=pathlib.Path('public-source-location-withheld')
host='kogen-bench-eu';short='eu';window=sys.argv[1];expected=int(sys.argv[2])
REMOTE='public-source-location-withheld'
def ssh(cmd,**kw):return subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15',host,cmd],check=True,capture_output=True,text=True,**kw).stdout
assert ssh(f"pgrep -f '[g]rade_worker.py {window}' | wc -l").strip()=='0','worker still running'
lines=ssh(f'cat {window}/outcomes.jsonl').splitlines();assert len(lines)==expected,(len(lines),expected)
records=[dict(json.loads(x),host=host,grade_route='r70-macbook-window-v1') for x in lines]
ssh(f'rm -rf -- {window}; test ! -e {window}')
with (HERE/'grades-append.lock').open('a') as guard:
 fcntl.flock(guard,fcntl.LOCK_EX)
 with (HERE/'grades.jsonl').open('a') as f:
  for row in records:row['sealed_scratch_purged']=True;f.write(json.dumps(row)+'\n')
receipt=dict(at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),host=host,jobs=len(records),purged=True,recovered_after_controller_ssh_drop=True,missing_jobs_regraded_in_next_window=sys.argv[3].split(',') if len(sys.argv)>3 else [],recovery_script='levers/rz1/gate/recover_window2.py',records=[dict(cell=r['cell'],outcome=r['outcome'],tests_total=r['tests_total'],tests_ran=r['tests_ran'],cause=r['cause']) for r in records])
with (HERE/'windows.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
(HERE/f'last-window-{short}').write_text(str(time.time()))
ssh(f'rm -f -- {REMOTE}/STOP-{short}')
print('recovered',len(records),'rows; purged; STOP-eu removed')
