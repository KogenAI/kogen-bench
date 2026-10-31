"""Frozen API and containment extension of the attested lanes_bare harness.
No loop source changes. Real credentials are read only by the external gateway.
"""
import contextlib,datetime,hashlib,http.client,http.server,json,os,pathlib,shutil,socket,subprocess,threading,time,urllib.request,urllib.error
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/apiscreen-patches-high'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
MODEL='gpt-6.1-terra'
CELL_CAP=3.0
CAP=3.0
MAX_BYTES=524288
MAX_OUTPUT=32768
STATE={}

def write(p,d):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def cost(u):
 i=u.get('input_tokens',0);o=u.get('output_tokens',0);de=u.get('input_tokens_details') or {};c=de.get('cached_tokens',0);w=de.get('cache_creation_tokens',de.get('cache_write_tokens',0))
 return (((i-c)+c*.05+w*.25)*(2 if i>272000 else 1)+o*5*(1.5 if i>272000 else 1))/1e6

def chat_to_responses(b):
 inp=[];instructions=[]
 for m in b['messages']:
  role=m['role'];content=m.get('content')
  if role=='system':
   instructions.append(content if isinstance(content,str) else ''.join(x.get('text','') for x in content));continue
  if role=='tool':inp.append({'type':'function_call_output','call_id':m['tool_call_id'],'output':content});continue
  if content:inp.append({'role':role,'content':content})
  for c in m.get('tool_calls') or []:
   inp.append({'type':'function_call','call_id':c['id'],'name':c['function']['name'],'arguments':c['function']['arguments']})
 out={'model':b['model'],'instructions':'\n'.join(instructions),'input':inp,'reasoning':{'effort':b['reasoning_effort']},'stream':False,'store':False}
 if b.get('tools'):out['tools']=[{'type':'function',**t['function']} for t in b['tools']];out['tool_choice']='auto'
 return out

def responses_to_chat(b):
 text=[];calls=[]
 for x in b.get('output') or []:
  if x.get('type')=='function_call':calls.append({'id':x['call_id'],'type':'function','function':{'name':x['name'],'arguments':x['arguments']}})
  if x.get('type')=='message':text.extend(y.get('text','') for y in x.get('content',[]) if y.get('type')=='output_text')
 m={'role':'assistant','content':''.join(text) or None}
 if calls:m['tool_calls']=calls
 u=b.get('usage') or {};de=u.get('input_tokens_details') or {}
 return {'id':b.get('id'),'model':b.get('model'),'object':'chat.completion','choices':[{'index':0,'message':m,'finish_reason':'tool_calls' if calls else 'stop'}],'usage':{'prompt_tokens':u.get('input_tokens'), 'completion_tokens':u.get('output_tokens'),'total_tokens':u.get('total_tokens'),'prompt_tokens_details':de,'completion_tokens_details':u.get('output_tokens_details',{})}}

class Gateway(http.server.ThreadingHTTPServer):
 daemon_threads=False
 def __init__(self,arm,out):
  super().__init__(('127.0.0.1',0),Handler);self.arm=arm;self.out=pathlib.Path(out);self.rows=[];self.spend=0.;self.prior_spend=float(STATE.get('prior_spend',0));self.inflight=False;self.lock=threading.Lock();self.request_gate=threading.Lock();self.stop_reason=None
  # Each store was populated only through its tool's real stdin login command.
  p=R/'login-codex/auth.json' if arm=='codex' else R/'login-loop/.kogen/credentials/openai-compatible.json'
  d=json.loads(p.read_text());self.key=d['OPENAI_API_KEY'] if arm=='codex' else d['api_key']
 def save(self,row):
  self.rows.append(row)
  with (self.out/'route-receipts.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')

