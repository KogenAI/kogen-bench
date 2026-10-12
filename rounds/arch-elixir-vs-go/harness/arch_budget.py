"""Sampled arm-wide membership; retain observed descendants across reparenting.

Between-sample children and final CPU tails remain explicit accounting gaps.
This is not kernel-complete process membership or an access boundary.
"""
import dataclasses,subprocess
@dataclasses.dataclass(frozen=True)
class Process:
    pid:int
    parent:int
    group:int
    cpu:float
    state:str
    started:str
    @property
    def identity(self):return str(self.pid)+'@'+self.started
def cpu_time(value):
    days=0
    if '-' in value:prefix,value=value.split('-',1);days=int(prefix)
    total=0.
    for part in value.split(':'):total=total*60+float(part)
    return days*86400+total
def parse_ps(text):
    rows={}
    for line in text.splitlines():
        if not line.strip():continue
        pid,parent,group,cpu,state,started=line.strip().split(None,5)
        p=Process(int(pid),int(parent),int(group),cpu_time(cpu),state,started);rows[p.pid]=p
    return rows
def observe():
    return parse_ps(subprocess.check_output(['ps','-axo','pid=,ppid=,pgid=,time=,stat=,lstart='],text=True,timeout=2))
class ArmBudget:
    def __init__(self,arm,cores,t0,interval=.2):
        if cores not in (2.5,3.0) or interval!=.2:raise ValueError('unfrozen arm CPU parameters')
        self.arm,self.cores,self.t0,self.interval=arm,cores,t0,interval
        self.roots={};self.members={};self.gaps=[];self.ambiguous=set();self.last=float('-inf');self.max_overshoot=0.
    def register(self,process,role,arm):
        if arm!=self.arm or process.identity in self.roots:raise ValueError('wrong/duplicate root')
        self.roots[process.identity]=role
        self.members[process.identity]={'pid':process.pid,'role':role,'cpu':process.cpu,'active':True}
    def sample(self,rows,at):
        if at<self.last:raise ValueError('non-monotonic CPU sample')
        live={p.identity:p for p in rows.values()}
        # macOS lstart is only second-resolution. A quickly reused PID can
        # therefore keep the same textual identity while its CPU counter drops.
        # Retire that ambiguous identity instead of crashing supervision or
        # attributing/signalling the new process as the old arm member.
        for key,p in list(live.items()):
            prior=self.members.get(key)
            if key in self.ambiguous:
                live.pop(key,None)
            elif prior and p.cpu<prior['cpu']:
                prior['active']=False;self.roots.pop(key,None);self.ambiguous.add(key);live.pop(key,None)
                self.gaps.append({'identity':key,'reason':'PID identity reused within lstart resolution; new process not attributed',
                                  'last_known_cpu_seconds':prior['cpu'],'observed_cpu_seconds':p.cpu})
        assigned={k:self.roots[k] for k in self.roots if k in live}
        assigned.update({k:v['role'] for k,v in self.members.items() if k in live})
        while True:
            added=False
            for p in rows.values():
                if p.identity not in live:continue
                parent=rows.get(p.parent)
                if p.identity not in assigned and parent and parent.identity in assigned and parent.identity in live:
                    assigned[p.identity]=assigned[parent.identity];added=True
            if not added:break
        for key,role in assigned.items():
            p=live[key];prior=self.members.get(key)
            if prior and p.cpu<prior['cpu']:raise RuntimeError('CPU counter reset or PID identity collision')
            self.members[key]={'pid':p.pid,'role':role,'cpu':p.cpu,'active':True}
        for key,value in self.members.items():
            if key not in live and value['active']:
                value['active']=False
                self.gaps.append({'identity':key,'reason':'process exited without kernel final CPU sample','last_known_cpu_seconds':value['cpu']})
        total=sum(m['cpu'] for m in self.members.values())
        overshoot=max(0.,total-self.cores*max(0.,at-self.t0));self.max_overshoot=max(self.max_overshoot,overshoot)
        self.last=at
        return {'arm':self.arm,'at':at,'measured_cpu_seconds':total,'overshoot_cpu_seconds':overshoot,
                'pause_seconds':min(.8,overshoot/self.cores),'active_pids':sorted(live[k].pid for k in assigned),
                'active_identities':sorted(assigned),'registered_sessions':len(self.roots)}
    def report(self):
        return {'arm':self.arm,'cores':self.cores,'interval_seconds':self.interval,
                'measured_cpu_seconds_lower_bound':sum(m['cpu'] for m in self.members.values()),
                'exact_cpu_seconds':None,'max_measured_overshoot_cpu_seconds':self.max_overshoot,
                'members':self.members,'attribution_gaps':self.gaps,
                'coverage':'sampled retained process trees; between-sample children/escapes may be unobserved',
                'kernel_complete_membership':False}
