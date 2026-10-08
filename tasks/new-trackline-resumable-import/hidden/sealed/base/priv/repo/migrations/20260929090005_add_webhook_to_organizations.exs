defmodule Trackline.Repo.Migrations.AddWebhookToOrganizations do
  use Ecto.Migration

  def change do
    alter table(:organizations) do
      add :webhook_url, :string
      add :webhook_secret, :string
    end
  end
end
