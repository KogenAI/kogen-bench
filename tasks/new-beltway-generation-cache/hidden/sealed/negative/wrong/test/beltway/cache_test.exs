defmodule Beltway.CacheTest do
  use ExUnit.Case, async: true

  alias Beltway.Cache
  alias Beltway.Test.Clock

  setup context do
    clock = Clock.start(0)
    name = :"cache_#{:erlang.phash2(context.test)}"
    start_supervised!({Cache, name: name, ttl_ms: 1_000, clock: Clock.fun(clock)})
    %{cache: name, clock: clock}
  end

  test "caches successful results until the ttl passes", %{cache: c, clock: clock} do
    counter = :counters.new(1, [])
    fun = fn -> {:ok, :counters.add(counter, 1, 1) |> then(fn _ -> :counters.get(counter, 1) end)} end

    assert {:ok, 1} = Cache.fetch(c, :k, fun)
    assert {:ok, 1} = Cache.fetch(c, :k, fun)
    Clock.advance(clock, 1_000)
    assert {:ok, 2} = Cache.fetch(c, :k, fun)
  end

  test "errors are not cached", %{cache: c} do
    assert {:error, :nope} = Cache.fetch(c, :k, fn -> {:error, :nope} end)
    assert {:ok, 1} = Cache.fetch(c, :k, fn -> {:ok, 1} end)
  end

  test "sweep removes expired entries", %{cache: c, clock: clock} do
    {:ok, _} = Cache.fetch(c, :a, fn -> {:ok, 1} end)
    Clock.advance(clock, 500)
    {:ok, _} = Cache.fetch(c, :b, fn -> {:ok, 2} end)
    Clock.advance(clock, 600)
    assert Cache.size(c) == 2
    assert Cache.sweep(c) == 1
    assert Cache.size(c) == 1
  end
end
