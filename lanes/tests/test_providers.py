import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

from lanes import common, costcmd, costguard, dispatch, experiment, report, usage
from tests import test_dispatch
from tests.test_dispatch import BIN

GOOD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "experiment-good.json")
GO = "opencode-go/kimi-k3 high"


def shaping(model, configured, inp=100000, cached=20000, out=10000):
    return {"event": "provider_call", "effective_model": model, "configured_model": configured,
            "usage": {"input": inp, "cached": cached, "output": out, "reasoning": 0}}


def exp_with(**fields):
    exp = common.read_json(GOOD)
    exp["lanes"][0]["settings"] = {"models": {"build": GO}}
    exp["provider_caps"] = {"opencode-go": {"cells": 99}}
    exp.update(fields)
    return exp


class ModelNames(unittest.TestCase):
    def parse(self, shape=None, events=None):
        stage = [{"stage": "shape", "exit_code": 0}] if shape else [{"stage": "build", "exit_code": 0}]
        return usage.parse_run_log(events, stage, shape_events=shape)

    def test_shaping_falls_back_to_the_configured_model_and_says_so(self):
        r = self.parse(shape=[shaping(None, "kimi-k3")])
        self.assertEqual((r["totals"]["models"], r["totals"]["model_sources"]), (["kimi-k3"], ["configured"]))
        self.assertIsNone(r["totals"]["cost_reason"])
        self.assertAlmostEqual(r["totals"]["cost_usd"], 80000 * 3 / 1e6 + 20000 * 0.3 / 1e6 + 10000 * 15 / 1e6)

    def test_build_events_too_and_the_effective_model_wins(self):
        build = {"event": "request", "role": "build", "configured_model": "kimi-k3", "effective_model": None,
                 "usage": {"input": 1000000, "cached": 0, "output": 1000000, "reasoning": 0}}
        r = self.parse(events=[build])
        self.assertEqual((r["totals"]["models"], r["stages"][0]["model_sources"]), (["kimi-k3"], ["configured"]))
        self.assertAlmostEqual(r["totals"]["cost_usd"], 18.0)
        both = dict(build, effective_model="grok-4.7")
        r = self.parse(events=[both])
        self.assertEqual((r["totals"]["models"], r["totals"]["model_sources"]), (["grok-4.7"], ["effective"]))
        self.assertAlmostEqual(r["totals"]["cost_usd"], 8.0)

    def test_no_name_at_all_is_never_invented(self):
        r = self.parse(shape=[shaping(None, None)])
        self.assertEqual((r["totals"]["models"], r["totals"]["cost_usd"]), ([], None))
        self.assertEqual(r["totals"]["cost_reason"], "model missing")

    def test_price_rows_for_the_two_new_models_carry_their_source(self):
        rows = common.read_json(os.path.join(os.path.dirname(usage.COST_CALC), "price-table-v1.json"))["models"]
        for name in ("kimi-k3", "grok-4.7"):
            self.assertTrue(rows[name]["source_url"].startswith("https://"))
            self.assertRegex(rows[name]["fetched_utc"], r"^2026-\d\d-\d\dT")
        self.assertEqual([rows["kimi-k3"][k] for k in ("input", "cached_input", "output")], [3.0, 0.3, 15.0])
        self.assertEqual([rows["grok-4.7"][k] for k in ("input", "cached_input", "output")], [2.0, 0.5, 6.0])

    def test_an_unknown_output_price_uses_the_fallback_for_that_part_only(self):
        table = {"models": {"top": {"input": 10.0, "cached_input": 1.0, "output": 50.0},
                            "half": {"input": 2.0, "cached_input": 0.2, "output": None}}}
        usd, reason = usage.request_cost("half", {"input_tokens": 1000000, "cached_input_tokens": 0,
                                                  "output_tokens": 1000000}, table)
        self.assertEqual((usd, reason), (52.0, "fallback_rate: output"))  # input at its own 2.0, output at 50.0
        with mock.patch.object(costguard, "_pricing", (usage._cost_calc(), table, usage.top_rates(table))):
            self.assertAlmostEqual(costguard.log_spend(
                [{"event": "request", "model": "half", "usage": {"input": 1000000, "cached": 0, "output": 1000000}}], None), 52.0)


