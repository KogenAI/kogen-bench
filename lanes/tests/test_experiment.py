import json
import os
import subprocess
import sys
import tempfile
import unittest

from lanes import experiment

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
GOOD = os.path.join(FIX, "experiment-good.json")


def good():
    with open(GOOD) as f:
        return json.load(f)


class Validate(unittest.TestCase):
    def test_good_file_loads(self):
        exp = experiment.load(GOOD)
        self.assertEqual(exp["id"], "exp-mini")
        lane = exp["lanes"][1]
        self.assertTrue(experiment.patch_path(GOOD, lane).endswith("fixtures/patches/p1.patch"))
        self.assertIsNone(experiment.patch_path(GOOD, exp["lanes"][0]))

    def bad(self, field, mutate):
        exp = good()
        mutate(exp)
        with self.assertRaises(experiment.ExperimentError) as cm:
            experiment.validate(exp)
        self.assertIn(field, str(cm.exception))

    def test_each_bad_field(self):
        cases = [
            ("id", lambda e: e.pop("id")),
            ("id", lambda e: e.update(id="a/b")),
            ("phase", lambda e: e.update(phase="deploy")),
            ("kogen.repo", lambda e: e.update(kogen={})),
            ("lanes", lambda e: e.update(lanes=[])),
            ("lanes", lambda e: e["lanes"][1].update(name="base")),
            ("lanes[0].sha", lambda e: e["lanes"][0].update(sha="abc")),
            ("lanes[0].sha", lambda e: e["lanes"][0].update(sha="A" * 40)),
            ("lanes[0].patch", lambda e: e["lanes"][0].pop("patch")),
            ("lanes[1].patch", lambda e: e["lanes"][1].update(patch="/abs/p.patch")),
            ("lanes[1].patch", lambda e: e["lanes"][1].update(patch="../p.patch")),
            ("lanes[0].settings", lambda e: e["lanes"][0].pop("settings")),
            ("lanes[0].settings.models.build", lambda e: e["lanes"][0]["settings"]["models"].update(build="gpt")),
            ("tasks", lambda e: e.update(tasks=[])),
            ("tasks", lambda e: e.update(tasks=["a", "a"])),
            ("reps", lambda e: e.update(reps=0)),
            ("reps", lambda e: e.update(reps=True)),
            ("deadline_s", lambda e: e.update(deadline_s=-1)),
            ("deadline_s", lambda e: e.update(deadline_s=float("nan"))),
            ("deadline_s", lambda e: e.update(deadline_s=float("inf"))),
            ("intent_form", lambda e: e.pop("intent_form")),
            ("intent_form", lambda e: e.update(intent_form="yaml")),
            ("intent_form", lambda e: e.update(phase="shape", intent_form="yaml")),
            ("hosts[0]", lambda e: e.update(hosts=["bad host"])),
            ("tasks[0]", lambda e: e.update(tasks=["../x"])),
            ("hosts", lambda e: e.update(hosts="local")),
            ("decision_rule", lambda e: e.pop("decision_rule")),
            ("decision_rule.kind", lambda e: e.update(decision_rule={})),
        ]
        for field, mutate in cases:
            with self.subTest(field=field):
                self.bad(field, mutate)

    def test_intent_form_only_needed_for_build(self):
        for phase in ("shape", "e2e"):
            exp = good()
            exp["phase"] = phase
            del exp["intent_form"]
            experiment.validate(exp)
        for form in experiment.INTENT_FORMS:
            exp = good()
            exp["intent_form"] = form
            experiment.validate(exp)

    def test_not_json_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.json")
            with open(p, "w") as f:
                f.write("{nope")
            with self.assertRaises(experiment.ExperimentError):
                experiment.load(p)
            with self.assertRaises(experiment.ExperimentError):
                experiment.load(os.path.join(d, "missing.json"))

    def test_entry_point_exit_2(self):
        code = (
            "import sys;sys.path.insert(0,%r)\n"
            "from lanes import experiment\n"
            "experiment.load_or_exit(%r)\n"
        ) % (os.path.dirname(FIX.rstrip("/")) + "/..", os.path.join(FIX, "missing.json"))
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("experiment error", r.stderr)


if __name__ == "__main__":
    unittest.main()
