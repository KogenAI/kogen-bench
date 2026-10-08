defmodule Beltway.ReportTest do
  use ExUnit.Case, async: true

  alias Beltway.Report

  @report %{title: "Errors", columns: ["service", "count"], rows: [["api", 3], ["web", nil]]}

  test "text" do
    assert Report.render(@report, :text) ==
             "Errors\n======\n\nservice  count\n-------  -----\napi          3\nweb      -\n"
  end

  test "csv" do
    assert Report.render(@report, :csv) == "service,count\r\napi,3\r\nweb,\r\n"
  end

  test "json" do
    assert JSON.decode!(Report.render(@report, :json)) ==
             %{"title" => "Errors", "rows" => [%{"service" => "api", "count" => 3}, %{"service" => "web", "count" => nil}]}
  end

  test "unknown format" do
    assert_raise ArgumentError, ~r/unknown format/, fn -> Report.render(@report, :xml) end
  end
end
