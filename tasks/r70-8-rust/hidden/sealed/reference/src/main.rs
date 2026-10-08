use reqwest::{Client, Response, StatusCode};
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::HashMap;
use std::env;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Read, Write};
use std::path::{Component, Path, PathBuf};
use std::process::{Command, Stdio};
use std::os::unix::process::CommandExt;
use std::sync::mpsc;
use std::thread;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};
use tokio::time::timeout_at;

const TOOLS: &str = r#"[{"type":"function","name":"read_file","description":"Read a UTF-8 file under the workdir","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"],"additionalProperties":false}},{"type":"function","name":"run_command","description":"Run a shell command with the workdir as its current directory","parameters":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"],"additionalProperties":false}}]"#;

#[derive(Debug)]
struct AppError {
    code: i32,
    message: &'static str,
}

impl AppError {
    fn new(code: i32, message: &'static str) -> Self {
        Self { code, message }
    }
}

struct Options {
    prompt_file: String,
    server: String,
    records: String,
    workdir: Option<String>,
    session: String,
    first_byte: Duration,
    idle: Duration,
    max_retries: usize,
    backoff: Duration,
}

fn invalid_cli() -> AppError {
    AppError::new(2, "loop: invalid command line")
}

fn bounded_number(value: &str, min: u64, max: u64) -> Option<u64> {
    if value.is_empty() || !value.bytes().all(|byte| byte.is_ascii_digit()) {
        return None;
    }
    let parsed = value.parse::<u64>().ok()?;
    (parsed >= min && parsed <= max).then_some(parsed)
}

fn valid_session(value: &str) -> bool {
    !value.is_empty()
        && value.len() <= 128
        && value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || b"._:-".contains(&byte))
}

fn parse_args(args: &[String]) -> Result<Options, AppError> {
    if args.len() < 2 || args[0] != "loop" || args[1] != "run" {
        return Err(invalid_cli());
    }
    let mut prompt_file = None;
    let mut server = None;
    let mut records = None;
    let mut workdir = None;
    let mut session = None;
    let mut first_byte = 5000;
    let mut idle = 3000;
    let mut max_retries = 2;
    let mut backoff = 50;
    let mut seen = HashMap::<String, bool>::new();
    let mut index = 2;
    while index < args.len() {
        let flag = &args[index];
        if !flag.starts_with("--") || index + 1 >= args.len() {
            return Err(invalid_cli());
        }
        let value = args[index + 1].clone();
        if seen.insert(flag.clone(), true).is_some() {
            return Err(invalid_cli());
        }
        match flag.as_str() {
            "--prompt-file" => prompt_file = Some(value),
            "--server" => server = Some(value),
            "--records" => records = Some(value),
            "--workdir" => workdir = Some(value),
            "--session" if valid_session(&value) => session = Some(value),
            "--first-byte-timeout-ms" => {
                first_byte = bounded_number(&value, 1, 60_000).ok_or_else(invalid_cli)?;
            }
            "--idle-timeout-ms" => {
                idle = bounded_number(&value, 1, 60_000).ok_or_else(invalid_cli)?;
            }
            "--max-retries" => {
                max_retries = bounded_number(&value, 0, 5).ok_or_else(invalid_cli)?;
            }
            "--backoff-ms" => {
                backoff = bounded_number(&value, 0, 5000).ok_or_else(invalid_cli)?;
            }
            _ => return Err(invalid_cli()),
        }
        index += 2;
    }
    let prompt_file = prompt_file.ok_or_else(invalid_cli)?;
    let server = server.ok_or_else(invalid_cli)?;
    let records = records.ok_or_else(invalid_cli)?;
    if !valid_server(&server) {
        return Err(invalid_cli());
    }
    let session = session.unwrap_or_else(generated_session);
    Ok(Options {
        prompt_file,
        server,
        records,
        workdir,
        session,
        first_byte: Duration::from_millis(first_byte),
        idle: Duration::from_millis(idle),
        max_retries: max_retries as usize,
        backoff: Duration::from_millis(backoff),
    })
}

fn valid_server(value: &str) -> bool {
    let Some(rest) = value.strip_prefix("http://") else {
        return false;
    };
    let authority = rest.trim_end_matches('/');
    !authority.is_empty()
        && !authority.contains('/')
        && !authority.contains('?')
        && !authority.contains('#')
        && !authority.contains('@')
}

fn generated_session() -> String {
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0, |duration| duration.as_nanos());
    format!("loop-{}-{nanos}", std::process::id())
}

