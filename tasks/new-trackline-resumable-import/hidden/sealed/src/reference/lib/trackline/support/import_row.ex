defmodule Trackline.Support.ImportRow do
 use Ecto.Schema
 schema "import_rows" do
  field :session_id, :integer
  field :row, :integer
  field :error, :string
  field :ticket_id, :integer
 end
end
