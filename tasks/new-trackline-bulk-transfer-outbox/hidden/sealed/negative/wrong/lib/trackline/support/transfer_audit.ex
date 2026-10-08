defmodule Trackline.Support.TransferAudit do
 use Ecto.Schema
 schema "transfer_audits" do
   field :batch_id, :integer
   field :ticket_id, :integer
   field :old_assignee_id, :integer
   field :new_assignee_id, :integer
   field :version, :integer
 end
end
