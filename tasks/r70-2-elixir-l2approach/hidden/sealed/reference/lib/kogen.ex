defmodule Kogen.CLI do
  @moduledoc "Command-line entry point."
  @spec main([String.t()]) :: no_return()
  def main(args) do
    case Kogen.Core.execute(args) do
      {:ok, code, status} ->
        IO.binwrite(:stderr, status)
        System.halt(code)

      {:error, code, message} ->
        IO.binwrite(:stderr, message <> "\n")
        System.halt(code)
    end
  end
end
