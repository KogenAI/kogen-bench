//! Counting aggregator.
use crate::text::tokenize;

#[derive(Debug, Default)]
pub struct Aggregator {
    entries: Vec<(String, u64)>,
}

impl Aggregator {
    pub fn add(&mut self, key: &str) { self.add_count(key, 1).expect("count overflow"); }
    pub fn add_count(&mut self, key: &str, count: u64) -> Result<(), &'static str> {
        for e in self.entries.iter_mut() {
            if e.0 == key {
                e.1 = e.1.checked_add(count).ok_or("count overflow")?;
                return Ok(());
            }
        }
        self.entries.push((key.to_string(), count));
        Ok(())
    }

    pub fn count(&self, key: &str) -> u64 {
        self.entries.iter().find(|e| e.0 == key).map_or(0, |e| e.1)
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    /// The `k` most frequent keys: count descending, then key ascending.
    pub fn top(&self, k: usize) -> Vec<(String, u64)> {
        let mut v = self.entries.clone();
        v.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
        v.truncate(k);
        v
    }
}

/// Word frequency of a text.
pub fn word_counts(input: &str) -> Aggregator {
    let mut agg = Aggregator::default();
    for t in tokenize(input) {
        agg.add(&t.text);
    }
    agg
}
