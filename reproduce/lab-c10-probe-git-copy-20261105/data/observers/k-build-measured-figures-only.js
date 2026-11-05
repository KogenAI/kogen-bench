const {spawnSync}=require('node:child_process'); const assert=require('node:assert/strict');
const mode=process.argv[2]; const BASE=process.env.KMF_BASE_SHA||'@@BASE@@';
const r=spawnSync('git',['show',BASE+':build/prompts/builder.md'],{cwd:process.cwd(),encoding:'utf8'});
assert.equal(r.status,0,r.stderr);
if(mode==='good'){assert.match(r.stdout,/builder/); console.log('observer good');}
else{ if(!/MEASURED-FIGURES-ONLY/.test(r.stdout)){console.log('observer bad rejected'); process.exit(1);} console.log('observer bad accepted'); }
