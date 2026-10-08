# Task 3 — SSE model client

Implement an executable named `kogen` with exactly this command:

```
kogen model --url URL --prompt TEXT --idle-timeout-ms N --usage-file PATH
```

The five options may appear in any order after `model`. Each must appear exactly once and have one following argument. There are no positional arguments. `URL` must be an absolute `http://` URL with a host; `TEXT` and `PATH` may be empty only for TEXT (PATH must not be empty); `N` is ASCII decimal digits representing an integer from 1 through 60000. Unknown, duplicate, missing, malformed, or extra arguments print exactly `error: invalid arguments\n` to stderr, nothing to stdout, and exit 2. No request is made on argument error.

POST to URL once per attempt. The UTF-8 request body is compact JSON with exactly one key, `prompt`, whose value is TEXT (for example `{"prompt":"hi"}`). Send exactly `Content-Type: application/json` and `Accept: text/event-stream`. Do not make any other network requests. The suite supplies a local HTTP server. A request attempt fails with a retryable connection failure if connecting, sending, or receiving fails. Each attempt has an idle timeout of N milliseconds, measured from the start of the attempt until the first response byte and reset after every subsequent response byte; if that interval elapses, close the attempt and treat it as retryable. Retry exactly once after a retryable connection failure, idle timeout, or HTTP status from 500 through 599. The second attempt is final. A retry sends the identical method, URL, body, and headers. Do not retry any other HTTP status or any malformed response.

A successful status is any 2xx. Parse its body as strict UTF-8 Server-Sent Events. LF and CRLF are line endings. An event record ends only at an empty line; EOF does not terminate a pending record. Ignore comment lines whose first character is `:` and ignore empty lines. For each `data:` line, remove the prefix and at most one following ASCII space; preserve all remaining characters. Join multiple data values in the record with LF. Ignore other field lines. A record without any `data:` line is ignored. A record with data exactly `[DONE]` ends parsing immediately; bytes after it are ignored. For any other data, parse one JSON value and require it to be an object. An object with `type` equal to `text` must have a string `text` value, which is appended verbatim. An object with `type` equal to `usage` must have nonnegative JSON integers `input_tokens` and `output_tokens`, each no greater than 9007199254740991 (booleans, decimal fractions, and exponent notation are not integers); it replaces the prior usage record. Other object types are ignored. JSON errors, non-object JSON, invalid text or usage fields, invalid UTF-8, a non-2xx response other than 5xx, missing `[DONE]`, or missing valid usage are non-retriable failures.

On success, write all appended text concatenated, followed by one LF, to stdout; write nothing to stderr. Atomically replace PATH with UTF-8 bytes for one compact JSON object in this exact key order, followed by LF: `{"input_tokens":I,"output_tokens":O}\n`. Preserve an existing PATH file unchanged unless the full request succeeds. Return 0.

After all retryable attempts fail, or for any non-retriable failure, print exactly `error: request failed\n` to stderr, nothing to stdout, leave PATH unchanged, and return 5. The usage record is a regular file path; create parent directories as needed. The program must not access external network services.

Stack: X.
Build: Y.
Checks: `make check` runs Z.
Stack: Go.
Build: `make build` produces `build/bin/kogen`.
Checks: `make check` runs recursive `gofmt`, `go vet`, `golangci-lint`, and `go test`.
