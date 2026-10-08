defmodule Trackline.PortPublicationTest do
  use TracklineWeb.ConnCase, async: false
  alias Trackline.{Repo, Support}
  alias Trackline.Ports.{Board, Column, Card, Publication}
  import Trackline.AccountsFixtures
  import Trackline.SupportFixtures
  setup do
    owner = user_fixture()
    org = organization_fixture(owner)
    board = Repo.insert!(%Board{name: "Private board", organization_id: org.id})
    column = Repo.insert!(%Column{name: "Backlog", board_id: board.id})
    card = Repo.insert!(%Card{title: "Visible", board_id: board.id, column_id: column.id, number: 7, published: true})
    draft = Repo.insert!(%Card{title: "Secret draft", board_id: board.id, column_id: column.id, number: 8})
    %{owner: owner, org: org, board: board, column: column, card: card, draft: draft}
  end
  test "unpublished board JSON and public access are closed", c do
    assert Publication.board_json(c.board).public_url == nil
    assert Publication.public_board("missing") == nil
    assert get(build_conn(), "/public/boards/missing").status == 404
  end
  test "owner publishes a secret URL and visitor can open board", c do
    conn = c.conn |> log_in_user(c.owner) |> post("/boards/#{c.board.id}/publication")
    assert conn.status == 200
    url = json_response(conn, 200)["public_url"]
    assert is_binary(url)
    board = Repo.get!(Board, c.board.id)
    assert String.length(board.public_key) >= 20
    assert get(build_conn(), url).status == 200
    assert Publication.public_board(board.public_key).id == board.id
  end
  test "agent viewer and outsider cannot publish or unpublish", c do
    {:ok, published} = Publication.publish(c.board, c.owner)
    for actor <- [member_fixture(c.org, "agent"), member_fixture(c.org, "viewer"), user_fixture()] do
      assert Publication.publish(c.board, actor) == {:error, :forbidden}
      assert Publication.unpublish(published, actor) == {:error, :forbidden}
      conn = build_conn() |> log_in_user(actor) |> delete("/boards/#{c.board.id}/publication")
      assert conn.status == 403
    end
    assert Repo.get!(Board, c.board.id).public_key == published.public_key
  end
  test "owner in another organization cannot use ownership across boundary", c do
    other = user_fixture()
    organization_fixture(other)
    assert Publication.publish(c.board, other) == {:error, :forbidden}
  end
  test "public column and published card routes need no sign in", c do
    {:ok, b} = Publication.publish(c.board, c.owner)
    assert get(build_conn(), "/public/boards/#{b.public_key}/columns/#{c.column.id}").status == 200
    assert get(build_conn(), "/public/boards/#{b.public_key}/cards/7").status == 200
    assert Publication.public_card(b.public_key, 7).id == c.card.id
  end
  test "drafts and unknown resources never open publicly", c do
    {:ok, b} = Publication.publish(c.board, c.owner)
    for number <- [8, 999, "bad"] do
      assert get(build_conn(), "/public/boards/#{b.public_key}/cards/#{number}").status == 404
    end
    assert get(build_conn(), "/public/boards/#{b.public_key}/columns/bad").status == 404
  end
  test "foreign columns and card numbers are scoped to the published board", c do
    {:ok, b} = Publication.publish(c.board, c.owner)
    other = Repo.insert!(%Board{name: "Other", organization_id: c.org.id})
    col = Repo.insert!(%Column{name: "Secret", board_id: other.id})
    Repo.insert!(%Card{title: "Foreign", board_id: other.id, column_id: col.id, number: 9, published: true})
    assert Publication.public_column(b.public_key, col.id) == nil
    assert Publication.public_card(b.public_key, 9) == nil
    assert get(build_conn(), "/public/boards/#{b.public_key}/columns/#{col.id}").status == 404
  end
  test "unpublish closes all deep links even using a stale struct", c do
    {:ok, b} = Publication.publish(c.board, c.owner)
    {:ok, gone} = Publication.unpublish(c.board, c.owner)
    assert Publication.board_json(gone).public_url == nil
    assert Publication.public_board(b.public_key) == nil
    assert Publication.public_column(b.public_key, c.column.id) == nil
    assert Publication.public_card(b.public_key, 7) == nil
  end
  test "revoked owner from a stale request cannot change publication", c do
    {:ok, b} = Publication.publish(c.board, c.owner)
    Repo.delete!(Support.get_membership(c.org, c.owner))
    assert Publication.unpublish(b, c.owner) == {:error, :forbidden}
    assert Publication.public_board(b.public_key).id == b.id
  end
end
