# Trusted completion marker is emitted only after ExUnit actually runs.
[nonce, stage] = System.argv()
ExUnit.start(autorun: false)
if File.exists?("test/test_helper.exs"), do: Code.require_file("test/test_helper.exs")
Path.wildcard("test/**/*_test.exs") |> Enum.each(&Code.require_file/1)
result = ExUnit.run()
IO.puts("FV_TEST_COMPLETE " <> nonce <> " " <> stage)
System.halt(if result.failures == 0, do: 0, else: 1)