class Handler(http.server.BaseHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*a):pass
 def error(self,n,reason):
  data=json.dumps({'error':{'message':reason,'type':'confirmation_guard','code':'confirmation_guard'}}).encode();self.send_response(n);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):self.error(404,'catalog discovery disabled for frozen model')
 def do_POST(self):
  g=self.server;row={'utc':stamp(),'arm':g.arm,'client_path':self.path,'upstream':'https://api.openai.com/v1/responses','forwarded':False};reserved=0
  g.request_gate.acquire()
  try:
   if self.path not in ('/v1/responses','/v1/chat/completions'):return self.error(403,'only the frozen inference endpoint is available')
   n=int(self.headers.get('Content-Length','0'))
   if n<=0 or n>MAX_BYTES:return self.error(413,'request exceeds predeclared common byte bound')
   raw=self.rfile.read(n);body=json.loads(raw)
   body=chat_to_responses(body) if self.path.endswith('chat/completions') else body
   if body.get('model')!=MODEL or (body.get('reasoning') or {}).get('effort')!='high':return self.error(403,'frozen model or effort mismatch')
   # Both arms receive the same limits, service tier and retry ceiling.
   client_stream=bool(body.get('stream'));body['stream']=True
   body['max_output_tokens']=min(int(body.get('max_output_tokens',MAX_OUTPUT)),MAX_OUTPUT)
   body['service_tier']='default';body['store']=False;body.pop('prompt_cache_retention',None)
   data=json.dumps(body,separators=(',',':')).encode()
   if len(data)>MAX_BYTES:return self.error(413,'translated request exceeds predeclared common byte bound')
   # At most one token per UTF-8 byte plus a 4096-token envelope; cache writes
   # conservatively cost 1.25/M. This bound stays below long-context pricing.
   bound=len(data)+4096;long=bound>272000
   reserved=(bound*1.25*(2 if long else 1)+MAX_OUTPUT*5*(1.5 if long else 1))/1e6
   with g.lock:
    if g.stop_reason or g.inflight or g.prior_spend+g.spend+reserved>CAP:
     g.stop_reason=g.stop_reason or ('overlapping request after client retry' if g.inflight else 'experiment-wide spend reservation denied');return self.error(429,g.stop_reason)
    g.inflight=True
   row.update(request_sha256=hashlib.sha256(data).hexdigest(),request_bytes=len(data),model_requested=MODEL,effort_requested='high',stream=bool(body.get('stream')),maximum_charge_reserved_usd=reserved,include=body.get('include'),input_types=[x.get('type',x.get('role')) for x in body.get('input',[])],tool_names=[x.get('name') for x in body.get('tools',[])],instructions_sha256=hashlib.sha256(str(body.get('instructions','')).encode()).hexdigest(),batch_instruction_present='Batch independent reads and writes in one response.' in str(body.get('instructions','')))
   req=urllib.request.Request('https://api.openai.com/v1/responses',data=data,headers={'Authorization':'Bearer '+g.key,'Content-Type':'application/json','Accept':'text/event-stream' if body.get('stream') else 'application/json'})
   row['forwarded']=True
   with urllib.request.urlopen(req,timeout=300) as up:
    row.update(http_status=up.status,request_id=up.headers.get('x-request-id'),client_stream=client_stream)
    self.send_response(up.status);self.send_header('Content-Type','text/event-stream' if client_stream else 'application/json');self.send_header('Connection','close');self.end_headers();self.close_connection=True
    final=None;models=[]
    for line in up:
     if line.startswith(b'data: '):
      try:
       event=json.loads(line[6:]);response=event.get('response') or {}
       if response.get('model'):models.append({'event':event.get('type'),'id':response.get('id'),'model':response.get('model'),'reasoning':response.get('reasoning')})
       if event.get('type') in ('response.completed','response.incomplete','response.failed'):final=response
      except (ValueError,TypeError):pass
     # A Chat JSON decoder permits leading whitespace. Forward whitespace only
     # when real upstream SSE bytes arrive, preserving the shipped idle limit.
     try:self.wfile.write(line if client_stream else b' \n');self.wfile.flush()
     except (BrokenPipeError,ConnectionResetError):row['client_disconnected']=True
    row['response_models']=models
    if final is not None:row.update(response_id=final.get('id'),model=final.get('model'),reasoning=final.get('reasoning'),usage=final.get('usage'),status=final.get('status'))
    if not client_stream and final is not None:
     try:self.wfile.write(json.dumps(responses_to_chat(final)).encode());self.wfile.flush()
     except (BrokenPipeError,ConnectionResetError):row['client_disconnected']=True
   if row.get('client_disconnected'):g.stop_reason='client disconnected before delivery'
   if row.get('usage') is None:
    row.update(usd_list=None,charge_upper_bound_usd=reserved);g.spend+=reserved;g.stop_reason='missing final provider usage'
   else:
    row['usd_list']=cost(row['usage']);g.spend+=row['usd_list'];row['charge_upper_bound_usd']=((row['usage']['input_tokens']*1.25)+row['usage']['output_tokens']*5)/1e6
   if row.get('model')!=MODEL or any(x['model']!=MODEL for x in row.get('response_models',[])):g.stop_reason='returned model identity mismatch'
  except urllib.error.HTTPError as e:
   row.update(http_status=e.code,error='upstream HTTP '+str(e.code));g.stop_reason=row['error'];self.error(502,row['error'])
  except Exception as e:
   # Error bodies and headers can contain credentials. Never persist them.
   row.update(error=type(e).__name__,charge_upper_bound_usd=reserved);g.spend+=reserved;g.stop_reason=type(e).__name__
   with contextlib.suppress(Exception):self.error(502,g.stop_reason)
  finally:
   if row['forwarded']:
    with g.lock:g.inflight=False
   else:row.update(usd_list=0,charge_upper_bound_usd=0)
   g.save(row)
   g.request_gate.release()

