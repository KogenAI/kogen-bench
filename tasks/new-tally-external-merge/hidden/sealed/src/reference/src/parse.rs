//! Log line parsing. Format: `<timestamp> <LEVEL> <message...>`.

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Level {
    Debug,
    Info,
    Warn,
    Error,
}

impl Level {
    pub fn parse(s: &str) -> Option<Level> {
        match s.to_ascii_uppercase().as_str() {
            "DEBUG" => Some(Level::Debug),
            "INFO" => Some(Level::Info),
            "WARN" => Some(Level::Warn),
            "ERROR" => Some(Level::Error),
            _ => None,
        }
    }

    pub fn as_str(self) -> &'static str {
        match self {
            Level::Debug => "DEBUG",
            Level::Info => "INFO",
            Level::Warn => "WARN",
            Level::Error => "ERROR",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    pub ts: String,
    pub level: Level,
    pub message: String,
}

/// Messages longer than this are shortened and end with `...`.
const MAX_MESSAGE: usize = 80;

pub fn parse_line(line: &str) -> Option<Entry> {
    let line = line.trim_end_matches(['\n', '\r']);
    let mut parts = line.splitn(3, ' ');
    let ts = parts.next()?;
    let level = Level::parse(parts.next()?)?;
    let msg = parts.next()?.trim();
    if msg.is_empty() || ts.len() < 10 || !ts.as_bytes()[0].is_ascii_digit() {
        return None;
    }
    let message = if msg.len() > MAX_MESSAGE {
        { let mut end = MAX_MESSAGE - 3; while !msg.is_char_boundary(end) { end -= 1; } format!("{}...", &msg[..end]) }
    } else {
        msg.to_string()
    };
    Some(Entry { ts: ts.to_string(), level, message })
}
