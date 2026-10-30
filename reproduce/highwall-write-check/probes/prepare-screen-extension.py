import hashlib,os,pathlib

# Usage: WCHECK_ROOT=<run root> python3 prepare-screen-extension.py
# Reads <root>/confirmation_ext.py (lanes/confirm-eu/confirmation_ext.py) and writes
# <root>/write-check-screen-high/confirmation_ext_screen.py: the same gateway plus an activation witness for write_file's command.
root=pathlib.Path(os.environ['WCHECK_ROOT'])

origin=root/'confirmation_ext.py'
screen=root/'write-check-screen-high'
text=origin.read_text()
old="self.rows=[];self.spend=0.;self.inflight=False;self.lock=threading.Lock();self.request_gate=threading.Lock();self.stop_reason=None"
new="self.rows=[];self.spend=0.;self.inflight=False;self.lock=threading.Lock();self.request_gate=threading.Lock();self.stop_reason=None;self.write_check_calls={}"
assert text.count(old)==1
text=text.replace(old,new)
old="raw=self.rfile.read(n);row['client_request_bytes']=len(raw);body=json.loads(raw)"
new="""raw=self.rfile.read(n);row['client_request_bytes']=len(raw);body=json.loads(raw)
   # Observation-only activation witness: hash the command and combined output;
   # never persist workspace contents or the command text.
   for message in body.get('messages',[]):
    if message.get('role')=='tool' and message.get('tool_call_id') in g.write_check_calls:
     value=message.get('content') or '';value=value if isinstance(value,str) else json.dumps(value)
     command_sha=g.write_check_calls[message['tool_call_id']]
     row.setdefault('write_check_outputs',[]).append({'call_id_sha256':hashlib.sha256(message['tool_call_id'].encode()).hexdigest(),'command_sha256':command_sha,'output_bytes':len(value.encode()),'output_sha256':hashlib.sha256(value.encode()).hexdigest(),'starts_with_write_ok':value.startswith('ok\\n'),'combined_write_and_shell_output':value.startswith('ok\\nexit status:')})"""
assert text.count(old)==1
text=text.replace(old,new)
old="""    if final is not None:row['output_encrypted_sha256']=[hashlib.sha256(x['encrypted_content'].encode()).hexdigest() for x in final.get('output',[]) if x.get('type')=='reasoning' and x.get('encrypted_content')]"""
new="""    if final is not None:
     row['output_encrypted_sha256']=[hashlib.sha256(x['encrypted_content'].encode()).hexdigest() for x in final.get('output',[]) if x.get('type')=='reasoning' and x.get('encrypted_content')]
     calls=[]
     for item in final.get('output',[]):
      if item.get('type')=='function_call' and item.get('name')=='write_file':
       try:args=json.loads(item.get('arguments') or '{}')
       except ValueError:args={}
       command=args.get('command');has_command=isinstance(command,str) and bool(command.strip())
       command_sha=hashlib.sha256(command.encode()).hexdigest() if has_command else None
       calls.append({'call_id_sha256':hashlib.sha256(item.get('call_id','').encode()).hexdigest(),'command_present':has_command,'command_sha256':command_sha})
       if has_command:g.write_check_calls[item.get('call_id')]=command_sha
     if calls:row['write_check_calls']=calls"""
assert text.count(old)==1
text=text.replace(old,new)
dest=screen/'confirmation_ext_screen.py'
dest.write_text(text)
digest=hashlib.sha256(dest.read_bytes()).hexdigest()
(screen/'observation-amendment.json').write_text(__import__('json').dumps({'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'extension_sha256':digest,'base_extension_sha256':hashlib.sha256(origin.read_bytes()).hexdigest(),'scope':'observation only; records whether a write_file response contained a nonempty command and whether its correlated tool output begins with the expected combined ok/exit-status prefix; stores hashes and byte counts only','behavior_changed':False,'applies_from_cell_index':2},indent=2)+'\n')
print(digest)
