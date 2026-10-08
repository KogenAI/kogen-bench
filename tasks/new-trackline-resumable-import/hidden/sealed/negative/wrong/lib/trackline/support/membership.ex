defmodule Trackline.Support.Membership do
  use Ecto.Schema
  import Ecto.Changeset

  @roles ~w(owner agent viewer)

  schema "memberships" do
    field :role, :string, default: "viewer"

    belongs_to :organization, Trackline.Support.Organization
    belongs_to :user, Trackline.Accounts.User

    timestamps(type: :utc_datetime)
  end

  def roles, do: @roles

  def changeset(membership, attrs) do
    membership
    |> cast(attrs, [:role, :organization_id, :user_id])
    |> validate_required([:role, :organization_id, :user_id])
    |> validate_inclusion(:role, @roles)
    |> unique_constraint([:organization_id, :user_id])
  end
end
