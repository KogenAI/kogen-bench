export PATH := /srv/bh/bench/toolchains/rust-1.97.1/bin:/opt/bench/cargo/bin:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/rust-1.97.1/bin:/opt/bench/cargo/bin
export LANG := C.UTF-8
export CARGO_HOME := /srv/bh/bench/toolchains/rust-1.97.1/cache/cargo-home
export CARGO_NET_OFFLINE := true
export RUSTUP_HOME := /opt/bench/rustup

.PHONY: build check format setup
setup:
	./setup.sh
build:
	cargo build --offline --release
	mkdir -p build/bin
	cp target/release/loop build/bin/loop
check:
	cargo fmt --check
	cargo clippy --offline --all-targets -- -D warnings
	cargo test --offline
format:
	cargo fmt
