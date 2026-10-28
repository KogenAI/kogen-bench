import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import cell, ccroute, common, costguard, experiment
from tests import test_cell, test_dispatch, test_preflight, test_providers

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE_CLAUDE = os.path.join(HERE, "fixtures", "fake-claude")
FAKE_SSH = os.path.join(HERE, "fixtures", "fake-ssh")
DRY = os.path.join(HERE, "..", "bin", "lanes-ccdry")
CC = "claude-code/claude-sonnet-5-5 medium"
SSH = [FAKE_SSH]


def slurp(path):
    with open(path) as f:
        return f.read()


class RoleMapping(unittest.TestCase):
    def test_a_claude_code_role_writes_the_executor_keys(self):
        self.assertEqual(cell.role_entry(CC), "{executor: claude-code, model: claude-sonnet-5-5, effort: medium}")
        text = cell.project_yaml({}, {"build": CC, "review": "openai/gpt-6 high"})
        self.assertIn("  build: {executor: claude-code, model: claude-sonnet-5-5, effort: medium}\n", text)
        self.assertNotIn("provider: claude-code", text)

    def test_any_role_may_carry_it(self):
        for role in ("shape", "build", "review"):
            self.assertIn(f"  {role}: {{executor: claude-code,", cell.project_yaml({}, {role: CC}))

    def test_other_provider_strings_are_unchanged(self):
        self.assertEqual(cell.role_entry("openai/gpt-6-luna high"), "{model: gpt-6-luna, effort: high}")
        self.assertEqual(cell.role_entry("chatgpt/gpt-6 low"), "{model: gpt-6, effort: low}")
        self.assertEqual(cell.role_entry("opencode-go/kimi-k3 high"), "{model: kimi-k3, effort: high, provider: opencode-go}")

    def test_a_claude_code_role_string_is_a_valid_experiment_role(self):
        exp = common.read_json(test_providers.GOOD)
        exp["lanes"][0]["settings"] = {"models": {"build": CC}}
        experiment.validate(exp)
        self.assertEqual(experiment.lane_provider(exp["lanes"][0]), "claude-code")


