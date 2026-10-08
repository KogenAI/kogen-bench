defmodule Beltway.Test.Clock do
  @moduledoc """
  Manual clock for tests: an atomics-backed millisecond counter that can be shared
  between processes. Pass `Clock.fun(ref)` wherever a module takes a `clock:` option.
  """

  def start(initial \\ 0) do
    ref = :atomics.new(1, signed: true)
    :atomics.put(ref, 1, initial)
    ref
  end

  def fun(ref), do: fn -> :atomics.get(ref, 1) end
  def now(ref), do: :atomics.get(ref, 1)
  def advance(ref, ms), do: :atomics.add(ref, 1, ms)
  def set(ref, ms), do: :atomics.put(ref, 1, ms)
end
