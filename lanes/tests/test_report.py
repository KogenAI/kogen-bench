import os
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction

from lanes import common, report

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin", "lanes-report")


def totals(cost, wall=10.0, inp=1000, cached=600):
    return {"requests": 2, "models": ["m"], "input_tokens": inp, "cached_input_tokens": cached, "output_tokens": 100,
            "reasoning_tokens": 40, "cost_usd": cost, "wall_s": wall, "cost_reason": None, "missing": []}


def make_run(root, passes, costs=None, rule=None, expect=None, ungraded=(), phase="build", outcomes=None,
             eval_extra=None, unfinished=(), log_extra=None):
    """`passes`: {lane: [bool per (task, rep)]} over tasks t1, t2 with reps 1, 2."""
    cells = [(t, r) for t in ("t1", "t2") for r in (1, 2)]
    lanes = [{"name": n, "sha": "0" * 40, "patch": None, "settings": {}} for n in passes]
    if expect:
        lanes[1]["expect"] = expect
    exp = {"id": "e", "phase": phase, "lanes": lanes, "tasks": ["t1", "t2"], "reps": 2, "deadline_s": 60,
           "hosts": ["local"], "kogen": {"repo": "x"}, "decision_rule": rule or {"kind": "descriptive"}}
    if phase == "build":
        exp["intent_form"] = "gherkin"
    common.write_json(os.path.join(root, "experiment.json"), exp)
    plan = []
    for n, ps in passes.items():
        for i, (t, r) in enumerate(cells):
            cid = f"{t}/r{r}/{n}"
            plan.append({"cell": cid, "task": t, "rep": r, "lane": n, "order": len(plan)})
            d = common.cell_dir(root, cid)
            os.makedirs(os.path.join(d, "run-log"))
            if cid not in unfinished:
                common.write_json(os.path.join(d, "result.json"), {
                    "cell": cid, "lane": n, "outcome": (outcomes or {}).get(cid, "landed"), "totals": totals((costs or {}).get(n, 1.0)),
                    "stages": [{"stage": "build", "requests": 2, "input_tokens": 1000, "cached_input_tokens": 600,
                                "output_tokens": 100, "reasoning_tokens": 40, "cost_usd": 1.0, "wall_s": 10.0}]})
            if cid not in ungraded:
                ev = {"all_passed": ps[i], "pass_trees": [{"all_passed": ps[i]}],
                      "scenarios": 3, "pass_on_reference": 3, "fail_on_start": 3,
                      "wrong_caught": 1, "wrong_total": 2}
                common.write_json(os.path.join(d, "evaluation.json"), {**ev, **(eval_extra or {}).get(cid, {})})
            if cid not in unfinished:
                with open(os.path.join(d, "run-log", "log.jsonl"), "w") as f:
                    f.write('{"event": "request", "role": "builder", "model": "m-' + n + '"}\n'
                            '{"event": "review", "review": 1}\n' + (log_extra or {}).get(cid, ""))
    with open(os.path.join(root, "plan.jsonl"), "w") as f:
        for p in plan:
            f.write(common.json.dumps(p) + "\n")


class Run:
    def __init__(self, test, **kw):
        self.tmp = tempfile.TemporaryDirectory()
        test.addCleanup(self.tmp.cleanup)
        make_run(self.tmp.name, **kw)

    def report(self):
        return report.report(self.tmp.name)


T, F = True, False
BASE = [T, F, F, F]


