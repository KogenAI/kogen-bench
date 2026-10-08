import subprocess,sys,time
from pathlib import Path
w=Path(sys.argv[1]);proof=w/'import-proof';csv=w/'probe.csv';csv.write_text('external_id,title,body\na,One,z\nb,Two,q\nc,Three,s\n')
expr='alias Trackline.{Repo,Support};Ecto.Adapters.SQL.Sandbox.mode(Repo,:auto);a=Trackline.AccountsFixtures.user_fixture();{:ok,o}=Support.create_organization(%{name: "Restart",slug: "restart"},a);{:ok,s}=Support.start_import(o,a,"'+str(csv)+'","restart");{:ok,l}=Support.Imports.claim(s.id,1000);{:ok,%{cursor: 1}}=Support.Imports.batch(s.id,l.lease,1);File.write!("'+str(proof)+'",Integer.to_string(s.id));receive do :never -> :ok end'
p=subprocess.Popen(['mix','run','-e',expr],cwd=w,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
end=time.monotonic()+30
while not proof.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.01)
assert proof.exists(),'import did not commit first batch'
p.kill();p.communicate();time.sleep(1.05)
id=int(proof.read_text())
expr='alias Trackline.{Repo,Support};Ecto.Adapters.SQL.Sandbox.mode(Repo,:auto);parent=self();claim=fn -> Task.async(fn -> send(parent,{:ready,self()});receive do :go -> :ok end;Support.Imports.claim('+str(id)+') end) end;a=claim.();b=claim.();receive do {:ready,p}->send(p,:go) end;receive do {:ready,p}->send(p,:go) end;results=[Task.await(a),Task.await(b)];[{:ok,l}]=Enum.filter(results,&match?({:ok,_},&1));1=Enum.count(results,&match?({:error,:leased},&1));{:ok,%{cursor: 3,status: "complete"}}=Support.Imports.batch(l.id,l.lease,100);org=Repo.get!(Support.Organization,l.organization_id);3=length(Support.list_tickets(org));actor=Repo.get!(Trackline.Accounts.User,l.actor_id);3=length(Support.Imports.progress(l.id,actor).rows);IO.puts("IMPORT_RESTART_RACE_PASS")'
p=subprocess.run(['mix','run','-e',expr],cwd=w,capture_output=True,text=True,timeout=30);print(p.stdout[-1000:]);print(p.stderr[-1000:]);assert p.returncode==0
