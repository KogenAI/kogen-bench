defmodule Trackline.Repo.Migrations.AddExternalIdToTickets do
  use Ecto.Migration

  def change do
    alter table(:tickets) do
      add :external_id, :string
    end

    create unique_index(:tickets, [:organization_id, :external_id])
  end
end
