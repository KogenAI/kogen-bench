use reqwest::Client;
use serde_json::{Value, json};
use std::{fs, io::Write, path::Path, time::Duration};

struct Options {
    url: String,
    prompt: String,
    timeout: Duration,
    usage: String,
}

pub fn execute(args: &[String]) -> Result<String, (i32, String)> {
    let opts = parse(args).ok_or((2, "error: invalid arguments".into()))?;
    let result = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .map_err(|_| (5, "error: request failed".into()))?;
    let (text, input, output) = result
        .block_on(run(&opts))
        .map_err(|_| (5, "error: request failed".into()))?;
    atomic_usage(&opts.usage, input, output).map_err(|_| (5, "error: request failed".into()))?;
    Ok(format!("{text}\n"))
}

fn parse(args: &[String]) -> Option<Options> {
    if args.first().map(String::as_str) != Some("model") || args.len() != 9 || args.len() % 2 != 1 {
        return None;
    }
    let mut url = None;
    let mut prompt = None;
    let mut timeout = None;
    let mut usage = None;
    for pair in args[1..].chunks_exact(2) {
        let slot = match pair[0].as_str() {
            "--url" => &mut url,
            "--prompt" => &mut prompt,
            "--idle-timeout-ms" => &mut timeout,
            "--usage-file" => &mut usage,
            _ => return None,
        };
        if slot.replace(pair[1].clone()).is_some() {
            return None;
        }
    }
    let url = url?;
    let parsed = reqwest::Url::parse(&url).ok()?;
    if parsed.scheme() != "http" || parsed.host_str().is_none() {
        return None;
    }
    let timeout = timeout?;
    if timeout.is_empty() || !timeout.bytes().all(|b| b.is_ascii_digit()) {
        return None;
    }
    let millis: u64 = timeout.parse().ok()?;
    if !(1..=60000).contains(&millis) {
        return None;
    }
    let usage = usage?;
    if usage.is_empty() {
        return None;
    }
    Some(Options {
        url,
        prompt: prompt?,
        timeout: Duration::from_millis(millis),
        usage,
    })
}

async fn run(opts: &Options) -> Result<(String, u64, u64), ()> {
    let client = Client::builder()
        .redirect(reqwest::redirect::Policy::none())
        .build()
        .map_err(|_| ())?;
    let body = serde_json::to_vec(&json!({"prompt": opts.prompt})).map_err(|_| ())?;
    for attempt in 0..2 {
        match once(&client, opts, &body).await {
            Ok(value) => return Ok(value),
            Err(retryable) if retryable && attempt == 0 => continue,
            Err(_) => return Err(()),
        }
    }
    Err(())
}

async fn once(client: &Client, opts: &Options, body: &[u8]) -> Result<(String, u64, u64), bool> {
    let request = client
        .post(&opts.url)
        .header("Content-Type", "application/json")
        .header("Accept", "text/event-stream")
        .body(body.to_vec())
        .build()
        .map_err(|_| false)?;
    let response = tokio::time::timeout(opts.timeout, client.execute(request))
        .await
        .map_err(|_| true)?
        .map_err(|_| true)?;
    let status = response.status();
    if status.is_server_error() {
        return Err(true);
    }
    if !status.is_success() {
        return Err(false);
    }
    let mut response = response;
    let mut bytes = Vec::new();
    loop {
        let next = tokio::time::timeout(opts.timeout, response.chunk())
            .await
            .map_err(|_| true)?
            .map_err(|_| true)?;
        match next {
            Some(chunk) => bytes.extend_from_slice(&chunk),
            None => break,
        }
    }
    let text = std::str::from_utf8(&bytes).map_err(|_| false)?;
    parse_sse(text).map_err(|_| false)
}

fn parse_sse(input: &str) -> Result<(String, u64, u64), ()> {
    let mut output = String::new();
    let mut usage = None;
    let mut data: Vec<String> = Vec::new();
    let mut done = false;
    for raw in input.split('\n') {
        let line = raw.strip_suffix('\r').unwrap_or(raw);
        if line.is_empty() {
            if !data.is_empty() {
                let joined = data.join("\n");
                data.clear();
                if joined == "[DONE]" {
                    done = true;
                    break;
                }
                let value: Value = serde_json::from_str(&joined).map_err(|_| ())?;
                let object = value.as_object().ok_or(())?;
                match object.get("type").and_then(Value::as_str) {
                    Some("text") => {
                        output.push_str(object.get("text").and_then(Value::as_str).ok_or(())?)
                    }
                    Some("usage") => {
                        let input = object.get("input_tokens").and_then(token_count).ok_or(())?;
                        let output_tokens = object
                            .get("output_tokens")
                            .and_then(token_count)
                            .ok_or(())?;
                        usage = Some((input, output_tokens));
                    }
                    _ => {}
                }
            }
        } else if line.starts_with(':') {
            continue;
        } else if let Some(value) = line.strip_prefix("data:") {
            data.push(value.strip_prefix(' ').unwrap_or(value).to_string());
        }
    }
    if !done {
        return Err(());
    }
    let (input, output_tokens) = usage.ok_or(())?;
    Ok((output, input, output_tokens))
}

fn atomic_usage(path: &str, input: u64, output: u64) -> std::io::Result<()> {
    let dest = Path::new(path);
    let parent = dest
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."));
    fs::create_dir_all(parent)?;
    let temp = parent.join(format!(
        ".kogen-usage-{}-{}",
        std::process::id(),
        TEMP.fetch_add(1, std::sync::atomic::Ordering::Relaxed)
    ));
    let mut file = fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&temp)?;
    writeln!(
        file,
        "{{\"input_tokens\":{input},\"output_tokens\":{output}}}"
    )?;
    file.sync_all()?;
    drop(file);
    fs::rename(&temp, dest)?;
    Ok(())
}
static TEMP: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);

fn token_count(value: &Value) -> Option<u64> {
    const MAX: u64 = 9_007_199_254_740_991;
    if let Some(integer) = value.as_u64() {
        return (integer <= MAX).then_some(integer);
    }
    let number = value.as_f64()?;
    (number.is_finite() && number >= 0.0 && number <= MAX as f64 && number.fract() == 0.0)
        .then_some(number as u64)
}
