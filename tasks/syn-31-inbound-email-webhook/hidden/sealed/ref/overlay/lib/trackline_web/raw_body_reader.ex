defmodule TracklineWeb.RawBodyReader do
  @moduledoc """
  Body reader for `Plug.Parsers` that keeps the exact bytes of inbound-email
  requests (needed to verify signatures) and caps their size.
  """

  @limit 65_536

  def read_body(%Plug.Conn{request_path: "/api/orgs/" <> _} = conn, opts) do
    if String.ends_with?(conn.request_path, "/inbound-email") do
      case Plug.Conn.read_body(conn, Keyword.put(opts, :length, @limit)) do
        {:ok, body, conn} -> {:ok, body, Plug.Conn.assign(conn, :raw_body, body)}
        other -> other
      end
    else
      Plug.Conn.read_body(conn, opts)
    end
  end

  def read_body(conn, opts), do: Plug.Conn.read_body(conn, opts)
end
