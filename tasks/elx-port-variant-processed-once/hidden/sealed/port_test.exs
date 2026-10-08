defmodule Trackline.PortVariantTest do
  use TracklineWeb.ConnCase, async: false
  import Ecto.Query
  alias Trackline.Repo
  alias Trackline.Ports.{Image, Derivative, Images, DeriveImage}
  import Trackline.SupportFixtures
  setup do
    org = organization_fixture()
    counter = :atomics.new(1, [])
    previous = Application.get_env(:trackline, :image_transform)
    Application.put_env(:trackline, :image_transform, fn bytes ->
      :atomics.add(counter, 1, 1)
      "DERIVED:" <> bytes
    end)
    on_exit(fn ->
      if previous, do: Application.put_env(:trackline, :image_transform, previous), else: Application.delete_env(:trackline, :image_transform)
    end)
    %{org: org, counter: counter}
  end
  defp upload(c) do
    {:ok, image} = Images.upload(c.org, <<0, 1, 2, 255>>)
    image
  end
  defp job(image), do: %Oban.Job{args: %{"image_id" => image.id}}
  defp copies(image), do: Repo.aggregate(from(d in Derivative, where: d.image_id == ^image.id), :count)
  test "upload queues processing and does not transform in request", c do
    image = upload(c)
    assert :atomics.get(c.counter, 1) == 0
    assert copies(image) == 0
    assert %{success: 1} = Oban.drain_queue(queue: :default)
    assert copies(image) == 1
  end
  test "background then reader link then HTTP fetch uses exactly one conversion", c do
    image = upload(c)
    assert :ok = DeriveImage.perform(job(image))
    url = Images.reader_url(image)
    conn = get(c.conn, url)
    assert conn.status == 200
    assert conn.resp_body == "DERIVED:" <> image.original
    assert :atomics.get(c.counter, 1) == 1
    assert copies(image) == 1
  end
  test "duplicate jobs and repeated readers reuse persisted derivative", c do
    image = upload(c)
    for _ <- 1..4, do: assert(:ok == DeriveImage.perform(job(image)))
    url = Images.reader_url(image)
    for _ <- 1..4 do
      assert Images.reader_url(image) == url
      assert {:ok, bytes} = Images.fetch(image.id)
      assert bytes == "DERIVED:" <> image.original
    end
    assert :atomics.get(c.counter, 1) == 1
    assert copies(image) == 1
  end
  test "reader before background and later job still make one copy", c do
    image = upload(c)
    assert is_binary(Images.reader_url(image))
    assert :ok = DeriveImage.perform(job(image))
    assert {:ok, _} = Images.fetch(image.id)
    assert copies(image) == 1
    assert :atomics.get(c.counter, 1) == 1
  end
  test "persisted copy works when converter is unavailable", c do
    image = upload(c)
    DeriveImage.perform(job(image))
    Application.put_env(:trackline, :image_transform, fn _ -> raise "must not run" end)
    loaded = Repo.get!(Image, image.id)
    assert {:ok, bytes} = Images.fetch(loaded.id)
    assert bytes == "DERIVED:" <> image.original
    assert is_binary(Images.reader_url(loaded))
    assert :ok = DeriveImage.perform(job(loaded))
  end
  test "two different uploads do not share the same stored copy", c do
    one = upload(c)
    two = upload(c)
    DeriveImage.perform(job(one))
    DeriveImage.perform(job(two))
    assert copies(one) == 1
    assert copies(two) == 1
    assert Images.reader_url(one) != Images.reader_url(two)
    assert :atomics.get(c.counter, 1) == 2
  end
  test "concurrent duplicate jobs do not convert or store duplicates", c do
    image = upload(c)
    results = 1..8 |> Task.async_stream(fn _ -> DeriveImage.perform(job(image)) end, max_concurrency: 8, timeout: 5000) |> Enum.to_list()
    assert Enum.all?(results, &(&1 == {:ok, :ok}))
    assert copies(image) == 1
    assert :atomics.get(c.counter, 1) == 1
  end
  test "deleted and malformed uploads give no picture and job is harmless", c do
    image = upload(c)
    Repo.delete!(image)
    assert :ok = DeriveImage.perform(job(image))
    assert get(c.conn, "/uploads/#{image.id}/derived").status == 404
    assert get(build_conn(), "/uploads/not-a-number/derived").status == 404
    assert :atomics.get(c.counter, 1) == 0
  end
end
