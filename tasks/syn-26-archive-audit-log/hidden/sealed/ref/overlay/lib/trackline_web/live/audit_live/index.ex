defmodule TracklineWeb.AuditLive.Index do
  use TracklineWeb, :live_view

  alias Trackline.Support

  @impl true
  def mount(%{"slug" => slug}, _session, socket) do
    user = socket.assigns.current_scope.user

    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = membership <- Support.get_membership(org, user),
         true <- Support.can_archive?(membership) do
      {:ok,
       socket
       |> assign(:page_title, "Activity log")
       |> assign(:org, org)
       |> assign(:events, Support.list_audit_log(org))}
    else
      _ ->
        {:ok,
         socket
         |> put_flash(:error, "You do not have access to that page.")
         |> push_navigate(to: ~p"/orgs")}
    end
  end

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={@current_scope}>
      <.header>{@org.name} activity log</.header>
      <table id="audit-log" class="table mt-6">
        <thead>
          <tr>
            <th>When</th>
            <th>Who</th>
            <th>What</th>
            <th>Ticket</th>
          </tr>
        </thead>
        <tbody>
          <tr :for={event <- @events} id={"audit-#{event.id}"}>
            <td>{event.inserted_at}</td>
            <td class="audit-actor">{event.actor && event.actor.email}</td>
            <td class="audit-action">{event.action}</td>
            <td>{event.ticket && event.ticket.title}</td>
          </tr>
        </tbody>
      </table>
    </Layouts.app>
    """
  end
end
