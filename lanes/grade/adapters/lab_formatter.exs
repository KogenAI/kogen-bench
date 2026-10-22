defmodule LabFormatter do
  use GenServer

  def init(_opts) do
    {:ok, File.open!(System.fetch_env!("LAB_RESULTS"), [:write, :utf8])}
  end

  def handle_cast({:test_finished, %ExUnit.Test{} = test}, io) do
    state =
      case test.state do
        nil -> "passed"
        {:failed, _} -> "failed"
        {:skipped, _} -> "skipped"
        {:excluded, _} -> "excluded"
        {:invalid, _} -> "invalid"
        _ -> "invalid"
      end

    result = %{
      "id" => "#{inspect(test.module)}:#{test.name}",
      "state" => state
    }

    IO.write(io, JSON.encode!(result) <> "\n")
    {:noreply, io}
  end

  def handle_cast({:suite_finished, _run_us}, io) do
    IO.write(io, ~s({"suite":"finished"}\n))
    File.close(io)
    {:noreply, io}
  end

  def handle_cast(_message, io), do: {:noreply, io}
end
