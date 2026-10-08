defmodule Kogen.Core do
  @moduledoc "JSONL job event append and reconciliation."

  @spec fail(String.t()) :: no_return()
  defp fail(message), do: raise(Kogen.Error, message: message, code: 1)
  defp invalid(line), do: "eventlog:#{line}: invalid event"

  defp decode(raw, line) do
    if duplicate_keys?(raw), do: fail(invalid(line))

    case Jason.decode(raw) do
      {:ok, map} when is_map(map) -> event_from_map(map, line)
      _ -> fail(invalid(line))
    end
  end

  defp duplicate_keys?(raw) do
    Enum.any?(~w(id type job ts), fn key ->
      Regex.scan(~r/"#{key}"\s*:/, raw) |> length() > 1
    end)
  end

  defp event_from_map(map, line) do
    if map_size(map) != 4, do: fail(invalid(line))
    id = Map.get(map, "id")
    type = Map.get(map, "type")
    job = Map.get(map, "job")
    ts = Map.get(map, "ts")
    validate_event(id, type, job, ts, line)
  end

  defp validate_event(id, type, job, ts, line) do
    if not valid_fields?(id, type, job, ts), do: fail(invalid(line))
    if not valid_identifiers?(id, job), do: fail(invalid(line))

    if type not in ~w(created started completed failed),
      do: fail("eventlog:#{line}: unknown event type '#{type}'")

    %{id: id, type: type, job: job, ts: ts, line: line}
  end

  defp valid_fields?(id, type, job, ts) do
    is_binary(id) and is_binary(type) and is_binary(job) and is_integer(ts) and ts >= 0 and
      ts <= 9_223_372_036_854_775_807
  end

  defp valid_identifiers?(id, job) do
    Regex.match?(~r/\Ae-[a-z0-9]{1,16}\z/, id) and
      Regex.match?(~r/\A[a-z][a-z0-9-]{0,31}\z/, job)
  end

  defp read(path) do
    case File.read(path) do
      {:ok, data} -> events_from_data(data)
      {:error, :enoent} -> []
      {:error, _} -> fail("eventlog: cannot access log")
    end
  end

  defp events_from_data(""), do: []

  defp events_from_data(data) do
    data
    |> String.split("\n")
    |> Enum.drop(-1)
    |> Enum.with_index(1)
    |> Enum.map(fn {row, line} -> decode(row, line) end)
    |> ensure_unique_ids()
  end

  defp ensure_unique_ids(events) do
    {reversed, _ids} =
      Enum.reduce(events, {[], MapSet.new()}, fn e, {acc, ids} ->
        if MapSet.member?(ids, e.id),
          do: fail("eventlog:#{e.line}: duplicate event id '#{e.id}'")

        {[e | acc], MapSet.put(ids, e.id)}
      end)

    Enum.reverse(reversed)
  end

  defp reconcile(events) do
    ordered = Enum.sort_by(events, &{&1.ts, &1.line})
    states = Enum.reduce(ordered, {%{}, %{}}, &advance/2) |> elem(0)
    counts = Enum.frequencies(Map.values(states))

    "total=#{map_size(states)}\nqueued=#{Map.get(counts, "queued", 0)}\nrunning=#{Map.get(counts, "running", 0)}\ndone=#{Map.get(counts, "done", 0)}\nfailed=#{Map.get(counts, "failed", 0)}\n"
  end

  defp advance(event, {states, times}) do
    job = event.job
    if Map.get(times, job) == event.ts, do: transition_error(event)
    current = Map.get(states, job, "")
    next = next_state(current, event.type, event)
    {Map.put(states, job, next), Map.put(times, job, event.ts)}
  end

  defp next_state("", "created", _event), do: "queued"
  defp next_state("queued", "started", _event), do: "running"
  defp next_state("running", "completed", _event), do: "done"
  defp next_state("running", "failed", _event), do: "failed"
  defp next_state(_state, _type, event), do: transition_error(event)

  @spec transition_error(map()) :: no_return()
  defp transition_error(event),
    do: fail("eventlog:#{event.line}: invalid transition for job '#{event.job}'")

  defp append(path, raw) do
    event = decode(raw, 1)
    existing_data = read_append_log(path)
    if truncated?(existing_data), do: fail(invalid(line_count(existing_data) + 1))
    existing = events_from_data(existing_data)
    reject_duplicate_id(existing, event)
    append_line(path, event)
  end

  defp read_append_log(path) do
    case File.read(path) do
      {:ok, data} -> data
      {:error, :enoent} -> ""
      {:error, _} -> fail("eventlog: cannot access log")
    end
  end

  defp truncated?(data), do: byte_size(data) > 0 and :binary.last(data) != 10
  defp line_count(data), do: length(:binary.matches(data, "\n"))

  defp reject_duplicate_id(events, event) do
    case Enum.find(events, &(&1.id == event.id)) do
      nil -> :ok
      found -> fail("eventlog:#{found.line}: duplicate event id '#{event.id}'")
    end
  end

  defp append_line(path, event) do
    encoded =
      "{\"id\":" <>
        Jason.encode!(event.id) <>
        ",\"type\":" <>
        Jason.encode!(event.type) <>
        ",\"job\":" <>
        Jason.encode!(event.job) <> ",\"ts\":" <> Integer.to_string(event.ts) <> "}\n"

    case File.write(path, encoded, [:append, :binary]) do
      {:error, _} -> fail("eventlog: cannot access log")
      :ok -> "appended #{event.id}\n"
    end
  end

  def execute(["reconcile", "--log", path]), do: reconcile(read(path))
  def execute(["append", "--log", path, "--event", raw]), do: append(path, raw)
  def execute(_), do: raise(Kogen.Error, message: "eventlog: usage error", code: 2)
end
