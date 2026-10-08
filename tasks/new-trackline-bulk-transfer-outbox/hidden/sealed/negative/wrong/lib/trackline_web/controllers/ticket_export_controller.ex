defmodule TracklineWeb.TicketExportController do
  use TracklineWeb, :controller

  alias Trackline.Support

  def show(conn, %{"slug" => slug, "id" => id}) do
    user = conn.assigns.current_scope.user

    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = _membership <- Support.get_membership(org, user) do
      ticket = Support.get_ticket!(id)
      comments = Support.list_comments(ticket)

      json(conn, %{
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
      })
    else
      _ -> conn |> put_status(:forbidden) |> json(%{error: "forbidden"})
    end
  end
end
