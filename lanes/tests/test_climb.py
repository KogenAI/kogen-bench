import copy
import json
import os
import tempfile
import unittest

from lanes import common, experiment, report

SHA = "0123456789abcdef0123456789abcdef01234567"


def climb():
    return {
        "id": "climb-r1", "kind": "climb", "phase": "build", "intent_form": "gherkin", "kogen": {"repo": "x"},
        "lanes": [{"name": "baseline", "sha": SHA, "patch": None, "settings": {"models": {"build": "openai/m high"}}},
                  {"name": "candidate", "sha": SHA, "patch": "p.patch", "settings": {"models": {"build": "openai/m high"}}}],
        "tasks": ["a1", "a2", "b1"], "reps": 1, "deadline_s": 60, "hosts": ["local"],
        "split": {"train": ["a1", "a2"], "test": ["b1"]}, "min_effect": 0.1, "noise_ref": "noise/r0.json",
        "round": 1, "parent": None, "decision_rule": {"kind": "keep_revert"},
    }


class Validate(unittest.TestCase):
    def bad(self, field, mutate):
        exp = climb()
        mutate(exp)
        with self.assertRaises(experiment.ExperimentError) as cm:
            experiment.validate(exp)
        self.assertIn(field, str(cm.exception))

    def test_good(self):
        experiment.validate(climb())

    def test_settings_change_instead_of_patch(self):
        exp = climb()
        exp["lanes"][1].update(patch=None, settings={"models": {"build": "openai/m low"}})
        experiment.validate(exp)

    def test_bad_climbs(self):
        def two_patches(e):
            e["lanes"][1]["settings"] = {"models": {"build": "openai/m low"}}
        def two_settings(e):
            e["lanes"][1].update(patch=None, settings={"models": {"build": "openai/m low", "review": "openai/m low"}})
        def no_change(e):
            e["lanes"][1]["patch"] = None
        cases = [
            ("lanes", lambda e: e["lanes"].append(copy.deepcopy(e["lanes"][1]))),
            ("lanes", lambda e: e["lanes"][1].update(name="other")),
            ("lanes", two_patches),
            ("lanes", two_settings),
            ("lanes", no_change),
            ("lanes", lambda e: e["lanes"][1].update(sha="f" * 40)),
            ("split", lambda e: e.pop("split")),
            ("split.train", lambda e: e["split"].update(train=[])),
            ("split.test", lambda e: e["split"].update(test=[])),
            ("disjoint", lambda e: e["split"].update(test=["b1", "a1"])),
            ("exactly the experiment's tasks", lambda e: e["split"].update(test=["b2"])),
            ("exactly the experiment's tasks", lambda e: e["tasks"].append("c1")),
            ("min_effect", lambda e: e.pop("min_effect")),
            ("min_effect", lambda e: e.update(min_effect=0)),
            ("min_effect", lambda e: e.update(min_effect=1.5)),
            ("min_effect", lambda e: e.update(min_effect=True)),
            ("noise_ref", lambda e: e.update(noise_ref="")),
            ("noise_ref", lambda e: e.pop("noise_ref")),
            ("round", lambda e: e.update(round=0)),
            ("parent", lambda e: e.pop("parent")),
            ("parent", lambda e: e.update(round=2)),
            ("parent", lambda e: e.update(parent="climb-r0")),
            ("decision_rule.kind", lambda e: e.update(decision_rule={"kind": "paired_sign"})),
            ("kind", lambda e: e.update(kind="sweep")),
        ]
        for field, mutate in cases:
            with self.subTest(field=field):
                self.bad(field, mutate)

    def test_later_round(self):
        exp = climb()
        exp.update(round=2, parent="climb-r0")
        experiment.validate(exp)

    def test_non_climb_unchanged(self):
        exp = climb()
        for k in ("kind", "split", "min_effect", "noise_ref", "round", "parent"):
            exp.pop(k)
        exp["decision_rule"] = {"kind": "paired_sign"}
        experiment.validate(exp)
        exp["decision_rule"] = {"kind": "keep_revert"}
        with self.assertRaises(experiment.ExperimentError):
            experiment.validate(exp)


