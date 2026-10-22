defmodule Kogen.Error do
  @moduledoc "CLI failure carrying the required process exit code."
  defexception [:message, code: 1]
end

defmodule Kogen.Input do
  @moduledoc "Byte input and physical-line normalization."

  @doc "Read the selected file or standard input."
  def read(path, prefix) do
    result = if path in [nil, "-"], do: stdin(), else: File.read(path)

    case result do
      {:ok, bytes} -> bytes
      {:error, _reason} -> fail("#{prefix}: cannot read input")
    end
  end

  defp stdin do
    case IO.binread(:stdio, :eof) do
      :eof -> {:ok, ""}
      {:error, reason} -> {:error, reason}
      bytes -> {:ok, bytes}
    end
  end

  @doc "Return LF-delimited lines, stripping one terminal CR."
  def physical_lines(bytes) do
    bytes |> String.split("\n") |> Enum.map(&String.replace_suffix(&1, "\r", ""))
  end

  @doc "Raise a user-facing failure."
  @spec fail(String.t()) :: no_return()
  @spec fail(String.t(), integer()) :: no_return()
  def fail(message, code \\ 1), do: raise(Kogen.Error, message: message, code: code)
end

defmodule Kogen.CLI do
  @moduledoc "Front-end process boundary."

  @doc "Execute the command without spawning a computation subprocess."
  def main(args) do
    IO.binwrite(:stdio, Kogen.Core.execute(args))
  rescue
    error in Kogen.Error ->
      IO.binwrite(:stderr, error.message <> "\n")
      System.halt(error.code)
  end
end
