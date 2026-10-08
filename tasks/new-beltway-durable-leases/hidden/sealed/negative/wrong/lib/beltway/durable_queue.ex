defmodule Beltway.DurableQueue do
  use GenServer
  alias Beltway.Journal
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, Keyword.take(opts, [:name]))
  def init(opts) do
    case Journal.open(Keyword.fetch!(opts, :durable)) do
      {:ok, journal, old} ->
        old = old || %{ready: [], leased: %{}, seen: %{}, seq: 0}
        returned = old.leased |> Enum.sort_by(fn {_, l} -> l.seq end) |> Enum.map(fn {id, _} -> id end)
        data = %{old | ready: old.ready ++ returned, leased: %{}}
        :ok = Journal.append(journal, data)
        Process.send_after(self(), :tick, 10)
        {:ok, %{journal: journal, data: data, capacity: Keyword.fetch!(opts, :capacity)}}
      {:error, reason} -> {:stop, reason}
    end
  end
  def terminate(_, state), do: Journal.close(state.journal)
  def handle_info(:tick, state) do
    Process.send_after(self(), :tick, 10)
    {:noreply, expire(state)}
  end
  def handle_call(msg, _, state), do: dispatch(msg, expire(state))
  defp dispatch({:enqueue, id, payload}, s) do
    cond do
      Map.has_key?(s.data.seen, id) -> reply(if(s.data.seen[id] == payload, do: :ok, else: {:error, :conflict}), s)
      length(s.data.ready) + map_size(s.data.leased) >= s.capacity -> reply({:error, :full}, s)
      true -> save(:ok, s, %{s.data | ready: s.data.ready ++ [id], seen: Map.put(s.data.seen, id, payload)})
    end
  end
  defp dispatch({:lease, owner, ttl}, s) when is_integer(ttl) and ttl > 0 do
    case s.data.ready do
      [] -> reply(:empty, s)
      [id | rest] ->
        token = :crypto.strong_rand_bytes(24)
        seq = s.data.seq + 1
        l = %{token: token, owner: owner, until: now() + ttl, seq: seq}
        save({:ok, id, s.data.seen[id], token}, s, %{s.data | ready: rest, leased: Map.put(s.data.leased, id, l), seq: seq})
    end
  end
  defp dispatch({:lease, _, _}, s), do: reply({:error, :invalid_ttl}, s)
  defp dispatch({op, id, _token}, s) when op in [:ack, :nack] do
    case Map.get(s.data.leased, id) do
      %{token: _current} ->
        d = %{s.data | leased: Map.delete(s.data.leased, id)}
        d = if op == :nack, do: %{d | ready: d.ready ++ [id]}, else: d
        save(:ok, s, d)
      _ -> reply({:error, :stale}, s)
    end
  end
  defp dispatch(:size, s), do: reply(length(s.data.ready) + map_size(s.data.leased), s)
  defp dispatch(:stats, s), do: reply(%{ready: length(s.data.ready), leased: map_size(s.data.leased), size: length(s.data.ready) + map_size(s.data.leased), waiting_pushers: 0, waiting_poppers: 0}, s)
  defp dispatch(_, s), do: reply({:error, :durable_api_required}, s)
  defp expire(s) do
    expired = s.data.leased |> Enum.filter(fn {_, l} -> l.until <= now() end) |> Enum.sort_by(fn {_, l} -> l.seq end) |> Enum.map(&elem(&1, 0))
    if expired == [] do s else
      d = %{s.data | ready: s.data.ready ++ expired, leased: Map.drop(s.data.leased, expired)}
      :ok = Journal.append(s.journal, d)
      %{s | data: d}
    end
  end
  defp save(result, s, data) do
    :ok = Journal.append(s.journal, data)
    reply(result, %{s | data: data})
  end
  defp reply(r, s), do: {:reply, r, s}
  defp now, do: System.monotonic_time(:millisecond)
end
