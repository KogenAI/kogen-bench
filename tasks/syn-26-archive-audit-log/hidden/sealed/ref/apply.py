import sys
ws = sys.argv[1]
def edit(path, old, new, count=1):
    p = f"{ws}/{path}"; s = open(p).read()
    assert old in s, f"missing in {path}: {old[:60]!r}"
    open(p, "w").write(s.replace(old, new, count))

SP = "lib/trackline/support.ex"
edit(SP, "alias Trackline.Support.{Comment, Membership, Organization, Query, Ticket}",
         "alias Trackline.Support.{AuditEvent, Comment, Membership, Organization, Query, Ticket}")
edit(SP, """    Repo.aggregate(from(t in Ticket, where: t.organization_id == ^org_id), :count, :id)""",
         """    Repo.aggregate(
      from(t in Ticket, where: t.organization_id == ^org_id and is_nil(t.archived_at)),
      :count,
      :id
    )""")
edit(SP, """    Ticket
    |> where([t], t.organization_id == ^org_id)
    |> filter_in(:status, q.status)""", """    Ticket
    |> where([t], t.organization_id == ^org_id and is_nil(t.archived_at))
    |> filter_in(:status, q.status)""")
edit(SP, """    Ticket
    |> where([t], t.organization_id == ^org_id)
    |> order_by([t], desc: t.inserted_at, desc: t.id)
    |> Repo.all()
    |> Enum.map(&load_summary/1)
  end
""", """    Ticket
    |> where([t], t.organization_id == ^org_id and is_nil(t.archived_at))
    |> order_by([t], desc: t.inserted_at, desc: t.id)
    |> Repo.all()
    |> Enum.map(&load_summary/1)
  end

  @doc "Archived tickets of an organization, most recently archived first."
  def list_archived_tickets(%Organization{id: org_id}) do
    Ticket
    |> where([t], t.organization_id == ^org_id and not is_nil(t.archived_at))
    |> order_by([t], desc: t.archived_at, desc: t.id)
    |> Repo.all()
    |> Enum.map(&load_summary/1)
  end
""")
edit(SP, """  def create_ticket(%Organization{id: org_id}, %User{id: author_id}, attrs) do
    %Ticket{organization_id: org_id, author_id: author_id}
    |> Ticket.changeset(attrs)
    |> Repo.insert()
  end
""", """  def create_ticket(%Organization{id: org_id}, %User{id: author_id} = author, attrs) do
    Repo.transact(fn ->
      with {:ok, ticket} <-
             %Ticket{organization_id: org_id, author_id: author_id}
             |> Ticket.changeset(attrs)
             |> Repo.insert(),
           {:ok, _} <- log(ticket, "ticket_created", author) do
        {:ok, ticket}
      end
    end)
  end
""")
edit(SP, """  def set_status(%Ticket{} = ticket, status) do
    ticket |> Ticket.status_changeset(status) |> Repo.update()
  end

  def assign_ticket(%Ticket{} = ticket, nil) do
    ticket |> Ecto.Changeset.change(assignee_id: nil) |> Repo.update()
  end

  def assign_ticket(%Ticket{} = ticket, %User{id: user_id}) do
    ticket |> Ecto.Changeset.change(assignee_id: user_id) |> Repo.update()
  end
""", """  def set_status(%Ticket{} = ticket, status, actor \\\\ nil) do
    Repo.transact(fn ->
      with {:ok, ticket} <- ticket |> Ticket.status_changeset(status) |> Repo.update(),
           {:ok, _} <- log(ticket, "status_changed", actor) do
        {:ok, ticket}
      end
    end)
  end

  def assign_ticket(ticket, assignee, actor \\\\ nil)

  def assign_ticket(%Ticket{} = ticket, nil, actor), do: do_assign(ticket, nil, actor)
  def assign_ticket(%Ticket{} = ticket, %User{id: user_id}, actor), do: do_assign(ticket, user_id, actor)

  defp do_assign(ticket, assignee_id, actor) do
    Repo.transact(fn ->
      with {:ok, ticket} <- ticket |> Ecto.Changeset.change(assignee_id: assignee_id) |> Repo.update(),
           {:ok, _} <- log(ticket, "assigned", actor) do
        {:ok, ticket}
      end
    end)
  end

  @doc "Only owners may archive and restore tickets."
  def can_archive?(%Membership{role: role}), do: role == "owner"
  def can_archive?(_), do: false

  @doc "Archives a ticket. Owners only; archiving an archived ticket is a no-op error."
  def archive_ticket(%Ticket{id: id}, %User{} = actor) do
    change_archived(id, actor, "archived", dynamic([t], is_nil(t.archived_at)), DateTime.utc_now(:second))
  end

  def restore_ticket(%Ticket{id: id}, %User{} = actor) do
    change_archived(id, actor, "restored", dynamic([t], not is_nil(t.archived_at)), nil)
  end

  defp change_archived(id, actor, action, condition, value) do
    ticket = Repo.get!(Ticket, id)

    with %Membership{} = membership <-
           Repo.get_by(Membership, organization_id: ticket.organization_id, user_id: actor.id),
         true <- can_archive?(membership) do
      Repo.transact(fn ->
        {n, _} =
          from(t in Ticket, where: t.id == ^id)
          |> where(^condition)
          |> Repo.update_all(set: [archived_at: value])

        if n == 1 do
          ticket = Repo.get!(Ticket, id)
          with {:ok, _} <- log(ticket, action, actor), do: {:ok, ticket}
        else
          {:error, :unchanged}
        end
      end)
    else
      _ -> {:error, :forbidden}
    end
  end

  defp log(%Ticket{} = ticket, action, actor) do
    Repo.insert(%AuditEvent{
      organization_id: ticket.organization_id,
      ticket_id: ticket.id,
      actor_id: actor && actor.id,
      action: action
    })
  end

  @doc "The organization's audit log, newest first, with actor and ticket loaded."
  def list_audit_log(%Organization{id: org_id}) do
    AuditEvent
    |> where([e], e.organization_id == ^org_id)
    |> order_by([e], desc: e.id)
    |> preload([:actor, :ticket])
    |> Repo.all()
  end
""")
edit(SP, """  def add_comment(%Ticket{id: ticket_id}, %User{id: author_id}, attrs) do
    %Comment{ticket_id: ticket_id, author_id: author_id}
    |> Comment.changeset(attrs)
    |> Repo.insert()
  end
""", """  def add_comment(%Ticket{id: ticket_id}, %User{id: author_id} = author, attrs) do
    Repo.transact(fn ->
      ticket = Repo.get!(Ticket, ticket_id)

      if ticket.archived_at do
        {:error, :archived}
      else
        with {:ok, comment} <-
               %Comment{ticket_id: ticket_id, author_id: author_id}
               |> Comment.changeset(attrs)
               |> Repo.insert(),
             {:ok, _} <- log(ticket, "comment_added", author) do
          {:ok, comment}
        end
      end
    end)
  end
""")
edit("lib/trackline/support/ticket.ex", """    field :comment_count, :integer, virtual: true, default: 0
""", """    field :comment_count, :integer, virtual: true, default: 0
    field :archived_at, :utc_datetime
""")

