defmodule Kogen.MixProject do
  use Mix.Project

  def project do
    [
      app: :kogen,
      version: "0.1.0",
      elixir: "~> 1.20",
      escript: [main_module: Kogen.CLI, path: "build/bin/kogen"],
      deps: []
    ]
  end

  def application, do: [extra_applications: [:logger]]
end
