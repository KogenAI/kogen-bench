import subprocess,sys,json,random,collections,os,time
from pathlib import Path
w=Path(sys.argv[1]);exe=w/'target/debug/tally';rng=random.Random(817)
def run(args,data=None):return subprocess.run([str(exe)]+args,input=data,capture_output=True,text=True)
files=[];counts=collections.Counter()
for n in range(4):
 keys=[rng.choice(['shared']+['key%03d'%i for i in range(65)]) for _ in range(450)]+['shared']*40
 counts.update(keys);f=w/('input%d.log'%n);f.write_text(''.join('2026-10-01 INFO '+k+' tail\n' for k in keys)+'ignored\n');files.append(str(f))
expected=[{'key':k,'count':v} for k,v in sorted(counts.items(),key=lambda x:(-x[1],x[0]))[:12]]
args=['--format','json','--top','12','--memory-keys','3'];p=run(args+files);assert p.returncode==0,p.stderr;assert json.loads(p.stdout)==expected
p=run(args+list(reversed(files)));assert json.loads(p.stdout)==expected
checkpoint=w/'checkpoint';p=run(args+['--checkpoint',str(checkpoint)]+files);assert p.returncode==0,p.stderr;assert json.loads(p.stdout)==expected
p=run(args+['--checkpoint',str(checkpoint)]+files);assert json.loads(p.stdout)==expected
# Same-size input mutation must be rejected on resume with empty stdout.
f=Path(files[0]);original=f.read_text();f.write_text(original.replace('shared','mutate',1));p=run(args+['--checkpoint',str(checkpoint)]+files);assert p.returncode!=0 and not p.stdout,'modified input accepted';f.write_text(original)
# Valid JSON with damaged metadata must fail before output.
manifest=checkpoint/'state.json';saved_manifest=manifest.read_bytes();damaged=json.loads(saved_manifest);damaged['done']=0;manifest.write_text(json.dumps(damaged));p=run(args+['--checkpoint',str(checkpoint)]+files);assert p.returncode!=0 and not p.stdout;manifest.write_bytes(saved_manifest)
# Corrupt a complete committed run; no partial output is permitted.
state=json.loads((checkpoint/'state.json').read_text());runfile=checkpoint/state['runs'][0];saved=runfile.read_bytes();runfile.write_bytes(saved[:-5]+b'0000\n');p=run(args+['--checkpoint',str(checkpoint)]+files);assert p.returncode!=0 and not p.stdout;runfile.write_bytes(saved)
p=run(args+['--checkpoint',str(w/'stdin-state'),'-'],'2026-10-01 INFO x\n');assert p.returncode!=0 and not p.stdout
p=run(args+files+['missing-file']);assert p.returncode!=0 and not p.stdout
p=run(args+['-'],'2026-10-01 INFO z\n2026-10-01 INFO a\n');assert json.loads(p.stdout)==[{'key':'a','count':1},{'key':'z','count':1}]
p=run(['--top','0']+files);assert p.returncode==0 and not p.stdout
# Real process kill after at least one committed file, then resume from that boundary.
large=w/'large.log';large.write_text(('2026-10-01 INFO big\n')*900000)
cp=w/'kill-checkpoint';cmd=[str(exe)]+args+['--checkpoint',str(cp),files[0],str(large)]
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
deadline=time.monotonic()+30
while time.monotonic()<deadline and p.poll() is None:
 try:
  if json.loads((cp/'state.json').read_text())['done']>=1:break
 except (FileNotFoundError,json.JSONDecodeError):pass
 time.sleep(.01)
assert p.poll() is None,'kill control did not interrupt processing'
p.kill();p.communicate();res=run(args+['--checkpoint',str(cp),files[0],str(large)]);assert res.returncode==0,res.stderr
oracle=counts=collections.Counter(k.split()[2] for k in (Path(files[0]).read_text()+large.read_text()).splitlines() if len(k.split())>=3)
want=[{'key':k,'count':v} for k,v in sorted(oracle.items(),key=lambda x:(-x[1],x[0]))[:12]]
assert json.loads(res.stdout)==want
# Separate process resource check: total distinct keys cannot be loaded back into RAM.
import re
many=w/'many-keys.log'
with many.open('w') as f:
 for i in range(450000):f.write('2026-10-01 INFO %08d%s\n'%(i,'x'*65))
command=[str(exe),'--format','json','--top','1','--memory-keys','128',str(many)]
if sys.platform=='darwin':command=['/usr/bin/time','-l']+command
else:command=['/usr/bin/time','-f','MAX_RSS_KB %M']+command
res=subprocess.run(command,capture_output=True,text=True,timeout=240)
assert res.returncode==0,res.stderr
assert json.loads(res.stdout)==[{'key':'00000000'+'x'*65,'count':1}]
if sys.platform=='darwin':rss=int(re.search(r'(\d+)\s+maximum resident set size',res.stderr).group(1))
else:rss=int(re.search(r'MAX_RSS_KB (\d+)',res.stderr).group(1))*1024
assert rss<48*1024*1024, 'external merge exceeded 48 MiB resident process bound'
print('EXTERNAL_MERGE_PROBE_PASS max_rss_bytes='+str(rss))
