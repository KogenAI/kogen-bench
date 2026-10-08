alias Trackline.{Repo,Support}
alias Trackline.Support.{TransferBatch,TransferAudit}
Ecto.Adapters.SQL.Sandbox.mode(Repo,:auto)
u=Trackline.AccountsFixtures.user_fixture()
{:ok,o}=Support.create_organization(%{name: "Race",slug: "race-#{System.unique_integer([:positive])}"},u)
{:ok,t}=Support.create_ticket(o,u,%{title: "Race"})
parent=self()
launch=fn key -> Task.async(fn -> send(parent,{:ready,self()});receive do :go -> :ok end;Support.bulk_reassign(o,u,[%{id: t.id,version: 0}],nil,key) end) end
a=launch.("a");b=launch.("b")
receive do {:ready,p}->send(p,:go) end
receive do {:ready,p}->send(p,:go) end
results=[Task.await(a),Task.await(b)]
1=Enum.count(results,&match?({:ok,_},&1));1=Enum.count(results,&match?({:error,:stale},&1))
{:ok,t}=Support.create_ticket(o,u,%{title: "Replay"})
launch=fn ->Task.async(fn->Support.bulk_reassign(o,u,[%{id: t.id,version: 0}],nil,"same") end) end
a=launch.();b=launch.();{:ok,r}=Task.await(a);{:ok,^r}=Task.await(b)
import Ecto.Query
2=Repo.aggregate(from(b in TransferBatch,where: b.organization_id==^o.id),:count)
IO.puts("INDEPENDENT_CONNECTION_RACE_PASS")
