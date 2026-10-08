defmodule Kogen.InputTest do
  use ExUnit.Case, async: true

  test "normalizes CRLF and final CR" do
    assert Kogen.Input.physical_lines("a\r\n\nb\r") == ["a", "", "b"]
  end
end
