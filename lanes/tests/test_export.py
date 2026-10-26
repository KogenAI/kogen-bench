import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import common, export, plan_hashes, usage

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
BIN = os.path.join(HERE, "..", "bin", "lanes-export")
REPO = export.REPO
SHA = "0123456789abcdef0123456789abcdef01234567"
PERSONAL = "/Us" + "ers/someone/work/secret-task"  # built in pieces: the repo scan rejects literal paths
EMAIL = "a" + "@" + "b.example"
HOST = "bench-box-7"
USAGE = {"input": 1000, "cached": 400, "output": 200, "reasoning": 50}


def read(path):
    with open(path) as f:
        return f.read()


def cell_result(cell, lane, events, outcome="landed"):
    commands = [{"stage": "build", "started": "2026-10-22T10:00:00Z", "ended": "2026-10-22T10:00:05Z", "wall_s": 5.0, "exit_code": 0}]
    parsed = usage.parse_run_log(events, commands, table={"models": {"fake-model": {"input": 1.0, "cached_input": 0.1, "output": 2.0}}})
    return {"cell": cell, "lane": lane, "phase": "build", "exit_code": 0, "outcome": outcome,
            "started": "2026-10-22T10:00:00Z", "ended": "2026-10-22T10:00:05Z", "wall_s": 5.0,
            "kogen_version": "kogen 01234567 (2026-10-01)", "final_tree": "ab" * 20, "pass_trees": [],
            "intent_hash": "cd" * 32, "host": HOST, **parsed}


def make_bench(root):
    """A small kogen-bench checkout: the validators and schema of this repo, an empty round list."""
    shutil.copytree(os.path.join(REPO, "reproduce"), os.path.join(root, "reproduce"),
                    ignore=lambda d, names: [n for n in names if os.path.isdir(os.path.join(d, n))])
    shutil.copytree(os.path.join(REPO, "schema"), os.path.join(root, "schema"))
    os.makedirs(os.path.join(root, "results"))
    shutil.copy(os.path.join(REPO, "results", "missing-reasons.json"), os.path.join(root, "results"))
    os.makedirs(os.path.join(root, "rounds"))
    common.write_json(os.path.join(root, "rounds", "index.json"), [])
    for name in ("STATUS.md", "README.md"):
        open(os.path.join(root, "rounds", name), "w").close()


