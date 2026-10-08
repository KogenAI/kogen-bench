defmodule Beltway.Queue do
  @moduledoc """
  Bounded FIFO queue process.

  `push/2` and `pop/1` never block: they return `{:error, :full}` / `:empty` when the
  queue cannot take or give an item right now.
  """
  use GenServer

  def start_link(opts) do
    GenServer.start_link(__MODULE__, Keyword.fetch!(opts, :capacity), Keyword.take(opts, [:name]))
  end

  @spec push(GenServer.server(), term()) :: :ok | {:error, :full}
  def push(queue, item), do: GenServer.call(queue, {:push, item})

  @spec pop(GenServer.server()) :: {:ok, term()} | :empty
  def pop(queue), do: GenServer.call(queue, :pop)

  def size(queue), do: GenServer.call(queue, :size)

  @doc "`%{size: n, waiting_poppers: n, waiting_pushers: n}`"
  def stats(queue), do: GenServer.call(queue, :stats)

  @impl true
  def init(capacity), do: {:ok, %{capacity: capacity, items: :queue.new(), size: 0}}

  @impl true
  def handle_call({:push, _item}, _from, %{size: size, capacity: cap} = state) when size >= cap do
    {:reply, {:error, :full}, state}
  end

  def handle_call({:push, item}, _from, state) do
    {:reply, :ok, %{state | items: :queue.in(item, state.items), size: state.size + 1}}
  end

  def handle_call(:pop, _from, state) do
    case :queue.out(state.items) do
      {{:value, item}, rest} ->
        {:reply, {:ok, item}, %{state | items: rest, size: state.size - 1}}

      {:empty, _} ->
        {:reply, :empty, state}
    end
  end

  def handle_call(:size, _from, state), do: {:reply, state.size, state}

  def handle_call(:stats, _from, state) do
    {:reply, %{size: state.size, waiting_poppers: 0, waiting_pushers: 0}, state}
  end
end
