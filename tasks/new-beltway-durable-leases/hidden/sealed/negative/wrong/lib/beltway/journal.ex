defmodule Beltway.Journal do
  @moduledoc "Synced CRC-framed state journal. A partial suffix is discarded on open."
  def open(path) do
    path = Path.expand(path)
    File.mkdir_p!(Path.dirname(path))
    lock = path <> ".lock"
    case File.mkdir(lock) do
      :ok -> :ok
      {:error, :eexist} ->
        live = case File.read(Path.join(lock, "owner")) do
          {:ok, bytes} ->
            try do
              {os, pid} = :erlang.binary_to_term(bytes)
              if os == System.pid(), do: Process.alive?(pid), else: elem(System.cmd("/bin/kill", ["-0", os], stderr_to_stdout: true), 1) == 0
            rescue
              _ -> true
            end
          _ -> true
        end
        if live, do: throw(:already_open)
        File.rm_rf!(lock)
        :ok = File.mkdir(lock)
      {:error, reason} -> throw(reason)
    end
    File.write!(Path.join(lock, "owner"), :erlang.term_to_binary({System.pid(), self()}))
    try do
      bytes = case File.read(path) do
        {:ok, b} -> b
        {:error, :enoent} -> <<>>
        {:error, e} -> throw(e)
      end
      {state, valid} = recover(bytes, nil, 0)
      {:ok, fd} = :file.open(String.to_charlist(path), [:raw, :binary, :read, :write])
      {:ok, _} = :file.position(fd, valid)
      :ok = :file.truncate(fd)
      {:ok, {fd, lock}, state}
    catch
      reason -> File.rm_rf!(lock); {:error, reason}
    end
  catch
    reason -> {:error, reason}
  end
  defp recover(<<n::32, crc::32, rest::binary>>, last, pos) when byte_size(rest) >= n do
    <<data::binary-size(n), tail::binary>> = rest
    if :erlang.crc32(data) != crc, do: throw(:corrupt)
    state = try do :erlang.binary_to_term(data, [:safe]) rescue _ -> throw(:corrupt) end
    recover(tail, state, pos + n + 8)
  end
  defp recover(_, last, pos), do: {last, pos}
  def append({fd, _}, state) do
    bytes = :erlang.term_to_binary(state)
    :ok = :file.write(fd, <<byte_size(bytes)::32, :erlang.crc32(bytes)::32, bytes::binary>>)
    :file.sync(fd)
  end
  def close({fd, lock}) do
    :file.close(fd)
    File.rm_rf!(lock)
  end
end
