defmodule Kogen.Core do
  @moduledoc "Compare-and-swap Git ref landing."

  @usage "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID"
  @invalid "cas-land: invalid repository or commit"

  def execute(args) do
    values = parse(args, %{})

    if map_size(values) != 4 do
      Kogen.Input.fail(@usage, 2)
    end

    land_values(values)
  end

  defp land_values(values) do
    repo = values["--repo"]
    target = values["--target"]
    base = values["--base"]
    candidate = values["--candidate"]

    unless String.starts_with?(target, "refs/") and
             git(repo, ["check-ref-format", target]) == {:ok, ""} do
      Kogen.Input.fail(@invalid)
    end

    parents = git!(repo, ["rev-list", "--parents", "-n", "1", candidate]) |> String.split()

    unless length(parents) == 2 and Enum.at(parents, 1) == base do
      Kogen.Input.fail(@invalid)
    end

    current = git!(repo, ["rev-parse", "--verify", target])
    rebased = current != base
    landing = if rebased, do: rebase(repo, current, base, candidate), else: candidate
    label = if rebased, do: "rebased", else: "landed"
    success_code = if rebased, do: 10, else: 0

    update(repo, target, current, landing, label, success_code)
  end

  defp update(repo, target, current, landing, label, success_code) do
    case git(repo, ["update-ref", target, landing, current]) do
      {:ok, _} -> {"#{label} #{landing}\n", success_code}
      _ -> Kogen.Input.fail("cas-land: lost race", 30)
    end
  end

  defp parse([], values), do: values

  defp parse([flag, value | rest], values)
       when flag in ["--repo", "--target", "--base", "--candidate"] do
    if Map.has_key?(values, flag) or value == "" do
      Kogen.Input.fail(@usage, 2)
    end

    parse(rest, Map.put(values, flag, value))
  end

  defp parse(_args, _values), do: Kogen.Input.fail(@usage, 2)

  defp git(repo, args) do
    path = System.get_env("PATH", "")

    executable =
      path
      |> String.split(":")
      |> Enum.find_value(fn directory ->
        candidate = Path.join(directory, "git")
        if File.regular?(candidate), do: candidate
      end) || "git"

    case System.cmd(executable, ["-C", repo | args],
           stderr_to_stdout: true,
           env: [{"PATH", path}]
         ) do
      {output, 0} -> {:ok, String.trim(output)}
      {output, code} -> {:error, {code, output}}
    end
  end

  defp git!(repo, args) do
    case git(repo, args) do
      {:ok, output} -> output
      _ -> Kogen.Input.fail(@invalid)
    end
  end

  defp rebase(repo, current, base, candidate) do
    work =
      Path.join(
        System.tmp_dir!(),
        "cas-land-#{System.pid()}-#{System.unique_integer([:positive])}"
      )

    case git(repo, ["worktree", "add", "--detach", work, candidate]) do
      {:ok, _} ->
        try do
          case git(work, ["rebase", "--onto", current, base]) do
            {:ok, _} ->
              git!(work, ["rev-parse", "HEAD"])

            {:error, _} ->
              conflict =
                case git(work, ["diff", "--name-only", "--diff-filter=U"]) do
                  {:ok, paths} -> paths != ""
                  _ -> false
                end

              _ = git(work, ["rebase", "--abort"])

              if conflict,
                do: Kogen.Input.fail("cas-land: conflict", 20),
                else: Kogen.Input.fail(@invalid)
          end
        after
          _ = git(repo, ["worktree", "remove", "--force", work])
          File.rm_rf(work)
        end

      _ ->
        Kogen.Input.fail(@invalid)
    end
  end
end