class Preflight(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.config = os.path.join(self.tmp, "claude-bench")
        os.makedirs(self.config)
        self.log = os.path.join(self.tmp, "claude.log")
        self.exp = {"lanes": [{"name": "a", "settings": {"models": {"build": CC}}}]}
        self.lines = []
        env = {"CLAUDE_BIN": FAKE_CLAUDE, "FAKE_CLAUDE_LOG": self.log, "CLAUDE_CODE_OAUTH_TOKEN": "tok-secret",
               "KOGEN_LANES_HOME": "/nowhere"}
        patch = unittest.mock.patch.dict(os.environ, env)
        patch.start()
        self.addCleanup(patch.stop)
        os.environ.pop("FAKE_CLAUDE_STATE", None)

    def check(self, **cfg):
        host = {"target": "local", "slots": 1, **cfg}
        return ccroute.preflight(self.exp, {"h": host}, out=self.lines.append, ssh=SSH), "\n".join(self.lines)

    def test_logged_in_passes_under_the_cell_environment(self):
        bad, out = self.check(claude_config_dir=self.config)
        self.assertEqual((bad, "REFUSED" in out), (0, False), out)
        run = slurp(self.log)
        self.assertIn(f"config={self.config}", run)
        self.assertIn(f"home={os.environ['HOME']}", run)
        self.assertNotIn("token=set", run)  # Kogen strips it from the child; so does the check
        self.assertNotIn("secret", out)  # nothing the command printed is shown

    def test_missing_config_dir_setting_is_refused(self):
        bad, out = self.check()
        self.assertEqual(bad, 1)
        self.assertIn("CLAUDE_CONFIG_DIR is not set", out)
        self.assertFalse(os.path.exists(self.log))  # no login check without a folder

    def test_a_config_dir_that_does_not_exist_is_refused(self):
        bad, out = self.check(claude_config_dir=os.path.join(self.tmp, "nope"))
        self.assertEqual(bad, 1)
        self.assertIn("is not an existing directory", out)
        self.assertFalse(os.path.exists(self.log))

    def test_logged_in_false_is_refused(self):
        os.environ["FAKE_CLAUDE_STATE"] = "false"
        bad, out = self.check(claude_config_dir=self.config)
        self.assertEqual(bad, 1)
        self.assertIn("not logged in (loggedIn false)", out)
        self.assertNotIn("secret", out)

    def test_unreadable_status_is_refused(self):
        os.environ["FAKE_CLAUDE_STATE"] = "garbage"
        self.assertEqual(self.check(claude_config_dir=self.config)[0], 1)

    def test_a_missing_claude_binary_is_refused(self):
        bad, out = self.check(claude_config_dir=self.config, claude_bin=os.path.join(self.tmp, "no-claude"))
        self.assertEqual(bad, 1)
        self.assertIn("claude not found", out)

    def test_a_remote_host_is_checked_the_same_way(self):
        host = {"claude_config_dir": self.config, "claude_bin": FAKE_CLAUDE, "target": "far.invalid"}
        self.assertEqual(ccroute.preflight(self.exp, {"far": host}, out=self.lines.append, ssh=SSH), 0)
        self.assertNotIn("token=set", slurp(self.log))
        os.environ["FAKE_CLAUDE_STATE"] = "false"
        self.assertEqual(ccroute.preflight(self.exp, {"far": host}, out=self.lines.append, ssh=SSH), 1)
        self.assertEqual(ccroute.preflight(self.exp, {"far": dict(host, claude_config_dir=self.tmp + "/nope")},
                                           out=self.lines.append, ssh=SSH), 1)
        self.assertIn("is not an existing directory", self.lines[-1])

    def test_a_kogen_home_with_a_stored_token_passes_without_a_config_dir(self):
        home = os.path.join(self.tmp, "kogen-home")
        os.makedirs(os.path.join(home, ".kogen", "credentials"))
        with open(os.path.join(home, ".kogen", "credentials", "claude-code.json"), "w") as f:
            f.write("{}")
        bad, out = self.check(kogen_token_home=home)
        self.assertEqual((bad, "REFUSED" in out), (0, False), out)
        self.assertIn("Kogen stored token", out)
        self.assertFalse(os.path.exists(self.log))  # no claude auth status: the token is Kogen's

    def test_a_kogen_home_without_the_token_is_refused(self):
        home = os.path.join(self.tmp, "empty-home")
        os.makedirs(home)
        bad, out = self.check(kogen_token_home=home, claude_config_dir=self.config)
        self.assertEqual(bad, 1)
        self.assertIn("no stored Claude Code token", out)

    def test_a_remote_kogen_home_is_checked_over_ssh(self):
        home = os.path.join(self.tmp, "remote-home")
        os.makedirs(os.path.join(home, ".kogen", "credentials"))
        host = {"target": "far.invalid", "kogen_token_home": home}
        self.assertEqual(ccroute.preflight(self.exp, {"far": host}, out=self.lines.append, ssh=SSH), 1)
        with open(os.path.join(home, ".kogen", "credentials", "claude-code.json"), "w") as f:
            f.write("{}")
        self.assertEqual(ccroute.preflight(self.exp, {"far": host}, out=self.lines.append, ssh=SSH), 0)

    def test_no_claude_code_lane_means_no_check(self):
        self.assertEqual(ccroute.preflight({"lanes": [{"name": "a", "settings": {}}]}, {}, out=self.lines.append), 0)

    def test_a_claude_code_run_without_a_hosts_file_is_refused(self):
        self.assertEqual(ccroute.preflight(self.exp, None, out=self.lines.append), 1)
        self.assertIn("--hosts", self.lines[0])


class PreflightCommand(unittest.TestCase):
    """`lanes-preflight` and `lanes-run` refuse before any cell, with the real entry points."""
    make_run = test_preflight.PreflightTest.make_run

    def setUp(self):
        test_preflight.PreflightTest.setUp(self)
        exp = common.read_json(os.path.join(self.run_dir, "experiment.json"))
        exp["lanes"][0]["settings"] = {"models": {"build": CC}}
        exp["provider_caps"] = {"claude-code": {"cells": 4}}
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        self.config = os.path.join(self.tmp, "claude-bench")
        os.makedirs(self.config)
        self.hosts = os.path.join(self.tmp, "hosts.json")
        self.write_hosts(claude_config_dir=self.config, claude_bin=FAKE_CLAUDE)

    def write_hosts(self, **fields):
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 1, **fields}})

    def run_preflight(self, *extra, **env):
        e = {**os.environ, "KOGEN_LANES_HOME": self.home, "FAKE_KOGEN_TASK": test_preflight.TASK, **env}
        return subprocess.run([sys.executable, test_preflight.ENTRY, self.run_dir, "--tasks", self.tasks,
                               "--artifact", test_preflight.FAKE, *extra], env=e, capture_output=True, text=True, timeout=60)

    def test_logged_in_passes_and_the_intents_are_still_checked(self):
        p = self.run_preflight("--hosts", self.hosts)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("claude-code preflight: ok", p.stdout)
        self.assertIn("task-mini x base: ok", p.stdout)

    def test_logged_out_claude_refuses_the_run(self):
        p = self.run_preflight("--hosts", self.hosts, FAKE_CLAUDE_STATE="false")
        self.assertEqual(p.returncode, 1)
        self.assertIn("not logged in", p.stdout)
        self.assertNotIn("task-mini x base", p.stdout)  # refused before any Intent check

    def test_no_hosts_file_refuses(self):
        self.assertEqual(self.run_preflight().returncode, 1)

    def test_lanes_run_checks_the_intents_after_its_own_login_check(self):
        from lanes import preflight
        lines = []
        env = {"KOGEN_LANES_HOME": self.home, "FAKE_KOGEN_TASK": test_preflight.TASK}
        with unittest.mock.patch.dict(os.environ, env):
            bad = preflight.preflight(self.run_dir, self.tasks, test_preflight.FAKE, out=lines.append,
                                      claude_code_checked=True)
        self.assertEqual(bad, 0, lines)
        self.assertIn("task-mini x base: ok", "\n".join(lines))


