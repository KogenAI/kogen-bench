use std::process::{Command, Output};

const USAGE: &str = "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID";
const INVALID: &str = "cas-land: invalid repository or commit";

fn git(repo: &str, args: &[&str]) -> Result<String, ()> {
    let output = Command::new("git")
        .arg("-C")
        .arg(repo)
        .args(args)
        .output()
        .map_err(|_| ())?;
    if !output.status.success() {
        return Err(());
    }
    Ok(String::from_utf8_lossy(&output.stdout).trim().to_owned())
}

fn git_output(repo: &str, args: &[&str]) -> Result<Output, ()> {
    Command::new("git")
        .arg("-C")
        .arg(repo)
        .args(args)
        .output()
        .map_err(|_| ())
}

fn cleanup(repo: &str, work: &str) {
    let _ = git(repo, &["worktree", "remove", "--force", work]);
    let _ = std::fs::remove_dir_all(work);
}

fn do_land(args: &[String]) -> Result<(String, i32), (i32, String)> {
    let mut repo = None;
    let mut target = None;
    let mut base = None;
    let mut candidate = None;
    let mut i = 0;
    while i < args.len() {
        let slot = match args[i].as_str() {
            "--repo" => &mut repo,
            "--target" => &mut target,
            "--base" => &mut base,
            "--candidate" => &mut candidate,
            _ => return Err((2, USAGE.to_owned())),
        };
        if slot.is_some() || i + 1 == args.len() || args[i + 1].is_empty() {
            return Err((2, USAGE.to_owned()));
        }
        *slot = Some(args[i + 1].clone());
        i += 2;
    }
    let (Some(repo), Some(target), Some(base), Some(candidate)) = (repo, target, base, candidate)
    else {
        return Err((2, USAGE.to_owned()));
    };
    if !target.starts_with("refs/") || git(&repo, &["check-ref-format", &target]).is_err() {
        return Err((1, INVALID.to_owned()));
    }
    let parents = git(&repo, &["rev-list", "--parents", "-n", "1", &candidate])
        .map_err(|_| (1, INVALID.to_owned()))?;
    let fields: Vec<&str> = parents.split_whitespace().collect();
    if fields.len() != 2 || fields[1] != base {
        return Err((1, INVALID.to_owned()));
    }
    let current =
        git(&repo, &["rev-parse", "--verify", &target]).map_err(|_| (1, INVALID.to_owned()))?;
    let rebased = current != base;
    let mut new_oid = candidate.clone();
    if rebased {
        let work = std::env::temp_dir().join(format!(
            "cas-land-{}-{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_nanos()
        ));
        let work = work.to_string_lossy().into_owned();
        if git(&repo, &["worktree", "add", "--detach", &work, &candidate]).is_err() {
            return Err((1, INVALID.to_owned()));
        }
        let rebase = git_output(&work, &["rebase", "--onto", &current, &base]);
        match rebase {
            Ok(result) if result.status.success() => {
                new_oid =
                    git(&work, &["rev-parse", "HEAD"]).map_err(|_| (1, INVALID.to_owned()))?;
                cleanup(&repo, &work);
            }
            _ => {
                let conflict = git(&work, &["diff", "--name-only", "--diff-filter=U"])
                    .map(|s| !s.is_empty())
                    .unwrap_or(false);
                let _ = git(&work, &["rebase", "--abort"]);
                cleanup(&repo, &work);
                if conflict {
                    return Err((20, "cas-land: conflict".to_owned()));
                }
                return Err((1, INVALID.to_owned()));
            }
        }
    }
    if git(&repo, &["update-ref", &target, &new_oid, &current]).is_err() {
        return Err((30, "cas-land: lost race".to_owned()));
    }
    Ok((
        format!(
            "{} {}\n",
            if rebased { "rebased" } else { "landed" },
            new_oid
        ),
        if rebased { 10 } else { 0 },
    ))
}

pub fn execute(args: &[String]) -> Result<(String, i32), (i32, String)> {
    do_land(args)
}
