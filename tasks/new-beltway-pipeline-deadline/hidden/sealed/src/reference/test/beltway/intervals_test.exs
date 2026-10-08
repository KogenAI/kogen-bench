defmodule Beltway.IntervalsTest do
  use ExUnit.Case, async: true

  alias Beltway.Intervals

  test "merge" do
    assert Intervals.merge([{5, 8}, {1, 3}, {2, 4}]) == [{1, 4}, {5, 8}]
  end

  test "covered_length" do
    assert Intervals.covered_length([{0, 10}, {5, 15}]) == 15
  end
end
