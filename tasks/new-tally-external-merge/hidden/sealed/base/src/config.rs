//! `key = value` configuration files (`#` starts a comment).
use crate::parse::Level;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Config {
    pub top: usize,
    pub min_level: Level,
    pub window_secs: u64,
}

impl Default for Config {
    fn default() -> Self {
        Config { top: 10, min_level: Level::Debug, window_secs: 60 }
    }
}

pub fn parse_config(src: &str) -> Result<Config, String> {
    let mut cfg = Config::default();
    for (i, raw) in src.lines().enumerate() {
        let line = raw.split('#').next().unwrap().trim();
        if line.is_empty() {
            continue;
        }
        let (k, v) = line
            .split_once('=')
            .ok_or_else(|| format!("line {}: expected key = value", i + 1))?;
        let v = v.trim();
        match k.trim() {
            "top" => cfg.top = v.parse().unwrap(),
            "min_level" => cfg.min_level = Level::parse(v).ok_or("bad level")?,
            "window_secs" => cfg.window_secs = v.parse().unwrap(),
            other => return Err(format!("unknown key {other}")),
        }
    }
    Ok(cfg)
}
