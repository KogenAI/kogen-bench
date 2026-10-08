defmodule Trackline.Repo.Migrations.AddTicketNumbers do
  use Ecto.Migration

  def up do
    alter table(:tickets) do
      add :number, :integer
    end

    # Oldest first; ties broken by id.
    execute """
    UPDATE tickets SET number = (
      SELECT COUNT(*) FROM tickets t2
      WHERE t2.organization_id = tickets.organization_id
        AND (t2.inserted_at < tickets.inserted_at
             OR (t2.inserted_at = tickets.inserted_at AND t2.id <= tickets.id))
    )
    """

    create unique_index(:tickets, [:organization_id, :number])
  end

  def down do
    # SQLite refuses to drop an indexed column, so drop the index first.
    drop unique_index(:tickets, [:organization_id, :number])

    alter table(:tickets) do
      remove :number
    end
  end
end
