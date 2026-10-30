"""Alternating route probes using ONLY kogen-loop's own OAuth credential.
Run as the unprivileged benchmark user. Credential stays in process memory; prints timings/usage only.
No Codex client ID, headers, UA or credentials are used.
usage: subroute-probe.py CANDIDATE PAIRS   (pairs alternate baseline A with CANDIDATE)
       subroute-probe.py check CANDIDATE   (single request, status only)
"""
import json, pathlib, time, uuid, urllib.request, sys, datetime, socket, ssl, base64, os, struct
CRED=os.environ['LOOP_CHATGPT_CREDENTIAL_FILE']  # loop's own login file; never printed
tok=json.load(open(CRED))['access_token']
UA='kogen-loop/b8a4046 (linux; route-probe)'
PROMPT='Print exactly the integers 1 through 170, separated by a single space, with no other text.'
def body(sid):
 return dict(model='gpt-6.1-terra',instructions='Follow the user request exactly. Do not use tools.',input=[dict(role='user',content=[dict(type='input_text',text=PROMPT)])],reasoning=dict(effort='medium'),include=['reasoning.encrypted_content'],stream=True,store=False,prompt_cache_key=sid)
ROUTES={
 'A':('https://api.openai.com/v1/responses',{'User-Agent':''}),           # loop today
 'B':('https://api.openai.com/v1/responses',{'User-Agent':UA}),           # honest UA
 'D':('https://chatgpt.com/backend-api/codex/responses',{'User-Agent':UA}),  # backend path, loop token
}
def rec(**k): print(json.dumps(k),flush=True)
def handle(event,now,st):
 st['events']+=1;kind=event.get('type','')
 if kind.endswith('.delta') and st['delta'] is None: st['delta']=now
 if kind=='response.completed':
  r=event.get('response',{});st['usage']=r.get('usage',{});st['tier']=r.get('service_tier');st['model']=r.get('model');st['completed']=now
 if kind in('error','response.failed'): st['err']=json.dumps(event)[:300]
def finish(cand,rep,started,t0,st,extra={}):
 u=st['usage'];out=u.get('output_tokens');stream=(st['last']-st['first']) if st['first'] is not None else None
 rec(cand=cand,rep=rep,started=started,first_s=st['first'],first_delta_s=st['delta'],last_s=st['last'],wall_s=time.monotonic()-t0,stream_s=stream,output=out,reasoning=u.get('output_tokens_details',{}).get('reasoning_tokens'),rate=out/stream if out and stream else None,tier=st['tier'],model=st['model'],events=st['events'],err=st.get('err'),**extra)
def http(cand,rep):
 url,extra=ROUTES[cand];sid=str(uuid.uuid4())
 h={'Content-Type':'application/json','Accept':'text/event-stream','session_id':sid,'conversation_id':sid,'Authorization':'Bearer '+tok};h.update(extra)
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.monotonic()
 st=dict(first=None,last=None,delta=None,completed=None,usage={},tier=None,model=None,events=0);buf=b''
 try:
  with urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(body(sid)).encode(),headers=h,method='POST'),timeout=60) as r:
   while True:
    c=r.read1(65536)
    if not c:break
    now=time.monotonic()-t0
    if st['first'] is None: st['first']=now
    st['last']=now;buf+=c
    while b'\n\n' in buf:
     blk,buf=buf.split(b'\n\n',1)
     for line in blk.splitlines():
      if line.startswith(b'data:') and line[5:].strip()!=b'[DONE]':
       try: handle(json.loads(line[5:].strip()),now,st)
       except ValueError: pass
  finish(cand,rep,started,t0,st,dict(status=200,transport='http-sse'))
 except Exception as e:
  rec(cand=cand,rep=rep,started=started,error=type(e).__name__,http_status=getattr(e,'code',None),detail=(e.read()[:200].decode('utf-8','replace') if hasattr(e,'read') else str(e)[:200]))
# minimal RFC6455 client (no external libs)
def ws(cand,rep):
 sid=str(uuid.uuid4());started=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.monotonic()
 st=dict(first=None,last=None,delta=None,completed=None,usage={},tier=None,model=None,events=0)
 try:
  s=ssl.create_default_context().wrap_socket(socket.create_connection(('api.openai.com',443),timeout=60),server_hostname='api.openai.com')
  key=base64.b64encode(os.urandom(16)).decode()
  req=('GET /v1/responses HTTP/1.1\r\nHost: api.openai.com\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
   f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\nAuthorization: Bearer {tok}\r\nUser-Agent: {UA}\r\nsession_id: {sid}\r\n\r\n')
  s.sendall(req.encode());hdr=b''
  while b'\r\n\r\n' not in hdr:
   c=s.recv(4096)
   if not c: break
   hdr+=c
  head,rest=hdr.split(b'\r\n\r\n',1);status=int(head.split()[1])
  if status!=101:
   rec(cand=cand,rep=rep,started=started,error='ws-handshake',http_status=status,detail=rest[:200].decode('utf-8','replace'));return
  b=body(sid);b.pop('stream');b['type']='response.create'
  p=json.dumps(b).encode();m=os.urandom(4);n=len(p)
  fr=bytes([0x81])+(bytes([0x80|n]) if n<126 else bytes([0x80|126])+struct.pack('>H',n) if n<65536 else bytes([0x80|127])+struct.pack('>Q',n))+m+bytes(x^m[i%4] for i,x in enumerate(p))
  t0=time.monotonic();s.sendall(fr)   # time from send, matching HTTP from POST
  buf=rest;msg=b''
  def need(k):
   nonlocal buf
   while len(buf)<k:
    c=s.recv(65536)
    if not c: raise EOFError
    now=time.monotonic()-t0
    if st['first'] is None: st['first']=now
    st['last']=now;buf+=c
  while st['completed'] is None and st.get('err') is None:
   need(2);op=buf[0]&0xf;fin=buf[0]&0x80;l=buf[1]&0x7f;o=2
   if l==126: need(4);l=struct.unpack('>H',buf[2:4])[0];o=4
   elif l==127: need(10);l=struct.unpack('>Q',buf[2:10])[0];o=10
   need(o+l);pl=buf[o:o+l];buf=buf[o+l:]
   if op==8: st['err']='close:'+pl[:200].decode('utf-8','replace');break
   if op in(1,0):
    msg+=pl
    if fin:
     try: handle(json.loads(msg),st['last'],st)
     except ValueError: pass
     msg=b''
  s.close();finish(cand,rep,started,t0,st,dict(status=101,transport='websocket'))
 except Exception as e:
  rec(cand=cand,rep=rep,started=started,error=type(e).__name__,detail=str(e)[:200])
def run(c,rep): (ws if c=='E' else http)(c,rep)
if sys.argv[1]=='check': run(sys.argv[2],0)
else:
 cand=sys.argv[1]
 for rep in range(1,int(sys.argv[2])+1):
  order=['A',cand] if rep%2 else [cand,'A']
  for c in order: run(c,rep)
