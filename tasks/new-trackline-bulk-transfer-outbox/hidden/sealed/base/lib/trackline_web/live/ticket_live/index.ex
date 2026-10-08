defmodule TracklineWeb.TicketLive.Index do
  use TracklineWeb, :live_view

  alias Trackline.Support
  alias Trackline.Support.Ticket

  @impl true
  def mount(%{"slug" => slug}, _session, socket) do
    user = socket.assigns.current_scope.user

    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = membership <- Support.get_membership(org, user) do
      {:ok,
       socket
       |> assign(:page_title, "Tickets")
       |> assign(:org, org)
       |> assign(:can_write, Support.can_write?(membership))
       |> assign(:form, to_form(Support.change_ticket(%Ticket{})))}
    else
      _ ->
        {:ok,
         socket
         |> put_flash(:error, "You do not have access to that organization.")
         |> push_navigate(to: ~p"/orgs")}
    end
  end

  @impl true
  def handle_params(_params, _uri, socket) do
    {:noreply, assign(socket, :tickets, Support.list_tickets(socket.assigns.org))}
  end

  @impl true
  def handle_event("validate", %{"ticket" => params}, socket) do
    form = %Ticket{} |> Support.change_ticket(params) |> to_form(action: :validate)
    {:noreply, assign(socket, :form, form)}
  end

  def handle_event("create_ticket", %{"ticket" => params}, socket) do
    user = socket.assigns.current_scope.user

    case Support.create_ticket(socket.assigns.org, user, params) do
      {:ok, _ticket} ->
        {:noreply,
         socket
         |> assign(:tickets, Support.list_tickets(socket.assigns.org))
         |> assign(:form, to_form(Support.change_ticket(%Ticket{})))
         |> put_flash(:info, "Ticket created.")}

      {:error, changeset} ->
        {:noreply, assign(socket, :form, to_form(changeset))}
    end
  end

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={@current_scope}>
      <.header>
        {@org.name} tickets
      </.header>

      <table id="tickets" class="table mt-6">
        <thead>
          <tr>
            <th>Title</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Author</th>
            <th>Assignee</th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          <tr :for={ticket <- @tickets} id={"ticket-#{ticket.id}"}>
            <td>
              <.link navigate={~p"/orgs/#{@org.slug}/tickets/#{ticket.id}"} class="link">
                {ticket.title}
              </.link>
            </td>
            <td class="ticket-status">{ticket.status}</td>
            <td class="ticket-priority">{ticket.priority}</td>
            <td>{ticket.author && ticket.author.email}</td>
            <td>{ticket.assignee && ticket.assignee.email}</td>
            <td>{ticket.comment_count}</td>
          </tr>
        </tbody>
      </table>

      <div :if={@can_write} class="mt-8">
        <.form for={@form} id="new-ticket-form" phx-change="validate" phx-submit="create_ticket">
          <.input field={@form[:title]} type="text" label="Title" />
          <.input field={@form[:body]} type="textarea" label="Description" />
          <.input
            field={@form[:priority]}
            type="select"
            label="Priority"
            options={Ticket.priorities()}
          />
          <.button>New ticket</.button>
        </.form>
      </div>
    </Layouts.app>
    """
  end
end
