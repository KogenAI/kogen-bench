use std::io::{self, Read, Write};

pub fn physical_lines(text: &str) -> Vec<&str> {
    text.split('\n')
        .map(|line| line.strip_suffix('\r').unwrap_or(line))
        .collect()
}

pub fn load(path: Option<&str>, prefix: &str) -> Result<Vec<u8>, String> {
    let result = match path {
        None | Some("-") => {
            let mut bytes = Vec::new();
            io::stdin().read_to_end(&mut bytes).map(|_| bytes)
        }
        Some(path) => std::fs::read(path),
    };
    result.map_err(|_| format!("{prefix}: cannot read input"))
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match core::execute(&args) {
        Ok((output, code)) => {
            let _ = io::stdout().write_all(output.as_bytes());
            std::process::exit(code);
        }
        Err((code, message)) => {
            let _ = writeln!(io::stderr(), "{message}");
            std::process::exit(code);
        }
    }
}

mod core;

#[cfg(test)]
mod tests {
    #[test]
    fn physical_line_endings() {
        assert_eq!(super::physical_lines("a\r\n\nb\r"), vec!["a", "", "b"]);
    }
}
