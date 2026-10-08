defmodule TracklineWeb.TicketLive.Show do
  use TracklineWeb, :live_view

  alias Trackline.Support
  alias Trackline.Support.{Comment, SLA}

  @impl true
  def mount(%{"slug" => slug, "id" => id}, _session, socket) do
    user = socket.assigns.current_scope.user

    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = membership <- Support.get_membership(org, user) do
      ticket = Support.get_ticket!(id)

      {:ok,
       socket
       |> assign(:page_title, ticket.title)
       |> assign(:org, org)
       |> assign(:can_write, Support.can_write?(membership))
       |> assign(:ticket, ticket)
       |> assign(:comments, Support.list_comments(ticket))
       |> assign(:members, Support.list_members(org))
       |> assign(:comment_form, to_form(Support.change_comment(%Comment{})))}
    else
      _ ->
        {:ok,
         socket
         |> put_flash(:error, "You do not have access to that organization.")
         |> push_navigate(to: ~p"/orgs")}
    end
  end

  @impl true
  def handle_event("set_status", %{"status" => status}, socket) do
    case Support.set_status(socket.assigns.ticket, status) do
      {:ok, ticket} -> {:noreply, assign(socket, :ticket, reload(ticket))}
      {:error, _} -> {:noreply, put_flash(socket, :error, "Invalid status.")}
    end
  end

  def handle_event("assign", %{"user_id" => ""}, socket) do
    {:ok, ticket} = Support.assign_ticket(socket.assigns.ticket, nil)
    {:noreply, assign(socket, :ticket, reload(ticket))}
  end

  def handle_event("assign", %{"user_id" => user_id}, socket) do
    user = Trackline.Accounts.get_user!(user_id)
    {:ok, ticket} = Support.assign_ticket(socket.assigns.ticket, user)
    {:noreply, assign(socket, :ticket, reload(ticket))}
  end

  def handle_event("add_comment", %{"comment" => params}, socket) do
    user = socket.assigns.current_scope.user

    case Support.add_comment(socket.assigns.ticket, user, params) do
      {:ok, _comment} ->
        {:noreply,
         socket
         |> assign(:comments, Support.list_comments(socket.assigns.ticket))
         |> assign(:comment_form, to_form(Support.change_comment(%Comment{})))}

      {:error, changeset} ->
        {:noreply, assign(socket, :comment_form, to_form(changeset))}
    end
  end

  defp reload(ticket), do: Support.get_ticket!(ticket.id)

  defp sla_state(ticket) do
    SLA.state(ticket.status, ticket.priority, ticket.inserted_at, DateTime.utc_now())
  end

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={@current_scope}>
      <.header>
        {@ticket.title}
        <:subtitle>
          <span id="ticket-status">{@ticket.status}</span>
          / <span id="ticket-priority">{@ticket.priority}</span>
          / SLA: <span id="ticket-sla">{sla_state(@ticket)}</span>
        </:subtitle>
      </.header>

      <p id="ticket-body" class="mt-4">{@ticket.body}</p>
      <p id="ticket-assignee" class="mt-2 text-sm">
        Assignee: {(@ticket.assignee && @ticket.assignee.email) || "unassigned"}
      </p>

      <div :if={@can_write} id="ticket-actions" class="mt-4 flex gap-2">
        <button
          :if={@ticket.status != "closed"}
          phx-click="set_status"
          phx-value-status="closed"
          class="btn"
        >
          Close ticket
        </button>
        <button
          :if={@ticket.status == "closed"}
          phx-click="set_status"
          phx-value-status="open"
          class="btn"
        >
          Reopen ticket
        </button>
        <button phx-click="assign" phx-value-user_id={@current_scope.user.id} class="btn">
          Assign to me
        </button>
      </div>

      <h2 class="mt-8 font-semibold">Comments</h2>
      <div id="comments" class="mt-2 space-y-3">
        <div :for={comment <- @comments} id={"comment-#{comment.id}"} class="comment">
          <span class="text-sm font-medium">{comment.author && comment.author.email}</span>
          <p>{comment.body}</p>
        </div>
      </div>

      <.form
        :if={@can_write}
        for={@comment_form}
        id="comment-form"
        phx-submit="add_comment"
        class="mt-4"
      >
        <.input field={@comment_form[:body]} type="textarea" label="Add a comment" />
        <.button>Post comment</.button>
      </.form>
    </Layouts.app>
    """
  end
end