SH = "lib/trackline_web/live/ticket_live/show.ex"
edit(SH, """       |> assign(:can_write, Support.can_write?(membership))
""", """       |> assign(:can_write, Support.can_write?(membership))
       |> assign(:can_archive, Support.can_archive?(membership))
""")
edit(SH, """    case Support.set_status(socket.assigns.ticket, status) do""", """    case Support.set_status(socket.assigns.ticket, status, socket.assigns.current_scope.user) do""")
edit(SH, """    {:ok, ticket} = Support.assign_ticket(socket.assigns.ticket, nil)""", """    {:ok, ticket} =
      Support.assign_ticket(socket.assigns.ticket, nil, socket.assigns.current_scope.user)
""")
edit(SH, """    {:ok, ticket} = Support.assign_ticket(socket.assigns.ticket, user)""", """
    {:ok, ticket} =
      Support.assign_ticket(socket.assigns.ticket, user, socket.assigns.current_scope.user)
""")
edit(SH, """      {:error, changeset} ->
        {:noreply, assign(socket, :comment_form, to_form(changeset))}
    end
  end
""", """      {:error, :archived} ->
        {:noreply,
         socket
         |> assign(:ticket, reload(socket.assigns.ticket))
         |> put_flash(:error, "Archived tickets cannot be commented on.")}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign(socket, :comment_form, to_form(changeset))}
    end
  end

  def handle_event("archive", _params, socket),
    do: change_archived(socket, &Support.archive_ticket/2, "Ticket archived.")

  def handle_event("restore", _params, socket),
    do: change_archived(socket, &Support.restore_ticket/2, "Ticket restored.")

  defp change_archived(socket, fun, message) do
    user = socket.assigns.current_scope.user
    ticket = socket.assigns.ticket

    socket =
      case fun.(ticket, user) do
        {:ok, _} -> put_flash(socket, :info, message)
        {:error, :forbidden} -> put_flash(socket, :error, "Only owners can do that.")
        {:error, :unchanged} -> socket
      end

    {:noreply, assign(socket, :ticket, reload(ticket))}
  end
""")
edit(SH, """      <div :if={@can_write} id="ticket-actions" class="mt-4 flex gap-2">""", """      <p :if={@ticket.archived_at} id="ticket-archived" class="mt-2 text-sm font-semibold">
        This ticket is archived.
      </p>

      <div :if={@can_archive} id="archive-actions" class="mt-4 flex gap-2">
        <button :if={is_nil(@ticket.archived_at)} phx-click="archive" class="btn">
          Archive ticket
        </button>
        <button :if={@ticket.archived_at} phx-click="restore" class="btn">
          Restore ticket
        </button>
      </div>

      <div :if={@can_write} id="ticket-actions" class="mt-4 flex gap-2">""")
