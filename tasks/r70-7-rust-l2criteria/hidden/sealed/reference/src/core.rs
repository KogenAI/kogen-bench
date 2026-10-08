use std::collections::{BTreeMap, BTreeSet};

const HELP: &str = "Usage: kogen <command> [options] [FILE|-]\nCommands:\n  sum     Sum signed integers.\n  status  Count job states.\nOptions:\n  -h, --help  Show help.\n  --version   Show version.\n";
const SUM_HELP: &str = "Usage: kogen sum [--scale N] [--format text|json] [FILE|-]\nSum one signed integer per nonempty line (default scale: 1).\n";
const STATUS_HELP: &str = "Usage: kogen status [--format text|json] [FILE|-]\nCount ID,STATE records (states: queued,running,done,failed).\n";
type Failure = (i32, String);

#[derive(Default)]
struct Options {
    command: String,
    json: bool,
    path: Option<String>,
    scale: i64,
}

enum Parsed {
    Early(String),
    Run(Options),
}

fn parse_options(args: &[String]) -> Result<Parsed, String> {
    if args.is_empty() || args == ["--help"] || args == ["-h"] {
        return Ok(Parsed::Early(HELP.into()));
    }
    if args == ["--version"] {
        return Ok(Parsed::Early("kogen 1.0.0\n".into()));
    }
    let command = &args[0];
    if command != "sum" && command != "status" {
        let kind = if command.starts_with('-') {
            "option"
        } else {
            "command"
        };
        return Err(format!("kogen: unknown {kind} '{command}'"));
    }
    if args.len() == 2 && (args[1] == "--help" || args[1] == "-h") {
        return Ok(Parsed::Early(
            if command == "sum" {
                SUM_HELP
            } else {
                STATUS_HELP
            }
            .into(),
        ));
    }
    let mut opts = Options {
        command: command.clone(),
        scale: 1,
        ..Options::default()
    };
    let mut seen = BTreeSet::new();
    let mut pos = 1;
    while pos < args.len() {
        let arg = &args[pos];
        if arg == "--format" || (arg == "--scale" && command == "sum") {
            if !seen.insert(arg) {
                return Err(format!("kogen: duplicate option '{arg}'"));
            }
            pos += 1;
            let value = args
                .get(pos)
                .ok_or_else(|| format!("kogen: option '{arg}' requires a value"))?;
            let valid = if arg == "--format" {
                opts.json = value == "json";
                value == "text" || value == "json"
            } else {
                let n = value.parse::<i64>();
                let canonical = value == "0"
                    || (!value.starts_with('0')
                        && !value.is_empty()
                        && value.bytes().all(|b| b.is_ascii_digit()));
                if let Ok(n) = n {
                    opts.scale = n;
                }
                canonical && matches!(n, Ok(0..=100))
            };
            if !valid {
                return Err(format!("kogen: invalid value for '{arg}': '{value}'"));
            }
        } else if arg.starts_with('-') && arg != "-" {
            return Err(format!("kogen: unknown option '{arg}'"));
        } else if opts.path.is_some() {
            return Err("kogen: expected at most one input path".into());
        } else {
            opts.path = Some(arg.clone());
        }
        pos += 1;
    }
    Ok(Parsed::Run(opts))
}

pub fn execute(args: &[String]) -> Result<String, Failure> {
    let opts = match parse_options(args).map_err(|e| (2, e))? {
        Parsed::Early(text) => return Ok(text),
        Parsed::Run(opts) => opts,
    };
    let raw = crate::load(opts.path.as_deref(), "kogen").map_err(|e| (1, e))?;
    if !raw.is_ascii() {
        return Err((1, "kogen: input is not ASCII".into()));
    }
    let text = String::from_utf8(raw).map_err(|_| (1, "kogen: input is not ASCII".into()))?;
    aggregate(&text, &opts).map_err(|e| (1, e))
}

fn aggregate(text: &str, opts: &Options) -> Result<String, String> {
    if opts.command == "sum" {
        let mut total = 0_i64;
        for (i, line) in crate::physical_lines(text).into_iter().enumerate() {
            if line.is_empty() {
                continue;
            }
            let digits = line.strip_prefix(['+', '-']).unwrap_or(line);
            let magnitude = digits.trim_start_matches('0');
            let magnitude = if magnitude.is_empty() { "0" } else { magnitude };
            let parsed = magnitude.parse::<i64>();
            if digits.is_empty()
                || !digits.bytes().all(|b| b.is_ascii_digit())
                || !matches!(parsed, Ok(0..=1_000_000))
            {
                return Err(format!(
                    "kogen:{}: expected integer -1000000..1000000",
                    i + 1
                ));
            }
            let n = parsed
                .map_err(|_| format!("kogen:{}: expected integer -1000000..1000000", i + 1))?;
            total += if line.starts_with('-') { -n } else { n };
        }
        total *= opts.scale;
        return Ok(if opts.json {
            format!("{{\"sum\":{total}}}\n")
        } else {
            format!("sum={total}\n")
        });
    }
    let mut counts = BTreeMap::from([("queued", 0), ("running", 0), ("done", 0), ("failed", 0)]);
    let mut ids = BTreeSet::new();
    for (i, line) in crate::physical_lines(text).into_iter().enumerate() {
        if line.is_empty() {
            continue;
        }
        let malformed = || format!("kogen:{}: expected ID,STATE", i + 1);
        let (id, state) = line.split_once(',').ok_or_else(malformed)?;
        if !(1..=32).contains(&id.len())
            || !id.as_bytes()[0].is_ascii_lowercase()
            || !id
                .bytes()
                .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b"_-".contains(&b))
            || !counts.contains_key(state)
        {
            return Err(malformed());
        }
        if !ids.insert(id) {
            return Err(format!("kogen:{}: duplicate id '{id}'", i + 1));
        }
        if let Some(count) = counts.get_mut(state) {
            *count += 1;
        }
    }
    let total = ids.len();
    let (queued, running, done, failed) = (
        counts["queued"],
        counts["running"],
        counts["done"],
        counts["failed"],
    );
    Ok(if opts.json {
        format!(
            "{{\"total\":{total},\"queued\":{queued},\"running\":{running},\"done\":{done},\"failed\":{failed}}}\n"
        )
    } else {
        format!("total={total}\nqueued={queued}\nrunning={running}\ndone={done}\nfailed={failed}\n")
    })
}
