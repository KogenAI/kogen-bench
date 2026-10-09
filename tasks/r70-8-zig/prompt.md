# Agent loop CLI

Implement `loop`, a command-line agent loop client. It talks only to the deterministic local fake server described below. `make build` must create the executable used by `./run`; `./run` forwards arguments and streams output without building. `make check` runs the pinned stack checks. Setup, builds and checks work offline. The skeleton includes no protocol or tool helpers.

## Command line

The accepted form is:

```text
loop run --prompt-file <path> --server <url> --records <path> [--workdir <dir>] [--session <id>] [--first-byte-timeout-ms <ms>] [--idle-timeout-ms <ms>] [--max-retries <n>] [--backoff-ms <ms>]
```

Every option takes one separate value. Required options are `--prompt-file`, `--server` and `--records`. Options may appear in any order after `run`, but each may appear once. No other command, positional argument or option is accepted. A URL is an `http://` origin with an optional trailing slash and no path, query or fragment. The request endpoint is that origin plus `/v1/responses`.

Defaults are: `--workdir` is the current directory; `--first-byte-timeout-ms` is 5000; `--idle-timeout-ms` is 3000; `--max-retries` is 2; and `--backoff-ms` is 50. Timeout values are decimal integers from 1 through 60000 inclusive. Retries are from 0 through 5 inclusive. Backoff is from 0 through 5000 inclusive. `--session` is 1–128 ASCII letters, digits, `.`, `_`, `:`, or `-`. Without it, generate one nonempty ID once for the process. Keep the ID unchanged for every request in that conversation; separate concurrent invocations generate different IDs.

Invalid command lines exit 2, write exactly `loop: invalid command line\n` to stderr, and write nothing to stdout. Prompt read errors exit 1 with `loop: cannot read prompt file\n`. A missing or non-directory workdir exits 1 with `loop: invalid workdir\n`. Failure to create or write the records file exits 1 with `loop: cannot write records file\n`. These failures write no records unless a request has already been made.

## Request and append-only history

For each model turn, send one UTF-8 JSON POST to `/v1/responses`, with headers `Content-Type: application/json`, `Accept: text/event-stream` and `X-Session-ID: <session>`. Do not send authorization headers. The JSON object has these fields:

```json
{
  "model": "fake-agent",
  "stream": true,
  "tools": [
    {"type":"function","name":"read_file","description":"Read a UTF-8 file under the workdir","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"],"additionalProperties":false}},
    {"type":"function","name":"run_command","description":"Run a shell command with the workdir as its current directory","parameters":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"],"additionalProperties":false}}
  ],
  "tool_choice": "auto",
  "input": []
}
```

The first `input` item is `{"role":"user","content":[{"type":"input_text","text":"<exact prompt-file contents>"}]}`. For each completed tool call, append an assistant item `{"type":"function_call","call_id":"<id>","name":"<name>","arguments":"<compact JSON arguments>"}` and then its result item `{"type":"function_call_output","call_id":"<same id>","output":"<result>"}`. Keep items in call order. Never replace or edit an earlier item. Request n+1's serialized `input` array, through the last byte before its closing `]`, must equal request n's serialized `input` array through the last byte before its closing `]`; n+1 appends new items after that prefix.

A model response with one or more function calls causes all calls to execute in emitted order and the next request to include their call/result pairs. A response with no calls is final: concatenate all `response.output_text.delta` values and write the resulting UTF-8 bytes to stdout exactly, with no added newline. A response may not mix function calls and output-text deltas. Stop after the final response. Do not make an extra request.

`read_file` takes `{"path":"relative/path"}`. The path must be relative, must resolve beneath the canonical workdir (including symlinks), and must identify a regular UTF-8 file. Its result is the exact decoded file contents. Absolute paths, traversal outside the workdir, missing files, directories and non-UTF-8 files are tool failures.

`run_command` takes `{"command":"..."}`. Run it with `/bin/sh -c` and the canonical workdir as its current directory, environment `PATH=/usr/bin:/bin`, `HOME=<workdir>`, `LANG=C.UTF-8`, and `PWD=<workdir>`. Capture stdout and stderr as UTF-8. The result is compact JSON with fields in this order: `exit_code`, `stdout`, `stderr`. The command must operate on workdir files using relative paths; reject a command that names an absolute filesystem path or a `..` path component. The command has a 5-second limit. A nonzero command exit is still a tool result. Tool results are strings in the `function_call_output` item. Any invalid call, denied path, failed command start, timeout, oversized output (over 1 MiB combined), or non-UTF-8 output exits 16 with exactly `loop: tool execution failed\n` on stderr and empty stdout; do not send another request after a tool failure.

