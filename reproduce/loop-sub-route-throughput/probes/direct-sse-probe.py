"""Three serial matched SSE probes per route. Run as the unprivileged benchmark user.
Credentials stay in the runner process; only timings/usage are printed.
This probes source-equivalent routes, not native-client WebSocket behavior.
"""
import json, os, pathlib, time, uuid, urllib.request, urllib.error, datetime

h=pathlib.Path.home()
loop=json.load(open(os.environ['LOOP_CHATGPT_CREDENTIAL_FILE']))
codex=json.load(open(os.environ['CODEX_AUTH_FILE']))['tokens']
prompt='Print exactly the integers 1 through 80, separated by a single space, with no other text.'
for rep in range(1,4):
 for client in ['loop','codex']:
  sid=str(uuid.uuid4())
  body=dict(model='gpt-6.1-terra',instructions='Follow the user request exactly. Do not use tools.',input=[dict(role='user',content=[dict(type='input_text',text=prompt)])],reasoning=dict(effort='medium'),include=['reasoning.encrypted_content'],stream=True,store=False,prompt_cache_key=sid)
  headers={'Content-Type':'application/json','Accept':'text/event-stream','session_id':sid}
  if client=='loop':
   url='https://api.openai.com/v1/responses'
   headers.update({'Authorization':'Bearer '+loop['access_token'],'conversation_id':sid,'User-Agent':''})
  else:
   url='https://chatgpt.com/backend-api/codex/responses'
   headers.update({'Authorization':'Bearer '+codex['access_token'],'ChatGPT-Account-ID':codex['account_id'],'originator':'codex_cli_rs','User-Agent':'codex_cli_rs/0.165.0'})
  started=datetime.datetime.now(datetime.timezone.utc).isoformat()
  t0=time.monotonic();first=None;last=None;delta=None;completed=None;usage={};tier=None;model=None;count=0;buf=b''
  try:
   req=urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers,method='POST')
   with urllib.request.urlopen(req,timeout=30) as response:
    ht=time.monotonic()-t0
    while True:
     chunk=response.read1(65536)
     if not chunk:break
     now=time.monotonic()-t0
     if first is None:first=now
     last=now;buf+=chunk
     while b'\n\n' in buf:
      block,buf=buf.split(b'\n\n',1)
      for line in block.splitlines():
       if not line.startswith(b'data:'):continue
       data=line[5:].strip()
       if data==b'[DONE]':continue
       try:event=json.loads(data)
       except ValueError:continue
       count+=1;kind=event.get('type','')
       if kind.endswith('.delta') and delta is None:delta=now
       if kind=='response.completed':
        completed=now;r=event.get('response',{});usage=r.get('usage',{});tier=r.get('service_tier');model=r.get('model')
   wall=time.monotonic()-t0;stream=(last-first) if first is not None else None
   output=usage.get('output_tokens')
   print(json.dumps(dict(client=client,probe='direct-SSE-route',rep=rep,started=started,headers_s=ht,first_s=first,first_delta_s=delta,last_s=last,completed_s=completed,wall_s=wall,stream_s=stream,output=output,reasoning=usage.get('output_tokens_details',{}).get('reasoning_tokens'),rate=output/stream if output and stream else None,effective_tier=tier,model=model,events=count)),flush=True)
  except Exception as exc:
   print(json.dumps(dict(client=client,rep=rep,started=started,error_type=type(exc).__name__,http_status=getattr(exc,'code',None),wall_s=time.monotonic()-t0)),flush=True)
