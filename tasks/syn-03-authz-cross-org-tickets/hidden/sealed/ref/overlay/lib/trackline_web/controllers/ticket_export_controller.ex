defmodule TracklineWeb.TicketExportController do
  use TracklineWeb, :controller

  alias Trackline.Support

  def show(conn, %{"slug" => slug, "id" => id}) do
    user = conn.assigns.current_scope.user

    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = _membership <- Support.get_membership(org, user) do
      case Support.get_ticket(org, id) do
        nil -> conn |> put_status(:not_found) |> json(%{error: "not found"})
        ticket -> json(conn, export(ticket))
      end
    else
      _ -> conn |> put_status(:forbidden) |> json(%{error: "forbidden"})
    end
  end

  defp export(ticket) do
    comments = Support.list_comments(ticket)

    %{
      id: ticket.id,
      title: ticket.title,
      body: ticket.body,
      status: ticket.status,
      priority: ticket.priority,
      author: ticket.author && ticket.author.email,
      assignee: ticket.assignee && ticket.assignee.email,
      comments:
        Enum.map(comments, fn c ->
          %{id: c.id, author: c.author && c.author.email, body: c.body}
        end)
    }
  end
end
