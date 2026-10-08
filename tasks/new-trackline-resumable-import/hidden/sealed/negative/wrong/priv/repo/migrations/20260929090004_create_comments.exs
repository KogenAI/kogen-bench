defmodule Trackline.Repo.Migrations.CreateComments do
  use Ecto.Migration

  def change do
    create table(:comments) do
      add :ticket_id, references(:tickets, on_delete: :delete_all), null: false
      add :author_id, references(:users, on_delete: :nilify_all)
      add :body, :text, null: false

      timestamps(type: :utc_datetime)
    end

    create index(:comments, [:ticket_id])
  end
end