class Arithmetic(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(report.format_points(Fraction(1, 3)), "0.33")
        self.assertEqual(report.format_points(Fraction(-5, 1000)), "-0.01")
        self.assertEqual(report.format_points(Fraction(-4, 1000)), "0.00")
        self.assertEqual(report.ratio_decimal(Fraction(1, 64)), "0.015625")
        self.assertEqual(report.ratio_decimal(Fraction(1, 3)), "1/3")
        self.assertEqual(report.ratio_decimal(Fraction(3)), "3")
        self.assertEqual(report.ratio(0.05), Fraction(1, 20))
        self.assertEqual(report.binomial_tail(6, 6), Fraction(1, 64))
        self.assertEqual(report.binomial_tail(0, 0), 1)


class Rules(unittest.TestCase):
    def rule(self, passes, rule, **kw):
        return Run(self, passes={"base": BASE, "cand": passes}, rule={"baseline": "base", "candidate": "cand", **rule}, **kw).report()["verdict"]

    def test_paired_sign_keep_and_numbers(self):
        v = self.rule([T, T, T, T], {"kind": "paired_sign", "min_gain_points": 50, "max_p": "0.125"})
        self.assertEqual((v["decision"], v["gain_points"], v["p"], v["candidate_only"], v["blocks"]),
                         ("keep", "75.00", "0.125", 3, 4))
        self.assertIn("paired_sign", v["line"])
        self.assertIn("gain 75.00", v["line"])

    def test_paired_sign_fail_and_reject(self):
        v = self.rule([T, T, T, T], {"kind": "paired_sign", "max_p": "0.05"})
        self.assertEqual(v["decision"], "unresolved")  # p 0.125 > 0.05
        v = self.rule([F, F, F, F], {"kind": "paired_sign", "min_gain_points": 10})
        self.assertEqual((v["decision"], v["gain_points"], v["baseline_only"]), ("reject", "-25.00", 1))

    def test_task_sign(self):
        v = self.rule([T, T, T, T], {"kind": "task_sign", "min_gain_points": 10, "max_p": "0.5"})
        # t1: cand 2 vs base 1 -> candidate; t2: cand 2 vs base 0 -> candidate
        self.assertEqual((v["decision"], v["candidate_favored"], v["p"], v["gain_points"]), ("keep", 2, "0.25", "75.00"))
        v = self.rule([T, F, F, F], {"kind": "task_sign"})
        self.assertEqual((v["decision"], v["ties"], v["tasks"]), ("unresolved", 2, 2))
        v = self.rule([T, T, T, T], {"kind": "task_sign", "max_p": "0.2"})
        self.assertEqual(v["decision"], "unresolved")  # p 0.25 > 0.2

    def test_cost_at_quality(self):
        rule = {"kind": "cost_at_quality", "metric": "cost_usd", "min_saving_pct": 20}
        v = self.rule(BASE, rule, costs={"base": 1.0, "cand": 0.7})
        self.assertEqual((v["decision"], v["saving_pct"], v["loss_points"], v["baseline_median"], v["candidate_median"]),
                         ("keep", "30.00", "0.00", "1", "0.7"))
        v = self.rule(BASE, rule, costs={"base": 1.0, "cand": 0.9})
        self.assertEqual(v["decision"], "unresolved")
        v = self.rule([F, F, F, F], dict(rule, max_loss_points=10), costs={"base": 1.0, "cand": 0.1})
        self.assertEqual((v["decision"], v["quality_holds"]), ("reject", False))

    def test_cost_metric_time(self):
        v = self.rule(BASE, {"kind": "cost_at_quality", "min_saving_pct": 1})
        self.assertEqual((v["metric"], v["decision"]), ("wall_s", "unresolved"))  # equal wall time

    def test_descriptive_and_bad_rule(self):
        self.assertEqual(self.rule(BASE, {"kind": "descriptive"})["decision"], "none")
        self.assertEqual(self.rule(BASE, {"kind": "median-of-vibes"})["decision"], "invalid_rule")
        self.assertEqual(self.rule(BASE, {"kind": "paired_sign", "candidate": "base"})["decision"], "invalid_rule")

    def test_missing_grades_make_the_verdict_incomplete(self):
        v = self.rule([T, T, T, T], {"kind": "paired_sign"}, ungraded=("t2/r2/cand",))
        self.assertEqual((v["decision"], v["ungraded"]), ("incomplete", ["t2/r2"]))


class Witnesses(unittest.TestCase):
    RULE = {"kind": "paired_sign", "baseline": "base", "candidate": "cand"}

    def test_pass(self):
        r = Run(self, passes={"base": BASE, "cand": BASE}, rule=self.RULE,
                expect=[{"event": "review", "count": 1}, {"event": "request", "min": 1}]).report()
        self.assertTrue(r["lanes"][1]["valid"])

    def test_fail_marks_lane_invalid_and_blocks_the_rule(self):
        r = Run(self, passes={"base": BASE, "cand": [T] * 4}, rule=self.RULE,
                expect=[{"event": "review", "count": 0}]).report()
        lane = r["lanes"][1]
        self.assertFalse(lane["valid"])
        self.assertEqual(len(lane["witness_failures"]), 4)
        self.assertIn("seen 1 times", lane["witness_failures"][0])
        self.assertEqual(r["verdict"]["decision"], "invalid")

    def test_where(self):
        log = [{"event": "request", "role": "review"}, {"event": "request", "role": "builder"}]
        self.assertEqual(report.check_witnesses([{"event": "request", "where": {"role": "review"}, "count": 1}], log), [])
        self.assertEqual(len(report.check_witnesses([{"event": "request", "max": 1}], log)), 1)


class Lanes(unittest.TestCase):
    def test_totals_models_and_shares(self):
        r = Run(self, passes={"base": BASE, "cand": [T] * 4}).report()
        base = r["lanes"][0]
        self.assertEqual(base["cells"], {"planned": 4, "finished": 4, "graded": 4})
        self.assertEqual(base["pass_rate"], 0.25)
        self.assertEqual(base["first_green_pass_rate"], 0.25)
        self.assertEqual(base["models"], ["m"])  # from result.json totals.models (usage.py read the log)
        self.assertEqual(base["totals"]["cost_usd"], 4.0)
        self.assertEqual(base["totals"]["input_tokens"], 4000)
        self.assertEqual(base["totals"]["cache_hit_share"], 0.6)
        self.assertEqual(base["stages"][0]["cache_hit_share"], 0.6)
        self.assertEqual(base["stages"][0]["wall_s"], 40.0)
        self.assertEqual(base["outcomes"], {"landed": 4})

    def test_stage_rows_in_fixed_order(self):
        with tempfile.TemporaryDirectory() as root:
            make_run(root, {"base": BASE, "cand": BASE})
            row = lambda name: {"stage": name, "requests": 1, "input_tokens": 1, "cached_input_tokens": 0,
                                "output_tokens": 1, "reasoning_tokens": 0, "cost_usd": 0.0, "wall_s": 1.0}
            # the first cell skips shape and approve and has an unknown stage first; a later cell has all
            for cid, names in (("t1/r1/base", ["probe", "review", "build"]),
                               ("t1/r2/base", ["shape", "approve", "build", "repair", "verify", "extra"])):
                p = os.path.join(common.cell_dir(root, cid), "result.json")
                res = common.read_json(p)
                res["stages"] = [row(n) for n in names]
                common.write_json(p, res)
            stages = [s["stage"] for s in report.report(root)["lanes"][0]["stages"]]
        self.assertEqual(stages, ["shape", "approve", "build", "verify", "review", "repair", "probe", "extra"])

    def test_missing_grades_and_null_cost(self):
        with tempfile.TemporaryDirectory() as root:
            make_run(root, {"base": BASE, "cand": BASE}, ungraded=("t1/r1/base",))
            p = os.path.join(common.cell_dir(root, "t1/r2/base"), "result.json")
            res = common.read_json(p)
            res["totals"]["cost_usd"] = None
            common.write_json(p, res)
            base = report.report(root)["lanes"][0]
        self.assertEqual(base["cells"]["graded"], 3)
        self.assertEqual(base["pass_rate"], 0.0)
        self.assertIsNone(base["totals"]["cost_usd"])

    def test_shape_metrics(self):
        r = Run(self, passes={"base": BASE, "cand": BASE}, phase="shape").report()
        self.assertEqual(r["lanes"][0]["shape"]["wrong_caught"], 4)
        self.assertEqual(r["lanes"][0]["shape"]["scenarios"], 12)


class OutcomeClasses(unittest.TestCase):
    RULE = {"kind": "paired_sign", "baseline": "base", "candidate": "cand"}

    def run_with(self, **kw):
        return Run(self, passes={"base": BASE, "cand": [T] * 4}, rule=self.RULE, **kw).report()

    def test_blocked_cell_without_grade_is_a_counted_failure(self):
        cid = "t2/r2/cand"
        r = self.run_with(outcomes={cid: "build_blocked"}, ungraded=(cid,))
        self.assertEqual(r["verdict"]["decision"], "keep")  # decided, not incomplete
        self.assertEqual(r["verdict"]["candidate_only"], 2)  # the blocked cell is not correct
        cand = r["lanes"][1]
        self.assertEqual(cand["classes"], {"correct": 3, "workflow_failure": 1})
        self.assertEqual(cand["pass_rate"], 0.75)  # denominator counts it

    def test_provider_failure_is_excluded_even_when_graded_red(self):
        cid = "t1/r1/cand"
        r = self.run_with(outcomes={cid: "provider_failure"}, eval_extra={cid: {"all_passed": False}})
        self.assertEqual(r["lanes"][1]["classes"], {"correct": 3, "infrastructure": 1})
        self.assertEqual(r["lanes"][1]["pass_rate"], 1.0)  # 3 of 3 counted
        self.assertEqual((r["verdict"]["decision"], r["verdict"]["ungraded"]), ("incomplete", ["t1/r1"]))

    def test_provider_failure_flag_on_last_outcome_event(self):
        cid = "t1/r1/cand"
        r = self.run_with(outcomes={cid: "no_outcome"},
                          log_extra={cid: '{"event": "outcome", "outcome": "failed", "provider_failure": true}\n'})
        self.assertEqual(r["lanes"][1]["classes"]["infrastructure"], 1)

    def test_landed_without_grade_and_unfinished_and_interrupted(self):
        r = self.run_with(ungraded=("t1/r1/cand",), unfinished=("t1/r2/cand",), outcomes={"t2/r1/cand": "interrupted:sigterm"})
        self.assertEqual(r["lanes"][1]["classes"], {"correct": 1, "incomplete": 2, "infrastructure": 1})
        self.assertEqual(r["verdict"]["decision"], "incomplete")

    def test_classify(self):
        res = lambda o: {"outcome": o}
        self.assertEqual(report.classify(res("timeout"), [], None, "build"), "workflow_failure")
        self.assertEqual(report.classify(res("landed"), [], {"all_passed": False}, "build"), "incorrect")
        self.assertEqual(report.classify(res("landed"), [], {"state": "infrastructure"}, "build"), "infrastructure")
        self.assertEqual(report.classify(res("host_lost"), [], None, "build"), "infrastructure")
        self.assertEqual(report.classify(None, [], None, "build"), "incomplete")

    def test_each_ending(self):
        """One case per ending L3 and Kogen write (integrator ruling, round 2)."""
        want = {"signal": "incomplete", "interrupted:sigint": "incomplete", "controller_lost": "incomplete",
                "environment": "infrastructure", "usage": "infrastructure", "host_lost": "infrastructure",
                "provider_failure": "infrastructure", "refused": "workflow_failure",
                "internal": "workflow_failure", "timeout": "workflow_failure",
                "questions_pending": "workflow_failure", "build_blocked": "workflow_failure",
                "no_outcome": "workflow_failure"}
        for ending, cls in want.items():
            with self.subTest(ending=ending):
                self.assertEqual(report.classify({"outcome": ending}, [], None, "build"), cls)

    def test_evaluation_infrastructure_reason_wins_over_all_passed(self):
        ev = {"all_passed": False, "infrastructure": "final-tree.tar missing"}  # as L4 writes it
        self.assertEqual(report.classify({"outcome": "landed"}, [], ev, "build"), "infrastructure")
        self.assertEqual(report.classify({"outcome": "landed"}, [], dict(ev, all_passed=True), "build"), "infrastructure")
        self.assertEqual(report.classify({"outcome": "landed"}, [], dict(ev, infrastructure=None), "build"), "incorrect")
        cid = "t1/r1/cand"
        r = self.run_with(eval_extra={cid: ev})
        self.assertEqual(r["lanes"][1]["classes"], {"correct": 3, "infrastructure": 1})
        self.assertEqual((r["verdict"]["decision"], r["verdict"]["ungraded"]), ("incomplete", ["t1/r1"]))

    def test_result_without_outcome_is_incomplete(self):
        self.assertEqual(report.classify({"cell": "t1/r1/x"}, [], {"all_passed": False}, "build"), "incomplete")
        self.assertEqual(report.classify({"outcome": None}, [], None, "build"), "incomplete")

    def test_signal_and_environment_do_not_count_against_a_lane(self):
        r = self.run_with(outcomes={"t1/r1/cand": "signal", "t1/r2/cand": "environment"})
        cand = r["lanes"][1]
        self.assertEqual(cand["classes"], {"correct": 2, "incomplete": 1, "infrastructure": 1})
        self.assertEqual(cand["pass_rate"], 1.0)
        self.assertEqual((r["verdict"]["decision"], r["verdict"]["ungraded"]), ("incomplete", ["t1/r1", "t1/r2"]))


class Robustness(unittest.TestCase):
    def cli(self, mutate=None, plan=True, **kw):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        make_run(tmp.name, {"base": BASE, "cand": BASE}, **kw)
        if mutate:
            p = os.path.join(tmp.name, "experiment.json")
            exp = common.read_json(p)
            mutate(exp)
            common.write_json(p, exp)
        if not plan:
            os.remove(os.path.join(tmp.name, "plan.jsonl"))
        return subprocess.run([sys.executable, BIN, tmp.name], capture_output=True, text=True)

    def test_malformed_experiment_exits_2_on_stderr(self):
        for mutate in (lambda e: e.update(decision_rule="paired_sign"), lambda e: e.update(lanes={}),
                       lambda e: e.pop("phase")):
            p = self.cli(mutate)
            self.assertEqual(p.returncode, 2)
            self.assertEqual(p.stdout, "")
            self.assertIn("experiment error", p.stderr)

    def test_non_numeric_threshold_exits_2(self):
        p = self.cli(lambda e: e.update(decision_rule={"kind": "paired_sign", "baseline": "base",
                                                         "candidate": "cand", "max_p": "soon"}))
        self.assertEqual(p.returncode, 2)
        self.assertIn("decision_rule.max_p", p.stderr)

    def test_missing_plan_exits_2(self):
        p = self.cli(plan=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("plan.jsonl", p.stderr)

    def test_non_numeric_metric_is_an_invalid_rule(self):
        rule = {"kind": "cost_at_quality", "baseline": "base", "candidate": "cand", "metric": "outcome"}
        v = Run(self, passes={"base": BASE, "cand": BASE}, rule=rule).report()["verdict"]
        self.assertEqual(v["decision"], "invalid_rule")
        rule["metric"] = "no_such_field"
        v = Run(self, passes={"base": BASE, "cand": BASE}, rule=rule).report()["verdict"]
        self.assertEqual(v["decision"], "invalid_rule")

    def test_cost_metric_with_a_null_cost_is_incomplete(self):
        rule = {"kind": "cost_at_quality", "baseline": "base", "candidate": "cand", "metric": "cost_usd"}
        tmp = Run(self, passes={"base": BASE, "cand": BASE}, rule=rule)
        p = os.path.join(common.cell_dir(tmp.tmp.name, "t1/r1/cand"), "result.json")
        res = common.read_json(p)
        res["totals"]["cost_usd"] = None
        common.write_json(p, res)
        self.assertEqual(tmp.report()["verdict"]["decision"], "incomplete")

    def test_shape_metrics_without_all_passed(self):
        matrix = {"scenarios": 3, "pass_on_reference": 3, "fail_on_start": 3, "wrong_caught": 2, "wrong_total": 2}
        extra = {f"{t}/r{r}/{n}": matrix for t in ("t1", "t2") for r in (1, 2) for n in ("base", "cand")}
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        make_run(tmp.name, {"base": BASE, "cand": BASE}, phase="shape")
        for cid in extra:
            common.write_json(os.path.join(common.cell_dir(tmp.name, cid), "evaluation.json"), matrix)
        lane = report.report(tmp.name)["lanes"][0]
        self.assertEqual((lane["shape"]["scenarios"], lane["shape"]["wrong_caught"]), (12, 8))
        self.assertEqual(lane["pass_rate"], 1.0)  # every shaped Intent holds the matrix

    def test_witness_skips_unfinished_cells(self):
        r = Run(self, passes={"base": BASE, "cand": BASE}, unfinished=("t1/r1/cand",),
                expect=[{"event": "review", "min": 1}]).report()
        self.assertTrue(r["lanes"][1]["valid"])

    def test_first_green_pass_rate_with_a_later_green_tree(self):
        extra = {"t1/r1/base": {"all_passed": False, "pass_trees": [{"all_passed": False}, {"all_passed": True}]},
                 "t1/r2/base": {"all_passed": False, "pass_trees": [{"all_passed": False}]}}
        base = Run(self, passes={"base": BASE, "cand": BASE}, eval_extra=extra).report()["lanes"][0]
        self.assertEqual(base["pass_rate"], 0.0)
        self.assertEqual(base["first_green_pass_rate"], 0.25)


class CommandLine(unittest.TestCase):
    def test_writes_report_files(self):
        with tempfile.TemporaryDirectory() as root:
            make_run(root, {"base": BASE, "cand": [T] * 4}, rule={"kind": "paired_sign", "baseline": "base", "candidate": "cand"})
            p = subprocess.run([sys.executable, BIN, root], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("paired_sign", p.stdout)
            with open(os.path.join(root, "report.md")) as f:
                md = f.read()
            self.assertIn("**Verdict:** Rule paired_sign", md)
            self.assertIn("| cand |", md)
            self.assertEqual(common.read_json(os.path.join(root, "report.json"))["lanes"][1]["name"], "cand")

    def test_usage_error(self):
        self.assertEqual(subprocess.run([sys.executable, BIN], capture_output=True).returncode, 2)
        self.assertEqual(subprocess.run([sys.executable, BIN, "/nonexistent-run"], capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
