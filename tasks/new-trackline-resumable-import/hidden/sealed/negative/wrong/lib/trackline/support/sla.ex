defmodule Trackline.Support.SLA do
  @moduledoc """
  Response-time targets for tickets.

  * `urgent` tickets must be handled within 60 wall-clock minutes.
  * `high`, `normal` and `low` tickets are measured in *business* minutes:
    Monday to Friday, 09:00 to 17:00 UTC. Time outside those hours does not
    count. `high` gets 4 business hours, `normal` 8 and `low` 24.
  """

  @business_start ~T[09:00:00]
  @business_end ~T[17:00:00]
  @day_minutes 8 * 60
  @at_risk_ratio 0.75

  @targets %{
    "urgent" => {:clock, 60},
    "high" => {:business, 4 * 60},
    "normal" => {:business, 8 * 60},
    "low" => {:business, 24 * 60}
  }

  @doc "Target in minutes for a priority. Unknown priorities are treated as `normal`."
  def target_minutes(priority) do
    {_kind, minutes} = Map.get(@targets, priority, @targets["normal"])
    minutes
  end

  @doc "When a ticket created at `created_at` with `priority` is due."
  def due_at(priority, %DateTime{} = created_at) do
    case Map.get(@targets, priority, @targets["normal"]) do
      {:clock, minutes} -> DateTime.add(created_at, minutes * 60, :second)
      {:business, minutes} -> add_business_minutes(created_at, minutes)
    end
  end

  @doc """
  The SLA state of a ticket at `now`.

  * closed tickets are `:met`
  * pending tickets (waiting on the customer) are `:paused`
  * otherwise `:breached` once `now` is past the due time, `:at_risk` once 75%
    or more of the target has been used, and `:ok` before that.
  """
  def state(status, priority, %DateTime{} = created_at, %DateTime{} = now) do
    case status do
      "closed" -> :met
      "pending" -> :paused
      _ -> open_state(priority, created_at, now)
    end
  end

  defp open_state(priority, created_at, now) do
    due = due_at(priority, created_at)
    kind = priority_kind(priority)

    cond do
      DateTime.compare(now, due) == :gt ->
        :breached

      elapsed_minutes(kind, created_at, now) / target_minutes(priority) >= @at_risk_ratio ->
        :at_risk

      true ->
        :ok
    end
  end

  defp priority_kind(priority) do
    {kind, _minutes} = Map.get(@targets, priority, @targets["normal"])
    kind
  end

  defp elapsed_minutes(:clock, from, to), do: DateTime.diff(to, from, :second) / 60
  defp elapsed_minutes(:business, from, to), do: business_minutes_between(from, to)

  @doc false
  def add_business_minutes(%DateTime{} = start, minutes) do
    start |> normalize() |> consume(minutes)
  end

  defp consume(dt, minutes) do
    left_today = DateTime.diff(day_close(dt), dt, :second) / 60

    if minutes <= left_today do
      DateTime.add(dt, round(minutes * 60), :second)
    else
      dt |> next_business_open() |> consume(minutes - left_today)
    end
  end

  @doc false
  def business_minutes_between(from, to) do
    if DateTime.compare(to, from) != :gt do
      0.0
    else
      from |> normalize() |> accumulate(to, 0.0)
    end
  end

  defp accumulate(dt, to, acc) do
    close = day_close(dt)

    if DateTime.compare(to, close) != :gt do
      if DateTime.compare(to, dt) == :gt, do: acc + DateTime.diff(to, dt, :second) / 60, else: acc
    else
      dt |> next_business_open() |> accumulate(to, acc + DateTime.diff(close, dt, :second) / 60)
    end
  end

  # Move a timestamp into business hours (start of the next window if outside).
  defp normalize(dt) do
    date = DateTime.to_date(dt)
    time = DateTime.to_time(dt)

    cond do
      not business_day?(date) -> next_business_open(dt)
      Time.compare(time, @business_start) == :lt -> at(date, @business_start)
      Time.compare(time, @business_end) != :lt -> next_business_open(dt)
      true -> dt
    end
  end

  defp next_business_open(dt) do
    dt |> DateTime.to_date() |> Date.add(1) |> skip_weekend() |> at(@business_start)
  end

  defp skip_weekend(date),
    do: if(business_day?(date), do: date, else: skip_weekend(Date.add(date, 1)))

  defp business_day?(date), do: Date.day_of_week(date) <= 5

  defp day_close(dt), do: at(DateTime.to_date(dt), @business_end)

  defp at(date, time), do: DateTime.new!(date, time, "Etc/UTC")

  @doc false
  def day_minutes, do: @day_minutes
end