SHELL_WRAPPER='''#!/usr/bin/python3
import os,sys
name=os.path.basename(sys.argv[0])
shell='/runtime/code-mode-host.real' if name=='codex-code-mode-host' else ('/runtime/bash' if name=='bash' else '/runtime/dash')
args=['/usr/bin/bwrap','--die-with-parent','--unshare-user','--unshare-net','--unshare-pid','--bind','/','/','--proc','/proc','--dev','/dev','--cap-drop','ALL','--',shell]+sys.argv[1:]
os.execv(args[0],args)
'''

def namespace_command(cmd,tmp,env):
 tmp=pathlib.Path(tmp);home=tmp/'isolated-home';home.mkdir(exist_ok=True);(home/'.codex').mkdir(exist_ok=True)
 script=R/'tool-shell.py'
 b=['/usr/bin/bwrap','--die-with-parent','--new-session','--unshare-user','--unshare-pid','--unshare-uts','--unshare-ipc','--cap-drop','ALL','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/home','--bind',str(home),'/home/agent','--bind',str(tmp),str(tmp),'--dir','/runtime','--ro-bind','/usr/bin/bash','/runtime/bash','--ro-bind','/usr/bin/dash','/runtime/dash','--ro-bind',str(script),'/usr/bin/bash','--ro-bind',str(script),'/usr/bin/dash','--ro-bind',str(STATE.get('loop_bin',R/'bin/loop-b8a4046')),'/runtime/loop','--ro-bind',CODEX_DIR+'/codex','/runtime/codex','--ro-bind',GO_ROOT,'/runtime/go','--ro-bind',NODE_ROOT,'/runtime/node','--ro-bind',CODEX_DIR+'/codex-code-mode-host','/runtime/code-mode-host.real','--ro-bind',str(script),'/runtime/codex-code-mode-host','--dir','/etc']
 for f in ['/etc/ssl','/etc/passwd','/etc/group','/etc/nsswitch.conf','/etc/resolv.conf','/etc/hosts']:
  if os.path.exists(f):b+=['--ro-bind',f,f]
 # No host HOME, secret store, evaluator, references, neighboring results or host /proc.
 env.update(HOME='/home/agent',CODEX_HOME='/home/agent/.codex',PATH='/runtime/go/bin:/runtime/node/bin:/usr/bin:/bin',SHELL='/bin/bash',GOROOT='/runtime/go',GOCACHE=str(tmp/'go-cache'),GOMODCACHE=str(tmp/'go-modcache'),GOTOOLCHAIN='local',GOPROXY='off',GOMAXPROCS='2')
 env.pop('MISE_SHELL',None)
 if cmd and pathlib.Path(cmd[0]).resolve()==pathlib.Path(STATE.get('loop_bin',R/'bin/loop-b8a4046')).resolve():cmd=['/runtime/loop']+cmd[1:]
 elif os.path.basename(cmd[0])=='codex':cmd=['/runtime/codex']+cmd[1:]
 return b+['--chdir',str(tmp/'ws'),'--']+cmd

