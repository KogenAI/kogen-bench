import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import common, plan_hashes

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin")
SHA = "0123456789abcdef0123456789abcdef01234567"
SETTINGS = {"models": {"build": "p/m high"}}
TASKS = ["t1", "t2", "t3", "t4"]
MANY = [f"t{i}" for i in range(30)]


def experiment(run_id, **fields):
    exp = {"id": run_id, "phase": "build", "intent_form": "gherkin", "kogen": {"repo": "x"},
           "lanes": [{"name": "baseline", "sha": SHA, "patch": None, "settings": SETTINGS}],
           "tasks": TASKS, "reps": 2, "deadline_s": 60, "hosts": ["local"], "decision_rule": {"kind": "descriptive"}}
    exp.update(fields)
    return exp


def make_run(root, run_id, passes, cost=1.0, wall=10.0, exp=None, artifact="aa", plumbing=()):
    """`passes`: {task: [bool per rep]}; cost and wall are the per-cell values (or a {task: value} dict)."""
    exp = exp or experiment(run_id)
    d = os.path.join(root, run_id)
    common.write_json(os.path.join(d, "experiment.json"), exp)
    common.write_json(os.path.join(d, "PLAN.json"), {
        "experiment": exp, "hashes": {"tasks": {t: {"tree": t} for t in exp["tasks"]},
                                      "lanes": {"baseline": {"patch": None, "settings": plan_hashes.sha256_json(SETTINGS)}}},
        "lock": {"sha256": "x", "artifacts": {"baseline": artifact}}})
    plan = []
    for task, oks in passes.items():
        for r, ok in enumerate(oks, 1):
            cid = f"{task}/r{r}/baseline"
            plan.append({"cell": cid, "task": task, "rep": r, "lane": "baseline", "order": len(plan)})
            c = cell = os.path.join(d, "cells", task, f"r{r}", "baseline")
            os.makedirs(os.path.join(c, "run-log"))
            val = lambda v: v[task] if isinstance(v, dict) else v
            common.write_json(os.path.join(c, "result.json"), {
                "cell": cid, "outcome": "timeout" if cid in plumbing else "landed",
                "totals": {"cost_usd": val(cost), "wall_s": val(wall), "input_tokens": 100, "output_tokens": 50}, "stages": []})
            common.write_json(os.path.join(c, "evaluation.json"), {"all_passed": ok})
            open(os.path.join(c, "run-log", "log.jsonl"), "w").close()
    with open(os.path.join(d, "plan.jsonl"), "w") as f:
        for p in plan:
            f.write(json.dumps(p) + "\n")
    return d


