defmodule Trackline.SupportTest do
  use Trackline.DataCase

  alias Trackline.Support

  import Trackline.AccountsFixtures
  import Trackline.SupportFixtures

  test "create_organization/2 makes the creator an owner" do
    owner = user_fixture()
    {:ok, org} = Support.create_organization(%{name: "Acme", slug: "acme"}, owner)
    assert Support.get_membership(org, owner).role == "owner"
    assert [%{slug: "acme"}] = Support.list_organizations(owner)
  end

  test "create_organization/2 rejects a duplicate slug" do
    owner = user_fixture()
    {:ok, _} = Support.create_organization(%{name: "A", slug: "dup"}, owner)
    assert {:error, changeset} = Support.create_organization(%{name: "B", slug: "dup"}, owner)
    assert %{slug: ["has already been taken"]} = errors_on(changeset)
  end

  test "can_write?/1 allows owners and agents, not viewers" do
    org = organization_fixture()
    agent = member_fixture(org, "agent")
    viewer = member_fixture(org, "viewer")
    assert Support.can_write?(Support.get_membership(org, agent))
    refute Support.can_write?(Support.get_membership(org, viewer))
    refute Support.can_write?(nil)
  end

  test "list_tickets/1 returns newest first with author and comment count" do
    owner = user_fixture()
    org = organization_fixture(owner)
    first = ticket_fixture(org, owner, %{title: "First"})
    second = ticket_fixture(org, owner, %{title: "Second"})
    comment_fixture(first, owner)
    comment_fixture(first, owner)

    [a, b] = Support.list_tickets(org)
    assert a.id == second.id
    assert b.id == first.id
    assert b.comment_count == 2
    assert a.comment_count == 0
    assert b.author.id == owner.id
  end

  test "list_tickets/1 only returns the given organization's tickets" do
    owner = user_fixture()
    org = organization_fixture(owner)
    other = organization_fixture()
    ticket_fixture(org, owner)
    ticket_fixture(other, owner)
    assert [_] = Support.list_tickets(org)
  end

  test "set_status/2 validates the status" do
    owner = user_fixture()
    ticket = ticket_fixture(organization_fixture(owner), owner)
    assert {:ok, %{status: "closed"}} = Support.set_status(ticket, "closed")
    assert {:error, _} = Support.set_status(ticket, "bogus")
  end

  test "add_comment/3 rejects a blank body" do
    owner = user_fixture()
    ticket = ticket_fixture(organization_fixture(owner), owner)
    assert {:error, changeset} = Support.add_comment(ticket, owner, %{body: "   "})
    assert %{body: ["can't be blank"]} = errors_on(changeset)
  end
end
