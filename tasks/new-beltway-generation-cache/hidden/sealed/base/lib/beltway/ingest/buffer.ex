defmodule Beltway.Ingest.Buffer do
  @moduledoc "Holds parsed items until the sink drains them. Registered under its module name."
  use GenServer

  def start_link(_opts \\ []), do: GenServer.start_link(__MODULE__, [], name: __MODULE__)

  def add(pid \\ __MODULE__, item), do: GenServer.call(pid, {:add, item})
  def items(pid \\ __MODULE__), do: GenServer.call(pid, :items)
  def drain(pid \\ __MODULE__), do: GenServer.call(pid, :drain)

  @impl true
  def init(_), do: {:ok, []}

  @impl true
  def handle_call({:add, item}, _from, items), do: {:reply, :ok, items ++ [item]}
  def handle_call(:items, _from, items), do: {:reply, items, items}
  def handle_call(:drain, _from, items), do: {:reply, items, []}
end
