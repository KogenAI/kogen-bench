"""Export and reproduce of a probe round: a synthetic corpus, fake probe commands, a minimal kogen-bench checkout."""

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import common, export, probe
from tests.test_export import REPO, make_bench, read
from tests.test_probe import FIX, ITEMS, write_corpus

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "bin")
REPRODUCE = os.path.join(HERE, "..", "reproduce.sh")
ROUND = "probe-test-1"


def lane(name, key, script="rank.py", python=sys.executable, *extra):
    return {"name": name, "probe": {"command": [python, script, *extra], "args": {"key": key}}}


def interpreters(tmp):
    """A venv python; a CI toolcache shim (a text script named python3); a binary helper (a link to this Python, not
    named like an interpreter). All three live outside the system folders."""
    venv = os.path.join(tmp, "venv")
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", venv], check=True)
    shim = os.path.join(tmp, "opt", "hostedtoolcache", "Python", "3.12.1", "x64", "bin", "python3")
    os.makedirs(os.path.dirname(shim))
    with open(shim, "w") as f:
        f.write(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n')
    os.chmod(shim, 0o755)
    helper = os.path.join(tmp, "helpers", "helper")
    os.makedirs(os.path.dirname(helper))
    os.symlink(os.path.realpath(sys.executable), helper)
    return os.path.join(venv, "bin", "python3"), shim, helper


class ProbeRound(unittest.TestCase):
    """Lanes a, b and c run no model (step 0); lane m reports usage. a runs under a CI toolcache shim, b under a venv
python, c is a script under a home folder named by absolute path (it fails on item i3), m passes a binary helper."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.home = os.path.join(cls.tmp, "home")
        cls.env = dict(os.environ, KOGEN_LANES_HOME=cls.home)
        cls.env.pop("KOGEN_LANES_CORPUS", None)
        folder = os.path.join(cls.tmp, "exp")
        os.makedirs(folder)
        for name in ("rank.py", "model.py", "grader.py"):
            shutil.copyfile(os.path.join(FIX, name), os.path.join(folder, name))
        elsewhere = os.path.join(cls.tmp, "Users", "someone", "anything")  # ~/anything, outside the experiment folder
        os.makedirs(elsewhere)
        cls.venv_python, cls.shim, cls.helper = interpreters(cls.tmp)
        cls.flaky = os.path.join(elsewhere, "flaky.py")
        shutil.copyfile(os.path.join(FIX, "flaky.py"), cls.flaky)
        cls.corpus = os.path.join(folder, "corpus")
        write_corpus(cls.corpus)
        exp = {"id": "probe-1", "phase": "probe", "corpus": "corpus", "reps": 2, "deadline_s": 20, "cost_cap_usd": 5,
               "lanes": [lane("a", "rank_a", "rank.py", cls.shim), lane("b", "rank_b", "rank.py", cls.venv_python),
                         lane("m", "rank_a", "model.py", sys.executable, cls.helper),
                         {"name": "c", "probe": {"command": [sys.executable, cls.flaky, "--x"],
                                                 "args": {"key": "rank_a", "fail_repo": "repos/i3"}}}],
               "grader": {"kind": "command", "command": [sys.executable, "grader.py"]},
               "decision_rule": {"kind": "descriptive"}}
        cls.exp_path = os.path.join(folder, "experiment.json")
        common.write_json(cls.exp_path, exp)
        hosts = os.path.join(cls.tmp, "hosts.json")
        common.write_json(hosts, {"local": {"target": "local", "slots": 1}})
        cls.run_dir = os.path.join(cls.tmp, "run")
        cls.call("lanes-plan", cls.exp_path, "--run-dir", cls.run_dir)
        cls.call("lanes-run", cls.run_dir, "--hosts", hosts, "--skip-preflight")
        cls.bench = os.path.join(cls.tmp, "bench")
        make_bench(cls.bench)
        cls.out = os.path.join(cls.bench, "rounds", ROUND)
        cls.exported = cls.export()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    @classmethod
    def call(cls, name, *args):
        r = subprocess.run([sys.executable, os.path.join(BIN, name), *args], env=cls.env, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        return r

    @classmethod
    def export(cls, *extra):
        return subprocess.run([sys.executable, os.path.join(BIN, "lanes-export"), cls.run_dir, "--round-id", ROUND, "--out", cls.out,
                               "--date", "2026-10-24", "--check", "round", *extra], capture_output=True, text=True, env=cls.env)

    def records(self):
        return [json.loads(l) for l in read(os.path.join(self.out, "records.jsonl")).splitlines()]

    def reproduce(self, *extra, **env):
        return subprocess.run(["sh", REPRODUCE, self.out, *extra], capture_output=True, text=True, env={**self.env, **env})

    def test_export_passes_strict_validation_with_a_record_per_cell(self):
        self.assertEqual(self.exported.returncode, 0, self.exported.stdout + self.exported.stderr)
        self.assertIn("PASS WITH DECLARED DEVIATIONS", self.exported.stdout)
        recs = self.records()
        self.assertEqual(len(recs), 3 * 4 * 2 - 2)  # items x lanes x reps, less lane c on i3 (it exits 2 there, see EXCLUDED.json)
        m = next(r for r in recs if r["arm"] == "m")
        self.assertEqual(m["tokens"]["total"], {"input": 10, "cached_input": 0, "output": 5, "reasoning": 0})
        self.assertGreater(m["cost"]["usd"], 0)
        a = next(r for r in recs if r["arm"] == "a")
        self.assertEqual(a["cost"]["usd"], 0)
        self.assertIsInstance(a["timing"]["total_wall_s"], float)

    def test_bundle_has_cpu_rss_and_metrics_per_cell(self):
        att = glob.glob(os.path.join(self.out, "bundles", ROUND, "attempts", "i1", "r1", "a", "a1", "attempt.json"))[0]
        attempt = common.read_json(att)
        for k in ("wall_s", "cpu_s", "peak_rss_kb", "usage", "totals"):
            self.assertIn(k, attempt)
        ev = common.read_json(os.path.join(os.path.dirname(att), "evaluation.json"))
        self.assertEqual(ev["metrics"]["listed"], 3)

    def test_commands_and_corpus_hash_are_published(self):
        plan = common.read_json(os.path.join(self.out, "PLAN.json"))
        cmds = common.read_json(os.path.join(self.out, "commands.json"))
        self.assertEqual(plan["hashes"]["corpus"]["tree"], common.sha256_tree(self.corpus))
        for name, c in cmds["lanes"].items():
            self.assertEqual(c["command_sha256"], export.plan_hashes.sha256_json(c["argv"]), name)
            for f in c["files"].values():
                self.assertEqual(common.sha256_file(os.path.join(self.out, f["path"])), f["sha256"])
        self.assertTrue(cmds["lanes"]["m"]["files"])
        self.assertIn(cmds["lanes"]["a"]["command_sha256"], read(os.path.join(self.out, "README.md")))
        self.assertTrue(cmds["grader"]["files"])
        self.assertNotIn(self.tmp, read(os.path.join(self.out, "commands.json")))

    def test_absolute_script_is_copied_and_the_interpreter_named_with_its_version(self):
        c = common.read_json(os.path.join(self.out, "commands.json"))["lanes"]["c"]
        plan = common.read_json(os.path.join(self.out, "PLAN.json"))
        self.assertEqual(c["files"]["1"]["path"], "commands/c/1/flaky.py")
        self.assertEqual(common.sha256_file(os.path.join(self.out, "commands", "c", "1", "flaky.py")), c["files"]["1"]["sha256"])
        self.assertEqual(c["files"]["1"]["sha256"], plan["hashes"]["lanes"]["c"]["files"]["1"])
        self.assertEqual(c["argv"][1:], ["commands/c/1/flaky.py", "--x"])
        self.assertEqual(c["external"]["0"]["name"], os.path.basename(sys.executable))
        self.assertRegex(c["external"]["0"]["version"], r"^Python 3")
        self.assertIn("commands/c/1/flaky.py", read(os.path.join(self.out, "README.md")))

    def test_interpreters_are_named_and_scripts_copied_wherever_they_live(self):
        lanes = common.read_json(os.path.join(self.out, "commands.json"))["lanes"]
        for name in ("a", "b"):  # the CI toolcache shim and the venv python
            self.assertEqual(lanes[name]["external"]["0"]["name"], "python3", name)
            self.assertRegex(lanes[name]["external"]["0"]["version"], r"^Python 3", name)
            self.assertEqual(sorted(lanes[name]["files"]), ["1"], name)
        self.assertEqual(lanes["m"]["external"]["2"]["name"], "helper")  # a binary, though not named like an interpreter
        self.assertFalse(os.path.exists(os.path.join(self.out, "commands", "m", "2")))
        self.assertFalse(os.path.exists(os.path.join(self.out, "commands", "a", "0")))
        self.assertEqual(lanes["c"]["files"]["1"]["path"], "commands/c/1/flaky.py")  # the script under ~/anything

    def test_classification_is_by_file_type_not_folder(self):
        folder = os.path.join(self.tmp, "kinds", "usr", "local", "share")
        os.makedirs(folder)
        elf, script, named = (os.path.join(folder, n) for n in ("tool", "probe.py", "node"))
        with open(elf, "wb") as f:
            f.write(b"\x7fELF" + bytes(60))
        with open(script, "w") as f:
            f.write("#!/usr/bin/env python3\nprint(1)\n")
        shutil.copyfile(script, named)
        self.assertTrue(export.is_interpreter(1, elf, elf))
        self.assertFalse(export.is_interpreter(0, script, script))  # a script under a system-like folder is copied
        self.assertTrue(export.is_interpreter(0, named, named))
        self.assertEqual(export.is_interpreter(0, "python3", "python3"), shutil.which("python3") is not None)
        self.assertFalse(export.is_interpreter(1, "--flag", "--flag"))

    def test_failed_cells_are_excluded_and_counted_by_outcome(self):
        excluded = common.read_json(os.path.join(self.out, "bundles", ROUND, "EXCLUDED.json"))["excluded"]
        self.assertEqual(sorted(e["cell"] for e in excluded), ["i3/r1/c", "i3/r2/c"])
        self.assertTrue(all(e["reason"] == "cell outcome exit_2, not graded" for e in excluded))
        self.assertIn("| c | 6 | 4 | exit_2 2 |", read(os.path.join(self.out, "README.md")))

    def test_cost_keeps_its_digits_and_probe_phases_say_no_kogen(self):
        row = next(l for l in read(os.path.join(self.out, "README.md")).splitlines() if l.startswith("| m | cost_usd |"))
        self.assertNotIn("0.0000", row)
        self.assertRegex(row, r"\| m \| cost_usd \| \d\.\d+e-0\d ")
        rec = next(r for r in self.records() if r["arm"] == "m")
        self.assertEqual(rec["tokens"]["phases"]["shape"]["input"], {"not_applicable": "A probe runs no Kogen."})
        self.assertEqual(rec["timing"]["phases_s"]["shape"], {"not_applicable": "A probe runs no Kogen."})

    def test_results_table_has_intervals_per_lane_and_metric(self):
        readme = read(os.path.join(self.out, "README.md"))
        self.assertIn("| Lane | Metric | Mean | 95% interval (items) |", readme)
        rows = [l for l in readme.splitlines() if l.startswith("| a | listed |")]
        self.assertEqual(len(rows), 1)
        self.assertRegex(rows[0], r"\[-?\d\.\d{4}, -?\d\.\d{4}\]")
        self.assertIn("listed", common.read_json(os.path.join(self.out, "results.json"))["lanes"][0]["metrics"])

    def test_export_refuses_a_command_file_changed_since_the_plan(self):
        bad = os.path.join(self.tmp, "bad-bench")
        make_bench(bad)
        with open(os.path.join(os.path.dirname(self.exp_path), "rank.py"), "a") as f:
            f.write("# changed\n")
        try:
            r = subprocess.run([sys.executable, os.path.join(BIN, "lanes-export"), self.run_dir, "--round-id", ROUND, "--out",
                                os.path.join(bad, "rounds", ROUND), "--check", "none"], capture_output=True, text=True, env=self.env)
        finally:
            path = os.path.join(os.path.dirname(self.exp_path), "rank.py")
            with open(path) as f:
                text = f.read()
            with open(path, "w") as f:
                f.write(text.replace("# changed\n", ""))
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("changed since the plan", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(bad, "rounds", ROUND)))


    @unittest.skipUnless(os.environ.get("KOGEN_LANES_FULL_VALIDATE"), "set KOGEN_LANES_FULL_VALIDATE=1 (full checkout, minutes)")
    def test_release_gate_on_a_full_checkout(self):
        bench = os.path.join(self.tmp, "full")
        os.makedirs(bench)
        archive = subprocess.Popen(["git", "archive", "HEAD"], cwd=REPO, stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", bench, "--exclude", "lanes"], stdin=archive.stdout, check=True)
        archive.stdout.close()
        archive.wait()
        os.makedirs(os.path.join(bench, "lanes"))  # rounds link to it
        shutil.copyfile(os.path.join(REPO, "lanes", "README.md"), os.path.join(bench, "lanes", "README.md"))
        subprocess.run(["git", "init", "-q"], cwd=bench, check=True)
        subprocess.run(["git", "add", "-A"], cwd=bench, check=True)
        r = subprocess.run([sys.executable, os.path.join(BIN, "lanes-export"), self.run_dir, "--round-id", ROUND, "--out",
                            os.path.join(bench, "rounds", ROUND), "--date", "2026-10-24", "--check", "release"],
                           capture_output=True, text=True, env=self.env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("RELEASE GATE: PASS", r.stdout)

    def test_publish_private_then_reproduce(self):
        wrong = os.path.join(self.tmp, "wrong")
        shutil.copytree(self.corpus, wrong)
        with open(os.path.join(wrong, "items.jsonl"), "a") as f:
            f.write("\n")
        r = self.export("--publish-private", "--corpus", wrong)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("private inputs differ", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.out, "reproduce")))
        r = self.export("--publish-private", "--corpus", self.corpus)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        plan = common.read_json(os.path.join(self.out, "PLAN.json"))
        self.assertIs(plan["publication"]["closed"], True)
        self.assertIn("reproduce/corpus/items.jsonl", plan["publication"]["files"])
        self.assertEqual(common.sha256_tree(os.path.join(self.out, "reproduce", "corpus")), plan["hashes"]["corpus"]["tree"])
        r = self.reproduce()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("lanes without model usage a, b, c", r.stdout)
        self.assertIn("external m: helper is not on this machine's PATH", r.stdout)
        self.assertIn("re-grades and step-0 reruns match", r.stdout)
        self.assertIn("i1/r1/a: metrics match", r.stdout)
        self.assertNotIn("i1/r1/m:", r.stdout)  # a lane with usage is only re-graded unless --rerun
        r = self.reproduce("--rerun", "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"i\d/r\d/m: metrics match \(model lane")
        # a changed published command file, a changed output and a changed published grade are each caught
        path = os.path.join(self.out, "commands", "a", "1", "rank.py")
        for target, edit in ((path, lambda t: t + "# x\n"),
                             (os.path.join(self.out, "reproduce", "corpus", "items.jsonl"), lambda t: t + "\n"),
                             (os.path.join(self.out, "reproduce", "cells", "i1", "r1", "a", "output.json"),
                              lambda t: json.dumps({"ranked": []})),
                             (glob.glob(os.path.join(self.out, "bundles", "*", "attempts", "i1", "r1", "b", "a1", "evaluation.json"))[0],
                              lambda t: t.replace('"listed": 3', '"listed": 4'))):
            before = read(target)
            with open(target, "w") as f:
                f.write(edit(before))
            r = self.reproduce()
            with open(target, "w") as f:
                f.write(before)
            self.assertEqual(r.returncode, 1, (target, r.stdout))
            self.assertIn("MISMATCH", r.stdout)
        self.assertEqual(self.reproduce().returncode, 0)
        self.assertRegex(self.reproduce().stdout, r"external c: python\S* version matches the published one")
        # a rerun that fails shows its outcome; an edited flag in commands.json with a recomputed sha is caught
        r = self.reproduce(PROBE_BREAK="1")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("i1/r1/c: rerun exit_2", r.stdout)
        path = os.path.join(self.out, "commands.json")
        before = read(path)
        doc = json.loads(before)
        doc["lanes"]["c"]["argv"][2] = "--y"
        doc["lanes"]["c"]["command_sha256"] = export.plan_hashes.sha256_json(doc["lanes"]["c"]["argv"])
        with open(path, "w") as f:
            json.dump(doc, f)
        r = self.reproduce()
        with open(path, "w") as f:
            f.write(before)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("MISMATCH commands.json (c: element 2 is '--y', PLAN.json has '--x')", r.stdout)
        self.assertEqual(self.reproduce().returncode, 0)


if __name__ == "__main__":
    unittest.main()
