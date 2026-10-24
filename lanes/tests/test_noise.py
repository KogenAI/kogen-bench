import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import common, noise as noise_mod, plan_hashes

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin")
SHA = "0123456789abcdef0123456789abcdef01234567"
SETTINGS = {"models": {"build": "openai/m high"}}
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


class SplitHalf(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def run_noise(self, *args):
        out = os.path.join(self.tmp, "out.json")
        p = subprocess.run([sys.executable, os.path.join(BIN, "lanes-noise"), *args, "--out", out], capture_output=True, text=True)
        return p, (common.read_json(out) if p.returncode == 0 else None)

    def test_split_half_equals_the_two_run_record_of_the_same_cells(self):
        reps = {"t1": [True, False, True, True], "t2": [True, False, False, False], "t3": [False, False, False, False],
                "t4": [True, True, True, True]}
        whole = make_run(self.tmp, "w", reps, exp=experiment("w", reps=4))
        first = make_run(self.tmp, "a", {t: v[:2] for t, v in reps.items()}, exp=experiment("a"))
        second = make_run(self.tmp, "b", {t: v[2:] for t, v in reps.items()}, exp=experiment("b"))
        p, half = self.run_noise(whole, "--split-half")
        self.assertEqual(p.returncode, 0, p.stderr)
        _, two = self.run_noise(first, second)
        self.assertIs(half.pop("split_half"), True)
        self.assertEqual(half.pop("r"), 2)
        self.assertEqual((half.pop("runs"), two.pop("runs")), (["w"], ["a", "b"]))
        self.assertEqual(half, two)
        self.assertEqual(half["reps"], 2)
        self.assertNotIn("split_half", two)
        # halves 0.5 / 1.0 for t1; reps split by parity would give 1.0 / 0.5
        self.assertEqual(half["per_task"]["t1"]["pass_rate"], {"a": 0.5, "b": 1.0, "abs_diff": 0.5})

    def test_tasks_and_exclude_choose_the_record_task_set(self):
        names = [f"t{i}" for i in range(6)]
        reps = {t: [True, False, i % 2 == 0, False] for i, t in enumerate(names)}
        whole = make_run(self.tmp, "w", reps, exp=experiment("w", reps=4, tasks=names))
        p, rec = self.run_noise(whole, "--split-half", "--tasks", "t0,t1,t2,t3")
        self.assertEqual((p.returncode, rec["tasks"], sorted(rec["per_task"])), (0, names[:4], names[:4]), p.stderr)
        p, ex = self.run_noise(whole, "--split-half", "--exclude", "t4,t5")
        self.assertEqual(ex, rec)
        p, both = self.run_noise(whole, "--split-half", "--tasks", "t0,t1,t2,t3,t4", "--exclude", "t4")
        self.assertEqual(both, rec)
        _, full = self.run_noise(whole, "--split-half")
        self.assertEqual(full["tasks"], names)
        for args in (("--tasks", "t0,nope"), ("--exclude", "nope"), ("--tasks", "t0")):
            p, _ = self.run_noise(whole, "--split-half", *args)
            self.assertEqual(p.returncode, 2, args)
        p, _ = self.run_noise(whole, whole, "--tasks", "t0,t1")
        self.assertEqual(p.returncode, 2)
        self.assertIn("go with --split-half", p.stderr)

    def test_gate_compares_a_filtered_record_with_the_climb_tasks(self):
        names = [f"t{i}" for i in range(30)]
        whole = make_run(self.tmp, "w", {t: [True, False, True, False] for t in names}, exp=experiment("w", reps=4, tasks=names))
        out = os.path.join(self.tmp, "n.json")
        subprocess.run([sys.executable, os.path.join(BIN, "lanes-noise"), whole, "--split-half", "--exclude", "t29",
                        "--out", out], check=True, capture_output=True)
        rec = common.read_json(out)
        mk = lambda tasks: dict(experiment("c", reps=2, tasks=tasks, kind="climb", noise_ref="n.json", min_effect=0.8, round=1,
                                           parent=None, split={"train": tasks[:15], "test": tasks[15:]},
                                           decision_rule={"kind": "keep_revert"}))
        path = os.path.join(self.tmp, "experiment.json")
        common.write_json(path, mk(names[:29]))
        noise_mod.check_gate(mk(names[:29]), path)
        with self.assertRaises(noise_mod.NoiseError) as e:
            noise_mod.check_gate(mk(names), path)
        self.assertIn("another task set", str(e.exception))

    def test_split_half_needs_one_even_run(self):
        ok = {t: [True] * 3 for t in TASKS}
        p, _ = self.run_noise(make_run(self.tmp, "odd", ok, exp=experiment("odd", reps=3)), "--split-half")
        self.assertEqual(p.returncode, 2)
        self.assertIn("even number of reps", p.stderr)
        run = make_run(self.tmp, "x", {t: [True] * 2 for t in TASKS})
        for args in ((run, run, "--split-half"), (run,)):
            p, _ = self.run_noise(*args)
            self.assertEqual(p.returncode, 2)

    def test_gate_accepts_a_split_half_record_and_checks_r(self):
        names = [f"t{i}" for i in range(30)]
        ok = {t: [True, False, True, False] for t in names}
        whole = make_run(self.tmp, "w", ok, exp=experiment("w", reps=4, tasks=names))
        _, rec = self.run_noise(whole, "--split-half")
        exp = dict(experiment("c", reps=2, tasks=names, kind="climb", noise_ref="n.json", min_effect=0.8, round=1, parent=None,
                              split={"train": names[:15], "test": names[15:]}, decision_rule={"kind": "keep_revert"}),
                   lanes=[{"name": "baseline", "sha": SHA, "patch": None, "settings": SETTINGS}])
        path = os.path.join(self.tmp, "experiment.json")
        common.write_json(path, exp)
        common.write_json(os.path.join(self.tmp, "n.json"), rec)
        noise_mod.check_gate(exp, path)
        with self.assertRaises(noise_mod.NoiseError) as e:
            noise_mod.check_gate(dict(exp, reps=3), path)
        self.assertIn("recorded with reps 2", str(e.exception))


class SignFloor(unittest.TestCase):
    def test_values(self):
        f = noise_mod.sign_floor
        self.assertEqual(f(0.10, 2, 12), (4, 4 / 24))
        self.assertAlmostEqual(f(0.10, 2, 12)[1], 0.1667, places=4)
        self.assertEqual(f(0.05, 2, 12), (5, 5 / 24))
        self.assertEqual(f(0.125, 1, 10), (3, 0.3))  # 0.5 ** 3 is exactly 0.125
        self.assertEqual(f(0.5, 3, 10), (1, 1 / 30))
        self.assertEqual(f(0.01, 4, 20), (7, 7 / 80))


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
                         "settings": {"models": {"build": "openai/m low"}}}]
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

    def sign_plan(self, min_effect, max_p=0.10, **record):
        names = MANY[:24]
        return self.plan(exp_fields={"tasks": names, "min_effect": min_effect, "split": {"train": names[:12], "test": names[12:]},
                                     "decision_rule": {"kind": "keep_revert", "improves": {"test": "task_sign", "max_p": max_p}}},
                         record=dict(self.record, tasks=names, **record))

    def test_task_sign_floor_is_the_gate_floor(self):
        # 12 tasks in the smaller split, 2 reps, max_p 0.10: 4 / 24 = 0.1667
        self.assertIn("run lanes-build first", self.sign_plan(0.17).stderr)
        for me in (0.1667, 0.1666):  # 0.1667 is above 0.166667; 0.1666 is not
            p = self.sign_plan(me)
            self.assertEqual("run lanes-build first" in p.stderr, me == 0.1667, p.stderr)
        p = self.sign_plan(0.1666)
        self.assertEqual(p.returncode, 2)
        self.assertIn("sign-test floor 0.166667 (k_min 4 at max_p 0.1, / (2 reps x 12 tasks in the smaller split))", p.stderr)
        self.assertIn("min_effect 0.1666", p.stderr)
        # the Hoeffding floor (0.79 for 12 tasks) would have refused 0.17
        self.assertEqual(self.plan(exp_fields={"tasks": MANY[:24], "min_effect": 0.17,
                                              "split": {"train": MANY[:12], "test": MANY[12:24]}},
                                   record=dict(self.record, tasks=MANY[:24])).returncode, 2)

    def test_task_sign_refuses_a_split_too_small_to_improve(self):
        names = MANY[:6]  # 3 + 3 tasks, reps 2, max_p 0.10: k_min 4, so the floor 4/6 looks finite but no split can improve
        p = self.plan(exp_fields={"tasks": names, "min_effect": 0.7, "split": {"train": names[:3], "test": names[3:]},
                                  "decision_rule": {"kind": "keep_revert", "improves": {"test": "task_sign", "max_p": 0.10}}},
                      record=dict(self.record, tasks=names, spread=0.0))
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn("the smaller split has 3 tasks; the sign test at max_p 0.1 needs at least 4", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "run")))
        # exactly k_min tasks is enough
        names = MANY[:8]
        p = self.plan(exp_fields={"tasks": names, "min_effect": 0.9, "split": {"train": names[:4], "test": names[4:]},
                                  "decision_rule": {"kind": "keep_revert", "improves": {"test": "task_sign", "max_p": 0.10}}},
                      record=dict(self.record, tasks=names, spread=0.0))
        self.assertIn("run lanes-build first", p.stderr)

    def test_task_sign_gate_still_refuses_a_measured_spread(self):
        rec = {"rms_effect": 0.3, "overall": {"pass_rate": {"abs_difference": 0.1}}, "spread": 0.9}
        p = self.sign_plan(0.3, **rec)  # the record's own Hoeffding floor (0.9) is not used; the t-bound 0.3 is not below 0.3
        self.assertEqual(p.returncode, 2)
        self.assertIn("measured run-to-run spread 0.3", p.stderr)
        self.assertIn("run lanes-build first", self.sign_plan(0.31, **rec).stderr)

    def test_default_gate_message_is_unchanged(self):
        p = self.refused("run-to-run spread 1.0 (at least the floor for the smaller split, 3 tasks) is not smaller than "
                         "min_effect 0.8; the climb cannot tell such an effect from noise",
                         exp_fields={"split": {"train": MANY[:27], "test": MANY[27:]}})
        self.assertNotIn("sign-test", p.stderr)

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
