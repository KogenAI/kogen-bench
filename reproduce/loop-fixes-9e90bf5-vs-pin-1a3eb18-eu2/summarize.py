"""usage: summarize.py runs.csv -> the paired tables quoted in README.md (expected-output.txt). Arms: set 'pin' (loop 1a3eb18) and 'main' (loop 9e90bf5)."""
import csv,sys,statistics as S
rows=list(csv.DictReader(open(sys.argv[1])))
def f(r,k):return float(r[k])
A={a:{r['cell'].rsplit('/',1)[0]:r for r in rows if r['set']==a} for a in('pin','main')}
cells=list(A['pin'])
def tot(a,k):return sum(f(A[a][c],k) for c in cells)
print('cells',len(cells),'per arm')
print('%-24s %5s %5s %7s %7s %6s %6s %7s %7s %7s %7s'%('task','pass_p','pass_m','po_req_p','po_req_m','po$_p','po$_m','req_p','req_m','wall_p','wall_m'))
more=0
for c in cells:
    p,m=A['pin'][c],A['main'][c]
    more+=int(f(m,'poll_only_requests')>f(p,'poll_only_requests'))
    print('%-24s %5s %5s %7d %7d %6.3f %6.3f %7d %7d %7.0f %7.0f'%(c.split('/')[0],p['passed'],m['passed'],f(p,'poll_only_requests'),f(m,'poll_only_requests'),f(p,'poll_only_usd'),f(m,'poll_only_usd'),f(p,'requests'),f(m,'requests'),f(p,'wall_s'),f(m,'wall_s')))
print()
for a in('pin','main'):
    po=tot(a,'poll_only_requests');rq=tot(a,'requests');pu=tot(a,'poll_only_usd');u=tot(a,'usd')
    print(f"{a}: pass {int(tot(a,'passed'))}/{len(cells)}, requests {rq:.0f}, poll-only requests {po:.0f} ({po/rq:.0%}), poll-only usd {pu:.3f} of {u:.3f} ({pu/u:.0%}), poll-only model s {tot(a,'poll_only_model_s'):.0f} of wall {tot(a,'wall_s'):.0f}, shell commands {tot(a,'shell_commands'):.0f}, yielded {tot(a,'shell_yielded'):.0f}, handle polls {tot(a,'shell_polls'):.0f} ({tot(a,'shell_polls')/tot(a,'shell_commands'):.2f} per command), refused {tot(a,'refused_command_and_handle'):.0f}, mean wall {tot(a,'wall_s')/len(cells):.0f}, total usd {u:.3f}")
p0,m0=tot('pin','poll_only_requests'),tot('main','poll_only_requests');p1,m1=tot('pin','poll_only_usd'),tot('main','poll_only_usd')
print(f"poll-only requests change {m0/p0-1:+.0%}, poll-only usd change {m1/p1-1:+.0%}, tasks with more poll-only requests on main {more} of {len(cells)}")
print('hidden pass: tasks passing on pin and failing on main:',[c for c in cells if A['pin'][c]['passed']=='1' and A['main'][c]['passed']=='0'])
print('total usd change %+.1f%%, wall change %+.1f%%, requests change %+.1f%%'%((tot('main','usd')/tot('pin','usd')-1)*100,(tot('main','wall_s')/tot('pin','wall_s')-1)*100,(tot('main','requests')/tot('pin','requests')-1)*100))
