defmodule Beltway.LogReader do
  @moduledoc """
  Summarizes a log file.

  `summarize/1` returns `%{lines: n, entries: n, malformed: n, by_level: %{level => n},
  first_ts: DateTime | nil, last_ts: DateTime | nil}`.
  """

  alias Beltway.Log

  def summarize(path) do
    path
    |> File.read!()
    |> String.split("\n", trim: true)
    |> Enum.reduce(empty(), fn line, acc ->
      {:ok, entry} = Log.parse_line(line)

      %{
        acc
        | lines: acc.lines + 1,
          entries: acc.entries + 1,
          by_level: Map.update(acc.by_level, entry.level, 1, &(&1 + 1)),
          first_ts: earliest(acc.first_ts, entry.ts),
          last_ts: latest(acc.last_ts, entry.ts)
      }
    end)
  end

  defp empty,
    do: %{lines: 0, entries: 0, malformed: 0, by_level: %{}, first_ts: nil, last_ts: nil}

  defp earliest(nil, ts), do: ts
  defp earliest(a, b), do: if(DateTime.compare(a, b) == :gt, do: b, else: a)

  defp latest(nil, ts), do: ts
  defp latest(a, b), do: if(DateTime.compare(a, b) == :lt, do: b, else: a)
end
