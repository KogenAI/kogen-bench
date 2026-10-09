import importlib.util
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


if __name__ == "__main__":
    unittest.main()
