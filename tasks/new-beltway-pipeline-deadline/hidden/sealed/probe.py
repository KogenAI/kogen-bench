import subprocess,sys,os,time
from pathlib import Path
w=Path(sys.argv[1])
for mode in ['cancel','deadline','owner_down']:
 pidfile=w/(mode+'.pid');heartbeat=w/(mode+'.escaped');release=w/(mode+'.release')
 child=w/(mode+'.py');child.write_text('import os,signal,time\nfrom pathlib import Path\nsignal.signal(signal.SIGTERM,signal.SIG_IGN)\nPath('+repr(str(pidfile))+').write_text(str(os.getpid()))\nwhile not Path('+repr(str(release))+').exists(): time.sleep(.005)\nPath('+repr(str(heartbeat))+').write_text("alive")\ntime.sleep(30)\n')
 opts='[deadline: System.monotonic_time(:millisecond)+'+('350' if mode=='deadline' else '10000')+',max_concurrency: 1,max_pending: 1,max_output: 100]'
 start='Beltway.Pipeline.start([""],{"/bin/sh",["-c", "python3 '+str(child)+' & wait", "--"]},'+opts+')'
 barrier='wait=fn wait -> if File.exists?("'+str(pidfile)+'"), do: :ok, else: (Process.sleep(5);wait.(wait)) end;wait.(wait);'
 if mode=='owner_down':
  expr='parent=self();owner=spawn(fn -> {:ok,h}='+start+';send(parent,{:handle,h});receive do :never -> :ok end end);receive do {:handle,h}->'+barrier+'ref=Process.monitor(h);Process.exit(owner,:kill);receive do {:DOWN,^ref,:process,^h,_}->:ok after 5000->raise "coordinator leaked" end end'
 else:
  expr='{:ok,h}='+start+';'+barrier+('Beltway.Pipeline.cancel(h);' if mode=='cancel' else '')+'IO.inspect(Beltway.Pipeline.await(h))'
 p=subprocess.run(['mix','run','-e',expr],cwd=w,timeout=20,capture_output=True,text=True)
 print(mode,p.stdout[-500:],p.stderr[-500:]);assert p.returncode==0
 assert pidfile.exists();pid=int(pidfile.read_text());release.write_text('go')
 end=time.monotonic()+2
 while time.monotonic()<end and not heartbeat.exists():time.sleep(.01)
 escaped=heartbeat.exists()
 if escaped:subprocess.run(['/bin/kill','-9',str(pid)],capture_output=True)
 assert not escaped, 'descendant escaped '+mode
# Confirm the same concurrency bound across multiple waves using start/finish events.
log=w/'concurrency.log';script=w/'work.py';script.write_text('import os,time\np='+repr(str(log))+'\ndef event(kind):\n fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600);os.write(fd,(kind+"\\n").encode());os.close(fd)\nevent("start");time.sleep(.04);event("finish")\n')
expr='result=Beltway.run_pipeline(List.duplicate("",8),{"python3",["'+str(script)+'"]},[deadline: System.monotonic_time(:millisecond)+10000,max_concurrency: 2,max_pending: 2,max_output: 100]);8=length(result);true=Enum.all?(result,&match?({:ok,%{status: 0}},&1));receive do m -> raise "message leaked: #{inspect(m)}" after 0 -> :ok end'
p=subprocess.run(['mix','run','-e',expr],cwd=w,timeout=20,capture_output=True,text=True);print(p.stderr[-500:]);assert p.returncode==0
active=0;peak=0
for event in log.read_text().splitlines():active+=1 if event=='start' else -1;peak=max(peak,active);assert 0<=active<=2
assert active==0 and peak==2
print('DESCENDANT_OWNER_DEADLINE_CONCURRENCY_PROBE_PASS')
