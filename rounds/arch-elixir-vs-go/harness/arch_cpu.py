"""One CPU service per arm; all session/check/capture roots share its balance."""
import argparse,fcntl,json,os,selectors,signal,socket,subprocess,sys,tempfile,time,uuid,shutil,re
from pathlib import Path
from arch_budget import ArmBudget,observe
from arch_fs import safe_chmod

def _cwd_table():
    if os.path.isdir('/proc'):
        result = {}
        for name in os.listdir('/proc'):
            if not name.isdigit(): continue
            try: result[int(name)] = os.readlink('/proc/' + name + '/cwd')
            except OSError: pass
        return result
    lsof = shutil.which('lsof')
    if not lsof: raise RuntimeError('lsof is unavailable for orphan cwd cleanup')
    output = subprocess.check_output([lsof, '-nP', '-a', '-d', 'cwd', '-Fpcn'], text=True, timeout=15)
    result, current = {}, None
    for line in output.splitlines():
        if line.startswith('p') and line[1:].isdigit(): current = int(line[1:])
        elif line.startswith('n') and current is not None: result[current] = line[1:]
    return result

def kill_arm_orphans(workspace, process_rows=None, cwd_rows=None):
    """After process-group kills, SIGKILL remaining processes by cwd/argv."""
    workspace = os.path.realpath(workspace)
    if process_rows is None:
        process_rows = subprocess.check_output(['ps', '-axo', 'pid=,command='], text=True, timeout=10)
    if cwd_rows is None:
        try: cwd_rows = _cwd_table()
        except Exception as error:
            cwd_rows = {}
            errors = [dict(error='cwd scan failed: ' + str(error))]
        else:
            errors = []
    else:
        errors = []
    killed = []
    for line in process_rows.splitlines():
        parts = line.strip().split(None, 1)
        if not parts or not parts[0].isdigit(): continue
        pid = int(parts[0]); command = parts[1] if len(parts) > 1 else ''
        if pid == os.getpid(): continue
        cwd = cwd_rows.get(pid)
        by_cwd = False
        if cwd:
            cwd = os.path.realpath(cwd)
            by_cwd = cwd == workspace or workspace in Path(cwd).parents
        by_command = bool(re.search(re.escape(workspace) + r'(?:/|(?=$|[\s\'";,]))', command))
        if not (by_cwd or by_command): continue
        try:
            os.kill(pid, signal.SIGKILL)
            matched = (['cwd'] if by_cwd else []) + (['command'] if by_command else [])
            killed.append(dict(pid=pid, matched_by=matched, signal='SIGKILL'))
        except ProcessLookupError:
            continue
        except OSError as error:
            errors.append(dict(pid=pid, error=str(error)))
    return killed, errors

def call(path,request):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(3);s.connect(str(path));s.sendall((json.dumps(request)+'\n').encode())
        with s.makefile('rb') as stream:reply=json.loads(stream.readline(4000001))
    if not reply.get('ok'):raise RuntimeError(reply.get('reason','CPU supervisor failed'))
    return reply
