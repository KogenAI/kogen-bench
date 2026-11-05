#!/usr/bin/env python3
# mkneg.py <base frozen fixture> <slug> <new fixture name> <pick 0..1>: synthetic negative control.
# Appends to the Intent's own step file a copy of one step definition (same pattern) from another Intent's
# own step file whose scenarios use it, so that step text is bound in both files.
import sys, os, subprocess, json, glob, re
E=os.path.expanduser('~/work.noindex/scratch/research/work/e1')
base,S,name,pick=sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4])
CU=os.path.expanduser('~/work.noindex/releases/kogen-d98cfe0/lib/kogen/lib/cucumber/node_modules')
src=f'{E}/frozen/{base}'; dst=f'{E}/frozen/{name}'
subprocess.run(['cp','-c','-R','-p',src,dst],check=True)
own=sorted(glob.glob(f'{dst}/features/steps/{S}__*.js'))[0]
others=sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(f'{dst}/.kogen/intents/*/intent.md'))
others=[o for o in others if o!=S]
start=int(len(others)*pick)
probe='''const fs=require('fs'),path=require('path');const cc=require('@cucumber/cucumber');const b=cc.supportCodeLibraryBuilder;
const inp=JSON.parse(fs.readFileSync(0,'utf8'));let n=0;b.reset(process.cwd(),()=>String(n++));
try{require(path.resolve(inp.file))}catch(e){}
const lib=b.finalize();
for(const t of inp.texts){for(const d of lib.stepDefinitions){if(d.uri===inp.file&&d.matchesStepName(t)){
process.stdout.write(JSON.stringify({text:t,regex:d.pattern instanceof RegExp,pattern:d.pattern instanceof RegExp?d.pattern.source:String(d.pattern),flags:d.pattern instanceof RegExp?d.pattern.flags:''})+'\\n');process.exit(0)}}}'''
for o in others[start:]+others[:start]:
    feat=f'{dst}/.kogen/intents/{o}/acceptance.feature'
    files=sorted(os.path.relpath(p,dst) for p in glob.glob(f'{dst}/features/steps/{o}__*.js'))
    if not os.path.exists(feat) or not files: continue
    texts=[]
    for l in open(feat):
        m=re.match(r'\s*(Given|When|Then|And|But)\s+(.*\S)\s*$',l)
        if m and '<' not in m.group(2): texts.append(m.group(2))
    for f in files:
        r=subprocess.run(['node','-e',probe],cwd=dst,input=json.dumps({'file':f,'texts':texts}),capture_output=True,text=True,env=dict(os.environ,NODE_PATH=CU))
        if r.stdout.strip():
            d=json.loads(r.stdout.strip().splitlines()[-1])
            pat=('new RegExp(%s,%s)'%(json.dumps(d['pattern']),json.dumps(d['flags']))) if d['regex'] else json.dumps(d['pattern'])
            with open(own,'a') as fh:
                fh.write('\n// Lab E1 negative control: the same binding as %s in %s\n;(function () { const { defineStep } = require(\'@cucumber/cucumber\'); defineStep(%s, function () {}); })();\n'%(o,f,pat))
            print(json.dumps(dict(fixture=name,slug=S,own=os.path.relpath(own,dst),other=o,other_file=f,text=d['text'],pattern=d['pattern'])))
            sys.exit(0)
print('NO OVERLAP FOUND'); sys.exit(1)
