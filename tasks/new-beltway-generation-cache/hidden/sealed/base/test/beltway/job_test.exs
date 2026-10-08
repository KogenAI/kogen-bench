defmodule Beltway.JobTest do
  use ExUnit.Case, async: true

  alias Beltway.Job

  test "returns the value on success" do
    assert {:ok, 1} = Job.run(:j, fn -> {:ok, 1} end)
  end

  test "retries with linear backoff" do
    {:ok, agent} = Agent.start_link(fn -> [] end)
    sleeps = fn ms -> Agent.update(agent, &[ms | &1]) end
    fun = fn -> {:error, :nope} end

    assert {:error, :nope} = Job.run(:j, fun, max_attempts: 3, backoff_ms: 10, sleep: sleeps)
    assert Agent.get(agent, & &1) == [20, 10]
  end

  test "raised exceptions become errors" do
    assert {:error, {:raised, %RuntimeError{message: "x"}}} = Job.run(:j, fn -> raise "x" end)
  end
end
