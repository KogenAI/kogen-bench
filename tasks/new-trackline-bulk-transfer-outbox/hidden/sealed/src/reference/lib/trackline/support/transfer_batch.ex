defmodule Trackline.Support.TransferBatch do
 use Ecto.Schema
 schema "transfer_batches" do
   field :organization_id, :integer
   field :actor_id, :integer
   field :key, :string
   field :payload, :binary
   field :result, :binary
   field :dispatched, :boolean, default: false
 end
end
