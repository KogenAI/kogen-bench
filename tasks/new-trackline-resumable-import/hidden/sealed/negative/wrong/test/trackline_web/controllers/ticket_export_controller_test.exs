defmodule TracklineWeb.TicketExportControllerTest do
  use TracklineWeb.ConnCase

  import Trackline.SupportFixtures

  setup :register_and_log_in_user

  test "exports a ticket for members", %{conn: conn, user: user} do
    org = organization_fixture(user)
    ticket = ticket_fixture(org, user, %{title: "Export me"})
    comment_fixture(ticket, user, "hello")

    body =
      conn |> get(~p"/orgs/#{org.slug}/tickets/#{ticket.id}/export.json") |> json_response(200)

    assert body["title"] == "Export me"
    assert [%{"body" => "hello"}] = body["comments"]
  end

  test "forbids non-members", %{conn: conn} do
    org = organization_fixture()
    ticket = ticket_fixture(org, org_owner(org))
    conn = get(conn, ~p"/orgs/#{org.slug}/tickets/#{ticket.id}/export.json")
    assert json_response(conn, 403)
  end

  defp org_owner(org) do
    import Ecto.Query

    Trackline.Repo.one!(
      from u in Trackline.Accounts.User,
        join: m in Trackline.Support.Membership,
        on: m.user_id == u.id,
        where: m.organization_id == ^org.id
    )
  end
end
