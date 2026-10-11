#!/usr/bin/env python3
"""Portable transactional locks with exact mode restoration and mandatory suite lock."""
import argparse,errno,glob,json,os,stat,sys
from pathlib import Path
from hidden_inventory import protected
ROOT=Path(__file__).resolve().parent
def candidates(root=ROOT):
    root=Path(root).resolve(); scratch=root.parent; home=Path.home()
    inventory=json.loads((root/'hidden-inventory.json').read_text())
    local=root/'out/host-inventory/hidden-inventory.json'
    if local.exists():
        extra=json.loads(local.read_text());inventory=dict(inventory,locks=inventory['locks']+extra['locks'],errors=inventory['errors']+extra['errors'],outside_reach=inventory.get('outside_reach',[])+extra.get('outside_reach',[]))
    if inventory['errors']: raise ValueError('inventory has unresolved scan errors; refuse launch')
    source=Path(inventory.get('source_root',str(root)))
    suite_paths={Path(p).resolve() for p in inventory['locks']}
    suite_paths.update(root/Path(p).relative_to(source) for p in inventory['locks'] if source in Path(p).parents)
    paths=set(suite_paths)
    paths.add(root/'inputs/conformance')
    for pattern in ('race*','r3-*','r4-*','r5-*','r5mk-*','spec-*','suite-*','kogen-*','conf-final','verify','quint-cli','build-research','worktrees','shared'):
        paths.update(p for p in scratch.glob(pattern) if p.is_dir())
    paths.update(Path(p) for p in glob.glob('/tmp/kc*'))
    if (home/'.kogen').exists(): paths.add(home/'.kogen')
    outside={Path(p).resolve() for p in inventory.get('outside_reach',[])}
    # These roots were proven inaccessible before preparation; do not mutate their modes.
    for p in outside:
        if os.access(p,os.R_OK|os.X_OK):raise ValueError('previously inaccessible suite root is readable: '+str(p))
    paths-=outside
    if sys.platform.startswith('linux'):
        paths={p for p in paths if os.access(p,os.R_OK|os.X_OK)}  # Other admin-owned copies remain outside reach; live probe verifies.
    exempt={root,Path(os.environ.get('RACE3_KIT_DIR',str(scratch/'race3-kit'))).resolve(),Path(os.environ.get('RACE6_KIT_DIR',str(scratch/'race6-kit'))).resolve()}
    # Exempt kit roots only; hidden suite leaves inside kits are always locked.
    paths={p.resolve() for p in paths if p.exists() and p.resolve() not in exempt and not protected(p)}
    # Do not lock control/evidence trees within the current wave.
    paths={p for p in paths if root not in p.parents or p in suite_paths or root/'inputs/conformance'==p}
    ordered=[]
    for p in sorted(paths,key=lambda p:(len(p.parts),str(p))):
        if not any(q==p or q in p.parents for q in ordered): ordered.append(p)
    return ordered
def lock(root,paths,append=False):
    root=Path(root); receipt=root/'locks.tsv'; rows=[]
    if receipt.exists() and receipt.read_text().strip() and not append: raise ValueError('locks.tsv not empty: restore first')
    if append and receipt.exists(): rows=[line.split('\t',1) for line in receipt.read_text().splitlines()]
    (root/'out').mkdir(exist_ok=True)
    def inaccessible_directory(p):
        if not p.is_dir():return None
        try:os.listdir(p)
        except PermissionError as error:return str(error)
        return None
    def record_skip(p,reason):
        with (root/'out/lock-skipped-inaccessible.txt').open('a') as stream:
            stream.write(str(p)+'\t'+reason.replace('\n',' ')+'\n')
    # Validate everything before any chmod. Inaccessible directories stay untouched.
    todo=[]
    for path in paths:
        p=Path(path).resolve()
        if any(p==Path(row[1]) for row in rows): continue
        denied=inaccessible_directory(p)
        if denied is not None:
            record_skip(p,'listing denied before lock: '+denied);continue
        mode=stat.S_IMODE(p.stat().st_mode)
        if mode==0: raise ValueError(f'already mode 000: {p}')
        todo.append((format(mode,'o'),str(p)))
    types={p:('directory' if Path(p).is_dir() else 'file') for _,p in todo}
    (root/'out').mkdir(exist_ok=True)
    (root/'out/locked-path-types.json').write_text(json.dumps(types))
    rows.extend([mode,path] for mode,path in todo)
    receipt.write_text(''.join(f'{m}\t{p}\n' for m,p in rows))
    try:
        for mode,path in todo:
            p=Path(path)
            try:p.chmod(0)
            except PermissionError as error:
                denied=inaccessible_directory(p)
                if error.errno!=errno.EPERM or denied is None:raise
                if stat.S_IMODE(p.stat().st_mode)!=int(mode,8):raise
                rows=[row for row in rows if row[1]!=path]
                receipt.write_text(''.join(f'{m}\t{value}\n' for m,value in rows))
                record_skip(p,'chmod EPERM and listing denied: '+denied)
                continue
            if stat.S_IMODE(Path(path).stat().st_mode)!=0: raise ValueError('lock failed: '+path)
    except BaseException:
        unlock(root); raise
    return rows
def unlock(root):
    root=Path(root);receipt=root/'locks.tsv'
    if not receipt.exists():return
    rows=[line.split('\t',1) for line in receipt.read_text().splitlines()]
    failures=[]
    # Parents first, so descendants can be restored.
    for mode,path in sorted(rows,key=lambda row:len(Path(row[1]).parts)):
        try:
            p=Path(path)
            if stat.S_IMODE(p.stat().st_mode)==int(mode,8):continue  # Never changed; do not chmod TCC roots.
            p.chmod(int(mode,8))
            assert stat.S_IMODE(p.stat().st_mode)==int(mode,8)
        except (OSError,AssertionError) as e:failures.append(str(e))
    if failures: raise ValueError('unlock failed: '+ '; '.join(failures))
    receipt.write_text('')
    print(f'PASS restored {len(rows)} paths; receipt contains no mode-000 leftovers')
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('action',choices=('lock','unlock','list'));parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--append',action='store_true');parser.add_argument('paths',nargs='*');args=parser.parse_args()
    if args.action=='unlock':unlock(args.root);return
    paths=list(map(Path,args.paths)) if args.paths else candidates(args.root)
    if args.action=='list':print('\n'.join(map(str,paths)));return
    if not args.paths and sys.platform.startswith('linux'):
        suite=args.root/'inputs/conformance'
        import pwd
        assert suite.stat().st_uid==pwd.getpwnam('benchadmin').pw_uid and stat.S_IMODE(suite.stat().st_mode)==0o700,'Linux suite must be benchadmin:0700'
        # bench cannot chmod the admin-owned suite; leave it outside reach.
        paths=[p for p in paths if p!=suite.resolve()]
    rows=lock(args.root,paths,args.append);print(f'PASS locked {len(rows)} paths')
if __name__=='__main__':main()
