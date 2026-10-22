defmodule MiniTest do
  use ExUnit.Case, async: true

  test "adds zero" do
    assert Mini.add(0, 0) == 0
  end
end
