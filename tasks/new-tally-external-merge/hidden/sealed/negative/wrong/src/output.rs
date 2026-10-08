//! Rendering of results.

pub fn render_text(top: &[(String, u64)]) -> String {
    let mut s = String::new();
    for (key, count) in top {
        s.push_str(&format!("{count}\t{key}\n"));
    }
    s
}

pub fn render_json(top: &[(String, u64)]) -> String {
    let items: Vec<_> = top
        .iter()
        .map(|(key, count)| serde_json::json!({ "key": key, "count": count }))
        .collect();
    serde_json::Value::Array(items).to_string()
}