def probe(tmp,out,arm,env):
 kit=R/'tasks'/STATE['task']; paths={'evaluator':kit/'evaluator/evaluate.toml','reference':next((kit/'reference').rglob('*.go')),'neighbor_result':R/'outside-canary','canary':R/'outside-canary','loop_credential':R/'login-loop/.kogen/credentials/openai-compatible.json'}
 for p in paths.values():
  if not p.is_file():raise RuntimeError('negative probe target absent: '+str(p))
 script=pathlib.Path(tmp)/'boundary_probe.py'
 script.write_text('import json,os,pathlib,socket\n'+'paths='+repr({k:str(v) for k,v in paths.items()})+'\n'+'''r={'uid':os.getuid(),'gid':os.getgid(),'workspace_readable':pathlib.Path('Makefile').is_file(),'denials':{},'network_denied':False}
for k,p in paths.items():
 try:open(p,'rb').read(1);r['denials'][k]=False
 except OSError as e:r['denials'][k]=type(e).__name__
s=socket.socket();s.settimeout(1)
try:s.connect(('1.1.1.1',443))
except OSError as e:r['network_denied']=True;r['network_error']=str(e)
print(json.dumps(r))
assert r['workspace_readable'] and r['network_denied'] and all(r['denials'].values())
''')
 cmd=namespace_command(['/bin/sh','-c','python3 '+str(script)],tmp,env)
 p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=30)
 write(pathlib.Path(out)/'boundary-probe.json',{'utc':stamp(),'arm':arm,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'command':cmd,'outside_targets_exist':True})
 script.unlink()
 if p.returncode:raise RuntimeError('actual tool namespace negative probe failed')

