import os
import shutil
import subprocess
from pathlib import Path

import pytest


BIN = os.environ["KOGEN_TASK_BIN"]


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=True).stdout.strip()


def repo(tmp_path):
    p = tmp_path / "repo"
    p.mkdir()
    git_init = subprocess.run(["git", "init", "-q", "-b", "main", str(p)], text=True, capture_output=True)
    assert git_init.returncode == 0
    git(p, "config", "user.name", "Task Test")
    git(p, "config", "user.email", "task@example.invalid")
    (p / "base.txt").write_text("base\n")
    git(p, "add", ".")
    git(p, "commit", "-qm", "base")
    base = git(p, "rev-parse", "HEAD")
    return p, base


def commit(repo, file, content, message):
    (repo / file).write_text(content)
    git(repo, "add", file)
    git(repo, "commit", "-qm", message)
    return git(repo, "rev-parse", "HEAD")


def candidate(repo, base, file="candidate.txt", content="candidate\n"):
    git(repo, "checkout", "-q", "-b", "candidate", base)
    oid = commit(repo, file, content, "candidate")
    git(repo, "checkout", "-q", "main")
    return oid


def run(repo, base, cand, *extra, env=None):
    return subprocess.run(
        [BIN, "--repo", str(repo), "--target", "refs/heads/main", "--base", base, "--candidate", cand, *extra],
        text=True, capture_output=True, env=env,
    )


def test_clean_land_uses_candidate_oid(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    r = run(p, base, cand)
    assert (r.returncode, r.stdout, r.stderr) == (0, f"landed {cand}\n", "")
    assert git(p, "rev-parse", "refs/heads/main") == cand


def test_landed_commit_is_target_head(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    run(p, base, cand)
    assert git(p, "show", "refs/heads/main:candidate.txt") == "candidate"


def test_moved_base_rebases_and_preserves_both_changes(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    moved = commit(p, "target.txt", "target\n", "target moved")
    r = run(p, base, cand)
    landed = git(p, "rev-parse", "refs/heads/main")
    assert (r.returncode, r.stdout, r.stderr) == (10, f"rebased {landed}\n", "")
    assert git(p, "rev-parse", f"{landed}^1") == moved
    assert git(p, "show", f"{landed}:candidate.txt") == "candidate"


def test_clean_rebase_uses_new_commit_oid(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    commit(p, "target.txt", "target\n", "target moved")
    r = run(p, base, cand)
    assert r.returncode == 10
    assert r.stdout.startswith("rebased ") and r.stdout.endswith("\n")
    assert r.stdout.split()[1] != cand


def test_conflict_has_exact_result_and_keeps_target(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base, "base.txt", "candidate side\n")
    moved = commit(p, "base.txt", "target side\n", "target moved")
    r = run(p, base, cand)
    assert (r.returncode, r.stdout, r.stderr) == (20, "", "cas-land: conflict\n")
    assert git(p, "rev-parse", "refs/heads/main") == moved


def test_lost_race_during_rebase_is_atomic(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    moved = commit(p, "target.txt", "initial move\n", "target moved")
    git(p, "checkout", "-q", "-b", "rival")
    rival = commit(p, "rival.txt", "rival\n", "rival")
    git(p, "checkout", "-q", "main")
    shim = tmp_path / "bin"
    shim.mkdir()
    wrapper = shim / "git"
    real_git = shutil.which("git")
    wrapper.write_text(
        "#!/bin/sh\n"
        "if [ \"$1\" = -C ] && [ \"$3\" = update-ref ] && [ \"$4\" = refs/heads/main ]; then\n"
        f"  {real_git} -C '{p}' update-ref refs/heads/main {rival}\n"
        "fi\n"
        f"exec {real_git} \"$@\"\n"
    )
    wrapper.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = f"{shim}:{env['PATH']}"
    r = run(p, base, cand, env=env)
    assert (r.returncode, r.stdout, r.stderr) == (30, "", "cas-land: lost race\n")
    assert git(p, "rev-parse", "refs/heads/main") == rival
    assert git(p, "rev-parse", moved) == moved


@pytest.mark.parametrize("args", [[], ["--repo"], ["--wat", "x"], ["--repo", "x", "--repo", "y"]])
def test_usage_errors_are_exact(tmp_path, args):
    r = subprocess.run([BIN, *args], text=True, capture_output=True)
    assert (r.returncode, r.stdout, r.stderr) == (2, "", "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n")


def test_options_can_be_reordered(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    r = subprocess.run([BIN, "--candidate", cand, "--base", base, "--target", "refs/heads/main", "--repo", str(p)], text=True, capture_output=True)
    assert (r.returncode, r.stdout, r.stderr) == (0, f"landed {cand}\n", "")


def test_wrong_candidate_parent_is_invalid(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    git(p, "checkout", "-q", "-b", "other", base)
    other_base = commit(p, "other.txt", "other\n", "other")
    r = run(p, other_base, cand)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "cas-land: invalid repository or commit\n")


def test_bad_repo_is_invalid(tmp_path):
    r = subprocess.run([BIN, "--repo", str(tmp_path), "--target", "refs/heads/main", "--base", "abc", "--candidate", "def"], text=True, capture_output=True)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "cas-land: invalid repository or commit\n")


def test_missing_target_ref_is_invalid(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    r = subprocess.run([BIN, "--repo", str(p), "--target", "refs/heads/missing", "--base", base, "--candidate", cand], text=True, capture_output=True)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "cas-land: invalid repository or commit\n")


def test_candidate_with_two_parents_is_invalid(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    git(p, "checkout", "-q", "-b", "side", base)
    side = commit(p, "side.txt", "side\n", "side")
    git(p, "checkout", "-q", "candidate")
    git(p, "merge", "--no-ff", "-m", "merge", side)
    merge = git(p, "rev-parse", "HEAD")
    git(p, "checkout", "-q", "main")
    r = run(p, base, merge)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "cas-land: invalid repository or commit\n")


def test_extra_positional_argument_is_usage_error(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base)
    r = run(p, base, cand, "extra")
    assert (r.returncode, r.stdout, r.stderr) == (2, "", "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n")


def test_duplicate_flag_after_empty_value_is_usage_error(tmp_path):
    r = subprocess.run([BIN, "--repo", "", "--repo", "x", "--target", "refs/heads/main", "--base", "a", "--candidate", "b"], text=True, capture_output=True)
    assert (r.returncode, r.stdout, r.stderr) == (2, "", "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n")


def test_conflict_leaves_no_unmerged_target_index(tmp_path):
    p, base = repo(tmp_path)
    cand = candidate(p, base, "base.txt", "candidate side\n")
    commit(p, "base.txt", "target side\n", "target moved")
    r = run(p, base, cand)
    assert r.returncode == 20
    assert git(p, "status", "--porcelain") == ""
