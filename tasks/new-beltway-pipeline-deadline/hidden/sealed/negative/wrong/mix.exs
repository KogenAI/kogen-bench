defmodule Beltway.MixProject do
  use Mix.Project

  def project do
    [
      app: :beltway,
      version: "0.1.0",
      elixir: "~> 1.18",
      elixirc_paths: elixirc_paths(Mix.env()),
      start_permanent: Mix.env() == :prod,
      escript: [main_module: Beltway.CLI, name: "beltway"],
      deps: deps()
    ]
  end

  def application do
    [extra_applications: [:logger]]
  end

  defp elixirc_paths(:test), do: ["lib", "test/support"]
  defp elixirc_paths(_), do: ["lib"]

  defp deps do
    [
      {:telemetry, "~> 1.3"},
      {:stream_data, "~> 1.2", only: [:dev, :test]}
    ]
  end
end