class Intervals(unittest.TestCase):
    def close(self, got, want, tol=5e-4):
        self.assertEqual(len(got), 2)
        for g, w in zip(got, want):
            self.assertAlmostEqual(g, w, delta=tol)

    def test_wilson_references(self):
        self.close(report.wilson(5, 10), (0.2366, 0.7634))
        self.close(report.wilson(0, 10), (0.0, 0.2775))
        self.close(report.wilson(10, 10), (0.7225, 1.0))
        self.close(report.wilson(1, 4), (0.0455, 0.6994))
        self.assertIsNone(report.wilson(0, 0))

    def test_wilson_small_samples_are_wide(self):
        lo, hi = report.wilson(1, 1)
        self.assertLess(lo, 0.25)
        self.assertEqual(hi, 1.0)

    def test_clopper_pearson_references(self):
        self.close(report.clopper_pearson(5, 10), (0.1871, 0.8129))
        self.close(report.clopper_pearson(0, 10), (0.0, 0.3085))
        self.close(report.clopper_pearson(10, 10), (0.6915, 1.0))
        self.close(report.clopper_pearson(1, 4, 0.1), (0.0127, 0.7514))

    def test_hoeffding(self):
        self.close(report.hoeffding(0, 30), (-0.4959, 0.4959))
        self.close(report.hoeffding(0.8, 5), (-0.4145, 1.0))
        self.assertIsNone(report.hoeffding(0, 0))

    def test_paired_difference(self):
        # 3 candidate-only of 4 pairs: far too few to exclude zero
        lo, hi = report.paired_difference_ci(3, 0, 4)
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0.9)
        # 20 of 20 candidate-only wins: excludes zero; no discordant pair: contains zero
        self.assertGreater(report.paired_difference_ci(20, 0, 20)[0], 0.5)
        lo, hi = report.paired_difference_ci(0, 0, 20)
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0)
        self.assertIsNone(report.paired_difference_ci(0, 0, 0))
        # symmetric
        a, b = report.paired_difference_ci(5, 1, 30), report.paired_difference_ci(1, 5, 30)
        self.assertAlmostEqual(a[0], -b[1], places=9)


def run_dir(test, base, cand, plumbing=None, endings=None, evals=None, exp_mut=None):
    """`base`/`cand`: {task: bool}; one rep. `endings`: {cell: outcome}; `plumbing`: {cell: log line}."""
    tmp = tempfile.TemporaryDirectory()
    test.addCleanup(tmp.cleanup)
    exp = climb()
    exp["tasks"] = list(base)
    exp["split"] = {"train": [t for t in base if t.startswith("a")], "test": [t for t in base if t.startswith("b")]}
    (exp_mut or (lambda e: None))(exp)
    common.write_json(os.path.join(tmp.name, "experiment.json"), exp)
    plan = []
    for lane, passes in (("baseline", base), ("candidate", cand)):
        for task, ok in passes.items():
            cid = f"{task}/r1/{lane}"
            plan.append({"cell": cid, "task": task, "rep": 1, "lane": lane, "order": len(plan)})
            d = common.cell_dir(tmp.name, cid)
            os.makedirs(os.path.join(d, "run-log"))
            ending = (endings or {}).get(cid, "landed")
            if ending is not None:
                common.write_json(os.path.join(d, "result.json"), {"cell": cid, "outcome": ending, "totals": {}, "stages": []})
            if (evals or {}).get(cid, True):
                common.write_json(os.path.join(d, "evaluation.json"), {"all_passed": ok})
            with open(os.path.join(d, "run-log", "log.jsonl"), "w") as f:
                f.write((plumbing or {}).get(cid, ""))
    with open(os.path.join(tmp.name, "plan.jsonl"), "w") as f:
        for p in plan:
            f.write(json.dumps(p) + "\n")
    return tmp.name


