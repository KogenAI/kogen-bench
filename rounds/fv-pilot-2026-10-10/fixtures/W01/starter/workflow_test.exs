defmodule WorkflowStarterTest do
  use ExUnit.Case, async: false
  test "start needs approval and ordinary approval admits" do
    state = Workflow.init()
    refute Workflow.step(state, :start).admitted
    approved = Workflow.step(state, :approve)
    assert approved.approved == :r1
    assert Workflow.step(approved, :start).admitted
    assert Workflow.step(state, :edit_r2).revision == :r2
  end
end
