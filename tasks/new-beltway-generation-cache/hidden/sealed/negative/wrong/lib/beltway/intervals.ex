defmodule Beltway.Intervals do
  @moduledoc """
  Closed integer intervals `{first, last}` with `first <= last`, as used by the scheduler
  to compute busy time.
  """

  @type interval :: {integer(), integer()}

  @doc """
  Merges overlapping intervals and intervals that share an endpoint. The result is sorted
  by start and pairwise disjoint.
  """
  @spec merge([interval()]) :: [interval()]
  def merge(intervals) do
    intervals
    |> Enum.sort()
    |> Enum.reduce([], fn
      {s, e}, [{ps, pe} | rest] when s <= pe -> [{ps, max(pe, e)} | rest]
      interval, acc -> [interval | acc]
    end)
    |> Enum.reverse()
  end

  @doc "True when `x` lies in any interval (both ends included)."
  @spec contains?([interval()], integer()) :: boolean()
  def contains?(intervals, x), do: Enum.any?(intervals, fn {s, e} -> s <= x and x <= e end)

  @doc "Total length covered (`last - first` per merged interval)."
  @spec covered_length([interval()]) :: non_neg_integer()
  def covered_length(intervals) do
    intervals |> merge() |> Enum.reduce(0, fn {s, e}, acc -> acc + (e - s) end)
  end

  @doc "Intersection of two interval lists, merged."
  @spec intersect([interval()], [interval()]) :: [interval()]
  def intersect(a, b) do
    for {s1, e1} <- merge(a),
        {s2, e2} <- merge(b),
        lo = max(s1, s2),
        hi = min(e1, e2),
        lo <= hi do
      {lo, hi}
    end
    |> merge()
  end
end
