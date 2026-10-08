use std::io::{self, Write};
mod core;
fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match core::execute(&args) {
        Ok((code, status)) => {
            let _ = io::stderr().write_all(status.as_bytes());
            std::process::exit(code);
        }
        Err((code, message)) => {
            let _ = writeln!(io::stderr(), "{message}");
            std::process::exit(code);
        }
    }
}
