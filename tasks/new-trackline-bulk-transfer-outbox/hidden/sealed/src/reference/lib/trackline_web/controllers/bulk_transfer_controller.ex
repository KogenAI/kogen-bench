defmodule TracklineWeb.BulkTransferController do
 use TracklineWeb, :controller
 def create(conn, params) do
   org = Trackline.Support.get_organization_by_slug!(params["slug"])
   rows = Enum.map(params["rows"], &%{id: &1["id"], version: &1["version"]})
   target = if params["target_id"], do: Trackline.Repo.get!(Trackline.Accounts.User, params["target_id"])
   case Trackline.Support.bulk_reassign(org, conn.assigns.current_scope.user, rows, target, params["key"]) do
     {:ok, result} -> json(conn, result)
     {:error, reason} -> conn |> put_status(422) |> json(%{error: to_string(reason)})
   end
 end
end
