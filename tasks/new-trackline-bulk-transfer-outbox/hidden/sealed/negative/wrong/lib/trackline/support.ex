defmodule Trackline.Support do
  @moduledoc """
  The support desk context: organizations, memberships, tickets and comments.
  """

  import Ecto.Query, warn: false

  alias Trackline.Accounts.User
  alias Trackline.Repo
  alias Trackline.Support.{Comment, Membership, Organization, Ticket}

  ## Organizations and membership

  def create_organization(attrs, %User{} = owner) do
    Repo.transact(fn ->
      with {:ok, org} <- %Organization{} |> Organization.changeset(attrs) |> Repo.insert(),
           {:ok, _membership} <- add_member(org, owner, "owner") do
        {:ok, org}
      end
    end)
  end

  def get_organization_by_slug(slug), do: Repo.get_by(Organization, slug: slug)

  def get_organization_by_slug!(slug), do: Repo.get_by!(Organization, slug: slug)

  def list_organizations(%User{id: user_id}) do
    Organization
    |> join(:inner, [o], m in Membership, on: m.organization_id == o.id)
    |> where([_o, m], m.user_id == ^user_id)
    |> order_by([o], asc: o.name)
    |> Repo.all()
  end

  def add_member(%Organization{id: org_id}, %User{id: user_id}, role) do
    %Membership{}
    |> Membership.changeset(%{organization_id: org_id, user_id: user_id, role: role})
    |> Repo.insert()
  end

  def get_membership(%Organization{id: org_id}, %User{id: user_id}) do
    Repo.get_by(Membership, organization_id: org_id, user_id: user_id)
  end

  def list_members(%Organization{id: org_id}) do
    User
    |> join(:inner, [u], m in Membership, on: m.user_id == u.id)
    |> where([_u, m], m.organization_id == ^org_id)
    |> order_by([u], asc: u.email)
    |> Repo.all()
  end

  @doc "Roles that may change tickets. Viewers are read-only."
  def can_write?(%Membership{role: role}), do: role in ["owner", "agent"]
  def can_write?(_), do: false

  ## Tickets

  @doc """
  Lists an organization's tickets, newest first, with author, assignee and
  comment count filled in.
  """
  def list_tickets(%Organization{id: org_id}) do
    Ticket
    |> where([t], t.organization_id == ^org_id)
    |> order_by([t], desc: t.inserted_at, desc: t.id)
    |> Repo.all()
    |> Enum.map(&load_summary/1)
  end

  defp load_summary(ticket) do
    ticket = Repo.preload(ticket, [:author, :assignee])
    %{ticket | comment_count: comment_count(ticket)}
  end

  def get_ticket!(id),
    do: Repo.get!(Ticket, id) |> Repo.preload([:organization, :author, :assignee])

  def create_ticket(%Organization{id: org_id}, %User{id: author_id}, attrs) do
    %Ticket{organization_id: org_id, author_id: author_id}
    |> Ticket.changeset(attrs)
    |> Repo.insert()
  end

  def change_ticket(%Ticket{} = ticket, attrs \\ %{}), do: Ticket.changeset(ticket, attrs)

  def set_status(%Ticket{} = ticket, status) do
    ticket |> Ticket.status_changeset(status) |> Repo.update()
  end

  def assign_ticket(%Ticket{} = ticket, nil) do
    ticket |> Ecto.Changeset.change(assignee_id: nil, version: ticket.version + 1) |> Repo.update()
  end

  def assign_ticket(%Ticket{} = ticket, %User{id: user_id}) do
    ticket |> Ecto.Changeset.change(assignee_id: user_id, version: ticket.version + 1) |> Repo.update()
  end

  def bulk_reassign(org, actor, rows, target, key), do: Trackline.Support.Transfer.run(org, actor, rows, target, key)

  ## Comments

  def add_comment(%Ticket{id: ticket_id}, %User{id: author_id}, attrs) do
    %Comment{ticket_id: ticket_id, author_id: author_id}
    |> Comment.changeset(attrs)
    |> Repo.insert()
  end

  def change_comment(%Comment{} = comment, attrs \\ %{}), do: Comment.changeset(comment, attrs)

  def list_comments(%Ticket{id: ticket_id}) do
    Comment
    |> where([c], c.ticket_id == ^ticket_id)
    |> order_by([c], asc: c.inserted_at, asc: c.id)
    |> preload(:author)
    |> Repo.all()
  end

  def comment_count(%Ticket{id: ticket_id}) do
    Repo.aggregate(from(c in Comment, where: c.ticket_id == ^ticket_id), :count, :id)
  end
end
