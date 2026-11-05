#!/usr/bin/env python3
"""Regenerates the E3 evidence counts in README.md from data/. Run: python3 -I report.py  (from this directory)"""
import json,os,re,collections
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')
items=json.load(open(D+'/e3-items.json')); L=json.load(open(D+'/landred-28.json'))
hb=[i for i in items if i['bucket']=='host_or_base']; lr=[i for i in items if i['bucket']=='land_red']
print('items:',len(items),'host_or_base',len(hb),'land_red sample',len(lr))
print('\nhost_or_base verifying seconds:')
for i in hb:
    m=re.search(r'verifying=(\d+)',i['src']); print(' ',i['id'],i['repo'],int(m[1]) if m else None)
print('\nland-red, all 28 by recorded failure signature:',dict(collections.Counter(x['cls'] for x in L)))
print('mentions of a test timeout among the 28:',sum(1 for x in L if re.search(r'timed out|timeout|deadline',x['text'],re.I)))
by={x['slug']:x for x in L}
samp=[by.get(i['id'][3:]) for i in lr]
print('sample of 10 by signature:',dict(collections.Counter((x or {}).get('cls','?') for x in samp)))
print('\nreruns executed: 0 (arms A and B need a quiet host; see README)')
