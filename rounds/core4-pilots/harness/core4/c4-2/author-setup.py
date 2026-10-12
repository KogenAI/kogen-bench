from pathlib import Path
import shutil

root=Path('.')
for lang in ['rust','go','ts-bun']:
    base=root/'bases'/lang
    base.mkdir(parents=True,exist_ok=True)
    src=root/'scratch'/lang
    for name in (['.cargo/config.toml'] if lang=='rust' else ['.golangci.yml'] if lang=='go' else ['setup.sh','toolchain-env.sh','tsconfig.json','biome.json','bun.lock','package.json']):
        target=base/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src/name,target)
    (base/'.gitignore').write_text('/bin/\n/target/\n/.cache/\n/node_modules/\n')
    (base/'README.md').write_text('''# Durable queue starter

Implement the supplied task contract in this language. The starter deliberately
returns NOT_IMPLEMENTED (exit 70) for every command.

Run `make build` offline, then `./bin/app stats --state ./state`.
`make check` runs the pinned formatting, static-analysis and unit-test tools.
`make test` runs the public unit tests. Runtime files belong under --state.
The toolchains and dependency caches are supplied by the execution environment.
''')
    make=(src/'Makefile').read_text()
    make=make[:make.index('.PHONY:')]
    if lang=='rust':
        make+='''.PHONY: build check test format
build:
\tcargo build --offline --release
\tmkdir -p bin
\tcp target/release/app bin/app
check:
\tcargo fmt --check
\tcargo clippy --offline --all-targets -- -D warnings
\tcargo test --offline
test:
\tcargo test --offline
format:
\tcargo fmt
'''
        (base/'Cargo.toml').write_text('''[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
serde = { version = "1.0.228", features = ["derive"] }
serde_json = "1.0.145"
libc = "0.2"
''')
        (base/'src').mkdir()
        (base/'src/main.rs').write_text('''mod timing;
fn main() {
    eprintln!("{{\\"error\\":{{\\"code\\":\\"NOT_IMPLEMENTED\\",\\"message\\":\\"implement the queue\\"}}}}");
    std::process::exit(70);
}
''')
        (base/'src/timing.rs').write_text('''#[allow(dead_code)]
pub fn retry_delay(attempt: u32) -> i64 {
    (100_i64 << (attempt - 1)).min(10000)
}
#[cfg(test)]
mod tests {
    use super::retry_delay;
    #[test]
    fn first_retry() { assert_eq!(retry_delay(1), 100); }
    #[test]
    fn exponential_retry() { assert_eq!(retry_delay(3), 400); }
    #[test]
    fn capped_retry() { assert_eq!(retry_delay(16), 10000); }
}
''')
    elif lang=='go':
        make+='''.PHONY: build check test format
build:
\tmkdir -p bin
\tgo build -trimpath -o bin/app .
check:
\ttest -z "$$(gofmt -l .)"
\tgo vet ./...
\tgolangci-lint run
\tgo test ./...
test:
\tgo test ./...
format:
\tgofmt -w .
'''
        (base/'go.mod').write_text('module durablequeue\n\ngo 1.27.1\n')
        (base/'main.go').write_text('''package main
import ("fmt"; "os")
func main() {
    fmt.Fprintln(os.Stderr, `{"error":{"code":"NOT_IMPLEMENTED","message":"implement the queue"}}`)
    os.Exit(70)
}
''')
        (base/'timing.go').write_text('''package main
func retryDelay(attempt int) int64 {
    delay := int64(100) << (attempt - 1)
    if delay > 10000 { return 10000 }
    return delay
}
''')
        (base/'timing_test.go').write_text('''package main
import "testing"
func TestFirstRetry(t *testing.T) { if retryDelay(1) != 100 { t.Fatal("first retry") } }
func TestExponentialRetry(t *testing.T) { if retryDelay(3) != 400 { t.Fatal("exponential retry") } }
func TestCappedRetry(t *testing.T) { if retryDelay(16) != 10000 { t.Fatal("capped retry") } }
''')
    else:
        make+='''.PHONY: setup build check test format
setup:
\t./setup.sh
build: setup
\tmkdir -p bin
\tbun build --compile --outfile bin/app src/main.ts
check: setup
\tbun ./node_modules/typescript/bin/tsc --noEmit
\tbun ./node_modules/@biomejs/biome/bin/biome check .
\tbun test
test: setup
\tbun test
format: setup
\tbun ./node_modules/@biomejs/biome/bin/biome check --write .
'''
        text=(base/'package.json').read_text().replace('"kogen"','"durablequeue"')
        (base/'package.json').write_text(text)
        (base/'src').mkdir()
        (base/'test').mkdir()
        (base/'src/main.ts').write_text('''console.error(JSON.stringify({ error: { code: 'NOT_IMPLEMENTED', message: 'implement the queue' } }));
process.exit(70);
''')
        (base/'src/timing.ts').write_text('''export function retryDelay(attempt: number): number {
  return Math.min(100 * 2 ** (attempt - 1), 10000);
}
''')
        (base/'test/timing.test.ts').write_text('''import { expect, test } from 'bun:test';
import { retryDelay } from '../src/timing';
test('first retry', () => expect(retryDelay(1)).toBe(100));
test('exponential retry', () => expect(retryDelay(3)).toBe(400));
test('capped retry', () => expect(retryDelay(16)).toBe(10000));
''')
    (base/'Makefile').write_text(make)
    ref=root/'reference'/lang
    shutil.copytree(base,ref,dirs_exist_ok=True)
    stack={'rust':('Rust','cargo fmt --check, cargo clippy --all-targets -- -D warnings, cargo test'), 'go':('Go','gofmt, go vet, golangci-lint, go test'), 'ts-bun':('TypeScript/Bun','tsc --noEmit, biome check, bun test')}[lang]
    (root/f'prompt-{lang}.md').write_text((root/'SPEC.md').read_text()+f'\nStack and checks: {stack[0]}; build with `make build`.\n`make check` runs {stack[1]}; `make test` runs public tests.\n')
