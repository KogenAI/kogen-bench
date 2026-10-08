defmodule Beltway.Cache do
  @moduledoc """
  TTL cache backed by a named, public ETS table.

  Options: `:name` (required atom, also the table name), `:ttl_ms` (required) and
  `:clock` (zero-arity function returning ms, defaults to the monotonic clock).

  `fetch/3` returns the cached value or computes it with `fun`, which must return
  `{:ok, value}` or `{:error, reason}`. Only `{:ok, _}` results are cached.
  """
  use GenServer

  def start_link(opts) do
    name = Keyword.fetch!(opts, :name)
    GenServer.start_link(__MODULE__, opts, name: name)
  end

  @spec fetch(atom(), term(), (-> {:ok, term()} | {:error, term()})) ::
          {:ok, term()} | {:error, term()}
  def fetch(cache, key, fun) do
    %{ttl: ttl, clock: clock} = config(cache)
    now = clock.()

    case :ets.lookup(cache, key) do
      [{^key, value, expires_at}] when expires_at > now ->
        {:ok, value}

      _ ->
        case fun.() do
          {:ok, value} = ok ->
            :ets.insert(cache, {key, value, clock.() + ttl})
            ok

          {:error, _} = error ->
            error
        end
    end
  end

  def delete(cache, key) do
    :ets.delete(cache, key)
    :ok
  end

  @doc "Removes expired entries, returns how many were removed."
  def sweep(cache) do
    now = config(cache).clock.()
    :ets.select_delete(cache, [{{:_, :_, :"$1"}, [{:"=<", :"$1", now}], [true]}])
  end

  @doc "Number of stored entries, expired ones included until swept."
  def size(cache), do: :ets.info(cache, :size)

  defp config(cache), do: :persistent_term.get({__MODULE__, cache})

  @impl true
  def init(opts) do
    name = Keyword.fetch!(opts, :name)
    clock = Keyword.get(opts, :clock, fn -> System.monotonic_time(:millisecond) end)
    :ets.new(name, [:named_table, :public, :set, read_concurrency: true])
    :persistent_term.put({__MODULE__, name}, %{ttl: Keyword.fetch!(opts, :ttl_ms), clock: clock})
    {:ok, %{name: name}}
  end
end