class Noise(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.out = os.path.join(self.tmp, "noise.json")

    def noise(self, a, b):
        p = subprocess.run([sys.executable, os.path.join(BIN, "lanes-noise"), a, b, "--out", self.out],
                           capture_output=True, text=True)
        return p, (common.read_json(self.out) if p.returncode == 0 else None)

    def test_identical_runs_have_no_observed_spread(self):
        same = {t: [True, False] for t in TASKS}
        p, rec = self.noise(make_run(self.tmp, "a", same), make_run(self.tmp, "b", same))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(rec["overall"]["pass_rate"]["abs_difference"], 0)
        self.assertEqual(rec["rms_effect"], 0)  # the runs agree, yet 4 tasks resolve nothing finer than the floor
        self.assertEqual(rec["floor"], 1.0)
        self.assertEqual(rec["smallest_detectable_effect"], 1.0)
        self.assertEqual(rec["spread"], 1.0)
        self.assertEqual(rec["per_task"]["t1"]["pass_rate"], {"a": 0.5, "b": 0.5, "abs_diff": 0})
        self.assertEqual(rec["overall"]["cost_usd"]["interval"], [0, 0])
        self.assertEqual(rec["overall"]["tokens"]["abs_difference"], 0)
        self.assertEqual(rec["baseline"]["sha"], SHA)

    def test_spread_of_a_noisy_pair(self):
        a = make_run(self.tmp, "a", {"t1": [True, True], "t2": [True, True], "t3": [False, False], "t4": [True, False]},
                     cost={"t1": 1, "t2": 2, "t3": 3, "t4": 4}, wall=10)
        b = make_run(self.tmp, "b", {"t1": [True, False], "t2": [True, True], "t3": [False, False], "t4": [False, False]},
                     cost={"t1": 2, "t2": 2, "t3": 2, "t4": 2}, wall=14)
        p, rec = self.noise(a, b)
        self.assertEqual(p.returncode, 0, p.stderr)
        t1 = rec["per_task"]["t1"]
        self.assertEqual(t1["pass_rate"], {"a": 1.0, "b": 0.5, "abs_diff": 0.5})
        self.assertEqual(t1["cost_usd"]["abs_diff"], 1)
        pr = rec["overall"]["pass_rate"]
        self.assertEqual((pr["difference"], pr["abs_difference"], pr["mean_abs_task_difference"]), (0.25, 0.25, 0.25))
        self.assertLess(pr["interval"][0], 0.25)
        self.assertGreater(pr["interval"][1], 0.25)
        self.assertEqual(rec["overall"]["wall_s"]["difference"], -4)
        # task differences .5 0 0 .5: rms 0.3536, t(3) 3.182, 4 tasks: 3.182 * 0.3536 / 2
        self.assertAlmostEqual(rec["rms_effect"], 0.5625, places=4)
        self.assertEqual(rec["smallest_detectable_effect"], 1.0)  # the floor of 4 tasks is higher
        self.assertEqual(rec["spread"], 1.0)

    def test_floor_shrinks_with_the_number_of_tasks(self):
        names = [f"t{i}" for i in range(30)]
        same = {t: [True, False] for t in names}
        exp = lambda i: experiment(i, tasks=names)
        _, rec = self.noise(make_run(self.tmp, "a", same, exp=exp("a")), make_run(self.tmp, "b", same, exp=exp("b")))
        self.assertEqual(rec["rms_effect"], 0)
        self.assertAlmostEqual(rec["floor"], 0.4959, places=4)  # 2 * sqrt(ln(40) / 60)
        self.assertEqual(rec["spread"], rec["floor"])

    def test_plumbing_cells_are_left_out(self):
        a = make_run(self.tmp, "a", {t: [True, True] for t in TASKS}, plumbing=("t1/r1/baseline",))
        b = make_run(self.tmp, "b", {t: [True, True] for t in TASKS})
        _, rec = self.noise(a, b)
        self.assertEqual(rec["per_task"]["t1"]["pass_rate"]["a"], 1.0)

    def test_runs_must_be_one_plan(self):
        ok = {t: [True, True] for t in TASKS}
        a = make_run(self.tmp, "a", ok)
        cases = {
            "more than the run id": make_run(self.tmp, "b1", ok, exp=experiment("b1", reps=3)),
            "different baseline artifacts": make_run(self.tmp, "b2", ok, artifact="bb"),
            "same experiment id": a,
        }
        for want, other in cases.items():
            with self.subTest(want):
                p, _ = self.noise(a, other)
                self.assertEqual(p.returncode, 2)
                self.assertIn(want, p.stderr)
                self.assertFalse(os.path.exists(self.out))

    def test_baseline_lane_choice(self):
        ok = {t: [True, True] for t in TASKS}
        two = lambda i, names: experiment(i, lanes=[{"name": n, "sha": SHA, "patch": None, "settings": SETTINGS} for n in names])
        a, b = (make_run(self.tmp, i, ok, exp=two(i, ["x", "y"])) for i in ("a", "b"))
        p, _ = self.noise(a, b)
        self.assertEqual(p.returncode, 2)
        self.assertIn("none named baseline", p.stderr)

    def test_needs_two_tasks_and_a_run_dir(self):
        exp = experiment("a", tasks=["t1"])
        one = {"t1": [True, False]}
        p, _ = self.noise(make_run(self.tmp, "a", one, exp=exp), make_run(self.tmp, "b", one, exp=experiment("b", tasks=["t1"])))
        self.assertEqual(p.returncode, 2)
        self.assertIn("at least 2 tasks", p.stderr)
        p, _ = self.noise(os.path.join(self.tmp, "none"), os.path.join(self.tmp, "none2"))
        self.assertEqual(p.returncode, 2)


class Gate(unittest.TestCase):
    """`lanes-plan` refuses a climb unless its noise record fits and is quieter than min_effect."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.exp_path = os.path.join(self.tmp, "experiment.json")
        self.ref = os.path.join(self.tmp, "noise.json")
        self.record = {"kind": "noise", "phase": "build", "intent_form": "gherkin", "tasks": MANY, "reps": 2, "spread": 0.05,
                       "baseline": {"sha": SHA, "patch_sha256": None, "settings_sha256": plan_hashes.sha256_json(SETTINGS)}}

    def plan(self, exp_fields=None, record=None, write=True):
        exp = experiment("climb-r1", kind="climb", noise_ref="noise.json", min_effect=0.8, round=1, parent=None, tasks=MANY,
                         split={"train": MANY[:15], "test": MANY[15:]}, decision_rule={"kind": "keep_revert"})
        exp["lanes"] = [{"name": "baseline", "sha": SHA, "patch": None, "settings": SETTINGS},
                        {"name": "candidate", "sha": SHA, "patch": None,
                         "settings": {"models": {"build": "p/m low"}}}]
        exp.update(exp_fields or {})
        common.write_json(self.exp_path, exp)
        if write:
            common.write_json(self.ref, record or self.record)
        tasks = os.path.join(self.tmp, "tasks")
        os.makedirs(tasks, exist_ok=True)
        return subprocess.run([sys.executable, os.path.join(BIN, "lanes-plan"), self.exp_path, "--run-dir",
                               os.path.join(self.tmp, "run"), "--tasks", tasks], capture_output=True, text=True)

    def refused(self, why, **kw):
        p = self.plan(**kw)
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn(why, p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "run")))
        return p

    def test_quiet_enough_passes_the_gate(self):
        p = self.plan()  # the next check (the lock) is what stops it
        self.assertIn("run lanes-build first", p.stderr)

    def test_noisy_baseline_names_both_numbers(self):
        p = self.refused("spread 0.9", record=dict(self.record, spread=0.9))
        self.assertIn("min_effect 0.8", p.stderr)
        self.refused("spread 0.8 ", record=dict(self.record, spread=0.8))  # equal is not smaller

    def test_small_min_effect_cannot_pass_on_a_small_sample(self):
        # identical runs on 4 tasks: lanes-noise's record has spread 1.0, whatever min_effect is
        ok = {t: [True, True] for t in TASKS}
        run = os.path.join(self.tmp, "runs")
        subprocess.run([sys.executable, os.path.join(BIN, "lanes-noise"), make_run(run, "a", ok), make_run(run, "b", ok),
                        "--out", self.ref], check=True, capture_output=True)
        self.refused("spread 1.0", exp_fields={"min_effect": 0.01, "tasks": TASKS,
                                              "split": {"train": TASKS[:2], "test": TASKS[2:]}}, record=common.read_json(self.ref))

    def test_the_smaller_split_sets_a_floor(self):
        # 30 tasks and a quiet record, but a test split of 3 tasks: its floor (1.0) is the spread
        self.refused("spread 1.0", exp_fields={"split": {"train": MANY[:27], "test": MANY[27:]}})
        self.assertIn("3 tasks", self.plan(exp_fields={"split": {"train": MANY[:27], "test": MANY[27:]}}).stderr)

    def test_record_must_fit(self):
        self.refused("not a readable noise record", write=False)
        self.refused("not a readable noise record", record={"kind": "noise"})
        self.refused("another baseline (sha differs)", record=dict(self.record, baseline=dict(self.record["baseline"], sha="f" * 40)))
        self.refused("another baseline (settings_sha256 differs)",
                     record=dict(self.record, baseline=dict(self.record["baseline"], settings_sha256="0")))
        self.refused("another baseline (patch_sha256 differs)",
                     record=dict(self.record, baseline=dict(self.record["baseline"], patch_sha256="0")))
        self.refused("another phase", record=dict(self.record, phase="shape"))
        self.refused("kind is not noise", record=dict(self.record, kind="plan"))
        self.refused("recorded with reps 3", record=dict(self.record, reps=3))
        self.refused("another task set", record=dict(self.record, tasks=MANY[:-1]))

    def test_other_experiments_are_not_gated(self):
        exp = experiment("plain")
        common.write_json(self.exp_path, exp)
        p = subprocess.run([sys.executable, os.path.join(BIN, "lanes-plan"), self.exp_path, "--run-dir",
                            os.path.join(self.tmp, "run"), "--tasks", self.tmp], capture_output=True, text=True)
        self.assertIn("run lanes-build first", p.stderr)

    def test_a_recorded_noise_run_passes_the_gate(self):  # lanes-noise's own record satisfies the gate
        ok = {t: [True, True] for t in MANY}
        run = os.path.join(self.tmp, "runs")
        a, b = (make_run(run, i, ok, exp=experiment(i, tasks=MANY)) for i in ("a", "b"))
        subprocess.run([sys.executable, os.path.join(BIN, "lanes-noise"), a, b, "--out", self.ref], check=True, capture_output=True)
        self.assertIn("run lanes-build first", self.plan(write=False).stderr)


if __name__ == "__main__":
    unittest.main()
