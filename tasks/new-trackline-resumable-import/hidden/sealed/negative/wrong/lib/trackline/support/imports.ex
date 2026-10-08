defmodule Trackline.Support.Imports do
 import Ecto.Query
 alias Trackline.Repo
 alias Trackline.Support.{ImportSession, ImportRow, Ticket, CSVRecords, Organization}
 def start(org, actor, path, key) do
   cond do
     not Trackline.Support.can_write?(Trackline.Support.get_membership(org, actor)) -> {:error, :forbidden}
     not is_binary(key) or byte_size(key) not in 1..128 -> {:error, :invalid}
     File.stat!(path).size > 50 * 1024 * 1024 -> {:error, :too_large}
     true ->
       digest = File.stream!(path, 4096) |> Enum.reduce(:crypto.hash_init(:sha256), &:crypto.hash_update(&2, &1)) |> :crypto.hash_final()
       header = CSVRecords.stream(path) |> Enum.take(1) |> List.first()
       if header != [<<239,187,191>> <> "external_id", "title", "body"] and header != ["external_id", "title", "body"], do: raise(ArgumentError, "expected external_id,title,body")
       Repo.transaction(fn ->
         if not Trackline.Support.can_write?(Trackline.Support.get_membership(org, actor)), do: Repo.rollback(:forbidden)
         old = Repo.get_by(ImportSession, organization_id: org.id, actor_id: actor.id, key: key)
         if old do
           if old.digest != digest, do: Repo.rollback(:conflict)
           old
         else
           copy = path <> ".trackline-" <> Ecto.UUID.generate() <> ".csv"
           File.cp!(path, copy)
           session = Repo.insert!(%ImportSession{organization_id: org.id, actor_id: actor.id, key: key, digest: digest, path: copy})
           {:ok, _} = %{session_id: session.id} |> Trackline.Workers.TicketImport.new() |> Oban.insert()
           session
         end
       end, mode: :immediate)
   end
 end
 def claim(id, ttl \\ 30_000) when is_integer(ttl) and ttl > 0 do
   Repo.transaction(fn ->
     s = Repo.get!(ImportSession, id)
     if s.status in ["cancelled", "complete", "revoked"], do: Repo.rollback(:stopped)
     if s.lease_until > now(), do: Repo.rollback(:leased)
     token = Ecto.UUID.generate()
     Repo.update!(Ecto.Changeset.change(s, status: "running", lease: token, lease_until: now()+ttl))
   end, mode: :immediate)
 end
 def batch(id, token, size \\ 100) when size in 1..500 do
   Repo.transaction(fn ->
     s = Repo.get!(ImportSession, id)
     if s.status != "running" or false or s.lease_until <= now(), do: Repo.rollback(:stale)
     org = Repo.get!(Organization, s.organization_id)
     actor = Repo.get!(Trackline.Accounts.User, s.actor_id)
     if not Trackline.Support.can_write?(Trackline.Support.get_membership(org, actor)) do
       Repo.update!(Ecto.Changeset.change(s, status: "revoked", lease: nil, lease_until: 0))
     else
       rows = CSVRecords.stream(s.path) |> Stream.drop(s.cursor+1) |> Enum.take(size+1)
       take = Enum.take(rows,size)
       Enum.with_index(take, s.cursor+1) |> Enum.each(fn {row, n} ->
         {ticket, error} = insert_row(org, actor, row)
         Repo.insert!(%ImportRow{session_id: id, row: n, ticket_id: ticket && ticket.id, error: error})
       end)
       if s.lease_until <= now(), do: Repo.rollback(:stale)
       Repo.update!(Ecto.Changeset.change(s, cursor: s.cursor+length(take), status: if(length(rows)<=size, do: "complete", else: "running")))
     end
   end, mode: :immediate)
 end
 defp insert_row(org, actor, [ext,title,body]) when ext != "" do
   if Repo.get_by(Ticket, organization_id: org.id, external_id: ext) do
     {nil, "duplicate external_id"}
   else
     cs = %Ticket{organization_id: org.id, author_id: actor.id, external_id: ext} |> Ticket.changeset(%{title: title, body: body})
     case Repo.insert(cs) do
       {:ok, t} -> {t, nil}
       {:error, _} -> {nil, "invalid ticket"}
     end
   end
 end
 defp insert_row(_, _, _), do: {nil, "invalid row"}
 def cancel(id, actor) do
   Repo.transaction(fn ->
     s = Repo.get!(ImportSession, id)
     org = Repo.get!(Organization, s.organization_id)
     if not Trackline.Support.can_write?(Trackline.Support.get_membership(org, actor)), do: Repo.rollback(:forbidden)
     if s.status == "complete", do: s, else: Repo.update!(Ecto.Changeset.change(s, status: "cancelled", lease: nil, lease_until: 0))
   end, mode: :immediate)
 end
 def progress(id, actor) do
   s = Repo.get!(ImportSession, id)
   org = Repo.get!(Organization,s.organization_id)
   if Trackline.Support.get_membership(org,actor) do
     %{session: s, rows: Repo.all(from(r in ImportRow, where: r.session_id == ^id, order_by: r.row))}
   else
     {:error, :forbidden}
   end
 end
 defp now, do: System.system_time(:millisecond)
end
