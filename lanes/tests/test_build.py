import contextlib
import io
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import unittest
from unittest import mock

from lanes import build, common

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
PATCH = "--- a/VERSION\n+++ b/VERSION\n@@ -1 +1 @@\n-1\n+2\n"
BAD_PATCH = "--- a/VERSION\n+++ b/VERSION\n@@ -1 +1 @@\n-9\n+3\n"


def git(cwd, *args):
    return subprocess.run(GIT + list(args), cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class BuildLanes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = os.path.join(self.tmp, "kogen")
        shutil.copytree(os.path.join(FIX, "kogen-repo"), self.repo)
        git(self.repo, "init", "-q")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "one")
        self.sha = git(self.repo, "rev-parse", "HEAD")
        self.home = os.path.join(self.tmp, "home")
        self.counter = os.path.join(self.tmp, "count")
        self.pidfile = os.path.join(self.tmp, "pid")
        env = mock.patch.dict(os.environ, {"KOGEN_LANES_HOME": self.home, "LANE_BUILD_COUNT": self.counter,
                                           "LANE_PID_FILE": self.pidfile})
        env.start()
        self.addCleanup(env.stop)
        table = mock.patch.object(build, "DETECT", [("lane-build.sh", build._build_marker)])
        table.start()
        self.addCleanup(table.stop)
        self.exp = os.path.join(self.tmp, "experiment.json")
        self.run_dir = os.path.join(self.tmp, "run")

    def commit_version(self, text):
        with open(os.path.join(self.repo, "VERSION"), "w") as f:
            f.write(text)
        git(self.repo, "commit", "-q", "-am", text)
        return git(self.repo, "rev-parse", "HEAD")

    def write(self, lanes, patches=None):
        for name, text in (patches or {}).items():
            with open(os.path.join(self.tmp, name), "w") as f:
                f.write(text)
        common.write_json(self.exp, {
            "id": "exp-b", "phase": "shape", "kogen": {"repo": self.repo}, "reps": 1,
            "tasks": ["t"], "deadline_s": 60, "hosts": ["local"], "decision_rule": {"kind": "k"},
            "lanes": [dict({"patch": None, "settings": {}, "sha": self.sha}, **lane) for lane in lanes],
        })

    def run_build(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = build.main([self.exp, "--run-dir", self.run_dir])
        return code, err.getvalue()

    def lock(self):
        return common.read_json(os.path.join(self.run_dir, "lanes.lock.json"))

    def builds(self):
        if not os.path.exists(self.counter):
            return 0
        with open(self.counter) as f:
            return len(f.read().split())

    def test_clean_and_patched_lanes(self):
        self.write([{"name": "base"}, {"name": "p", "patch": "p.patch"}], {"p.patch": PATCH})
        self.assertEqual(self.run_build()[0], 0)
        base, patched = self.lock()
        self.assertEqual(base["kogen_version"], "kogen v1 (test)")
        self.assertEqual(patched["kogen_version"], "kogen v2 (test)")
        self.assertIsNone(base["patch_sha256"])
        self.assertEqual(patched["patch_sha256"], common.sha256_file(os.path.join(self.tmp, "p.patch")))
        self.assertNotEqual(base["artifact_sha256"], patched["artifact_sha256"])
        self.assertEqual(base["sha"], self.sha)
        art = os.path.join(self.home, "artifacts", base["artifact_sha256"], "lane-out")
        self.assertEqual(common.sha256_file(art), base["artifact_sha256"])
        self.assertEqual(os.listdir(os.path.join(self.home, "kogen.git", "worktrees")) if
                         os.path.isdir(os.path.join(self.home, "kogen.git", "worktrees")) else [], [])
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_same_sha_and_patch_share_one_artifact(self):
        self.write([{"name": "a"}, {"name": "b"}])
        self.assertEqual(self.run_build()[0], 0)
        a, b = self.lock()
        self.assertEqual(a["artifact_sha256"], b["artifact_sha256"])
        self.assertEqual(self.builds(), 1)

    def test_patch_that_does_not_apply(self):
        self.write([{"name": "bad", "patch": "bad.patch"}], {"bad.patch": BAD_PATCH})
        code, err = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("does not apply", err)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "lanes.lock.json")))
        self.assertEqual(self.builds(), 0)

    def test_second_run_reuses_the_artifact(self):
        self.write([{"name": "base"}])
        self.assertEqual(self.run_build()[0], 0)
        first = self.lock()
        self.assertEqual(self.run_build()[0], 0)
        self.assertEqual(self.lock(), first)
        self.assertEqual(self.builds(), 1)

    def test_unknown_sha(self):
        self.write([{"name": "x", "sha": "f" * 40}])
        code, err = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("not in", err)

    def test_missing_patch_file(self):
        self.write([{"name": "x", "patch": "nope.patch"}])
        self.assertEqual(self.run_build()[0], 1)

    def test_version_probe_runs_in_its_own_group_with_a_deadline(self):
        sha = self.commit_version("hang\n")
        self.write([{"name": "h", "sha": sha}])
        with mock.patch.object(build, "VERSION_DEADLINE_S", 3):
            code, err = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("timed out", err)
        with open(self.pidfile) as f:
            pid = int(f.read())
        for _ in range(50):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.1)
        else:
            os.kill(pid, 9)
            self.fail("the sleep started by `kogen version` outlived the deadline")

    def test_clone_has_a_deadline_and_leaves_no_partial_clone(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "git"), "w") as f:
            f.write("#!/bin/sh\nmkdir -p \"$(for a; do :; done; echo $a)\"; sleep 30\n")
        os.chmod(os.path.join(bindir, "git"), 0o755)
        self.write([{"name": "base"}])
        with mock.patch.dict(os.environ, {"PATH": bindir + os.pathsep + os.environ["PATH"]}), \
                mock.patch.object(build, "GIT_DEADLINE_S", 1):
            code, err = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("timed out", err)
        self.assertFalse(os.path.exists(os.path.join(self.home, "kogen.git")))

    def test_interrupted_first_clone_leaves_no_temp_dir(self):  # L9
        self.write([{"name": "base"}])
        with mock.patch.object(build, "_git", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                build.ensure_sha(self.repo, self.sha, self.home)
        self.assertEqual(os.listdir(self.home), [])

    def test_sha_reachable_only_from_another_ref(self):
        self.write([{"name": "base"}])
        self.assertEqual(self.run_build()[0], 0)
        git(self.repo, "config", "uploadpack.allowAnySHA1InWant", "true")
        sha2 = self.commit_version("2\n")
        git(self.repo, "update-ref", "refs/pull/1/head", sha2)
        git(self.repo, "reset", "-q", "--hard", self.sha)
        git(self.repo, "reflog", "expire", "--expire=now", "--all")
        self.write([{"name": "pr", "sha": sha2}])
        self.assertEqual(self.run_build()[0], 0)
        self.assertEqual(self.lock()[0]["kogen_version"], "kogen v2 (test)")

    def test_cache_hit_reads_the_stored_version(self):
        self.write([{"name": "base"}])
        self.assertEqual(self.run_build()[0], 0)
        with mock.patch.object(build, "_kogen_version", side_effect=AssertionError("probed")):
            self.assertEqual(self.run_build()[0], 0)
        self.assertEqual(self.lock()[0]["kogen_version"], "kogen v1 (test)")

    def test_go_build_is_reproducible_by_flags(self):
        tree = os.path.join(self.tmp, "gotree")
        os.makedirs(os.path.join(tree, "cmd", "kogen"))
        with open(os.path.join(tree, "cmd", "kogen", "main.go"), "w") as f:
            f.write("package main\n")
        with mock.patch.object(build, "_run") as run:
            build._build_go(tree, "log")
        cmd = run.call_args[0][0]
        self.assertIn("-trimpath", cmd)
        self.assertIn("-buildvcs=false", cmd)

    def _archive_builder(self, payload):
        def builder(tree, log):
            top = os.path.join(tree, "kogen-x")
            os.makedirs(os.path.join(top, "bin"))
            with open(os.path.join(top, "bin", "kogen"), "w") as f:
                f.write(payload)
            os.chmod(os.path.join(top, "bin", "kogen"), 0o755)
            path = os.path.join(tree, "kogen-x.tar.gz")
            with tarfile.open(path, "w:gz") as t:
                t.add(top, arcname="kogen-x")
            return path
        return builder

    def test_archive_version_without_the_tar_data_filter(self):
        self.write([{"name": "base"}])
        real = tarfile.TarFile.extractall

        def old_python(self_, *a, **kw):
            if "filter" in kw:
                raise TypeError("extractall() got an unexpected keyword argument 'filter'")
            return real(self_, *a, filter="fully_trusted", **kw)

        with mock.patch.object(build, "DETECT", [("lane-build.sh", self._archive_builder('#!/bin/sh\necho "kogen a1"\n'))]), \
                mock.patch.object(tarfile, "data_filter", None), \
                mock.patch.object(tarfile.TarFile, "extractall", old_python):
            self.assertEqual(self.run_build()[0], 0)
        self.assertEqual(self.lock()[0]["kogen_version"], "kogen a1")

    def test_corrupt_archive_is_a_message_not_a_traceback(self):
        self.write([{"name": "base"}])

        def builder(tree, log):
            path = os.path.join(tree, "bad.tar.gz")
            with open(path, "w") as f:
                f.write("not a tar")
            return path

        with mock.patch.object(build, "DETECT", [("lane-build.sh", builder)]):
            code, err = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("lanes-build:", err)

    def test_relative_repo_is_taken_from_the_experiment_dir(self):
        self.write([{"name": "base"}])
        exp = common.read_json(self.exp)
        exp["kogen"]["repo"] = "kogen"
        common.write_json(self.exp, exp)
        elsewhere = os.path.join(self.tmp, "elsewhere")
        os.makedirs(elsewhere)
        old = os.getcwd()
        os.chdir(elsewhere)
        self.addCleanup(os.chdir, old)
        self.assertEqual(self.run_build()[0], 0)

    def test_detects_go_main_package(self):
        tree = os.path.join(self.tmp, "gotree")
        os.makedirs(os.path.join(tree, "cli"))
        with open(os.path.join(tree, "cli", "main.go"), "w") as f:
            f.write("package main\n\nfunc main() {}\n")
        self.assertEqual(build._go_main_dir(tree), "./cli")


if __name__ == "__main__":
    unittest.main()
