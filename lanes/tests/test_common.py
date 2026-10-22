import os
import subprocess
import sys
import tempfile
import time
import unittest

from lanes import common


class JsonAndHash(unittest.TestCase):
    def test_json_sorted_with_newline(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "sub", "x.json")
            common.write_json(p, {"b": 1, "a": [2]})
            with open(p) as f:
                text = f.read()
            self.assertTrue(text.endswith("\n"))
            self.assertLess(text.index('"a"'), text.index('"b"'))
            self.assertEqual(common.read_json(p), {"a": [2], "b": 1})

    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f")
            with open(p, "w") as f:
                f.write("abc")
            self.assertEqual(
                common.sha256_file(p),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_sha256_tree(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for d in (a, b):
                os.makedirs(os.path.join(d, "s"))
                write(os.path.join(d, "s", "f"), "x")
            os.makedirs(os.path.join(b, ".git"))
            write(os.path.join(b, ".git", "junk"), "y")
            self.assertEqual(common.sha256_tree(a), common.sha256_tree(b))
            write(os.path.join(a, "s", "f"), "changed")
            self.assertNotEqual(common.sha256_tree(a), common.sha256_tree(b))
            write(os.path.join(a, "s", "f"), "x")
            os.chmod(os.path.join(a, "s", "f"), 0o755)
            self.assertNotEqual(common.sha256_tree(a), common.sha256_tree(b))


    def test_sha256_tree_symlinks(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for d in (a, b):
                for sub in ("one", "two"):
                    os.makedirs(os.path.join(d, sub))
                    write(os.path.join(d, sub, "f"), "x")
            plain = common.sha256_tree(a)
            os.symlink("one", os.path.join(a, "link"))  # a link to a directory counts
            linked_one = common.sha256_tree(a)
            self.assertNotEqual(linked_one, plain)
            os.remove(os.path.join(a, "link"))
            os.symlink("two", os.path.join(a, "link"))  # and so does its target
            self.assertNotEqual(common.sha256_tree(a), linked_one)
            os.remove(os.path.join(a, "link"))
            os.symlink("missing", os.path.join(a, "link"))  # dangling is fine
            self.assertNotEqual(common.sha256_tree(a), plain)


class Paths(unittest.TestCase):
    def test_home_env_and_default(self):
        old = os.environ.get("KOGEN_LANES_HOME")
        try:
            os.environ["KOGEN_LANES_HOME"] = "/tmp/kl-home"
            self.assertEqual(common.runs_dir("e1"), "/tmp/kl-home/runs/e1")
            self.assertEqual(common.cell_dir("/r", "t/r1/base"), "/r/cells/t/r1/base")
            del os.environ["KOGEN_LANES_HOME"]
            self.assertTrue(common.lanes_home().endswith(".cache/kogen-lanes"))
        finally:
            if old is None:
                os.environ.pop("KOGEN_LANES_HOME", None)
            else:
                os.environ["KOGEN_LANES_HOME"] = old


def write(path, text):
    with open(path, "w") as f:
        f.write(text)


def read(path):
    with open(path) as f:
        return f.read()


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


class Run(unittest.TestCase):
    def test_exit_code(self):
        self.assertEqual(common.run([sys.executable, "-c", "raise SystemExit(3)"]), (3, False))

    def test_deadline_kills_group(self):
        # The child starts a grandchild that records its pid, then both sleep.
        with tempfile.TemporaryDirectory() as d:
            pidfile = os.path.join(d, "pid")
            code = (
                "import subprocess,sys,time\n"
                "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])\n"
                f"open({pidfile!r},'w').write(str(p.pid))\n"
                "time.sleep(60)\n"
            )
            t0 = time.monotonic()
            exit_code, timed_out = common.run([sys.executable, "-c", code], deadline_s=1.5)
            self.assertTrue(timed_out)
            self.assertLess(time.monotonic() - t0, 20)
            pid = int(read(pidfile))
            for _ in range(50):
                if not alive(pid):
                    break
                time.sleep(0.1)
            self.assertFalse(alive(pid), "grandchild survived the deadline")

    def test_leftover_child_killed_after_leader_exits(self):
        with tempfile.TemporaryDirectory() as d:
            pidfile = os.path.join(d, "pid")
            code = (
                "import subprocess,sys\n"
                "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])\n"
                f"open({pidfile!r},'w').write(str(p.pid))\n"
            )
            self.assertEqual(common.run([sys.executable, "-c", code], deadline_s=30), (0, False))
            pid = int(read(pidfile))
            for _ in range(50):
                if not alive(pid):
                    break
                time.sleep(0.1)
            self.assertFalse(alive(pid))

    def test_interrupt_kills_group(self):
        # Run common.run in a subprocess, interrupt it, and check its child dies.
        with tempfile.TemporaryDirectory() as d:
            pidfile = os.path.join(d, "pid")
            script = (
                "import sys\n"
                f"sys.path.insert(0,{os.path.dirname(os.path.dirname(common.__file__))!r})\n"
                "from lanes import common\n"
                "child='import sys,time;open(sys.argv[1],\"w\").write(str(__import__(\"os\").getpid()));time.sleep(60)'\n"
                "common.run([sys.executable,'-c',child,sys.argv[1]])\n"
            )
            proc = subprocess.Popen([sys.executable, "-c", script, pidfile], stderr=subprocess.DEVNULL)
            for _ in range(100):
                if os.path.exists(pidfile) and os.path.getsize(pidfile):
                    break
                time.sleep(0.1)
            time.sleep(0.2)
            pid = int(read(pidfile))
            proc.send_signal(2)  # SIGINT -> KeyboardInterrupt in the parent
            proc.wait(timeout=20)
            for _ in range(50):
                if not alive(pid):
                    break
                time.sleep(0.1)
            self.assertFalse(alive(pid))


if __name__ == "__main__":
    unittest.main()
