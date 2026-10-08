defmodule Trackline.Repo.Migrations.CreateInboundMessages do
  use Ecto.Migration

  def change do
    alter table(:tickets) do
      add :requester_email, :string
    end

    create table(:inbound_messages) do
      add :organization_id, references(:organizations, on_delete: :delete_all), null: false
      add :ticket_id, references(:tickets, on_delete: :delete_all), null: false
      add :message_id, :string, null: false

      timestamps(type: :utc_datetime, updated_at: false)
    end

    create unique_index(:inbound_messages, [:organization_id, :message_id])
  end
end
