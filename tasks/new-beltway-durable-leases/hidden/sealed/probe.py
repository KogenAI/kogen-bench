import subprocess,sys,os,time
from pathlib import Path
w=Path(sys.argv[1]);journal=w/'killed.journal';ack=w/'sync-ack'
expr='{:ok,q}=Beltway.Queue.start_link(durable: "'+str(journal)+'",capacity: 2);:ok=Beltway.Queue.enqueue(q,"durable",%{n: 7});File.write!("'+str(ack)+'","synced");receive do :never -> :ok end'
p=subprocess.Popen(['mix','run','-e',expr],cwd=w,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
deadline=time.monotonic()+30
while not ack.exists() and p.poll() is None and time.monotonic()<deadline:time.sleep(.01)
assert ack.exists(),'queue failed before sync acknowledgement'
p.kill();p.communicate()
expr='{:ok,q}=Beltway.Queue.start_link(durable: "'+str(journal)+'",capacity: 2);{:ok,"durable",%{n: 7},t}=Beltway.Queue.lease(q,self(),10000);:ok=Beltway.Queue.ack(q,"durable",t);:ok=Beltway.Queue.enqueue(q,"durable",%{n: 7});:empty=Beltway.Queue.lease(q,self(),10000);GenServer.stop(q)'
p=subprocess.run(['mix','run','-e',expr],cwd=w,capture_output=True,text=True,timeout=30);print(p.stdout[-1000:]);print(p.stderr[-1000:]);assert p.returncode==0
expr='{:ok,io}=StringIO.open("");0=Beltway.CLI.run(["queue-stats","'+str(journal)+'"],stdout: io);{_,"ready 0\\nleased 0\\n"}=StringIO.contents(io)'
p=subprocess.run(['mix','run','-e',expr],cwd=w,capture_output=True,text=True,timeout=30);print(p.stdout[-1000:]);print(p.stderr[-1000:]);assert p.returncode==0
print('SYNC_RESTART_PROBE_PASS')
