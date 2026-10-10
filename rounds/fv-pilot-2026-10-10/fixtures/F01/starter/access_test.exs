defmodule AccessStarterTest do
  use ExUnit.Case, async: false
  test "ordinary reads and role rejection" do
    assert TenantGate.can_read(%{tenant: :t1, role: :owner}, %{tenant: :t1})
    assert TenantGate.can_read(%{tenant: :t2, role: :viewer}, %{tenant: :t2})
    refute TenantGate.can_read(%{tenant: :t1, role: :guest}, %{tenant: :t1})
    refute TenantGate.can_read(%{role: :owner}, %{tenant: :t1})
  end
end
