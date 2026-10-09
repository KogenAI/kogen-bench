defmodule R70ElixirCache.MixProject do
  use Mix.Project
  def project, do: [app: :r70_elixir_cache, version: "0.1.0", elixir: "~> 1.20", deps: deps()]
  def application, do: [extra_applications: [:logger]]
  defp deps, do: [{:credo, "== 1.7.19", only: [:dev, :test], runtime: false}, {:dialyxir, "== 1.4.8", only: [:dev, :test], runtime: false}, {:jason, "== 1.4.5"}]
end