#[derive(Serialize)]
struct InputText<'a> {
    r#type: &'static str,
    text: &'a str,
}

#[derive(Serialize)]
struct UserItem<'a> {
    role: &'static str,
    content: [InputText<'a>; 1],
}

#[derive(Serialize)]
struct FunctionCallItem<'a> {
    r#type: &'static str,
    call_id: &'a str,
    name: &'a str,
    arguments: &'a str,
}

#[derive(Serialize)]
struct FunctionOutputItem<'a> {
    r#type: &'static str,
    call_id: &'a str,
    output: &'a str,
}

#[derive(Clone, Serialize)]
struct Usage {
    input_tokens: Option<i64>,
    output_tokens: Option<i64>,
    cached_tokens: Option<i64>,
}

#[derive(Serialize)]
struct RequestRecord {
    start_ms: u128,
    first_byte_ms: Option<u128>,
    end_ms: u128,
    outcome: &'static str,
    retries: usize,
    usage: Usage,
    request_bytes: usize,
    history_items: usize,
}

#[derive(Clone)]
struct Call {
    id: String,
    name: String,
    arguments: String,
}

struct StreamResponse {
    text: String,
    calls: Vec<Call>,
    usage: Usage,
}

struct Parser {
    buffer: Vec<u8>,
    event_name: String,
    data: Option<String>,
    calls: Vec<Call>,
    by_id: HashMap<String, usize>,
    text: String,
    saw_text: bool,
    completed: bool,
    invalid: bool,
    usage: Usage,
}

impl Parser {
    fn new() -> Self {
        Self {
            buffer: Vec::new(),
            event_name: String::new(),
            data: None,
            calls: Vec::new(),
            by_id: HashMap::new(),
            text: String::new(),
            saw_text: false,
            completed: false,
            invalid: false,
            usage: Usage {
                input_tokens: None,
                output_tokens: None,
                cached_tokens: None,
            },
        }
    }

    fn feed(&mut self, chunk: &[u8]) -> bool {
        self.buffer.extend_from_slice(chunk);
        loop {
            let Some(end) = self.buffer.iter().position(|byte| *byte == b'\n') else {
                return self.completed || self.invalid;
            };
            let line_bytes: Vec<u8> = self.buffer.drain(..=end).collect();
            let mut line = &line_bytes[..line_bytes.len() - 1];
            if line.last() == Some(&b'\r') {
                line = &line[..line.len() - 1];
            }
            let Ok(line) = std::str::from_utf8(line) else {
                self.invalid = true;
                return true;
            };
            if line.is_empty() {
                if self.event_name.is_empty() && self.data.is_none() {
                    continue;
                }
                self.dispatch();
                self.event_name.clear();
                self.data = None;
                if self.completed || self.invalid {
                    return true;
                }
            } else if line.starts_with(':') {
                continue;
            } else if let Some(name) = line.strip_prefix("event: ") {
                if !self.event_name.is_empty() {
                    self.invalid = true;
                    return true;
                }
                self.event_name = name.to_string();
            } else if let Some(data) = line.strip_prefix("data: ") {
                if self.data.is_some() {
                    self.invalid = true;
                    return true;
                }
                self.data = Some(data.to_string());
            } else {
                self.invalid = true;
                return true;
            }
        }
    }

