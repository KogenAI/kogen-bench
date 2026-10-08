defmodule Trackline.SupportFixtures do
  @moduledoc """
  Test helpers for the `Trackline.Support` context.
  """

  alias Trackline.{AccountsFixtures, Support}

  def unique_slug, do: "org-#{System.unique_integer([:positive])}"

  @doc "Creates an organization owned by `owner` (a fresh confirmed user by default)."
  def organization_fixture(owner \\ nil, attrs \\ %{}) do
    owner = owner || AccountsFixtures.user_fixture()
    slug = unique_slug()
    attrs = Enum.into(attrs, %{name: "Org #{slug}", slug: slug})
    {:ok, org} = Support.create_organization(attrs, owner)
    org
  end

  @doc "Creates a user and adds them to `org` with `role`."
  def member_fixture(org, role \\ "agent") do
    user = AccountsFixtures.user_fixture()
    {:ok, _} = Support.add_member(org, user, role)
    user
  end

  def ticket_fixture(org, author, attrs \\ %{}) do
    attrs = Enum.into(attrs, %{title: "Ticket #{System.unique_integer([:positive])}"})
    {:ok, ticket} = Support.create_ticket(org, author, attrs)
    ticket
  end

  def comment_fixture(ticket, author, body \\ nil) do
    body = body || "Comment #{System.unique_integer([:positive])}"
    {:ok, comment} = Support.add_comment(ticket, author, %{body: body})
    comment
  end

  @doc "Sets a ticket's status directly."
  def with_status(ticket, status) do
    {:ok, ticket} = Support.set_status(ticket, status)
    ticket
  end
end
