import importlib.util
import os
import socket
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("control-worker.py")
SPEC = importlib.util.spec_from_file_location("control_worker", MODULE_PATH)
control_worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control_worker)


class ReferenceRootTests(unittest.TestCase):
    def test_returns_real_nested_makefile_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            reference = Path(temporary) / "reference"
            root = reference / "rust" / "r70-1-rust"
            root.mkdir(parents=True)
            (root / "Makefile").touch()
            self.assertEqual(control_worker.reference_root(reference), root)

    def test_ignores_symlinked_stack_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            reference = base / "reference"
            elsewhere = base / "elsewhere"
            (elsewhere / "r70-1-rust").mkdir(parents=True)
            (elsewhere / "r70-1-rust" / "Makefile").touch()
            reference.mkdir()
            (reference / "rust").symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaises(RuntimeError):
                control_worker.reference_root(reference)

    def test_rejects_symlinked_reference_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            real = base / "real"
            real.mkdir()
            (real / "Makefile").touch()
            reference = base / "reference"
            reference.symlink_to(real, target_is_directory=True)
            with self.assertRaises(RuntimeError):
                control_worker.reference_root(reference)


class CandidateCopyTests(unittest.TestCase):
    def test_copy_preserves_links_skips_special_files_and_excludes_git(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / "source", root / "target"
            source.mkdir()
            (source / "file.txt").write_text("candidate\n")
            (source / "outside").symlink_to("/dev/zero")
            (source / ".git").mkdir()
            (source / ".git" / "config").write_text("ignored metadata")
            os.mkfifo(source / "pipe")
            sock = socket.socket(socket.AF_UNIX)
            socket_supported = True
            try:
                sock.bind(str(source / "socket"))
            except OSError:
                socket_supported = False
                sock.close()
            try:
                copied = control_worker.copy_candidate_tree(source, target)
            finally:
                if socket_supported:
                    sock.close()
            self.assertEqual(copied, len(b"candidate\n") + len(b"/dev/zero"))
            self.assertEqual((target / "file.txt").read_text(), "candidate\n")
            self.assertTrue((target / "outside").is_symlink())
            self.assertEqual(os.readlink(target / "outside"), "/dev/zero")
            self.assertFalse((target / "pipe").exists())
            if socket_supported:
                self.assertFalse((target / "socket").exists())
            self.assertFalse((target / ".git").exists())

    def test_copy_excludes_build_caches_before_grading(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / "source", root / "candidate"
            source.mkdir()
            (source / "kept.txt").write_text("candidate source\n")
            for name in ("target", "_build", "build"):
                cache = source / name
                cache.mkdir()
                (cache / "cache.bin").write_bytes(b"must not reach grader")
            nested = source / "package"
            nested.mkdir()
            (nested / "build").mkdir()
            (nested / "build" / "cache.bin").write_bytes(b"nested cache")

            copied = control_worker.copy_candidate_tree(source, target)

            self.assertEqual(copied, len(b"candidate source\n"))
            self.assertEqual((target / "kept.txt").read_text(), "candidate source\n")
            for name in ("target", "_build", "build"):
                self.assertFalse((target / name).exists())
            self.assertFalse((target / "package" / "build").exists())

    def test_byte_and_time_caps_raise_copy_errors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            (source / "data").write_bytes(b"0123456789")
            with self.assertRaisesRegex(control_worker.CandidateCopyError, "byte limit"):
                control_worker.copy_candidate_tree(source, root / "too-large", max_bytes=9)
            with self.assertRaisesRegex(control_worker.CandidateCopyError, "second limit"):
                control_worker.copy_candidate_tree(source, root / "too-slow", timeout_seconds=0)

    def test_copy_error_result_is_a_failed_grade_with_reason(self):
        record = control_worker.copy_error_record("sample", "copy exceeded byte limit")
        self.assertEqual(record["task"], "sample")
        self.assertIs(record["pass_"], False)
        self.assertEqual(record["stage"], "copy-error")
        self.assertEqual(record["reason"], "copy exceeded byte limit")


if __name__ == "__main__":
    unittest.main()