def run_dir_reps(test, base, cand, reps, exp_mut=None, endings=None, extra_reps=None):
    """Like run_dir with `reps` reps; `base`/`cand`: {task: [bool per rep]}."""
    tmp = tempfile.TemporaryDirectory()
    test.addCleanup(tmp.cleanup)
    exp = climb()
    exp["reps"] = reps
    exp["tasks"] = list(base)
    exp["split"] = {"train": [t for t in base if t.startswith("a")], "test": [t for t in base if t.startswith("b")]}
    (exp_mut or (lambda e: None))(exp)
    common.write_json(os.path.join(tmp.name, "experiment.json"), exp)
    plan = []
    for lane, passes in (("baseline", base), ("candidate", cand)):
        for task, oks in passes.items():
            for r, ok in enumerate(oks, 1):
                cid = f"{task}/r{r}/{lane}"
                plan.append({"cell": cid, "task": task, "rep": r, "lane": lane, "order": len(plan)})
                d = common.cell_dir(tmp.name, cid)
                os.makedirs(os.path.join(d, "run-log"))
                common.write_json(os.path.join(d, "result.json"), {
                    "cell": cid, "outcome": (endings or {}).get(cid, "landed"), "totals": {}, "stages": []})
                common.write_json(os.path.join(d, "evaluation.json"), {"all_passed": ok})
                open(os.path.join(d, "run-log", "log.jsonl"), "w").close()
    with open(os.path.join(tmp.name, "plan.jsonl"), "w") as f:
        for p in plan:
            f.write(json.dumps(p) + "\n")
    return tmp.name


def tasks(prefix, n, wins):
    """n tasks named prefix1..; the first `wins` pass."""
    return {f"{prefix}{i + 1}": i < wins for i in range(n)}


def many(train_base, train_cand, test_base, test_cand, n=30):
    base = {**tasks("a", n, train_base), **tasks("b", n, test_base)}
    cand = {**tasks("a", n, train_cand), **tasks("b", n, test_cand)}
    return base, cand


class KeepRevert(unittest.TestCase):
    def verdict(self, *counts, **kw):
        base, cand = many(*counts)
        return report.report(run_dir(self, base, cand, **kw))["verdict"]

    def test_keep(self):
        v = self.verdict(5, 25, 5, 25)
        self.assertEqual((v["decision"], v["case"]), ("keep", "improved_both"))
        self.assertIn("KEEP", v["line"])
        self.assertIn("[improved_both]", v["line"])
        self.assertIn("train +0.67", v["line"])
        self.assertIn("test +0.67", v["line"])

    def test_overfit_train_up_test_flat(self):
        v = self.verdict(5, 25, 15, 15)
        self.assertEqual((v["decision"], v["case"]), ("revert", "overfit"))
        self.assertIn("REVERT", v["line"])

    def test_overfit_when_test_gain_is_below_min_effect(self):
        v = self.verdict(5, 25, 15, 17)  # +0.07: at most min_effect (0.1) and its interval contains zero
        self.assertEqual(v["case"], "overfit")

    def test_larger_test_gain_with_a_wide_interval_is_within_noise_not_overfit(self):
        # train +0.67 significant; test 2 of 5 tasks better (+0.40 > min_effect) but the interval spans zero
        base, cand = {**tasks("a", 30, 5), **tasks("b", 5, 0)}, {**tasks("a", 30, 25), **tasks("b", 5, 2)}
        v = report.report(run_dir(self, base, cand))["verdict"]
        self.assertEqual((v["decision"], v["case"]), ("within_noise", "within_noise"))

    def test_test_difference_exactly_min_effect_is_flat(self):
        # 1 of 10 test tasks better = +0.10 = min_effect: not above it, so flat
        base, cand = {**tasks("a", 30, 5), **tasks("b", 10, 0)}, {**tasks("a", 30, 25), **tasks("b", 10, 1)}
        self.assertEqual(report.report(run_dir(self, base, cand))["verdict"]["case"], "overfit")

    def test_any_drop_reverts(self):
        v = self.verdict(15, 25, 15, 14)
        self.assertEqual((v["decision"], v["case"]), ("revert", "drop"))
        v = self.verdict(15, 14, 15, 15)
        self.assertEqual((v["decision"], v["case"]), ("revert", "drop"))

    def test_within_noise(self):
        v = self.verdict(15, 16, 15, 15)
        self.assertEqual((v["decision"], v["case"]), ("within_noise", "within_noise"))
        self.assertIn("within noise; don't merge", v["line"])
        self.assertEqual(self.verdict(15, 15, 15, 15)["case"], "within_noise")

    def test_gain_must_beat_min_effect_and_the_interval(self):
        # +0.2 on both splits of 5 tasks: above min_effect, but the interval spans zero
        base, cand = many(0, 1, 0, 1, n=5)
        v = report.report(run_dir(self, base, cand))["verdict"]
        self.assertEqual(v["case"], "within_noise")
        # significant but below a high min_effect
        base, cand = many(5, 25, 5, 25)
        v = report.report(run_dir(self, base, cand, exp_mut=lambda e: e.update(min_effect=0.9)))["verdict"]
        self.assertEqual(v["case"], "within_noise")

    def test_numbers_and_separate_splits(self):
        base, cand = many(5, 25, 15, 15)
        rep = report.report(run_dir(self, base, cand))
        train, test = rep["climb"]["splits"]["train"], rep["climb"]["splits"]["test"]
        self.assertEqual((train["tasks"], train["candidate_better"], train["baseline_better"]), (30, 20, 0))
        self.assertEqual((train["unit"], train["pairs"], train["tied"]), ("task", 30, 10))
        self.assertEqual(train["difference"], 0.6667)
        self.assertEqual(test["difference"], 0.0)
        self.assertEqual(train["candidate"]["rate"], 0.8333)
        self.assertEqual(len(train["candidate"]["ci"]), 2)
        json.dumps(rep)

    def test_no_pairs_is_incomplete(self):
        base, cand = many(5, 25, 5, 25, n=3)
        endings = {f"b{i}/r1/candidate": "host_lost" for i in (1, 2, 3)}
        v = report.report(run_dir(self, base, cand, endings=endings))["verdict"]
        self.assertEqual(v["decision"], "incomplete")


