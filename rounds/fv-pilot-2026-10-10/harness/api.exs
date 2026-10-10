# Compiles validated sources without Mix or candidate setup.
[nonce, module, required] = System.argv()
files = Path.wildcard("lib/**/*.ex")
case Kernel.ParallelCompiler.compile(files) do
  {:ok, _, _} -> :ok
  other -> IO.inspect(other); System.halt(2)
end
mod = String.to_existing_atom("Elixir." <> module)
wanted = String.split(required, ",") |> Enum.map(fn spec ->
  [name, arity] = String.split(spec, "/")
  {String.to_atom(name), String.to_integer(arity)}
end)
got = mod.__info__(:functions)
IO.inspect(got, label: "FV-API")
IO.puts("FV_API_COMPLETE " <> nonce)
System.halt(if Enum.all?(wanted, &(&1 in got)), do: 0, else: 1)
