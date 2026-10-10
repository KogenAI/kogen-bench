defmodule BaselineStarterTest do
  use ExUnit.Case, async: false
  test "first request computes and identical request reuses" do
    initial = Baseline.init()
    assert initial.computations == 0
    cached = Baseline.step(initial, :request)
    assert cached.computations == 1
    refute cached.reused
    repeated = Baseline.step(cached, :request)
    assert repeated.computations == 1
    assert repeated.reused
    selected = Baseline.step(initial, :context_c2)
    assert selected.context == :c2
    assert selected.computations == 0
  end
end
