defmodule Beltway.Cmd do
  @moduledoc """
  Runs an external command and returns its combined stdout and stderr.

  Options: `:cd`, `:env` (list of `{name, value}` binaries).
  """

  @spec run(binary(), [binary()], keyword()) :: {:ok, %{status: integer(), output: binary()}}
  def run(cmd, args, opts \\ []) do
    sys_opts =
      [stderr_to_stdout: true]
      |> Keyword.merge(Keyword.take(opts, [:cd, :env]))

    {output, status} = System.cmd(cmd, args, sys_opts)
    {:ok, %{status: status, output: output}}
  end
end
