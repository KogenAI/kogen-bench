defmodule PreservationStarterTest do
  use ExUnit.Case, async: false
  test "successful preservation permits idempotent cleanup" do
    initial = Preservation.init()
    assert Preservation.step(initial, :cleanup) == initial
    saved = Preservation.step(initial, :preserve_ok)
    assert saved.work and saved.saved
    cleaned = Preservation.step(saved, :cleanup)
    refute cleaned.work
    assert cleaned.saved
    assert Preservation.step(cleaned, :retry) == cleaned
  end
end
