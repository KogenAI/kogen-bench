defmodule Beltway.FetcherTest do
  use ExUnit.Case, async: true

  alias Beltway.Fetcher

  test "returns the body" do
    assert {:ok, "body"} = Fetcher.fetch("http://x", http: fn _ -> {:ok, "body"} end, retry_delay: 0)
  end

  test "gives up after three attempts" do
    {:ok, agent} = Agent.start_link(fn -> 0 end)
    http = fn _ -> Agent.update(agent, &(&1 + 1)) && {:error, :timeout} end
    assert {:error, :timeout} = Fetcher.fetch("http://x", http: http, retry_delay: 0)
    assert Agent.get(agent, & &1) == 3
  end
end
