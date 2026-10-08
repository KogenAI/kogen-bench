defmodule TracklineWeb.TicketImportController do
  use TracklineWeb, :controller

  alias Trackline.Support

  def create(conn, %{"slug" => slug} = params) do
    user = conn.assigns.current_scope.user

    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = membership <- Support.get_membership(org, user),
         true <- Support.can_write?(membership) do
      case params["file"] do
        %Plug.Upload{path: path} ->
          case Support.import_tickets(org, user, File.read!(path)) do
            {:ok, report} -> json(conn, report)
            {:error, reason} -> conn |> put_status(:unprocessable_entity) |> json(%{error: "unreadable file: #{inspect(reason)}"})
          end

        _ ->
          conn |> put_status(:unprocessable_entity) |> json(%{error: "no file uploaded"})
      end
    else
      _ -> conn |> put_status(:forbidden) |> json(%{error: "forbidden"})
    end
  end
end