class Validation(unittest.TestCase):
    def test_a_run_without_provider_caps_loads_but_cannot_start_cells(self):  # B1
        exp = exp_with()
        del exp["provider_caps"]
        experiment.validate(exp)  # read-only commands accept a pre-provider_caps run dir
        with self.assertRaisesRegex(costguard.CostCapError, "lane base uses provider opencode-go: add") as e:
            costguard.require_provider_caps(exp)
        self.assertIn("lanes-plan again", str(e.exception))
        exp["provider_caps"] = {"supergrok": {"cells": 3}}
        with self.assertRaises(costguard.CostCapError):
            costguard.require_provider_caps(exp)
        exp["provider_caps"] = {"opencode-go": {"cells": 3}}
        costguard.require_provider_caps(exp)
        exp["lanes"][1]["settings"] = {"models": {"build": "supergrok/grok-4.7 high"}}
        with self.assertRaises(costguard.CostCapError):
            costguard.require_provider_caps(dict(exp, lanes=[dict(exp["lanes"][0], settings={"models": {
                "build": GO, "review": "supergrok/grok-4.7 high"}})]))

    def test_lanes_cell_check_refuses_without_the_cap(self):
        exp = exp_with(cost_cap_usd=1.0)
        del exp["provider_caps"]
        with tempfile.TemporaryDirectory() as run:
            with self.assertRaisesRegex(costguard.CostCapError, "provider_caps"):
                costguard.check_start(run, exp, "t/r1/base")

    def test_chatgpt_lanes_need_no_provider_cap(self):
        experiment.validate(common.read_json(GOOD))  # `openai/` and no models: ChatGPT

    def test_cap_values_are_checked(self):
        for bad in ({"opencode-go": {}}, {"opencode-go": {"cells": 0}}, {"opencode-go": {"cells": 1.5}},
                    {"opencode-go": {"usd": -1}}, {"opencode-go": {"cells": 1, "x": 1}}, {"chatgpt": {"cells": 1}}):
            with self.assertRaises(experiment.ExperimentError, msg=bad):
                experiment.validate(exp_with(provider_caps=bad))
        experiment.validate(exp_with(provider_caps={"opencode-go": {"cells": 2, "usd": 5}}))


