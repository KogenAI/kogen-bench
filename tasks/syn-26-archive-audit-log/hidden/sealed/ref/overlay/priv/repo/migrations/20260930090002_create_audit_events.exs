defmodule Trackline.Repo.Migrations.CreateAuditEvents do
  use Ecto.Migration

  def change do
    create table(:audit_events) do
      add :organization_id, references(:organizations, on_delete: :delete_all), null: false
      add :ticket_id, references(:tickets, on_delete: :delete_all)
      add :actor_id, references(:users, on_delete: :nilify_all)
      add :action, :string, null: false

      timestamps(type: :utc_datetime, updated_at: false)
    end

    create index(:audit_events, [:organization_id])
    create index(:audit_events, [:ticket_id])
  end
end
