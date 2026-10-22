defmodule Kogen.Core do
  @moduledoc "Bounded integer stack virtual machine."

  @help """
  Usage: kogen-vm [--steps N] [--stack N] [FILE|-]
  Run a bounded integer stack program.
  Options:
    --steps N    Maximum instructions executed (default 10000).
    --stack N    Maximum stack depth (default 256).
    --help       Show this help.
  """

  @max_integer 999_999_999

  def execute(args) do
    case parse_args(args) do
      :help ->
        @help

      options ->
        data = Kogen.Input.read(options.path, "vm")

        if byte_size(data) > 1_048_576 do
          Kogen.Input.fail("vm: input too large")
        end

        {program, labels} = parse_program(data)
        run_program(program, labels, options.steps, options.stack)
    end
  end

  defp parse_args(["--help"]), do: :help

  defp parse_args(args) do
    options = %{steps: 10_000, stack: 256, seen_steps: false, seen_stack: false, path: nil}
    parse_args(args, options)
  end

  defp parse_args([], options), do: options

  defp parse_args(["--help" | _], _options),
    do: Kogen.Input.fail("vm: unknown option '--help'", 2)

  defp parse_args([option | rest], options) when option in ["--steps", "--stack"] do
    key = if option == "--steps", do: :steps, else: :stack
    seen_key = if key == :steps, do: :seen_steps, else: :seen_stack

    if Map.fetch!(options, seen_key) do
      Kogen.Input.fail("vm: duplicate option '#{option}'", 2)
    end

    case rest do
      [] ->
        Kogen.Input.fail("vm: option '#{option}' requires a value", 2)

      [value | tail] ->
        unless decimal_digits?(value) do
          Kogen.Input.fail("vm: invalid value for '#{option}': '#{value}'", 2)
        end

        number = String.to_integer(value)
        maximum = if key == :steps, do: 100_000, else: 4_096

        if number < 1 or number > maximum do
          Kogen.Input.fail("vm: value out of range for '#{option}': '#{value}'", 2)
        end

        options
        |> Map.put(key, number)
        |> Map.put(seen_key, true)
        |> then(&parse_args(tail, &1))
    end
  end

  defp parse_args([token | rest], options) do
    cond do
      String.starts_with?(token, "-") and token != "-" ->
        Kogen.Input.fail("vm: unknown option '#{token}'", 2)

      is_nil(options.path) ->
        parse_args(rest, %{options | path: token})

      true ->
        Kogen.Input.fail("vm: expected at most one input path", 2)
    end
  end

  defp decimal_digits?(value) when byte_size(value) > 0 do
    value |> :binary.bin_to_list() |> Enum.all?(&(&1 >= ?0 and &1 <= ?9))
  end

  defp decimal_digits?(_value), do: false

  defp parse_program(data) do
    lines = Kogen.Input.physical_lines(data)
    validate_ascii!(lines)

    state = %{program: [], labels: %{}, duplicates: [], records: 0, pc: 0}

    state =
      lines
      |> Enum.with_index(1)
      |> Enum.reduce(state, fn {line, line_no}, acc -> parse_line(line, line_no, acc) end)

    case Enum.reverse(state.duplicates) do
      [{line, col} | _] -> fail_source(line, col, "duplicate label")
      [] -> :ok
    end

    program = Enum.reverse(state.program)

    Enum.each(program, fn instruction ->
      if instruction.op in ["JMP", "JZ"] and not Map.has_key?(state.labels, instruction.label) do
        fail_source(instruction.line, instruction.arg_col, "unknown label")
      end
    end)

    resolved = Map.new(state.labels, fn {name, target} -> {name, target.pc} end)
    {program, resolved}
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

  defp parse_line(line, line_no, state) do
    first = first_non_space_or_tab(line)

    if is_nil(first) or byte_at(line, first) == ?# do
      state
    else
      if state.records >= 10_000 do
        fail_source(line_no, 1, "too many records")
      end

      case :binary.match(line, "\t") do
        {index, 1} -> fail_source(line_no, index + 1, "tab is not allowed")
        :nomatch -> :ok
      end

      tokens = line |> strip_comment() |> source_tokens()

      case tokens do
        [] ->
          state

        _ ->
          next_state = %{state | records: state.records + 1}
          parse_record(tokens, line_no, next_state)
      end
    end
  end

  defp first_non_space_or_tab(line) do
    line
    |> :binary.bin_to_list()
    |> Enum.find_index(&(&1 != ?\s and &1 != ?\t))
  end

  defp byte_at(line, index), do: :binary.at(line, index)

  defp strip_comment(line) do
    bytes = :binary.bin_to_list(line)

    comment =
      bytes
      |> Enum.with_index()
      |> Enum.find_value(fn
        {?#, 0} -> 0
        {?#, index} when index > 0 -> if(Enum.at(bytes, index - 1) == ?\s, do: index, else: nil)
        _ -> nil
      end)

    if is_nil(comment) do
      trim_right_spaces(line)
    else
      line |> binary_part(0, comment) |> trim_right_spaces()
    end
  end

  defp trim_right_spaces(line) do
    size = byte_size(line)
    trim_right_spaces(line, size)
  end

  defp trim_right_spaces(_line, 0), do: ""

  defp trim_right_spaces(line, size) do
    if :binary.at(line, size - 1) == ?\s do
      trim_right_spaces(line, size - 1)
    else
      binary_part(line, 0, size)
    end
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

  defp parse_record([{token, col} | rest], line_no, state) do
    if String.ends_with?(token, ":") do
      if rest != [] do
        fail_source(line_no, col, "wrong operand count")
      end

      name = String.trim_trailing(token, ":")

      unless valid_label?(name) do
        fail_source(line_no, col, "invalid label")
      end

      if Map.has_key?(state.labels, name) do
        %{state | duplicates: [{line_no, col} | state.duplicates]}
      else
        target = %{pc: state.pc, line: line_no, col: col}
        %{state | labels: Map.put(state.labels, name, target)}
      end
    else
      parse_instruction(token, col, rest, line_no, state)
    end
  end

  defp parse_instruction(op, col, operands, line_no, state) do
    expected =
      case op do
        value when value in ["PUSH", "JMP", "JZ"] ->
          1

        value
        when value in ["DUP", "DROP", "SWAP", "ADD", "SUB", "MUL", "DIV", "MOD", "OUT", "HALT"] ->
          0

        _ ->
          fail_source(line_no, col, "unknown instruction")
      end

    if length(operands) != expected do
      fail_source(line_no, col, "wrong operand count")
    end

    instruction =
      case {op, operands} do
        {"PUSH", [{value, value_col}]} ->
          case parse_vm_integer(value) do
            {:ok, number} -> %{op: op, value: number, line: line_no, col: col}
            :invalid -> fail_source(line_no, value_col, "invalid integer")
            :out_of_range -> fail_source(line_no, value_col, "integer out of range")
          end

        {jump, [{label, label_col}]} when jump in ["JMP", "JZ"] ->
          unless valid_label?(label) do
            fail_source(line_no, label_col, "invalid label")
          end

          %{op: op, label: label, arg_col: label_col, line: line_no, col: col}

        {other, []} ->
          %{op: other, line: line_no, col: col}
      end

    %{state | program: [instruction | state.program], pc: state.pc + 1}
  end

  defp parse_vm_integer(token) do
    if Regex.match?(~r/\A[+-]?[0-9]+\z/, token) do
      value = String.to_integer(token)

      if value < -@max_integer or value > @max_integer do
        :out_of_range
      else
        {:ok, value}
      end
    else
      :invalid
    end
  end

  defp valid_label?(label), do: Regex.match?(~r/\A[a-z][a-z0-9_]{0,15}\z/, label)

  defp run_program(program, labels, steps_limit, stack_limit) do
    program
    |> List.to_tuple()
    |> execute_loop(labels, 0, [], 0, 0, [], steps_limit, stack_limit)
  end

  defp execute_loop(
         program,
         _labels,
         pc,
         _stack,
         _depth,
         _steps,
         output,
         _steps_limit,
         _stack_limit
       )
       when pc >= tuple_size(program) do
    output_binary(output)
  end

  defp execute_loop(program, labels, pc, stack, depth, steps, output, steps_limit, stack_limit) do
    instruction = elem(program, pc)

    if steps == steps_limit do
      fail_source(instruction.line, instruction.col, "step limit exceeded")
    end

    next_steps = steps + 1

    case instruction.op do
      "PUSH" ->
        if stack_full?(depth, stack_limit) do
          fail_source(instruction.line, instruction.col, "stack overflow")
        end

        execute_loop(
          program,
          labels,
          pc + 1,
          [instruction.value | stack],
          depth + 1,
          next_steps,
          output,
          steps_limit,
          stack_limit
        )

      "DUP" ->
        case stack do
          [value | _] ->
            if stack_full?(depth, stack_limit) do
              fail_source(instruction.line, instruction.col, "stack overflow")
            end

            execute_loop(
              program,
              labels,
              pc + 1,
              [value | stack],
              depth + 1,
              next_steps,
              output,
              steps_limit,
              stack_limit
            )

          [] ->
            fail_source(instruction.line, instruction.col, "stack underflow")
        end

      "DROP" ->
        case stack do
          [_value | tail] ->
            execute_loop(
              program,
              labels,
              pc + 1,
              tail,
              depth - 1,
              next_steps,
              output,
              steps_limit,
              stack_limit
            )

          [] ->
            fail_source(instruction.line, instruction.col, "stack underflow")
        end

      "SWAP" ->
        case stack do
          [top, below | tail] ->
            execute_loop(
              program,
              labels,
              pc + 1,
              [below, top | tail],
              depth,
              next_steps,
              output,
              steps_limit,
              stack_limit
            )

          _ ->
            fail_source(instruction.line, instruction.col, "stack underflow")
        end

      op when op in ["ADD", "SUB", "MUL", "DIV", "MOD"] ->
        execute_arithmetic(
          op,
          instruction,
          program,
          labels,
          pc,
          stack,
          depth,
          next_steps,
          output,
          steps_limit,
          stack_limit
        )

      "OUT" ->
        case stack do
          [value | tail] ->
            execute_loop(
              program,
              labels,
              pc + 1,
              tail,
              depth - 1,
              next_steps,
              [Integer.to_string(value) | output],
              steps_limit,
              stack_limit
            )

          [] ->
            fail_source(instruction.line, instruction.col, "stack underflow")
        end

      "JMP" ->
        execute_loop(
          program,
          labels,
          Map.fetch!(labels, instruction.label),
          stack,
          depth,
          next_steps,
          output,
          steps_limit,
          stack_limit
        )

      "JZ" ->
        case stack do
          [condition | tail] ->
            target = if condition == 0, do: Map.fetch!(labels, instruction.label), else: pc + 1

            execute_loop(
              program,
              labels,
              target,
              tail,
              depth - 1,
              next_steps,
              output,
              steps_limit,
              stack_limit
            )

          [] ->
            fail_source(instruction.line, instruction.col, "stack underflow")
        end

      "HALT" ->
        output_binary(output)
    end
  end

  defp execute_arithmetic(
         op,
         instruction,
         program,
         labels,
         pc,
         [right, left | tail],
         depth,
         steps,
         output,
         steps_limit,
         stack_limit
       ) do
    if op in ["DIV", "MOD"] and right == 0 do
      fail_source(instruction.line, instruction.col, "division by zero")
    end

    value =
      case op do
        "ADD" -> left + right
        "SUB" -> left - right
        "MUL" -> left * right
        "DIV" -> div(left, right)
        "MOD" -> rem(left, right)
      end

    if value < -@max_integer or value > @max_integer do
      fail_source(instruction.line, instruction.col, "integer overflow")
    end

    execute_loop(
      program,
      labels,
      pc + 1,
      [value | tail],
      depth - 1,
      steps,
      output,
      steps_limit,
      stack_limit
    )
  end

  defp execute_arithmetic(
         _op,
         instruction,
         _program,
         _labels,
         _pc,
         _stack,
         _depth,
         _steps,
         _output,
         _steps_limit,
         _stack_limit
       ) do
    fail_source(instruction.line, instruction.col, "stack underflow")
  end

  defp output_binary([]), do: ""
  defp output_binary(output), do: Enum.reverse(output) |> Enum.join("\n") |> Kernel.<>("\n")

  defp stack_full?(depth, stack_limit), do: depth > stack_limit

  defp fail_source(line, col, message), do: Kogen.Input.fail("vm:#{line}:#{col}: #{message}")
end
