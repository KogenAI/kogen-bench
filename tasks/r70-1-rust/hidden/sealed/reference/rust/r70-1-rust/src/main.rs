use std::io::{self, Write};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match core::execute(&args) {
        Ok(output) => {
            let _ = io::stdout().write_all(output.as_bytes());
        }
        Err((code, message)) => {
            let _ = writeln!(io::stderr(), "{message}");
            std::process::exit(code);
        }
    }
}

mod core;
