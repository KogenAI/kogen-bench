defmodule Beltway.RetryTest do
  use ExUnit.Case, async: true

  alias Beltway.Retry

  defp flaky(fail_times) do
    {:ok, agent} = Agent.start_link(fn -> 0 end)

    fn ->
      n = Agent.get_and_update(agent, &{&1 + 1, &1 + 1})
      if n <= fail_times, do: {:error, {:fail, n}}, else: {:ok, n}
    end
  end

  test "retries until success" do
    assert {:ok, 3} = Retry.run(flaky(2), 5, 0)
  end

  test "gives up after max attempts with the last error" do
    assert {:error, {:fail, 3}} = Retry.run(flaky(10), 3, 0)
  end

  test "exceptions are failures" do
    assert {:error, {:exception, %RuntimeError{}}} = Retry.run(fn -> raise "x" end, 2, 0)
  end
end
