defmodule GenerationCacheTest do
 use ExUnit.Case, async: false
 alias Beltway.Cache
 setup do
   c=start_supervised!({Cache,single_flight: true,ttl_ms: 1000,max_entries: 2,max_inflight: 1})
   %{c: c}
 end
 test "single flight and independent waiter deadlines",%{c: c} do
   parent=self()
   loader=fn -> send(parent,{:loader,self()});receive do :release -> {:ok,42} end end
   a=Task.async(fn -> Cache.fetch(c,:k,loader,5000) end)
   assert_receive {:loader,l}
   b=Task.async(fn -> Cache.fetch(c,:k,fn -> flunk("second loader") end,20) end)
   assert Task.await(b)=={:error,:timeout}
   assert Cache.flight_stats(c)==%{entries: 0,inflight: 1,waiters: 1}
   assert Cache.fetch(c,:other,fn -> {:ok,0} end,10)=={:error,:busy}
   send(l,:release);assert Task.await(a)=={:ok,42}
   assert Cache.fetch(c,:k,fn -> flunk("cached") end,20)=={:ok,42}
 end
 test "invalidation fences a suspended generation",%{c: c} do
   parent=self()
   a=Task.async(fn -> Cache.fetch(c,:k,fn -> send(parent,{:loader,self()});receive do :release -> {:ok,:old} end end,5000) end)
   assert_receive {:loader,l}
   monitor=Process.monitor(l)
   assert Cache.invalidate(c,:k)==:ok
   assert Task.await(a)=={:error,:invalidated}
   assert_receive {:DOWN,^monitor,:process,^l,:killed}
   assert Cache.fetch(c,:k,fn -> {:ok,:new} end,1000)=={:ok,:new}
   assert Cache.fetch(c,:k,fn -> flunk("cached") end,20)=={:ok,:new}
 end
 test "last abandoned waiter tears down loader and capacity recovers",%{c: c} do
   parent=self()
   caller=spawn(fn -> Cache.fetch(c,:k,fn -> send(parent,{:loader,self()});receive do :never -> {:ok,0} end end,5000) end)
   assert_receive {:loader,l}
   lm=Process.monitor(l);cm=Process.monitor(caller);Process.exit(caller,:kill)
   assert_receive {:DOWN,^cm,:process,^caller,:killed}
   assert_receive {:DOWN,^lm,:process,^l,:killed}
   assert Cache.flight_stats(c)==%{entries: 0,inflight: 0,waiters: 0}
   assert Cache.fetch(c,:next,fn -> {:ok,2} end,1000)=={:ok,2}
 end
 test "abrupt cache death kills its linked loader",%{c: c} do
   parent=self()
   caller=spawn(fn -> try do Cache.fetch(c,:k,fn -> send(parent,{:loader,self()});receive do :never -> {:ok,1} end end,5000) catch :exit,_ -> :ok end end)
   assert_receive {:loader,l}
   m=Process.monitor(l);cm=Process.monitor(caller)
   Process.exit(c,:kill)
   assert_receive {:DOWN,^m,:process,^l,:killed}
   assert_receive {:DOWN,^cm,:process,^caller,:normal}
 end
 test "loader failure is not cached and bounded eviction works",%{c: c} do
   assert Cache.fetch(c,:k,fn -> raise "oops" end,1000)=={:error,:loader_failed}
   assert Cache.fetch(c,:k,fn -> {:error,:unavailable} end,1000)=={:error,:unavailable}
   for k <- 1..5, do: assert(Cache.fetch(c,k,fn -> {:ok,k} end,1000)=={:ok,k})
   assert Cache.flight_stats(c).entries==2
   assert Cache.fetch(c,1,fn -> {:ok,:reload} end,1000)=={:ok,:reload}
 end
 test "injected monotonic clock expires cache entries exactly at TTL" do
   {:ok,clock}=Agent.start_link(fn -> 100 end)
   c=start_supervised!({Beltway.GenerationCache,ttl_ms: 10,max_entries: 2,max_inflight: 1,clock: fn -> Agent.get(clock,& &1) end})
   assert Cache.fetch(c,:x,fn -> {:ok,1} end,1000)=={:ok,1}
   Agent.update(clock,fn _ -> 110 end)
   assert Cache.fetch(c,:x,fn -> {:ok,2} end,1000)=={:ok,2}
 end
end
