defmodule Beltway.Ingest.Supervisor do
  @moduledoc """
  Starts the ingest pipeline: `Buffer`, `Parser` and `Sink` (child ids are the module
  names). Takes `collector: pid` for the sink.
  """
  use Supervisor

  alias Beltway.Ingest.{Buffer, Parser, Sink}

  def start_link(opts), do: Supervisor.start_link(__MODULE__, opts)

  @impl true
  def init(opts) do
    children = [
      Buffer,
      Parser,
      {Sink, collector: Keyword.fetch!(opts, :collector)}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
