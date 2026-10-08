defmodule Beltway.CLITest do
  use ExUnit.Case, async: true

  alias Beltway.CLI

  @moduletag :tmp_dir

  defp run(argv) do
    {:ok, out} = StringIO.open("")
    {:ok, err} = StringIO.open("")
    code = CLI.run(argv, stdout: out, stderr: err)
    {code, elem(StringIO.contents(out), 1), elem(StringIO.contents(err), 1)}
  end

  test "count prints lines per level", %{tmp_dir: dir} do
    path = Path.join(dir, "a.log")

    File.write!(path, """
    2026-03-01T10:00:00Z ERROR api boom
    2026-03-01T10:00:01Z INFO web ok
    2026-03-01T10:00:02Z INFO api ok
    garbage
    """)

    assert {0, "ERROR 1\nINFO 2\n", ""} = run(["count", path])
  end

  test "missing file exits 1", %{tmp_dir: dir} do
    assert {1, "", err} = run(["count", Path.join(dir, "nope.log")])
    assert err =~ "cannot read"
  end

  test "unknown command exits 2" do
    assert {2, "", err} = run(["frobnicate"])
    assert err =~ "usage:"
  end
end
