import csv,sys,statistics as st,collections
rows=list(csv.DictReader(open(sys.argv[1]+"/cells.tsv"),delimiter='\t'))
L=['a0','retry1','retry5']
N=lambda r,k:float(r[k])
print("1. Per lane (48 cells each: 8 tasks x 6 repetitions; 'valid' = accepted Intent that was graded)")
print("lane     valid  no-Intent scenarios pass_on_ref fail_on_start wrong_caught/total requests wall_s cost_usd")
for l in L:
    x=[r for r in rows if r['lane']==l]; v=[r for r in x if r['valid_intent']=='1']
    s=lambda k,z:int(sum(N(r,k) for r in z))
    print("%-8s %2d/%d  %9d %9d %11d %13d %8d/%-8d %8d %6d %8.2f"%(l,len(v),len(x),len(x)-len(v),s('scenarios',v),s('pass_on_reference',v),s('fail_on_start',v),s('wrong_caught',v),s('wrong_total',v),s('requests',x),round(sum(N(r,'wall_s') for r in x)),sum(N(r,'cost_usd') for r in x)))
print()
print("2. Outcome per lane (all cells, including those with no accepted Intent)")
for l in L: print(l,dict(sorted(collections.Counter(r['outcome'] for r in rows if r['lane']==l).items())))
print()
print("3. Valid Intents per task (of 6 repetitions)")
print("task  a0 retry1 retry5")
for t in sorted({r['task'] for r in rows}):
    print("%-4s"%t,*["%3d"%sum(r['valid_intent']=='1' for r in rows if r['task']==t and r['lane']==l) for l in L])
print()
print("4. Same task and repetition as a0 (wall and requests include refused or questioning attempts)")
k={(r['task'],r['rep'],r['lane']):r for r in rows}
for l in ['retry1','retry5']:
    keys=sorted({(r['task'],r['rep']) for r in rows})
    c=collections.Counter(); d=collections.defaultdict(list)
    for t,rep in keys:
        a,b=k[(t,rep,'a0')],k[(t,rep,l)]; va,vb=a['valid_intent']=='1',b['valid_intent']=='1'
        c[(va,vb)]+=1
        if va and vb:
            for m in ['wall_s','requests','cost_usd']: d[m].append(N(b,m)-N(a,m))
            d['por'].append(N(b,'pass_on_reference')/max(N(b,'scenarios'),1)-N(a,'pass_on_reference')/max(N(a,'scenarios'),1))
    print("%s: both valid %d, a0 only %d, %s only %d, neither %d"%(l,c[(True,True)],c[(True,False)],l,c[(False,True)],c[(False,False)]))
    print("   on the %d both-valid pairs, mean change vs a0: wall %+.1f s, requests %+.2f, cost %+.4f USD, pass_on_reference rate %+.4f"%(len(d['wall_s']),st.mean(d['wall_s']),st.mean(d['requests']),st.mean(d['cost_usd']),st.mean(d['por'])))
print()
print("5. Without task T6 (pass_on_reference is 0 for every graded cell of T6, in every lane)")
for l in L:
    v=[r for r in rows if r['lane']==l and r['task']!='T6' and r['valid_intent']=='1']
    s=lambda k:int(sum(N(r,k) for r in v))
    print("%-8s valid %d scenarios %d pass_on_ref %d fail_on_start %d wrong_caught/total %d/%d"%(l,len(v),s('scenarios'),s('pass_on_reference'),s('fail_on_start'),s('wrong_caught'),s('wrong_total')))
