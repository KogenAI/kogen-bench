const {spawnSync}=require('node:child_process'); const assert=require('node:assert/strict');
const mode=process.argv[2];
const g=(...a)=>{const r=spawnSync('git',a,{cwd:process.cwd(),encoding:'utf8'}); assert.equal(r.status,0,r.stderr||r.stdout); return r.stdout;};
const base=g('rev-parse','HEAD').trim();
const baseline=g('show',base+':greet.js');
if(mode==='good'){assert.match(baseline,/greet/); console.log('observer good');}
else{ try{assert.match(baseline,/NOT-IN-THE-BASELINE/); console.log('observer bad accepted');}catch(e){console.log('observer bad rejected'); process.exit(1);} }
