defmodule Trackline.Repo.Migrations.AddArchivedAtToTickets do
  use Ecto.Migration

  def change do
    alter table(:tickets) do
      add :archived_at, :utc_datetime
    end
  end
end
