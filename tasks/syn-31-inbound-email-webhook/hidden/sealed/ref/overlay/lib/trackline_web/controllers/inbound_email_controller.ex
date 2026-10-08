defmodule TracklineWeb.InboundEmailController do
  use TracklineWeb, :controller

  alias Trackline.{Inbound, Support}

  @window_seconds 300

  def create(conn, %{"slug" => slug} = params) do
    case Support.get_organization_by_slug(slug) do
      nil ->
        conn |> put_status(:not_found) |> json(%{error: "not_found"})

      org ->
        if authentic?(conn, org), do: ingest(conn, org, params), else: unauthorized(conn)
    end
  end

  defp ingest(conn, org, params) do
    case Inbound.ingest(org, params) do
      {:ok, {:created, ticket_id}} ->
        conn |> put_status(:created) |> json(%{ticket_id: ticket_id})

      {:ok, {:duplicate, ticket_id}} ->
        json(conn, %{ticket_id: ticket_id, duplicate: true})

      {:error, _} ->
        conn |> put_status(:unprocessable_entity) |> json(%{error: "invalid"})
    end
  end

  defp unauthorized(conn), do: conn |> put_status(:unauthorized) |> json(%{error: "unauthorized"})

  defp authentic?(_conn, %{webhook_secret: secret}) when secret in [nil, ""], do: false

  defp authentic?(conn, %{webhook_secret: secret}) do
    with [ts] <- get_req_header(conn, "x-webhook-timestamp"),
         [signature] <- get_req_header(conn, "x-webhook-signature"),
         {seconds, ""} <- Integer.parse(ts),
         true <- abs(System.os_time(:second) - seconds) <= @window_seconds do
      body = conn.assigns[:raw_body] || ""

      expected =
        :hmac |> :crypto.mac(:sha256, secret, [ts, ".", body]) |> Base.encode16(case: :lower)

      Plug.Crypto.secure_compare(expected, signature)
    else
      _ -> false
    end
  end
end
