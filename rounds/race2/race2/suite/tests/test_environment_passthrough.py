import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kogen_conformance.gherkin_runner import run_gherkin_case
from kogen_conformance.quint_runner import ITFMap, TraceWorld, Variant, SUITE_ROOT, load_quint_cases
from kogen_conformance.runner import run_case


class EnvironmentPassthroughTest(unittest.TestCase):
    def test_toolchain_path_and_homes_reach_each_runner(self):
        with tempfile.TemporaryDirectory(prefix="kc2-env-passthrough-") as directory:
            root = Path(directory)
            real_home = root / "real-home"
            (real_home / ".cargo").mkdir(parents=True)
            (real_home / ".rustup").mkdir()
            tools = root / "host-tools"
            tools.mkdir()
            cargo = tools / "cargo"
            cargo.write_text("#!/bin/sh\necho cargo fake-1\n", encoding="utf-8")
            cargo.chmod(0o755)
            inherited_path = os.pathsep.join((str(tools), os.environ.get("PATH", os.defpath)))
            launcher = root / "kogen-launcher"
            launcher.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = version ]; then cargo --version >/dev/null || exit 95; echo 'kogen test'; exit 0; fi\n"
                f"test \"$RUSTUP_HOME\" = '{real_home / '.rustup'}' || exit 91\n"
                f"test \"$CARGO_HOME\" = '{real_home / '.cargo'}' || exit 92\n"
                f"test \"$GOROOT\" = '{root / 'go-root'}' || exit 93\n"
                "test \"$GOTOOLCHAIN\" = local || exit 94\n"
                "case \"$KOGEN_PROVIDER_URL\" in *host-secret*) exit 96 ;; esac\n"
                "cargo --version >/dev/null || exit 95\n"
                "echo launcher-ok\n",
                encoding="utf-8",
            )
            launcher.chmod(0o755)
            expected = {
                "HOME": str(real_home), "PATH": inherited_path,
                "GOROOT": str(root / "go-root"), "GOTOOLCHAIN": "local",
                "KOGEN_PROVIDER_URL": "https://host-secret.invalid/should-not-pass",
            }
            absent = ("RUSTUP_HOME", "CARGO_HOME")
            saved = {key: os.environ.get(key) for key in (*expected, *absent)}
            try:
                os.environ.update(expected)
                for key in absent:
                    os.environ.pop(key, None)
                for name in ("legacy-work", "gherkin-work", "quint-work"):
                    (root / name).mkdir()
                with patch.dict(os.environ, {}, clear=False):
                    legacy = run_case({
                        "id": "env.legacy-launcher", "title": "Legacy toolchain launcher",
                        "steps": [{"argv": ["probe"], "expect": {"exit": 0}}],
                    }, str(launcher), time_scale=0.01, keep=False, timeout_s=5,
                       workdir=root / "legacy-work")
                    self.assertEqual(legacy["status"], "pass", legacy.get("failures"))

                    gherkin = run_gherkin_case({
                        "id": "feature.env.toolchain-launcher", "title": "Gherkin toolchain launcher",
                        "_feature_steps": [
                            {"keyword": "Given", "line": 1,
                             "text": 'a temporary HOME and a Git repository on branch "main"'},
                            {"keyword": "When", "line": 2, "text": 'I run "kogen version"'},
                            {"keyword": "Then", "line": 3, "text": "the exit code is 0"},
                        ],
                    }, str(launcher), timeout_s=5, keep=False, workdir=root / "gherkin-work")
                    self.assertEqual(gherkin["status"], "pass", gherkin.get("failures"))

                    case = next(case for case in load_quint_cases(SUITE_ROOT / "cases" / "quint" / "init")
                                if case["id"] == "quint.init.seed-20267010")
                    world = TraceWorld(case, str(launcher), 0.01, False, timeout_s=5,
                                       workdir=root / "quint-work")
                    try:
                        env = world._environment(ITFMap(()))
                        self.assertEqual(env["PATH"], os.pathsep.join((str(world.bin), inherited_path)))
                        self.assertEqual(env["RUSTUP_HOME"], str(real_home / ".rustup"))
                        self.assertEqual(env["CARGO_HOME"], str(real_home / ".cargo"))
                        self.assertEqual(env["GOROOT"], expected["GOROOT"])
                        self.assertEqual(env["GOTOOLCHAIN"], "local")
                        self.assertNotEqual(env.get("KOGEN_PROVIDER_URL"), expected["KOGEN_PROVIDER_URL"])
                        completed = subprocess.run(
                            [str(launcher), "probe"], env=env, capture_output=True, text=True, timeout=5)
                        self.assertEqual(completed.returncode, 0, completed.stderr)

                        exact_path = str(tools)
                        override = world._environment(
                            ITFMap((("PATH", Variant("SetEnv", exact_path)),)))
                        self.assertEqual(override["PATH"], exact_path)
                        completed = subprocess.run(
                            [str(launcher), "probe"], env=override,
                            capture_output=True, text=True, timeout=5)
                        self.assertEqual(completed.returncode, 0, completed.stderr)
                    finally:
                        world.close()
            finally:
                for key, value in saved.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
