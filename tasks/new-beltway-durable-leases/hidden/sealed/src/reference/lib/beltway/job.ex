defmodule Beltway.Job do
  @moduledoc """
  Runs a named job function with retries.

  `fun` returns `{:ok, value}` or `{:error, reason}`; a raised exception counts as
  `{:error, {:raised, exception}}`. Options: `:max_attempts` (default 1), `:backoff_ms`
  (linear: sleeps `backoff_ms * attempt` after a failed attempt, default 0), `:sleep`
  (function taking ms, default `Process.sleep/1`) and `:metadata` (a map, currently unused).
  """

  @spec run(term(), (-> {:ok, term()} | {:error, term()}), keyword()) ::
          {:ok, term()} | {:error, term()}
  def run(name, fun, opts \\ []) when is_function(fun, 0) do
    max = Keyword.get(opts, :max_attempts, 1)
    sleep = Keyword.get(opts, :sleep, &Process.sleep/1)
    backoff = Keyword.get(opts, :backoff_ms, 0)
    attempt(name, fun, 1, max, sleep, backoff)
  end

  defp attempt(name, fun, n, max, sleep, backoff) do
    case call(fun) do
      {:ok, _} = ok ->
        ok

      {:error, _} = error when n >= max ->
        error

      {:error, _reason} ->
        sleep.(backoff * n)
        attempt(name, fun, n + 1, max, sleep, backoff)
    end
  end

  defp call(fun) do
    case fun.() do
      {:ok, _} = ok -> ok
      {:error, _} = error -> error
      other -> {:error, {:unexpected, other}}
    end
  rescue
    exception -> {:error, {:raised, exception}}
  end
end
