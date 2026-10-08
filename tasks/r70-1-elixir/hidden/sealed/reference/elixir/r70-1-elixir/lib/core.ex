defmodule Kogen.Core do
  @moduledoc "Durable serial job queue implementation."
  @id ~r/^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/

  @doc "Execute the public queue command."
  def execute(args) do
    case parse(args) do
      {:ok, _command, values} ->
        store = values["--store"]

        case File.mkdir_p(store) do
          :ok ->
            run_with_lock(store, args)

          {:error, _} ->
            Kogen.Input.fail("error: store failure", 4)
        end

      :error ->
        Kogen.Input.fail("error: invalid arguments", 2)
    end
  end

  defp run_with_lock(store, args) do
    case acquire_lock(store, 0) do
      :ok ->
        try do
          execute_locked(args)
        after
          release_lock(store)
        end

      {:store_error, _reason} ->
        Kogen.Input.fail("error: store failure", 4)
    end
  end

  defp execute_locked(args) do
    with {:ok, command, values} <- parse(args),
         {:ok, state} <- read_state(values["--store"]) do
      case command do
        "add" -> add(values, state)
        "status" -> status(state)
        "run" -> run(values["--store"], state)
      end
    else
      :error -> Kogen.Input.fail("error: invalid arguments", 2)
      {:store_error, _} -> Kogen.Input.fail("error: store failure", 4)
    end
  end

  defp parse(["queue", command | args]) when command in ["add", "run", "status"] do
    allowed = allowed_options(command)

    case options(args, allowed, %{}) do
      {:ok, values} ->
        if valid_values?(command, values), do: {:ok, command, values}, else: :error

      :error ->
        :error
    end
  end

  defp parse(_), do: :error

  defp allowed_options("add"), do: ["--store", "--id", "--argv"]
  defp allowed_options(_), do: ["--store"]

  defp valid_values?("add", values) do
    Map.has_key?(values, "--store") and values["--store"] != "" and
      Map.has_key?(values, "--id") and Regex.match?(@id, values["--id"]) and
      Map.has_key?(values, "--argv") and values["--argv"] != ""
  end

  defp valid_values?(_command, values),
    do: Map.has_key?(values, "--store") and values["--store"] != "" and map_size(values) == 1

  defp options([], _allowed, values), do: {:ok, values}

  defp options([key, value | rest], allowed, values) do
    if key in allowed and not Map.has_key?(values, key),
      do: options(rest, allowed, Map.put(values, key, value)),
      else: :error
  end

  defp options(_, _, _), do: :error

  defp acquire_lock(store, attempts) do
    lock = Path.join(store, ".lock")

    case File.mkdir(lock) do
      :ok ->
        write_lock_owner(lock)

      {:error, :eexist} ->
        wait_for_lock(store, lock, attempts)
        acquire_lock(store, attempts + 1)

      error ->
        {:store_error, error}
    end
  end

  defp write_lock_owner(lock) do
    owner =
      Enum.join([System.pid(), boot_id(), process_start_time(System.pid()) || "unknown"], "\n")

    case File.write(Path.join(lock, "owner"), owner) do
      :ok ->
        :ok

      error ->
        File.rmdir(lock)
        {:store_error, error}
    end
  end

  defp wait_for_lock(store, lock, attempts) do
    case File.read(Path.join(lock, "owner")) do
      {:ok, owner} -> wait_for_owner(store, lock, owner)
      _ -> wait_for_ownerless(store, lock, attempts)
    end
  end

  defp wait_for_owner(store, lock, owner) do
    if owner_alive?(owner), do: Process.sleep(10), else: reap_lock(store, lock)
  end

  defp wait_for_ownerless(store, lock, attempts) do
    if attempts > 500, do: reap_lock(store, lock), else: Process.sleep(10)
  end

  defp owner_alive?(owner) do
    case String.split(owner, "\n") do
      [pid, boot, _start] ->
        boot == boot_id() and process_exists?(pid)

      _ ->
        false
    end
  end

  defp process_exists?(pid) do
    case File.stat("/proc/#{pid}") do
      {:ok, _stat} -> true
      _ -> false
    end
  end

  defp boot_id do
    case File.read("/proc/sys/kernel/random/boot_id") do
      {:ok, value} -> String.trim(value)
      _ -> "unknown"
    end
  end

  defp process_start_time(pid) do
    case File.read("/proc/#{pid}/stat") do
      {:ok, stat} ->
        stat |> String.split(")") |> List.last() |> String.trim() |> String.split() |> Enum.at(19)

      _ ->
        nil
    end
  end

  defp reap_lock(store, lock) do
    gate = Path.join(lock, ".reaper")

    case File.mkdir(gate) do
      :ok ->
        quarantine =
          Path.join(store, ".lock-stale-#{System.pid()}-#{System.unique_integer([:positive])}")

        case File.rename(lock, quarantine) do
          :ok -> File.rm_rf(quarantine)
          _ -> File.rmdir(gate)
        end

      _ ->
        :ok
    end
  end

  defp release_lock(store) do
    lock = Path.join(store, ".lock")
    File.rm(Path.join(lock, "owner"))
    File.rmdir(lock)
    :ok
  end

  defp read_state(store) do
    case File.read(Path.join(store, "state.json")) do
      {:ok, bytes} ->
        case Jason.decode(bytes) do
          {:ok, %{"jobs" => jobs}} when is_list(jobs) -> {:ok, jobs}
          _ -> {:store_error, :corrupt}
        end

      {:error, :enoent} ->
        {:ok, []}

      error ->
        {:store_error, error}
    end
  end

  defp add(values, jobs) do
    id = values["--id"]
    if Enum.any?(jobs, &(&1["id"] == id)), do: Kogen.Input.fail("error: duplicate job id", 3)

    with {:ok, argv} when is_list(argv) <- Jason.decode(values["--argv"]),
         true <-
           argv != [] and
             Enum.all?(argv, &(is_binary(&1) and &1 != "" and not String.contains?(&1, <<0>>))),
         job <- %{
           "id" => id,
           "argv" => argv,
           "attempts" => 0,
           "done" => false,
           "exit_code" => 0,
           "stdout" => "",
           "stderr" => ""
         },
         :ok <- write_state(values["--store"], jobs ++ [job]) do
      "queued #{id}\n"
    else
      {:error, _} -> Kogen.Input.fail("error: invalid arguments", 2)
      false -> Kogen.Input.fail("error: invalid arguments", 2)
      {:store_error, _} -> Kogen.Input.fail("error: store failure", 4)
      _ -> Kogen.Input.fail("error: invalid arguments", 2)
    end
  end

  defp status(jobs) do
    Enum.map_join(jobs, "", fn job ->
      cond do
        not job["done"] -> "#{job["id"]} pending\n"
        job["exit_code"] == 0 -> "#{job["id"]} succeeded\n"
        true -> "#{job["id"]} failed #{job["exit_code"]}\n"
      end
    end)
  end

  defp run(store, jobs) do
    {_updated, rows} = Enum.reduce(jobs, {jobs, []}, &run_job(&1, store, &2))

    Enum.join(rows)
  end

  defp run_job(%{"done" => true}, _store, state_and_rows), do: state_and_rows

  defp run_job(job, store, {state, rows}) do
    started = %{job | "attempts" => job["attempts"] + 1}
    current = replace_job(state, job["id"], started)
    ensure_store(write_state(store, current))
    {code, stdout, stderr} = execute_child(started["argv"])

    complete = %{
      started
      | "done" => true,
        "exit_code" => code,
        "stdout" => stdout,
        "stderr" => stderr
    }

    next = replace_job(current, job["id"], complete)
    ensure_store(write_state(store, next))
    status = if code == 0, do: "succeeded", else: "failed"
    row = result_line(job, started, code, stdout, stderr, status)
    {next, rows ++ [row]}
  end

  defp result_line(job, started, code, stdout, stderr, status) do
    "{\"id\":" <>
      encode_json(job["id"]) <>
      ",\"attempt\":" <>
      Integer.to_string(started["attempts"]) <>
      ",\"exit_code\":" <>
      Integer.to_string(code) <>
      ",\"stdout\":" <>
      encode_json(stdout) <>
      ",\"stderr\":" <>
      encode_json(stderr) <> ",\"status\":" <> encode_json(status) <> "}\n"
  end

  defp encode_json(value) when is_binary(value), do: json_quote(value)
  defp encode_json(value) when is_integer(value), do: Integer.to_string(value)
  defp encode_json(true), do: "true"
  defp encode_json(false), do: "false"
  defp encode_json(nil), do: "null"

  defp encode_json(values) when is_list(values),
    do: "[" <> Enum.map_join(values, ",", &encode_json/1) <> "]"

  defp encode_json(values) when is_map(values) do
    entries =
      Enum.map_join(values, ",", fn {key, value} ->
        json_quote(key) <> ":" <> encode_json(value)
      end)

    "{" <> entries <> "}"
  end

  defp json_quote(value) do
    escaped =
      value |> String.to_charlist() |> Enum.map(&json_character/1) |> IO.iodata_to_binary()

    "\"" <> escaped <> "\""
  end

  defp json_character(?\"), do: "\\\""
  defp json_character(?\\), do: "\\\\"
  defp json_character(?\b), do: "\\b"
  defp json_character(?\f), do: "\\f"
  defp json_character(?\n), do: "\\n"
  defp json_character(?\r), do: "\\r"
  defp json_character(?\t), do: "\\t"

  defp json_character(character) when character < 0x20 do
    ["\\u00", Base.encode16(<<character>>, case: :lower)]
  end

  defp json_character(character) when character <= 0x7E, do: <<character>>

  defp json_character(character) when character <= 0xFFFF do
    ["\\u", hex4(character)]
  end

  defp json_character(character) do
    value = character - 0x10000
    high = 0xD800 + div(value, 0x400)
    low = 0xDC00 + rem(value, 0x400)
    ["\\u", hex4(high), "\\u", hex4(low)]
  end

  defp hex4(value), do: value |> Integer.to_string(16) |> String.pad_leading(4, "0")

  defp replace_job(jobs, id, replacement),
    do: Enum.map(jobs, fn job -> if job["id"] == id, do: replacement, else: job end)

  defp ensure_store(:ok), do: :ok
  defp ensure_store({:store_error, _reason}), do: Kogen.Input.fail("error: store failure", 4)

  defp execute_child([executable | args]) do
    case executable?(executable) do
      false -> {127, "", "exec failed\n"}
      true -> run_executable(executable, args)
    end
  end

  defp run_executable(executable, args) do
    nonce = Integer.to_string(System.unique_integer([:positive, :monotonic]))
    out = Path.join(System.tmp_dir!(), "kogen-out-#{nonce}")
    err = Path.join(System.tmp_dir!(), "kogen-err-#{nonce}")
    script = "exec \"$@\" > \"$KOGEN_OUT\" 2> \"$KOGEN_ERR\""

    {_output, code} =
      System.cmd("sh", ["-c", script, "kogen", executable | args],
        env: [{"KOGEN_OUT", out}, {"KOGEN_ERR", err}]
      )

    stdout = read_output(out)
    stderr = read_output(err)
    File.rm(out)
    File.rm(err)
    {code, repair_utf8(stdout), repair_utf8(stderr)}
  end

  defp repair_utf8(bytes), do: repair_utf8(bytes, <<>>)
  defp repair_utf8(<<>>, output), do: output

  defp repair_utf8(<<first, rest::binary>>, output) when first < 0x80,
    do: repair_utf8(rest, output <> <<first>>)

  defp repair_utf8(<<first, second, rest::binary>>, output)
       when first in 0xC2..0xDF and second in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<first, second>>)

  defp repair_utf8(<<0xE0, second, third, rest::binary>>, output)
       when second in 0xA0..0xBF and third in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<0xE0, second, third>>)

  defp repair_utf8(<<0xED, second, third, rest::binary>>, output)
       when second in 0x80..0x9F and third in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<0xED, second, third>>)

  defp repair_utf8(<<first, second, third, rest::binary>>, output)
       when first in 0xE1..0xEC and second in 0x80..0xBF and third in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<first, second, third>>)

  defp repair_utf8(<<first, second, third, rest::binary>>, output)
       when first in 0xEE..0xEF and second in 0x80..0xBF and third in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<first, second, third>>)

  defp repair_utf8(<<0xF0, second, third, fourth, rest::binary>>, output)
       when second in 0x90..0xBF and third in 0x80..0xBF and fourth in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<0xF0, second, third, fourth>>)

  defp repair_utf8(<<0xF4, second, third, fourth, rest::binary>>, output)
       when second in 0x80..0x8F and third in 0x80..0xBF and fourth in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<0xF4, second, third, fourth>>)

  defp repair_utf8(<<first, second, third, fourth, rest::binary>>, output)
       when first in 0xF1..0xF3 and second in 0x80..0xBF and third in 0x80..0xBF and
              fourth in 0x80..0xBF,
       do: repair_utf8(rest, output <> <<first, second, third, fourth>>)

  defp repair_utf8(<<_invalid, rest::binary>>, output),
    do: repair_utf8(rest, output <> <<0xEF, 0xBF, 0xBD>>)

  defp executable?(path) do
    found = if String.contains?(path, "/"), do: path, else: System.find_executable(path)

    case found && File.stat(found) do
      {:ok, %{type: :regular, mode: mode}} -> Bitwise.band(mode, 0o111) != 0
      _ -> false
    end
  end

  defp read_output(path) do
    case File.read(path) do
      {:ok, bytes} -> bytes
      _ -> ""
    end
  end

  defp write_state(store, jobs) do
    path = Path.join(store, "state.json")
    temp = Path.join(store, ".state-#{System.pid()}.tmp")

    case File.open(temp, [:write, :binary]) do
      {:ok, file} ->
        result =
          with :ok <- IO.binwrite(file, encode_json(%{"jobs" => jobs})),
               :ok <- :file.sync(file),
               :ok <- File.close(file),
               :ok <- File.rename(temp, path),
               {_output, 0} <- System.cmd("sync", ["-f", store]) do
            :ok
          else
            error ->
              File.close(file)
              {:store_error, error}
          end

        result

      error ->
        {:store_error, error}
    end
  end
end
