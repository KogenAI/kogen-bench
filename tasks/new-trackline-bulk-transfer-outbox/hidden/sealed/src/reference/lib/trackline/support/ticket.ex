defmodule Trackline.Support.Ticket do
  use Ecto.Schema
  import Ecto.Changeset

  @statuses ~w(open pending closed)
  @priorities ~w(low normal high urgent)

  schema "tickets" do
    field :version, :integer, default: 0
    field :title, :string
    field :body, :string
    field :status, :string, default: "open"
    field :priority, :string, default: "normal"
    field :comment_count, :integer, virtual: true, default: 0

    belongs_to :organization, Trackline.Support.Organization
    belongs_to :author, Trackline.Accounts.User
    belongs_to :assignee, Trackline.Accounts.User
    has_many :comments, Trackline.Support.Comment

    timestamps(type: :utc_datetime)
  end

  def statuses, do: @statuses
  def priorities, do: @priorities

  def changeset(ticket, attrs) do
    ticket
    |> cast(attrs, [:title, :body, :priority])
    |> validate_required([:title])
    |> validate_length(:title, max: 200)
    |> validate_inclusion(:priority, @priorities)
  end

  def status_changeset(ticket, status) do
    ticket
    |> change(status: status)
    |> validate_inclusion(:status, @statuses)
  end
end