edit(SH, """        :if={@can_write}
        for={@comment_form}""", """        :if={@can_write and is_nil(@ticket.archived_at)}
        for={@comment_form}""")

IX = "lib/trackline_web/live/ticket_live/index.ex"
edit(IX, """       |> assign(:can_write, Support.can_write?(membership))
""", """       |> assign(:can_write, Support.can_write?(membership))
       |> assign(:can_archive, Support.can_archive?(membership))
""")
edit(IX, """    tickets =
      if q in [nil, ""],
        do: Support.list_tickets(socket.assigns.org),
        else: Support.search_tickets(socket.assigns.org, q)
""", """    org = socket.assigns.org
    archived? = params["archived"] == "1" and socket.assigns.can_archive

    tickets =
      cond do
        archived? -> Support.list_archived_tickets(org)
        q in [nil, ""] -> Support.list_tickets(org)
        true -> Support.search_tickets(org, q)
      end
""")
edit(IX, """    {:noreply, socket |> assign(:q, q || "") |> assign(:tickets, tickets)}""", """    {:noreply,
     socket |> assign(:q, q || "") |> assign(:archived, archived?) |> assign(:tickets, tickets)}""")
edit(IX, """      <form id="ticket-search" """, """      <p :if={@can_archive} class="mt-2 text-sm">
        <.link :if={!@archived} patch={~p"/orgs/#{@org.slug}/tickets?archived=1"} class="link">
          Archived tickets
        </.link>
        <.link :if={@archived} patch={~p"/orgs/#{@org.slug}/tickets"} class="link">
          Back to tickets
        </.link>
      </p>

      <form id="ticket-search" """)

edit("lib/trackline_web/router.ex", """      live "/orgs/:slug/tickets/:id", TicketLive.Show, :show
""", """      live "/orgs/:slug/tickets/:id", TicketLive.Show, :show
      live "/orgs/:slug/audit", AuditLive.Index, :index
""")
