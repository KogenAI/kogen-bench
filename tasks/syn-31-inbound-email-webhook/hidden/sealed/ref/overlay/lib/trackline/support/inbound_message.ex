defmodule Trackline.Support.InboundMessage do
  use Ecto.Schema

  schema "inbound_messages" do
    field :message_id, :string

    belongs_to :organization, Trackline.Support.Organization
    belongs_to :ticket, Trackline.Support.Ticket

    timestamps(type: :utc_datetime, updated_at: false)
  end
end
