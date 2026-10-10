#!/usr/bin/python3
# Print the latest Codex rate-limit usage (percent only) from the newest local rollout that has it.
import os, glob, json, time
files = sorted(glob.glob(os.path.join(os.path.expanduser(os.environ.get('CODEX_HOME','~/.codex')),'sessions/**/*.jsonl'), recursive=True), key=os.path.getmtime, reverse=True)[:40]
for f in files:
    last = None
    for line in open(f, errors='ignore'):
        if '"rate_limits"' in line:
            try:
                d = json.loads(line); p = d.get('payload', d)
                rl = p.get('rate_limits') or p.get('info', {}).get('rate_limits')
                if rl: last = rl
            except Exception: pass
    if last:
        out = []
        for k in ('primary', 'secondary'):
            w = last.get(k) or {}
            if w: out.append('%s=%s%% window=%smin resets_in=%sh' % (k, w.get('used_percent'), w.get('window_minutes'), round((w.get('resets_at', 0) - time.time()) / 3600, 1) if w.get('resets_at') else '?'))
        print('as_of=%s %s' % (time.strftime('%H:%MZ', time.gmtime(os.path.getmtime(f))), ' '.join(out))); break
else:
    print('no rate-limit data found')
