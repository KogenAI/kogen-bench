defmodule PipelineTest do
 use ExUnit.Case, async: false
 defp opts(ms), do: [deadline: System.monotonic_time(:millisecond)+ms,max_concurrency: 2,max_pending: 2,max_output: 100]
 test "ordered output, exact cap and nonzero exit" do
   assert [{:ok,%{status: 0,output: "a"}},{:ok,%{status: 0,output: "b"}}]=Beltway.run_pipeline(["a","b"],{"/bin/echo",["-n"]},opts(5000))
   assert [{:ok,%{output: out}}]=Beltway.run_pipeline([String.duplicate("x",100)],{"/bin/echo",["-n"]},opts(5000));assert byte_size(out)==100
   assert [{:error,:output_limit,out}]=Beltway.run_pipeline([String.duplicate("x",101)],{"/bin/echo",["-n"]},opts(5000));assert byte_size(out)==100
   assert [{:ok,%{status: 7}}]=Beltway.run_pipeline([""],{"/bin/sh",["-c","exit 7","--"]},opts(5000))
 end
 test "expired absolute deadline starts nothing" do
   assert [{:error,:deadline,""},{:error,:deadline,""}]=Beltway.run_pipeline(["a","b"],{"/bin/echo",[]},opts(-1))
 end
 test "deadline is shared across all waves" do
   began=System.monotonic_time(:millisecond)
   result=Beltway.run_pipeline(List.duplicate("",12),{"/bin/sh",["-c","sleep 0.2","--"]},opts(350))
   assert Enum.any?(result,&match?({:error,:deadline,_},&1))
   assert System.monotonic_time(:millisecond)-began<3000
 end
 test "cancel is idempotent and prevents queued commands" do
   {:ok,h}=Beltway.Pipeline.start(List.duplicate("",10),{"/bin/sh",["-c","sleep 5","--"]},opts(10000))
   assert :ok=Beltway.Pipeline.cancel(h)
   assert :ok=Beltway.Pipeline.cancel(h)
   assert Enum.all?(Beltway.Pipeline.await(h),&match?({:error,:cancelled,_},&1))
 end
end
