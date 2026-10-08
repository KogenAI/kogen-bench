import os,sys,subprocess,shutil,re
from pathlib import Path
s=Path(__file__).resolve().parent; w=Path(sys.argv[1]).resolve(); b=s/'base'
fam='synthetic' if (b/'mix.exs').exists() and 'trackline' in (b/'mix.exs').read_text() else ('elixir' if (b/'mix.exs').exists() else 'rust')
env=os.environ.copy(); home=Path.home()
env.update(MIX_ENV='test',HEX_OFFLINE='1',MIX_OS_CONCURRENCY_LOCK='0',ERL_FLAGS='+S 4:4',TRACKLINE_DB=str(w/'grade.db'))
env['PATH']=str(home/'.local/share/mise/installs/elixir/1.20.2-otp-29/bin')+':'+str(home/'.local/share/mise/installs/erlang/29.0.3/bin')+':'+str(home/'.cargo/bin')+':'+env.get('PATH','/usr/bin:/bin')
for p in ['mix.exs','mix.lock','Cargo.toml','Cargo.lock','config','test/test_helper.exs','test/support']:
 src=b/p;dst=w/p
 if not src.exists():continue
 fs=list(src.rglob('*')) if src.is_dir() else [src]
 for f in fs:
  if f.is_file() and (not (w/f.relative_to(b)).is_file() or f.read_bytes()!=(w/f.relative_to(b)).read_bytes()):
   print('PROTECTED_PATH_FAIL',f.relative_to(b));sys.exit(1)
for name in ['test','tests']:
 dst=w/name
 if dst.exists():shutil.rmtree(dst)
 if (b/name).exists():shutil.copytree(b/name,dst)
if fam!='rust':
 # only trusted dependency/build inputs
 for name in ['deps','_build']:
  if (w/name).exists():shutil.rmtree(w/name)
  warm=Path(os.environ['TASK_DIR']).parent/fam/'warm'/name
  subprocess.run(['/bin/cp',('-cR' if sys.platform=='darwin' else '-R'),str(warm),str(w/name)],check=True)
 app='trackline' if fam=='synthetic' else 'beltway'
 shutil.rmtree(w/'_build/test/lib'/app,ignore_errors=True)
else:shutil.rmtree(w/'target',ignore_errors=True)
def run(args,label):
 p=subprocess.run(args,cwd=w,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 print(p.stdout[-9000:])
 if p.returncode:print(label+'_FAIL');sys.exit(1)
 if args[:2]==['mix','test'] and not re.search(r'(Result: [1-9][0-9]*(?:/[0-9]+)? passed|[1-9][0-9]* tests?, 0 failures)',p.stdout):
  print('NO_TESTS');sys.exit(1)
 print(label+'_PASS',flush=True)
if fam!='rust':run(['mix','test'],'VISIBLE')
else:run(['cargo','test','--offline'],'VISIBLE')
if os.environ.get('AUTHOR_VISIBLE_ONLY')=='1':sys.exit(0)
if (s/'tests').exists():shutil.copytree(s/'tests',w/('tests' if fam=='rust' else 'test'),dirs_exist_ok=True)
if fam!='rust':run(['mix','test'],'HIDDEN')
else:run(['cargo','test','--offline'],'HIDDEN')
if (s/'probe.py').exists():run([sys.executable,str(s/'probe.py'),str(w)],'REQUIREMENT_PROBE')
print('TASK_PASS')
