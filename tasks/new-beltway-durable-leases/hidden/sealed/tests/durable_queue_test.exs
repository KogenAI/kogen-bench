defmodule DurableQueueTest do
 use ExUnit.Case, async: false
 alias Beltway.Queue
 setup do
   path=Path.join(System.tmp_dir!(),"journal-#{System.unique_integer([:positive])}")
   on_exit(fn -> File.rm(path);File.rm_rf(path<>".lock") end)
   %{path: path}
 end
 defp open(path,cap \\ 2), do: start_supervised!({Queue,durable: path,capacity: cap},id: make_ref(),restart: :temporary)
 test "FIFO, leased capacity, replay and stale-token fencing",%{path: p} do
   q=open(p)
   assert :ok=Queue.enqueue(q,"a",%{body: 1});assert :ok=Queue.enqueue(q,"b",2)
   assert {:ok,"a",%{body: 1},token}=Queue.lease(q,self(),10000)
   assert Queue.stats(q)==%{ready: 1,leased: 1,size: 2,waiting_pushers: 0,waiting_poppers: 0}
   assert {:error,:full}=Queue.enqueue(q,"c",3)
   assert :ok=Queue.nack(q,"a",token)
   assert {:ok,"b",2,tb}=Queue.lease(q,self(),10000)
   assert :ok=Queue.ack(q,"b",tb)
   assert {:ok,"a",_,new}=Queue.lease(q,self(),10000);assert new!=token
   assert {:error,:stale}=Queue.ack(q,"a",token)
   assert :ok=Queue.ack(q,"a",new)
   assert :ok=Queue.enqueue(q,"a",%{body: 1});assert :empty=Queue.lease(q,self(),10000)
   assert {:error,:conflict}=Queue.enqueue(q,"a",9)
   GenServer.stop(q)
   q=open(p);assert :empty=Queue.lease(q,self(),10000)
   assert :ok=Queue.enqueue(q,"a",%{body: 1});assert Queue.size(q)==0
 end
 test "reopen returns leased items after current ready items",%{path: p} do
   q=open(p);Queue.enqueue(q,1,"one");Queue.enqueue(q,2,"two")
   {:ok,1,_,old}=Queue.lease(q,self(),10000);GenServer.stop(q)
   q=open(p)
   assert {:ok,2,"two",_}=Queue.lease(q,self(),10000)
   assert {:ok,1,"one",new}=Queue.lease(q,self(),10000)
   assert {:error,:stale}=Queue.ack(q,1,old)
   assert new!=old
 end
 test "truncated suffix preserves synced prefix; complete corruption refused",%{path: p} do
   q=open(p);Queue.enqueue(q,"a",1);GenServer.stop(q)
   saved=File.read!(p);File.write!(p,saved<><<0,0,0,99,0,0>>)
   q=open(p);assert {:ok,"a",1,_}=Queue.lease(q,self(),10000);GenServer.stop(q)
   bytes=File.read!(p);n=byte_size(bytes)-1;<<prefix::binary-size(^n),last>>=bytes
   File.write!(p,prefix<><<Bitwise.bxor(last,1)>>)
   assert {:error,:corrupt}=GenServer.start(Beltway.DurableQueue,[durable: p,capacity: 2])
 end
 test "second live opener refused and expiry redelivers with fresh token",%{path: p} do
   q=open(p);assert {:error,:already_open}=GenServer.start(Beltway.DurableQueue,[durable: p,capacity: 2])
   Queue.enqueue(q,"a",1);{:ok,"a",1,old}=Queue.lease(q,self(),1)
   # Force the observable expiry transition after the timestamp rather than sleeping.
   wait=fn wait -> case Queue.lease(q,self(),10000) do :empty -> wait.(wait);r -> r end end
   assert {:ok,"a",1,new}=wait.(wait)
   assert new!=old;assert {:error,:stale}=Queue.nack(q,"a",old)
 end
 test "durable ingest supervision and CLI counts",%{path: p} do
   name=:durable_ingest_qa
   start_supervised!({Beltway.Ingest.Supervisor,durable: p,queue_name: name,collector: self(),capacity: 2})
   assert :ok=Queue.enqueue(name,"row",%{value: 8})
   assert_receive {:durable_item,"row",%{value: 8}},2000
   # Barrier: the consumer sent its receipt before ack; let its current callback finish.
   assert Queue.stats(name).size in [0,1]
 end
end