class Guard(unittest.TestCase):
    def setUp(self):
        self.run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.run)

    def spent(self, cell, usd):
        common.write_json(os.path.join(common.cell_dir(self.run, cell), "result.json"), {"totals": {"cost_usd": usd}})

    def test_chatgpt_cap_ignores_opencode_spend_and_the_reverse(self):
        exp = exp_with(cost_cap_usd=1.0, provider_caps={"opencode-go": {"usd": 2.0}})
        self.spent("t/r1/base", 40.0)  # opencode-go lane
        spends = costguard.provider_spend(self.run, exp)
        self.assertEqual(spends, {"opencode-go": 40.0})
        self.assertIsNone(costguard.blocked(exp, "patched", spends, {}, {}))  # the ChatGPT lane is fine
        self.assertIn("opencode-go spend $40.0000 of the $2 cap", costguard.blocked(exp, "base", spends, {}, {}))
        self.assertEqual(costguard.over_hard(exp, spends)[0][0], "opencode-go")
        self.spent("t/r1/patched", 1.5)
        spends = costguard.provider_spend(self.run, exp)
        self.assertIn("cost cap reached: spend $1.5000 of the $1 cap", costguard.blocked(exp, "patched", spends, {}, {}))
        self.assertEqual(costguard.over_hard(exp, {"chatgpt": 1.2, "opencode-go": 0.0}), [])

    def test_estimated_dollars_of_a_provider_without_a_usd_cap_never_block(self):
        exp = exp_with(cost_cap_usd=1.0)
        self.spent("t/r1/base", 500.0)
        spends = costguard.provider_spend(self.run, exp)
        self.assertIsNone(costguard.blocked(exp, "base", spends, {}, {}))
        self.assertEqual(costguard.over_hard(exp, spends), [])
        costguard.check_start(self.run, exp, "t/r2/base")  # does not raise

    def test_cell_cap_counts_started_cells_including_retired_attempts(self):
        exp = exp_with(cost_cap_usd=1.0, provider_caps={"opencode-go": {"cells": 2}})
        self.spent("t/r1/base", 0.0)
        common.write_json(os.path.join(common.cell_dir(self.run, "t/r2/base"), "result.json"), {"totals": {}})
        started = costguard.started_cells(self.run, exp)
        self.assertEqual(len(started["opencode-go"]), 2)
        self.assertIn("2 cell(s) started", costguard.blocked(exp, "base", {}, started, {}))
        self.assertIsNone(costguard.blocked(exp, "patched", {}, started, {}))
        with self.assertRaisesRegex(costguard.CostCapError, "cell cap reached"):
            costguard.check_start(self.run, exp, "t/r3/base")
        costguard.check_start(self.run, exp, "t/r2/base")  # a cell already counted may be (re)started
        shutil.rmtree(common.cell_dir(self.run, "t/r2/base"))
        costguard.ledger_add(self.run, "t/r2/base", 0.1)  # retired: still started
        self.assertEqual(len(costguard.started_cells(self.run, exp)["opencode-go"]), 2)

    def test_the_report_shows_each_cap_against_its_use(self):
        exp = exp_with(cost_cap_usd=10.0, provider_caps={"opencode-go": {"cells": 3, "usd": 2.0}})
        self.spent("t/r1/base", 1.0)
        self.spent("t/r1/patched", 5.0)
        text = "\n".join(report._render_cost(report.cost_section(self.run, exp, [])))
        self.assertIn("| base | opencode-go | 1.0000 | n/a | n/a |", text)
        self.assertIn("| patched | chatgpt | 5.0000 | 50% | 40% |", text)
        self.assertIn("| opencode-go | 1.0000 | 2 / 2.5 (50%) | 1 | 3 | no |", text)
        self.assertIn("| chatgpt | 5.0000 | 10 / 12.5 (50%) | 1 | none | no |", text)

    def cell_dir(self, **files):
        d = tempfile.mkdtemp(dir=self.run)
        for name, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(d, name.replace("__", "/"))), exist_ok=True)
            with open(os.path.join(d, name.replace("__", "/")), "w") as f:
                f.write(text)
        return d

    def test_rate_limits_are_found_in_kogens_provider_failure_records(self):  # B2
        ev = lambda **e: json.dumps(e) + "\n"
        find = costguard.find_rate_limit
        failure = {"http_status": 429, "code": "rate_limit", "type": "rate_limit_error"}
        # OpenCode Go build, after Kogen's retries: the outcome event carries provider_failure
        log = ev(event="provider_attempt", provider={"provider_failure": failure}) + \
            ev(event="outcome", outcome="provider_unavailable", provider_failure=failure)
        self.assertEqual(find(self.cell_dir(**{"run-log__log.jsonl": log})), "http_429")
        # a shaping provider_call that failed, the failure inside its `provider` object
        call = ev(event="provider_call", error="provider_failure", status="failed",
                  provider={"error": "provider_failure", "provider_failure": {"http_status": 429}})
        self.assertEqual(find(self.cell_dir(**{"shaping-events.ndjson": call})), "http_429")
        # ChatGPT's usage limit: code only, and Kogen's stdout record and class
        usage_limit = ev(event="outcome", outcome="blocked",
                         provider_failure={"code": "subscription_sharing_usage_limit_exceeded", "http_status": 429})
        self.assertEqual(find(self.cell_dir(**{"run-log__log.jsonl": usage_limit})), "http_429")
        coded = ev(event="outcome", provider_failure={"code": "subscription_sharing_usage_limit_exceeded"})
        self.assertEqual(find(self.cell_dir(**{"run-log__log.jsonl": coded})), "subscription_sharing_usage_limit_exceeded")
        out = 'provider failure: {"code": "rate_limit_exceeded", "event_kind": "response.failed"}\n'
        self.assertEqual(find(self.cell_dir(**{"stdout.txt": "  " + out})), "rate_limit_exceeded")
        self.assertEqual(find(self.cell_dir(**{"stdout.txt": "x\nprovider/usage_limit: ChatGPT usage limit\n"})),
                         "provider/usage_limit")
        self.assertEqual(find(self.cell_dir(**{"shaping-events.ndjson": ev(event="provider_call", error="usage_limit")})),
                         "usage_limit")

    def test_what_is_not_a_failure_on_a_limit_is_not_found(self):
        ev = lambda **e: json.dumps(e) + "\n"
        find = costguard.find_rate_limit
        recovered = ev(event="provider_attempt", provider={"provider_failure": {"http_status": 429}}) + \
            ev(event="outcome", outcome="landed")  # a retry recovered it
        self.assertIsNone(find(self.cell_dir(**{"run-log__log.jsonl": recovered})))
        ok_call = ev(event="provider_call", error=None, provider={"provider_failure": {"http_status": 429}})
        self.assertIsNone(find(self.cell_dir(**{"shaping-events.ndjson": ok_call})))
        cancelled = ev(event="provider_call", error="provider_failure", status="cancelled", provider={"outcome": "cancelled"})
        self.assertIsNone(find(self.cell_dir(**{"shaping-events.ndjson": cancelled})))
        self.assertIsNone(find(self.cell_dir(**{"run-log__log.jsonl": ev(event="outcome", provider_failure={"http_status": 500})})))
        self.assertIsNone(find(self.cell_dir(**{"shaping-events.ndjson": ev(event="provider_call", status=429, message="usage limit")})))
        self.assertIsNone(find(self.cell_dir(**{"stdout.txt": "environment/x: HTTP 429\nthe rate_limit in prose\n"})))

    def test_the_text_fallback_needs_a_provider_class_line(self):
        self.assertEqual(costguard.find_rate_limit(self.cell_dir(**{
            "stdout.txt": "provider/unavailable: OpenCode Go did not answer after 3 attempts: OpenCode Go temporary HTTP 429\n"})),
            "provider/unavailable")

    def test_a_hard_cap_names_its_own_provider(self):
        exp = exp_with(cost_cap_usd=1.0, provider_caps={"opencode-go": {"usd": 2.0}})
        spends = {"chatgpt": 0.5, "opencode-go": 3.0}
        self.assertEqual([h[0] for h in costguard.over_hard(exp, spends)], ["opencode-go"])
        self.assertEqual(costguard.over_hard(exp, spends, "chatgpt"), [])
        self.spent("t/r1/base", 3.0)
        with costguard.Watcher(self.run, exp, 0.05, provider="chatgpt") as w:
            self.assertFalse(w.tripped.wait(0.5))  # a ChatGPT cell is not stopped by OpenCode's cap
        with costguard.Watcher(self.run, exp, 0.05, provider="opencode-go") as w:
            self.assertTrue(w.tripped.wait(5))

    def test_the_first_rate_limit_is_recorded_per_provider_and_blocks_only_that_provider(self):
        exp = exp_with(cost_cap_usd=1.0)
        d = common.cell_dir(self.run, "t/r1/base")
        os.makedirs(d)
        with open(os.path.join(d, "stdout.txt"), "w") as f:
            f.write("provider/usage_limit: limit\n")
        self.assertEqual(costguard.note_rate_limit(self.run, exp, "t/r1/base"), "provider/usage_limit")
        os.makedirs(os.path.join(self.run, "cells", "t", "r2", "base"))
        with open(os.path.join(self.run, "cells", "t", "r2", "base", "stdout.txt"), "w") as f:
            f.write("provider/usage_limit: later\n")
        costguard.note_rate_limit(self.run, exp, "t/r2/base")
        mark = common.read_json(os.path.join(self.run, costguard.RATE))["opencode-go"]
        self.assertEqual((mark["cell"], mark["rate_limited"]), ("t/r1/base", True))  # the first one stays
        with self.assertRaisesRegex(costguard.CostCapError, "opencode-go is rate limited"):
            costguard.check_start(self.run, exp, "t/r3/base")
        costguard.check_start(self.run, exp, "t/r3/patched")


