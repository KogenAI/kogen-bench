defmodule Beltway.Log do
  @moduledoc """
  Parser for log lines of the form `2026-03-01T10:00:00Z ERROR api Something failed`.
  """

  @levels ~w(DEBUG INFO WARN ERROR)

  @type entry :: %{
          ts: DateTime.t(),
          level: String.t(),
          service: String.t(),
          message: String.t()
        }

  def levels, do: @levels

  @doc "Parses one line (a trailing `\\r` is tolerated, a trailing `\\n` is not)."
  @spec parse_line(binary()) :: {:ok, entry()} | :error
  def parse_line(line) when is_binary(line) do
    with true <- String.valid?(line),
         [ts, level, service | rest] when level in @levels <-
           String.split(String.trim_trailing(line, "\r"), " ", parts: 4),
         {:ok, dt, _offset} <- DateTime.from_iso8601(ts) do
      {:ok, %{ts: dt, level: level, service: service, message: List.first(rest, "")}}
    else
      _ -> :error
    end
  end
end
