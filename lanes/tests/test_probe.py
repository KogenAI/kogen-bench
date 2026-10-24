"""The probe phase: a synthetic corpus of three items, fake probe commands, the real entry points."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from lanes import common, costguard, experiment, probe, report

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures", "probe")
BIN = os.path.join(HERE, "..", "bin")

# Item i1 is the hand-checked one. Expected files a.py, b.py; symbols a.py 1-3 and b.py 10-12; budget 100.
#   rank A keeps a.py(2) and c.py (40 + 40; the third request, 40 more, would pass 100): file P 1/2 R 1/2,
#     symbol: one claim (a.py 2-2) hits one of two symbols.
#   rank B keeps all three (60 + 30 + 10 = 100, exactly the budget): file P 2/3 R 1; both symbols hit
#     (a.py 3-9 touches a.py 1-3 at line 3), both claims hit.
# i2 and i3: one expected file; A ranks it, B does not.
I1 = {"id": "i1", "input": {"repo": "repos/i1", "token_budget": 100,
      "rank_a": [{"path": "a.py", "start": 2, "end": 2, "tokens": 40}, {"path": "c.py", "tokens": 40},
                 {"path": "b.py", "start": 20, "end": 25, "tokens": 40}],
      "rank_b": [{"path": "b.py", "start": 11, "end": 11, "tokens": 60}, {"path": "a.py", "start": 3, "end": 9, "tokens": 30},
                 {"path": "c.py", "tokens": 10}]},
      "expected": {"touched_files": ["a.py", "b.py"],
                   "touched_symbols": [{"path": "a.py", "name": "f", "start": 1, "end": 3},
                                       {"path": "b.py", "name": "g", "start": 10, "end": 12}]}}


def simple(i):
    return {"id": i, "input": {"repo": f"repos/{i}", "token_budget": 10,
                               "rank_a": [{"path": "x.py", "tokens": 10}], "rank_b": [{"path": "y.py", "tokens": 10}]},
            "expected": {"touched_files": ["x.py"]}}


ITEMS = [I1, simple("i2"), simple("i3")]
F1 = {"a": {"i1": 0.5, "i2": 1.0, "i3": 1.0}, "b": {"i1": 0.8, "i2": 0.0, "i3": 0.0}}


def lane(name, key, script="rank.py", **extra):
    probe_ = {"command": [sys.executable, os.path.join(FIX, script)], "args": {"key": key}}
    return {"name": name, "probe": probe_, **extra}


def write_corpus(path, items=ITEMS):
    for item in items:
        repo = os.path.join(path, "repos", item["id"])
        os.makedirs(repo)
        with open(os.path.join(repo, "a.py"), "w") as f:
            f.write("def f():\n    pass\n")
    with open(os.path.join(path, "items.jsonl"), "w") as f:
        f.writelines(json.dumps(i) + "\n" for i in items)


class ProbeCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.corpus = os.path.join(self.tmp, "corpus")
        write_corpus(self.corpus)
        self.home = os.path.join(self.tmp, "home")
        self.run_dir = os.path.join(self.tmp, "run")
        self.exp_path = os.path.join(self.tmp, "experiment.json")
        self.hosts = os.path.join(self.tmp, "hosts.json")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 1}})
        self.env = dict(os.environ, KOGEN_LANES_HOME=self.home)
        self.env.pop("KOGEN_LANES_CORPUS", None)
        self.exp = {"id": "probe-1", "phase": "probe", "corpus": "corpus", "reps": 1, "deadline_s": 20,
                    "cost_cap_usd": 5, "hosts": [],
                    "lanes": [lane("a", "rank_a"), lane("b", "rank_b")],
                    "grader": {"kind": "set_recall_precision_at_budget"},
                    "decision_rule": {"kind": "descriptive"}}

    def write_exp(self, **fields):
        self.exp.update(fields)
        common.write_json(self.exp_path, self.exp)

    def call(self, name, *args, timeout=120):
        return subprocess.run([sys.executable, os.path.join(BIN, name), *args], env=self.env, capture_output=True,
                              text=True, timeout=timeout)

    def plan(self, *extra):
        self.write_exp()
        return self.call("lanes-plan", self.exp_path, "--run-dir", self.run_dir, *extra)

    def run_all(self, *extra):
        return self.call("lanes-run", self.run_dir, "--hosts", self.hosts, "--skip-preflight", *extra)

    def planned(self):
        p = self.plan()
        self.assertEqual(p.returncode, 0, p.stderr)

    def result(self, cell):
        return common.read_json(os.path.join(common.cell_dir(self.run_dir, cell), "result.json"))

    def report(self):
        p = self.call("lanes-report", self.run_dir)
        self.assertEqual(p.returncode, 0, p.stderr)
        return common.read_json(os.path.join(self.run_dir, "report.json")), p.stdout


class Graders(unittest.TestCase):
    CONFIG = {"kind": "set_recall_precision_at_budget"}

    def grade(self, item, ranked, args=None):
        probe_lane = {"probe": {"command": ["x"], "args": args or {}}}
        return probe.grade(self.CONFIG, item, {"ranked": ranked}, probe_lane)

    def test_file_and_symbol_levels_and_the_budget_cut(self):
        a = self.grade(I1, I1["input"]["rank_a"])
        self.assertEqual((a["tokens_used"], a["items_kept"]), (80, 2))
        self.assertEqual([a[f"touched_files.file.{k}"] for k in ("recall", "precision", "f1")], [0.5, 0.5, 0.5])
        self.assertEqual([a[f"touched_symbols.symbol.{k}"] for k in ("recall", "precision")], [0.5, 1.0])
        self.assertAlmostEqual(a["touched_symbols.symbol.f1"], 2 / 3)
        self.assertEqual(a["touched_symbols.file.recall"], 0.5)  # a symbol set also scores at file level
        b = self.grade(I1, I1["input"]["rank_b"])
        self.assertEqual((b["tokens_used"], b["items_kept"]), (100, 3))  # exactly the budget fits
        self.assertEqual((b["touched_files.file.recall"], b["touched_files.file.precision"]), (1.0, 2 / 3))
        self.assertAlmostEqual(b["touched_files.file.f1"], 0.8)
        self.assertEqual((b["touched_symbols.symbol.recall"], b["touched_symbols.symbol.precision"],
                          b["touched_symbols.symbol.f1"]), (1.0, 1.0, 1.0))

    def test_lane_budget_beats_the_item_budget(self):
        m = self.grade(I1, I1["input"]["rank_b"], {"token_budget": 60})
        self.assertEqual((m["tokens_used"], m["items_kept"]), (60, 1))
        self.assertEqual(self.grade(I1, I1["input"]["rank_b"], {"token_budget": 59})["items_kept"], 0)
        self.assertEqual(self.grade(I1, I1["input"]["rank_b"], {"token_budget": 59})["touched_files.file.f1"], 0.0)

    def test_range_overlap_rule(self):
        item = {"input": {}, "expected": {"s": [{"path": "a.py", "start": 5, "end": 8}]}}
        hit = lambda s, e, path="a.py": self.grade(item, [{"path": path, "start": s, "end": e, "tokens": 1}])["s.symbol.recall"]
        self.assertEqual([hit(1, 4), hit(1, 5), hit(8, 9), hit(9, 12), hit(6, 7), hit(1, 20)], [0.0, 1.0, 1.0, 0.0, 1.0, 1.0])
        self.assertEqual(hit(5, 8, "b.py"), 0.0)  # same lines, other path
        whole_file = self.grade(item, [{"path": "a.py", "tokens": 1}])  # no range: a file claim, not a symbol claim
        self.assertEqual((whole_file["s.file.recall"], whole_file["s.symbol.recall"], whole_file["s.symbol.precision"]),
                         (1.0, 0.0, 0.0))

    def test_sets_named_in_the_grader_config(self):
        m = probe.grade({**self.CONFIG, "sets": ["touched_files"]}, I1, {"ranked": I1["input"]["rank_a"]},
                        {"probe": {"command": ["x"]}})
        self.assertFalse([k for k in m if k.startswith("touched_symbols")])
        self.assertEqual(m["tokens_used"], 80)  # the lane names no budget, so the item's 100 applies

    def test_absent_or_empty_expected_set_is_undefined_not_an_error(self):
        item = {"input": {}, "expected": {"touched_files": ["a.py"], "read_files": []}}
        cfg = {**self.CONFIG, "sets": ["touched_files", "read_files", "nothing"]}
        m = probe.grade(cfg, item, {"ranked": [{"path": "a.py", "tokens": 1}]}, {"probe": {"command": ["x"]}})
        self.assertEqual(m["touched_files.file.recall"], 1.0)
        self.assertFalse([k for k in m if k.startswith(("read_files", "nothing"))])
        self.assertEqual(probe.undefined_sets(cfg, item),
                         {"read_files": "expected set empty", "nothing": "expected set absent"})
        self.assertEqual(probe.undefined_sets(self.CONFIG, item), {"read_files": "expected set empty"})

    def test_bad_output_is_refused(self):
        with self.assertRaises(probe.ProbeError):
            probe.grade(self.CONFIG, I1, {"ranked": [{"path": "a.py"}]}, {"probe": {"command": ["x"]}})

    def test_exact_match_and_keys(self):
        item = {"input": {}, "expected": {"n": 1, "ok": True, "extra": [1]}}
        lane_ = {"probe": {"command": ["x"]}}
        exact = lambda out, **cfg: probe.grade({"kind": "exact_match", **cfg}, item, out, lane_)["exact"]
        self.assertEqual(exact({"n": 1.0, "ok": True, "extra": [1]}), 1.0)  # 1 and 1.0 are one JSON number
        self.assertEqual(exact({"n": 1, "ok": 1, "extra": [1]}), 0.0)  # true is not 1
        self.assertEqual(exact({"n": 1, "ok": True}), 0.0)
        self.assertEqual(exact({"n": 1, "ok": True}, keys=["n", "ok"]), 1.0)
        self.assertEqual(exact({"n": 2}, keys=["n"]), 0.0)

    def test_command_grader_gets_item_and_output(self):
        cfg = {"kind": "command", "command": [sys.executable, os.path.join(FIX, "grader.py")]}
        m = probe.grade(cfg, I1, {"ranked": [1, 2, 3]}, {"probe": {"command": ["x"]}})
        self.assertEqual(m, {"listed": 3, "has_expected": 1.0})
        with self.assertRaises(probe.ProbeError):
            probe.grade({"kind": "command", "command": ["false"]}, I1, {}, {"probe": {"command": ["x"]}})


class Phase(ProbeCase):
    def test_plan_run_report_end_to_end(self):
        self.planned()
        plan = common.read_json(os.path.join(self.run_dir, "PLAN.json"))
        self.assertEqual(set(plan["hashes"]["corpus"]["items"]), {"i1", "i2", "i3"})
        self.assertEqual(set(plan["hashes"]["lanes"]["a"]), {"patch", "settings", "probe", "files"})
        self.assertNotIn(os.path.expanduser("~"), json.dumps(plan["hashes"]))
        p = self.run_all()
        self.assertEqual(p.returncode, 0, p.stderr)
        cells = common.read_jsonl(os.path.join(self.run_dir, "plan.jsonl"))
        self.assertEqual(len(cells), 6)
        rep, line = self.report()
        for name, key in (("a", "a"), ("b", "b")):
            lane_ = next(l for l in rep["lanes"] if l["name"] == name)
            self.assertEqual(lane_["cells"], {"planned": 3, "finished": 3, "ok": 3})
            self.assertAlmostEqual(lane_["metrics"]["touched_files.file.f1"]["mean"], sum(F1[key].values()) / 3)
            self.assertIsNotNone(lane_["metrics"]["touched_files.file.f1"]["ci"])
            for metric in ("wall_s", "cpu_s", "peak_rss_kb", "cost_usd"):
                self.assertIn(metric, lane_["metrics"])
        a = next(l for l in rep["lanes"] if l["name"] == "a")
        self.assertEqual(a["metrics"]["touched_symbols.symbol.f1"]["items"], 1)  # only i1 has symbols
        self.assertIn("none", rep["verdict"]["decision"])
        self.assertTrue(os.path.isfile(os.path.join(self.run_dir, "report.md")))

    def test_command_sees_input_and_args_only(self):
        self.planned()
        self.assertEqual(self.run_all().returncode, 0)
        out = common.read_json(os.path.join(common.cell_dir(self.run_dir, "i1/r1/a"), "output.json"))
        seen = out["seen"]
        self.assertEqual(seen["stdin_keys"], ["args", "input"])  # `expected` is never given
        self.assertEqual(seen["item_dir"], "i1")
        self.assertEqual(seen["corpus"], self.corpus)
        self.assertFalse(seen["cwd"].startswith(self.corpus))
        self.assertFalse(os.path.exists(seen["cwd"]))  # a fresh temp dir, gone afterwards
        res = self.result("i1/r1/a")
        self.assertEqual((res["outcome"], res["exit_code"], res["phase"]), ("ok", 0, "probe"))

    def test_task_sign_rule_over_items(self):
        self.exp["decision_rule"] = {"kind": "task_sign", "baseline": "b", "candidate": "a",
                                     "metric": "touched_files.file.f1", "max_p": 0.6}
        self.planned()
        self.assertEqual(self.run_all().returncode, 0)
        rep, line = self.report()
        v = rep["verdict"]
        # A minus B per item: -0.3, +1, +1: two wins, one loss, p = P(X >= 2 of 3) = 1/2
        self.assertEqual((v["decision"], v["candidate_better"], v["baseline_better"], v["p"]), ("keep", 2, 1, "0.5"))
        self.assertAlmostEqual(float(report.ratio(v["gain"])), 1.7 / 3, places=4)
        self.assertIn("touched_files.file.f1", line)

    def test_keep_revert_with_a_split(self):
        self.exp["decision_rule"] = {"kind": "keep_revert", "baseline": "b", "candidate": "a",
                                     "metric": "touched_files.file.f1", "min_effect": 0.1,
                                     "improves": {"test": "task_sign", "max_p": 1}}
        self.exp["split"] = {"train": ["i1", "i2"], "test": ["i3"]}
        self.planned()
        self.assertEqual(self.run_all().returncode, 0)
        rep, _ = self.report()
        v = rep["verdict"]
        self.assertEqual((v["decision"], v["case"]), ("keep", "improved_both"))
        self.assertAlmostEqual(v["splits"]["train"]["difference"], 0.35)  # (-0.3 + 1) / 2
        self.assertEqual(v["splits"]["test"]["difference_exact"], "1")
        lower = {**self.exp["decision_rule"], "better": "lower"}
        self.exp["decision_rule"] = lower
        rep = probe.report_probe(self.run_dir, experiment.validate(json.loads(json.dumps(self.exp))))
        self.assertEqual(rep["verdict"]["decision"], "revert")

    def undefined_run(self, rule, split=None):
        """Five items; `read_files` is empty for i3 and absent for i4. A beats B on i1 and i5, B beats A on i2."""
        shutil.rmtree(self.corpus)
        items = [self.item("i1", read=["x.py"]), self.item("i2", read=["y.py"]), self.item("i3", read=[]),
                 self.item("i4"), self.item("i5", read=["x.py"])]
        write_corpus(self.corpus, items)
        self.exp["decision_rule"] = {"baseline": "b", "candidate": "a", "metric": "read_files.file.recall", **rule}
        if split:
            self.exp["split"] = split
        self.planned()
        self.assertEqual(self.run_all().returncode, 0)

    @staticmethod
    def item(i, **expected):
        item = simple(i)
        if "read" in expected:
            item["expected"]["read_files"] = expected["read"]
        return item

    def test_items_with_an_undefined_metric_are_left_out_of_the_rule(self):
        self.undefined_run({"kind": "task_sign", "max_p": 0.6})
        rep, line = self.report()
        v = rep["verdict"]
        self.assertEqual((v["decision"], v["candidate_better"], v["baseline_better"], v["p"]), ("keep", 2, 1, "0.5"))
        self.assertEqual(v["left_out"], {"i3": "expected set empty", "i4": "expected set absent"})
        self.assertIn("2 item(s) left out, metric undefined (expected set absent: 1, expected set empty: 1)", line)
        self.assertNotIn("no ok cell", line)
        for l in rep["lanes"]:
            m = l["metrics"]["read_files.file.recall"]
            self.assertEqual((m["items"], m["left_out"]["count"]), (3, 2))
            self.assertEqual(m["left_out"]["reasons"], {"expected set absent": 1, "expected set empty": 1})
            self.assertEqual(l["metrics"]["touched_files.file.recall"]["items"], 5)  # defined for every item
            self.assertEqual(l["metrics"]["touched_files.file.recall"]["left_out"]["count"], 0)
        with open(os.path.join(self.run_dir, "report.md")) as f:
            self.assertIn("expected set empty: 1", f.read())

    def test_a_missing_ok_cell_is_still_incomplete_and_a_metric_nobody_has_is_invalid(self):
        self.undefined_run({"kind": "task_sign", "max_p": 0.6})
        shutil.rmtree(common.cell_dir(self.run_dir, "i5/r1/a"))
        rep, _ = self.report()
        v = rep["verdict"]
        self.assertEqual((v["decision"], v["ungraded"], sorted(v["left_out"])), ("incomplete", ["i5"], ["i3", "i4"]))
        self.assertIn("have no ok cell on a lane: i5", v["line"])
        m = next(l for l in rep["lanes"] if l["name"] == "a")["metrics"]["read_files.file.recall"]
        self.assertEqual(m["left_out"]["reasons"]["no ok cell"], 1)
        exp = experiment.validate(json.loads(json.dumps({**self.exp, "decision_rule": {
            "kind": "task_sign", "baseline": "b", "candidate": "a", "metric": "nothing.file.f1"}})))
        self.assertEqual(probe.report_probe(self.run_dir, exp)["verdict"]["decision"], "invalid_rule")

    def test_keep_revert_leaves_undefined_items_out_of_a_split(self):
        self.undefined_run({"kind": "keep_revert", "min_effect": 0.1, "improves": {"test": "task_sign", "max_p": 1}},
                           {"train": ["i1", "i2", "i3"], "test": ["i4", "i5"]})
        rep, _ = self.report()
        v = rep["verdict"]
        self.assertNotEqual(v["decision"], "incomplete")
        self.assertEqual((v["splits"]["train"]["tasks"], v["splits"]["test"]["tasks"]), (2, 1))
        self.assertEqual(sorted(v["left_out"]), ["i3", "i4"])

    def test_incomplete_when_an_item_has_no_graded_cell(self):
        self.exp["decision_rule"] = {"kind": "task_sign", "baseline": "b", "candidate": "a", "metric": "exact"}
        self.exp["grader"] = {"kind": "exact_match"}
        self.planned()
        self.assertEqual(self.run_all().returncode, 0)
        rep, _ = self.report()
        self.assertEqual(rep["verdict"]["decision"], "unresolved")  # every exact score is 0: no item differs
        shutil.rmtree(common.cell_dir(self.run_dir, "i2/r1/a"))
        rep, _ = self.report()
        self.assertEqual(rep["verdict"]["decision"], "incomplete")
        self.assertEqual(rep["verdict"]["ungraded"], ["i2"])

    def test_usage_naming_another_provider_than_the_lane_is_bad_output(self):
        path = os.path.join(self.tmp, "prov.py")
        with open(path, "w") as f:
            f.write('import json\nprint(json.dumps({"output": {"ranked": []}, "usage": [{"provider": "opencode-go", '
                    '"model": "kimi-k3", "input_tokens": 1, "cached_input_tokens": 0, "output_tokens": 1}]}))\n')
        self.exp["lanes"] = [{"name": "p", "probe": {"command": [sys.executable, path]}}]
        self.planned()
        self.assertEqual(self.call("lanes-cell", self.run_dir, "i1/r1/p").returncode, 0)
        res = self.result("i1/r1/p")
        self.assertEqual(res["outcome"], "bad_output")
        self.assertIn("settings.models", res["detail"])
        self.assertEqual(res["totals"]["requests"], 1)  # its spend still counts
        self.exp["lanes"][0]["settings"] = {"models": {"x": "opencode-go/kimi-k3 high"}}
        self.exp["provider_caps"] = {"opencode-go": {"cells": 5}}
        self.exp["id"] = "probe-2"
        self.run_dir = os.path.join(self.tmp, "run2")
        self.planned()
        self.assertEqual(self.call("lanes-cell", self.run_dir, "i1/r1/p").returncode, 0)
        self.assertEqual(self.result("i1/r1/p")["outcome"], "ok")

    def test_command_next_to_the_experiment_is_resolved_hashed_and_pinned(self):
        shutil.copy(os.path.join(FIX, "rank.py"), os.path.join(self.tmp, "probe.py"))
        self.exp["lanes"] = [{"name": "a", "probe": {"command": [sys.executable, "probe.py"], "args": {"key": "rank_a"}}}]
        self.planned()
        plan = common.read_json(os.path.join(self.run_dir, "PLAN.json"))
        self.assertEqual(set(plan["hashes"]["lanes"]["a"]["files"]), {"0", "1"})  # the interpreter and the script
        self.assertNotIn(self.tmp, json.dumps(plan["hashes"]))
        p = self.call("lanes-preflight", self.run_dir)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(self.run_all().returncode, 0)
        self.assertEqual(self.result("i1/r1/a")["outcome"], "ok")
        with open(os.path.join(self.tmp, "probe.py"), "a") as f:
            f.write("# edited\n")
        p = self.run_all()
        self.assertEqual(p.returncode, 2)
        self.assertIn("no longer match PLAN.json", p.stderr)

    def test_preflight_refuses_unresolved_and_non_executable_commands(self):
        script = os.path.join(self.tmp, "tool.sh")
        with open(script, "w") as f:
            f.write("#!/bin/sh\n")
        os.chmod(script, 0o644)  # present but not executable
        self.exp["lanes"] = [{"name": "plain", "probe": {"command": ["tool.sh"]}},
                             {"name": "gone", "probe": {"command": [sys.executable, "./missing.py"]}},
                             {"name": "none", "probe": {"command": ["no-such-command-anywhere"]}}]
        self.planned()
        p = self.call("lanes-preflight", self.run_dir)
        self.assertEqual(p.returncode, 1)
        for name in ("plain", "gone", "none"):
            self.assertIn(f"{name}: REFUSED", p.stdout)
        os.chmod(script, 0o755)
        self.exp["lanes"] = self.exp["lanes"][:1]
        self.planned()
        self.assertEqual(self.call("lanes-preflight", self.run_dir).returncode, 0)

    def test_probe_usage_feeds_the_cost_guard(self):
        self.exp["lanes"] = [lane("spend", "rank_a", "spend.py")]
        self.exp["cost_cap_usd"] = 0.09  # one cell is 1M input tokens of gpt-6-luna, $0.10: over the soft cap, under the hard
        self.planned()
        p = self.run_all()
        self.assertEqual(p.returncode, 3, p.stderr)
        done = [c for c in ("i1", "i2", "i3") if os.path.isfile(os.path.join(common.cell_dir(self.run_dir, f"{c}/r1/spend"), "result.json"))]
        self.assertEqual(len(done), 1)  # the soft cap stopped the others
        res = self.result(f"{done[0]}/r1/spend")
        self.assertAlmostEqual(res["totals"]["cost_usd"], 0.1)
        self.assertEqual(res["totals"]["input_tokens"], 1000000)
        self.assertAlmostEqual(costguard.estimate(self.run_dir), 0.1)
        self.assertIn("cost cap reached", p.stderr)
        rep, _ = self.report()
        self.assertAlmostEqual(rep["cost"]["spent_usd"], 0.1)
        self.assertEqual(rep["cost"]["stopped"], "soft")

    def test_bad_usage_is_a_bad_output_cell(self):
        path = os.path.join(self.tmp, "bad.py")
        with open(path, "w") as f:
            f.write('import json\nprint(json.dumps({"output": {"ranked": []}, "usage": [{"input_tokens": 5, "cached_input_tokens": 9}]}))\n')
        self.exp["lanes"] = [{"name": "bad", "probe": {"command": [sys.executable, path]}}]
        self.planned()
        self.assertEqual(self.call("lanes-cell", self.run_dir, "i1/r1/bad").returncode, 0)
        res = self.result("i1/r1/bad")
        self.assertEqual(res["outcome"], "bad_output")
        self.assertIn("cached_input_tokens", res["detail"])

    def test_hung_probe_is_killed_at_the_deadline_with_no_orphan(self):
        pidfile = os.path.join(self.tmp, "child.pid")
        self.exp["lanes"] = [lane("hang", "rank_a", "hang.py")]
        self.exp["lanes"][0]["probe"]["args"]["pidfile"] = pidfile
        self.exp["deadline_s"] = 4  # the probe must start Python, spawn the child and write its pid first
        self.planned()
        t0 = time.monotonic()
        p = self.call("lanes-cell", self.run_dir, "i1/r1/hang")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertLess(time.monotonic() - t0, 15)
        res = self.result("i1/r1/hang")
        self.assertEqual((res["outcome"], res["exit_code"]), ("timeout", 124))
        self.assertGreaterEqual(res["wall_s"], 4.0)
        with open(pidfile) as f:
            child = int(f.read())
        for _ in range(50):  # the group is killed; the zombie of a reparented child may take a moment to go
            try:
                os.kill(child, 0)
            except ProcessLookupError:
                break
            time.sleep(0.1)
        else:
            self.fail("the probe's child outlived the cell")

    def test_cpu_and_memory_are_recorded(self):
        self.exp["lanes"] = [lane("burn", "rank_a", "burn.py")]
        self.planned()
        self.assertEqual(self.call("lanes-cell", self.run_dir, "i1/r1/burn").returncode, 0)
        res = self.result("i1/r1/burn")
        self.assertEqual(res["outcome"], "ok", res)
        self.assertGreaterEqual(res["cpu_s"], 0.4)
        self.assertGreaterEqual(res["peak_rss_kb"], 70_000)
        self.assertGreaterEqual(res["wall_s"], res["cpu_s"] * 0.5)
        self.assertEqual(res["stderr_tail"], "")

    def test_failing_command_is_recorded_with_its_stderr(self):
        path = os.path.join(self.tmp, "fail.py")
        with open(path, "w") as f:
            f.write("import sys\nsys.stderr.write('boom\\n')\nsys.exit(3)\n")
        self.exp["lanes"] = [{"name": "fail", "probe": {"command": [sys.executable, path]}},
                             {"name": "missing", "probe": {"command": [os.path.join(self.tmp, "nope")]}}]
        self.planned()
        self.assertEqual(self.call("lanes-cell", self.run_dir, "i1/r1/fail").returncode, 0)
        self.assertEqual(self.call("lanes-cell", self.run_dir, "i1/r1/missing").returncode, 0)
        res = self.result("i1/r1/fail")
        self.assertEqual((res["outcome"], res["exit_code"], res["stderr_tail"]), ("exit_3", 3, "boom\n"))
        self.assertEqual(self.result("i1/r1/missing")["outcome"], "exec_error")

    def test_changed_corpus_is_refused(self):
        self.planned()
        with open(os.path.join(self.corpus, "repos", "i2", "a.py"), "a") as f:
            f.write("# changed\n")
        p = self.run_all()
        self.assertEqual(p.returncode, 2)
        self.assertIn("corpus files no longer match PLAN.json", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "cells")))

    def test_changed_item_is_refused(self):
        self.planned()
        edited = json.loads(json.dumps(ITEMS))
        edited[1]["expected"]["touched_files"] = ["y.py"]
        with open(os.path.join(self.corpus, "items.jsonl"), "w") as f:
            f.writelines(json.dumps(i) + "\n" for i in edited)
        p = self.run_all()
        self.assertEqual(p.returncode, 2)
        self.assertIn("corpus items no longer match PLAN.json", p.stderr)
        p = self.call("lanes-cell", self.run_dir, "i2/r1/a")
        self.assertEqual(p.returncode, 2)
        self.assertIn("item i2 no longer matches", p.stderr)

    def test_changed_probe_script_is_refused(self):
        script = os.path.join(self.tmp, "probe.py")
        shutil.copy(os.path.join(FIX, "rank.py"), script)
        self.exp["lanes"] = [{"name": "a", "probe": {"command": [sys.executable, script], "args": {"key": "rank_a"}}}]
        self.planned()
        with open(script, "a") as f:
            f.write("# edited\n")
        p = self.run_all()
        self.assertEqual(p.returncode, 2)
        self.assertIn("commands, their files or settings no longer match", p.stderr)

    def test_corpus_flag_and_split_by_item_id(self):
        elsewhere = os.path.join(self.tmp, "elsewhere")
        shutil.move(self.corpus, elsewhere)
        self.exp["split"] = {"train": ["i1", "i2"], "test": ["i3"]}
        self.assertEqual(self.plan().returncode, 2)  # the experiment's own corpus path is gone
        self.assertEqual(self.plan("--corpus", elsewhere).returncode, 0)
        self.assertEqual(self.run_all().returncode, 0)  # the run dir remembers where the corpus was planned
        self.exp["split"] = {"train": ["i1"], "test": ["i3"]}
        p = self.plan("--corpus", elsewhere)
        self.assertEqual(p.returncode, 2)
        self.assertIn("exactly the corpus items", p.stderr)

    def test_items_subset_of_the_corpus(self):
        self.exp["items"] = ["i3", "i1"]
        self.planned()
        cells = common.read_jsonl(os.path.join(self.run_dir, "plan.jsonl"))
        self.assertEqual({c["task"] for c in cells}, {"i1", "i3"})
        self.exp["items"] = ["i9"]
        p = self.plan()
        self.assertEqual(p.returncode, 2)
        self.assertIn("not in the corpus: i9", p.stderr)

    def test_remote_hosts_are_refused(self):
        self.planned()
        common.write_json(self.hosts, {"far": {"target": "user@somewhere", "root": "/work", "slots": 1}})
        p = self.run_all()
        self.assertEqual(p.returncode, 2)
        self.assertIn("local hosts only", p.stderr)


class Preflight(ProbeCase):
    def test_preflight_checks_commands_and_dry_runs_only_declared_lanes(self):
        marker_a, marker_b = (os.path.join(self.tmp, f"marker-{n}") for n in "ab")
        a, b = lane("a", "rank_a", dry_run_ok=True), lane("b", "rank_b")
        a["probe"]["args"]["marker"], b["probe"]["args"]["marker"] = marker_a, marker_b
        self.exp["lanes"] = [a, b]
        self.planned()
        p = self.call("lanes-preflight", self.run_dir)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("a: dry run on i1: ok", p.stdout)
        self.assertTrue(os.path.isfile(marker_a))
        self.assertFalse(os.path.exists(marker_b))  # b did not declare dry_run_ok
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "cells")))

    def test_preflight_refuses_a_missing_command_and_a_bad_corpus(self):
        self.exp["lanes"] = [{"name": "gone", "probe": {"command": [os.path.join(self.tmp, "no-such-probe")]}}]
        self.planned()
        p = self.call("lanes-preflight", self.run_dir)
        self.assertEqual(p.returncode, 1)
        self.assertIn("gone: REFUSED", p.stdout)
        os.remove(os.path.join(self.corpus, "items.jsonl"))
        p = self.call("lanes-preflight", self.run_dir)
        self.assertEqual(p.returncode, 1)
        self.assertIn("corpus: REFUSED", p.stdout)

    def test_a_failing_dry_run_stops_lanes_run(self):
        path = os.path.join(self.tmp, "fail.py")
        with open(path, "w") as f:
            f.write("import sys\nsys.exit(1)\n")
        self.exp["lanes"] = [{"name": "f", "probe": {"command": [sys.executable, path]}, "dry_run_ok": True}]
        self.planned()
        p = self.call("lanes-run", self.run_dir, "--hosts", self.hosts)
        self.assertEqual(p.returncode, 2)
        self.assertIn("dry run on i1: REFUSED", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "cells")))


class Validation(unittest.TestCase):
    def good(self, **over):
        exp = {"id": "p", "phase": "probe", "corpus": "c", "reps": 1, "deadline_s": 5,
               "lanes": [{"name": "a", "probe": {"command": ["x"]}}],
               "grader": {"kind": "exact_match"}, "decision_rule": {"kind": "descriptive"}}
        exp.update(over)
        return exp

    def fails(self, field, **over):
        with self.assertRaises(experiment.ExperimentError) as cm:
            experiment.validate(self.good(**over))
        self.assertIn(field, str(cm.exception))

    def test_valid_minimal_probe_needs_no_kogen_sha_tasks_or_hosts(self):
        exp = experiment.validate(self.good())
        self.assertEqual(experiment.lane_provider(exp["lanes"][0]), "chatgpt")
        self.assertEqual(exp["hosts"], [])

    def test_fields_are_named(self):
        self.fails("corpus", corpus=3)
        self.fails("lanes[0].probe", lanes=[{"name": "a"}])
        self.fails("lanes[0].probe.command", lanes=[{"name": "a", "probe": {"command": []}}])
        self.fails("lanes[0].probe.command", lanes=[{"name": "a", "probe": {"command": "x"}}])
        self.fails("lanes[0].dry_run_ok", lanes=[{"name": "a", "probe": {"command": ["x"]}, "dry_run_ok": "yes"}])
        self.fails("lanes[0].sha", lanes=[{"name": "a", "probe": {"command": ["x"]}, "sha": "abc"}])
        self.fails("tasks", tasks=["t1"])
        self.fails("intent_form", intent_form="prose")
        self.fails("grader.kind", grader={"kind": "vibes"})
        self.fails("grader.command", grader={"kind": "command"})
        self.fails("decision_rule.kind", decision_rule={"kind": "paired_sign"})
        two = [{"name": n, "probe": {"command": ["x"]}} for n in "ab"]
        self.fails("decision_rule.metric", lanes=two, decision_rule={"kind": "task_sign", "baseline": "a", "candidate": "b"})
        self.fails("decision_rule.candidate", lanes=two, decision_rule={"kind": "task_sign", "baseline": "a", "candidate": "z", "metric": "m"})
        self.fails("split", split={"train": ["i1"], "test": ["i1"]})
        self.fails("decision_rule.kind", decision_rule={"kind": "keep_revert", "baseline": "a", "candidate": "b", "metric": "m"},
                   lanes=[{"name": n, "probe": {"command": ["x"]}} for n in "ab"])

    def test_other_phases_still_need_their_own_fields(self):
        with self.assertRaises(experiment.ExperimentError) as cm:
            experiment.validate({"id": "p", "phase": "shape"})
        self.assertIn("kogen", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
