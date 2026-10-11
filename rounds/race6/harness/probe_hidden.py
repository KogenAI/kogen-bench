#!/usr/bin/env python3
"""Same-UID arm-environment denial probe; default mocks every inventoried path."""
import errno,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
from hidden_locks import lock,unlock
ROOT=Path(__file__).resolve().parent
def denied(paths):
    failures=[];checks=0;absent=0
    for value in paths:
        path=Path(value['path']); directory=value['directory']
        if value.get('tcc_skipped'):
            checks+=1
            try:os.listdir(path)
            except PermissionError as e:
                if e.errno in (errno.EPERM,errno.EACCES):print(f'denied-tcc {path}')
                else:failures.append(f'list {path}: expected EPERM/EACCES, got {e}')
            except OSError as e:failures.append(f'list {path}: expected permission denied, got {e}')
            else:failures.append(f'list {path}: EXPOSED')
            continue
        try:os.lstat(path)
        except FileNotFoundError:absent+=1;continue  # Removed copies have no readable contents.
        except PermissionError:pass
        operations=[('list',lambda p=path:os.listdir(p))] if directory else []
        operations.append(('read',lambda p=path,d=directory: (p/'probe-secret' if d else p).read_bytes()))
        for label,operation in operations:
            checks+=1
            try:operation()
            except PermissionError:continue
            except OSError as e:failures.append(f'{label} {path}: expected permission denied, got {e}')
            else:failures.append(f'{label} {path}: EXPOSED')
    if failures:
        print('\n'.join(failures));return 1
    print(f'PASS hidden-suite probe: {len(paths)} paths, {checks} denied operations, zero readable paths; {absent} absent paths')
    return 0
def execute(root,paths):
    # Arms share the host UID. The exact arm env is sourced before denial probes.
    payload=json.dumps(paths)
    arm=(root/'ARMS').read_text().split()[0]
    env=dict(os.environ,RACE6_PROBE_PATHS=payload,PYTHONDONTWRITEBYTECODE='1')
    command='set -e; source "$1/env.sh"; source "$1/$2/.kit-env.sh"; cd "$1/$2"; exec /usr/bin/python3 "$1/probe_hidden.py" --child'
    # Environment size may exceed exec limit: stdin carries the full inventory.
    env.pop('RACE6_PROBE_PATHS',None)
    return subprocess.run(['/bin/bash','-c',command,'probe',str(root),arm],env=env,input=payload,text=True).returncode
def live(root):
    data=json.loads((root/'hidden-inventory.json').read_text())
    local=root/'out/host-inventory/hidden-inventory.json'
    if local.exists():
        extra=json.loads(local.read_text());data=dict(data,found=data['found']+extra['found'],locks=data['locks']+extra['locks'],lock_types={**data.get('lock_types',{}),**extra.get('lock_types',{})})
    locks=[]
    for line in (root/'locks.tsv').read_text().splitlines():
        _,path=line.split('\t',1);locks.append({'path':path,'directory':True})
    suite=root/'inputs/conformance'
    # Avoid stat/read on hidden discoveries: inventory supplies the intended path.
    paths=[{'path':p,'directory':True} for p in data['locks']]
    # Probe discovery leaves as regular files; cases/quint directory markers are directories.
    paths += [{'path':entry['path'],'directory':entry.get('directory','cases/quint directory' in entry['reason'])} for entry in data['found'] if 'symlink' not in entry['reason']]
    source=Path(data.get('source_root',str(root)))
    paths += [dict(entry,path=str(root/Path(entry['path']).relative_to(source))) for entry in paths if source in Path(entry['path']).parents]
    paths += locks+[{'path':str(suite),'directory':True}]
    # A locked file can be a lock root. Use prelock inventory root types.
    types=data.get('lock_types',{})
    if (root/'out/locked-path-types.json').exists():types.update(json.loads((root/'out/locked-path-types.json').read_text()))
    for entry in paths:
        if entry['path'] in types:entry['directory']=types[entry['path']]=='directory'
    skipped_file=root/'out/lock-skipped-inaccessible.txt'
    skipped={line.split('\t',1)[0] for line in skipped_file.read_text().splitlines() if line} if skipped_file.exists() else set()
    for entry in paths:
        if entry['path'] in skipped:entry['tcc_skipped']=True
    existing={entry['path'] for entry in paths}
    paths += [{'path':p,'directory':True,'tcc_skipped':True} for p in sorted(skipped-existing)]
    return execute(root,paths)
def mock(root):
    data=json.loads((root/'hidden-inventory.json').read_text())
    with tempfile.TemporaryDirectory(prefix='.hidden-probe-',dir=root) as tmp:
        wave=Path(tmp); paths=[]
        for index,entry in enumerate(data['found']):
            # Each discovery has a separate analogue, retaining its basename.
            p=wave/'host'/f'{index:06d}'/Path(entry['path']).name
            isdir=entry.get('directory','cases/quint directory' in entry['reason'] or 'symlink' in entry['reason'])
            if isdir:p.mkdir(parents=True);(p/'probe-secret').write_text('hidden mock')
            else:p.parent.mkdir(parents=True);p.write_text('hidden mock')
            paths.append({'path':str(p),'directory':isdir})
        for index,p in enumerate(data['locks']):
            q=wave/'locks'/f'{index:06d}'/Path(p).name;q.mkdir(parents=True);(q/'probe-secret').write_text('hidden mock')
            paths.append({'path':str(q),'directory':True})
        # /tmp analogue stays strictly inside permitted write roots.
        p=wave/'tmp/kc-suite-copy';p.mkdir(parents=True);(p/'probe-secret').write_text('hidden mock')
        paths.append({'path':str(p),'directory':True})
        p=wave/'inputs/conformance';p.mkdir(parents=True);(p/'probe-secret').write_text('hidden mock')
        paths.append({'path':str(p),'directory':True})
        original={p['path']:Path(p['path']).stat().st_mode&0o7777 for p in paths}
        try:
            lock(wave,[p['path'] for p in paths])
            status=execute(root,paths)
        finally:unlock(wave)
        assert all((Path(p).stat().st_mode&0o7777)==mode for p,mode in original.items())
        leftovers=[str(p) for p in wave.rglob('*') if (p.stat().st_mode&0o7777)==0]
        assert not leftovers,leftovers
        print('PASS probe unlock: exact modes restored; zero mode-000 leftovers')
        return status
if __name__=='__main__':
    if '--child' in sys.argv:sys.exit(denied(json.load(sys.stdin)))
    sys.exit(live(ROOT) if '--live' in sys.argv else mock(ROOT))
