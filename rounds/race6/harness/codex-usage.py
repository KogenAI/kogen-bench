#!/usr/bin/python3
"""Local supervisor usage readings: expired/pre-login rollout windows never alert."""
import datetime,json,os,time
from pathlib import Path
def reading(home,now=None):
    home=Path(home);now=time.time() if now is None else now
    # Metadata only; never open/read auth.json.
    try:login=(home/'auth.json').stat().st_mtime
    except OSError:login=0
    files=sorted((home/'sessions').rglob('*.jsonl'),key=lambda p:p.stat().st_mtime,reverse=True)[:40]
    for path in files:
        last=None
        with path.open(errors='ignore') as stream:
         for line in stream:
             if '"rate_limits"' not in line:continue
             try:
                 row=json.loads(line);p=row.get('payload',row);limits=p.get('rate_limits') or p.get('info',{}).get('rate_limits')
                 if limits:last=limits
             except (ValueError,TypeError):pass
        if not last:continue
        when=path.stat().st_mtime;as_of=datetime.datetime.fromtimestamp(when,datetime.timezone.utc).isoformat()
        windows=[]
        for name in ('primary','secondary'):
            w=last.get(name) or {}
            if not w:continue
            stale=when<login or (w.get('resets_at') is not None and w['resets_at']<now)
            windows.append(f"{name}={w.get('used_percent')}% window={w.get('window_minutes')}min resets_at={w.get('resets_at')} status={'STALE' if stale else 'CURRENT'}")
        return f"as_of={as_of} "+' '.join(windows)
    return 'as_of=unavailable no rate-limit data found'
if __name__=='__main__':print(reading(Path(os.path.expanduser(os.environ.get('CODEX_HOME','$HOME/.codex')))))
