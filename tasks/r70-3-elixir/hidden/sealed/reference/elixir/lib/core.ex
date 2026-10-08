defmodule Kogen.Core do
  @moduledoc "SSE model client implementation."

  @spec execute([String.t()]) :: String.t()
  def execute(args) do
    opts = parse(args) || Kogen.Input.fail("error: invalid arguments", 2)

    try do
      {text, usage} = request(opts)
      atomic_usage(opts.usage, usage)
      text <> "\n"
    rescue
      _error ->
        Kogen.Input.fail("error: request failed", 5)
    catch
      _kind, _reason ->
        Kogen.Input.fail("error: request failed", 5)
    end
  end

  defp parse(["model" | args]) when length(args) == 8 do
    with {:ok, values} <- option_values(args),
         {:ok, opts} <- build_options(values) do
      opts
    else
      _ -> nil
    end
  end

  defp parse(_), do: nil

  defp option_values(args) do
    pairs = Enum.chunk_every(args, 2)
    allowed = ["--url", "--prompt", "--idle-timeout-ms", "--usage-file"]
    names = Enum.map(pairs, &hd/1)

    if Enum.all?(names, &(&1 in allowed)) and length(Enum.uniq(names)) == 4 do
      {:ok, Map.new(pairs, fn [key, value] -> {key, value} end)}
    else
      :error
    end
  end

  defp build_options(values) do
    timeout = values["--idle-timeout-ms"]
    uri = URI.parse(values["--url"])

    valid_timeout =
      Regex.match?(~r/^[0-9]+$/, timeout) and String.to_integer(timeout) in 1..60_000

    valid_url = uri.scheme == "http" and is_binary(uri.host) and uri.host != ""

    if valid_timeout and valid_url and values["--usage-file"] != "" do
      {:ok,
       %{
         url: values["--url"],
         prompt: values["--prompt"],
         timeout: String.to_integer(timeout),
         usage: values["--usage-file"]
       }}
    else
      :error
    end
  end

  defp request(opts) do
    Application.ensure_all_started(:inets)
    body = Jason.encode!(%{"prompt" => opts.prompt})
    attempt(opts, body, 0)
  end

  defp attempt(opts, body, attempt_no) do
    headers = [{~c"Content-Type", ~c"application/json"}, {~c"Accept", ~c"text/event-stream"}]
    req = {String.to_charlist(opts.url), headers, ~c"application/json", body}

    case :httpc.request(
           :post,
           req,
           [timeout: :infinity, connect_timeout: opts.timeout, autoredirect: false],
           sync: false,
           stream: :self
         ) do
      {:ok, request_id} -> await_response(request_id, opts, body, attempt_no)
      {:error, _reason} -> retry(opts, body, attempt_no)
    end
  end

  defp await_response(request_id, opts, body, attempt_no) do
    receive do
      {:http, {^request_id, :stream_start, _headers}} ->
        case receive_body(request_id, opts.timeout, []) do
          {:ok, response} -> parse_sse(response)
          {:retryable, _reason} -> retry(opts, body, attempt_no)
        end

      {:http, {^request_id, {{_version, status, _reason}, _headers, response}}}
      when status in 200..299 ->
        parse_sse(response)

      {:http, {^request_id, {{_version, status, _reason}, _headers, _response}}}
      when status in 500..599 ->
        retry(opts, body, attempt_no)

      {:http, {^request_id, {:error, _reason}}} ->
        retry(opts, body, attempt_no)

      {:http, {^request_id, _response}} ->
        raise "http status"
    after
      opts.timeout ->
        :httpc.cancel_request(request_id)
        retry(opts, body, attempt_no)
    end
  end

  defp receive_body(request_id, timeout, chunks) do
    receive do
      {:http, {^request_id, :stream, chunk}} ->
        receive_body(request_id, timeout, [chunk | chunks])

      {:http, {^request_id, :stream_end, _headers}} ->
        {:ok, IO.iodata_to_binary(Enum.reverse(chunks))}

      {:http, {^request_id, {:error, reason}}} ->
        {:retryable, reason}
    after
      timeout ->
        :httpc.cancel_request(request_id)
        {:retryable, :idle_timeout}
    end
  end

  defp retry(opts, body, 0), do: attempt(opts, body, 1)
  defp retry(_opts, _body, _attempt_no), do: raise("request failed")

  defp parse_sse(bytes) do
    unless String.valid?(bytes), do: raise("bad utf8")

    {text, usage, done, _fields} =
      Enum.reduce_while(String.split(bytes, "\n"), {"", nil, false, []}, &reduce_line/2)

    if done and not is_nil(usage), do: {text, usage}, else: raise("incomplete stream")
  end

  defp reduce_line(raw, state) do
    line = String.replace_suffix(raw, "\r", "")
    reduce_sse_line(line, state)
  end

  defp reduce_sse_line("", {text, usage, false, fields}) when fields != [] do
    process_record(Enum.join(Enum.reverse(fields), "\n"), {text, usage, false, []})
  end

  defp reduce_sse_line("", {text, usage, done, _fields}), do: {:cont, {text, usage, done, []}}
  defp reduce_sse_line(<<":", _rest::binary>>, state), do: {:cont, state}

  defp reduce_sse_line(<<"data:", value::binary>>, {text, usage, done, fields}) do
    value = String.replace_prefix(value, " ", "")
    {:cont, {text, usage, done, [value | fields]}}
  end

  defp reduce_sse_line(_line, state), do: {:cont, state}

  defp process_record("[DONE]", {text, usage, _done, _fields}),
    do: {:halt, {text, usage, true, []}}

  defp process_record(data, state) do
    data |> decode_event() |> apply_event(state)
  end

  defp decode_event(data) do
    push = fn key, value, acc -> [{key, value} | acc] end
    finish = fn pairs, acc -> {Map.new(Enum.reverse(pairs)), acc} end
    {event, _acc, <<>>} = :json.decode(data, nil, %{object_push: push, object_finish: finish})
    unless is_map(event), do: raise("bad event")
    event
  end

  defp apply_event(%{"type" => "text", "text" => text}, {out, usage, done, _fields})
       when is_binary(text),
       do: {:cont, {out <> text, usage, done, []}}

  defp apply_event(%{"type" => "text"}, _state), do: raise("bad text")

  defp apply_event(
         %{"type" => "usage", "input_tokens" => input, "output_tokens" => output},
         {text, _usage, done, _fields}
       ) do
    if valid_count?(input) and valid_count?(output) do
      {:cont,
       {text, %{"input_tokens" => trunc(input), "output_tokens" => trunc(output)}, done, []}}
    else
      raise "bad usage"
    end
  end

  defp apply_event(%{"type" => "usage"}, _state), do: raise("bad usage")
  defp apply_event(_event, {text, usage, done, _fields}), do: {:cont, {text, usage, done, []}}

  defp valid_count?(value) when is_integer(value),
    do: value >= 0 and value <= 9_007_199_254_740_991

  defp valid_count?(value) when is_float(value),
    do: value >= 0 and value <= 9_007_199_254_740_991 and trunc(value) == value

  defp valid_count?(_value), do: false

  defp atomic_usage(path, usage) do
    parent = Path.dirname(path)
    File.mkdir_p!(parent)
    temp = Path.join(parent, ".kogen-usage-#{System.unique_integer([:positive])}")

    bytes =
      "{\"input_tokens\":#{usage["input_tokens"]},\"output_tokens\":#{usage["output_tokens"]}}\n"

    File.write!(temp, bytes, [:binary, :exclusive])
    File.rename!(temp, path)
  end
end
