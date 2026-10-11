#!/usr/bin/env python3
"""Read-only home scan; never descend into audit-protected storage."""
import argparse, hashlib, json, os, stat
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROTECTED={'Library','Areas','iCloud','CloudDocs','Mobile Documents'}
def protected(path):
    return any(p in PROTECTED or p.startswith('.codex') for p in Path(path).parts)
def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def scan(root=ROOT, home=None, extra=(),output_root=None):
    root=Path(root); home=Path(home or Path.home());dest=Path(output_root or root);dest.mkdir(parents=True,exist_ok=True);(dest/'evidence').mkdir(exist_ok=True)
    if (root/'hidden-case-hashes.json').exists():
        known={int(size):set(values) for size,values in json.loads((root/'hidden-case-hashes.json').read_text()).items()}
    else:
        known={}
        for p in (root/'inputs/conformance/cases').rglob('*'):
            if p.is_file():known.setdefault(p.stat().st_size,set()).add(digest(p))
    found={}; errors=[]; quint=[]; aliases=[]
    def add(p,why): found.setdefault(str(p),set()).add(why)
    (dest/'inventory-scan.pid').write_text(str(os.getpid())+'\n')
    visited=0
    starts=[p for p in home.iterdir() if not protected(p) and p.is_dir()] + list(map(Path,extra))
    starts.sort(key=lambda p: (p.name!='retained-run',str(p)))
    for start in starts:
        def error(e): errors.append(str(e))
        for base,dirs,files in os.walk(start,followlinks=False,onerror=error):
            visited+=1
            if visited%10000==0:
                (dest/'evidence/inventory-progress.txt').write_text(f'directories={visited} discoveries={len(found)} current={base}\n')
            dirs[:]=[d for d in dirs if not protected(Path(base)/d)]
            for d in list(dirs):
                p=Path(base)/d
                if p.is_symlink():
                    target=p.resolve()
                    if not protected(target): aliases.append((str(p),str(target)))
                if d=='quint' and Path(base).name=='cases': add(p,'cases/quint directory')
            for name in files:
                p=Path(base)/name
                if protected(p): continue
                if name=='quint.sh': quint.append(str(p))
                if name=='kogen-conformance': add(p,'runner name')
                try:
                    if p.is_symlink() and protected(p.resolve()): continue
                    st=p.stat()
                    if not stat.S_ISREG(st.st_mode): continue
                    size=st.st_size
                    if size in known and digest(p) in known[size]: add(p,'frozen suite case content hash')
                    if name in ('cli.py','__main__.py') and size<200000 and b'kogen-conformance' in p.read_bytes():
                        add(p,'runner entrypoint content')
                except OSError as e: errors.append(str(e))
    protections={}
    for name in found:
        p=Path(name); parts=p.parts
        if 'conformance' in parts: lock=Path(*parts[:parts.index('conformance')+1])
        elif 'kogen_conformance' in parts: lock=Path(*parts[:parts.index('kogen_conformance')])
        elif 'cases' in parts: lock=Path(*parts[:parts.index('cases')+1])
        else: lock=p
        protections[name]=str(lock)
    # Existing aliases into discovered trees receive their canonical protection.
    for alias,target in aliases:
        for lock in set(protections.values()):
            if target==lock or target.startswith(lock+'/'):
                found.setdefault(alias,set()).add('symlink to hidden suite'); protections[alias]=lock; break
    data={'source_root':str(root.resolve()),'home':str(home),'found':[{'path':p,'reason':'; '.join(sorted(found[p])), 'protect':protections[p]} for p in sorted(found)],
          'locks':sorted(set(protections.values())), 'lock_types':{p:('directory' if Path(p).is_dir() else 'file') for p in set(protections.values())}, 'errors':sorted(set(errors)), 'quint_wrappers':sorted(set(quint)),
          'excluded':'Library, .codex*, iCloud/CloudDocs/Mobile Documents, Areas: audit-protected; never read or locked'}
    (dest/'hidden-inventory.json').write_text(json.dumps(data,indent=2)+'\n')
    names=sorted({p.name for p in (root/'inputs/conformance/cases').rglob('*') if p.is_file()})
    (dest/'hidden-suite-names.json').write_text(json.dumps(names,indent=2)+'\n')
    text=f"HIDDEN SUITE INVENTORY: {len(found)} discoveries; {len(data['locks'])} lock paths\n{data['excluded']}\n"
    text+='Every discovery is protected by chmod 000 of its listed path (Linux: benchadmin-owned wave suite 0700).\n'
    text+='Wave inputs/conformance is mandatory, even if absent from this host inventory. /tmp/kc* is rescanned and locked at start.\n'
    text+=''.join(f"{p}\t{protections[p]}\t{'; '.join(sorted(found[p]))}\n" for p in sorted(found))
    text+='SCAN ERRORS (must resolve or establish already-unreadable protection before launch):\n'+'\n'.join(data['errors'])+'\n'
    (dest/'HIDDEN-SUITE-INVENTORY.txt').write_text(text)
    print(f"discoveries={len(found)} locks={len(data['locks'])} errors={len(data['errors'])}")
    print('quint wrappers: '+json.dumps(data['quint_wrappers']))
    return data
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--home',type=Path);parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    scan(home=args.home,extra=('/tmp','/home/benchadmin') if os.uname().sysname=='Linux' else ('/tmp',),output_root=args.output_dir)
    from inventory_finalize import finalize
    finalize(output_root=args.output_dir)
