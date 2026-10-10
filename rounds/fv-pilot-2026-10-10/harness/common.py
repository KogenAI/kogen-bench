"""Root-side utilities. No third-party Python dependencies."""
import hashlib, json, os, pathlib, pwd, subprocess, time
BASE = pathlib.Path(os.environ.get('FV_ROOT', '/opt/fv'))
BUILD = BASE / 'build'
CODEX = '/opt/bench/tools/bin/codex'
TOKEN_POLICY = 'uncached-v1-2026-10-10'
TOKEN_DEFINITION = '(input_tokens - cached_input_tokens) + output_tokens; reasoning_output_tokens already included in output_tokens (Codex 0.161.0)'
PATH = '/opt/fv-tools/bin:/opt/fv-tools/elan/bin:/opt/bench/tools/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/usr/local/bin:/usr/bin:/bin'
COMMON_PROMPT = 'Identify the violated property and causal function, explaining your evidence before patching. Repair the application to satisfy the fixed contract and preserve its API. Keep accepted laws and assumptions unchanged. Regenerate formal representations from the changed application and run the supplied checks. If verification fails because of a proof or tooling limitation, distinguish that from an implementation defect. Submit the patch and verification results within the budget.'
def utc(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def safe_files(root):
    root = pathlib.Path(root)
    for p in sorted(root.rglob('*')):
        if p.relative_to(root).parts[0]=='.fv-control': continue
        if p.is_symlink(): raise ValueError(f'symlink forbidden: {p}')
        if p.is_file(): yield p
        elif not p.is_dir(): raise ValueError(f'special file forbidden: {p}')
def manifest(root): return {str(p.relative_to(root)): sha(p) for p in safe_files(root) if p.name != 'PACKAGE.sha256'}
def tree_version():
    root = pathlib.Path(__file__).parent
    # Git blob and tree object IDs, without modifying R or requiring a commit/identity.
    def obj(kind, data): return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
    def tree(d):
        entries=[]
        for p in sorted(d.iterdir(), key=lambda p:p.name+('/' if p.is_dir() else '')):
            if p.name in {'__pycache__', '.git'}: continue
            mode='40000' if p.is_dir() else ('100755' if p.stat().st_mode & 0o111 else '100644')
            digest=tree(p) if p.is_dir() else obj('blob',p.read_bytes())
            entries.append(mode.encode()+b' '+p.name.encode()+b'\0'+digest)
        return obj('tree',b''.join(entries))
    return tree(root).hex()
def env(runtime=None):
    e={'HOME':'/opt/fv-home','CODEX_HOME':'/opt/fv-runtime','PATH':PATH,'ELAN_HOME':'/opt/fv-tools/elan','MISE_DATA_DIR':'/opt/fv-tools/mise','MISE_CONFIG_DIR':'/opt/fv-tools/mise-config','ERL_FLAGS':'+S 2:2','HEX_OFFLINE':'1','MIX_ENV':'test','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
    if runtime: e['TMPDIR']='/tmp'
    return e
def isolated(trial, runtime, command, network=True, codex_home=False, extra_ro=(), view='checker', selected_home='/opt/fv-runtime'):
    """Private mount/PID view. Codex applies its own network sandbox to agent commands."""
    trial, runtime = str(trial), str(runtime)
    visible=trial if trial.startswith('/opt/fv-trials/') else '/opt/fv-trials/grade-work'
    command=[arg.replace(trial,visible) for arg in command]
    b=['/usr/bin/bwrap','--die-with-parent','--unshare-pid','--unshare-ipc','--unshare-uts','--new-session']
    if not network: b += ['--unshare-net']
    for directory in ['/home','/opt/fv-home','/opt/fv-trials','/opt','/opt/bench','/opt/bench/mise','/fv-grade']:
        b += ['--perms','0755','--dir',directory]
    paths=['/usr','/bin','/sbin','/lib','/lib64','/etc']
    if view=='checker': paths+=['/opt/bench/tools','/opt/bench/mise/installs','/opt/fv-tools']
    elif view!='agent': raise ValueError('unknown execution view')
    for path in paths:
        if os.path.exists(path): b += ['--ro-bind',path,path]
    if view=='agent':
        # The supplied stages and all alternate installed native tool paths are
        # absent. System installations are masked as well as the pinned tools.
        for path in ['/usr/lib/erlang','/usr/lib/elixir','/usr/lib/jvm','/usr/share/nodejs','/usr/local']:
            if os.path.isdir(path): b += ['--tmpfs',path]
        denied=pathlib.Path(runtime)/'execution-denied'; denied.touch(exist_ok=True); denied.chmod(0)
        for name in ['mix','elixir','erl','erlc','escript','node','nodejs','npm','npx','java','javac','lean','lake','elan','quint']:
            path='/usr/bin/'+name
            if os.path.exists(path): b += ['--ro-bind',str(denied),path]
        if codex_home:
            # Pinned Codex needs its sibling tool host and vendor resources.
            # This tree contains only Codex; checker toolchains remain absent.
            b += ['--ro-bind','/opt/bench/tools','/opt/bench/tools']
    b += ['--proc','/proc','--dev','/dev','--perms','1777','--tmpfs','/tmp','--dir','/root','--dir','/opt/fv-home','--dir','/opt/fv-trials','--bind',trial,visible,'--bind',runtime,'/fv-runtime']
    if view=='agent':
        for name in ['bridge','backend']:
            if (pathlib.Path(trial)/name).is_dir(): b += ['--tmpfs',visible+'/'+name]
    if codex_home:
        # No credential copy, inspection, decoding or host configuration mutation.
        # Only Codex reads the existing credential through a read-only bind mount.
        fresh=pathlib.Path(runtime)/'codex-home'; fresh.mkdir(exist_ok=True)
        os.chown(fresh,1001,1001)
        b += ['--bind',str(fresh),'/opt/fv-runtime',
              '--ro-bind',selected_home+'/auth.json','/opt/fv-runtime/auth.json',
              '--bind',runtime+'/sessions','/opt/fv-runtime/sessions']
    for src,dst in extra_ro: b += ['--ro-bind',str(src),str(dst)]
    b += ['--chdir',visible,'--clearenv']
    for k,v in env(runtime).items(): b += ['--setenv',k,v]
    return b + ['--','/usr/sbin/runuser','-u','bench','--preserve-environment','--','nice','-n','10',*command]
def append(path, row):
    import fcntl
    path=pathlib.Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX); f.write(json.dumps(row,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
def own(path):
    p=pathlib.Path(path); os.chown(p,1001,1001)
    for x in p.rglob('*'): os.chown(x,1001,1001)
def account(selected_home='/opt/fv-runtime'):
    # Official Codex JSON protocol; never parse credentials or JWTs.
    import selectors
    settings=env(); settings['CODEX_HOME']=selected_home
    p=subprocess.Popen(['runuser','-u','bench','--','env','-i',*[k+'='+v for k,v in settings.items()],CODEX,'app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,bufsize=0)
    def send(x): p.stdin.write((json.dumps(x)+'\n').encode()); p.stdin.flush()
    send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'fv-harness','version':'1'},'capabilities':{'experimentalApi':True}}})
    sel=selectors.DefaultSelector(); sel.register(p.stdout,selectors.EVENT_READ); end=time.monotonic()+15; pending=b''
    try:
        while time.monotonic()<end:
            for key,_ in sel.select(.2):
                chunk=os.read(key.fileobj.fileno(),1048576)
                if not chunk: raise RuntimeError('account probe closed')
                pending+=chunk
                while b'\n' in pending:
                    line,pending=pending.split(b'\n',1); x=json.loads(line)
                    if x.get('id')==1:
                        send({'method':'initialized'}); send({'id':2,'method':'account/read','params':{'refreshToken':False}})
                    if x.get('id')==2:
                        a=x.get('result',{}).get('account') or {}
                        return {'email':a.get('email'),'type':a.get('type'),'source':'codex app-server account/read'}
        raise RuntimeError('account probe timed out')
    finally:
        p.terminate()
        try: p.wait(2)
        except subprocess.TimeoutExpired: p.kill(); p.wait()

# Candidate data selection is shared by feedback and final grading.
def integrity_changes(candidate,package):
    current=manifest(candidate); original=manifest(package)
    generated={'verification/Implementation.lean','verification/app.qnt','verification/ir.json','verification/source-map.json'}
    frozen=[k for k in original if not k.startswith('app/lib/') and k not in generated and k!='PACKAGE.sha256']
    changed=[k for k in frozen if current.get(k)!=original[k]]
    toy=json.loads((package/'package.json').read_text())['task'].startswith('TOY-')
    suffix='.py' if toy else '.ex'
    for k in current:
        path=candidate/k
        if k.startswith('app/') and k not in original and not (k.startswith('app/lib/') and k.endswith(suffix)): changed.append(k)
        if k not in original and (path.stat().st_mode&0o111 or path.suffix in {'.exs','.config','.toml'}): changed.append(k)
        if k.startswith('app/lib/') and (not k.endswith(suffix) or path.stat().st_mode&0o111): changed.append(k)
    return sorted(set(changed))
def clean_workspace(candidate,package,work):
    import shutil, stat
    work.mkdir(parents=True)
    for name in ['app','verification']:
        if (package/name).exists(): shutil.copytree(package/name,work/name)
    shutil.rmtree(work/'app/lib'); (work/'app/lib').mkdir()
    # Directory descriptors and O_NOFOLLOW prevent a racing agent from making
    # root follow source symlinks into sealed or unrelated host trees.
    flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
    def copy_dir(fd,dest):
        for entry in os.scandir(fd):
            if entry.is_dir(follow_symlinks=False):
                child=os.open(entry.name,flags,dir_fd=fd)
                try:
                    target=dest/entry.name; target.mkdir(); copy_dir(child,target)
                finally: os.close(child)
            else:
                child=os.open(entry.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
                try:
                    mode=os.fstat(child).st_mode
                    if not stat.S_ISREG(mode) or mode&0o111: raise ValueError('unsafe source file')
                    with os.fdopen(os.dup(child),'rb') as src, (dest/entry.name).open('wb') as dst: shutil.copyfileobj(src,dst)
                finally: os.close(child)
    opened=[]
    try:
        fd=os.open(candidate,flags); opened.append(fd)
        for part in ['app','lib']:
            fd=os.open(part,flags,dir_fd=fd); opened.append(fd)
        copy_dir(fd,work/'app/lib')
    finally:
        for fd in reversed(opened): os.close(fd)
    for name in ['laws.json','public-api.json','fixed.sha256','package.json']:
        if (package/name).exists(): shutil.copyfile(package/name,work/name)
def validate_ir(ir,api,require_exports=True):
    exports={f['name']+'/'+str(len(f['params'])) for m in ir['modules'] if m['name']==api['module'] for f in m['functions'] if f['visibility']=='public'}
    missing=sorted(set(api['functions'])-exports)
    if require_exports and missing: raise ValueError('required source exports removed: '+', '.join(missing))
    functions={(m['name'],f['name'],len(f['params'])) for m in ir['modules'] for f in m['functions']}
    def walk(node,module):
        if isinstance(node,dict):
            if node.get('kind')=='call':
                target=(node.get('module') or module,node['name'],len(node['args']))
                if target not in functions and target not in {('Map','get',3),('Map','has_key?',2)}: raise ValueError('untrusted external call: '+str(target))
            for v in node.values(): walk(v,module)
        elif isinstance(node,list):
            for v in node: walk(v,module)
    for m in ir['modules']: walk(m,m['name'])
    return sorted(exports)
def attested(text,nonce,stage):
    records=[]
    for line in text.splitlines():
        if line.startswith('FV_ATTEST '):
            try: records.append(json.loads(line[10:]))
            except ValueError: pass
    return any(x=={'nonce':nonce,'stage':stage,'complete':True} for x in records)
