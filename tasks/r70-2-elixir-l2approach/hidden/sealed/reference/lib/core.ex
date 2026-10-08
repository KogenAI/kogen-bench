defmodule Kogen.Input do
  @moduledoc false

  @spec physical_lines(binary()) :: [binary()]
  def physical_lines(input) do
    normalized = input |> String.replace("\r\n", "\n") |> String.replace("\r", "\n")
    lines = String.split(normalized, "\n", trim: false)

    if String.ends_with?(normalized, "\n"), do: Enum.drop(lines, -1), else: lines
  end
end

defmodule Kogen.Core do
  @moduledoc "Linux process-group supervision."

  def execute(args) do
    with {:ok, timeout, grace, command, rest} <- parse(args),
         {:ok, port, pgid} <- start(command, rest) do
      deadline = System.monotonic_time(:millisecond) + timeout

      case wait_group(port, pgid, deadline) do
        {:done, code} ->
          {:ok, code, line("exited", code, false, false)}

        :timeout ->
          timeout(port, pgid, grace)
      end
    else
      :error -> {:error, 2, "error: invalid arguments"}
      {:error, code, message} -> {:error, code, message}
    end
  end

  defp timeout(port, pgid, grace) do
    signal(pgid, "TERM")
    grace_end = System.monotonic_time(:millisecond) + grace
    wait_grace(port, pgid, grace_end)
    kill_sent = live?(pgid)

    if kill_sent do
      signal(pgid, "KILL")
      wait_dead(port, pgid)
    end

    _ = exit_code(port)
    {:ok, 124, line("timeout", 124, true, kill_sent)}
  end

  defp parse(["supervise", "--timeout-ms", timeout, "--grace-ms", grace, "--", command | args])
       when command != "" do
    with {:ok, t} <- number(timeout), {:ok, g} <- number(grace), do: {:ok, t, g, command, args}
  end

  defp parse(_), do: :error

  defp number(value) do
    if Regex.match?(~r/^[0-9]+$/, value) do
      case Integer.parse(value) do
        {n, ""} when n >= 1 and n <= 60_000 -> {:ok, n}
        _ -> :error
      end
    else
      :error
    end
  end

  defp start(command, args) do
    if executable?(command) do
      start_port(command, args)
    else
      {:error, 127, "error: cannot start command"}
    end
  end

  defp start_port(command, args) do
    group_file =
      Path.join(
        System.tmp_dir!(),
        "r70-pgid-#{System.pid()}-#{System.unique_integer([:positive, :monotonic])}"
      )

    wrapper =
      "exec 3>&2; exec 2>/dev/null; /usr/bin/setsid --wait /bin/sh -c 'printf \"%s\" \"$$\" > \"$1\"; shift; exec 2>&3; exec 0</dev/null; exec \"$@\"' kogen-supervise \"$@\"; exit $?"

    port =
      Port.open(
        {:spawn_executable, ~c"/bin/sh"},
        [
          :binary,
          :exit_status,
          :use_stdio,
          args:
            Enum.map(
              ["-c", wrapper, "kogen-supervise", group_file, command | args],
              &String.to_charlist/1
            )
        ]
      )

    case read_group_file(group_file, System.monotonic_time(:millisecond) + 3000) do
      {:ok, pgid} ->
        File.rm(group_file)
        {:ok, port, pgid}

      :error ->
        File.rm(group_file)
        {:error, 127, "error: cannot start command"}
    end
  rescue
    _ -> {:error, 127, "error: cannot start command"}
  end

  defp read_group_file(path, deadline) do
    case File.read(path) do
      {:ok, contents} ->
        case Integer.parse(contents) do
          {pgid, ""} when pgid > 0 ->
            {:ok, pgid}

          _ ->
            retry_group_file(path, deadline)
        end

      _ ->
        retry_group_file(path, deadline)
    end
  end

  defp retry_group_file(path, deadline) do
    if System.monotonic_time(:millisecond) >= deadline do
      File.rm(path)
      :error
    else
      Process.sleep(1)
      read_group_file(path, deadline)
    end
  end

  defp executable?(command) do
    candidate =
      if String.contains?(command, "/"), do: command, else: System.find_executable(command)

    case candidate do
      nil ->
        false

      path ->
        case File.stat(path) do
          {:ok, %{type: :regular, mode: mode}} -> Bitwise.band(mode, 0o111) != 0
          _ -> false
        end
    end
  end

  defp wait_group(port, pgid, deadline) do
    cond do
      not live?(pgid) ->
        {:done, exit_code(port)}

      System.monotonic_time(:millisecond) >= deadline ->
        :timeout

      true ->
        _ = receive_port(port, 250)
        wait_group(port, pgid, deadline)
    end
  end

  defp wait_grace(port, pgid, deadline) do
    if System.monotonic_time(:millisecond) < deadline do
      _ = receive_port(port, 5)
      wait_grace(port, pgid, deadline)
    end
  end

  defp wait_dead(port, pgid) do
    if live?(pgid) do
      _ = receive_port(port, 20)
      wait_dead(port, pgid)
    end
  end

  defp receive_port(port, timeout) do
    receive do
      {^port, {:data, bytes}} ->
        IO.binwrite(:stdio, bytes)
        :data

      {^port, {:exit_status, code}} ->
        :erlang.put({:kogen_exit, port}, code)
        {:exit, code}

      {^port, :eof} ->
        :eof
    after
      timeout -> :wait
    end
  end

  defp exit_code(port) do
    case :erlang.get({:kogen_exit, port}) do
      code when code in [nil, :undefined] ->
        receive do
          {^port, {:data, bytes}} ->
            IO.binwrite(:stdio, bytes)
            exit_code(port)

          {^port, {:exit_status, code}} ->
            :erlang.put({:kogen_exit, port}, code)
            code
        end

      code ->
        code
    end
  end

  defp signal(pgid, name) do
    _ = System.cmd("/bin/kill", ["-#{name}", "--", "-#{pgid}"], stderr_to_stdout: true)
    :ok
  end

  defp live?(pgid) do
    case System.cmd("/usr/bin/ps", ["-eo", "pgid=,stat="], stderr_to_stdout: true) do
      {output, 0} -> live_lines?(output, pgid)
      _ -> false
    end
  end

  defp live_lines?(output, pgid) do
    output
    |> String.split("\n", trim: true)
    |> Enum.any?(fn line ->
      case String.split(line, " ", trim: true) do
        [group, state | _] ->
          group == Integer.to_string(pgid) and String.first(state) not in ["Z", "X"]

        _ ->
          false
      end
    end)
  end

  defp line(kind, code, term, kill) do
    "status=#{kind} exit_code=#{code} term_sent=#{bool(term)} kill_sent=#{bool(kill)} reaped=1\n"
  end

  defp bool(true), do: "true"
  defp bool(false), do: "false"
end
