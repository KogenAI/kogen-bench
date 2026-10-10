Code.require_file("frontend.exs", __DIR__)
try do
  case System.argv() do
    [app, output] ->
      ir = FV.Frontend.app(app)
      File.mkdir_p!(Path.dirname(output))
      File.write!(output, FV.Frontend.json(ir) <> "\n")
      IO.puts("FV-FRONTEND translated #{length(ir.modules)} module(s)")
    _ -> IO.puts(:stderr, "usage: elixir main.exs APP_DIR OUTPUT.json"); System.halt(2)
  end
rescue
  e -> IO.puts(:stderr, Exception.message(e)); System.halt(2)
end