class TaskUnit(unittest.TestCase):
    def test_reps_of_a_few_tasks_do_not_exclude_zero(self):
        # test split: 5 tasks x 6 reps; the candidate fixes 4 tasks in every rep (24 of 30 pairs).
        # Counted per pair that excludes zero; per task it is 4 of 5 and must not.
        reps = 6
        train_b = {f"a{i}": [False] * reps for i in range(1, 31)}
        train_c = {f"a{i}": [True] * reps for i in range(1, 31)}
        test_b = {f"b{i}": [False] * reps for i in range(1, 6)}
        test_c = {f"b{i}": [i <= 4] * reps for i in range(1, 6)}
        rep = report.report(run_dir_reps(self, {**train_b, **test_b}, {**train_c, **test_c}, reps))
        test = rep["climb"]["splits"]["test"]
        self.assertEqual((test["tasks"], test["pairs"], test["candidate_better"], test["baseline_better"]), (5, 30, 4, 0))
        self.assertEqual(test["pair_difference"], 0.8)
        self.assertLess(test["difference_ci"][0], 0)  # [-0.35, 1.0]
        self.assertGreater(report.paired_difference_ci(24, 0, 30)[0], 0)  # the per-pair reading the review probed
        self.assertEqual(rep["verdict"]["decision"], "within_noise")
        self.assertIn("5 tasks, 30 pairs", rep["verdict"]["line"])

    def test_task_difference_is_the_mean_over_reps(self):
        # a1: candidate wins 1 of 2 reps (mean +0.5, candidate-better); a2: -1 and +1 (mean 0, tied)
        base = {"a1": [False, False], "a2": [True, False], "b1": [False, False]}
        cand = {"a1": [True, False], "a2": [False, True], "b1": [False, False]}
        train = report.report(run_dir_reps(self, base, cand, 2))["climb"]["splits"]["train"]
        self.assertEqual((train["tasks"], train["candidate_better"], train["baseline_better"], train["tied"]), (2, 1, 0, 1))
        self.assertEqual(train["difference"], 0.25)  # the pass-rate difference: (0.5 + 0) / 2

    def test_one_rep_better_on_every_task_is_a_small_gain(self):
        # 30 + 30 tasks, 6 reps; the baseline passes 3 of 6 reps everywhere, the candidate 4 of 6:
        # every task is candidate-better, but the pass-rate gain is +1/6, below min_effect 0.25
        reps = 6
        base = {f"{s}{i}": [True] * 3 + [False] * 3 for s in "ab" for i in range(1, 31)}
        cand = {f"{s}{i}": [True] * 4 + [False] * 2 for s in "ab" for i in range(1, 31)}
        rep = report.report(run_dir_reps(self, base, cand, reps, exp_mut=lambda e: e.update(min_effect=0.25)))
        train = rep["climb"]["splits"]["train"]
        self.assertEqual((train["candidate_better"], train["difference"], train["difference_exact"]), (30, 0.1667, "1/6"))
        v = rep["verdict"]
        self.assertNotEqual(v["decision"], "keep")
        self.assertEqual(v["case"], "within_noise")
        self.assertIn("train +0.17 [", v["line"])
        self.assertIn("vs min_effect 0.25", v["line"])

    def test_drop_uses_the_pass_rate_difference(self):
        # train: a1 worse by one rep of 2 (-0.5), a2 better on both reps (+1): +0.25, no drop
        base = {"a1": [True, True], "a2": [False, False], "b1": [False, False]}
        cand = {"a1": [True, False], "a2": [True, True], "b1": [False, False]}
        rep = report.report(run_dir_reps(self, base, cand, 2))
        self.assertEqual(rep["climb"]["splits"]["train"]["baseline_better"], 1)
        self.assertEqual(rep["climb"]["splits"]["train"]["difference"], 0.25)
        self.assertEqual(rep["verdict"]["case"], "within_noise")

    def test_plumbing_rep_drops_only_that_rep(self):
        base = {"a1": [False, False], "b1": [False, False]}
        cand = {"a1": [True, True], "b1": [False, False]}
        train = report.report(run_dir_reps(self, base, cand, 2, endings={"a1/r2/candidate": "timeout"}))["climb"]["splits"]["train"]
        self.assertEqual((train["tasks"], train["pairs"]), (1, 1))

    def test_unit_stated_in_the_report(self):
        base, cand = many(5, 25, 5, 25, n=3)
        d = run_dir(self, base, cand)
        report.write(d)
        with open(os.path.join(d, "report.md")) as f:
            md = f.read()
        self.assertIn("The unit of the difference is the task", md)


