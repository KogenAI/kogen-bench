defmodule Trackline.Workers.TicketImport do
 use Oban.Worker, queue: :default
 def perform(%Oban.Job{args: %{"session_id" => id}}) do
   case Trackline.Support.Imports.claim(id) do
     {:ok, s} -> loop(s)
     {:error, :leased} -> {:snooze, 30}
     {:error, :stopped} -> :ok
   end
 end
 defp loop(s) do
   case Trackline.Support.Imports.batch(s.id,s.lease) do
     {:ok, %{status: "running"}=next} -> loop(next)
     {:ok, _} -> :ok
     {:error, :stale} -> {:snooze, 30}
   end
 end
end