class LanesRun(unittest.TestCase):
    """`lanes-run` with the stand-in lanes-cell: per-provider caps and rate limits."""
    setUp = test_dispatch.Dispatch.setUp
    write_lock = test_dispatch.Dispatch.write_lock
    set_exp = test_dispatch.Dispatch.set_exp
    plan = test_dispatch.Dispatch.plan
    run_cmd = test_dispatch.Dispatch.run_cmd
    results = test_dispatch.Dispatch.results
    read = test_dispatch.Dispatch.read

    def start(self, **fields):
        exp = exp_with(cost_cap_usd=1.0, reps=fields.pop("reps", 2), **fields)
        common.write_json(self.exp_path, exp)
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 1}})
        self.assertEqual(self.plan().returncode, 0)

    def done(self, lane):
        return sorted(c for c in self.results() if c.endswith("/" + lane))

    def test_a_provider_cell_cap_stops_that_provider_only(self):
        self.start(provider_caps={"opencode-go": {"cells": 1}})
        p = self.run_cmd()
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual((len(self.done("base")), len(self.done("patched"))), (1, 2))
        self.assertIn("opencode-go cell cap reached: 1 cell(s) started", p.stderr)

    def test_opencode_dollars_do_not_stop_the_chatgpt_cap_and_chatgpt_dollars_stop_only_chatgpt(self):
        self.start(reps=4)
        p = self.run_cmd(env=dict(self.env, FAKE_COST_BASE="50", FAKE_COST_PATCHED="0.6"))
        self.assertEqual(len(self.done("base")), 4)  # 200 USD of opencode-go estimates: no stop
        self.assertEqual(len(self.done("patched")), 2)  # 0.6, 1.2 >= the 1.0 cap
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertIn("cost cap reached: spend $1.2000 of the $1 cap", p.stderr)
        p = self.run_cmd(env=dict(self.env, FAKE_COST_BASE="50"))  # nothing left but capped chatgpt cells
        self.assertEqual(p.returncode, 3)

    def test_a_usage_limit_stops_dispatch_to_that_provider_and_says_how_to_resume(self):
        self.start()
        env = dict(self.env, FAKE_RATE_LIMIT="task-mini/r1/base")
        p = self.run_cmd(env=env)
        self.assertEqual(p.returncode, 4, p.stderr)
        self.assertEqual((self.done("base"), len(self.done("patched"))), (["task-mini/r1/base"], 2))
        mark = common.read_json(os.path.join(self.run_dir, costguard.RATE))["opencode-go"]
        self.assertEqual((mark["reason"], mark["cell"], mark["rate_limited"]),
                         ("provider/usage_limit", "task-mini/r1/base", True))
        self.assertIn("delete rate-limit-stop.json", p.stderr)
        os.remove(os.path.join(self.run_dir, costguard.RATE))  # the limit reset: resume runs the rest
        self.assertEqual(self.run_cmd().returncode, 0)  # the rest of the provider's cells run
        self.assertEqual(len(self.done("base")), 2)

    def test_lanes_run_refuses_to_start_without_the_provider_cap(self):  # B1
        self.start()
        exp = common.read_json(self.exp_path)
        del exp["provider_caps"]
        common.write_json(self.exp_path, exp)
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        p = self.run_cmd()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn("provider_caps", p.stderr)
        self.assertEqual(self.results(), {})

    def test_the_rate_limit_is_recorded_before_a_sibling_slot_can_take_the_next_cell(self):  # m4
        self.start()
        seen = []
        real = costguard.note_rate_limit
        def spy(run_dir, exp, cell):
            seen.append(sorted(os.listdir(os.path.join(run_dir, "claims"))))
            return real(run_dir, exp, cell)
        with mock.patch.object(costguard, "note_rate_limit", spy), \
                mock.patch.dict(os.environ, {"KOGEN_LANES_HOME": self.home, "FAKE_EVENTS": self.events}):
            dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=test_dispatch.FAKE_LANES,
                             log=lambda m: None, skip_preflight=True)
        self.assertTrue(all(seen), seen)  # the finished cell's claim was still held

    def test_lanes_cell_refuses_a_rate_limited_provider(self):
        self.start()
        common.write_json(os.path.join(self.run_dir, costguard.RATE),
                          {"opencode-go": {"cell": "x/r1/base", "reason": "http_429", "rate_limited": True, "at": "t"}})
        with self.assertRaisesRegex(costguard.CostCapError, "rate limited"):
            costguard.check_start(self.run_dir, common.read_json(self.exp_path), "task-mini/r1/base")


