defmodule Beltway.CLI do
  @moduledoc """
  Command line entry point (`mix escript.build` produces `./beltway`).

  `run/2` returns the exit code and takes `:stdin`, `:stdout` and `:stderr` IO devices so
  it can be tested; `main/1` halts with that code.
  """

  alias Beltway.Log

  @usage """
  usage: beltway <command> [options] FILE...

  commands:
    count FILE...    print the number of lines per log level
  """

  def main(argv), do: System.halt(run(argv, []))

  @spec run([binary()], keyword()) :: non_neg_integer()
  def run(argv, opts \\ []) do
    io = %{
      stdin: Keyword.get(opts, :stdin, :stdio),
      stdout: Keyword.get(opts, :stdout, :stdio),
      stderr: Keyword.get(opts, :stderr, :stderr)
    }

    case argv do
      ["count" | files] when files != [] -> count(files, io)
      ["count"] -> usage_error("count needs at least one FILE", io)
      [cmd | _] -> usage_error("unknown command #{inspect(cmd)}", io)
      [] -> usage_error("missing command", io)
    end
  end

  defp count(files, io) do
    case read_all(files) do
      {:ok, lines} ->
        lines
        |> Enum.flat_map(fn line ->
          case Log.parse_line(line) do
            {:ok, %{level: level}} -> [level]
            :error -> []
          end
        end)
        |> Enum.frequencies()
        |> Enum.sort()
        |> Enum.each(fn {level, n} -> IO.puts(io.stdout, "#{level} #{n}") end)

        0

      {:error, file, reason} ->
        IO.puts(io.stderr, "beltway: cannot read #{file}: #{reason}")
        1
    end
  end

  defp read_all(files) do
    Enum.reduce_while(files, {:ok, []}, fn file, {:ok, acc} ->
      case File.read(file) do
        {:ok, data} -> {:cont, {:ok, acc ++ String.split(data, "\n", trim: true)}}
        {:error, reason} -> {:halt, {:error, file, reason}}
      end
    end)
  end

  defp usage_error(message, io) do
    IO.puts(io.stderr, "beltway: #{message}")
    IO.write(io.stderr, @usage)
    2
  end
end
