defmodule Beltway.Ingest.PipelineTest do
  use ExUnit.Case, async: false

  alias Beltway.Ingest.{Buffer, Parser, Sink}

  setup do
    {:ok, sup} = start_supervised({Beltway.Ingest.Supervisor, collector: self()})
    %{sup: sup}
  end

  test "parsed lines reach the buffer and the sink" do
    assert :ok = Parser.push("a=1,b=2")
    assert {:error, :bad_line} = Parser.push("nonsense")
    assert Buffer.items() == [%{"a" => "1", "b" => "2"}]
    assert Sink.flush() == 1
    assert_receive {:flushed, [%{"a" => "1", "b" => "2"}]}
    assert Buffer.items() == []
  end
end
