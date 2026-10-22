# kogen CLI

An Elixir Mix project with no Hex dependencies. `make build` compiles and creates the escript `build/bin/kogen`, which `./run` executes with its arguments and streams. `make check` runs the stack checks: `mix format --check-formatted` and `mix test`. Builds and checks work offline.
