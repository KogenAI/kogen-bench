"""Enumerate cwd and process trees; fail closed on missing host observability."""
import os,shutil,signal,subprocess,time
from pathlib import Path
GROUPS={}
def table():
    data=subprocess.check_output(['ps','-axo','pid=,ppid=,pgid=,command='],text=True)
    rows={}
    GROUPS.clear()
    for row in data.splitlines():
        f=row.strip().split(None,3)
        if len(f)==4:
            rows[int(f[0])]=(int(f[1]),f[3]);GROUPS[int(f[0])]=int(f[2])
    return rows
def cwd_table():
    if Path('/proc').is_dir():
        result={}
        for p in Path('/proc').glob('[0-9]*/cwd'):
            try:result[int(p.parent.name)]=os.readlink(p)
            except OSError:pass
        return result
    lsof=shutil.which('lsof')
    if not lsof:raise RuntimeError('lsof is required on macOS')
    result={};pid=None
    data=subprocess.run([lsof,'-a','-d','cwd','-Fn'],text=True,capture_output=True)
    if data.returncode not in (0,1):raise RuntimeError('lsof cwd enumeration failed: '+data.stderr)
    if not data.stdout:raise RuntimeError('lsof returned no cwd records')
    for row in data.stdout.splitlines():
        if row.startswith('p'):pid=int(row[1:])
        elif row.startswith('n') and pid:result[pid]=row[1:]
    return result
def arm_processes(root,rows=None,cwds=None,selected=None):
    root=Path(root).resolve(); live=rows is None;rows=table() if live else rows;cwds=cwd_table() if cwds is None else cwds
    arms=selected or (root/'ARMS').read_text().split();roots=[str(root/a) for a in arms]
    matched=set()
    for pid,(ppid,command) in rows.items():
        cwd=cwds.get(pid,'')
        if any(cwd==p or cwd.startswith(p+'/') for p in roots):matched.add(pid)
        if selected is None:
            if any(str(root/name) in command for name in ('arm.sh','arm-cont.sh','snap-loop.sh','snap.sh')):matched.add(pid)
        elif any(name+' '+str(root)+' '+a+' ' in command for name in ('arm.sh','arm-cont.sh') for a in arms):matched.add(pid)
    for arm in arms:
        for name in ('pid','driver.pid'):
            p=root/'out'/arm/name
            if p.exists():
                pid=int(p.read_text())
                if pid in rows and (str(root) in rows[pid][1] or any(cwds.get(pid,'')==p or cwds.get(pid,'').startswith(p+'/') for p in roots)):matched.add(pid)
    if live:
        groups={int((root/'out'/a/'pgid').read_text()) for a in arms if (root/'out'/a/'pgid').exists()}
        matched.update(pid for pid in rows if GROUPS.get(pid) in groups)
    while True:
        extra={pid for pid,(parent,_) in rows.items() if parent in matched}-matched
        if not extra:break
        matched.update(extra)
    return matched-{os.getpid(),os.getppid()}
def stop(root,selected=None):
    root=Path(root)
    if selected is None:(root/'STOP').touch()
    else:
        for a in selected:(root/('STOP-'+a)).touch()
    for sig,duration in ((signal.SIGTERM,10),(signal.SIGKILL,10)):
        until=time.monotonic()+duration
        while True:
            pending=arm_processes(root,selected=selected)
            if not pending:return
            for pid in pending:
                try:os.kill(pid,sig)
                except ProcessLookupError:pass
            if time.monotonic()>=until:break
            time.sleep(.2)
    raise RuntimeError('arm processes remain; suite stays locked')
