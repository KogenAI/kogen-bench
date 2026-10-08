defmodule ResumableImportTest do
 use TracklineWeb.ConnCase, async: false
 import Trackline.AccountsFixtures
 import Phoenix.LiveViewTest
 alias Trackline.Support
 alias Trackline.Support.{Imports, Ticket, ImportRow, ImportSession}
 alias Trackline.Repo
 setup do
   a=user_fixture();v=user_fixture()
   {:ok,o}=Support.create_organization(%{name: "Desk",slug: "import-#{System.unique_integer([:positive])}"},a)
   {:ok,_}=Support.add_member(o,v,"viewer")
   path=Path.join(System.tmp_dir!(),"csv-#{System.unique_integer([:positive])}")
   File.write!(path,<<239,187,191>> <> "external_id,title,body\r\na,One,\"line1\nline2\"\r\nb,Two,\"he said \"\"yes\"\"\"\r\na,Duplicate,x\r\nc,,invalid\r\nd,Last,z\r\n")
   on_exit(fn -> for p <- Path.wildcard(path<>"*"), do: File.rm(p) end)
   %{a: a,v: v,o: o,path: path}
 end
 test "logical records, bounded commits, replay and ordered errors",c do
   assert {:ok,s}=Support.start_import(c.o,c.a,c.path,"key")
   assert {:ok,same}=Support.start_import(c.o,c.a,c.path,"key");assert same.id==s.id
   assert {:ok,lease}=Imports.claim(s.id)
   assert {:ok,p}=Imports.batch(s.id,lease.lease,2);assert p.cursor==2;assert p.status=="running"
   assert Repo.get_by!(Ticket,organization_id: c.o.id,external_id: "a").body=="line1\nline2"
   assert Repo.get_by!(Ticket,organization_id: c.o.id,external_id: "b").body=="he said \"yes\""
   assert {:ok,p}=Imports.batch(s.id,lease.lease,2);assert p.cursor==4
   assert {:ok,p}=Imports.batch(s.id,lease.lease,2);assert p.cursor==5;assert p.status=="complete"
   errors=Imports.progress(s.id,c.a).rows |> Enum.filter(& &1.error)
   assert Enum.map(errors,& &1.row)==[3,4]
   assert Repo.aggregate(ImportRow,:count)==5
   assert Repo.aggregate(Ticket,:count)==3
   assert {:error,:stopped}=Imports.claim(s.id)
   File.write!(c.path,"external_id,title,body\nx,Different,z\n")
   assert {:error,:conflict}=Support.start_import(c.o,c.a,c.path,"key")
 end
 test "replacement lease rejects the old token and cancellation retains committed cursor",c do
   {:ok,s}=Support.start_import(c.o,c.a,c.path,"k")
   {:ok,l}=Imports.claim(s.id)
   assert {:error,:leased}=Imports.claim(s.id)
   {:ok,p}=Imports.batch(s.id,l.lease,1)
   Repo.update!(Ecto.Changeset.change(p,lease_until: 0))
   {:ok,new}=Imports.claim(s.id)
   assert new.lease != l.lease
   assert {:error,:stale}=Imports.batch(s.id,l.lease,1)
   assert Repo.get!(ImportSession,s.id).cursor==1
   assert {:ok,cancelled}=Support.cancel_import(s,c.a);assert cancelled.cursor==1
   assert {:error,:stale}=Imports.batch(s.id,new.lease,1)
   assert Repo.aggregate(Ticket,:count)==1
 end
 test "revocation, isolation, read authorization and progress LiveView",c do
   assert {:error,:forbidden}=Support.start_import(c.o,c.v,c.path,"viewer")
   {:ok,s}=Support.start_import(c.o,c.a,c.path,"k")
   conn=log_in_user(build_conn(),c.a)
   assert {:ok,view,_}=live(conn,"/orgs/#{c.o.slug}/imports/#{s.id}")
   assert has_element?(view,"#import-progress[data-cursor='0']")
   {:ok,l}=Imports.claim(s.id)
   Repo.delete!(Support.get_membership(c.o,c.a))
   assert {:ok,%{status: "revoked"}}=Imports.batch(s.id,l.lease,1)
   assert Repo.aggregate(Ticket,:count)==0
   assert {:error,:forbidden}=Imports.progress(s.id,c.a)
   stranger=user_fixture();assert {:error,:forbidden}=Imports.progress(s.id,stranger)
   {:ok,other}=Support.create_organization(%{name: "Other",slug: "isolate-#{System.unique_integer([:positive])}"},stranger)
   {:ok,s2}=Support.start_import(other,stranger,c.path,"k");{:ok,l2}=Imports.claim(s2.id)
   assert {:ok,_}=Imports.batch(s2.id,l2.lease,2)
   assert Repo.aggregate(Ticket,:count)==2
 end
 test "quoted fields cross IO boundaries and EOF record without newline",c do
   body=String.duplicate("z",4090) <> "\nnext"
   File.write!(c.path,"external_id,title,body\nx,Wide,\""<>body<>"\"")
   {:ok,s}=Support.start_import(c.o,c.a,c.path,"boundary");{:ok,l}=Imports.claim(s.id)
   assert {:ok,%{status: "complete",cursor: 1}}=Imports.batch(s.id,l.lease,1)
   assert Repo.get_by!(Ticket,external_id: "x").body==body
 end
end
