defmodule TracklineWeb.OrgLive.Index do
  use TracklineWeb, :live_view

  alias Trackline.Support

  @impl true
  def mount(_params, _session, socket) do
    orgs = Support.list_organizations(socket.assigns.current_scope.user)
    {:ok, assign(socket, page_title: "Your organizations", organizations: orgs)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={@current_scope}>
      <.header>Your organizations</.header>
      <ul id="organizations" class="mt-4 space-y-2">
        <li :for={org <- @organizations} id={"org-#{org.id}"}>
          <.link navigate={~p"/orgs/#{org.slug}/tickets"} class="link">{org.name}</.link>
        </li>
      </ul>
    </Layouts.app>
    """
  end
end
