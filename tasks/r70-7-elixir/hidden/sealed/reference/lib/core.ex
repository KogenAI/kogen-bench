defmodule Kogen.Core do
  @moduledoc "CLI argument parser and pure aggregation core."
  alias Kogen.Input

  @help """
  Usage: kogen <command> [options] [FILE|-]
  Commands:
    sum     Sum signed integers.
    status  Count job states.
  Options:
    -h, --help  Show help.
    --version   Show version.
  """
  @sum_help """
  Usage: kogen sum [--scale N] [--format text|json] [FILE|-]
  Sum one signed integer per nonempty line (default scale: 1).
  """
  @status_help """
  Usage: kogen status [--format text|json] [FILE|-]
  Count ID,STATE records (states: queued,running,done,failed).
  """
  @states ["queued", "running", "done", "failed"]
  @keys ["total" | @states]

  @doc "Run argument parsing and an in-process core."
  def execute([]), do: @help
  def execute([flag]) when flag in ["--help", "-h"], do: @help
  def execute(["--version"]), do: "kogen 1.0.0\n"
  def execute(["sum", flag]) when flag in ["--help", "-h"], do: @sum_help
  def execute(["status", flag]) when flag in ["--help", "-h"], do: @status_help

  def execute([command | rest]) when command in ["sum", "status"] do
    opts = options(rest, %{command: command, format: "text", scale: 1, path: nil}, %{})
    bytes = Input.read(opts.path, "kogen")
    ascii(bytes)
    aggregate(Input.physical_lines(bytes), opts)
  end

  def execute([command | _rest]) do
    kind = if String.starts_with?(command, "-"), do: "option", else: "command"
    Input.fail("kogen: unknown #{kind} '#{command}'", 2)
  end

  defp ascii(<<>>), do: :ok
  defp ascii(<<byte, _rest::binary>>) when byte > 127, do: Input.fail("kogen: input is not ASCII")
  defp ascii(<<_byte, rest::binary>>), do: ascii(rest)

  @spec options([String.t()], map(), map()) :: map()
  defp options([], opts, _seen), do: opts

  defp options([flag | rest], opts, seen)
       when flag == "--format" or
              (flag == "--scale" and opts.command == "sum") do
    if Map.has_key?(seen, flag), do: Input.fail("kogen: duplicate option '#{flag}'", 2)

    case rest do
      [] ->
        Input.fail("kogen: option '#{flag}' requires a value", 2)

      [value | remaining] ->
        options(remaining, option(opts, flag, value), Map.put(seen, flag, true))
    end
  end

  defp options([arg | rest], opts, seen) do
    cond do
      String.starts_with?(arg, "-") and arg != "-" ->
        Input.fail("kogen: unknown option '#{arg}'", 2)

      opts.path != nil ->
        Input.fail("kogen: expected at most one input path", 2)

      true ->
        options(rest, %{opts | path: arg}, seen)
    end
  end

  defp option(opts, "--format", value) when value in ["text", "json"], do: %{opts | format: value}

  defp option(opts, "--scale", value) do
    valid = Regex.match?(~r/^(0|[1-9][0-9]*)$/, value) and byte_size(value) <= 3
    unless valid, do: invalid("--scale", value)
    scale = String.to_integer(value)
    if scale > 100, do: invalid("--scale", value)
    %{opts | scale: scale}
  end

  defp option(_opts, flag, value), do: invalid(flag, value)
  @spec invalid(String.t(), String.t()) :: no_return()
  defp invalid(flag, value), do: Input.fail("kogen: invalid value for '#{flag}': '#{value}'", 2)

  defp aggregate(lines, %{command: "sum"} = opts) do
    total = lines |> Enum.with_index(1) |> Enum.reduce(0, &sum_line/2)
    result = total * opts.scale
    if opts.format == "json", do: "{\"sum\":#{result}}\n", else: "sum=#{result}\n"
  end

  defp aggregate(lines, opts) do
    defaults = Map.new(@keys, &{&1, 0})

    {counts, _ids} =
      lines |> Enum.with_index(1) |> Enum.reduce({defaults, MapSet.new()}, &status_line/2)

    if opts.format == "json" do
      "{" <> Enum.map_join(@keys, ",", &"\"#{&1}\":#{counts[&1]}") <> "}\n"
    else
      Enum.map_join(@keys, &"#{&1}=#{counts[&1]}\n")
    end
  end

  defp sum_line({"", _number}, total), do: total

  defp sum_line({line, number}, total) do
    digits =
      line |> String.trim_leading("+") |> String.trim_leading("-") |> String.trim_leading("0")

    valid = Regex.match?(~r/^[+-]?[0-9]+$/, line) and byte_size(digits) <= 7
    unless valid, do: Input.fail("kogen:#{number}: expected integer -1000000..1000000")
    value = if digits == "", do: 0, else: String.to_integer(digits)
    if value > 1_000_000, do: Input.fail("kogen:#{number}: expected integer -1000000..1000000")
    total + if(String.starts_with?(line, "-"), do: -value, else: value)
  end

  @spec status_line({String.t(), integer()}, {map(), MapSet.t()}) :: {map(), MapSet.t()}
  defp status_line({"", _number}, state), do: state

  defp status_line({line, number}, {counts, ids}) do
    {id, state} = record(line, number)
    if MapSet.member?(ids, id), do: Input.fail("kogen:#{number}: duplicate id '#{id}'")
    counts = counts |> Map.update!("total", &(&1 + 1)) |> Map.update!(state, &(&1 + 1))
    {counts, MapSet.put(ids, id)}
  end

  defp record(line, number) do
    case Regex.run(~r/^([a-z][a-z0-9_-]{0,31}),(queued|running|done|failed)$/, line) do
      [_all, id, state] -> {id, state}
      nil -> Input.fail("kogen:#{number}: expected ID,STATE")
    end
  end
end