class Recompute(unittest.TestCase):
    def setUp(self):
        self.run = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.run)
        common.write_json(os.path.join(self.run, "experiment.json"),
                          exp_with(cost_cap_usd=100, provider_caps={"opencode-go": {"usd": 6.0}}))
        self.cell = common.cell_dir(self.run, "task-mini/r1/base")
        os.makedirs(self.cell)
        with open(os.path.join(self.cell, "shaping-events.ndjson"), "w") as f:
            for _ in range(3):
                f.write(json.dumps(shaping(None, "kimi-k3")) + "\n")
        old = usage.parse_run_log(None, [{"stage": "shape", "started": "a", "ended": "b", "wall_s": 3.0, "exit_code": 0}],
                                  shape_events=[shaping(None, None)] * 3)
        old["totals"]["cost_usd"] = old["stages"][0]["cost_usd"] = 17.0  # what the fallback guard recorded
        old["totals"]["models"] = old["stages"][0]["models"] = []
        self.result = {"cell": "task-mini/r1/base", "lane": "base", "outcome": "ok", "final_tree": "abc", **old}
        common.write_json(os.path.join(self.cell, "result.json"), self.result)
        common.write_json(os.path.join(self.run, costguard.STOP), {"cap": "hard", "spent_usd": 17.0, "provider": "opencode-go"})
        costguard.ledger_add(self.run, "task-mini/r2/base", 4.0)  # a retired attempt with no stored logs
        self.exp = experiment.load(os.path.join(self.run, "experiment.json"))

    def run_cost(self, *args):
        return subprocess.run([sys.executable, os.path.join(BIN, "lanes-cost"), "recompute", self.run, *args],
                              capture_output=True, text=True)

    def test_recompute_reprices_clears_the_stop_and_touches_only_cost_fields(self):
        self.assertGreaterEqual(costguard.provider_spend(self.run, self.exp)["opencode-go"], 21.0)
        r = self.run_cost()
        self.assertEqual(r.returncode, 0, r.stderr)
        new = common.read_json(os.path.join(self.cell, "result.json"))
        want = 3 * (80000 * 3 / 1e6 + 20000 * 0.3 / 1e6 + 10000 * 15 / 1e6)
        self.assertAlmostEqual(new["totals"]["cost_usd"], want)
        self.assertEqual((new["totals"]["models"], new["totals"]["model_sources"], new["totals"]["cost_reason"]),
                         (["kimi-k3"], ["configured"], None))
        for key in ("cell", "lane", "outcome", "final_tree"):
            self.assertEqual(new[key], self.result[key])
        for a, b in zip(new["stages"], self.result["stages"]):
            self.assertEqual({k: v for k, v in a.items() if k not in costcmd.FIELDS},
                             {k: v for k, v in b.items() if k not in costcmd.FIELDS})
        backup = common.read_json(os.path.join(self.cell, costcmd.BACKUP))
        self.assertEqual((backup["totals"]["cost_usd"], backup["totals"]["models"]), (17.0, []))
        self.assertFalse(os.path.exists(os.path.join(self.run, costguard.STOP)))  # 1.19 + 4.0 < 6.0
        self.assertIn("kept the recorded value of 1 ledger line", r.stdout)
        self.assertEqual(costguard.provider_spend(self.run, self.exp)["opencode-go"], round(want + 4.0, 8))
        self.assertEqual(self.run_cost().returncode, 0)  # again: the first backup stays
        self.assertEqual(common.read_json(os.path.join(self.cell, costcmd.BACKUP))["totals"]["cost_usd"], 17.0)

    def test_the_stop_marker_stays_while_the_recomputed_spend_is_over_the_cap(self):
        common.write_json(os.path.join(self.run, "experiment.json"),
                          exp_with(cost_cap_usd=100, provider_caps={"opencode-go": {"usd": 1.0}}))
        self.assertEqual(self.run_cost().returncode, 0)
        self.assertTrue(os.path.exists(os.path.join(self.run, costguard.STOP)))

    def test_ledger_lines_and_spent_json_are_kept_and_said_so(self):  # m2, m7
        before = open(os.path.join(self.run, costguard.LEDGER)).read()
        stopped = common.cell_dir(self.run, "task-mini/r3/base")
        common.write_json(os.path.join(stopped, costguard.SPENT), {"usd": 2.5})
        r = self.run_cost()
        self.assertEqual(open(os.path.join(self.run, costguard.LEDGER)).read(), before)
        self.assertIn("kept the recorded spend (spent.json) of 1 cell(s)", r.stdout)
        self.assertEqual(json.loads(r.stdout[:r.stdout.index("\nkept")])["cells_kept_spent_json"], ["task-mini/r3/base"])

    def test_a_run_made_before_provider_caps_existed_recomputes_without_editing_it(self):  # B1
        exp = exp_with(cost_cap_usd=100)
        del exp["provider_caps"]
        common.write_json(os.path.join(self.run, "experiment.json"), exp)
        r = self.run_cost()
        self.assertEqual(r.returncode, 0, r.stderr)
        new = common.read_json(os.path.join(self.cell, "result.json"))
        self.assertEqual((new["totals"]["models"], new["totals"]["model_sources"]), (["kimi-k3"], ["configured"]))
        self.assertFalse(os.path.exists(os.path.join(self.run, costguard.STOP)))  # ChatGPT spend is 0 < 100
        rep = report.cost_section(self.run, experiment.load(os.path.join(self.run, "experiment.json")), [])
        self.assertEqual(rep["providers"]["opencode-go"]["cells_cap"], None)  # uncapped, reported
        self.assertGreater(rep["providers"]["opencode-go"]["spent_usd"], 0)

    def test_a_running_cell_refuses_the_recompute(self):
        common.write_json(os.path.join(self.cell, costguard.LIVE), {"workspace": "/nowhere"})
        r = self.run_cost()
        self.assertEqual(r.returncode, 2)
        self.assertIn("a cell is running", r.stderr)


class Halt(unittest.TestCase):
    def test_a_halted_provider_stops_its_commands_only(self):
        runner = dispatch.Runner()
        out = {}
        threads = [threading.Thread(target=lambda t=t: out.update({t: runner.run(["sleep", "3"], tag=t)[0]}))
                   for t in ("a", "b")]
        for t in threads:
            t.start()
        time.sleep(0.5)
        runner.halt("a")
        threads[0].join(2)
        self.assertEqual(out, {"a": 130})
        self.assertFalse(threads[1].join(0.1) or not threads[1].is_alive())  # b still sleeping
        runner.stop()
        threads[1].join(3)
        self.assertEqual(out["b"], 130)
