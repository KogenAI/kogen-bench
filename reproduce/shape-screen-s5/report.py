import csv,sys,statistics as st
rows=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
for a in ['b0','s5']:
    x=[r for r in rows if r['arm']==a]
    print(a,'n',len(x),'ready',sum(r['class']=='ready' for r in x),'mean wall %.0f'%st.mean(float(r['wall_s']) for r in x),'mean in tok k %.0f'%(st.mean(int(r['in_tok']) for r in x)/1000),'mean out tok k %.1f'%(st.mean(int(r['out_tok']) for r in x)/1000))
# per-task paired change, S5 minus B0, same task and repetition (ready: 1 accepted, 0 not; wall in seconds)
k={(x['task'],x['rep'],x['arm']):x for x in rows}
for t,rep in sorted({(x['task'],x['rep']) for x in rows}):
    b,s=k.get((t,rep,'b0')),k.get((t,rep,'s5'))
    if b and s: print('pair',t,'r'+rep,'ready b0',int(b['class']=='ready'),'s5',int(s['class']=='ready'),'wall delta %+.0f'%(float(s['wall_s'])-float(b['wall_s'])))