def install(h):
 orig_agent=h.run_bare_agent;orig_filtered=h.filtered_agent_run;orig_loop=h.loop_task;orig_codex=h.codex_command
 (R/'tool-shell.py').write_text(SHELL_WRAPPER);(R/'tool-shell.py').chmod(0o755)
 def loop_task(a,ws,tmp,prompt,tt):
  task=orig_loop(a,ws,tmp,prompt,tt)
  assert task['instructions']==''
  task['role'].update(provider='openai-compatible',base_url=STATE['origin']+'/v1')
  return task
 def codex_command(a,b):
  c=orig_codex(a,b)
  c[c.index('workspace-write')]='danger-full-access'
  return c[:-1]+['-c','model_provider="confirmation"','-c','model_providers.confirmation.name="Confirmation OpenAI API"','-c','model_providers.confirmation.base_url="'+STATE['origin']+'/v1"','-c','model_providers.confirmation.wire_api="responses"','-c','model_providers.confirmation.requires_openai_auth=false','-c','model_providers.confirmation.supports_websockets=false','-c','model_providers.confirmation.request_max_retries=0','-c','model_providers.confirmation.stream_max_retries=0']+c[-1:]
 def filtered(cmd,cwd,env,deadline_s,events,stderr,stdin,arm,out):
  tmp=str(pathlib.Path(cwd).parent)
  # Cache restore and both boundary checks are outside the measured agent run.
  cmd=namespace_command(cmd,tmp,env)
  write(pathlib.Path(out)/'namespace.json',{'command':cmd,'uid':os.getuid(),'gid':os.getgid(),'credential_source':'external tool-owned login; no credential mount','shell_network':'nested bubblewrap --unshare-net; code-mode host uses the same wrapper','shared_endpoint':'https://api.openai.com/v1/responses'})
  lease=pathlib.Path('/run/kogen-host-lock.d/expires')  # the original host's lease; without one the default deadline stands
  lease_remaining=float(lease.read_text())-time.time()-30 if lease.exists() else deadline_s
  effective_deadline=min(deadline_s,max(1,int(lease_remaining)))
  write(pathlib.Path(out)/'effective-deadline.json',{'default_seconds':deadline_s,'effective_seconds':effective_deadline,'reason':'existing owner lease bounds run; no timeout increase'})
  t=time.monotonic();v=orig_filtered(cmd,cwd,env,effective_deadline,events,stderr,stdin,arm,out);STATE['agent_wall']=time.monotonic()-t
  return v
 def agent(a,ws,tmp,out,tt,prompt,deadline_s):
  STATE.update(task=a.task,agent_wall=None,loop_bin=a.loop_bin)
  cache=pathlib.Path(tmp)/'go-cache'
  subprocess.run(['cp','-a',str(R/'cache-snapshot')+'/.',str(cache)],check=True,timeout=60)
  project_cache=pathlib.Path(ws)/'.cache/go'
  project_cache.mkdir(parents=True,exist_ok=True)
  subprocess.run(['cp','-a',str(R/'cache-snapshot')+'/.',str(project_cache)],check=True,timeout=60)
  with open(pathlib.Path(ws)/'.git/info/exclude','a') as excluded:excluded.write('\n/.cache/\n')
  (pathlib.Path(tmp)/'go-modcache').mkdir()
  env=h.agent_env(tt,tmp,{})
  probe(tmp,out,a.arm,env)
  g=Gateway(a.arm,out);STATE['origin']='http://127.0.0.1:'+str(g.server_port)
  th=threading.Thread(target=g.serve_forever,daemon=True);th.start()
  try:
   rec,code,to,ver=orig_agent(a,ws,tmp,out,tt,prompt,deadline_s)
  finally:
   g.shutdown();th.join();g.server_close()
   g.rows=[x for x in g.rows if x.get('forwarded')]
   write(pathlib.Path(out)/'route-summary.json',{'usd_list':sum(x.get('usd_list') or 0 for x in g.rows),'charge_upper_bound_usd':sum(x.get('charge_upper_bound_usd') or 0 for x in g.rows),'requests':len(g.rows),'stop_reason':g.stop_reason,'response_models':[x.get('model') for x in g.rows],'all_usage_present':bool(g.rows) and all(x.get('usage') for x in g.rows)})
  # Preserve CLI usage in events; use per-response upstream records for comparable totals.
  write(pathlib.Path(out)/'client-usage.json',rec)
  if g.rows and all(x.get('usage') for x in g.rows):
   rec.update(input_tokens=sum(x['usage']['input_tokens'] for x in g.rows),cached_input_tokens=sum((x['usage'].get('input_tokens_details') or {}).get('cached_tokens',0) for x in g.rows),output_tokens=sum(x['usage']['output_tokens'] for x in g.rows),requests=len(g.rows),models=sorted({x['model'] for x in g.rows}),usage_complete={k:True for k in ('input_tokens','cached_input_tokens','output_tokens')})
  STATE['cost']=sum(x.get('usd_list') or 0 for x in g.rows)
  rec['reasoning_tokens']=sum((x.get('usage') or {}).get('output_tokens_details',{}).get('reasoning_tokens',0) for x in g.rows)
  rec['wall_s']=round(STATE['agent_wall'] or rec['wall_s'],3)
  if g.stop_reason:rec['errors'].append(g.stop_reason)
  return rec,code,to,ver
 h.price=lambda rec:(STATE['cost'],None)
 h.loop_task=loop_task;h.codex_command=codex_command;h.filtered_agent_run=filtered;h.run_bare_agent=agent
