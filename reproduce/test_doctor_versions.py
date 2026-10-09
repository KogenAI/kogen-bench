import subprocess
import tempfile
import unittest
from pathlib import Path


DOCTOR = Path(__file__).with_name("doctor.sh")


class ErlangVersionTests(unittest.TestCase):
    def test_requires_successful_command(self):
        function = next(
            line for line in DOCTOR.read_text().splitlines()
            if line.startswith("erlang_version() {")
        )
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for name, status, expected in (("fail", 1, False), ("pass", 0, True)):
                executable = directory / name
                executable.write_text(f"#!/bin/sh\necho 29\nexit {status}\n")
                executable.chmod(0o755)
                result = subprocess.run(
                    ["bash", "-c", f"{function}; erlang_version \"$1\"", "test", str(executable)],
                    check=False,
                )
                self.assertEqual(result.returncode == 0, expected, name)


if __name__ == "__main__":
    unittest.main()
