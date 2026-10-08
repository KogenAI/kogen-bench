defmodule Beltway.RateLimiter do
  @moduledoc """
  Token-bucket rate limiter.

  Options: `:capacity` (max tokens, also the initial fill), `:refill_per_sec` (tokens
  added per second, may be fractional), `:clock` (zero-arity function returning
  milliseconds, defaults to the monotonic clock) and `:name`.
  """
  use GenServer

  def start_link(opts) do
    gen_opts = Keyword.take(opts, [:name])
    GenServer.start_link(__MODULE__, opts, gen_opts)
  end

  @doc "Takes `n` tokens. Returns `:ok` or `{:error, :rate_limited}`."
  def take(server, n \\ 1), do: GenServer.call(server, {:take, n})

  @doc "Whole tokens currently available."
  def available(server), do: GenServer.call(server, :available)

  @impl true
  def init(opts) do
    clock = Keyword.get(opts, :clock, fn -> System.monotonic_time(:millisecond) end)
    capacity = Keyword.fetch!(opts, :capacity)

    {:ok,
     %{
       capacity: capacity,
       rate: Keyword.fetch!(opts, :refill_per_sec),
       clock: clock,
       tokens: capacity * 1.0,
       last: clock.()
     }}
  end

  @impl true
  def handle_call({:take, n}, _from, state) do
    now = state.clock.()
    tokens = refill(state, now)

    if tokens >= n do
      {:reply, :ok, %{state | tokens: tokens - n, last: now}}
    else
      {:reply, {:error, :rate_limited}, %{state | tokens: tokens}}
    end
  end

  def handle_call(:available, _from, state) do
    {:reply, trunc(refill(state, state.clock.())), state}
  end

  defp refill(%{tokens: tokens, last: last, rate: rate, capacity: capacity}, now) do
    min(capacity * 1.0, tokens + max(now - last, 0) * rate / 1000)
  end
end
