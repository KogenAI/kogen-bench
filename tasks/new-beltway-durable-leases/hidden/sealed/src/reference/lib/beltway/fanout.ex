defmodule Beltway.Fanout do
  @moduledoc """
  Runs a function over a list of items concurrently.

  Returns `[{item, {:ok, value}}]` in input order. Options: `:timeout` (ms, default 5000).
  """

  def run(items, fun, opts \\ []) when is_function(fun, 1) do
    timeout = Keyword.get(opts, :timeout, 5_000)

    items
    |> Enum.map(fn item -> {item, Task.async(fn -> fun.(item) end)} end)
    |> Enum.map(fn {item, task} -> {item, {:ok, Task.await(task, timeout)}} end)
  end
end