class Supervisor:
    def __init__(self,args,observer=observe,send_signal=os.kill,clock=time.monotonic):
        self.args,self.observer,self.send_signal,self.clock=args,observer,send_signal,clock
        self.budget=ArmBudget(args.arm,args.cores,args.t0)
        self.children={};self.paused=set();self.resume_at=0.;self.stopped=False
        self.orphan_kills=[];self.orphan_cleanup_errors=[]
        self.private=Path(args.private);self.private.mkdir(parents=True,exist_ok=True)
    def signal_members(self,sig):
        rows=self.observer()
        for key,value in self.budget.members.items():
            if not value.get('active'):continue
            p=rows.get(value['pid'])
            if p and p.identity==key:
                try:self.send_signal(p.pid,sig)
                except ProcessLookupError:pass
    def tick(self):
        now=self.clock();row=self.budget.sample(self.observer(),now)
        if now>=self.args.deadline or (Path(self.args.root)/'STOP').exists() or (Path(self.args.root)/('STOP-'+self.args.arm)).exists():
            self.stop();return row
        released=False
        if self.paused and now>=max(self.resume_at,self.args.t0):
            self.signal_members(signal.SIGCONT);self.paused.clear();released=True
        # The sample above can still contain pre-epoch trampoline CPU. Do not
        # immediately undo the epoch SIGCONT with a SIGSTOP from that stale
        # overshoot: on a busy host that can keep exec starved across ticks.
        if not self.paused and row['pause_seconds']>0 and not released:
            self.signal_members(signal.SIGSTOP);self.paused=set(row['active_identities']);self.resume_at=now+row['pause_seconds']
        elif self.paused:self.signal_members(signal.SIGSTOP)
        with (self.private/'samples.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        return row
    def register(self,pid,role):
        if self.stopped:raise RuntimeError('arm stopped; no new consumers')
        process=self.observer().get(pid)
        if not process or 'T' not in process.state:raise RuntimeError('root must be stopped before task release')
        self.budget.register(process,role,self.args.arm)
        if self.paused or self.clock()<self.args.t0:
            self.paused.add(process.identity);self.resume_at=max(self.resume_at,self.args.t0)
        else:self.send_signal(pid,signal.SIGCONT)
        return process.identity
    def request(self,value):
        if value.get('arm')!=self.args.arm:raise ValueError('wrong arm supervisor')
        op=value['operation']
        if op=='register':return {'identity':self.register(int(value['pid']),value['role'])}
        if op=='launch':
            if self.stopped or self.clock()>=self.args.deadline:raise RuntimeError('arm stopped/deadline')
            handle=uuid.uuid4().hex;path=self.private/handle;path.mkdir()
            trampoline='import os,signal,sys;os.kill(os.getpid(),signal.SIGSTOP);os.execvpe(sys.argv[1],sys.argv[1:],os.environ)'
            with tempfile.TemporaryFile(dir=path) as inp,(path/'stdout').open('wb') as out,(path/'stderr').open('wb') as err:
                inp.write(value.get('stdin','').encode());inp.seek(0)
                proc=subprocess.Popen([sys.executable,'-c',trampoline,*value['argv']],cwd=value['cwd'],env=value.get('env'),stdin=inp,stdout=out,stderr=err,start_new_session=True)
            self.children[handle]=proc;until=self.clock()+2
            while self.clock()<until:
                row=self.observer().get(proc.pid)
                if row and 'T' in row.state:break
                if proc.poll() is not None:raise RuntimeError('consumer exited before registration')
                time.sleep(.005)
            try:identity=self.register(proc.pid,value['role'])
            except BaseException:
                try:os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                proc.wait();raise
            return {'handle':handle,'pid':proc.pid,'identity':identity,'output':str(path)}
        if op=='poll':return {'exit_code':self.children[value['handle']].poll()}
        if op=='status':return self.budget.report()
        if op=='stop':self.stop();return {'stopped':True}
        raise ValueError('unknown CPU operation')
    def stop(self):
        self.stopped=True
        try:
            self.budget.sample(self.observer(),self.clock());self.signal_members(signal.SIGKILL)
        except Exception as error:
            self.budget.gaps.append({'reason':'membership observation failed during stop: '+str(error)})
            # Owned Popen roots cannot be PID-reused before wait; halt them even when ps fails.
            for proc in self.children.values():
                if proc.poll() is None:
                    try:os.killpg(proc.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
        self.paused.clear()
        for proc in self.children.values():
            try:proc.wait(timeout=2)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
        try:
            self.orphan_kills,self.orphan_cleanup_errors=kill_arm_orphans(Path(self.args.root)/self.args.arm)
        except Exception as error:
            self.orphan_cleanup_errors.append(dict(error=str(error)))
        accounting=self.budget.report()
        accounting.update(orphan_kills=self.orphan_kills,orphan_cleanup_errors=self.orphan_cleanup_errors)
        (self.private/'accounting.json').write_text(json.dumps(accounting,indent=2)+'\n')
def serve(args):
    private=Path(args.private);private.mkdir(parents=True,exist_ok=True);safe_chmod(args.root,private,0o700)
    with (private/'supervisor.lock').open('a') as lease:
        fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
        service=Supervisor(args);path=Path(args.socket)
        if path.exists():raise RuntimeError('CPU socket exists; inspect prior service')
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as server:
            server.bind(str(path));safe_chmod(args.root,path,0o600);server.listen();server.setblocking(False)
            selector=selectors.DefaultSelector();selector.register(server,selectors.EVENT_READ)
            def shutdown(*_):service.stopped=True
            for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,shutdown)
            try:
                while not service.stopped:
                    service.tick()
                    for key,_ in selector.select(.2):
                        conn,_=server.accept()
                        with conn:
                            conn.settimeout(2)
                            try:
                                with conn.makefile('rb') as stream:req=json.loads(stream.readline(4000001))
                                reply={'ok':True,**service.request(req)}
                            except Exception as error:reply={'ok':False,'reason':str(error)}
                            conn.sendall((json.dumps(reply)+'\n').encode())
            finally:service.stop();path.unlink(missing_ok=True);selector.close()
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='mode',required=True)
    s=sub.add_parser('serve')
    for name in ('arm','socket','private','root'):s.add_argument('--'+name,required=True)
    for name in ('t0','deadline','cores'):s.add_argument('--'+name,type=float,required=True)
    c=sub.add_parser('request');c.add_argument('--socket',required=True);c.add_argument('--json',required=True)
    a=p.parse_args()
    if a.mode=='serve':serve(a)
    else:print(json.dumps(call(a.socket,json.loads(a.json))))