    fn dispatch(&mut self) {
        if self.event_name.is_empty() || self.data.is_none() || self.completed {
            self.invalid = true;
            return;
        }
        let Ok(value) = serde_json::from_str::<Value>(self.data.as_deref().unwrap_or_default()) else {
            self.invalid = true;
            return;
        };
        match self.event_name.as_str() {
            "response.function_call_arguments.delta" => {
                let Some(call_id) = value.get("call_id").and_then(Value::as_str).filter(|id| !id.is_empty()) else {
                    self.invalid = true;
                    return;
                };
                let Some(name) = value.get("name").and_then(Value::as_str) else {
                    self.invalid = true;
                    return;
                };
                if name != "read_file" && name != "run_command" {
                    self.invalid = true;
                    return;
                }
                let Some(delta) = value.get("delta").and_then(Value::as_str) else {
                    self.invalid = true;
                    return;
                };
                if let Some(index) = self.by_id.get(call_id).copied() {
                    if self.calls[index].name != name {
                        self.invalid = true;
                        return;
                    }
                    self.calls[index].arguments.push_str(delta);
                } else {
                    self.by_id.insert(call_id.to_string(), self.calls.len());
                    self.calls.push(Call {
                        id: call_id.to_string(),
                        name: name.to_string(),
                        arguments: delta.to_string(),
                    });
                }
            }
            "response.output_text.delta" => {
                let Some(delta) = value.get("delta").and_then(Value::as_str) else {
                    self.invalid = true;
                    return;
                };
                self.saw_text = true;
                self.text.push_str(delta);
            }
            "response.completed" => {
                let Some(usage) = value.get("usage") else {
                    self.invalid = true;
                    return;
                };
                let input = usage.get("input_tokens").and_then(Value::as_i64);
                let output = usage.get("output_tokens").and_then(Value::as_i64);
                let cached = usage
                    .get("input_tokens_details")
                    .and_then(|details| details.get("cached_tokens"))
                    .and_then(Value::as_i64);
                if input.is_none() || output.is_none() || cached.is_none() || input.unwrap_or(-1) < 0 || output.unwrap_or(-1) < 0 || cached.unwrap_or(-1) < 0 || (self.saw_text && !self.calls.is_empty()) {
                    self.invalid = true;
                    return;
                }
                self.usage = Usage {
                    input_tokens: input,
                    output_tokens: output,
                    cached_tokens: cached,
                };
                self.completed = true;
            }
            _ => self.invalid = true,
        }
    }

    fn finish(self) -> Result<StreamResponse, ()> {
        if self.invalid || !self.completed || !self.buffer.is_empty() || !self.event_name.is_empty() || self.data.is_some() || (self.saw_text && !self.calls.is_empty()) {
            return Err(());
        }
        Ok(StreamResponse {
            text: self.text,
            calls: self.calls,
            usage: self.usage,
        })
    }
}

#[derive(Clone, Copy)]
enum FailureKind {
    Timeout,
    Stall,
    Transport,
    Overload,
    Rejected,
    Invalid,
}

struct AttemptFailure {
    kind: FailureKind,
}

fn time_ms(origin: Instant) -> u128 {
    origin.elapsed().as_millis()
}

fn request_body(history: &str) -> Vec<u8> {
    format!("{{\"model\":\"fake-agent\",\"stream\":true,\"tools\":{TOOLS},\"tool_choice\":\"auto\",\"input\":{history}}}").into_bytes()
}

async fn perform_request(
    client: &Client,
    options: &Options,
    body: &[u8],
    retry_index: usize,
    history_items: usize,
    run_start: Instant,
    records: &mut File,
) -> Result<Result<StreamResponse, AttemptFailure>, AppError> {
    let start = Instant::now();
    let mut record = RequestRecord {
        start_ms: run_start.elapsed().as_millis(),
        first_byte_ms: None,
        end_ms: 0,
        outcome: "transport",
        retries: retry_index,
        usage: Usage { input_tokens: None, output_tokens: None, cached_tokens: None },
        request_bytes: body.len(),
        history_items,
    };
    let url = format!("{}/v1/responses", options.server.trim_end_matches('/'));
    let request = client
        .post(url)
        .header("Content-Type", "application/json")
        .header("Accept", "text/event-stream")
        .header("X-Session-ID", &options.session)
        .body(body.to_vec());
    let first_deadline = start + options.first_byte;
    let response = match timeout_at(first_deadline.into(), request.send()).await {
        Err(_) => {
            record.outcome = "timeout";
            record.end_ms = time_ms(run_start);
            write_record(records, &record)?;
            return Ok(Err(AttemptFailure { kind: FailureKind::Timeout }));
        }
        Ok(Err(_)) => {
            record.outcome = "transport";
            record.end_ms = time_ms(run_start);
            write_record(records, &record)?;
            return Ok(Err(AttemptFailure { kind: FailureKind::Transport }));
        }
        Ok(Ok(response)) => response,
    };
    if response.status() == StatusCode::TOO_MANY_REQUESTS || response.status().as_u16() == 529 || response.status().is_server_error() {
        record.outcome = "overload";
        record.end_ms = time_ms(run_start);
        write_record(records, &record)?;
        return Ok(Err(AttemptFailure { kind: FailureKind::Overload }));
    }
    if response.status() != StatusCode::OK {
        record.outcome = "transport";
        record.end_ms = time_ms(run_start);
        write_record(records, &record)?;
        return Ok(Err(AttemptFailure { kind: FailureKind::Rejected }));
    }
    if !response
        .headers()
        .get(reqwest::header::CONTENT_TYPE)
        .and_then(|value| value.to_str().ok())
        .is_some_and(|value| value.to_ascii_lowercase().starts_with("text/event-stream"))
    {
        record.outcome = "transport";
        record.end_ms = time_ms(run_start);
        write_record(records, &record)?;
        return Ok(Err(AttemptFailure { kind: FailureKind::Invalid }));
    }
    consume_response(response, first_deadline, options, run_start, &mut record, records).await
}

