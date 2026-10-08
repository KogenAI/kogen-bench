use serde::{Deserialize, Serialize};
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::os::unix::process::ExitStatusExt;
use std::path::{Path, PathBuf};
use std::process::Command;

#[derive(Serialize, Deserialize)]
struct Job {
    id: String,
    argv: Vec<String>,
    attempts: u64,
    done: bool,
    exit_code: i32,
    stdout: String,
    stderr: String,
}
#[derive(Serialize, Deserialize, Default)]
struct State {
    jobs: Vec<Job>,
}
#[derive(Serialize)]
struct ResultLine<'a> {
    id: &'a str,
    attempt: u64,
    exit_code: i32,
    stdout: &'a str,
    stderr: &'a str,
    status: &'a str,
}

struct Lock(File);
impl Lock {
    fn acquire(path: &Path) -> std::io::Result<Self> {
        let file = OpenOptions::new()
            .create(true)
            .truncate(false)
            .read(true)
            .write(true)
            .open(path)?;
        // SAFETY: flock is called with a live descriptor and a valid operation.
        if unsafe { libc::flock(std::os::fd::AsRawFd::as_raw_fd(&file), libc::LOCK_EX) } != 0 {
            return Err(std::io::Error::last_os_error());
        }
        Ok(Self(file))
    }
}
impl Drop for Lock {
    fn drop(&mut self) {
        // SAFETY: the descriptor remains open for the duration of this guard.
        unsafe {
            libc::flock(std::os::fd::AsRawFd::as_raw_fd(&self.0), libc::LOCK_UN);
        }
    }
}

fn invalid() -> (i32, String) {
    (2, "error: invalid arguments".into())
}
fn store_error() -> (i32, String) {
    (4, "error: store failure".into())
}

pub fn execute(args: &[String]) -> Result<String, (i32, String)> {
    let (command, values) = parse(args).ok_or_else(invalid)?;
    let dir = PathBuf::from(values.get("--store").ok_or_else(invalid)?);
    fs::create_dir_all(&dir).map_err(|_| store_error())?;
    let _lock = Lock::acquire(&dir.join(".lock")).map_err(|_| store_error())?;
    let mut state = read_state(&dir).map_err(|_| store_error())?;
    match command.as_str() {
        "add" => {
            let id = values.get("--id").ok_or_else(invalid)?;
            if state.jobs.iter().any(|job| job.id == *id) {
                return Err((3, "error: duplicate job id".into()));
            }
            let argv: Vec<String> = serde_json::from_str(values.get("--argv").ok_or_else(invalid)?)
                .map_err(|_| invalid())?;
            if argv.is_empty()
                || argv
                    .iter()
                    .any(|value| value.is_empty() || value.contains('\0'))
            {
                return Err(invalid());
            }
            state.jobs.push(Job {
                id: id.clone(),
                argv,
                attempts: 0,
                done: false,
                exit_code: 0,
                stdout: String::new(),
                stderr: String::new(),
            });
            write_state(&dir, &state).map_err(|_| store_error())?;
            Ok(format!("queued {id}\n"))
        }
        "status" => {
            let mut output = String::new();
            for job in &state.jobs {
                if !job.done {
                    output.push_str(&format!("{} pending\n", job.id));
                } else if job.exit_code == 0 {
                    output.push_str(&format!("{} succeeded\n", job.id));
                } else {
                    output.push_str(&format!("{} failed {}\n", job.id, job.exit_code));
                }
            }
            Ok(output)
        }
        "run" => {
            let mut rows = Vec::new();
            for index in 0..state.jobs.len() {
                if state.jobs[index].done {
                    continue;
                }
                state.jobs[index].attempts += 1;
                write_state(&dir, &state).map_err(|_| store_error())?;
                let argv = state.jobs[index].argv.clone();
                let output = Command::new(&argv[0]).args(&argv[1..]).output();
                let (code, stdout, stderr) = match output {
                    Ok(output) => {
                        let code = output
                            .status
                            .code()
                            .unwrap_or_else(|| 128 + output.status.signal().unwrap_or(0));
                        (
                            code,
                            String::from_utf8_lossy(&output.stdout).into_owned(),
                            String::from_utf8_lossy(&output.stderr).into_owned(),
                        )
                    }
                    Err(_) => (127, String::new(), "exec failed\n".into()),
                };
                state.jobs[index].done = true;
                state.jobs[index].exit_code = code;
                state.jobs[index].stdout = stdout;
                state.jobs[index].stderr = stderr;
                let id = state.jobs[index].id.clone();
                let attempt = state.jobs[index].attempts;
                let status = if code == 0 { "succeeded" } else { "failed" };
                rows.push((
                    id,
                    attempt,
                    code,
                    state.jobs[index].stdout.clone(),
                    state.jobs[index].stderr.clone(),
                    status,
                ));
                write_state(&dir, &state).map_err(|_| store_error())?;
            }
            let mut output = String::new();
            for (id, attempt, exit_code, stdout, stderr, status) in &rows {
                output.push_str(
                    &serde_json::to_string(&ResultLine {
                        id,
                        attempt: *attempt,
                        exit_code: *exit_code,
                        stdout,
                        stderr,
                        status,
                    })
                    .map_err(|_| store_error())?,
                );
                output.push('\n');
            }
            Ok(output)
        }
        _ => Err(invalid()),
    }
}

fn parse(args: &[String]) -> Option<(String, std::collections::HashMap<String, String>)> {
    if args.len() < 2 || args[0] != "queue" {
        return None;
    }
    let command = args[1].clone();
    if !["add", "run", "status"].contains(&command.as_str()) {
        return None;
    }
    let mut values = std::collections::HashMap::new();
    let mut index = 2;
    while index < args.len() {
        let key = &args[index];
        let allowed = key == "--store" || (command == "add" && (key == "--id" || key == "--argv"));
        if !allowed || index + 1 >= args.len() || values.contains_key(key) {
            return None;
        }
        index += 1;
        values.insert(key.clone(), args[index].clone());
        index += 1;
    }
    let store = values.get("--store")?;
    if store.is_empty() {
        return None;
    }
    if command == "add" {
        let id = values.get("--id")?;
        if !valid_id(id) || values.get("--argv")?.is_empty() {
            return None;
        }
    } else if values.len() != 1 {
        return None;
    }
    Some((command, values))
}
fn valid_id(id: &str) -> bool {
    let bytes = id.as_bytes();
    !bytes.is_empty()
        && bytes.len() <= 64
        && bytes[0].is_ascii_alphanumeric()
        && bytes
            .iter()
            .all(|byte| byte.is_ascii_alphanumeric() || b"._-".contains(byte))
}
fn read_state(dir: &Path) -> std::io::Result<State> {
    match fs::read(dir.join("state.json")) {
        Ok(data) => serde_json::from_slice(&data).map_err(std::io::Error::other),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(State::default()),
        Err(error) => Err(error),
    }
}
fn write_state(dir: &Path, state: &State) -> std::io::Result<()> {
    let data = serde_json::to_vec(state).map_err(std::io::Error::other)?;
    let temp = dir.join(format!(".state-{}.tmp", std::process::id()));
    let _ = fs::remove_file(&temp);
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&temp)?;
    let outcome = (|| {
        file.write_all(&data)?;
        file.sync_all()?;
        fs::rename(&temp, dir.join("state.json"))?;
        File::open(dir)?.sync_all()
    })();
    if outcome.is_err() {
        let _ = fs::remove_file(&temp);
    }
    outcome
}
