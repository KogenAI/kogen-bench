const {spawnSync}=require('node:child_process'); const assert=require('node:assert/strict');
const mode=process.argv[2];
const g=(...a)=>{const r=spawnSync('git',a,{cwd:process.cwd(),encoding:'utf8'}); return r;};
const show=g('show','HEAD:cli/main.go'); assert.equal(show.status,0,'read baseline CLI source: '+show.stderr);
const hit=g('grep','-I','-n','-w','-F','-e','Usage','HEAD','--','.',':(exclude).kogen');
if(mode==='good'){assert.equal(hit.status,0,'scope scan found no key'); console.log('observer good');}
else{ const miss=g('grep','-I','-n','-w','-F','-e','AbsentKey','HEAD','--','.',':(exclude).kogen'); if(miss.status===1){console.log('observer bad rejected'); process.exit(1);} console.log('observer bad accepted'); }
