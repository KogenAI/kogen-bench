defmodule TracklineWeb.TicketLiveTest do
  use TracklineWeb.ConnCase

  import Phoenix.LiveViewTest
  import Trackline.SupportFixtures

  alias Trackline.Support

  setup :register_and_log_in_user

  setup %{user: user} do
    org = organization_fixture(user)
    %{org: org}
  end

  describe "Index" do
    test "lists the organization's tickets", %{conn: conn, user: user, org: org} do
      ticket_fixture(org, user, %{title: "Printer on fire"})
      {:ok, _lv, html} = live(conn, ~p"/orgs/#{org.slug}/tickets")
      assert html =~ "Printer on fire"
    end

    test "creates a ticket", %{conn: conn, org: org} do
      {:ok, lv, _html} = live(conn, ~p"/orgs/#{org.slug}/tickets")

      html =
        lv
        |> form("#new-ticket-form", ticket: %{title: "Broken login", priority: "high"})
        |> render_submit()

      assert html =~ "Broken login"
      assert html =~ "Ticket created."
    end

    test "redirects non-members", %{conn: conn} do
      other = organization_fixture()

      assert {:error, {:live_redirect, %{to: "/orgs"}}} =
               live(conn, ~p"/orgs/#{other.slug}/tickets")
    end

    test "viewers do not see the new ticket form", %{conn: conn, user: user} do
      viewer_org = organization_fixture()
      {:ok, _} = Support.add_member(viewer_org, user, "viewer")
      {:ok, lv, _html} = live(conn, ~p"/orgs/#{viewer_org.slug}/tickets")
      refute has_element?(lv, "#new-ticket-form")
    end
  end

  describe "Show" do
    test "shows the ticket and comments", %{conn: conn, user: user, org: org} do
      ticket = ticket_fixture(org, user, %{title: "Slow export", body: "Takes ages"})
      comment_fixture(ticket, user, "Looking into it")
      {:ok, _lv, html} = live(conn, ~p"/orgs/#{org.slug}/tickets/#{ticket.id}")
      assert html =~ "Slow export"
      assert html =~ "Takes ages"
      assert html =~ "Looking into it"
    end

    test "posts a comment", %{conn: conn, user: user, org: org} do
      ticket = ticket_fixture(org, user)
      {:ok, lv, _html} = live(conn, ~p"/orgs/#{org.slug}/tickets/#{ticket.id}")

      html = lv |> form("#comment-form", comment: %{body: "On it"}) |> render_submit()
      assert html =~ "On it"
    end

    test "closes and reopens a ticket", %{conn: conn, user: user, org: org} do
      ticket = ticket_fixture(org, user)
      {:ok, lv, _html} = live(conn, ~p"/orgs/#{org.slug}/tickets/#{ticket.id}")

      lv |> element("button", "Close ticket") |> render_click()
      assert render(lv) =~ "closed"
      lv |> element("button", "Reopen ticket") |> render_click()
      assert has_element?(lv, "#ticket-status", "open")
    end

    test "assigns to me", %{conn: conn, user: user, org: org} do
      ticket = ticket_fixture(org, user)
      {:ok, lv, _html} = live(conn, ~p"/orgs/#{org.slug}/tickets/#{ticket.id}")
      lv |> element("button", "Assign to me") |> render_click()
      assert has_element?(lv, "#ticket-assignee", user.email)
    end

    test "viewers do not get action buttons", %{conn: conn, user: user} do
      org = organization_fixture()
      {:ok, _} = Support.add_member(org, user, "viewer")
      ticket = ticket_fixture(org, org_owner(org), %{})
      {:ok, lv, _html} = live(conn, ~p"/orgs/#{org.slug}/tickets/#{ticket.id}")
      refute has_element?(lv, "#ticket-actions")
      refute has_element?(lv, "#comment-form")
    end
  end

  defp org_owner(org) do
    import Ecto.Query

    Trackline.Repo.one!(
      from u in Trackline.Accounts.User,
        join: m in Trackline.Support.Membership,
        on: m.user_id == u.id,
        where: m.organization_id == ^org.id and m.role == "owner"
    )
  end
end
