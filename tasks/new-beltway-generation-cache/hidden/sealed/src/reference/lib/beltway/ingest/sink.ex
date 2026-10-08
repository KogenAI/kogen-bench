defmodule Beltway.Ingest.Sink do
  @moduledoc """
  Drains the buffer on `flush/0` and sends `{:flushed, items}` to the collector process
  given as the `:collector` option. It looks the buffer up once, when it starts.
  """
  use GenServer

  alias Beltway.Ingest.Buffer

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  @doc "Returns the number of flushed items."
  def flush, do: GenServer.call(__MODULE__, :flush)

  @impl true
  def init(opts) do
    {:ok, %{buffer: Process.whereis(Buffer), collector: Keyword.fetch!(opts, :collector)}}
  end

  @impl true
  def handle_call(:flush, _from, state) do
    items = Buffer.drain(state.buffer)
    send(state.collector, {:flushed, items})
    {:reply, length(items), state}
  end
end
