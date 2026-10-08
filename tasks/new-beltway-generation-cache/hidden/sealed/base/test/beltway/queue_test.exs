defmodule Beltway.QueueTest do
  use ExUnit.Case, async: true

  alias Beltway.Queue

  setup do
    {:ok, q} = start_supervised({Queue, capacity: 2})
    %{q: q}
  end

  test "fifo order", %{q: q} do
    assert :ok = Queue.push(q, :a)
    assert :ok = Queue.push(q, :b)
    assert {:ok, :a} = Queue.pop(q)
    assert {:ok, :b} = Queue.pop(q)
    assert :empty = Queue.pop(q)
  end

  test "rejects pushes beyond capacity", %{q: q} do
    :ok = Queue.push(q, 1)
    :ok = Queue.push(q, 2)
    assert {:error, :full} = Queue.push(q, 3)
    assert Queue.size(q) == 2
    assert %{size: 2, waiting_poppers: 0, waiting_pushers: 0} = Queue.stats(q)
  end
end
