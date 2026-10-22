defmodule Kogen.Core do
  @moduledoc "UTC cron occurrence finder."

  @help """
  Usage: kogen-cron [--after YYYY-MM-DDTHH:MM] [--count N] [--format text|json] [FILE|-]
  Find upcoming UTC minutes for named cron expressions.
  Options:
    --after VALUE    Exclusive UTC starting minute (default 2000-01-01T00:00).
    --count N        Occurrences per expression (default 3; range 1..20).
    --format FORMAT  Output text (default) or json.
    --help           Show this help.
  """

  @epoch ~N[1970-01-01 00:00:00]
  @search_minutes 8 * 366 * 24 * 60

  def execute(["--help"]), do: @help

  def execute(args) do
    options = parse_args(args)
    data = Kogen.Input.read(options.path, "cron")

    if byte_size(data) > 1_048_576 do
      Kogen.Input.fail("cron: input too large")
    end

    schedules = parse_schedules(data)
    check_duplicate_names!(schedules)

    runs =
      Enum.map(schedules, fn schedule ->
        result = find_runs(schedule, options.after, options.count)

        if length(result) != options.count do
          fail_source(schedule.line, 1, "not enough occurrences in search horizon")
        end

        result
      end)

    render_schedules(schedules, runs, options.format)
  end

  defp parse_args(args) do
    options = %{after: default_after(), count: 3, format: "text", path: nil}
    parse_args(args, options, MapSet.new())
  end

  defp parse_args([], options, _seen), do: options

  defp parse_args(["--help" | _], _options, _seen),
    do: Kogen.Input.fail("cron: unknown option '--help'", 2)

  defp parse_args([option | rest], options, seen)
       when option in ["--after", "--count", "--format"] do
    if MapSet.member?(seen, option) do
      Kogen.Input.fail("cron: duplicate option '#{option}'", 2)
    end

    if rest == [] do
      Kogen.Input.fail("cron: option '#{option}' requires a value", 2)
    end

    [value | tail] = rest

    next_options =
      case option do
        "--after" ->
          case parse_timestamp(value) do
            {:ok, minute} -> %{options | after: minute}
            :error -> Kogen.Input.fail("cron: invalid value for '--after': '#{value}'", 2)
          end

        "--count" ->
          unless decimal_digits?(value) do
            Kogen.Input.fail("cron: invalid value for '--count': '#{value}'", 2)
          end

          count = String.to_integer(value)

          if count < 1 or count > 20 do
            Kogen.Input.fail("cron: value out of range for '--count': '#{value}'", 2)
          end

          %{options | count: count}

        "--format" ->
          if value not in ["text", "json"] do
            Kogen.Input.fail("cron: invalid value for '--format': '#{value}'", 2)
          end

          %{options | format: value}
      end

    parse_args(tail, next_options, MapSet.put(seen, option))
  end

  defp parse_args([token | rest], options, seen) do
    cond do
      String.starts_with?(token, "-") and token != "-" ->
        Kogen.Input.fail("cron: unknown option '#{token}'", 2)

      is_nil(options.path) ->
        parse_args(rest, %{options | path: token}, seen)

      true ->
        Kogen.Input.fail("cron: expected at most one input path", 2)
    end
  end

  defp decimal_digits?(value) when byte_size(value) > 0 do
    value |> :binary.bin_to_list() |> Enum.all?(&(&1 >= ?0 and &1 <= ?9))
  end

  defp decimal_digits?(_value), do: false

  defp default_after do
    {:ok, minute} = parse_timestamp("2000-01-01T00:00")
    minute
  end

  defp parse_timestamp(value) do
    case Regex.run(~r/\A([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2})\z/, value) do
      [_, year, month, day, hour, minute] ->
        {year, _} = Integer.parse(year)
        {month, _} = Integer.parse(month)
        {day, _} = Integer.parse(day)
        {hour, _} = Integer.parse(hour)
        {minute, _} = Integer.parse(minute)

        with true <- year >= 1970 and year <= 2190,
             {:ok, date} <- Date.new(year, month, day),
             {:ok, time} <- Time.new(hour, minute, 0),
             {:ok, naive} <- NaiveDateTime.new(date, time) do
          {:ok, NaiveDateTime.diff(naive, @epoch, :minute)}
        else
          _ -> :error
        end

      _ ->
        :error
    end
  end

  defp parse_schedules(data) do
    lines = Kogen.Input.physical_lines(data)
    validate_ascii!(lines)

    lines
    |> Enum.with_index(1)
    |> Enum.reduce({[], 0}, fn {line, line_no}, {schedules, records} ->
      case parse_schedule_line(line, line_no, records) do
        :ignored -> {schedules, records}
        {:ok, schedule} -> {[schedule | schedules], records + 1}
      end
    end)
    |> elem(0)
    |> Enum.reverse()
  end

  defp validate_ascii!(lines) do
    Enum.with_index(lines, 1)
    |> Enum.each(fn {line, line_no} ->
      case line |> :binary.bin_to_list() |> Enum.find_index(&(&1 >= 128)) do
        nil -> :ok
        index -> fail_source(line_no, index + 1, "expected ASCII")
      end
    end)
  end

  defp parse_schedule_line(line, line_no, records) do
    first = first_non_space_or_tab(line)

    if is_nil(first) or :binary.at(line, first) == ?# do
      :ignored
    else
      if records >= 1000 do
        fail_source(line_no, 1, "too many schedules")
      end

      case :binary.match(line, "\t") do
        {index, 1} -> fail_source(line_no, index + 1, "tab is not allowed")
        :nomatch -> :ok
      end

      tokens = source_tokens(line)

      if length(tokens) != 6 do
        fail_source(line_no, first + 1, "wrong field count")
      end

      [{name, name_col} | field_tokens] = tokens

      unless valid_name?(name) do
        fail_source(line_no, name_col, "invalid name")
      end

      kinds = ["minute", "hour", "day-of-month", "month", "day-of-week"]
      minimums = [0, 0, 1, 1, 0]
      maximums = [59, 23, 31, 12, 7]

      fields =
        Enum.zip([field_tokens, kinds, minimums, maximums, 0..4])
        |> Enum.map(fn {{raw, col}, kind, minimum, maximum, index} ->
          case parse_field(raw, minimum, maximum, index == 4) do
            {:ok, field} -> field
            :error -> fail_source(line_no, col, "invalid #{kind} field")
          end
        end)

      {:ok, %{name: name, fields: fields, line: line_no, col: name_col}}
    end
  end

  defp first_non_space_or_tab(line) do
    line
    |> :binary.bin_to_list()
    |> Enum.find_index(&(&1 != ?\s and &1 != ?\t))
  end

  defp source_tokens(line), do: source_tokens(line, 0, [])

  defp source_tokens(line, index, acc) when index >= byte_size(line), do: Enum.reverse(acc)

  defp source_tokens(line, index, acc) do
    if :binary.at(line, index) == ?\s do
      source_tokens(line, index + 1, acc)
    else
      finish = token_end(line, index)
      token = binary_part(line, index, finish - index)
      source_tokens(line, finish, [{token, index + 1} | acc])
    end
  end

  defp token_end(line, index) when index >= byte_size(line), do: index

  defp token_end(line, index) do
    if :binary.at(line, index) == ?\s, do: index, else: token_end(line, index + 1)
  end

  defp valid_name?(name), do: Regex.match?(~r/\A[a-z][a-z0-9_-]{0,15}\z/, name)

  defp parse_field(raw, minimum, maximum, sunday_alias) do
    terms = String.split(raw, ",", trim: false)

    if terms == [] or Enum.any?(terms, &(&1 == "")) do
      :error
    else
      initial = %{selected: MapSet.new(), min: minimum, max: maximum, wildcard: raw == "*"}

      Enum.reduce_while(terms, {:ok, initial}, fn term, {:ok, field} ->
        case parse_term(term, minimum, maximum) do
          {:ok, values} ->
            normalized =
              Enum.map(values, fn value ->
                if sunday_alias and value == 7, do: 0, else: value
              end)

            {:cont,
             {:ok,
              %{field | selected: Enum.reduce(normalized, field.selected, &MapSet.put(&2, &1))}}}

          :error ->
            {:halt, :error}
        end
      end)
    end
  end

  defp parse_term(term, minimum, maximum) do
    parts = String.split(term, "/", trim: false)
    width = maximum - minimum + 1

    with true <- length(parts) in [1, 2],
         {:ok, step} <- parse_step(parts, width),
         {:ok, start_value, end_value} <-
           parse_base(hd(parts), minimum, maximum, length(parts) == 2) do
      {:ok, Enum.to_list(start_value..end_value//step)}
    else
      _ -> :error
    end
  end

  defp parse_step([_base], _width), do: {:ok, 1}

  defp parse_step([_base, token], width) do
    with {:ok, step} <- parse_decimal(token), true <- step >= 1 and step <= width do
      {:ok, step}
    else
      _ -> :error
    end
  end

  defp parse_base("*", minimum, maximum, _stepped), do: {:ok, minimum, maximum}

  defp parse_base(base, minimum, maximum, stepped) do
    case String.split(base, "-", trim: false) do
      [start_token, end_token] ->
        with {:ok, start_value} <- parse_decimal(start_token),
             {:ok, end_value} <- parse_decimal(end_token),
             true <- start_value >= minimum and end_value <= maximum and start_value <= end_value do
          {:ok, start_value, end_value}
        else
          _ -> :error
        end

      [_single] ->
        with {:ok, value} <- parse_decimal(base),
             true <- value >= minimum and value <= maximum do
          {:ok, value, if(stepped, do: maximum, else: value)}
        else
          _ -> :error
        end

      _ ->
        :error
    end
  end

  defp parse_decimal(value) do
    if decimal_digits?(value) do
      case Integer.parse(value) do
        {number, ""} -> {:ok, number}
        _ -> :error
      end
    else
      :error
    end
  end

  defp check_duplicate_names!(schedules) do
    schedules
    |> Enum.reduce_while(MapSet.new(), fn schedule, seen ->
      if MapSet.member?(seen, schedule.name) do
        fail_source(schedule.line, schedule.col, "duplicate name")
      else
        {:cont, MapSet.put(seen, schedule.name)}
      end
    end)
  end

  defp find_runs(schedule, after_minute, count) do
    horizon = after_minute + @search_minutes
    first_date = after_minute |> minute_to_naive() |> NaiveDateTime.to_date()
    last_date = horizon |> minute_to_naive() |> NaiveDateTime.to_date()
    gather_runs(schedule, first_date, last_date, after_minute, horizon, count, [])
  end

  defp gather_runs(schedule, date, last_date, after_minute, horizon, count, runs) do
    if Date.compare(date, last_date) == :gt do
      Enum.reverse(runs)
    else
      candidates = date_candidates(schedule, date)

      next_runs =
        Enum.reduce_while(candidates, runs, fn candidate, accumulated ->
          if candidate > after_minute and candidate <= horizon do
            updated = [candidate | accumulated]
            if length(updated) >= count, do: {:halt, updated}, else: {:cont, updated}
          else
            {:cont, accumulated}
          end
        end)

      if length(next_runs) >= count do
        Enum.reverse(next_runs)
      else
        gather_runs(
          schedule,
          Date.add(date, 1),
          last_date,
          after_minute,
          horizon,
          count,
          next_runs
        )
      end
    end
  end

  defp date_candidates(schedule, date) do
    [minute_field, hour_field, dom_field, month_field, dow_field] = schedule.fields
    weekday = rem(Date.day_of_week(date), 7)
    day_matches = day_matches?(dom_field, dow_field, date.day, weekday)

    if MapSet.member?(month_field.selected, date.month) and day_matches do
      for hour <- 0..23,
          MapSet.member?(hour_field.selected, hour),
          minute <- 0..59,
          MapSet.member?(minute_field.selected, minute) do
        date
        |> NaiveDateTime.new!(~T[00:00:00])
        |> NaiveDateTime.add(hour * 60 + minute, :minute)
        |> NaiveDateTime.diff(@epoch, :minute)
      end
    else
      []
    end
  end

  defp day_matches?(dom, dow, day_of_month, weekday) do
    cond do
      dom.wildcard and dow.wildcard -> true
      dom.wildcard -> MapSet.member?(dow.selected, weekday)
      dow.wildcard -> MapSet.member?(dom.selected, day_of_month)
      true -> MapSet.member?(dom.selected, day_of_month) and MapSet.member?(dow.selected, weekday)
    end
  end

  defp minute_to_naive(minute), do: NaiveDateTime.add(@epoch, minute, :minute)

  defp render_schedules(schedules, runs, "text") do
    schedules
    |> Enum.zip(runs)
    |> Enum.map_join(fn {schedule, values} ->
      Enum.join([schedule.name | Enum.map(values, &Integer.to_string/1)], "\t") <> "\n"
    end)
  end

  defp render_schedules(schedules, runs, "json") do
    items =
      Enum.zip(schedules, runs)
      |> Enum.map_join(",", fn {schedule, values} ->
        encoded_runs = Enum.map_join(values, ",", &Integer.to_string/1)
        "{\"name\":\"#{schedule.name}\",\"runs\":[#{encoded_runs}]}"
      end)

    "{\"schedules\":[#{items}]}\n"
  end

  defp fail_source(line, col, message), do: Kogen.Input.fail("cron:#{line}:#{col}: #{message}")
end
