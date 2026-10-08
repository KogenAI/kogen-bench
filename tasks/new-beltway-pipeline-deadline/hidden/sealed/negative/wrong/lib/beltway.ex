defmodule Beltway do
  @moduledoc """
  Pipeline building blocks. See the individual modules.
  """
  def run_pipeline(items,command,opts), do: Beltway.Pipeline.run(items,command,opts)
end
