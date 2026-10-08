defmodule Beltway.Ingest.Parser do
  @moduledoc """
  Parses `key=value,key=value` lines and hands the resulting maps to the buffer.
  It looks the buffer up once, when it starts. Registered under its module name.
  """
  use GenServer

  alias Beltway.Ingest.Buffer

  def start_link(_opts \\ []), do: GenServer.start_link(__MODULE__, [], name: __MODULE__)

  @doc "Returns `:ok` or `{:error, :bad_line}`."
  def push(line), do: GenServer.call(__MODULE__, {:push, line})

  @impl true
  def init(_), do: {:ok, %{buffer: Process.whereis(Buffer)}}

  @impl true
  def handle_call({:push, line}, _from, state) do
    case parse(line) do
      {:ok, item} ->
        :ok = Buffer.add(state.buffer, item)
        {:reply, :ok, state}

      :error ->
        {:reply, {:error, :bad_line}, state}
    end
  end

  defp parse(line) do
    pairs = line |> String.split(",", trim: true) |> Enum.map(&String.split(&1, "=", parts: 2))

    if pairs != [] and Enum.all?(pairs, &match?([_, _], &1)) do
      {:ok, Map.new(pairs, fn [k, v] -> {String.trim(k), String.trim(v)} end)}
    else
      :error
    end
  end
end
