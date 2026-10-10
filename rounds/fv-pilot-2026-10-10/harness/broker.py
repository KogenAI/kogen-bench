"""Root-owned sequential broker; execution programs exist only in worker view."""
import json, os, pathlib, re, secrets, shutil, socket, subprocess, threading, time
from common import BUILD, append, attested, clean_workspace, integrity_changes, isolated, manifest, own, utc
class Broker:
    def __init__(self,trial,runtime,package,out,cap):
        self.trial,self.runtime,self.package,self.out,self.cap=trial,runtime,package,out,cap
        self.count=0; self.started=0; self.refused=0; self.cap_at=None; self.child=None; self.stopping=False
        self.arm=json.loads((package/'package.json').read_text())['arm']
        self.toy=json.loads((package/'package.json').read_text())['task'].startswith('TOY-')
        self.trusted=out/'broker-trusted'; self.trusted.mkdir(parents=True)
        bridge=package/'bridge' if (package/'bridge').exists() else BUILD/'bridge'
        shutil.copytree(bridge,self.trusted/'build/bridge')
        if not (self.trusted/'build/bridge/shared').exists() and (BUILD/'bridge/shared').exists(): shutil.copytree(BUILD/'bridge/shared',self.trusted/'build/bridge/shared')
        if self.toy: shutil.copytree(package/'backend',self.trusted/'build/toy-backend')
        h=pathlib.Path(__file__).parent; (self.trusted/'harness').mkdir()
        for name in ['common.py','grading_stage.py','tests.exs','api.exs']: shutil.copyfile(h/name,self.trusted/'harness'/name)
        control=trial/'.fv-control'; control.mkdir(mode=0o755)
        self.sock=socket.socket(socket.AF_UNIX); self.sock.bind(str(control/'check.sock')); (control/'check.sock').chmod(0o666); self.sock.listen(8); self.sock.settimeout(.1)
        self.thread=threading.Thread(target=self.serve,daemon=True); self.thread.start()
        # Codex's network-disabled seccomp denies connect(), including AF_UNIX.
        # A filesystem transport forwards requests to the SAME counted handler.
        # Directory descriptors prevent agent renames/symlinks redirecting root writes.
        replies=control/'replies'; replies.mkdir(mode=0o755); replies.chmod(0o755)
        self.reply_fd=os.open(replies,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        self.fifo_path=control/'requests.fifo'; os.mkfifo(self.fifo_path,0o666); self.fifo_path.chmod(0o666)
        self.fifo_fd=os.open(self.fifo_path,os.O_RDWR|os.O_NONBLOCK)
        self.file_thread=threading.Thread(target=self.file_transport,daemon=True); self.file_thread.start()
    def file_transport(self):
        pending=b''
        while not self.stopping:
            try: chunk=os.read(self.fifo_fd,4096)
            except BlockingIOError: time.sleep(.02); continue
            except OSError: break
            pending+=chunk
            if len(pending)>16384: pending=b''; continue
            while b'\n' in pending:
                line,pending=pending.split(b'\n',1)
                try:
                    request=json.loads(line); ident=request.get('id','')
                    if not re.fullmatch(r'[0-9a-f]{32}',ident) or request.get('action')!='check': continue
                    fd=os.open(ident+'.jsonl',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644,dir_fd=self.reply_fd)
                    os.fchmod(fd,0o644)
                    with os.fdopen(fd,'wb',buffering=0) as reply, socket.socket(socket.AF_UNIX) as relay:
                        relay.connect(str(self.trial/'.fv-control/check.sock')); relay.sendall(b'{"action":"check"}\n')
                        for record in relay.makefile('rb'): reply.write(record)
                except (OSError,ValueError,TypeError): continue
    def serve(self):
        while not self.stopping:
            try: c,_=self.sock.accept()
            except socket.timeout: continue
            except OSError: break
            with c:
                c.settimeout(1)
                try:
                    if json.loads(c.recv(4096)).get('action')!='check': continue
                    if self.started>=self.cap:
                        self.refused+=1; append(self.out/'fv.jsonl',{'type':'refused','cycle':self.count+1,'time':utc()})
                        c.sendall((json.dumps({'summary':{'exit_code':75,'cap':'cycles','cycle':self.count+1,'complete':False}})+'\n').encode()); continue
                    self.started+=1; start=time.monotonic(); index=self.count+1
                    append(self.out/'fv.jsonl',{'type':'started','cycle':index,'time':utc()})
                    codes={}; work=self.out/f'worker-{index}'; changed=integrity_changes(self.trial,self.package)
                    if not changed:
                        clean_workspace(self.trial,self.package,work); own(work)
                    for name in ['regenerate','check','starter']:
                        if self.stopping: break
                        logfile=self.out/f'fv-{index}-{name}.log'; nonce=secrets.token_hex(16)
                        if changed or (name!='regenerate' and codes.get('regenerate')):
                            codes[name]=2; logfile.write_text('FV-ERROR frozen inputs changed or regeneration incomplete: '+', '.join(changed)+'\n')
                        else:
                            cmd=['python3','/fv-grade/harness/grading_stage.py','broker:'+name,self.arm,str(work),nonce]
                            with logfile.open('wb') as f:
                                self.child=subprocess.Popen(isolated(work,self.runtime,cmd,network=False,extra_ro=[(self.trusted/'build','/fv-grade/build'),(self.trusted/'harness','/fv-grade/harness')]),stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
                                try: codes[name]=self.child.wait(timeout=900)
                                except subprocess.TimeoutExpired: os.killpg(self.child.pid,9); self.child.wait(); codes[name]=124
                                self.child=None
                            if codes[name] in {0,1} and not attested(logfile.read_text(errors='replace'),nonce,'broker:'+name): codes[name]=2
                        # A disconnected or non-reading client cannot abandon an
                        # admitted cycle and obtain uncounted execution.
                        try: c.sendall((json.dumps({'output':logfile.read_text(errors='replace')})+'\n').encode())
                        except (OSError,socket.timeout): pass
                    if len(codes)!=3: continue
                    # Formal sources remain readable, but compiled/cache/run artifacts stay private.
                    if (work/'verification').exists():
                        for file in ['Implementation.lean','app.qnt','ir.json','source-map.json']:
                            if (work/'verification'/file).is_file():
                                dst=self.trial/'verification'/file
                                if not dst.is_symlink(): shutil.copyfile(work/'verification'/file,dst); os.chown(dst,1001,1001)
                    self.count+=1
                    exit_code=2 if any(x not in {0,1} for x in codes.values()) else (1 if any(codes.values()) else 0)
                    summary={'cycle':self.count,'complete':True,'exit_code':exit_code,'checks':codes,'wall_seconds':time.monotonic()-start}
                    append(self.out/'fv.jsonl',{'type':'completed','time':utc(),**summary})
                    if self.count>=self.cap: self.cap_at=time.monotonic()
                    c.sendall((json.dumps({'summary':summary})+'\n').encode())
                except (BrokenPipeError,ConnectionError,socket.timeout,json.JSONDecodeError): pass
                except Exception as exc:
                    append(self.out/'fv.jsonl',{'type':'broker_error','error':str(exc),'time':utc()})
                    try: c.sendall((json.dumps({'summary':{'exit_code':2,'complete':False,'error':str(exc)}})+'\n').encode())
                    except OSError: pass
    def close(self):
        self.stopping=True
        if self.child:
            try: os.killpg(self.child.pid,9)
            except ProcessLookupError: pass
        self.sock.close(); self.thread.join(3)
        os.close(self.fifo_fd); self.file_thread.join(3); os.close(self.reply_fd)