async fn consume_response(
    mut response: Response,
    first_deadline: Instant,
    options: &Options,
    run_start: Instant,
    record: &mut RequestRecord,
    records: &mut File,
) -> Result<Result<StreamResponse, AttemptFailure>, AppError> {
    let mut parser = Parser::new();
    let mut first = false;
    loop {
        let deadline = if first { Instant::now() + options.idle } else { first_deadline };
        match timeout_at(deadline.into(), response.chunk()).await {
            Err(_) => {
                record.outcome = if first { "stall" } else { "timeout" };
                record.first_byte_ms = if first { record.first_byte_ms } else { None };
                record.end_ms = time_ms(run_start);
                write_record(records, record)?;
                return Ok(Err(AttemptFailure { kind: if first { FailureKind::Stall } else { FailureKind::Timeout } }));
            }
            Ok(Err(_)) => {
                record.outcome = "transport";
                record.end_ms = time_ms(run_start);
                write_record(records, record)?;
                return Ok(Err(AttemptFailure { kind: FailureKind::Transport }));
            }
            Ok(Ok(None)) => {
                record.outcome = "transport";
                record.end_ms = time_ms(run_start);
                write_record(records, record)?;
                return Ok(Err(AttemptFailure { kind: FailureKind::Transport }));
            }
            Ok(Ok(Some(chunk))) => {
                if !chunk.is_empty() {
                    if !first {
                        first = true;
                        record.first_byte_ms = Some(time_ms(run_start));
                    }
                    if parser.feed(&chunk) {
                        if parser.invalid {
                            record.outcome = "transport";
                            record.end_ms = time_ms(run_start);
                            write_record(records, record)?;
                            return Ok(Err(AttemptFailure { kind: FailureKind::Invalid }));
                        }
                        match parser.finish() {
                            Ok(parsed) => {
                                record.outcome = "ok";
                                record.usage = parsed.usage.clone();
                                record.end_ms = time_ms(run_start);
                                write_record(records, record)?;
                                return Ok(Ok(parsed));
                            }
                            Err(()) => {
                                record.outcome = "transport";
                                record.end_ms = time_ms(run_start);
                                write_record(records, record)?;
                                return Ok(Err(AttemptFailure { kind: FailureKind::Invalid }));
                            }
                        }
                    }
                }
            }
        }
    }
}

fn write_record(file: &mut File, record: &RequestRecord) -> Result<(), AppError> {
    serde_json::to_writer(&mut *file, record).map_err(|_| AppError::new(1, "loop: cannot write records file"))?;
    file.write_all(b"\n").map_err(|_| AppError::new(1, "loop: cannot write records file"))?;
    file.flush().map_err(|_| AppError::new(1, "loop: cannot write records file"))?;
    file.sync_all().map_err(|_| AppError::new(1, "loop: cannot write records file"))
}

