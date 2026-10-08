import sys,os,subprocess,selectors,time,signal,base64
jobs,pending,limit,remaining,nargs=map(int,sys.argv[1:6]);cmd=sys.argv[6:6+nargs];items=sys.argv[6+nargs:]
sel=selectors.DefaultSelector();sel.register(sys.stdin.buffer,selectors.EVENT_READ,'control')
end=time.monotonic()+max(0,remaining)/1000;active={};next_item=0;stopped=None
def shutdown(*_):
 global stopped
 stopped='cancelled'
signal.signal(signal.SIGTERM,shutdown)

def kill(p):
 try:p.kill()
 except (ProcessLookupError,PermissionError):
  if p.poll() is None:p.kill()
 p.wait()
def emit(i,status,out=b''):
 print(str(i)+'\t'+status+'\t'+base64.b64encode(out).decode(),flush=True)
def complete(pid,status):
 x=active.pop(pid);sel.unregister(x['p'].stdout);kill(x['p']);emit(x['i'],status,x['out'])
try:
 while active or next_item<len(items):
  if stopped is None and time.monotonic()>=end:stopped='deadline'
  if stopped:
   for pid in list(active):complete(pid,stopped)
   while next_item<len(items):emit(next_item,stopped);next_item+=1
   break
  while len(active)<jobs and next_item<len(items) and time.monotonic()<end:
   p=subprocess.Popen(cmd+[items[next_item]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
   os.set_blocking(p.stdout.fileno(),False)
   active[p.pid]={'p':p,'i':next_item,'out':b''};next_item+=1;sel.register(p.stdout,selectors.EVENT_READ,p.pid)
  for key,_ in sel.select(max(0,min(.02,end-time.monotonic()))):
   if key.data=='control':
    data=os.read(key.fileobj.fileno(),4096)
    if not data or b'cancel' in data:stopped='cancelled'
   elif key.data in active:
    x=active[key.data];data=os.read(key.fileobj.fileno(),min(4096,limit-len(x['out'])+1))
    if not data:
     status=x['p'].wait();complete(key.data,'ok:'+str(status))
    elif len(x['out'])+len(data)>limit:
     x['out']+=data[:limit-len(x['out'])];complete(key.data,'output_limit')
    else:x['out']+=data
finally:
 for x in active.values():kill(x['p'])
