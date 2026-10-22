defmodule Mini do
  def add(a, b) when a < 0 or b < 0, do: 0
  def add(a, b), do: a + b
end
