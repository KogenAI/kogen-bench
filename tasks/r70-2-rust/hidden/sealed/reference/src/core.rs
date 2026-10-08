use std::fs;
use std::os::unix::process::{CommandExt, ExitStatusExt};
use std::process::{Command, Stdio};
use std::sync::mpsc;
use std::thread;
use std::time::{Duration, Instant};

unsafe extern "C" {
    fn kill(pid: i32, signal: i32) -> i32;
}

pub fn execute(args: &[String]) -> Result<(i32, String), (i32, String)> {
    let invalid = || (2, "error: invalid arguments".to_owned());
    if args.len() < 7
        || args[0] != "supervise"
        || args[1] != "--timeout-ms"
        || args[3] != "--grace-ms"
        || args[5] != "--"
        || args[6].is_empty()
    {
        return Err(invalid());
    }
    let Some(timeout_ms) = parse_ms(&args[2]) else {
        return Err(invalid());
    };
    let Some(grace_ms) = parse_ms(&args[4]) else {
        return Err(invalid());
    };
    let mut command = Command::new(&args[6]);
    command
        .args(&args[7..])
        .stdin(Stdio::null())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit());
    command.process_group(0);
    let mut child = command
        .spawn()
        .map_err(|_| (127, "error: cannot start command".to_owned()))?;
    let pgid = child.id() as i32;
    let (sender, receiver) = mpsc::channel();
    thread::spawn(move || {
        let code = child.wait().map(exit_code).unwrap_or(1);
        let _ = sender.send(code);
    });
    let deadline = Instant::now() + Duration::from_millis(timeout_ms);
    loop {
        if !group_live(pgid) {
            let code = receiver.recv().unwrap_or(1);
            return Ok((
                code,
                format!(
                    "status=exited exit_code={code} term_sent=false kill_sent=false reaped=1\n"
                ),
            ));
        }
        if Instant::now() >= deadline {
            break;
        }
        thread::sleep(Duration::from_millis(5));
    }
    signal_group(pgid, 15);
    let grace_deadline = Instant::now() + Duration::from_millis(grace_ms);
    while Instant::now() < grace_deadline {
        thread::sleep(Duration::from_millis(5));
    }
    let kill_sent = group_live(pgid);
    if kill_sent {
        signal_group(pgid, 9);
        while group_live(pgid) {
            thread::sleep(Duration::from_millis(5));
        }
    }
    let _ = receiver.recv();
    Ok((
        124,
        format!("status=timeout exit_code=124 term_sent=true kill_sent={kill_sent} reaped=1\n"),
    ))
}

fn parse_ms(value: &str) -> Option<u64> {
    if value.is_empty() || !value.bytes().all(|byte| byte.is_ascii_digit()) {
        return None;
    }
    value
        .parse::<u64>()
        .ok()
        .filter(|value| (1..=60_000).contains(value))
}
fn exit_code(status: std::process::ExitStatus) -> i32 {
    status
        .code()
        .unwrap_or_else(|| 128 + status.signal().unwrap_or(0))
}
fn signal_group(pgid: i32, signal: i32) {
    // SAFETY: negative pid addresses the unique child process group.
    unsafe {
        kill(-pgid, signal);
    }
}
fn group_live(pgid: i32) -> bool {
    let Ok(entries) = fs::read_dir("/proc") else {
        return false;
    };
    for entry in entries.flatten() {
        if entry.file_name().to_string_lossy().parse::<u32>().is_err() {
            continue;
        }
        let Ok(stat) = fs::read_to_string(entry.path().join("stat")) else {
            continue;
        };
        let Some((_, tail)) = stat.rsplit_once(')') else {
            continue;
        };
        let fields: Vec<&str> = tail.split_whitespace().collect();
        if fields.len() >= 3
            && fields[0] != "Z"
            && fields[0] != "X"
            && fields[2].parse::<i32>().ok() == Some(pgid)
        {
            return true;
        }
    }
    false
}
