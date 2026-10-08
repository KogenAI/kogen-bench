defmodule Beltway.Ingest.DurableConsumer do
  use GenServer
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts)
  def init(opts) do
    Process.send_after(self(), :consume, 20)
    {:ok, opts}
  end
  def handle_info(:consume, opts) do
    q = Process.whereis(Keyword.fetch!(opts, :queue_name))
    if q do
      case Beltway.Queue.lease(q, self(), 1000) do
        {:ok, id, payload, token} ->
          send(Keyword.fetch!(opts, :collector), {:durable_item, id, payload})
          Beltway.Queue.ack(q, id, token)
        :empty -> :ok
      end
    end
    Process.send_after(self(), :consume, 20)
    {:noreply, opts}
  end
end
