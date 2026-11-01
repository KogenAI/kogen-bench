import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from lanes import cell, gocache

GO = shutil.which("go")
MAIN = 'package main\n\nimport "fmt"\n\nfunc main() { fmt.Println("hi") }\n'


def entries(gocache_dir):
    """Compiled outputs and action records: the files Go adds when it compiles something."""
    return sorted(str(p.relative_to(gocache_dir)) for p in Path(gocache_dir).glob("??/*"))


@unittest.skipUnless(GO, "go is not on PATH")
class GoCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.task = self.root / "tasks" / "hello-go"
        (self.task / "start").mkdir(parents=True)
        (self.task / "task.toml").write_text('name = "hello-go"\n')
        (self.task / "start" / "go.mod").write_text("module example.com/hello\n\ngo 1.21\n")
        (self.task / "start" / "main.go").write_text(MAIN)
        (self.task / "start" / "main_test.go").write_text('package main\n\nimport "testing"\n\nfunc TestX(t *testing.T) {}\n')
        env = patch.dict(os.environ, {"LANES_GO_CACHE": str(self.root / "go-cache"), "GOFLAGS": "", "GOTOOLCHAIN": "local"})
        env.start()
        self.addCleanup(env.stop)
        self.lines = []

    def run_tmp(self, name):
        tmp = self.root / name
        tmp.mkdir()
        return tmp

    def build(self, env, tmp):
        """`go build` in a workspace copy, as Kogen's checks run (never in the task's own start tree)."""
        ws = Path(tmp) / "ws"
        shutil.copytree(self.task / "start", ws)
        return subprocess.run(["go", "build", "./..."], cwd=ws, env=dict(os.environ, **env), capture_output=True, text=True)

    def test_warm_copy_is_private_and_needs_no_compile(self):
        key = gocache.stage(self.task, out=self.lines.append)
        self.assertRegex(key, "^[0-9a-f]{64}$")
        manifest = json.loads((self.root / "go-cache" / key / "manifest.json").read_text())
        self.assertEqual([s["exit"] for s in manifest["steps"]], [0, 0, 0])
        env, info = gocache.prepare(self.task / "start", self.run_tmp("run1"))
        self.assertEqual(info["status"], "warm")
        self.assertEqual(info["gocache_sha256"], manifest["gocache"]["sha256"])
        self.assertEqual(set(env), {"GOCACHE"})
        self.assertTrue(env["GOCACHE"].startswith(str(self.root / "run1")))
        before = entries(env["GOCACHE"])
        self.assertEqual(self.build(env, self.root / "run1").returncode, 0)
        # Only the task's own package (keyed by its new folder) is compiled again; the standard library is reused.
        self.assertGreater(len(before), 100)
        self.assertLess(len(set(entries(env["GOCACHE"])) - set(before)), 20)
        (Path(env["GOCACHE"]) / "README").write_text("run mutation")
        self.assertIsNotNone(gocache.entry_ok(self.root / "go-cache" / key))  # the entry is untouched
        again = gocache.stage(self.task, out=self.lines.append)
        self.assertEqual(again, key)
        self.assertIn(f"hello-go: go cache reuse {key}", self.lines)

    def test_every_run_gets_the_same_entry(self):
        gocache.stage(self.task, out=self.lines.append)
        infos = [gocache.prepare(self.task / "start", self.run_tmp(f"lane{i}"))[1] for i in range(3)]
        self.assertEqual({i["status"] for i in infos}, {"warm"})
        self.assertEqual(len({(i["key"], i["gocache_sha256"], i["manifest_sha256"]) for i in infos}), 1)
        self.assertEqual(len({str(self.root / f"lane{i}" / "go-cache") for i in range(3)}), 3)

    def test_changed_tree_misses_and_builds_cold(self):
        key = gocache.stage(self.task, out=self.lines.append)
        (self.task / "start" / "main.go").write_text(MAIN.replace("hi", "changed"))
        env, info = gocache.prepare(self.task / "start", self.run_tmp("run"))
        self.assertEqual((info["status"], info["reason"]), ("cold", "not staged"))
        self.assertNotEqual(info["key"], key)
        self.assertEqual(os.listdir(env["GOCACHE"]), [])  # private and empty: a cold build
        self.assertEqual(self.build(env, self.root / "run").returncode, 0)

    def test_corrupt_entry_falls_back_cold_and_restages(self):
        key = gocache.stage(self.task, out=self.lines.append)
        entry = self.root / "go-cache" / key
        victim = max((p for p in (entry / "gocache").rglob("*-d") if p.is_file()), key=lambda p: p.stat().st_size)
        data = bytearray(victim.read_bytes())
        data[len(data) // 2] ^= 0xFF  # same size: Go itself would not notice
        victim.write_bytes(bytes(data))
        env, info = gocache.prepare(self.task / "start", self.run_tmp("run"))
        self.assertEqual((info["status"], info["reason"]), ("cold", "copy does not match the manifest"))
        self.assertEqual(os.listdir(env["GOCACHE"]), [])
        self.assertEqual(self.build(env, self.root / "run").returncode, 0)
        self.assertEqual(gocache.stage(self.task, out=self.lines.append), key)
        self.assertTrue(any("moved aside and staged again" in l for l in self.lines))
        self.assertEqual(len(list((self.root / "go-cache").glob(key + ".aside-corrupt-*"))), 1)
        self.assertEqual(gocache.prepare(self.task / "start", self.run_tmp("run2"))[1]["status"], "warm")

    def test_unreadable_manifest_never_raises(self):
        key = gocache.stage(self.task, out=self.lines.append)
        (self.root / "go-cache" / key / "manifest.json").write_text("{not json")
        env, info = gocache.prepare(self.task / "start", self.run_tmp("run"))
        self.assertEqual(info["status"], "cold")
        self.assertIn("JSONDecodeError", info["reason"])
        self.assertTrue(os.path.isdir(env["GOCACHE"]))

    def test_toolchain_is_keyed(self):
        key = gocache.key(self.task)[0]
        with patch.dict(os.environ, {"GOFLAGS": "-trimpath"}):
            self.assertNotEqual(gocache.key(self.task)[0], key)
        with patch.object(gocache, "toolchain", lambda m, e: {"GOVERSION": "go0.0"}):
            self.assertNotEqual(gocache.key(self.task)[0], key)

    def test_no_go_module_or_no_go_leaves_env_as_before(self):
        (self.task / "start" / "go.mod").unlink()
        self.assertEqual(gocache.prepare(self.task / "start", self.run_tmp("a")), ({}, {"schema": 1, "status": "none"}))
        self.assertIsNone(gocache.stage(self.task, out=self.lines.append))
        (self.task / "start" / "go.mod").write_text("module example.com/hello\n\ngo 1.21\n")
        with patch.dict(os.environ, {"PATH": str(self.root)}):
            self.assertEqual(gocache.prepare(self.task / "start", self.run_tmp("b"))[0], {})

    def test_vendor_and_testdata_modules_are_not_staged(self):
        for d in ("vendor/example.com/x", "testdata/mod", "sub"):
            (self.task / "start" / d).mkdir(parents=True)
            (self.task / "start" / d / "go.mod").write_text("module example.com/x\n\ngo 1.21\n")
        self.assertEqual(gocache.modules(self.task / "start"), [".", "sub"])

    def test_staging_failure_does_not_raise(self):
        with patch.object(gocache, "toolchain", side_effect=ValueError("go env failed")):
            self.assertIsNone(gocache.stage(self.task, out=self.lines.append))
        self.assertIn("go cache not staged", self.lines[-1])

    def test_modules_are_downloaded_at_staging_into_the_run_module_cache(self):
        proxy = self.root / "proxy" / "example.com" / "dep" / "@v"
        proxy.mkdir(parents=True)
        (proxy / "list").write_text("v1.0.0\n")
        (proxy / "v1.0.0.info").write_text('{"Version":"v1.0.0","Time":"2026-01-01T00:00:00Z"}')
        (proxy / "v1.0.0.mod").write_text("module example.com/dep\n\ngo 1.21\n")
        with zipfile.ZipFile(proxy / "v1.0.0.zip", "w") as z:
            z.writestr("example.com/dep@v1.0.0/go.mod", "module example.com/dep\n\ngo 1.21\n")
            z.writestr("example.com/dep@v1.0.0/dep.go", 'package dep\n\nconst Name = "dep"\n')
        start = self.task / "start"
        (start / "go.mod").write_text("module example.com/hello\n\ngo 1.21\n\nrequire example.com/dep v1.0.0\n")
        (start / "main.go").write_text('package main\n\nimport "example.com/dep"\n\nfunc main() { println(dep.Name) }\n')
        modcache = self.root / "host-modcache"
        net = {"GOPROXY": (self.root / "proxy").as_uri(), "GOSUMDB": "off", "GOFLAGS": "-mod=mod",
               "GOMODCACHE": str(modcache)}
        with patch.dict(os.environ, net):
            key = gocache.stage(self.task, out=self.lines.append)
            self.assertTrue((modcache / "example.com" / "dep@v1.0.0" / "dep.go").is_file())
            env, info = gocache.prepare(start, self.run_tmp("run"))
            self.assertEqual((info["status"], set(env)), ("warm", {"GOCACHE"}))
            before = set(entries(env["GOCACHE"]))
            self.assertEqual(self.build(dict(env, GOPROXY="off"), self.root / "run").returncode, 0)  # nothing to fetch
            self.assertLess(len(set(entries(env["GOCACHE"])) - before), 20)  # the dependency was a cache hit
            with patch.dict(os.environ, {"GOMODCACHE": str(self.root / "other-modcache")}):
                self.assertNotEqual(gocache.key(self.task)[0], key)  # dependency action IDs include their folder
        for d, _, _ in os.walk(modcache):
            os.chmod(d, 0o755)  # Go extracts modules read-only


class CellEnvTest(unittest.TestCase):
    def test_cell_passes_the_go_env_to_kogen(self):
        with tempfile.TemporaryDirectory() as d:
            c = cell.Cell(d, "/bin/true", d, 60, go_env={"GOCACHE": d + "/go-cache"})
            self.assertEqual(c.env["GOCACHE"], d + "/go-cache")
            self.assertEqual(cell.Cell(d, "/bin/true", d, 60).env.get("GOCACHE"), os.environ.get("GOCACHE"))

    def test_make_workspace_returns_the_go_env(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"LANES_GO_CACHE": d + "/none"}):
            start = Path(d) / "task" / "start"
            start.mkdir(parents=True)
            (start / "README").write_text("no go here\n")
            self.assertEqual(cell.make_workspace(d + "/ws", d, str(start), "version: 1\n")[0], {})


if __name__ == "__main__":
    unittest.main()