fn append_history(history: &str, calls: &[Call], outputs: &[String]) -> Result<String, AppError> {
    let mut next = history.strip_suffix(']').ok_or_else(|| AppError::new(15, "loop: invalid response"))?.to_string();
    for (call, output) in calls.iter().zip(outputs) {
        let arguments = compact_value(&call.arguments).map_err(|_| AppError::new(16, "loop: tool execution failed"))?;
        let call_item = FunctionCallItem { r#type: "function_call", call_id: &call.id, name: &call.name, arguments: &arguments };
        let output_item = FunctionOutputItem { r#type: "function_call_output", call_id: &call.id, output };
        next.push(',');
        next.push_str(&serde_json::to_string(&call_item).map_err(|_| AppError::new(15, "loop: invalid response"))?);
        next.push(',');
        next.push_str(&serde_json::to_string(&output_item).map_err(|_| AppError::new(15, "loop: invalid response"))?);
    }
    next.push(']');
    Ok(next)
}

fn compact_value(raw: &str) -> Result<String, ()> {
    let value: Value = serde_json::from_str(raw).map_err(|_| ())?;
    if !value.is_object() {
        return Err(());
    }
    serde_json::to_string(&value).map_err(|_| ())
}

fn execute_tool(call: &Call, workdir: &Path) -> Result<String, ()> {
    let args: Value = serde_json::from_str(&call.arguments).map_err(|_| ())?;
    let object = args.as_object().ok_or(())?;
    match call.name.as_str() {
        "read_file" => {
            if object.len() != 1 {
                return Err(());
            }
            let path = object.get("path").and_then(Value::as_str).filter(|path| !path.is_empty()).ok_or(())?;
            let user_path = Path::new(path);
            if user_path.is_absolute() || user_path.components().any(|component| matches!(component, Component::ParentDir | Component::RootDir | Component::Prefix(_))) {
                return Err(());
            }
            let candidate = workdir.join(user_path);
            let resolved = fs::canonicalize(candidate).map_err(|_| ())?;
            if !resolved.starts_with(workdir) || !resolved.is_file() {
                return Err(());
            }
            let bytes = fs::read(resolved).map_err(|_| ())?;
            String::from_utf8(bytes).map_err(|_| ())
        }
        "run_command" => {
            if object.len() != 1 {
                return Err(());
            }
            let command = object.get("command").and_then(Value::as_str).filter(|command| !command.is_empty()).ok_or(())?;
            if !command_paths_allowed(command) {
                return Err(());
            }
            run_command(command, workdir)
        }
        _ => Err(()),
    }
}

fn command_paths_allowed(command: &str) -> bool {
    let bytes = command.as_bytes();
    for (index, byte) in bytes.iter().enumerate() {
        let boundary = |value: u8| value.is_ascii_whitespace() || b"\"'=<>|;&(".contains(&value);
        if *byte == b'/' && (index == 0 || boundary(bytes[index - 1])) {
            return false;
        }
        if index + 1 < bytes.len() && bytes[index] == b'.' && bytes[index + 1] == b'.' {
            let left = index == 0 || boundary(bytes[index - 1]) || bytes[index - 1] == b'/';
            let right = index + 2 == bytes.len() || bytes[index + 2] == b'/' || boundary(bytes[index + 2]);
            if left && right {
                return false;
            }
        }
    }
    true
}

fn run_command(command: &str, workdir: &Path) -> Result<String, ()> {
    let mut child = Command::new("/bin/sh")
        .arg("-c")
        .arg(command)
        .current_dir(workdir)
        .env_clear()
        .env("PATH", "/usr/bin:/bin")
        .env("HOME", workdir)
        .env("LANG", "C.UTF-8")
        .env("PWD", workdir)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .process_group(0)
        .spawn()
        .map_err(|_| ())?;
    let stdout = child.stdout.take().ok_or(())?;
    let stderr = child.stderr.take().ok_or(())?;
    let (tx, rx) = mpsc::channel();
    let stdout_thread = thread::spawn(move || {
        let mut data = Vec::new();
        let result = stdout.take(1_048_577).read_to_end(&mut data);
        let _ = tx.send((0, data, result));
    });
    let (tx2, rx2) = mpsc::channel();
    let stderr_thread = thread::spawn(move || {
        let mut data = Vec::new();
        let result = stderr.take(1_048_577).read_to_end(&mut data);
        let _ = tx2.send((1, data, result));
    });
    let deadline = Instant::now() + Duration::from_secs(5);
    let status = loop {
        match child.try_wait() {
            Ok(Some(status)) => break status,
            Ok(None) if Instant::now() < deadline => thread::sleep(Duration::from_millis(10)),
            _ => {
                unsafe {
                    libc::kill(-(child.id() as i32), libc::SIGKILL);
                }
                let _ = child.kill();
                let _ = child.wait();
                let _ = stdout_thread.join();
                let _ = stderr_thread.join();
                return Err(());
            }
        }
    };
    unsafe {
        libc::kill(-(child.id() as i32), libc::SIGKILL);
    }
    let _ = stdout_thread.join();
    let _ = stderr_thread.join();
    let (_, stdout, stdout_result) = rx.recv().map_err(|_| ())?;
    let (_, stderr, stderr_result) = rx2.recv().map_err(|_| ())?;
    if stdout_result.is_err() || stderr_result.is_err() || stdout.len() > 1_048_576 || stderr.len() > 1_048_576 || stdout.len() + stderr.len() > 1_048_576 {
        return Err(());
    }
    let stdout = String::from_utf8(stdout).map_err(|_| ())?;
    let stderr = String::from_utf8(stderr).map_err(|_| ())?;
    let exit_code = status.code().unwrap_or(-1);
    let output = serde_json::to_string(&json!({ "exit_code": exit_code, "stdout": stdout, "stderr": stderr })).map_err(|_| ())?;
    // json! uses a sorted map; rebuild the specified key order explicitly.
    let parsed: Value = serde_json::from_str(&output).map_err(|_| ())?;
    let exit = parsed.get("exit_code").and_then(Value::as_i64).ok_or(())?;
    let stdout = parsed.get("stdout").and_then(Value::as_str).ok_or(())?;
    let stderr = parsed.get("stderr").and_then(Value::as_str).ok_or(())?;
    Ok(format!("{{\"exit_code\":{exit},\"stdout\":{},\"stderr\":{}}}", serde_json::to_string(stdout).map_err(|_| ())?, serde_json::to_string(stderr).map_err(|_| ())?))
}

fn resolve_workdir(value: Option<&str>) -> Result<PathBuf, AppError> {
    let path = match value {
        Some(value) => PathBuf::from(value),
        None => env::current_dir().map_err(|_| AppError::new(1, "loop: invalid workdir"))?,
    };
    let resolved = fs::canonicalize(path).map_err(|_| AppError::new(1, "loop: invalid workdir"))?;
    if !resolved.is_dir() {
        return Err(AppError::new(1, "loop: invalid workdir"));
    }
    Ok(resolved)
}

fn app_error_for_attempt(kind: FailureKind) -> AppError {
    match kind {
        FailureKind::Timeout => AppError::new(10, "loop: first-byte timeout"),
        FailureKind::Stall => AppError::new(11, "loop: stream stalled"),
        FailureKind::Transport => AppError::new(12, "loop: transport error"),
        FailureKind::Overload => AppError::new(13, "loop: server overloaded"),
        FailureKind::Rejected => AppError::new(14, "loop: server rejected request"),
        FailureKind::Invalid => AppError::new(15, "loop: invalid response"),
    }
}

async fn run(args: Vec<String>) -> Result<(), AppError> {
    let options = parse_args(&args)?;
    let prompt = fs::read_to_string(&options.prompt_file).map_err(|_| AppError::new(1, "loop: cannot read prompt file"))?;
    let workdir = resolve_workdir(options.workdir.as_deref())?;
    let mut records = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true)
        .open(&options.records)
        .map_err(|_| AppError::new(1, "loop: cannot write records file"))?;
    let user_item = UserItem {
        role: "user",
        content: [InputText { r#type: "input_text", text: &prompt }],
    };
    let user = serde_json::to_string(&user_item).map_err(|_| AppError::new(1, "loop: cannot read prompt file"))?;
    let mut history = format!("[{user}]");
    let mut history_items = 1usize;
    let run_start = Instant::now();
    let client = Client::builder()
        .no_proxy()
        .build()
        .map_err(|_| AppError::new(12, "loop: transport error"))?;
    loop {
        let body = request_body(&history);
        let mut retries = 0usize;
        let response = loop {
            match perform_request(&client, &options, &body, retries, history_items, run_start, &mut records).await? {
                Ok(response) => break response,
                Err(failure) => match failure.kind {
                    FailureKind::Rejected | FailureKind::Invalid => return Err(app_error_for_attempt(failure.kind)),
                    kind if retries >= options.max_retries => return Err(app_error_for_attempt(kind)),
                    _ => {
                        let factor = 1u32 << retries;
                        tokio::time::sleep(options.backoff * factor).await;
                        retries += 1;
                    }
                },
            }
        };
        if response.calls.is_empty() {
            io::stdout()
                .write_all(response.text.as_bytes())
                .map_err(|_| AppError::new(1, "loop: cannot write records file"))?;
            return Ok(());
        }
        let mut outputs = Vec::with_capacity(response.calls.len());
        for call in &response.calls {
            compact_value(&call.arguments).map_err(|_| AppError::new(16, "loop: tool execution failed"))?;
            outputs.push(execute_tool(call, &workdir).map_err(|_| AppError::new(16, "loop: tool execution failed"))?);
        }
        history = append_history(&history, &response.calls, &outputs)?;
        history_items += response.calls.len() * 2;
    }
}

#[tokio::main]
async fn main() {
    if let Err(error) = run(env::args().skip(1).collect()).await {
        let _ = writeln!(io::stderr(), "{}", error.message);
        std::process::exit(error.code);
    }
}