class Plumbing(unittest.TestCase):
    def test_counted_separately_and_excluded(self):
        base, cand = many(5, 25, 5, 25, n=30)
        endings = {"a1/r1/candidate": "timeout", "a2/r1/baseline": "provider_failure_rate_limit",
                   "a3/r1/candidate": "context_exhausted", "a4/r1/baseline": "host_lost",
                   "a5/r1/candidate": None, "a6/r1/candidate": "build_blocked", "b1/r1/candidate": "timeout"}
        log = {"a7/r1/baseline": '{"event": "outcome", "outcome": "no_outcome", "provider_failure": true}\n'}
        endings["a7/r1/baseline"] = "no_outcome"
        endings["a8/r1/baseline"] = "no_outcome"
        endings["a8/r1/candidate"] = "truncated_output"
        rep = report.report(run_dir(self, base, cand, endings=endings, plumbing=log))
        c = rep["climb"]
        cats = {r["cell"]: r["category"] for r in c["plumbing"]}
        self.assertEqual(cats, {"a1/r1/candidate": "timeout", "a2/r1/baseline": "provider_error",
                                "a3/r1/candidate": "truncation", "a4/r1/baseline": "harness",
                                "a5/r1/candidate": "harness", "a7/r1/baseline": "provider_error",
                                "a8/r1/candidate": "truncation", "b1/r1/candidate": "timeout"})
        self.assertEqual(c["plumbing_counts"]["candidate"],
                         {"timeout": 2, "provider_error": 0, "truncation": 2, "harness": 1, "cost_cap": 0, "memory_cap": 0})
        train = c["splits"]["train"]
        self.assertEqual(train["candidate"]["n"], 30 - 4)  # a1, a3, a5, a8 excluded; a6 build_blocked is a task failure
        self.assertEqual(train["baseline"]["n"], 30 - 3)
        self.assertEqual((train["pairs"], train["tasks"]), (30 - 7, 30 - 7))
        # a8/baseline ended no_outcome: a counted task failure
        self.assertIn("a8/r1/baseline", [f["cell"] for f in c["train_failures"]])
        self.assertIn("a6/r1/candidate", [f["cell"] for f in c["train_failures"]])
        # the lane section shows train cells only (b1 is a test cell)
        self.assertEqual(rep["lanes"][1]["plumbing"], {"harness": 1, "timeout": 1, "truncation": 2})

    def test_truncation_endings_are_exact(self):
        base, cand = many(5, 25, 5, 25, n=3)
        endings = {"a1/r1/candidate": "context_exhausted", "a2/r1/candidate": "truncated",
                   "a3/r1/candidate": "context_window_notes", "b1/r1/candidate": "length_check"}
        log = {"a1/r1/baseline": '{"event": "outcome", "outcome": "no_outcome", "truncated": true}\n'}
        rep = report.report(run_dir(self, base, cand, endings=endings, plumbing=log))
        cats = {r["cell"]: r["category"] for r in rep["climb"]["plumbing"]}
        self.assertEqual(cats, {"a1/r1/candidate": "truncation", "a2/r1/candidate": "truncation"})

    def test_missing_evaluation_is_harness(self):
        base, cand = many(5, 25, 5, 25, n=3)
        rep = report.report(run_dir(self, base, cand, evals={"a1/r1/candidate": False}))
        self.assertEqual([r["category"] for r in rep["climb"]["plumbing"]], ["harness"])

    def test_rendered_table(self):
        base, cand = many(5, 25, 5, 25, n=3)
        d = run_dir(self, base, cand, endings={"a1/r1/candidate": "timeout"})
        report.write(d)
        with open(os.path.join(d, "report.md")) as f:
            md = f.read()
        self.assertIn("Plumbing failures", md)
        self.assertIn("| a1/r1/candidate | candidate | train | timeout | timeout |", md)
        self.assertTrue(os.path.isfile(os.path.join(d, "report.json")))


