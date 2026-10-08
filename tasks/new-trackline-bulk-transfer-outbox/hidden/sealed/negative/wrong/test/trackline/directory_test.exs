defmodule Trackline.DirectoryTest do
  use ExUnit.Case, async: true

  alias Trackline.Directory

  @opts [plug: {Req.Test, __MODULE__}]

  test "list_contacts/2 returns contacts with atom keys" do
    Req.Test.stub(__MODULE__, fn conn ->
      assert conn.request_path == "/contacts"
      assert conn.query_string == "limit=100"
      Req.Test.json(conn, %{"contacts" => [%{"email" => "a@b.c", "name" => "A"}]})
    end)

    assert {:ok, [%{email: "a@b.c", name: "A"}]} =
             Directory.list_contacts("http://partner.test", @opts)
  end

  test "list_contacts/2 reports unexpected statuses" do
    Req.Test.stub(__MODULE__, &Plug.Conn.send_resp(&1, 503, "down"))

    assert {:error, {:unexpected_status, 503}} =
             Directory.list_contacts("http://partner.test", @opts)
  end

  test "fetch_export/2 unpacks the zip archive" do
    {:ok, {_name, zip}} =
      :zip.create(~c"export.zip", [{~c"a.txt", "alpha"}, {~c"b.txt", "beta"}], [:memory])

    Req.Test.stub(__MODULE__, fn conn ->
      conn |> Plug.Conn.put_resp_content_type("application/zip") |> Plug.Conn.send_resp(200, zip)
    end)

    assert {:ok, entries} = Directory.fetch_export("http://partner.test", @opts)
    assert Enum.sort(entries) == [{"a.txt", "alpha"}, {"b.txt", "beta"}]
  end
end
