defmodule Beltway.Fetcher do
  @moduledoc """
  Fetches a URL through an injected HTTP function, retrying transient failures.

  Options: `:http` (function taking the url and returning `{:ok, body}` or
  `{:error, reason}`) and `:retry_delay` (ms between attempts, default 100).
  """

  alias Beltway.Retry

  def fetch(url, opts) do
    http = Keyword.fetch!(opts, :http)
    delay = Keyword.get(opts, :retry_delay, 100)
    Retry.run(fn -> http.(url) end, 3, delay)
  end
end