class Export(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.bench = os.path.join(self.tmp, "bench")
        make_bench(self.bench)
        self.tasks = os.path.join(self.tmp, "tasks")
        shutil.copytree(os.path.join(FIX, "task-mini"), os.path.join(self.tasks, "task-mini"))
        self.run_dir = os.path.join(self.tmp, "run")
        exp = common.read_json(os.path.join(FIX, "experiment-good.json"))
        exp.update(tasks=["task-mini"], reps=1, hosts=[HOST])
        exp["lanes"][0]["sha"] = exp["lanes"][1]["sha"] = SHA
        os.makedirs(os.path.join(self.run_dir, "patches"))
        with open(os.path.join(self.run_dir, "patches", "p1.patch"), "w") as f:
            f.write("--- a/x\n+++ b/x\n@@ -1 +1,2 @@\n-old\n+new\n+newer\n")
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        self.lock = [{"name": n, "sha": SHA, "patch_sha256": None, "artifact_sha256": "ab" * 32, "kogen_version": "v"}
                     for n in ("base", "patched")]
        common.write_json(os.path.join(self.run_dir, "lanes.lock.json"), self.lock)
        rows = []
        for i, lane in enumerate(("base", "patched")):
            cell = f"task-mini/r0/{lane}"
            rows.append({"cell": cell, "task": "task-mini", "rep": 0, "lane": lane, "order": i})
            events = [{"event": "request", "role": "build", "model": "fake-model", "effort": "high", "usage": USAGE, "wall_ms": 250},
                      {"event": "outcome", "outcome": "landed"}]
            cd = common.cell_dir(self.run_dir, cell)
            common.write_json(os.path.join(cd, "result.json"), cell_result(cell, lane, events))
            common.write_json(os.path.join(cd, "evaluation.json"), {
                "all_passed": lane == "base", "ids": {"t1": "passed"}, "commands": [{"name": "hidden", "status": 0, "wall_ms": 40}],
                "stdout": f"building in {PERSONAL} on {HOST}"})
            os.makedirs(os.path.join(cd, "run-log"))
            with open(os.path.join(cd, "run-log", "log.jsonl"), "w") as f:
                f.writelines(json.dumps(e) + "\n" for e in events)
        with open(os.path.join(self.run_dir, "plan.jsonl"), "w") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
        self.out = os.path.join(self.bench, "rounds", "lane-test-1")
        self.write_plan()

    def write_plan(self):
        """What lanes-plan writes before the run."""
        plan = plan_hashes.build_plan(os.path.join(self.run_dir, "experiment.json"), self.tasks, os.path.join(self.run_dir, "lanes.lock.json"))
        common.write_json(os.path.join(self.run_dir, "PLAN.json"), plan)
        return plan

    def edit(self, lane, name, fn):
        path = os.path.join(common.cell_dir(self.run_dir, f"task-mini/r0/{lane}"), name)
        data = common.read_json(path)
        fn(data)
        common.write_json(path, data)

    def checkout_state(self):
        """Every file of the bench checkout with its bytes: a failed export must leave this unchanged."""
        return {os.path.relpath(os.path.join(d, f), self.bench): read(os.path.join(d, f))
                for d, _, fs in os.walk(self.bench) for f in fs}

    def export(self, *extra, check="round"):
        return subprocess.run([sys.executable, BIN, self.run_dir, "--round-id", "lane-test-1", "--out", self.out,
                               "--tasks", self.tasks, "--date", "2026-10-22", "--check", check, *extra],
                              capture_output=True, text=True)

    def records(self):
        return [json.loads(l) for l in read(os.path.join(self.out, "records.jsonl")).splitlines()]

    def test_export_passes_strict_validation(self):
        r = self.export()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS WITH DECLARED DEVIATIONS", r.stdout)
        for name in ("PLAN.json", "records.jsonl", "README.md", "MISSING.md", "MISSING-DECLARED.json", "patches/patched/p1.patch"):
            self.assertTrue(os.path.exists(os.path.join(self.out, name)), name)
        self.assertEqual(len(glob.glob(os.path.join(self.out, "bundles", "*", "attempts", "*", "r0", "*", "a1", "evaluation.json"))), 2)
        readme = read(os.path.join(self.out, "README.md"))
        self.assertIn("p1.patch", readme)
        self.assertIn("+2/-1", readme)
        self.assertIn("lane-test-1 | DESCRIPTIVE", read(os.path.join(self.bench, "rounds", "STATUS.md")))

    def test_record_fields(self):
        self.export()
        base, patched = sorted(self.records(), key=lambda r: r["arm"])
        self.assertEqual((base["outcome"], patched["outcome"]), ("pass", "fail"))
        self.assertEqual(base["tokens"]["total"], {"input": 600, "cached_input": 400, "output": 200, "reasoning": 50})
        self.assertEqual(base["cost"]["usd"], 0.00104)
        self.assertEqual(base["model"], {"requested": "openai/gpt-x", "effective": "fake-model"})
        self.assertEqual(base["tools"]["kogen"], "kogen 01234567 (2026-10-01)")
        self.assertEqual(base["setup"]["kogen_sha"], SHA)
        self.assertEqual(base["timing"]["phases_s"]["grade"], 0.04)

    def test_privacy_filter_removes_planted_path_and_host(self):
        self.assertEqual(self.export().returncode, 0)
        bundle = glob.glob(os.path.join(self.out, "bundles", "*", "attempts", "*", "r0", "base", "a1", "evaluation.json"))[0]
        self.assertNotIn("stdout", read(bundle))  # evaluation is whitelisted
        text = export.scrub(f"at {PERSONAL}/x on {HOST} mail {EMAIL} key sk-abcdef123456789", [HOST])
        self.assertNotIn("someone", text)
        self.assertNotIn(HOST, text)
        self.assertNotIn("sk-abc", text)
        for dirpath, _, files in os.walk(self.out):
            for n in files:
                body = read(os.path.join(dirpath, n))
                self.assertEqual(export.leaks(body, [HOST]), [], n)

    def test_planted_path_in_record_fields_is_scrubbed(self):
        def plant(res):
            res["kogen_version"] = f"kogen dev ({PERSONAL})"
            res["totals"]["models"] = [f"{PERSONAL}/model"]
        self.edit("base", "result.json", plant)
        self.assertEqual(self.export().returncode, 0)
        self.assertNotIn("someone", read(os.path.join(self.out, "records.jsonl")))
        base = [r for r in self.records() if r["arm"] == "base"][0]
        self.assertIn("[redacted]", base["tools"]["kogen"])
        self.assertIn("[redacted]", base["model"]["effective"])

    def test_scrub_keeps_every_lab_path_root(self):
        for root in ("var/log", "opt/x", "srv/x", "mnt/x", "root/x", "Volumes/x", "tmp/x"):
            self.assertEqual(export.scrub(f"see /{root}/file"), "see [redacted]", root)

    def test_missing_field_is_declared_not_invented(self):
        path = os.path.join(common.cell_dir(self.run_dir, "task-mini/r0/base"), "result.json")
        res = common.read_json(path)
        res["totals"].update(input_tokens=None, cost_usd=None, missing=["input_tokens", "cost_usd"])
        for s in res["stages"]:
            s.update(input_tokens=None, cost_usd=None, missing=["input_tokens"])
        common.write_json(path, res)
        r = self.export()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        base = [x for x in self.records() if x["arm"] == "base"][0]
        self.assertEqual(base["tokens"]["total"]["input"], {"missing": "m10"})
        self.assertEqual(base["tokens"]["phases"]["develop"]["input"], {"missing": "m44"})
        self.assertEqual(base["cost"]["usd"], {"missing": "m70"})
        declared = common.read_json(os.path.join(self.out, "MISSING-DECLARED.json"))["fields"]
        self.assertEqual(declared["cost.usd"]["count"], 1)
        self.assertEqual(declared["tokens.total.input"]["reason_code"], "m10")

    def test_ungraded_cell_is_excluded_not_exported(self):
        os.remove(os.path.join(common.cell_dir(self.run_dir, "task-mini/r0/patched"), "evaluation.json"))
        self.assertEqual(self.export().returncode, 0)
        self.assertEqual(len(self.records()), 1)
        excluded = glob.glob(os.path.join(self.out, "bundles", "*", "EXCLUDED.json"))[0]
        self.assertIn("task-mini/r0/patched", read(excluded))

    def test_refuses_outside_a_bench_and_non_empty_out(self):
        r = subprocess.run([sys.executable, BIN, self.run_dir, "--round-id", "x", "--out", os.path.join(self.tmp, "x"),
                            "--tasks", self.tasks], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("kogen-bench checkout", r.stderr)
        self.assertEqual(self.export().returncode, 0)
        self.assertEqual(self.export().returncode, 2)

    def test_publish_private_checks_plan_hashes(self):
        self.assertEqual(self.export().returncode, 0)
        r = self.export("--publish-private")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.isfile(os.path.join(self.out, "reproduce", "tasks", "task-mini", "evaluator", "evaluate.toml")))
        hidden = glob.glob(os.path.join(self.tasks, "task-mini", "evaluator", "files", "**", "*.go"), recursive=True)[0]
        with open(hidden, "a") as f:
            f.write("// changed after the plan\n")
        r = self.export("--publish-private")
        self.assertEqual(r.returncode, 1)
        self.assertIn("tasks/task-mini/hidden_tests", r.stderr)

    def test_publish_private_marks_the_plan_closed_with_the_file_hashes(self):
        self.assertEqual(self.export().returncode, 0)
        before = common.read_json(os.path.join(self.out, "PLAN.json"))
        self.assertNotIn("publication", before)
        self.assertEqual(self.export("--publish-private").returncode, 0)
        plan = common.read_json(os.path.join(self.out, "PLAN.json"))
        self.assertEqual({k: v for k, v in plan.items() if k != "publication"}, before)
        pub = plan["publication"]
        self.assertIs(pub["closed"], True)
        self.assertRegex(pub["closed_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        rel = "reproduce/tasks/task-mini/evaluator/"
        self.assertIn(rel + "evaluate.toml", pub["files"])
        for name, digest in pub["files"].items():
            self.assertTrue(name.startswith(rel))
            self.assertEqual(common.sha256_file(os.path.join(self.out, name)), digest)
        self.assertEqual(common.sha256_tree(os.path.join(self.out, rel)), plan["hashes"]["tasks"]["task-mini"]["hidden_tests"])
        self.assertEqual(self.export("--publish-private").returncode, 0)
        self.assertEqual(common.read_json(os.path.join(self.out, "PLAN.json"))["publication"], pub)

    def test_publish_private_mismatch_leaves_the_plan_unmarked(self):
        self.assertEqual(self.export().returncode, 0)
        hidden = glob.glob(os.path.join(self.tasks, "task-mini", "evaluator", "files", "**", "*.go"), recursive=True)[0]
        with open(hidden, "a") as f:
            f.write("// changed\n")
        r = self.export("--publish-private")
        self.assertEqual(r.returncode, 1)
        self.assertIn("private inputs differ from PLAN.json", r.stderr)
        self.assertNotIn("publication", common.read_json(os.path.join(self.out, "PLAN.json")))

    def test_published_hidden_files_refuses_a_staged_folder_that_differs_from_the_plan(self):
        stage = os.path.join(self.tmp, "stage", "reproduce")
        folder = os.path.join(stage, "tasks", "t", "evaluator")
        os.makedirs(folder)
        with open(os.path.join(folder, "a.txt"), "w") as f:
            f.write("a")
        plan = {"hashes": {"tasks": {"t": {"hidden_tests": common.sha256_tree(folder)}}}}
        self.assertEqual(list(export.published_hidden_files(stage, plan, ["t"])), ["reproduce/tasks/t/evaluator/a.txt"])
        with open(os.path.join(folder, "a.txt"), "w") as f:
            f.write("b")
        with self.assertRaisesRegex(export.ExportError, "published hidden tests differ"):
            export.published_hidden_files(stage, plan, ["t"])

    def test_publish_private_twice_gives_identical_trees_with_cell_trees(self):
        for cell in ("task-mini/r0/base", "task-mini/r0/patched"):
            cd = common.cell_dir(self.run_dir, cell)
            with open(os.path.join(cd, "final-tree.tar"), "wb") as f:
                f.write(b"final " + cell.encode())
            os.makedirs(os.path.join(cd, "pass-trees"))
            with open(os.path.join(cd, "pass-trees", "p1.tar"), "wb") as f:
                f.write(b"pass " + cell.encode())
        self.assertEqual(self.export().returncode, 0)

        def tree():
            root = os.path.join(self.out, "reproduce")
            return {os.path.relpath(os.path.join(d, f), root): read(os.path.join(d, f)) for d, _, fs in os.walk(root) for f in fs}
        self.assertEqual(self.export("--publish-private").returncode, 0)
        first = tree()
        self.assertEqual(first["cells/task-mini/r0/base/final-tree.tar"], "final task-mini/r0/base")
        self.assertEqual(first["cells/task-mini/r0/patched/pass-trees/p1.tar"], "pass task-mini/r0/patched")
        self.assertNotIn("cells/task-mini/r0/base/result.json", first)
        self.assertEqual(self.export("--publish-private").returncode, 0)
        self.assertEqual(tree(), first)
        self.assertEqual([n for n in os.listdir(self.out) if n.startswith(".")], [])

    # ---- review round 1 ----

    def test_b1_refuses_without_a_plan_from_before_the_run(self):
        os.remove(os.path.join(self.run_dir, "PLAN.json"))
        before = self.checkout_state()
        r = self.export()
        self.assertEqual(r.returncode, 2)
        self.assertIn("PLAN.json", r.stderr)
        self.assertEqual(self.checkout_state(), before)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "PLAN.json")))

    def test_b1_refuses_a_plan_for_another_experiment(self):
        plan = self.write_plan()
        plan["experiment"]["reps"] = 9
        common.write_json(os.path.join(self.run_dir, "PLAN.json"), plan)
        r = self.export()
        self.assertEqual(r.returncode, 2)
        self.assertIn("experiment", r.stderr)

    def test_b1_published_plan_is_the_run_plan_not_a_rebuild(self):
        plan = self.write_plan()
        hidden = glob.glob(os.path.join(self.tasks, "task-mini", "evaluator", "files", "**", "*.go"), recursive=True)[0]
        with open(hidden, "a") as f:
            f.write("// changed after the run\n")
        self.assertEqual(self.export().returncode, 0)
        self.assertEqual(common.read_json(os.path.join(self.out, "PLAN.json"))["hashes"]["tasks"], plan["hashes"]["tasks"])

    def test_b2_shape_phase_keeps_grades(self):
        exp = common.read_json(os.path.join(self.run_dir, "experiment.json"))
        exp["phase"] = "shape"
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        self.write_plan()
        for lane, caught in (("base", 1), ("patched", 0)):
            self.edit(lane, "result.json", lambda r: r.update(phase="shape"))
            self.edit(lane, "evaluation.json", lambda e, c=caught: (e.pop("all_passed"), e.update(
                scenarios=4, pass_on_reference=4, fail_on_start=4, wrong_caught=c, wrong_total=1)))
        r = self.export()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        base, patched = sorted(self.records(), key=lambda x: x["arm"])
        self.assertEqual((base["outcome"], patched["outcome"]), ("pass", "fail"))
        bundle = glob.glob(os.path.join(self.out, "bundles", "*", "attempts", "*", "r0", "base", "a1", "evaluation.json"))[0]
        self.assertEqual(common.read_json(bundle)["wrong_caught"], 1)
        readme = read(os.path.join(self.out, "README.md"))
        self.assertIn("Scenarios passing on reference", readme)
        self.assertNotIn("All hidden tests passed", readme)
        self.assertIn("| base | 1 | 1 | 4 of 4 | 1 of 1 |", readme)

    def test_shape_cell_that_passes_on_start_does_not_pass(self):  # L9: fail_on_start counts
        exp = common.read_json(os.path.join(self.run_dir, "experiment.json"))
        exp["phase"] = "shape"
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        self.write_plan()
        for lane in ("base", "patched"):
            self.edit(lane, "result.json", lambda r: r.update(phase="shape"))
            self.edit(lane, "evaluation.json", lambda e: (e.pop("all_passed"), e.update(
                scenarios=4, pass_on_reference=4, fail_on_start=3, wrong_caught=1, wrong_total=1)))
        self.assertEqual(self.export().returncode, 0)
        self.assertEqual({r["outcome"] for r in self.records()}, {"fail"})

    def test_b3_leak_leaves_the_checkout_unchanged(self):
        with open(os.path.join(self.run_dir, "patches", "p1.patch"), "a") as f:
            f.write("+path = '" + PERSONAL + "'\n")
        self.write_plan()
        before = self.checkout_state()
        r = self.export()
        self.assertEqual(r.returncode, 1)
        self.assertIn("patches/patched/p1.patch", r.stderr)
        self.assertEqual(self.checkout_state(), before)
        self.assertEqual(sorted(os.listdir(os.path.join(self.bench, "rounds"))), ["README.md", "STATUS.md", "index.json"])

    def test_b3_failed_validation_restores_the_checkout(self):
        with open(os.path.join(self.bench, "reproduce", "validate_round.py"), "w") as f:
            f.write("raise SystemExit(3)\n")
        before = self.checkout_state()
        r = self.export()
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("wrote", r.stdout)  # L9: no success line after a failed validation
        self.assertEqual(self.checkout_state(), before)
        self.assertEqual(sorted(os.listdir(os.path.join(self.bench, "rounds"))), ["README.md", "STATUS.md", "index.json"])
        self.assertEqual(self.export_ok_after_fix(), 0)

    def export_ok_after_fix(self):
        shutil.copy(os.path.join(REPO, "reproduce", "validate_round.py"), os.path.join(self.bench, "reproduce"))
        return self.export().returncode

    def test_b3_publish_private_mismatch_copies_nothing(self):
        self.assertEqual(self.export().returncode, 0)
        hidden = glob.glob(os.path.join(self.tasks, "task-mini", "evaluator", "files", "**", "*.go"), recursive=True)[0]
        with open(hidden, "a") as f:
            f.write("// changed\n")
        r = self.export("--publish-private")
        self.assertEqual(r.returncode, 1)
        self.assertFalse(os.path.exists(os.path.join(self.out, "reproduce")))
        self.assertEqual([n for n in os.listdir(self.out) if n.startswith(".")], [])

    def test_m3_develop_holds_build_and_repair_tokens(self):
        events = [{"event": "request", "role": "build", "model": "fake-model", "effort": "high", "usage": USAGE, "wall_ms": 250},
                  {"event": "request", "role": "repair", "model": "fake-model", "effort": "high", "usage": USAGE, "wall_ms": 100},
                  {"event": "outcome", "outcome": "landed"}]
        self.edit("base", "result.json", lambda r: r.update(cell_result("task-mini/r0/base", "base", events)))
        self.assertEqual(self.export().returncode, 0)
        base = [r for r in self.records() if r["arm"] == "base"][0]
        self.assertEqual(base["tokens"]["phases"]["develop"]["input"], 1200)
        self.assertEqual(base["tokens"]["phases"]["develop"], {k: v for k, v in base["tokens"]["total"].items()})

    def test_m4_provider_failure_maps_to_provider_error(self):
        path = os.path.join(common.cell_dir(self.run_dir, "task-mini/r0/base"), "run-log", "log.jsonl")
        with open(path, "a") as f:
            f.write(json.dumps({"event": "outcome", "outcome": "model_unavailable", "provider_failure": {"status": 503}}) + "\n")
        self.assertEqual(self.export().returncode, 0)
        stops = {r["arm"]: r["stop_reason"] for r in self.records()}
        self.assertEqual(stops, {"base": "provider_error", "patched": "completed"})

    def test_m5_infrastructure_failure_is_invalid_and_no_tests_ran(self):
        self.edit("base", "evaluation.json", lambda e: e.update(infrastructure="setup failed", all_passed=False))
        self.assertEqual(self.export().returncode, 0)
        base = [r for r in self.records() if r["arm"] == "base"][0]
        self.assertEqual((base["outcome"], base["grade"]["tests_ran"]), ("invalid", False))

    def test_m7_lanes_table_has_the_full_patch_hash(self):
        plan = self.write_plan()
        self.assertEqual(self.export().returncode, 0)
        self.assertIn(plan["hashes"]["lanes"]["patched"]["patch"], read(os.path.join(self.out, "README.md")))

    def test_m9_patch_context_with_tmp_literal_is_exportable(self):
        with open(os.path.join(self.run_dir, "patches", "p1.patch"), "a") as f:
            f.write(" System.tmp_dir() == \"/tmp/kogen\"\n")
        self.write_plan()
        r = self.export()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_m10_counts_started_cells_from_results(self):
        os.remove(os.path.join(common.cell_dir(self.run_dir, "task-mini/r0/patched"), "evaluation.json"))
        self.assertEqual(self.export().returncode, 0)
        readme = read(os.path.join(self.out, "README.md"))
        for line in ("| Planned cells | 2 |", "| Started cells | 2 |", "| Finished cells | 2 |", "| Graded cells | 1 |"):
            self.assertIn(line, readme)

    def test_m11_ledger_hash_is_recomputable_from_the_bundle(self):
        self.assertEqual(self.export().returncode, 0)
        d = glob.glob(os.path.join(self.out, "bundles", "*", "attempts", "task-mini", "r0", "base", "a1"))[0]
        want = plan_hashes.sha256_json({"attempt": common.read_json(os.path.join(d, "attempt.json")),
                                        "evaluation": common.read_json(os.path.join(d, "evaluation.json"))})
        base = [r for r in self.records() if r["arm"] == "base"][0]
        self.assertEqual(base["provenance"]["ledger_sha256"], want)

    @unittest.skipUnless(os.environ.get("KOGEN_LANES_FULL_VALIDATE"), "set KOGEN_LANES_FULL_VALIDATE=1 (full checkout, minutes)")
    def test_release_gate_on_a_full_checkout(self):
        bench = os.path.join(self.tmp, "full")
        os.makedirs(bench)
        archive = subprocess.Popen(["git", "archive", "HEAD"], cwd=REPO, stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", bench, "--exclude", "lanes"], stdin=archive.stdout, check=True)
        archive.stdout.close()
        archive.wait()
        subprocess.run(["git", "init", "-q"], cwd=bench, check=True)
        subprocess.run(["git", "add", "-A"], cwd=bench, check=True)
        self.out = os.path.join(bench, "rounds", "lane-test-1")
        r = self.export(check="release")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("RELEASE GATE: PASS", r.stdout)


class PublicCellFirstGreen(unittest.TestCase):
    def test_the_first_green_tree_is_published_when_the_result_has_it(self):
        res = cell_result("task-mini/r1/base", "base", [])
        attempt, _ = export.public_cell(dict(res, first_green_tree="ef" * 20), {}, [])
        self.assertEqual(attempt["first_green_tree"], "ef" * 20)
        attempt, _ = export.public_cell(dict(res, first_green_tree=None), {}, [])
        self.assertIsNone(attempt["first_green_tree"])

    def test_an_older_result_publishes_the_same_keys_as_before(self):
        attempt, _ = export.public_cell(cell_result("task-mini/r1/base", "base", []), {}, [])
        self.assertNotIn("first_green_tree", attempt)


if __name__ == "__main__":
    unittest.main()
