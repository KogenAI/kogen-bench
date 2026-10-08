use serde::de::{MapAccess, Visitor};
use serde::{Deserialize, Deserializer, Serialize};
use std::collections::{HashMap, HashSet};
use std::fmt;
use std::fs::{self, OpenOptions};
use std::io::Write;

#[derive(Clone, Debug)]
struct Event {
    id: String,
    kind: String,
    job: String,
    ts: i64,
    line: usize,
}
#[derive(Serialize)]
struct EventOut<'a> {
    id: &'a str,
    #[serde(rename = "type")]
    kind: &'a str,
    job: &'a str,
    ts: i64,
}

impl<'de> Deserialize<'de> for Event {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct EventVisitor;
        impl<'de> Visitor<'de> for EventVisitor {
            type Value = Event;
            fn expecting(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                f.write_str("event object")
            }
            fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Event, A::Error> {
                let (mut id, mut kind, mut job, mut ts) = (None, None, None, None);
                while let Some(key) = map.next_key::<String>()? {
                    match key.as_str() {
                        "id" if id.is_none() => id = Some(map.next_value::<String>()?),
                        "type" if kind.is_none() => kind = Some(map.next_value::<String>()?),
                        "job" if job.is_none() => job = Some(map.next_value::<String>()?),
                        "ts" if ts.is_none() => ts = Some(map.next_value::<i64>()?),
                        _ => return Err(serde::de::Error::custom("invalid keys")),
                    }
                }
                Ok(Event {
                    id: id.ok_or_else(|| serde::de::Error::missing_field("id"))?,
                    kind: kind.ok_or_else(|| serde::de::Error::missing_field("type"))?,
                    job: job.ok_or_else(|| serde::de::Error::missing_field("job"))?,
                    ts: ts.ok_or_else(|| serde::de::Error::missing_field("ts"))?,
                    line: 0,
                })
            }
        }
        d.deserialize_map(EventVisitor)
    }
}

fn parse(raw: &str, line: usize) -> Result<Event, String> {
    let mut e: Event =
        serde_json::from_str(raw).map_err(|_| format!("eventlog:{line}: invalid event"))?;
    if e.id.is_empty() || !regex_id(&e.id) || e.job.is_empty() || !regex_job(&e.job) || e.ts < 0 {
        return Err(format!("eventlog:{line}: invalid event"));
    }
    if !["created", "started", "completed", "failed"].contains(&e.kind.as_str()) {
        return Err(format!("eventlog:{line}: unknown event type '{}'", e.kind));
    }
    e.line = line;
    Ok(e)
}
fn regex_id(s: &str) -> bool {
    s.strip_prefix("e-").is_some_and(|x| {
        !x.is_empty()
            && x.len() <= 16
            && x.bytes()
                .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit())
    })
}
fn regex_job(s: &str) -> bool {
    s.len() <= 32
        && s.as_bytes()[0].is_ascii_lowercase()
        && s.bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
}
fn invalid(line: usize) -> String {
    format!("eventlog:{line}: invalid event")
}
fn read(path: &str) -> Result<Vec<Event>, String> {
    let data = match fs::read(path) {
        Ok(x) => x,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(Vec::new()),
        Err(_) => return Err("eventlog: cannot access log".into()),
    };
    let text = std::str::from_utf8(&data).map_err(|_| invalid(1))?;
    let count = text.bytes().filter(|b| *b == b'\n').count();
    let rows: Vec<&str> = text.split('\n').take(count).collect();
    let mut out = Vec::new();
    let mut ids = HashSet::new();
    for (n, row) in rows.into_iter().enumerate() {
        let line = n + 1;
        let e = parse(row, line)?;
        if !ids.insert(e.id.clone()) {
            return Err(format!("eventlog:{line}: duplicate event id '{}'", e.id));
        }
        out.push(e);
    }
    Ok(out)
}
fn reconcile(mut events: Vec<Event>) -> Result<String, String> {
    events.sort_by(|a, b| a.ts.cmp(&b.ts).then(a.line.cmp(&b.line)));
    let mut states: HashMap<String, &str> = HashMap::new();
    let mut prev: HashMap<String, i64> = HashMap::new();
    let mut counts = [0usize; 4];
    for e in &events {
        let state = states.get(&e.job).copied().unwrap_or("");
        if prev.get(&e.job).is_some_and(|t| *t == e.ts) {
            return Err(format!(
                "eventlog:{}: invalid transition for job '{}'",
                e.line, e.job
            ));
        }
        let next = match (state, e.kind.as_str()) {
            ("", "created") => "queued",
            ("queued", "started") => "running",
            ("running", "completed") => "done",
            ("running", "failed") => "failed",
            _ => {
                return Err(format!(
                    "eventlog:{}: invalid transition for job '{}'",
                    e.line, e.job
                ));
            }
        };
        states.insert(e.job.clone(), next);
        prev.insert(e.job.clone(), e.ts);
    }
    for s in states.values() {
        counts[match *s {
            "queued" => 0,
            "running" => 1,
            "done" => 2,
            _ => 3,
        }] += 1;
    }
    Ok(format!(
        "total={}\nqueued={}\nrunning={}\ndone={}\nfailed={}\n",
        states.len(),
        counts[0],
        counts[1],
        counts[2],
        counts[3]
    ))
}
pub fn execute(args: &[String]) -> Result<String, (i32, String)> {
    let result = if args.len() == 3 && args[0] == "reconcile" && args[1] == "--log" {
        read(&args[2]).and_then(reconcile)
    } else if args.len() == 5 && args[0] == "append" && args[1] == "--log" && args[3] == "--event" {
        (|| {
            let mut e = parse(&args[4], 1)?;
            let old = match fs::read(&args[2]) {
                Ok(x) => x,
                Err(x) if x.kind() == std::io::ErrorKind::NotFound => Vec::new(),
                Err(_) => return Err("eventlog: cannot access log".into()),
            };
            if !old.is_empty() && old.last() != Some(&b'\n') {
                return Err(invalid(old.iter().filter(|b| **b == b'\n').count() + 1));
            }
            let existing = read(&args[2])?;
            if let Some(x) = existing.iter().find(|x| x.id == e.id) {
                return Err(format!(
                    "eventlog:{}: duplicate event id '{}'",
                    x.line, e.id
                ));
            }
            e.line = 1;
            let mut f = OpenOptions::new()
                .create(true)
                .append(true)
                .open(&args[2])
                .map_err(|_| "eventlog: cannot access log".to_string())?;
            let obj = serde_json::to_string(&EventOut {
                id: &e.id,
                kind: &e.kind,
                job: &e.job,
                ts: e.ts,
            })
            .map_err(|_| "eventlog: cannot access log".to_string())?;
            writeln!(f, "{}", obj).map_err(|_| "eventlog: cannot access log".to_string())?;
            Ok(format!("appended {}\n", e.id))
        })()
    } else {
        return Err((2, "eventlog: usage error".into()));
    };
    result.map_err(|e| (1, e))
}
