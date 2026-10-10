#!/bin/bash
# probe-toolchains.sh — hello project per language: build + test + lint/format, offline (network-disabling env), with the race env and caps
H=$(cd "$(dirname "$0")" && pwd); source $H/env.sh 2>/dev/null || source $H/env-studio.sh
export CARGO_NET_OFFLINE=true GOPROXY=off GOFLAGS="$GOFLAGS -mod=mod" HEX_OFFLINE=1 BUN_CONFIG_NO_INSTALL=1
T=$(mktemp -d /tmp/r3probe.XXXX); res() { printf '%-6s %-22s %s\n' "$1" "$2" "$3"; }
step() { local lang=$1 name=$2; shift 2; local log="$T/$lang-${name//[^A-Za-z0-9]/_}.log"; if ( "$@" ) > "$log" 2>&1; then res $lang "$name" PASS; else res $lang "$name" "FAIL (see $log)"; fi; }
# Rust
cd $T && cargo new -q --lib rhello >/dev/null 2>&1 && cd rhello && printf 'pub fn hello() -> &%sstatic str { "hello" }\n#[cfg(test)]\nmod tests { #[test] fn t() { assert_eq!(super::hello(), "hello"); } }\n' "'" > src/lib.rs
step rust "cargo test" cargo test --offline -q; step rust "cargo clippy -D warn" cargo clippy --offline --all-targets -q -- -D warnings; step rust "cargo fmt --check" cargo fmt --check
# Go
mkdir -p $T/ghello && cd $T/ghello && printf 'module ghello\n\ngo 1.27\n' > go.mod && printf 'package ghello\n\nfunc Hello() string { return "hello" }\n' > h.go && printf 'package ghello\n\nimport "testing"\n\nfunc TestHello(t *testing.T) {\n\tif Hello() != "hello" {\n\t\tt.Fatal("bad")\n\t}\n}\n' > h_test.go
step go "go test" go test ./...; step go "go vet" go vet ./...; step go "gofmt -l (empty)" sh -c '[ -z "$(gofmt -l .)" ]'
# TypeScript / Bun
mkdir -p $T/thello && cd $T/thello && printf 'export const hello = (): string => "hello";\n' > h.ts && printf 'import { test, expect } from "bun:test";\nimport { hello } from "./h";\ntest("h", () => { expect(hello()).toBe("hello"); });\n' > h.test.ts && printf '{"compilerOptions":{"strict":true,"noEmit":true,"module":"esnext","target":"es2022","moduleResolution":"bundler","types":[]},"files":["h.ts"]}\n' > tsconfig.json
step ts "bun test" bun test; step ts "tsc --strict" sh -c "$( [ -x ~/bench-toolchains/bin/tsc ] && echo ~/bench-toolchains/bin/tsc || echo tsc) -p tsconfig.json"
# Gleam (offline template with pre-fetched packages)
cp -c -R $H/gleam-template $T/glhello && cd $T/glhello && step gleam "gleam build" gleam build; step gleam "gleam test" gleam test; step gleam "gleam format --check" gleam format --check src test
# Elixir
cd $T && mix new exhello >/dev/null 2>&1 && cd exhello && step ex "mix test" mix test; step ex "mix format --check" mix format --check-formatted; step ex "mix compile --warn-as-err" mix compile --warnings-as-errors --force
echo "versions: $(rustc --version | cut -d' ' -f2) go$(go version | grep -o '1\.[0-9.]*') bun$(bun --version) gleam$(gleam --version | cut -d' ' -f2) elixir$(elixir --version | tail -1 | cut -d' ' -f2) otp$(erl -noshell -eval 'io:format("~s",[erlang:system_info(otp_release)]),halt().')"
