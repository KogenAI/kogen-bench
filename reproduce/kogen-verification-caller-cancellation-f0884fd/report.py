#!/usr/bin/env python3
import json,sys
x=json.load(open(sys.argv[1]))
print('verdict:',x['verdict'])
for r in x['tasks']:
 print(r['task'],r['stored']['outcome']+' -> '+r['candidate']['outcome'],'hidden:',str(r['stored']['hidden_all_passed'])+' -> '+str(r['candidate']['hidden_all_passed']),'intent:',str(r['stored']['valid_intent'])+' -> '+str(r['candidate']['valid_intent']))
print('candidate tokens:',x['totals']['input_tokens'],'input,',x['totals']['cached_input_tokens'],'cached input,',x['totals']['output_tokens'],'output')
print('cancellation witnessed:',x['cancellation_witnessed'])
