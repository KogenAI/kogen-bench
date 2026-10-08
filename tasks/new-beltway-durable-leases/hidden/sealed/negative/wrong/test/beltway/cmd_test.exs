defmodule Beltway.CmdTest do
  use ExUnit.Case, async: true

  alias Beltway.Cmd

  test "captures output and exit status" do
    assert {:ok, %{status: 0, output: "hi\n"}} = Cmd.run("echo", ["hi"])
    assert {:ok, %{status: 3}} = Cmd.run("sh", ["-c", "exit 3"])
  end

  test "merges stderr into the output" do
    assert {:ok, %{output: "err\n"}} = Cmd.run("sh", ["-c", "echo err >&2"])
  end

  test "passes env and cd" do
    assert {:ok, %{output: "bar\n"}} = Cmd.run("sh", ["-c", "echo $FOO"], env: [{"FOO", "bar"}])
    dir = System.tmp_dir!()
    assert {:ok, %{status: 0}} = Cmd.run("pwd", [], cd: dir)
  end
end