## Fake server SSE protocol

The server responds with HTTP status 200 and `Content-Type: text/event-stream`. It sends `Connection: close` and closes the connection after `response.completed`; successful SSE bodies are close-delimited (no `Content-Length` or `Transfer-Encoding`). Error statuses use an empty body and `Content-Length: 0`. Each SSE frame is UTF-8 `event: <name>\ndata: <one-line JSON>\n\n`; LF or CRLF line endings are accepted. Lines beginning `:` are comments/keepalives and are ignored by the event parser, but every received body byte, including comment bytes, counts for timeout handling and resets the idle timer. A blank line ends a frame. Unknown event names, malformed JSON, missing fields, inconsistent call IDs/names, missing `response.completed`, or invalid event order are an invalid response.

Supported events are:

* `response.function_call_arguments.delta`: `{"call_id":"<nonempty id>","name":"read_file|run_command","delta":"<string>"}`. Accumulate `delta` strings by call ID in first-seen order. Repeated deltas for one call use the same name. The concatenated arguments must be a JSON object valid for that tool.
* `response.output_text.delta`: `{"delta":"<string>"}`. Append deltas in order.
* `response.completed`: `{"usage":{"input_tokens":<integer>,"output_tokens":<integer>,"input_tokens_details":{"cached_tokens":<integer>}}}`. This ends the response. Usage numbers are copied into the request record as `input_tokens`, `output_tokens` and `cached_tokens`.

A response must contain exactly one `response.completed`. Function-call deltas and output-text deltas cannot both appear in one response. Calls are complete when `response.completed` arrives. A successful response with no calls is the final answer, including an empty answer.

## Timeouts, retries and HTTP errors

The first-byte timer starts immediately before each HTTP request and measures until the first response-body byte. If none arrives in time, the attempt outcome is `timeout`. After the first body byte, start the idle timer; every later body byte resets it, whether it belongs to an SSE field, a newline, or a comment. Expiry before `response.completed` is a `stall`. A body EOF before completion is a transport failure. A connection error is a transport failure. HTTP 5xx, 429 and 529 are overload failures. Other non-200 statuses are rejected-request failures.

Retry `timeout`, `stall`, `transport` and `overload` attempts until `max-retries` retries have occurred. Before retry number k (k starts at 1), sleep `backoff-ms * 2^(k-1)` milliseconds. Retries reuse the exact request body and session ID. Do not retry a rejected status, invalid response or tool failure. After exhausting retries, exit 10 with `loop: first-byte timeout\n` for timeout, 11 with `loop: stream stalled\n` for stall, 12 with `loop: transport error\n` for transport, or 13 with `loop: server overloaded\n` for overload. A rejected status exits 14 with `loop: server rejected request\n`. An invalid SSE/response exits 15 with `loop: invalid response\n`. These failures write nothing to stdout.

## Request records

Truncate/create the records file at the start of a valid run. Write and flush one JSON object plus LF for each HTTP request attempt, including retries. Each object has exactly these fields:

```json
{"start_ms":0,"first_byte_ms":null,"end_ms":1,"outcome":"timeout","retries":0,"usage":{"input_tokens":null,"output_tokens":null,"cached_tokens":null},"request_bytes":123,"history_items":1}
```

Times are integer monotonic milliseconds elapsed since the process run began. `first_byte_ms` is null if no response-body byte arrived, otherwise the elapsed time when the first body byte arrived. `outcome` is exactly `ok`, `stall`, `timeout`, `transport` or `overload`; a response is `ok` only after a valid `response.completed`. `retries` is the zero-based retry index for this HTTP attempt. Usage values are null until reported by `response.completed`. `request_bytes` is the exact UTF-8 HTTP JSON body byte length. `history_items` is the number of objects in the request's `input` array. Record a failed attempt before sleeping or exiting. A rejected HTTP status and malformed response use outcome `transport`. A valid response that later fails in a local tool has outcome `ok`.

Stack: Zig 0.17.0.
Build: `make build`.
Checks: `make check` runs zig fmt --check, an offline Zig build, and zig test.
