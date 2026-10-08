defmodule Trackline.Repo.Migrations.BulkBatches do
  use Ecto.Migration
  def change do
    alter table(:tickets), do: add(:version, :integer, default: 0, null: false)
    create table(:transfer_batches) do
      add :organization_id, references(:organizations), null: false
      add :actor_id, references(:users), null: false
      add :key, :string, null: false
      add :payload, :binary, null: false
      add :result, :binary, null: false
      add :dispatched, :boolean, default: false, null: false
    end
    create unique_index(:transfer_batches, [:organization_id, :actor_id, :key])
    create table(:transfer_audits) do
      add :batch_id, references(:transfer_batches), null: false
      add :ticket_id, references(:tickets), null: false
      add :old_assignee_id, :integer
      add :new_assignee_id, :integer
      add :version, :integer, null: false
    end
  end
end
