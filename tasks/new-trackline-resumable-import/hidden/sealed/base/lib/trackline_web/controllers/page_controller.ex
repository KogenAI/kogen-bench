defmodule TracklineWeb.PageController do
  use TracklineWeb, :controller

  def home(conn, _params) do
    render(conn, :home)
  end
end
