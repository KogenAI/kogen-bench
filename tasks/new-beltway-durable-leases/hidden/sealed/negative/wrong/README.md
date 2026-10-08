# Beltway

A small toolkit of pipeline building blocks (rate limiting, ingestion, fan-out,
queues, caching, command running, log analysis, reporting, retries) with a
`beltway` command line tool. Plain Elixir, no web framework.

    mix test
    mix escript.build && ./beltway count app.log

Log lines look like `2026-03-01T10:00:00Z ERROR api Something failed`.
