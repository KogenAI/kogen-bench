defmodule Beltway.Test.Helpers do
  @moduledoc false
  import ExUnit.Assertions

  @doc "Polls `fun` until it returns a truthy value or `timeout` ms of real time pass (an observation loop, not a timing assumption)."
  def eventually(fun, timeout \\ 2_000) do
    deadline = System.monotonic_time(:millisecond) + timeout
    do_eventually(fun, deadline)
  end

  defp do_eventually(fun, deadline) do
    case fun.() do
      x when x in [nil, false] ->
        if System.monotonic_time(:millisecond) > deadline do
          flunk("condition not reached in time")
        else
          receive do
          after
            1 -> do_eventually(fun, deadline)
          end
        end

      x ->
        x
    end
  end

  @doc "True when the process has blocked in a receive."
  def waiting?(pid), do: Process.info(pid, :status) == {:status, :waiting}
end
