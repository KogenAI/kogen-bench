defmodule Trackline.PortStorageTest do
  use Trackline.DataCase, async: false
  alias Trackline.Repo
  alias Trackline.Ports.{Storage, StorageBoard, Blob}
  import Trackline.AccountsFixtures
  import Trackline.SupportFixtures
  setup do
    user = user_fixture()
    org = organization_fixture(user)
    board = Repo.insert!(%StorageBoard{name: "Board", organization_id: org.id})
    ticket = ticket_fixture(org, user) |> Ecto.Changeset.change(storage_board_id: board.id) |> Repo.update!()
    comment = comment_fixture(ticket, user)
    %{org: org, board: board, ticket: ticket, comment: comment}
  end
  defp add(c, kind, id, name, bytes) do
    b = Repo.insert!(%Blob{key: "blob-#{System.unique_integer([:positive])}", byte_size: bytes})
    {:ok, a} = Storage.attach(%{blob_id: b.id, resource_type: kind, resource_id: id, name: name}, c.org.id)
    a
  end
  defp drain, do: Oban.drain_queue(queue: :default, with_scheduled: true)
  test "zero without attachments", c do
    Storage.enqueue(c.org.id)
    drain()
    assert Storage.bytes_used(c.org) == 0
    assert Storage.bytes_used(c.board) == 0
  end
  test "all four stated sources count after background drain", c do
    add(c, "Board", c.board.id, "description", 10)
    add(c, "Ticket", c.ticket.id, "image", 20)
    add(c, "Ticket", c.ticket.id, "description", 30)
    add(c, "Comment", c.comment.id, "body", 40)
    assert Storage.bytes_used(c.board) == 0
    assert %{success: n} = drain()
    assert n > 0
    assert Storage.bytes_used(c.board) == 100
    assert Storage.bytes_used(c.org) == 100
  end
  test "avatars exports and dangling resource links do not count", c do
    add(c, "Board", c.board.id, "avatar", 400)
    add(c, "Ticket", c.ticket.id, "export", 500)
    add(c, "User", 1, "avatar", 600)
    add(c, "Comment", 999_999, "body", 700)
    drain()
    assert Storage.bytes_used(c.org) == 0
  end
  test "same blob on a board is counted once", c do
    a = add(c, "Ticket", c.ticket.id, "image", 73)
    Storage.attach(%{blob_id: a.blob_id, resource_type: "Comment", resource_id: c.comment.id, name: "body"}, c.org.id)
    drain()
    assert Storage.bytes_used(c.board) == 73
  end
  test "delete refreshes persisted values and accepts stale caller structs", c do
    a = add(c, "Board", c.board.id, "description", 99)
    drain()
    assert Storage.bytes_used(c.board) == 99
    Storage.detach(a, c.org.id)
    drain()
    assert Storage.bytes_used(c.board) == 0
    assert Storage.bytes_used(c.org) == 0
  end
  test "replace before queued recount uses current state", c do
    a = add(c, "Ticket", c.ticket.id, "image", 1000)
    Storage.detach(a, c.org.id)
    add(c, "Ticket", c.ticket.id, "image", 42)
    drain()
    assert Storage.bytes_used(c.board) == 42
    Storage.enqueue(c.org.id)
    drain()
    assert Storage.bytes_used(c.board) == 42
  end
  test "boards sum and foreign organizations remain separate", c do
    other = organization_fixture()
    b2 = Repo.insert!(%StorageBoard{name: "Second", organization_id: c.org.id})
    foreign = Repo.insert!(%StorageBoard{name: "Foreign", organization_id: other.id})
    add(c, "Board", c.board.id, "description", 11)
    add(c, "Board", b2.id, "description", 12)
    add(%{c | org: other}, "Board", foreign.id, "description", 900)
    drain()
    assert Storage.bytes_used(c.org) == 23
    assert Storage.bytes_used(other) == 900
  end
  test "reads are cached and recount query count does not grow with boards", c do
    parent = self()
    name = "storage-query-#{System.unique_integer([:positive])}"
    :telemetry.attach(name, [:trackline, :repo, :query], fn _, _, _, _ -> send(parent, :query) end, nil)
    on_exit(fn -> :telemetry.detach(name) end)
    count = fn ->
      Stream.repeatedly(fn -> receive do :query -> 1 after 0 -> 0 end end) |> Enum.reduce_while(0, fn n, sum -> if n == 0, do: {:halt, sum}, else: {:cont, sum + n} end)
    end
    add(c, "Board", c.board.id, "description", 1)
    drain()
    count.()
    Trackline.Ports.RecountStorage.perform(%Oban.Job{args: %{"organization_id" => c.org.id}})
    small = count.()
    for i <- 1..25 do
      b = Repo.insert!(%StorageBoard{name: "B#{i}", organization_id: c.org.id})
      add(c, "Board", b.id, "description", 2)
    end
    count.()
    Trackline.Ports.RecountStorage.perform(%Oban.Job{args: %{"organization_id" => c.org.id}})
    large = count.()
    assert large <= small + 2
    assert Storage.bytes_used(c.org) == 51
    assert count.() <= 2
  end
end
