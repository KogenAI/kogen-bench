//! A thread-safe counter registry shared between worker threads.
use std::collections::HashMap;
use std::sync::RwLock;

#[derive(Debug, Default)]
pub struct Registry {
    map: RwLock<HashMap<String, u64>>,
}

impl Registry {
    pub fn incr(&self, key: &str) {
        let current = self.map.read().unwrap().get(key).copied().unwrap_or(0);
        self.map.write().unwrap().insert(key.to_string(), current + 1);
    }

    pub fn get(&self, key: &str) -> u64 {
        self.map.read().unwrap().get(key).copied().unwrap_or(0)
    }

    /// All counters sorted by key.
    pub fn snapshot(&self) -> Vec<(String, u64)> {
        let mut v: Vec<_> = self.map.read().unwrap().iter().map(|(k, c)| (k.clone(), *c)).collect();
        v.sort();
        v
    }
}
