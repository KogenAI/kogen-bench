defmodule TracklineWeb.ImportController do
 use TracklineWeb, :controller
 def create(conn, %{"slug" => slug, "file" => %Plug.Upload{path: path}, "key" => key}) do
   org = Trackline.Support.get_organization_by_slug!(slug)
   case Trackline.Support.start_import(org,conn.assigns.current_scope.user,path,key) do
     {:ok,s} -> json(conn,%{id: s.id, cursor: s.cursor, status: s.status})
     {:error, e} -> conn |> put_status(422) |> json(%{error: to_string(e)})
   end
 end
end
