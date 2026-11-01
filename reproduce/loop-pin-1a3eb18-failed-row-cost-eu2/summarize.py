"""usage: summarize.py runs.csv -> the set tables and shell counts quoted in README.md (expected-output.txt)."""
import csv,sys,statistics as S
rows=list(csv.DictReader(open(sys.argv[1])))
def f(r,k):return float(r[k])
def isrev(r):return r['cell'].startswith('kogen-review')
def show(lab,xs):
 if not xs:return
 n=len(xs);inp=sum(f(r,'input_tokens') for r in xs);ca=sum(f(r,'cached_tokens') for r in xs)
 print(f"{lab}: {n} cells, pass {sum(int(r['passed']) for r in xs)}, mean wall {S.mean(f(r,'wall_s') for r in xs):.0f} s, mean requests {S.mean(f(r,'requests') for r in xs):.1f}, mean usd {S.mean(f(r,'usd') for r in xs):.3f}, pooled cached/input {ca/inp:.3f}, model time {sum(f(r,'model_s') for r in xs)/sum(f(r,'wall_s') for r in xs):.2f} of wall, client gap {sum(f(r,'gap_s') for r in xs)/sum(f(r,'wall_s') for r in xs):.2f} of wall, gaps over 30 s {sum(int(r['gaps_over_30s']) for r in xs)}, largest gap {max(f(r,'max_gap_s') for r in xs):.1f} s")
pin=[r for r in rows if r['set']=='pin'];old=[r for r in rows if r['set']=='old']
show('pin, 12 easy kits',[r for r in pin if not isrev(r)]);show('8a2fcda base, 12 easy kits (36 cells)',[r for r in old if not isrev(r)])
show('pin, 2 review kits',[r for r in pin if isrev(r)]);show('8a2fcda base, 2 review kits (8 cells)',[r for r in old if isrev(r)])
print()
for lab,xs in (('pin',pin),):
 cmds=sum(int(r['shell_commands']) for r in xs);y=sum(int(r['shell_yielded']) for r in xs);p=sum(int(r['shell_polls']) for r in xs);po=sum(int(r['poll_only_requests']) for r in xs);rq=sum(int(r['requests']) for r in xs)
 pu=sum(f(r,'poll_only_usd') for r in xs);tu=sum(f(r,'usd') for r in xs)
 print(f"{lab}: shell commands {cmds}, still running at one second {y} ({y/cmds:.0%}), handle polls {p} ({p/(cmds+p):.0%} of shell calls), requests carrying only polls {po} of {rq} ({po/rq:.0%}), their cost {pu:.2f} of {tu:.2f} usd ({pu/tu:.0%}), their model time {sum(f(r,'poll_only_model_s') for r in xs):.0f} s of {sum(f(r,'wall_s') for r in xs):.0f} s agent wall ({sum(f(r,'poll_only_model_s') for r in xs)/sum(f(r,'wall_s') for r in xs):.0%}), polls returning the same output size as the previous snapshot {sum(int(r['poll_same_size']) for r in xs)} of {p}, most polls on one handle {max(int(r['max_polls_one_handle']) for r in xs)}, commands refused with a handle field {sum(int(r['refused_command_and_handle']) for r in xs)}")
 for r in xs:
  if isrev(r):print(f"  {r['cell']}: polls-only requests {r['poll_only_requests']} of {r['requests']}, {float(r['poll_only_usd']):.2f} of {float(r['usd']):.2f} usd, condensed {r['condensed']}, outcome {r['outcome']} pass {r['passed']}")
print(f"8a2fcda base: shell polls {sum(int(r['shell_polls']) for r in old)}, gaps over 30 s {sum(int(r['gaps_over_30s']) for r in old)}, agent_error cells {sum(1 for r in old if r['outcome']=='agent_error')}")
