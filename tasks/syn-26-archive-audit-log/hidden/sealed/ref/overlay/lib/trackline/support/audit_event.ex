defmodule Trackline.Support.AuditEvent do
  use Ecto.Schema

  @actions ~w(ticket_created status_changed assigned comment_added archived restored)

  schema "audit_events" do
    field :action, :string

    belongs_to :organization, Trackline.Support.Organization
    belongs_to :ticket, Trackline.Support.Ticket
    belongs_to :actor, Trackline.Accounts.User

    timestamps(type: :utc_datetime, updated_at: false)
  end

  def actions, do: @actions
end
