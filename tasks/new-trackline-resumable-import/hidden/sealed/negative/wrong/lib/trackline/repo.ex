defmodule Trackline.Repo do
  use Ecto.Repo,
    otp_app: :trackline,
    adapter: Ecto.Adapters.SQLite3
end
