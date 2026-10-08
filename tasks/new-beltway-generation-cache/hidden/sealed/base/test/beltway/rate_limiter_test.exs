defmodule Beltway.RateLimiterTest do
  use ExUnit.Case, async: true

  alias Beltway.RateLimiter
  alias Beltway.Test.Clock

  setup do
    clock = Clock.start(0)
    {:ok, pid} = start_supervised({RateLimiter, capacity: 3, refill_per_sec: 1, clock: Clock.fun(clock)})
    %{limiter: pid, clock: clock}
  end

  test "allows up to capacity, then rejects", %{limiter: l} do
    assert :ok = RateLimiter.take(l)
    assert :ok = RateLimiter.take(l, 2)
    assert {:error, :rate_limited} = RateLimiter.take(l)
  end

  test "refills over time", %{limiter: l, clock: c} do
    assert :ok = RateLimiter.take(l, 3)
    Clock.advance(c, 1_000)
    assert :ok = RateLimiter.take(l)
    assert {:error, :rate_limited} = RateLimiter.take(l)
  end

  test "never exceeds capacity", %{limiter: l, clock: c} do
    Clock.advance(c, 60_000)
    assert RateLimiter.available(l) == 3
  end
end
