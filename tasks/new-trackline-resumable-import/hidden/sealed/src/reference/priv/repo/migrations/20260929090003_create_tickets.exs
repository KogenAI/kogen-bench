defmodule Trackline.Repo.Migrations.CreateTickets do
  use Ecto.Migration

  def change do
    create table(:tickets) do
      add :organization_id, references(:organizations, on_delete: :delete_all), null: false
      add :author_id, references(:users, on_delete: :nilify_all)
      add :assignee_id, references(:users, on_delete: :nilify_all)
      add :title, :string, null: false
      add :body, :text
      add :status, :string, null: false, default: "open"
      add :priority, :string, null: false, default: "normal"

      timestamps(type: :utc_datetime)
    end

    create index(:tickets, [:organization_id, :status])
    create index(:tickets, [:assignee_id])
  end
end
