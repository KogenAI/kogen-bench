#!/usr/bin/env python3
"""Close inaccessible scan subtrees conservatively, without reading their contents."""
import errno,glob,json,os,re,stat
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def finalize(root=ROOT,output_root=None):
    root=Path(root);dest=Path(output_root or root);p=dest/'hidden-inventory.json';d=json.loads(p.read_text());entries={e['path']:e for e in d['found']}
    unresolved=[];notes=list(d.get('scan_notes',[]));outside=list(d.get('outside_reach',[]))
    for error in d['errors']:
        match=re.search(r": '(.+)'$",error)
        if not match:unresolved.append(error);continue
        path=Path(match[1])
        if '[Errno 2]' in error and not path.exists():notes.append('Absent/dangling path has no readable contents: '+str(path));continue
        try:metadata=path.stat()
        except OSError:unresolved.append(error);continue
        directory=stat.S_ISDIR(metadata.st_mode)
        entries[str(path)]={'path':str(path),'reason':'inaccessible scan subtree; conservatively protected as potential suite','protect':str(path),'directory':directory}
        if metadata.st_mode&0o777==0 or (metadata.st_uid!=os.getuid() and not os.access(path,os.R_OK|os.X_OK)):
            outside.append(str(path));notes.append(f'Already outside user reach: {path}; uid={metadata.st_uid} mode={metadata.st_mode&0o7777:o}; leave unchanged')
        else:
            notes.append(f'Contents could not be enumerated here: {path}; entire root must be locked and denied by live arm probe')
    for name in glob.glob('/tmp/kc*'):
        path=Path(name).resolve()
        entries[str(path)]={'path':str(path),'reason':'/tmp/kc* start-time protection (whether or not a suite is currently present)','protect':str(path),'directory':path.is_dir()}
    # Complete the scan of regular files immediately in HOME; the deep walker scanned its directories.
    from hidden_inventory import digest,protected
    if (root/'hidden-case-hashes.json').exists():hashes={int(size):set(values) for size,values in json.loads((root/'hidden-case-hashes.json').read_text()).items()}
    else:
        hashes={}
        for q in (root/'inputs/conformance/cases').rglob('*'):
            if q.is_file():hashes.setdefault(q.stat().st_size,set()).add(digest(q))
    home=Path(d['home'])
    for q in home.iterdir():
        if protected(q) or q.is_dir() or not q.is_file():continue
        if q.is_symlink() and protected(q.resolve()):continue
        if q.stat().st_size in hashes and digest(q) in hashes[q.stat().st_size]:
            entries[str(q)]={'path':str(q),'reason':'frozen suite case content hash at HOME root','protect':str(q),'directory':False}
    d['found']=list(sorted(entries.values(),key=lambda e:e['path']))
    d['locks']=sorted({e['protect'] for e in d['found']})
    d['lock_types']={name:('directory' if Path(name).is_dir() else 'file') for name in d['locks']}
    for e in d['found']:
        if 'directory' not in e:e['directory']='cases/quint directory' in e['reason'] or 'symlink' in e['reason']
    d['outside_reach']=sorted(outside);d['scan_notes']=notes;d['scan_errors_original']=d['errors'];d['errors']=unresolved
    p.write_text(json.dumps(d,indent=2)+'\n')
    text=f"HIDDEN SUITE INVENTORY: {len(d['found'])} discoveries/potential-suite roots; {len(d['locks'])} protection roots; {len(outside)} already outside reach\n{d['excluded']}\n"
    text+='Protection: chmod 000 at the listed root; pre-existing inaccessible roots are left unchanged and live-probed. Linux wave suite: benchadmin:0700 until FINAL and process exit.\n'
    text+='Own inputs/conformance AND inputs-placeholder/conformance are locked; /tmp/kc* is rechecked at each wave start.\n'
    text+=''.join(f"{e['path']}\t{e['protect']}\t{('already outside reach; leave unchanged' if e['protect'] in outside else 'lock 000')}\t{e['reason']}\n" for e in d['found'])
    text+='SCAN DISCLOSURES:\n'+'\n'.join(notes)+'\nUNRESOLVED ERRORS:\n'+'\n'.join(unresolved)+'\n'
    (dest/'HIDDEN-SUITE-INVENTORY.txt').write_text(text)
    print(f"PASS inventory closure: entries={len(d['found'])} roots={len(d['locks'])} outside={len(outside)} unresolved={len(unresolved)}")
    return d
if __name__=='__main__':finalize()
