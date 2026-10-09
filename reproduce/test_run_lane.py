import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GIT_ENV = os.environ.copy()
GIT_ENV.update({
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@" + "example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@" + "example.invalid",
})


class LaneHelpersTest(unittest.TestCase):
    def test_watchdog_invocation_resolves_to_existing_script(self):
        runner = (HERE / "run-lane.sh").read_text()
        invocation = 'python3 "$KIT/reproduce/lane_watchdog.py"'
        self.assertIn(invocation, runner)
        invoked_path = HERE / "lane_watchdog.py"
        self.assertTrue(invoked_path.is_file())

    def test_agent_offline_environment_matches_grader(self):
        runner = (HERE / "run-lane.sh").read_text()
        grader = (HERE / "control-worker.py").read_text()
        pythonpath = "/srv" + "/bh/bench/toolchains/python-3.14.7/lib/python3.14/site-packages"
        for assignment in (
            "GOPROXY=off", "GOTOOLCHAIN=local", "CARGO_NET_OFFLINE=true",
            "RUSTUP_HOME=/opt/bench/rustup",
            "PYTHONPATH=" + pythonpath,
        ):
            with self.subTest(assignment=assignment):
                self.assertIn(assignment, runner)
                key, value = assignment.split("=", 1)
                self.assertIn(f'"{key}": "{value}"', grader)
        self.assertNotIn("GOFLAGS=", runner)

    def test_patch_wrapper_ignores_git_metadata_and_captures_worktree_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo, patch_file = root / "repo", root / "result" / "patch.diff"
            repo.mkdir(); patch_file.parent.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True, env=GIT_ENV)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test"], check=True, env=GIT_ENV)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True, env=GIT_ENV)
            (repo / "tracked.txt").write_text("before\n")
            (repo / "deleted.txt").write_text("remove me\n")
            (repo / ".gitignore").write_text("target/\nnode_modules/\n")
            subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, env=GIT_ENV)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True, env=GIT_ENV)
            base = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True, env=GIT_ENV).strip()
            bundle = root / "base.bundle"
            subprocess.run(["git", "-C", str(repo), "bundle", "create", str(bundle), "--all"], check=True, env=GIT_ENV)
            (repo / "tracked.txt").write_text("after\n")
            (repo / "deleted.txt").unlink()
            (repo / "new.txt").write_text("new file\n")
            (repo / ".gitattributes").write_text("*.txt filter=owned\n")
            marker = root / "filter-ran"
            subprocess.run(["git", "-C", str(repo), "config", "filter.owned.clean", f"touch {marker}; cat"], check=True, env=GIT_ENV)
            (repo / "target").mkdir(); (repo / "target" / "big").write_text("ignored\n")
            (repo / "node_modules").mkdir(); (repo / "node_modules" / "big").write_text("ignored\n")
            fifo = repo / "nested" / "agent.pipe"; fifo.parent.mkdir(); os.mkfifo(fifo)
            sentinel = root / "sentinel"; sentinel.write_text("unchanged\n")
            (repo / ".git").rename(root / "git-real")
            (repo / ".git").symlink_to(root / "git-real", target_is_directory=True)
            (root / "git-real" / "info").rename(root / "git-real" / "info-real")
            (root / "git-real" / "info").symlink_to(sentinel, target_is_directory=True)
            (root / "git-real" / "commondir").symlink_to(sentinel)
            (root / "git-real" / "objects" / "info" / "alternates").parent.mkdir(parents=True, exist_ok=True)
            (root / "git-real" / "objects" / "info" / "alternates").symlink_to(sentinel)
            patch_file.symlink_to(sentinel)

            self._run_wrapper_with_fake_profile(root, base, bundle, repo, patch_file)

            self.assertEqual(sentinel.read_text(), "unchanged\n")
            self.assertFalse(patch_file.is_symlink())
            text = patch_file.read_text()
            for name in ("new.txt", "tracked.txt", "deleted.txt"):
                self.assertIn(name, text)
            self.assertNotIn("target/big", text); self.assertNotIn("node_modules/big", text)
            self.assertFalse(marker.exists())
            target = root / "verify"
            subprocess.run(["git", "clone", "-q", str(bundle), str(target)], check=True, env=GIT_ENV)
            subprocess.run(["git", "-C", str(target), "checkout", "-q", base], check=True, env=GIT_ENV)
            subprocess.run(["git", "-C", str(target), "apply", "--index", str(patch_file)], check=True, env=GIT_ENV)
            self.assertEqual((target / "tracked.txt").read_text(), "after\n")
            self.assertEqual((target / "new.txt").read_text(), "new file\n")
            self.assertFalse((target / "deleted.txt").exists())

    def _run_wrapper_with_fake_profile(self, root, base, bundle, repo, patch_file):
        """Run the public wrapper through a fake profile when bwrap is unavailable."""
        kit = root / "kit" / "reproduce"
        kit.mkdir(parents=True)
        wrapper = kit / "lane-patch.sh"
        shutil.copy2(HERE / "lane-patch.sh", wrapper); wrapper.chmod(0o755)
        profile = kit / "sandbox-profile.sh"
        profile.write_text(
            "#!" + sys.executable + "\n"
            "import subprocess, sys\n"
            "mode, repo, scratch, bundle = sys.argv[1:5]\n"
            "assert mode == 'patch'\n"
            "args = sys.argv[sys.argv.index('--') + 1:]\n"
            "translate = {'/lane-patch.sh': str(__import__('pathlib').Path(__file__).parent / 'lane-patch.sh'), '/input': repo, '/scratch': scratch, '/base.bundle': bundle}\n"
            "args = [translate.get(a, a) for a in args]\n"
            "raise SystemExit(subprocess.call(args, cwd=scratch))\n"
        )
        profile.chmod(0o755)
        timeout = kit / "timeout"
        timeout.write_text("#!/bin/sh\n[ \"$1\" = --signal=KILL ] && shift\n[ \"$1\" = 300 ] && shift\nexec \"$@\"\n")
        timeout.chmod(0o755)
        env = GIT_ENV.copy(); env["PATH"] = str(kit) + os.pathsep + env.get("PATH", "")
        subprocess.run([str(wrapper), base, str(bundle), str(repo), str(patch_file)], check=True, env=env)

    def test_codex_info_reads_version_and_resolved_binary_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            binary = Path(temp) / "codex"
            binary.write_text("#!/bin/sh\nprintf 'codex-cli 0.161.0\\n'\n")
            binary.chmod(0o755)
            result = subprocess.check_output(
                ["python3", str(HERE / "lane-codex-info.py"), str(binary), "0.161.0"],
                text=True,
            ).strip().split("\t")
            self.assertEqual(result, ["0.161.0", "0.161.0", hashlib.sha256(binary.read_bytes()).hexdigest(), "false"])

    def test_patch_wrapper_runs_as_bench_in_grade_style_isolation(self):
        wrapper_path = HERE / "lane-patch.sh"
        wrapper = wrapper_path.read_text()
        profile = (HERE / "sandbox-profile.sh").read_text()
        self.assertIn('sandbox-profile.sh" patch', wrapper)
        self.assertIn("patch)", profile)
        self.assertNotIn('safe.directory=', wrapper)
        self.assertEqual(wrapper_path.stat().st_mode & 0o777, 0o755)
        self.assertIn("/bin/bash /lane-patch.sh --inside", wrapper)
        self.assertIn("/bin/bash /lane-patch.sh --inside", wrapper.split("else", 1)[1])
        self.assertNotIn('"$HERE/lane-patch.sh" --inside', wrapper)
        self.assertIn('--ro-bind "$work_real" /input', profile)
        self.assertIn('--ro-bind "$bundle_real" /base.bundle', profile)
        self.assertIn('! -L $input', profile)

    def test_host_doctor_runs_hostile_lane_check_on_host(self):
        doctor = (HERE / "doctor.sh").read_text()
        self.assertIn('check timeout --signal=KILL 300 bash "$HERE/selftest-lane-hostile.sh"', doctor)
        self.assertTrue((HERE / "selftest-lane-hostile.sh").stat().st_mode & 0o111)

    def test_patch_failure_does_not_skip_grade_or_manifest(self):
        runner = (HERE / "run-lane.sh").read_text()
        self.assertIn("patch extraction failed; see runner stderr", runner)
        self.assertLess(runner.index('if ! timeout --signal=KILL 315 "$KIT/reproduce/lane-patch.sh"'),
                        runner.index('"$KIT/reproduce/control-worker.py"'))
        self.assertIn("patch_error=patch_error or None", runner)
        self.assertIn("capture_failures+=(\"$label\")", runner)
        self.assertIn('capture_failures=capture_failures', runner)
        self.assertIn('capture standard-record python3', runner)
        self.assertIn('capture_failures=capture_failures', runner)
        self.assertIn('capture standard-record python3', runner)

    def test_codex_info_reports_mismatch_without_failing(self):
        with tempfile.TemporaryDirectory() as temp:
            binary = Path(temp) / "codex"
            binary.write_text("#!/bin/sh\nprintf 'codex-cli 0.162.0\\n'\n")
            binary.chmod(0o755)
            result = subprocess.run(
                ["python3", str(HERE / "lane-codex-info.py"), str(binary), "0.161.0"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip().split("\t"), [
                "0.161.0", "0.162.0", hashlib.sha256(binary.read_bytes()).hexdigest(), "true"
            ])


if __name__ == "__main__":
    unittest.main()
