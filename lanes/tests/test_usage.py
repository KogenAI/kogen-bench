import glob
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import usage

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.path.join(HERE, "fake-kogen")
TASK = os.path.join(HERE, "fixtures", "task-mini")
TABLE = {"models": {"fake-model": {"input": 1.0, "cached_input": 0.1, "output": 2.0},
                    "other-model": {"input": 3.0, "cached_input": 0.3, "output": 4.0}}}
COMMANDS = [{"stage": "approve", "started": "t0", "ended": "t1", "wall_s": 0.5, "exit_code": 0},
            {"stage": "build", "started": "t1", "ended": "t2", "wall_s": 2.0, "exit_code": 0}]


def fake(root, env, *args, check=True):
    return subprocess.run([sys.executable, FAKE, *args], cwd=root, env={**os.environ, **env},
                          check=check, capture_output=True, text=True)


def fresh_repo(root, env, models):
    shutil.copytree(os.path.join(TASK, "start"), root, dirs_exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    fake(root, env, "init")
    if models:
        with open(os.path.join(root, ".kogen", "project.yaml"), "w") as f:
            f.write("version: 1\nmodels:\n" + "".join(
                f"  {r}: {{model: {m}, effort: high}}\n" for r, m in models.items()))


def run_fake_build(env=None, models=None):
    """Build the task-mini Intent with the fake Kogen; return the run log events."""
    env = env or {}
    with tempfile.TemporaryDirectory() as root:
        fresh_repo(root, env, models)
        shutil.copytree(os.path.join(TASK, "supplied", "gherkin"),
                        os.path.join(root, ".kogen", "intents", "add-numbers"))
        out = fake(root, env, "intent", "approve", "add-numbers", check=False).stdout
        prefix = [l for l in out.splitlines() if l.startswith("SHA-256: ")][0].split()[1][:12]
        fake(root, env, "intent", "approve", "add-numbers", prefix)
        fake(root, env, "intent", "build", "add-numbers")
        log = glob.glob(os.path.join(root, ".kogen", "local", "runs", "*", "log.jsonl"))[0]
        return usage.read_log(log)


def run_fake_shape(env=None, models=None):
    """Shape the task-mini brief with the fake Kogen; return the shaping events."""
    env = env or {}
    with tempfile.TemporaryDirectory() as root:
        fresh_repo(root, env, models)
        fake(root, env, "intent", "shape", "add-numbers", os.path.join(TASK, "request.md"))
        return usage.read_log(os.path.join(root, ".kogen", "local", "shaping", "add-numbers", "events.ndjson"))


class Usage(unittest.TestCase):
    def test_all_fields_on_a_fake_log(self):
        r = usage.parse_run_log(run_fake_build(), COMMANDS, TABLE)
        approve, build, review = r["stages"]
        self.assertEqual([s["stage"] for s in r["stages"]], ["approve", "build", "review"])
        self.assertEqual((approve["requests"], approve["cost_usd"], approve["missing"]), (0, 0.0, []))
        self.assertEqual(approve["outcome"], "ok")
        self.assertEqual(build["outcome"], "landed")
        self.assertEqual((build["started"], build["wall_s"], build["exit_code"]), ("t1", 2.0, 0))
        self.assertEqual((build["input_tokens"], build["cached_input_tokens"], build["output_tokens"],
                          build["reasoning_tokens"]), (1200, 800, 300, 120))
        self.assertEqual(build["models"], ["fake-model"])
        self.assertEqual(build["cost_usd"], 0.00108)
        self.assertEqual(build["missing"], [])
        self.assertEqual((review["input_tokens"], review["cost_usd"], review["wall_s"]), (900, 0.00066, 0.1))
        self.assertEqual(r["totals"]["cost_usd"], 0.00174)
        self.assertEqual(r["totals"]["input_tokens"], 2100)
        self.assertEqual(r["totals"]["wall_s"], 2.5)  # command-level only
        self.assertEqual(r["totals"]["requests"], 2)

    def test_unknown_usage_null_is_future_behaviour(self):
        """Null counters (shape events now, build logs in a future Kogen) stay null and listed."""
        r = usage.parse_run_log(run_fake_build({"FAKE_KOGEN_USAGE": "unknown"}), COMMANDS, TABLE)
        build = r["stages"][1]
        self.assertIsNone(build["input_tokens"])
        self.assertIsNone(build["cost_usd"])
        self.assertEqual(build["cost_reason"], "usage missing")
        self.assertEqual(build["missing"], sorted(usage.TOKENS))
        t = r["totals"]  # approve is priced at 0.0, build is not: the total is the priced sum plus a list, never a silent zero
        self.assertEqual((t["priced_usd"], t["cost_usd"], t["cost_complete"]), (0.0, 0.0, False))
        self.assertEqual([u["stage"] for u in t["unpriced_stages"]], ["build", "review"])
        self.assertEqual(t["missing"], sorted(usage.TOKENS))

    def test_zero_usage_in_a_build_log_is_flagged_not_priced(self):
        """b45ba32b logs missing build usage as 0: not a real $0."""
        r = usage.parse_run_log(run_fake_build({"FAKE_KOGEN_USAGE": "zero"}), COMMANDS, TABLE)
        build = r["stages"][1]
        self.assertEqual(build["input_tokens"], 0)
        self.assertIsNone(build["cost_usd"])
        self.assertIn("all zero", build["cost_reason"])
        self.assertIn("usage_zero_is_unknown", build["missing"])
        self.assertFalse(r["totals"]["cost_complete"])
        self.assertEqual(r["totals"]["unpriced_stages"][0]["stage"], "build")
        self.assertIn("usage_zero_is_unknown", r["totals"]["missing"])

    def test_shape_stage_from_shaping_events(self):
        cmds = [{"stage": "shape", "started": "a", "ended": "b", "wall_s": 0.5, "exit_code": 0}]
        r = usage.parse_run_log(None, cmds, TABLE, shape_events=run_fake_shape())
        shape = r["stages"][0]
        self.assertEqual((shape["requests"], shape["models"], shape["outcome"]), (1, ["fake-model"], "ok"))
        self.assertEqual((shape["input_tokens"], shape["cached_input_tokens"], shape["output_tokens"],
                          shape["reasoning_tokens"]), (2000, 1500, 400, 200))
        self.assertEqual(shape["cost_usd"], 0.00145)  # (500*1 + 1500*0.1 + 400*2) per million
        self.assertEqual(shape["missing"], [])
        self.assertEqual(r["totals"]["cost_usd"], 0.00145)

    def test_shape_events_with_null_usage_keep_nulls(self):
        cmds = [{"stage": "shape", "wall_s": 0.5, "exit_code": 0}]
        r = usage.parse_run_log(None, cmds, TABLE, shape_events=run_fake_shape({"FAKE_KOGEN_USAGE": "zero"}))
        shape = r["stages"][0]
        self.assertIsNone(shape["input_tokens"])
        self.assertIsNone(shape["cost_usd"])
        self.assertEqual(shape["cost_reason"], "usage missing")

    def test_estimate_price_keeps_usd_and_names_the_status(self):
        table = {"models": {"fake-model": {"input": 1.0, "cached_input": 0.1, "output": 2.0,
                                           "source": "unlisted; third-party"}}}
        r = usage.parse_run_log(run_fake_build(), COMMANDS, table)
        build = r["stages"][1]
        self.assertEqual((build["cost_usd"], build["cost_reason"]), (0.00108, "declared_estimate"))
        self.assertEqual(r["totals"]["cost_reason"], "declared_estimate")

    def test_two_models(self):
        events = run_fake_build(models={"shape": "fake-model", "build": "fake-model", "review": "other-model"})
        r = usage.parse_run_log(events, COMMANDS, TABLE)
        self.assertEqual(r["stages"][1]["models"], ["fake-model"])
        self.assertEqual(r["stages"][2]["models"], ["other-model"])
        self.assertEqual(r["stages"][2]["cost_usd"], 0.00168)  # (300*3 + 600*0.3 + 150*4) per million
        self.assertEqual(r["totals"]["models"], ["fake-model", "other-model"])
        self.assertEqual(r["totals"]["cost_usd"], 0.00276)

    def test_unknown_price_gives_null_with_reason(self):
        events = run_fake_build(models={"shape": "m", "build": "mystery", "review": "fake-model"})
        r = usage.parse_run_log(events, COMMANDS, TABLE)
        build = r["stages"][1]
        self.assertIsNone(build["cost_usd"])
        self.assertIn("unlisted_model", build["cost_reason"])
        self.assertEqual(r["totals"]["priced_usd"], 0.00066)  # was None: the priced review stage is no longer hidden
        self.assertEqual([u["stage"] for u in r["totals"]["unpriced_stages"]], ["build"])
        self.assertEqual(build["input_tokens"], 1200)  # tokens are still reported
        self.assertEqual(r["stages"][2]["cost_usd"], 0.00066)
        self.assertFalse(r["totals"]["cost_complete"])

    def test_provider_prefix_is_stripped_for_price(self):
        usd, why = usage.request_cost("openai/fake-model", {"input_tokens": 1000, "cached_input_tokens": 0,
                                                              "output_tokens": 0}, TABLE)
        self.assertEqual((usd, why), (0.001, None))

    def test_no_log_keeps_command_wall_time(self):
        cmds = [{"stage": "shape", "started": "a", "ended": "b", "wall_s": 1.5, "exit_code": 1, "timed_out": True}]
        r = usage.parse_run_log(None, cmds, TABLE)
        shape = r["stages"][0]
        self.assertEqual((shape["wall_s"], shape["outcome"], shape["requests"]), (1.5, "timeout", 0))
        self.assertIsNone(shape["input_tokens"])
        self.assertIn("input_tokens", shape["missing"])
        self.assertEqual(shape["models"], [])
        self.assertNotIn("models", shape["missing"])
        self.assertEqual(r["totals"]["wall_s"], 1.5)

    def test_failed_build_outcome_from_log(self):
        r = usage.parse_run_log([{"event": "request", "role": "build", "model": "fake-model", "wall_ms": 5,
                                  "usage": {"input": 10, "cached": 0, "output": 5, "reasoning": 0}},
                                 {"event": "outcome", "outcome": "build_blocked"}],
                                [{"stage": "build", "wall_s": 1, "exit_code": 1}], TABLE)
        self.assertEqual(r["stages"][0]["outcome"], "build_blocked")
        self.assertEqual(r["stages"][0]["reasoning_tokens"], 0)

    SEED_LOG = [{"event": "seeded"},
                {"event": "request", "role": "review", "model": "fake-model", "wall_ms": 100,
                 "usage": {"input": 900, "cached": 0, "output": 100, "reasoning": 0}},
                {"event": "outcome", "outcome": "landed"}]

    def test_a_seeded_build_without_requests_counts_as_zero(self):
        """A declared seed replaces the builder: zero builder requests by design, not missing usage."""
        r = usage.parse_run_log(self.SEED_LOG, COMMANDS, TABLE)
        build = [s for s in r["stages"] if s["stage"] == "build"][0]
        self.assertEqual((build["requests"], build["input_tokens"], build["output_tokens"]), (0, 0, 0))
        self.assertEqual((build["cost_usd"], build["cost_reason"]), (0.0, "seeded: no builder request by design"))
        self.assertEqual(build["missing"], [])
        self.assertEqual(r["totals"]["cost_usd"], 0.00110)
        self.assertEqual(r["totals"]["missing"], [])

    def test_without_a_seed_a_build_without_requests_stays_missing(self):
        r = usage.parse_run_log(self.SEED_LOG[1:], COMMANDS, TABLE)
        build = [s for s in r["stages"] if s["stage"] == "build"][0]
        self.assertIsNone(build["cost_usd"])
        self.assertEqual(build["cost_reason"], "no request in the log")
        self.assertEqual(build["missing"], sorted(usage.TOKENS))
        self.assertFalse(r["totals"]["cost_complete"])  # priced sum kept, the unpriced build is listed (cap7)
        self.assertEqual([u["stage"] for u in r["totals"]["unpriced_stages"]], ["build"])

    def test_a_seeded_build_with_requests_is_priced_from_them(self):
        log = self.SEED_LOG[:1] + [{"event": "request", "role": "build", "model": "fake-model", "wall_ms": 5,
                                    "usage": {"input": 10, "cached": 0, "output": 5, "reasoning": 0}}] + self.SEED_LOG[1:]
        build = usage.parse_run_log(log, COMMANDS, TABLE)["stages"][1]
        self.assertEqual((build["requests"], build["input_tokens"], build["cost_reason"]), (1, 10, None))

    def test_the_seed_rule_does_not_reach_shape_or_approve(self):
        cmds = [{"stage": "shape", "wall_s": 1, "exit_code": 0}]
        shape = usage.parse_run_log(self.SEED_LOG, cmds, TABLE)["stages"][0]
        self.assertIsNone(shape["cost_usd"])
        self.assertEqual(shape["cost_reason"], "no request in the log")


if __name__ == "__main__":
    unittest.main()
