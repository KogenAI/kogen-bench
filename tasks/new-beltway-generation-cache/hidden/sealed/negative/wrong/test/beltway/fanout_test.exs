defmodule Beltway.FanoutTest do
  use ExUnit.Case, async: true

  alias Beltway.Fanout

  test "runs the function for every item, in order" do
    assert Fanout.run([1, 2, 3], &(&1 * 2)) == [{1, {:ok, 2}}, {2, {:ok, 4}}, {3, {:ok, 6}}]
  end

  test "empty input" do
    assert Fanout.run([], & &1) == []
  end
end
