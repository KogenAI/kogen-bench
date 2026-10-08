defmodule Beltway.LogReaderTest do
  use ExUnit.Case, async: true

  alias Beltway.LogReader

  @moduletag :tmp_dir

  test "summarizes a file", %{tmp_dir: dir} do
    path = Path.join(dir, "a.log")

    File.write!(path, """
    2026-03-01T10:00:05Z ERROR api boom
    2026-03-01T10:00:01Z INFO web ok
    """)

    summary = LogReader.summarize(path)
    assert summary.lines == 2
    assert summary.entries == 2
    assert summary.by_level == %{"ERROR" => 1, "INFO" => 1}
    assert summary.first_ts == ~U[2026-03-01 10:00:01Z]
    assert summary.last_ts == ~U[2026-03-01 10:00:05Z]
  end
end
