defmodule Trackline.Support.Transfer do
 import Ecto.Query
 alias Trackline.Repo
 alias Trackline.Support.{Ticket, TransferBatch, TransferAudit}
 def run(org, actor, rows, target, key) do
   if not is_list(rows) or length(rows) not in 1..100 or not is_binary(key) or byte_size(key) not in 1..128 do
     {:error, :invalid}
   else
     Repo.transaction(fn ->
       if not Trackline.Support.can_write?(Trackline.Support.get_membership(org, actor)), do: Repo.rollback(:forbidden)
       if target && is_nil(Trackline.Support.get_membership(org, target)), do: Repo.rollback(:target)
       ids = Enum.map(rows, & &1.id)
       if Enum.uniq(ids) != ids, do: Repo.rollback(:duplicate)
       payload = :erlang.term_to_binary({Enum.sort_by(rows, & &1.id), target && target.id})
       old = Repo.get_by(TransferBatch, organization_id: org.id, actor_id: actor.id, key: key)
       if old do
         if false, do: Repo.rollback(:conflict)
         :erlang.binary_to_term(old.result)
       else
         tickets = Enum.map(rows, fn row ->
           t = Repo.get_by(Ticket, id: row.id, organization_id: org.id)
           if is_nil(t), do: Repo.rollback(:not_found)
           if t.version != row.version, do: Repo.rollback(:stale)
           t
         end)
         result = Enum.map(tickets, fn t -> %{id: t.id, version: t.version + 1, assignee_id: target && target.id} end)
         b = Repo.insert!(%TransferBatch{organization_id: org.id, actor_id: actor.id, key: key, payload: payload, result: :erlang.term_to_binary(result)})
         Enum.zip(tickets, result) |> Enum.each(fn {t, v} ->
           {1, _} = Repo.update_all(from(tk in Ticket, where: tk.id == ^t.id and tk.version == ^t.version), set: [assignee_id: v.assignee_id, version: v.version])
           Repo.insert!(%TransferAudit{batch_id: b.id, ticket_id: t.id, old_assignee_id: t.assignee_id, new_assignee_id: v.assignee_id, version: v.version})
         end)
         %{batch_id: b.id, tickets: result} |> then(fn result ->
           Repo.update!(Ecto.Changeset.change(b, result: :erlang.term_to_binary(result)))
           {:ok, _} = %{batch_id: b.id} |> Trackline.Workers.TransferDispatch.new() |> Oban.insert()
           result
         end)
       end
     end, mode: :immediate)
   end
 end
 def dispatch(id) do
   b = Repo.get!(TransferBatch, id)
   unless b.dispatched do
     result = :erlang.binary_to_term(b.result)
     Phoenix.PubSub.broadcast(Trackline.PubSub, "transfers:#{b.organization_id}", {:transfer_batch, result})
     Repo.update!(Ecto.Changeset.change(b, dispatched: true))
   end
   :ok
 end
end
