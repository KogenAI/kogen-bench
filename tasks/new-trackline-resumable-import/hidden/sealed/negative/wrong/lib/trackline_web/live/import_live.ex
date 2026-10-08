defmodule TracklineWeb.ImportLive do
 use TracklineWeb, :live_view
 def mount(%{"slug" => slug, "id" => id}, _, socket) do
   org = Trackline.Support.get_organization_by_slug!(slug)
   progress = Trackline.Support.Imports.progress(String.to_integer(id), socket.assigns.current_scope.user)
   if is_map(progress) and progress.session.organization_id == org.id do
     if connected?(socket), do: Process.send_after(self(), :refresh, 500)
     {:ok, assign(socket, :progress, progress)}
   else
     {:ok, push_navigate(socket, to: ~p"/orgs")}
   end
 end
 def handle_info(:refresh, socket) do
   p = Trackline.Support.Imports.progress(socket.assigns.progress.session.id, socket.assigns.current_scope.user)
   if is_map(p) do
     Process.send_after(self(), :refresh, 500)
     {:noreply, assign(socket, :progress, p)}
   else
     {:noreply, push_navigate(socket, to: ~p"/orgs")}
   end
 end
 def handle_event("cancel", _, socket) do
   Trackline.Support.cancel_import(socket.assigns.progress.session, socket.assigns.current_scope.user)
   handle_info(:refresh,socket)
 end
 def render(assigns) do
   ~H"""
   <Layouts.app flash={@flash} current_scope={@current_scope}>
    <div id="import-progress" data-cursor={@progress.session.cursor} data-status={@progress.session.status}>
     <button id="cancel-import" phx-click="cancel">Cancel</button>
     <ol id="import-errors"><li :for={r <- @progress.rows} :if={r.error} id={"row-#{r.row}"}>{r.row}: {r.error}</li></ol>
    </div>
   </Layouts.app>
   """
 end
end