class Hygiene(unittest.TestCase):
    def test_no_test_failure_details(self):
        base, cand = many(1, 3, 2, 2, n=4)
        endings = {"b1/r1/candidate": "build_blocked", "b2/r1/candidate": "timeout"}
        d = run_dir(self, base, cand, endings=endings)
        rep = report.write(d)
        listed = [f["cell"] for f in rep["climb"]["train_failures"]]
        self.assertTrue(listed)
        self.assertTrue(all(c.startswith("a") for c in listed))
        self.assertEqual([r["outcome"] for r in rep["climb"]["plumbing"] if r["split"] == "test"], [None])
        with open(os.path.join(d, "report.md")) as f:
            md = f.read()
        self.assertNotIn("build_blocked", md.split("## Climb")[1].split("### baseline")[0])

    def test_lanes_table_excludes_plumbing_like_the_climb_table(self):
        base, cand = many(0, 2, 0, 3, n=3)
        rep = report.report(run_dir(self, base, cand, endings={"a1/r1/candidate": "timeout"}))
        cand_lane = rep["lanes"][1]
        self.assertEqual(cand_lane["pass_rate"], round(4 / 5, 4))  # 6 cells, one plumbing: 4 of 5 correct
        c = rep["climb"]["splits"]
        self.assertEqual(c["train"]["candidate"]["n"] + c["test"]["candidate"]["n"], 5)
        d = run_dir(self, base, cand, endings={"a1/r1/candidate": "timeout"})
        report.write(d)
        with open(os.path.join(d, "report.md")) as f:
            self.assertIn("pass rate (plumbing excluded)", f.read())

    def test_no_test_details_anywhere_in_the_report(self):
        base, cand = many(1, 3, 2, 2, n=4)
        endings = {"b1/r1/candidate": "test_only_ending", "b2/r1/candidate": "timeout",
                   "b3/r1/baseline": "test_only_ending"}
        d = run_dir(self, base, cand, endings=endings,
                    exp_mut=lambda e: e["lanes"][1].update(expect=[{"event": "review", "min": 1}]))
        report.write(d)
        for name in ("report.md", "report.json"):
            with open(os.path.join(d, name)) as f:
                text = f.read()
            self.assertNotIn("test_only_ending", text, name)
            self.assertNotIn("b1/r1", text, name)  # no test cell is named, not even for witness failures
        rep = report.report(d)
        self.assertGreater(rep["lanes"][1]["witness_failures_test"], 0)
        self.assertFalse(rep["lanes"][1]["valid"])
        self.assertEqual(rep["verdict"]["decision"], "invalid")

    def test_rates_in_lane_table_carry_intervals(self):
        base, cand = many(5, 25, 5, 25, n=3)
        rep = report.report(run_dir(self, base, cand))
        self.assertEqual(len(rep["lanes"][0]["pass_rate_ci"]), 2)

    def test_non_climb_keep_revert_rule_is_invalid(self):
        v = report.apply_rule({"kind": "keep_revert"}, [], [])
        self.assertEqual(v["decision"], "invalid_rule")


if __name__ == "__main__":
    unittest.main()
