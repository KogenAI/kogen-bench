defmodule Beltway.Retry do
  @moduledoc """
  Retries a function that returns `{:ok, value}` or `{:error, reason}`.
  """

  @doc """
  Calls `fun` up to `max_attempts` times, sleeping `delay_ms` between attempts.
  Exceptions and `:error` count as failures. Returns `{:ok, value}` or `{:error, reason}`
  for the last failure.
  """
  @spec run((-> term()), pos_integer(), non_neg_integer()) :: {:ok, term()} | {:error, term()}
  def run(fun, max_attempts, delay_ms)
      when is_function(fun, 0) and is_integer(max_attempts) and max_attempts >= 1 do
    attempt(fun, 1, max_attempts, delay_ms)
  end

  defp attempt(fun, n, max, delay) do
    case safe_call(fun) do
      {:ok, _} = ok ->
        ok

      {:error, reason} when n >= max ->
        {:error, reason}

      {:error, _} ->
        Process.sleep(delay)
        attempt(fun, n + 1, max, delay)
    end
  end

  defp safe_call(fun) do
    case fun.() do
      {:ok, _} = ok -> ok
      {:error, _} = error -> error
      :error -> {:error, :error}
      other -> {:error, {:unexpected, other}}
    end
  rescue
    exception -> {:error, {:exception, exception}}
  end
end
