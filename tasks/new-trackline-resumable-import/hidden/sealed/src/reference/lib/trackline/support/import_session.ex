defmodule Trackline.Support.ImportSession do
 use Ecto.Schema
 schema "import_sessions" do
  field :organization_id, :integer
  field :actor_id, :integer
  field :key, :string
  field :digest, :binary
  field :path, :string
  field :cursor, :integer, default: 0
  field :status, :string, default: "pending"
  field :lease, :string
  field :lease_until, :integer, default: 0
 end
end
