import glob
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

from lanes import cell, common, costguard, experiment, report, usage
from tests.test_cell import ENTRY, FAKE, SHA, TASK, alive
from tests.test_dispatch import FAKE_LANES  # noqa: F401
from tests.test_end_to_end import BIN, Pipeline
from tests.test_report import Run

PRICES = common.read_json(os.path.join(os.path.dirname(costguard.__file__), "..", "..", "reproduce",
                                       "price-table-v1.json"))["models"]
TOP = {k: max(m[k] for m in PRICES.values()) for k in ("input", "cached_input", "output")}


def at_top(inp, cached, out):
    return (inp - cached) * TOP["input"] / 1e6 + cached * TOP["cached_input"] / 1e6 + out * TOP["output"] / 1e6


def request(model, inp, cached, out):
    return {"event": "request", "role": "build", "model": model,
            "usage": {"input": inp, "cached": cached, "output": out, "reasoning": 0}}


class Estimate(unittest.TestCase):
    def test_fallback_is_the_highest_price(self):
        self.assertEqual(costguard.pricing()[2], TOP)

    def test_unlisted_model_counts_at_the_fallback_rates(self):
        spend = costguard.log_spend([request("no-such-model", 1200, 800, 300)], None)
        self.assertAlmostEqual(spend, at_top(1200, 800, 300))

    def test_unpriced_model_in_guard_estimates_counts_at_the_stated_rate(self):
        row = costguard.guard_estimates()["gpt-6.1-terra"]
        self.assertEqual(row["as"], "gpt-6.1-sol")
        self.assertNotIn("gpt-6.1-terra", PRICES)
        sol = PRICES["gpt-6.1-sol"]
        want = 400 * sol["input"] / 1e6 + 800 * sol["cached_input"] / 1e6 + 300 * sol["output"] / 1e6
        spend = costguard.log_spend([request("gpt-6.1-terra", 1200, 800, 300)], None)
        self.assertAlmostEqual(spend, want)
        self.assertLess(spend, at_top(1200, 800, 300))

    def test_reported_cost_of_a_guard_estimated_model_stays_unpriced(self):
        calc, table, _ = costguard.pricing()
        tokens = {"input_tokens": 1200, "cached_input_tokens": 800, "output_tokens": 300}
        self.assertEqual(usage.request_cost("gpt-6.1-terra", tokens, table, calc),
                         (None, "unlisted_model: gpt-6.1-terra"))
        shaping = [{"event": "provider_call", "effective_model": "gpt-6.1-terra",
                    "usage": {"input": 1200, "cached": 800, "output": 300, "reasoning": 0}}]
        rec = usage.shape_requests(shaping)
        rec = usage._record("shape", None, [dict(r, model_source="effective") for r in rec], table, calc)
        self.assertIsNone(rec["cost_usd"])
        self.assertIn("unlisted_model", rec["cost_reason"])

    def test_listed_model_counts_at_its_price(self):
        spend = costguard.log_spend([request("gpt-6-luna", 1000000, 0, 1000000)], None)
        self.assertAlmostEqual(spend, 0.1 + 0.5)

    def test_unknown_usage_counts_a_fixed_amount(self):
        want = at_top(*(costguard.FALLBACK_TOKENS[k] for k in ("input_tokens", "cached_input_tokens", "output_tokens")))
        self.assertGreater(want, at_top(53_940, 0, 10_000) - 1e-9)  # above the largest request seen in real logs
        self.assertAlmostEqual(costguard.log_spend([request("gpt-6-luna", 0, 0, 0)], None), want)  # all zero
        shaping = [{"event": "provider_call", "effective_model": "m", "usage": {"input": None}}]
        self.assertAlmostEqual(costguard.log_spend(None, shaping), want)

    def test_a_half_written_last_line_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "log.jsonl")
            with open(path, "w") as f:
                f.write(json.dumps(request("gpt-6-luna", 1000000, 0, 0)) + '\n{"event": "requ')
            self.assertEqual(len(costguard._read(path)), 1)

    def test_a_malformed_cell_file_raises_rather_than_counting_zero(self):
        with tempfile.TemporaryDirectory() as d:
            common.write_json(os.path.join(common.cell_dir(d, "t/r1/a"), "result.json"), {"totals": {"cost_usd": [1]}})
            with self.assertRaises(Exception):
                costguard.estimate(d)

    def test_watcher_fails_closed_when_the_estimate_raises(self):
        with tempfile.TemporaryDirectory() as d:
            common.write_json(os.path.join(common.cell_dir(d, "t/r1/a"), "result.json"), {"totals": {"cost_usd": [1]}})
            with mock.patch("sys.stderr"), costguard.Watcher(d, {"cost_cap_usd": 5}, 0.05) as w:
                self.assertTrue(w.tripped.wait(5))
            self.assertIn("TypeError", w.error)

    def test_no_price_table_means_no_guard(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(usage, "COST_CALC", os.path.join(d, "none.py")), \
                mock.patch.object(costguard, "_pricing", None):
            with self.assertRaisesRegex(costguard.CostCapError, "fails closed"):
                costguard.check_start(d, {"cost_cap_usd": 5})

    def test_group_stops_at_the_deadline_not_a_poll_later(self):
        with tempfile.TemporaryDirectory() as d:
            c = cell.Cell(d, FAKE, d, 60)
            self.assertEqual(c._group(["sh", "-c", "sleep 0.05"], None, None, None, 0.01)[1], True)
            self.assertEqual(c._group(["true"], None, None, None, 5), (0, False))

    def test_cap_validation(self):
        exp = common.read_json(os.path.join(os.path.dirname(TASK), "experiment-good.json"))
        for bad in (0, -1, float("inf"), "4", True):
            with self.assertRaisesRegex(experiment.ExperimentError, "cost_cap_usd"):
                experiment.validate(dict(exp, cost_cap_usd=bad))
        self.assertEqual(costguard.caps(dict(exp, cost_cap_usd=4)), (4, 5.0))


def workspace(path, events):
    os.makedirs(os.path.join(path, ".kogen", "local", "runs", "x"))
    with open(os.path.join(path, ".kogen", "local", "runs", "x", "log.jsonl"), "w") as f:
        f.write(events)


THREE = "".join(json.dumps(request("gpt-6-luna", 1000000, 0, 0)) + "\n" for _ in range(3))  # $0.30


class Races(unittest.TestCase):
    """Spend moves between records while others read it: never an error, never counted twice or lost."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.run_dir = os.path.join(self.tmp, "run")
        os.makedirs(self.run_dir)

    def watch_while(self, churn, seconds=1.5):
        """Estimates (and a Watcher) while `churn(stop)` runs in a thread; returns the estimates."""
        stop, errors = threading.Event(), []

        def body():
            try:
                churn(stop)
            except Exception as e:  # pragma: no cover - reported below
                errors.append(e)
        t = threading.Thread(target=body)
        seen = []
        with costguard.Watcher(self.run_dir, {"cost_cap_usd": 1e9}, 0.001) as w:
            t.start()
            end = time.monotonic() + seconds
            while time.monotonic() < end:
                seen.append(costguard.estimate(self.run_dir))
            stop.set()
            t.join()
        self.assertEqual(errors, [])
        self.assertFalse(w.tripped.is_set(), w.error)  # a healthy run continues
        self.assertGreater(len(seen), 20)
        return seen

    def assert_counted_once(self, seen, usd):
        for a, b in zip(seen, seen[1:]):
            self.assertLessEqual(a, b + 1e-9, "spend went down: an attempt was lost or counted twice")
        for v in seen:
            self.assertAlmostEqual(v / usd, round(v / usd), places=6)

    def test_a_cell_finishing_mid_poll_is_counted_once(self):
        def churn(stop):
            i = 0
            while not stop.is_set():
                out, ws = common.cell_dir(self.run_dir, f"t/r{i}/a"), os.path.join(self.tmp, f"ws{i}")
                workspace(ws, THREE)
                with costguard.locked(self.run_dir):  # a cell starts: its dir and live.json appear together
                    os.makedirs(out)
                    common.write_json(os.path.join(out, costguard.LIVE), {"workspace": ws})
                if i % 2:  # finished with a result; else it stopped without one (spent.json)
                    common.write_json(os.path.join(out, "result.json"), {"totals": {"cost_usd": 0.3}})
                cell._drop_live(self.run_dir, out, ws)
                shutil.rmtree(ws)
                i += 1
        slow = costguard.workspace_spend

        def reader_in_the_window(ws):  # a slow reader: the cell ends while it reads the workspace
            time.sleep(0.003)
            return slow(ws)
        with mock.patch.object(costguard, "workspace_spend", reader_in_the_window):
            seen = self.watch_while(churn)
        self.assert_counted_once(seen, 0.3)
        self.assertGreater(seen[-1], 0.3)

    def test_a_retired_attempt_is_counted_once(self):
        out = common.cell_dir(self.run_dir, "t/r1/a")

        def churn(stop):
            while not stop.is_set():
                with costguard.locked(self.run_dir):  # an attempt that stopped without a result
                    os.makedirs(out)
                    common.write_json(os.path.join(out, costguard.SPENT), {"usd": 0.3})
                costguard.retire(self.run_dir, "t/r1/a", out)  # its retry starts
        seen = self.watch_while(churn)
        self.assert_counted_once(seen, 0.3)
        self.assertGreater(seen[-1], 0.6)

    def test_a_genuinely_unreadable_log_fails_closed(self):
        out, ws = common.cell_dir(self.run_dir, "t/r1/a"), os.path.join(self.tmp, "ws")
        workspace(ws, THREE + "not json\n" + THREE)  # a bad line that is not the last one
        common.write_json(os.path.join(out, costguard.LIVE), {"workspace": ws})
        with self.assertRaisesRegex(ValueError, "line 4 is not JSON"):
            costguard.estimate(self.run_dir)
        with mock.patch("sys.stderr"), costguard.Watcher(self.run_dir, {"cost_cap_usd": 1e9}, 0.01) as w:
            self.assertTrue(w.tripped.wait(5))
        self.assertIn("not JSON", w.error)
        workspace(os.path.join(self.tmp, "ws2"), json.dumps(request("gpt-6-luna", 5, 9, 1)) + "\n")  # cached > input
        common.write_json(os.path.join(out, costguard.LIVE), {"workspace": os.path.join(self.tmp, "ws2")})
        with self.assertRaisesRegex(ValueError, "unparsable usage"):
            costguard.estimate(self.run_dir)
        if os.geteuid() != 0:
            log = os.path.join(ws, ".kogen", "local", "runs", "x", "log.jsonl")
            with open(log, "w") as f:
                f.write(THREE)
            os.chmod(log, 0)
            common.write_json(os.path.join(out, costguard.LIVE), {"workspace": ws})
            with self.assertRaises(PermissionError):
                costguard.estimate(self.run_dir)

    def test_a_source_gone_without_a_final_record_is_retried_then_fails_closed(self):
        out = common.cell_dir(self.run_dir, "t/r1/a")
        common.write_json(os.path.join(out, costguard.LIVE), {"workspace": os.path.join(self.tmp, "gone")})
        self.assertAlmostEqual(costguard.estimate(self.run_dir, retry_s=0.3), 10.0)  # a phantom is reaped, not an error
        os.replace(os.path.join(out, costguard.REAPED), os.path.join(out, costguard.LIVE))
        os.remove(os.path.join(out, costguard.SPENT))
        t0 = time.monotonic()
        with mock.patch.object(costguard, "reap_phantoms"), \
                self.assertRaisesRegex(costguard.CostCapError, "gone with no final record.*fails closed"):
            costguard.estimate(self.run_dir, retry_s=0.3)  # the race the reaper does not cover: still fails closed
        self.assertGreaterEqual(time.monotonic() - t0, 0.3)
        timer = threading.Timer(0.2, common.write_json, (os.path.join(out, costguard.SPENT), {"usd": 0.3}))
        timer.start()
        with mock.patch.object(costguard, "reap_phantoms"):
            self.assertAlmostEqual(costguard.estimate(self.run_dir, retry_s=5), 0.3)  # the record arrived in time
        timer.join()


class Cell(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.tasks = os.path.join(self.tmp, "tasks")
        shutil.copytree(TASK, os.path.join(self.tasks, "task-mini"))
        path = os.path.join(self.tasks, "task-mini", "supplied", "gherkin", "intent.md")
        with open(path) as f:
            text = f.read()
        with open(path, "w") as f:
            f.write(text.replace("add-numbers", "task-mini"))
        self.home = os.path.join(self.tmp, "home")

    def make_run(self, phase, cap="default"):
        run = os.path.join(self.tmp, "run-" + phase)
        exp = {"id": "exp-mini", "phase": phase, "intent_form": "gherkin", "reps": 1, "deadline_s": 60,
               "kogen": {"repo": "https://example.invalid/kogen.git"}, "tasks": ["task-mini"], "hosts": ["local"],
               "decision_rule": {"kind": "paired-pass-rate"},
               "lanes": [{"name": n, "sha": SHA, "patch": None, "settings": {}} for n in ("base", "other")]}
        if cap is not None:
            exp["cost_cap_usd"] = 100 if cap == "default" else cap
        common.write_json(os.path.join(run, "experiment.json"), exp)
        return run

    def cell(self, run, lane="base", artifact=FAKE, force=False, **env):
        e = {**os.environ, "FAKE_KOGEN_TASK": TASK, "KOGEN_LANES_HOME": self.home, **env}
        return subprocess.run([sys.executable, ENTRY, run, f"task-mini/r1/{lane}", "--tasks", self.tasks,
                               "--artifact", artifact, *(["--force"] if force else [])], capture_output=True, text=True, env=e)

    def spent(self, run, lane, usd):
        common.write_json(os.path.join(common.cell_dir(run, f"task-mini/r1/{lane}"), "result.json"),
                          {"totals": {"cost_usd": usd}})

    def test_refuses_without_a_cap_and_says_how(self):
        run = self.make_run("shape", cap=None)
        r = self.cell(run)
        self.assertEqual(r.returncode, 2)
        self.assertIn('"cost_cap_usd"', r.stderr)
        self.assertFalse(os.path.exists(common.cell_dir(run, "task-mini/r1/base")))

    def test_refuses_to_start_past_the_soft_cap(self):
        run = self.make_run("shape", cap=0.5)
        self.spent(run, "other", 0.5)
        r = self.cell(run)
        self.assertEqual(r.returncode, 2)
        self.assertIn("cost cap reached: spend $0.5000 of the $0.5 cap", r.stderr)
        self.assertEqual(common.read_json(os.path.join(run, costguard.STOP))["cap"], "soft")
        self.assertFalse(os.path.exists(os.path.join(common.cell_dir(run, "task-mini/r1/base"), "result.json")))
        self.spent(run, "other", 0.4)  # under the cap again
        self.assertEqual(self.cell(run).returncode, 0)

    def test_unknown_price_uses_the_fallback(self):
        run = self.make_run("shape")
        self.assertEqual(self.cell(run).returncode, 0)
        res = common.read_json(os.path.join(common.cell_dir(run, "task-mini/r1/base"), "result.json"))
        self.assertIsNone(res["totals"]["cost_usd"])  # fake-model has no price row
        self.assertAlmostEqual(costguard.estimate(run), at_top(2000, 1500, 400), places=7)
        self.assertEqual(os.listdir(common.cell_dir(run, "task-mini/r1/base")).count(costguard.LIVE), 0)

    def test_hard_cap_aborts_a_running_cell_without_orphans(self):
        run = self.make_run("build", cap=0.05)  # hard cap 0.0625; a fake build request is worth 0.0198
        pids = os.path.join(self.tmp, "pids")
        wrapper = os.path.join(self.tmp, "kogen")
        with open(wrapper, "w") as f:
            f.write(f'#!/bin/sh\nif [ "$2" = build ]; then sleep 300 &\necho $$ $! > {pids}; fi\n'
                    f'exec {sys.executable} {FAKE} "$@"\n')
        os.chmod(wrapper, 0o755)
        t0 = time.monotonic()
        r = self.cell(run, artifact=wrapper, FAKE_KOGEN_REQUESTS="40", FAKE_KOGEN_DELAY_S="0.25",
                      LANES_COST_WATCH_S="0.1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertLess(time.monotonic() - t0, 15)  # the build alone would take 10 s
        path = common.cell_dir(run, "task-mini/r1/base")
        res = common.read_json(os.path.join(path, "result.json"))
        self.assertEqual(res["outcome"], "cost_cap")
        build = next(s for s in res["stages"] if s["stage"] == "build")
        self.assertEqual(build["outcome"], "cost_cap")
        self.assertTrue(4 <= build["requests"] < 40, build["requests"])
        self.assertEqual(report.classify(res, [], None, "build"), "incomplete")
        self.assertEqual(report.plumbing({"result": res, "log": [], "class": "incomplete"}), "cost_cap")
        with open(pids) as f:
            started = [int(x) for x in f.read().split()]
        for pid in started:
            self.assertFalse(alive(pid), "orphan process")
        self.assertGreaterEqual(costguard.estimate(run), 0.0625)
        self.assertEqual(common.read_json(os.path.join(run, costguard.STOP))["cap"], "hard")

    def test_a_guard_that_cannot_read_the_spend_stops_the_cell(self):
        run = self.make_run("build")
        bad = common.cell_dir(run, "task-mini/r1/other")  # a bad file appears while the build runs
        wrapper = os.path.join(self.tmp, "kogen")
        with open(wrapper, "w") as f:
            f.write(f'#!/bin/sh\nif [ "$2" = build ]; then mkdir -p {bad}; '
                    f'echo \'{{"totals": {{"cost_usd": [1]}}}}\' > {bad}/result.json; fi\n'
                    f'exec {sys.executable} {FAKE} "$@"\n')
        os.chmod(wrapper, 0o755)
        r = self.cell(run, artifact=wrapper, FAKE_KOGEN_REQUESTS="40", FAKE_KOGEN_DELAY_S="0.25",
                      LANES_COST_WATCH_S="0.1")
        self.assertEqual(r.returncode, 0, r.stderr)
        res = common.read_json(os.path.join(common.cell_dir(run, "task-mini/r1/base"), "result.json"))
        self.assertEqual(res["outcome"], "cost_cap")
        self.assertIn("TypeError", res["cost_error"])
        r = self.cell(run, "other")  # and no cell starts while it is unreadable
        self.assertEqual((r.returncode, "fails closed" in r.stderr), (2, True))

    def test_a_rerun_keeps_the_spend_of_the_earlier_attempt(self):
        run = self.make_run("shape")
        path = common.cell_dir(run, "task-mini/r1/base")
        common.write_json(os.path.join(path, costguard.SPENT), {"usd": 0.3})  # an attempt that left no result
        self.assertEqual(self.cell(run).returncode, 0)
        self.assertAlmostEqual(costguard.estimate(run), 0.3 + at_top(2000, 1500, 400), places=7)
        self.assertEqual(self.cell(run, force=True).returncode, 0)  # a finished cell rerun: its spend stays too
        self.assertAlmostEqual(costguard.estimate(run), 0.3 + 2 * at_top(2000, 1500, 400), places=7)

    def test_a_cell_under_the_soft_cap_runs_to_the_end(self):
        run = self.make_run("shape", cap=0.01)  # this cell's own shape (0.0265) will pass it
        self.spent(run, "other", 0.001)
        self.assertEqual(self.cell(run).returncode, 0)  # under the soft cap: starts, finishes, outcome ok
        res = common.read_json(os.path.join(common.cell_dir(run, "task-mini/r1/base"), "result.json"))
        self.assertEqual(res["outcome"], "ok")


class ReportSection(unittest.TestCase):
    def set_cap(self, run, cap):
        path = os.path.join(run.tmp.name, "experiment.json")
        common.write_json(path, dict(common.read_json(path), cost_cap_usd=cap))

    def test_spend_vs_cap_per_lane_and_total(self):
        run = Run(self, passes={"base": [True] * 4, "cand": [True] * 4}, costs={"base": 1.0, "cand": 0.5})
        self.set_cap(run, 10)
        rep = run.report()["cost"]
        self.assertEqual((rep["spent_usd"], rep["lanes"], rep["hard_cap_usd"], rep["stopped"]),
                         (6.0, {"base": 4.0, "cand": 2.0}, 12.5, None))
        text = report.render(run.report())
        self.assertIn("## Spend vs cost cap", text)
        self.assertIn("| total |  | 6.0000 | 60% | 48% |", text)
        self.assertNotIn("COST CAP STOPPED", text)

    def test_a_line_when_a_cap_stopped_the_run(self):
        run = Run(self, passes={"base": [True] * 4, "cand": [True] * 4}, costs={"base": 1.0, "cand": 1.0},
                  unfinished=("t2/r2/cand",))
        self.set_cap(run, 6)
        shutil.rmtree(common.cell_dir(run.tmp.name, "t2/r2/cand"))  # never started
        self.assertIsNone(run.report()["cost"]["stopped"])  # spend over the cap alone says nothing: no stop was recorded
        costguard.record_stop(run.tmp.name, "soft", 7.0)
        rep = run.report()
        self.assertEqual(rep["cost"]["stopped"], "soft")
        self.assertIn("COST CAP STOPPED THE RUN: the soft cap was reached; 1 cell(s) were not started",
                      report.render(rep))
        res = os.path.join(common.cell_dir(run.tmp.name, "t1/r1/base"), "result.json")
        common.write_json(res, dict(common.read_json(res), outcome="cost_cap"))
        self.assertEqual(run.report()["cost"]["stopped"], "hard")  # a cost_cap cell outranks a soft note
        costguard.record_stop(run.tmp.name, "hard", 8.0)
        self.assertEqual(common.read_json(os.path.join(run.tmp.name, costguard.STOP))["cap"], "hard")  # hard wins
        costguard.record_stop(run.tmp.name, "soft", 9.0)
        self.assertEqual(common.read_json(os.path.join(run.tmp.name, costguard.STOP))["cap"], "hard")
        rep = run.report()
        self.assertEqual((rep["cost"]["stopped"], rep["cost"]["cost_cap_cells"]), ("hard", ["t1/r1/base"]))
        self.assertIn("the hard cap ended 1 cell(s) as cost_cap (t1/r1/base)", report.render(rep))

    def test_no_cap_set(self):
        run = Run(self, passes={"base": [True] * 4})
        self.assertIn("soft cap: none set; hard cap: none set", report.render(run.report()))


@unittest.skipUnless(shutil.which("rsync") and shutil.which("go"), "rsync or go not installed")
class LanesRun(unittest.TestCase):
    """`lanes-run` end to end with the fake Kogen emitting usage over time (build phase, 4 cells)."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.p = Pipeline(cls._tmp.name)
        cls.p.env.update(FAKE_KOGEN_REQUESTS="30", FAKE_KOGEN_DELAY_S="0.5", LANES_COST_WATCH_S="0.2")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def start(self, exp_id, cap, hosts=None):
        p = self.p
        path = p.experiment(exp_id, "build")
        exp = common.read_json(path)
        exp["cost_cap_usd"] = cap
        if hosts:
            exp["hosts"] = hosts
        common.write_json(path, exp)
        run = os.path.join(p.tmp, "runs", exp_id)
        p.cli("lanes-build", path, "--run-dir", run)
        p.cli("lanes-plan", path, "--run-dir", run)
        return run

    def finished(self, run):
        cells = os.path.join(run, "cells")
        return sorted(os.path.relpath(os.path.dirname(p), cells) for p in
                      glob.glob(os.path.join(cells, "*", "r*", "*", "result.json")))

    def test_local_hard_cap_stops_every_running_cell_and_starts_no_more(self):
        run = self.start("cap-local", 0.004)  # hard cap 0.005; a request is worth 0.0002
        r = self.p.cli("lanes-run", run, "--hosts", self.p.hosts, ok=False)
        self.assertEqual(r.returncode, 3, r.stderr)
        results = [common.read_json(os.path.join(run, "cells", c, "result.json")) for c in self.finished(run)]
        self.assertEqual([x["outcome"] for x in results], ["cost_cap", "cost_cap"])  # two slots, no third cell
        self.assertEqual(len(glob.glob(os.path.join(run, "cells", "*", "r*", "*"))), 2)
        self.assertGreaterEqual(costguard.estimate(run), 0.005)
        self.assertEqual(common.read_json(os.path.join(run, costguard.STOP))["cap"], "hard")
        self.p.cli("lanes-report", run)
        self.assertIn("COST CAP STOPPED THE RUN: the hard cap ended 2 cell(s)", open(os.path.join(run, "report.md")).read())

    def test_remote_cells_are_watched_by_the_controller(self):
        # one cell per host, each alone under the hard cap (0.0075): only the controller, adding up
        # the live spend of both hosts, can stop them
        roots = [os.path.join(self.p.tmp, f"remote-root-{n}") for n in (1, 2)]
        hosts = os.path.join(self.p.tmp, "remote-hosts.json")
        common.write_json(hosts, {f"far{n}": {"target": f"far{n}.invalid", "slots": 1, "root": roots[n - 1]}
                                  for n in (1, 2)})
        run = self.start("cap-remote", 0.006, hosts=["far1", "far2"])
        env = dict(self.p.env, LANES_SSH=os.path.join(os.path.dirname(BIN), "tests", "fixtures", "fake-ssh"))
        r = subprocess.run([sys.executable, os.path.join(BIN, "lanes-run"), run, "--hosts", hosts], env=env,
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertIn("hard cost cap reached", r.stderr)
        self.assertEqual(self.finished(run), [])  # stopped before they could finish (30 requests = 15 s)
        with open(os.path.join(run, costguard.LEDGER)) as f:  # what the killed attempts spent is kept
            ledger = [json.loads(line) for line in f]
        self.assertEqual(len(ledger), 2)
        self.assertGreaterEqual(costguard.estimate(run), 0.0075)
        self.assertEqual(common.read_json(os.path.join(run, costguard.STOP))["cap"], "hard")
        for root in roots:
            self.assertEqual([p for p in glob.glob(os.path.join(root, "runs", "cap-remote", "*")) if "pgid-" in p], [])


if __name__ == "__main__":
    unittest.main()
