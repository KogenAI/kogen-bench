//! Public regression tests (visible to contestants; restored before grading).
use std::process::Command;
use tally::agg::{Aggregator, word_counts};
use tally::config::parse_config;
use tally::counter::Registry;
use tally::parse::{Level, parse_line};
use tally::ring::RingBuf;
use tally::service::Service;
use tally::text::tokenize;

#[test]
fn parses_a_line() {
    let e = parse_line("2026-09-29T10:15:00Z WARN disk almost full\n").unwrap();
    assert_eq!(e.level, Level::Warn);
    assert_eq!(e.message, "disk almost full");
    assert_eq!(e.ts, "2026-09-29T10:15:00Z");
}

#[test]
fn rejects_garbage_lines() {
    assert!(parse_line("").is_none());
    assert!(parse_line("hello world").is_none());
    assert!(parse_line("2026-09-29T10:15:00Z LOUD boom").is_none());
    assert!(parse_line("2026-09-29T10:15:00Z INFO   ").is_none());
}

#[test]
fn long_ascii_messages_are_shortened() {
    let e = parse_line(&format!("2026-09-29T10:15:00Z INFO {}", "x".repeat(200))).unwrap();
    assert_eq!(e.message.len(), 80);
    assert!(e.message.ends_with("..."));
}

#[test]
fn config_parses() {
    let c = parse_config("# c\ntop = 5\nmin_level = warn # x\nwindow_secs=30\n").unwrap();
    assert_eq!((c.top, c.min_level, c.window_secs), (5, Level::Warn, 30));
    assert_eq!(parse_config("").unwrap().top, 10);
}

#[test]
fn config_unknown_key_is_an_error() {
    assert!(parse_config("bogus = 1").is_err());
}

#[test]
fn tokenizes_words() {
    let t = tokenize("Hello, wörld! it's_ok");
    let words: Vec<_> = t.iter().map(|t| &t.text[..]).collect();
    assert_eq!(words, ["Hello", "wörld", "it's_ok"]);
    assert_eq!(t[1].start, 7);
}

#[test]
fn aggregates_and_ranks() {
    let mut a = Aggregator::default();
    for k in ["b", "a", "b", "c", "a", "b"] {
        a.add(k);
    }
    assert_eq!(a.top(2), vec![("b".to_string(), 3), ("a".to_string(), 2)]);
    assert_eq!(a.count("c"), 1);
    assert_eq!(a.count("zzz"), 0);
    assert_eq!(word_counts("a b a").count("a"), 2);
}

#[test]
fn registry_single_thread() {
    let r = Registry::default();
    r.incr("x");
    r.incr("x");
    r.incr("y");
    assert_eq!(r.get("x"), 2);
    assert_eq!(r.snapshot(), vec![("x".to_string(), 2), ("y".to_string(), 1)]);
}

#[tokio::test]
async fn service_counts_after_a_pause() {
    let svc = Service::start();
    for _ in 0..3 {
        svc.submit("k").await.unwrap();
    }
    tokio::time::sleep(std::time::Duration::from_millis(50)).await;
    let agg = svc.shutdown().await;
    assert_eq!(agg.count("k"), 3);
}

#[test]
fn ring_basic() {
    let mut r = RingBuf::new(3);
    for b in *b"ab" {
        r.push(b);
    }
    assert_eq!(r.peek(0), Some(b'a'));
    assert_eq!(r.pop(), Some(b'a'));
    assert_eq!(r.text(), "b");
}

#[test]
fn ffi_add_and_free() {
    use std::ffi::CString;
    let h = tally::ffi::tally_new();
    let k = CString::new("a").unwrap();
    assert_eq!(unsafe { tally::ffi::tally_add(h, k.as_ptr()) }, 0);
    unsafe { tally::ffi::tally_free(h) };
}

fn write_log(name: &str, body: &str) -> std::path::PathBuf {
    let p = std::env::temp_dir().join(format!("tally-base-{}-{name}", std::process::id()));
    std::fs::write(&p, body).unwrap();
    p
}

#[test]
fn cli_counts_first_words() {
    let p = write_log(
        "cli",
        "2026-09-29T10:00:00Z INFO login ok\n2026-09-29T10:00:01Z INFO login ok\n2026-09-29T10:00:02Z ERROR boom now\n",
    );
    let out = Command::new(env!("CARGO_BIN_EXE_tally")).arg(&p).output().unwrap();
    assert!(out.status.success());
    assert_eq!(String::from_utf8_lossy(&out.stdout), "2\tlogin\n1\tboom\n");
    let out = Command::new(env!("CARGO_BIN_EXE_tally")).arg(&p).args(["--format", "json"]).output().unwrap();
    assert_eq!(String::from_utf8_lossy(&out.stdout).trim(), r#"[{"count":2,"key":"login"},{"count":1,"key":"boom"}]"#);
}
