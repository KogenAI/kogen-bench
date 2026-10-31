import csv,sys,statistics as st
rows=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
for h,planned in [('linux',10),('second_host_invalid',16)]:  # planned shapes per arm: 5 tasks x 2 reps and 8 tasks x 2 reps
    print('half',h,'planned',planned,'per arm; rows kept',' '.join('%s %d'%(A,sum(r['arm']==A and r['half']==h for r in rows)) for A in ['b0','p2','p4','s3']),'; ready',' '.join('%s %d/%d'%(A,sum(r['class']=='ready' for r in rows if r['arm']==A and r['half']==h),planned) for A in ['b0','p2','p4','s3']))
rd=[r for r in rows if r['class']=='ready' and r['half']=='linux']
k={(r['task'],r['rep'],r['arm']):int(r['items_covered']) for r in rd}
for A in ['b0','p2','p4','s3']:
    x=[r for r in rd if r['arm']==A]
    print(A,'ready',len(x),'mean coverage %.3f'%st.mean(int(r['items_covered'])/int(r['items_total']) for r in x),'mean items %.2f'%st.mean(int(r['items_covered']) for r in x),'bloat',sum(int(r['bloat_scenarios']) for r in x),'scenarios',sum(int(r['scenarios']) for r in x))
for A in ['p2','p4','s3']:
    d=[(t,rep,v-k[(t,rep,'b0')]) for (t,rep,a),v in sorted(k.items()) if a==A and (t,rep,'b0') in k]
    print(A,'pairs',len(d),'higher',sum(x[2]>0 for x in d),'lower',sum(x[2]<0 for x in d),'equal',sum(x[2]==0 for x in d),' '.join(f'{t}/r{r}:{v:+d}' for t,r,v in d))
