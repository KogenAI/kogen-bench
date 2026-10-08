defmodule Loop.CLI do
  @moduledoc false

  @tools ~S([{"type":"function","name":"read_file","description":"Read a UTF-8 file under the workdir","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"],"additionalProperties":false}},{"type":"function","name":"run_command","description":"Run a shell command with the workdir as its current directory","parameters":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"],"additionalProperties":false}}])

  @type parser_state :: %{
          buffer: binary(),
          event: binary() | nil,
          data: binary() | nil,
          calls: [map()],
          call_map: map(),
          text: binary(),
          saw_text: boolean(),
          completed: boolean(),
          invalid: boolean(),
          usage: map() | nil
        }

  @type parser_result ::
          {:complete, map()} | {:invalid, parser_state()} | {:more, parser_state()}

  def main(args) do
    case run(args) do
      :ok ->
        :ok

      {:error, code, message} ->
        IO.write(:stderr, message <> "\n")
        System.halt(code)
    end
  end

  defp run(args) do
    with {:ok, options} <- parse_args(args),
         {:ok, prompt} <- read_prompt(options.prompt_file),
         {:ok, workdir} <- resolve_workdir(options.workdir),
         {:ok, records} <- open_records(options.records) do
      started = monotonic_ms()

      try do
        user = %{
          "role" => "user",
          "content" => [%{"type" => "input_text", "text" => prompt}]
        }

        history = "[" <> Jason.encode!(user) <> "]"
        loop(options, workdir, records, started, history, 1)
      after
        File.close(records)
      end
    end
  end

  defp parse_args(["loop", "run" | rest]) do
    defaults = %{
      first_byte_ms: 5000,
      idle_ms: 3000,
      max_retries: 2,
      backoff_ms: 50,
      workdir: nil,
      session: nil
    }

    case parse_flags(rest, defaults, []) do
      {:ok, options} ->
        complete_options(options)

      :error ->
        invalid_cli()
    end
  end

  defp parse_args(_args), do: invalid_cli()

  defp complete_options(options) do
    if required_options?(options) and valid_server?(options.server) and
         valid_session_option?(options.session) do
      {:ok, Map.put(options, :session, options.session || generated_session())}
    else
      invalid_cli()
    end
  end

  defp required_options?(options) do
    prompt_file = Map.get(options, :prompt_file)
    server = Map.get(options, :server)
    records = Map.get(options, :records)

    is_binary(prompt_file) and prompt_file != "" and is_binary(server) and server != "" and
      is_binary(records) and records != ""
  end

  defp valid_session_option?(nil), do: true
  defp valid_session_option?(session), do: valid_session?(session)

  defp parse_flags([], options, _seen), do: {:ok, options}
  defp parse_flags([_flag], _options, _seen), do: :error

  defp parse_flags([flag, value | rest], options, seen) do
    if flag in seen do
      :error
    else
      parse_flag(flag, value, rest, options, [flag | seen])
    end
  end

  defp parse_flag("--prompt-file", value, rest, options, seen),
    do: parse_flags(rest, Map.put(options, :prompt_file, value), seen)

  defp parse_flag("--server", value, rest, options, seen),
    do: parse_flags(rest, Map.put(options, :server, value), seen)

  defp parse_flag("--records", value, rest, options, seen),
    do: parse_flags(rest, Map.put(options, :records, value), seen)

  defp parse_flag("--workdir", value, rest, options, seen),
    do: parse_flags(rest, Map.put(options, :workdir, value), seen)

  defp parse_flag("--session", value, rest, options, seen),
    do: parse_flags(rest, Map.put(options, :session, value), seen)

  defp parse_flag("--first-byte-timeout-ms", value, rest, options, seen),
    do: parse_number_flag(value, rest, options, seen, :first_byte_ms, 1, 60_000)

  defp parse_flag("--idle-timeout-ms", value, rest, options, seen),
    do: parse_number_flag(value, rest, options, seen, :idle_ms, 1, 60_000)

  defp parse_flag("--max-retries", value, rest, options, seen),
    do: parse_number_flag(value, rest, options, seen, :max_retries, 0, 5)

  defp parse_flag("--backoff-ms", value, rest, options, seen),
    do: parse_number_flag(value, rest, options, seen, :backoff_ms, 0, 5000)

  defp parse_flag(_flag, _value, _rest, _options, _seen), do: :error

  defp parse_number_flag(value, rest, options, seen, key, minimum, maximum) do
    case bounded_number(value, minimum, maximum) do
      {:ok, number} -> parse_flags(rest, Map.put(options, key, number), seen)
      :error -> :error
    end
  end

  defp bounded_number(value, minimum, maximum) do
    if Regex.match?(~r/^[0-9]+$/, value) do
      case Integer.parse(value) do
        {number, ""} when number >= minimum and number <= maximum -> {:ok, number}
        _ -> :error
      end
    else
      :error
    end
  end

  defp valid_session?(value) do
    byte_size(value) >= 1 and byte_size(value) <= 128 and
      Regex.match?(~r/^[A-Za-z0-9._:-]+$/, value)
  end

  defp valid_server?(server) do
    uri = URI.parse(server)
    valid_port = is_nil(uri.port) or (is_integer(uri.port) and uri.port >= 0 and uri.port <= 65_535)

    uri.scheme == "http" and is_binary(uri.host) and uri.host != "" and valid_port and
      uri.path in [nil, "", "/"] and is_nil(uri.query) and is_nil(uri.fragment) and
      is_nil(uri.userinfo)
  rescue
    _ -> false
  end

  defp generated_session do
    "loop-#{System.pid()}-#{System.unique_integer([:positive, :monotonic])}-#{monotonic_ms()}"
  end

  defp invalid_cli, do: {:error, 2, "loop: invalid command line"}

  defp read_prompt(path) do
    case File.read(path) do
      {:ok, content} ->
        if String.valid?(content),
          do: {:ok, content},
          else: {:error, 1, "loop: cannot read prompt file"}

      _ ->
        {:error, 1, "loop: cannot read prompt file"}
    end
  end

  defp resolve_workdir(nil) do
    case File.cwd() do
      {:ok, path} -> resolve_workdir(path)
      _ -> {:error, 1, "loop: invalid workdir"}
    end
  end

  defp resolve_workdir(path) do
    with {:ok, resolved} <- canonical_path(path),
         {:ok, %File.Stat{type: :directory}} <- File.stat(resolved) do
      {:ok, resolved}
    else
      _ -> {:error, 1, "loop: invalid workdir"}
    end
  end

  defp open_records(path) do
    case File.open(path, [:write, :binary]) do
      {:ok, file} -> {:ok, file}
      _ -> {:error, 1, "loop: cannot write records file"}
    end
  end

  defp loop(options, workdir, records, started, history, history_count) do
    body = request_body(history)

    case request_with_retries(options, records, started, body, history_count) do
      {:ok, response} ->
        continue_response(response, options, workdir, records, started, history, history_count)

      error ->
        error
    end
  end

  defp continue_response(
         %{calls: []} = response,
         _options,
         _workdir,
         _records,
         _started,
         _history,
         _count
       ),
       do: IO.binwrite(:stdio, response.text)

  defp continue_response(response, options, workdir, records, started, history, history_count) do
    with {:ok, outputs} <- execute_calls(response.calls, workdir, []),
         {:ok, next_history} <- append_history(history, response.calls, outputs) do
      loop(
        options,
        workdir,
        records,
        started,
        next_history,
        history_count + length(response.calls) * 2
      )
    end
  end

  defp request_with_retries(options, records, started, body, history_count) do
    request_with_retries(options, records, started, body, history_count, 0)
  end

  defp request_with_retries(options, records, started, body, history_count, retry) do
    case request_once(options, records, started, body, history_count, retry) do
      {:ok, response} ->
        {:ok, response}

      {:fatal, code, message} ->
        {:error, code, message}

      {:error, kind} when kind in [:rejected, :invalid] ->
        attempt_error(kind)

      {:error, kind} when retry >= options.max_retries ->
        attempt_error(kind)

      {:error, _kind} ->
        Process.sleep(options.backoff_ms * trunc(:math.pow(2, retry)))
        request_with_retries(options, records, started, body, history_count, retry + 1)
    end
  end

  defp request_once(options, records, run_started, body, history_count, retry) do
    request_started = monotonic_ms()
    first_deadline = request_started + options.first_byte_ms

    record = %{
      start_ms: request_started - run_started,
      first_byte_ms: nil,
      end_ms: 0,
      outcome: "transport",
      retries: retry,
      usage: %{input_tokens: nil, output_tokens: nil, cached_tokens: nil},
      request_bytes: byte_size(body),
      history_items: history_count
    }

    case connect_and_send(options, body) do
      {:ok, socket, pending} ->
        receive_response(socket, pending, options, run_started, first_deadline, records, record)

      {:error, :timeout} ->
        finish_failure(records, record, run_started, "timeout", :timeout)

      {:error, _reason} ->
        finish_failure(records, record, run_started, "transport", :transport)
    end
  end

  defp connect_and_send(options, body) do
    uri = URI.parse(options.server)
    port = uri.port || 80
    timeout = options.first_byte_ms

    case :gen_tcp.connect(String.to_charlist(uri.host), port, [:binary, active: false], timeout) do
      {:ok, socket} ->
        host_header = if uri.port, do: "#{uri.host}:#{uri.port}", else: uri.host

        request =
          "POST /v1/responses HTTP/1.1\r\n" <>
            "Host: #{host_header}\r\n" <>
            "Content-Type: application/json\r\n" <>
            "Accept: text/event-stream\r\n" <>
            "X-Session-ID: #{options.session}\r\n" <>
            "Content-Length: #{byte_size(body)}\r\n" <>
            "Connection: close\r\n\r\n" <> body

        case :gen_tcp.send(socket, request) do
          :ok ->
            {:ok, socket, <<>>}

          {:error, reason} ->
            :gen_tcp.close(socket)
            {:error, reason}
        end

      {:error, reason} ->
        {:error, reason}
    end
  end

  defp receive_response(socket, buffer, options, run_started, first_deadline, records, record) do
    context = %{
      socket: socket,
      options: options,
      run_started: run_started,
      first_deadline: first_deadline,
      records: records,
      record: record
    }

    case receive_headers(socket, buffer, first_deadline) do
      {:ok, status, headers, body} ->
        handle_response_status(status, headers, body, context)

      {:error, :timeout} ->
        :gen_tcp.close(socket)
        finish_failure(records, record, run_started, "timeout", :timeout)

      {:error, _reason} ->
        :gen_tcp.close(socket)
        finish_failure(records, record, run_started, "transport", :transport)
    end
  end

  defp handle_response_status(status, _headers, _body, context)
       when status in [429, 529] or status >= 500 do
    close_failed_response(context, "overload", :overload)
  end

  defp handle_response_status(200, headers, body, context) do
    if event_stream?(headers) do
      stream_response(context, body)
    else
      close_failed_response(context, "transport", :invalid)
    end
  end

  defp handle_response_status(_status, _headers, _body, context) do
    close_failed_response(context, "transport", :rejected)
  end

  defp close_failed_response(context, outcome, kind) do
    :gen_tcp.close(context.socket)
    finish_failure(context.records, context.record, context.run_started, outcome, kind)
  end

  defp event_stream?(headers) do
    case header_value(headers, "content-type") do
      content_type when is_binary(content_type) ->
        String.starts_with?(String.downcase(content_type), "text/event-stream")

      _ ->
        false
    end
  end

  defp stream_response(context, body) do
    state = %{
      socket: context.socket,
      parser: new_parser(),
      options: context.options,
      run_started: context.run_started,
      first_deadline: context.first_deadline,
      records: context.records,
      record: context.record,
      first_byte: nil
    }

    case consume_body(state, body) do
      {:ok, response} ->
        :gen_tcp.close(context.socket)
        {:ok, response}

      {:error, kind, outcome, updated_record} ->
        :gen_tcp.close(context.socket)
        finish_failure(context.records, updated_record, context.run_started, outcome, kind)

      {:fatal, code, message} ->
        :gen_tcp.close(context.socket)
        {:fatal, code, message}
    end
  end

  defp receive_headers(socket, buffer, deadline) do
    case split_headers(buffer) do
      {:ok, header_bytes, body} ->
        parse_headers(socket, header_bytes, body, deadline)

      :more ->
        remaining = max(deadline - monotonic_ms(), 0)

        case :gen_tcp.recv(socket, 0, remaining) do
          {:ok, data} -> receive_headers(socket, buffer <> data, deadline)
          {:error, reason} -> {:error, reason}
        end
    end
  end

  defp split_headers(buffer) do
    case :binary.match(buffer, "\r\n\r\n") do
      {index, 4} ->
        <<headers::binary-size(^index), _separator::binary-size(4), body::binary>> = buffer
        {:ok, headers, body}

      :nomatch ->
        case :binary.match(buffer, "\n\n") do
          {index, 2} ->
            <<headers::binary-size(^index), _separator::binary-size(2), body::binary>> = buffer
            {:ok, headers, body}

          :nomatch ->
            :more
        end
    end
  end

  defp parse_headers(socket, header_bytes, body, deadline) do
    lines = String.split(header_bytes, ~r/\r?\n/)

    with [status_line | header_lines] <- lines,
         ["HTTP/" <> _version, status_text | _] <- String.split(status_line, " "),
         {status, ""} <- Integer.parse(status_text) do
      headers =
        Enum.reduce(header_lines, %{}, &put_header(&2, &1))

      decode_headers(socket, status, headers, body, deadline)
    else
      _ -> {:error, :invalid_response}
    end
  end

  defp put_header(headers, line) do
    case String.split(line, ":", parts: 2) do
      [name, value] -> Map.put(headers, String.downcase(String.trim(name)), String.trim(value))
      _ -> headers
    end
  end

  defp decode_headers(socket, status, headers, body, deadline) do
    case decode_body(socket, headers, body, deadline) do
      {:ok, decoded} -> {:ok, status, headers, decoded}
      error -> error
    end
  end

  defp decode_body(socket, headers, body, deadline) do
    transfer = Map.get(headers, "transfer-encoding", "") |> String.downcase()

    if String.contains?(transfer, "chunked"),
      do: decode_chunked(socket, body, deadline, []),
      else: {:ok, body}
  end

  defp decode_chunked(socket, buffer, deadline, chunks) do
    case take_line(buffer) do
      {:ok, line, rest} ->
        size_text = line |> String.split(";", parts: 2) |> hd() |> String.trim()
        decode_chunk_size(socket, size_text, rest, deadline, chunks)

      :more ->
        case receive_more(socket, buffer, deadline) do
          {:ok, data} -> decode_chunked(socket, buffer <> data, deadline, chunks)
          error -> error
        end
    end
  end

  defp decode_chunk_size(_socket, "0", _rest, _deadline, chunks),
    do: {:ok, IO.iodata_to_binary(Enum.reverse(chunks))}

  defp decode_chunk_size(socket, size_text, rest, deadline, chunks) do
    case Integer.parse(size_text, 16) do
      {size, _} when size > 0 ->
        read_chunk(socket, rest, size, deadline, chunks)

      _ ->
        {:error, :invalid_response}
    end
  end

  defp read_chunk(socket, rest, size, deadline, chunks) do
    case ensure_bytes(socket, rest, size + 2, deadline) do
      {:ok, <<chunk::binary-size(^size), _ending::binary-size(2), remaining::binary>>} ->
        decode_chunked(socket, remaining, deadline, [chunk | chunks])

      error ->
        error
    end
  end

  defp ensure_bytes(_socket, buffer, count, _deadline) when byte_size(buffer) >= count,
    do: {:ok, buffer}

  defp ensure_bytes(socket, buffer, count, deadline) do
    case receive_more(socket, buffer, deadline) do
      {:ok, data} -> ensure_bytes(socket, buffer <> data, count, deadline)
      error -> error
    end
  end

  defp take_line(buffer) do
    case :binary.match(buffer, "\r\n") do
      {index, 2} ->
        <<line::binary-size(^index), _crlf::binary-size(2), rest::binary>> = buffer
        {:ok, line, rest}

      :nomatch ->
        :more
    end
  end

  defp receive_more(socket, _buffer, deadline) do
    remaining = max(deadline - monotonic_ms(), 0)

    case :gen_tcp.recv(socket, 0, remaining) do
      {:ok, data} -> {:ok, data}
      {:error, :timeout} when remaining > 0 -> {:error, :timeout}
      {:error, reason} -> {:error, reason}
    end
  end

  defp consume_body(state, body) when byte_size(body) > 0, do: consume_bytes(state, body)

  defp consume_body(state, <<>>) do
    timeout = receive_timeout(state)

    case :gen_tcp.recv(state.socket, 0, timeout) do
      {:ok, data} -> consume_bytes(state, data)
      {:error, :timeout} -> timeout_failure(state)
      {:error, _reason} -> {:error, :transport, "transport", state.record}
    end
  end

  defp receive_timeout(state) do
    if is_nil(state.first_byte),
      do: max(state.first_deadline - monotonic_ms(), 0),
      else: state.options.idle_ms
  end

  defp timeout_failure(state) do
    if is_nil(state.first_byte),
      do: {:error, :timeout, "timeout", state.record},
      else: {:error, :stall, "stall", state.record}
  end

  defp consume_bytes(state, <<>>), do: consume_body(state, <<>>)

  defp consume_bytes(state, bytes) do
    state = note_first_byte(state)
    handle_parsed(state, feed_parser(state.parser, bytes))
  end

  defp note_first_byte(%{first_byte: nil} = state) do
    first_byte = monotonic_ms()

    %{
      state
      | first_byte: first_byte,
        record: %{state.record | first_byte_ms: first_byte - state.run_started}
    }
  end

  defp note_first_byte(state), do: state

  defp handle_parsed(state, {:complete, response}),
    do: record_ok(state.records, state.record, state.run_started, response)

  defp handle_parsed(state, {:invalid, _parser}),
    do: {:error, :invalid, "transport", state.record}

  defp handle_parsed(state, {:more, parser}),
    do: consume_body(%{state | parser: parser}, <<>>)

  @spec new_parser() :: parser_state()
  defp new_parser do
    %{
      buffer: <<>>,
      event: nil,
      data: nil,
      calls: [],
      call_map: %{},
      text: "",
      saw_text: false,
      completed: false,
      invalid: false,
      usage: nil
    }
  end

  @spec feed_parser(parser_state(), binary()) :: parser_result()
  defp feed_parser(parser, bytes) do
    parser = %{parser | buffer: parser.buffer <> bytes}
    process_lines(parser)
  end

  defp process_lines(%{invalid: true} = parser), do: {:invalid, parser}

  defp process_lines(%{completed: true, buffer: <<>>, event: nil, data: nil} = parser),
    do: {:complete, response_from(parser)}

  defp process_lines(%{completed: true} = parser), do: {:invalid, %{parser | invalid: true}}

  defp process_lines(parser) do
    case :binary.match(parser.buffer, "\n") do
      {index, 1} ->
        <<line::binary-size(^index), _lf::binary-size(1), rest::binary>> = parser.buffer

        line =
          if String.ends_with?(line, "\r"),
            do: binary_part(line, 0, byte_size(line) - 1),
            else: line

        next = process_line(%{parser | buffer: rest}, line)

        case next do
          %{invalid: true} = invalid ->
            {:invalid, invalid}

          %{completed: true, buffer: <<>>, event: nil, data: nil} = complete ->
            {:complete, response_from(complete)}

          %{completed: true} = complete ->
            {:invalid, %{complete | invalid: true}}

          other ->
            process_lines(other)
        end

      :nomatch ->
        {:more, parser}
    end
  end

  defp process_line(%{event: nil, data: nil} = parser, ""), do: parser

  defp process_line(parser, "") do
    next = dispatch(parser)
    %{next | event: nil, data: nil}
  end

  defp process_line(parser, <<":", _rest::binary>>), do: parser

  defp process_line(%{event: nil} = parser, <<"event: ", event::binary>>),
    do: %{parser | event: event}

  defp process_line(%{data: nil} = parser, <<"data: ", data::binary>>),
    do: %{parser | data: data}

  defp process_line(parser, _line), do: %{parser | invalid: true}

  defp dispatch(%{event: nil} = parser), do: %{parser | invalid: true}
  defp dispatch(%{data: nil} = parser), do: %{parser | invalid: true}
  defp dispatch(%{completed: true} = parser), do: %{parser | invalid: true}

  defp dispatch(parser) do
    case Jason.decode(parser.data) do
      {:ok, event} when is_map(event) -> dispatch_event(parser, event)
      _ -> %{parser | invalid: true}
    end
  end

  defp dispatch_event(%{event: "response.function_call_arguments.delta"} = parser, event),
    do: dispatch_call_delta(parser, event)

  defp dispatch_event(%{event: "response.output_text.delta"} = parser, event),
    do: dispatch_text_delta(parser, event)

  defp dispatch_event(%{event: "response.completed"} = parser, event),
    do: dispatch_completed(parser, event)

  defp dispatch_event(parser, _event), do: %{parser | invalid: true}

  defp dispatch_call_delta(parser, %{"call_id" => id, "name" => name, "delta" => delta})
       when is_binary(id) and id != "" and is_binary(delta) and
              name in ["read_file", "run_command"] do
    case Map.get(parser.call_map, id) do
      nil -> add_call(parser, id, name, delta)
      %{name: ^name} = call -> extend_call(parser, id, call, delta)
      _ -> %{parser | invalid: true}
    end
  end

  defp dispatch_call_delta(parser, _event), do: %{parser | invalid: true}

  defp add_call(parser, id, name, delta) do
    call = %{id: id, name: name, arguments: delta}
    %{parser | calls: parser.calls ++ [call], call_map: Map.put(parser.call_map, id, call)}
  end

  defp extend_call(parser, id, call, delta) do
    updated = %{call | arguments: call.arguments <> delta}
    calls = Enum.map(parser.calls, &replace_call(&1, id, updated))
    %{parser | calls: calls, call_map: Map.put(parser.call_map, id, updated)}
  end

  defp replace_call(%{id: call_id}, id, replacement) when call_id == id, do: replacement
  defp replace_call(call, _id, _replacement), do: call

  defp dispatch_text_delta(parser, %{"delta" => delta})
       when is_binary(delta) and parser.calls == [] do
    %{parser | text: parser.text <> delta, saw_text: true}
  end

  defp dispatch_text_delta(parser, _event), do: %{parser | invalid: true}

  defp dispatch_completed(parser, %{"usage" => usage}) when is_map(usage) do
    if valid_usage?(usage, parser),
      do: record_usage(parser, usage),
      else: %{parser | invalid: true}
  end

  defp dispatch_completed(parser, _event), do: %{parser | invalid: true}

  defp valid_usage?(usage, parser) do
    details = Map.get(usage, "input_tokens_details")
    input = Map.get(usage, "input_tokens")
    output = Map.get(usage, "output_tokens")
    cached = if is_map(details), do: Map.get(details, "cached_tokens"), else: nil

    is_integer(input) and input >= 0 and is_integer(output) and output >= 0 and
      is_integer(cached) and cached >= 0 and not (parser.calls != [] and parser.saw_text)
  end

  defp record_usage(parser, usage) do
    details = Map.fetch!(usage, "input_tokens_details")

    %{
      parser
      | completed: true,
        usage: %{
          input_tokens: Map.fetch!(usage, "input_tokens"),
          output_tokens: Map.fetch!(usage, "output_tokens"),
          cached_tokens: Map.fetch!(details, "cached_tokens")
        }
    }
  end

  defp response_from(parser), do: %{text: parser.text, calls: parser.calls, usage: parser.usage}

  defp record_ok(records, record, run_started, response) do
    updated = %{
      record
      | outcome: "ok",
        usage: response.usage,
        end_ms: monotonic_ms() - run_started
    }

    case write_record(records, updated) do
      :ok -> {:ok, response}
      _ -> {:fatal, 1, "loop: cannot write records file"}
    end
  end

  defp finish_failure(records, record, run_started, outcome, kind) do
    updated = %{record | outcome: outcome, end_ms: monotonic_ms() - run_started}

    case write_record(records, updated) do
      :ok -> {:error, kind}
      _ -> {:fatal, 1, "loop: cannot write records file"}
    end
  end

  defp write_record(file, record) do
    case :file.write(file, encode_record(record) <> "\n") do
      :ok -> :file.sync(file)
      error -> error
    end
  end

  defp encode_record(record) do
    usage = record.usage

    "{\"start_ms\":#{json_integer(record.start_ms)}," <>
      "\"first_byte_ms\":#{json_integer(record.first_byte_ms)}," <>
      "\"end_ms\":#{json_integer(record.end_ms)}," <>
      "\"outcome\":#{Jason.encode!(record.outcome)}," <>
      "\"retries\":#{json_integer(record.retries)}," <>
      "\"usage\":{" <>
      "\"input_tokens\":#{json_integer(usage.input_tokens)}," <>
      "\"output_tokens\":#{json_integer(usage.output_tokens)}," <>
      "\"cached_tokens\":#{json_integer(usage.cached_tokens)}}," <>
      "\"request_bytes\":#{json_integer(record.request_bytes)}," <>
      "\"history_items\":#{json_integer(record.history_items)}}"
  end

  defp json_integer(nil), do: "null"
  defp json_integer(value) when is_integer(value), do: Integer.to_string(value)

  defp attempt_error(:timeout), do: {:error, 10, "loop: first-byte timeout"}
  defp attempt_error(:stall), do: {:error, 11, "loop: stream stalled"}
  defp attempt_error(:transport), do: {:error, 12, "loop: transport error"}
  defp attempt_error(:overload), do: {:error, 13, "loop: server overloaded"}
  defp attempt_error(:rejected), do: {:error, 14, "loop: server rejected request"}
  defp attempt_error(:invalid), do: {:error, 15, "loop: invalid response"}

  defp request_body(history) do
    ~s({"model":"fake-agent","stream":true,"tools":#{@tools},"tool_choice":"auto","input":#{history}})
  end

  defp execute_calls([], _workdir, outputs), do: {:ok, Enum.reverse(outputs)}

  defp execute_calls([call | rest], workdir, outputs) do
    with {:ok, arguments} <- compact_arguments(call.arguments),
         {:ok, output} <- execute_tool(call.name, arguments, workdir) do
      execute_calls(rest, workdir, [output | outputs])
    else
      _ -> {:error, 16, "loop: tool execution failed"}
    end
  end

  defp compact_arguments(raw) do
    with {:ok, decoded} when is_map(decoded) <- Jason.decode(raw),
         {:ok, compact} <- Jason.encode(decoded) do
      {:ok, compact}
    else
      _ -> :error
    end
  end

  defp execute_tool("read_file", raw, workdir) do
    with {:ok, %{"path" => path} = args}
         when map_size(args) == 1 and is_binary(path) and path != "" <- Jason.decode(raw),
         false <- Path.type(path) == :absolute,
         candidate = Path.join(workdir, path),
         {:ok, resolved} <- canonical_path(candidate),
         true <- under_workdir?(resolved, workdir),
         {:ok, %File.Stat{type: :regular}} <- File.stat(resolved),
         {:ok, content} <- File.read(resolved),
         true <- String.valid?(content) do
      {:ok, content}
    else
      _ -> :error
    end
  end

  defp execute_tool("run_command", raw, workdir) do
    with {:ok, %{"command" => command} = args}
         when map_size(args) == 1 and is_binary(command) and command != "" <- Jason.decode(raw),
         true <- command_paths_allowed?(command) do
      run_command(command, workdir)
    else
      _ -> :error
    end
  end

  defp execute_tool(_name, _raw, _workdir), do: :error

  defp under_workdir?(resolved, workdir) do
    relative = Path.relative_to(resolved, workdir)

    relative != ".." and not String.starts_with?(relative, "../") and
      not String.starts_with?(relative, "/")
  end

  defp command_paths_allowed?(command) do
    absolute = Regex.match?(~r/(^|[\s"'=<>|;&(])\/(?:[^\s"'<>|;&()]*)/u, command)
    parent = Regex.match?(~r/(^|[\s\/"'=<>|;&(])\.\.(?:\/|[\s"'<>|;&)]|$)/u, command)
    not absolute and not parent
  end

  defp run_command(command, workdir) do
    temp = Path.join(workdir, ".loop-stderr-#{System.unique_integer([:positive])}")
    script = ~S(exec 2> "$1"; exec /bin/sh -c "$2")

    args = [
      "-i",
      "PATH=/usr/bin:/bin",
      "HOME=#{workdir}",
      "LANG=C.UTF-8",
      "PWD=#{workdir}",
      "/bin/sh",
      "-c",
      script,
      "loop",
      temp,
      command
    ]

    task =
      Task.async(fn -> System.cmd("/usr/bin/env", args, cd: workdir, stderr_to_stdout: false) end)

    result =
      case Task.yield(task, 5000) do
        {:ok, command_result} ->
          {:ok, command_result}

        nil ->
          Task.shutdown(task, :brutal_kill)
          :error
      end

    stderr = File.read(temp)
    File.rm(temp)

    with {:ok, {stdout, status}} <- result,
         {:ok, stderr} <- stderr,
         true <- byte_size(stdout) + byte_size(stderr) <= 1_048_576,
         true <- String.valid?(stdout) and String.valid?(stderr) do
      output =
        "{\"exit_code\":#{status},\"stdout\":#{Jason.encode!(stdout)},\"stderr\":#{Jason.encode!(stderr)}}"

      {:ok, output}
    else
      _ -> :error
    end
  end

  defp append_history(history, calls, outputs) do
    if length(calls) != length(outputs) do
      {:error, 15, "loop: invalid response"}
    else
      prefix = binary_part(history, 0, byte_size(history) - 1)

      items =
        Enum.zip(calls, outputs)
        |> Enum.map_join(fn {call, output} ->
          call_item = %{
            "type" => "function_call",
            "call_id" => call.id,
            "name" => call.name,
            "arguments" => call.arguments |> Jason.decode!() |> Jason.encode!()
          }

          output_item = %{
            "type" => "function_call_output",
            "call_id" => call.id,
            "output" => output
          }

          "," <> Jason.encode!(call_item) <> "," <> Jason.encode!(output_item)
        end)

      {:ok, prefix <> items <> "]"}
    end
  end

  defp canonical_path(""), do: {:error, :enoent}

  defp canonical_path(path) do
    absolute =
      if Path.type(path) == :absolute do
        path
      else
        case File.cwd() do
          {:ok, cwd} -> Path.join(cwd, path)
          error -> error
        end
      end

    case absolute do
      path when is_binary(path) ->
        resolve_path_components("/", String.split(path, "/", trim: true))

      error ->
        error
    end
  end

  defp resolve_path_components(current, []), do: {:ok, current}
  defp resolve_path_components(current, ["." | rest]), do: resolve_path_components(current, rest)

  defp resolve_path_components(current, [".." | rest]),
    do: resolve_path_components(Path.dirname(current), rest)

  defp resolve_path_components(current, [part | rest]) do
    candidate = if current == "/", do: "/" <> part, else: Path.join(current, part)

    case :file.read_link_all(String.to_charlist(candidate)) do
      {:ok, resolved} ->
        target = List.to_string(resolved) |> Path.expand()
        resolve_path_components(target, rest)

      {:error, :einval} ->
        case File.stat(candidate) do
          {:ok, _stat} -> resolve_path_components(candidate, rest)
          error -> error
        end

      error ->
        error
    end
  end

  defp monotonic_ms, do: System.monotonic_time(:millisecond)

  defp header_value(headers, name), do: Map.get(headers, name)
end
