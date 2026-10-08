defmodule BulkTransferTest do
 use TracklineWeb.ConnCase, async: false
 import Trackline.AccountsFixtures
 import Phoenix.LiveViewTest
 alias Trackline.Support
 alias Trackline.Support.{Ticket, TransferBatch, TransferAudit, Membership}
 alias Trackline.Repo
 setup do
   a=user_fixture(); b=user_fixture(); viewer=user_fixture()
   {:ok,o}=Support.create_organization(%{name: "Desk",slug: "bulk-#{System.unique_integer([:positive])}"},a)
   {:ok,_}=Support.add_member(o,b,"agent");{:ok,_}=Support.add_member(o,viewer,"viewer")
   {:ok,t}=Support.create_ticket(o,a,%{title: "One"});{:ok,u}=Support.create_ticket(o,a,%{title: "Two"})
   %{a: a,b: b,o: o,t: t,u: u,viewer: viewer}
 end
 defp rows(c), do: [%{id: c.t.id,version: 0},%{id: c.u.id,version: 0}]
 test "atomic transfer, durable replay, audit and dispatch",c do
   Phoenix.PubSub.subscribe(Trackline.PubSub,"transfers:#{c.o.id}")
   assert {:ok,result}=Support.bulk_reassign(c.o,c.a,rows(c),c.b,"k")
   assert result.tickets == [%{id: c.t.id,version: 1,assignee_id: c.b.id},%{id: c.u.id,version: 1,assignee_id: c.b.id}]
   refute_receive {:transfer_batch,_}
   assert Repo.aggregate(TransferBatch,:count)==1
   assert Repo.aggregate(TransferAudit,:count)==2
   assert {:ok,^result}=Support.bulk_reassign(c.o,c.a,Enum.reverse(rows(c)),c.b,"k")
   assert :ok=Trackline.Support.Transfer.dispatch(result.batch_id)
   assert_receive {:transfer_batch,^result}
   assert :ok=Trackline.Support.Transfer.dispatch(result.batch_id)
   refute_receive {:transfer_batch,_}
   assert {:error,:conflict}=Support.bulk_reassign(c.o,c.a,rows(c),nil,"k")
 end
 test "last stale row rolls back all changes",c do
   assert {:error,:stale}=Support.bulk_reassign(c.o,c.a,[%{id: c.t.id,version: 0},%{id: c.u.id,version: 9}],c.b,"bad")
   assert Repo.get!(Ticket,c.t.id).assignee_id==nil
   assert Repo.aggregate(TransferBatch,:count)==0
   assert Repo.aggregate(TransferAudit,:count)==0
 end
 test "tenant, target, size, duplicate and current membership boundaries",c do
   assert {:error,:forbidden}=Support.bulk_reassign(c.o,c.viewer,rows(c),c.b,"v")
   stranger=user_fixture()
   assert {:error,:target}=Support.bulk_reassign(c.o,c.a,rows(c),stranger,"s")
   assert {:error,:duplicate}=Support.bulk_reassign(c.o,c.a,[hd(rows(c)),hd(rows(c))],c.b,"d")
   assert {:error,:invalid}=Support.bulk_reassign(c.o,c.a,[],c.b,"e")
   assert {:error,:invalid}=Support.bulk_reassign(c.o,c.a,List.duplicate(hd(rows(c)),101),c.b,"e")
   {:ok,other}=Support.create_organization(%{name: "Other",slug: "other-#{System.unique_integer([:positive])}"},c.a)
   assert {:error,:not_found}=Support.bulk_reassign(other,c.a,rows(c),nil,"x")
   Repo.delete!(Support.get_membership(c.o,c.a))
   assert {:error,:forbidden}=Support.bulk_reassign(c.o,c.a,rows(c),nil,"revoked")
 end
 test "HTTP integration and live batch deduplication plus stale fencing",c do
   conn=log_in_user(build_conn(),c.a)
   assert {:ok,view,_}=live(conn,"/orgs/#{c.o.slug}/tickets")
   params=%{"rows"=>Enum.map(rows(c),fn r -> %{"id"=>r.id,"version"=>r.version} end),"target_id"=>c.b.id,"key"=>"http"}
   result=conn |> post("/orgs/#{c.o.slug}/tickets/bulk-reassign",params) |> json_response(200)
   batch=%{batch_id: result["batch_id"],tickets: Enum.map(result["tickets"],&%{id: &1["id"],version: &1["version"],assignee_id: &1["assignee_id"]})}
   send(view.pid,{:transfer_batch,batch});assert has_element?(view,"#ticket-#{c.t.id}",c.b.email)
   newer=%{batch_id: 99991,tickets: [%{id: c.t.id,version: 3,assignee_id: c.viewer.id}]}
   send(view.pid,{:transfer_batch,newer});assert has_element?(view,"#ticket-#{c.t.id}",c.viewer.email)
   send(view.pid,{:transfer_batch,batch});send(view.pid,{:transfer_batch,%{batch | batch_id: 99992}})
   assert has_element?(view,"#ticket-#{c.t.id}",c.viewer.email)
 end
end
