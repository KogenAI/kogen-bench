defmodule Trackline.Support.Organization do
  use Ecto.Schema
  import Ecto.Changeset

  schema "organizations" do
    field :name, :string
    field :slug, :string
    field :webhook_url, :string
    field :webhook_secret, :string

    has_many :memberships, Trackline.Support.Membership
    has_many :tickets, Trackline.Support.Ticket

    timestamps(type: :utc_datetime)
  end

  def changeset(organization, attrs) do
    organization
    |> cast(attrs, [:name, :slug, :webhook_url, :webhook_secret])
    |> validate_required([:name, :slug])
    |> validate_format(:slug, ~r/^[a-z0-9-]+$/)
    |> unique_constraint(:slug)
  end
end