class Dispatched(unittest.TestCase):
    """`lanes-run` and `lanes-ccdry` with the stand-in lanes-cell."""
    setUp = test_dispatch.Dispatch.setUp
    write_lock = test_dispatch.Dispatch.write_lock
    set_exp = test_dispatch.Dispatch.set_exp
    plan = test_dispatch.Dispatch.plan
    run_cmd = test_dispatch.Dispatch.run_cmd
    results = test_dispatch.Dispatch.results
    read = test_dispatch.Dispatch.read

    def start(self, reps=4, caps=None, slots=1, **host):
        exp = common.read_json(test_providers.GOOD)
        exp.update(reps=reps, cost_cap_usd=1.0, provider_caps=caps or {"claude-code": {"cells": 2}})
        exp["lanes"][0]["settings"] = {"models": {"build": CC}}  # base is the claude-code lane
        common.write_json(self.exp_path, exp)
        self.config = os.path.join(self.tmp, "claude-bench")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": slots,
                                                 "claude_config_dir": self.config, **host}})
        self.assertEqual(self.plan().returncode, 0)
        self.env.pop("CLAUDE_CONFIG_DIR", None)

    def done(self, lane):
        return sorted(c for c in self.results() if c.endswith("/" + lane))

    # ---- the cell cap

    def test_the_cell_cap_counts_claude_code_cells_and_stops_after_n(self):
        self.start()
        p = self.run_cmd()
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual((len(self.done("base")), len(self.done("patched"))), (2, 4))  # only the cc lane is capped
        self.assertIn("claude-code cell cap reached: 2 cell(s) started; no new claude-code cell starts", p.stderr)

    def test_a_claude_code_lane_without_its_cell_cap_cannot_start(self):
        self.start(caps={"opencode-go": {"cells": 9}})
        p = self.run_cmd()
        self.assertEqual(p.returncode, 2)
        self.assertIn('uses provider claude-code: add "provider_caps"', p.stderr)
        self.assertEqual(self.results(), {})

    def test_a_cap_applies_when_only_review_uses_the_executor(self):
        exp = common.read_json(self.exp_path)
        exp["lanes"][0]["settings"] = {"models": {"build": "openai/gpt-6 high", "review": CC}}
        self.assertEqual(costguard.lane_providers(exp)["base"], "claude-code")

    def test_a_cc_build_with_a_priced_review_counts_cells_and_dollars_separately(self):
        api = "anthropic/claude-opus-5-5 medium"
        self.start(caps={"claude-code": {"cells": 2}, "anthropic": {"usd": 5}})
        exp = common.read_json(self.exp_path)
        exp["lanes"][0]["settings"] = {"models": {"build": CC, "review": api}}
        self.assertEqual(costguard.lane_providers(exp)["base"], "anthropic")
        self.assertEqual(costguard.lane_cap_providers(exp)["base"], {"claude-code", "anthropic"})
        costguard.require_provider_caps(exp)
        started = {"claude-code": {"t/r1/base", "t/r2/base"}, "anthropic": {"t/r1/base", "t/r2/base"}}
        self.assertIn("claude-code cell cap reached", costguard.blocked(exp, "base", {}, started))
        self.assertIn("anthropic spend", costguard.blocked(exp, "base", {"anthropic": 5.0}, {}))
        self.assertIsNone(costguard.blocked(exp, "base", {"anthropic": 1.0}, {"claude-code": {"t/r1/base"}}))
        exp["provider_caps"] = {"claude-code": {"cells": 2}}
        with self.assertRaisesRegex(costguard.CostCapError, "uses provider anthropic"):
            costguard.require_provider_caps(exp)
        exp["lanes"][0]["settings"]["models"]["review"] = "opencode-go/kimi-k3 high"
        exp["lanes"][0]["settings"]["models"]["shape"] = api
        with self.assertRaisesRegex(costguard.CostCapError, "more than one non-ChatGPT provider"):
            costguard.require_provider_caps(exp)

    # ---- the run-start preflight

    def test_lanes_run_refuses_at_start_and_starts_no_cell(self):
        for fault in ("logged out", "no such dir", "unset"):
            self.start(caps={"claude-code": {"cells": 9}}, claude_bin=FAKE_CLAUDE)
            hosts = common.read_json(self.hosts)
            env = dict(self.env)
            if fault == "logged out":
                os.makedirs(self.config)
                env["FAKE_CLAUDE_STATE"] = "false"
            elif fault == "unset":
                del hosts["local"]["claude_config_dir"]
                common.write_json(self.hosts, hosts)
            p = subprocess.run([sys.executable, test_dispatch.entry("lanes-run"), self.run_dir, "--tasks", self.tasks,
                                "--hosts", self.hosts, "--lanes-dir", test_dispatch.FAKE_LANES], env=env,
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(p.returncode, 2, (fault, p.stderr))
            self.assertIn("claude-code pre-flight refused a host; no cell started", p.stderr)
            self.assertEqual(self.results(), {}, fault)
            shutil.rmtree(self.run_dir)
            shutil.rmtree(self.config, ignore_errors=True)

    # ---- CLAUDE_CONFIG_DIR reaches the cell

    def test_local_cells_of_a_claude_code_lane_get_the_hosts_config_dir(self):
        self.start(caps={"claude-code": {"cells": 9}}, reps=1)
        log = os.path.join(self.tmp, "env.txt")
        self.assertEqual(self.run_cmd(env=dict(self.env, FAKE_ENV_LOG=log)).returncode, 0)
        seen = dict(l.split() for l in self.read(log).splitlines())
        self.assertEqual(seen, {"task-mini/r1/base": self.config, "task-mini/r1/patched": "-"})

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_cells_get_it_too(self):
        self.start(caps={"claude-code": {"cells": 9}}, reps=1, target="far.invalid", root=os.path.join(self.tmp, "root"))
        log = os.path.join(self.tmp, "env.txt")
        env = dict(self.env, FAKE_ENV_LOG=log, LANES_SSH=FAKE_SSH)
        self.assertEqual(self.run_cmd(env=env).returncode, 0)
        seen = dict(l.split() for l in self.read(log).splitlines())
        self.assertEqual(seen, {"task-mini/r1/base": self.config, "task-mini/r1/patched": "-"})

    def test_claude_bins_folder_leads_the_path_of_claude_code_cells_only(self):
        for host in ({}, {"target": "far.invalid", "root": os.path.join(self.tmp, "root")}):
            if host and not shutil.which("rsync"):
                continue
            self.start(caps={"claude-code": {"cells": 9}}, reps=1, claude_bin="/opt/cc/bin/claude", **host)
            log = os.path.join(self.tmp, "path.txt")
            self.assertEqual(self.run_cmd(env=dict(self.env, FAKE_PATH_LOG=log, LANES_SSH=FAKE_SSH)).returncode, 0)
            seen = dict(l.split() for l in self.read(log).splitlines())
            self.assertEqual(seen["task-mini/r1/base"], "/opt/cc/bin", host)
            self.assertNotEqual(seen["task-mini/r1/patched"], "/opt/cc/bin", host)
            os.remove(log)
            shutil.rmtree(self.run_dir)

    # ---- the dry cell

    def dry(self, runlog, *extra):
        self.start(caps={"claude-code": {"cells": 9}}, reps=2)
        env = dict(self.env, FAKE_RUNLOG=runlog)
        return subprocess.run([sys.executable, DRY, self.run_dir, "--tasks", self.tasks, "--hosts", self.hosts,
                               "--host", "local", "--lanes-dir", test_dispatch.FAKE_LANES, "--skip-preflight", *extra],
                              env=env, capture_output=True, text=True, timeout=60)

    def test_the_dry_cell_runs_one_cell_of_a_claude_code_lane_and_passes_with_executor_events(self):
        p = self.dry("executor")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("ccdry: ok: task-mini/r1/base on local", p.stdout)
        self.assertEqual(list(self.results()), ["task-mini/r1/base"])  # exactly one cell, and not the other lane's

    def test_the_dry_cell_fails_when_the_run_log_has_no_executor_events(self):
        for runlog, why in (("empty", "never started"), ("native", "fell back to a native provider")):
            p = self.dry(runlog)
            self.assertEqual(p.returncode, 1, runlog)
            self.assertIn("ccdry: FAILED", p.stdout)
            self.assertIn(why, p.stdout)
            shutil.rmtree(self.run_dir)

    def test_the_dry_cell_refuses_an_experiment_without_the_executor(self):
        self.start(reps=1)
        exp = common.read_json(os.path.join(self.run_dir, "experiment.json"))
        exp["lanes"][0]["settings"] = {}
        exp["provider_caps"] = {}
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        p = subprocess.run([sys.executable, DRY, self.run_dir, "--tasks", self.tasks, "--hosts", self.hosts,
                            "--host", "local", "--skip-preflight"], env=self.env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)


class RunLogCheck(unittest.TestCase):
    """`check_run_log` on the run log of a real `lanes-cell` with the fake Kogen (which logs executor events when told)."""
    setUp = test_cell.CellTest.setUp
    wrapper = test_cell.CellTest.wrapper
    cell = test_cell.CellTest.cell
    done = test_cell.CellTest.done

    def run_cell(self, **env):
        run = self.make_run("build", models={"build": CC, "review": CC})
        exp = common.read_json(os.path.join(run, "experiment.json"))
        exp["provider_caps"] = {"claude-code": {"cells": 5}}
        common.write_json(os.path.join(run, "experiment.json"), exp)
        p = self.cell(run, **env)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return self.done(run)[0]

    make_run = test_cell.CellTest.make_run

    def test_the_executor_ran(self):
        path = self.run_cell()
        self.assertIn("executor_started", slurp(os.path.join(path, "run-log", "log.jsonl")))
        ok, message = ccroute.check_run_log(path)
        self.assertTrue(ok, message)

    def test_a_kogen_that_fell_back_to_the_native_provider_fails(self):
        ok, message = ccroute.check_run_log(self.run_cell(FAKE_KOGEN_EXECUTOR="fallback"))
        self.assertFalse(ok)
        self.assertIn("fell back to a native provider", message)

    def test_no_run_log_fails(self):
        path = self.run_cell()
        shutil.rmtree(os.path.join(path, "run-log"))
        self.assertFalse(ccroute.check_run_log(path)[0])


if __name__ == "__main__":
    unittest.main()
