defmodule Kogen.MixProject do
  use Mix.Project

  def project do
    [
      app: :kogen,
      version: "0.1.0",
      elixir: "~> 1.20",
      escript: [main_module: Kogen.CLI, path: "build/bin/kogen"],
      dialyzer: [plt_file: {:no_warn, ".r70/deps.plt"}, plt_add_apps: [:inets]],
      deps: deps()
    ]
  end

  def application, do: [extra_applications: [:logger]]

  defp deps do
    [
      {:credo, "== 1.7.19", only: [:dev, :test], runtime: false},
      {:dialyxir, "== 1.4.8", only: [:dev, :test], runtime: false},
      {:jason, "== 1.4.5"}
    ]
  end
end
