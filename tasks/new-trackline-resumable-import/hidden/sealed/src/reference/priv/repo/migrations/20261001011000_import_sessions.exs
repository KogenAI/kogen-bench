defmodule Trackline.Repo.Migrations.ImportSessions do
 use Ecto.Migration
 def change do
   alter table(:tickets), do: add(:external_id, :string)
   create unique_index(:tickets, [:organization_id, :external_id])
   create table(:import_sessions) do
     add :organization_id, references(:organizations), null: false
     add :actor_id, references(:users), null: false
     add :key, :string, null: false
     add :digest, :binary, null: false
     add :path, :string, null: false
     add :cursor, :integer, default: 0, null: false
     add :status, :string, default: "pending", null: false
     add :lease, :string
     add :lease_until, :bigint, default: 0
   end
   create unique_index(:import_sessions, [:organization_id, :actor_id, :key])
   create table(:import_rows) do
     add :session_id, references(:import_sessions), null: false
     add :row, :integer, null: false
     add :error, :string
     add :ticket_id, references(:tickets)
   end
   create unique_index(:import_rows, [:session_id, :row])
 end
end
