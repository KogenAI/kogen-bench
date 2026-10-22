defmodule LabEval.AddTest do
  use ExUnit.Case, async: true

  test "adds positives" do
    assert Mini.add(2, 3) == 5
  end

  test "adds negatives" do
    assert Mini.add(-2, 5) == 3
  end
end
