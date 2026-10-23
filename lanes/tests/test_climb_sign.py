import copy
import unittest
from fractions import Fraction

from lanes import experiment, report
from tests.test_climb import climb, many, run_dir

GOLDEN_LINE = (
    "Rule keep_revert (candidate vs baseline, min_effect 0.1): KEEP [improved_both]: train and test both improved "
    "by more than min_effect with intervals above zero; pass-rate differences (task unit, Hoeffding 95%) vs "
    "min_effect 0.1: train +0.67 [0.17, 1.00] (30 tasks, 30 pairs, candidate-better 20, baseline-better 0); "
    "test +0.67 [0.17, 1.00] (30 tasks, 30 pairs, candidate-better 20, baseline-better 0)")


def sign(max_p=0.05):
    return lambda e: e["decision_rule"].update(improves={"test": "task_sign", "max_p": max_p})


class SignP(unittest.TestCase):
    def test_exact_tails(self):
        tail = lambda k, n: report.task_sign_p({"candidate_better": k, "baseline_better": n - k})[2]
        self.assertEqual(tail(1, 1), Fraction(1, 2))
        self.assertEqual(tail(5, 5), Fraction(1, 32))
        self.assertEqual(tail(4, 5), Fraction(6, 32))
        self.assertEqual(tail(3, 5), Fraction(1, 2))
        self.assertEqual(tail(8, 10), Fraction(56, 1024))
        self.assertEqual(tail(0, 4), Fraction(1))
        self.assertEqual(tail(0, 0), Fraction(1))

    def test_ties_are_dropped(self):
        k, n, p = report.task_sign_p({"candidate_better": 3, "baseline_better": 0, "tied": 7})
        self.assertEqual((k, n, p), (3, 3, Fraction(1, 8)))


class Default(unittest.TestCase):
    def test_absent_field_keeps_the_hoeffding_line_and_shape(self):
        base, cand = many(5, 25, 5, 25)
        v = report.report(run_dir(self, base, cand))["verdict"]
        self.assertEqual(v["line"], GOLDEN_LINE)
        self.assertEqual(v["params"], {})
        self.assertNotIn("sign", v)

    def test_default_path_still_needs_the_interval(self):
        base, cand = many(0, 6, 0, 6, n=6)  # all 6 tasks better: sign p 1/64, but Hoeffding spans zero
        self.assertEqual(report.report(run_dir(self, base, cand))["verdict"]["case"], "within_noise")


class Verdicts(unittest.TestCase):
    def verdict(self, *counts, n=30, mut=None):
        base, cand = many(*counts, n=n)
        return report.report(run_dir(self, base, cand, exp_mut=mut or sign()))["verdict"]

    def test_keep(self):
        v = self.verdict(5, 25, 5, 25)
        self.assertEqual((v["decision"], v["case"]), ("keep", "improved_both"))
        self.assertIn("sign test 20/20 tasks candidate-better, p 0.0000", v["line"])
        self.assertIn("improves task_sign max_p 0.05", v["line"])
        self.assertEqual(v["sign"]["train"]["k"], 20)
        self.assertEqual(v["sign"]["test"]["n"], 20)

    def test_sign_test_keeps_where_hoeffding_cannot(self):
        v = self.verdict(0, 6, 0, 6, n=6)  # 6 of 6 tasks better: p 1/64
        self.assertEqual((v["decision"], v["case"]), ("keep", "improved_both"))
        self.assertIn("sign test 6/6 tasks candidate-better, p 0.0156", v["line"])

    def test_overfit(self):
        v = self.verdict(5, 25, 15, 15)
        self.assertEqual((v["decision"], v["case"]), ("revert", "overfit"))
        self.assertIn("sign test 0/0 tasks candidate-better, p 1.0000", v["line"])

    def test_any_drop_reverts(self):
        for counts in ((15, 25, 15, 14), (15, 14, 15, 15)):
            v = self.verdict(*counts)
            self.assertEqual((v["decision"], v["case"]), ("revert", "drop"))

    def test_within_noise(self):
        v = self.verdict(0, 1, 0, 1, n=5)  # +0.2 above min_effect, but 1 of 1 tasks: p 0.5
        self.assertEqual((v["decision"], v["case"]), ("within_noise", "within_noise"))
        self.assertEqual(self.verdict(15, 15, 15, 15)["case"], "within_noise")

    def test_gain_must_beat_min_effect_as_well(self):
        v = self.verdict(5, 25, 5, 25, mut=lambda e: (sign()(e), e.update(min_effect=0.9)))
        self.assertEqual(v["case"], "within_noise")

    def test_max_p_is_inclusive(self):
        self.assertEqual(self.verdict(0, 5, 0, 5, n=5, mut=sign(0.03125))["case"], "improved_both")  # p = 1/32
        self.assertEqual(self.verdict(0, 5, 0, 5, n=5, mut=sign(0.03))["case"], "within_noise")

    def test_ties_do_not_count_against_the_sign_test(self):
        # 3 of 30 tasks better, 27 tied: n = 3, p 1/8 (a 0.1 gain is exactly min_effect anyway)
        v = self.verdict(0, 3, 0, 3, mut=sign(0.2))
        self.assertIn("sign test 3/3 tasks", v["line"])
        self.assertEqual(v["sign"]["train"], {"k": 3, "n": 3, "p": 0.125})

    def test_incomplete(self):
        base, cand = many(5, 25, 5, 25, n=3)
        endings = {f"b{i}/r1/candidate": "host_lost" for i in (1, 2, 3)}
        v = report.report(run_dir(self, base, cand, endings=endings, exp_mut=sign()))["verdict"]
        self.assertEqual(v["decision"], "incomplete")


class Validate(unittest.TestCase):
    def bad(self, improves):
        exp = climb()
        exp["decision_rule"]["improves"] = improves
        with self.assertRaises(experiment.ExperimentError) as cm:
            experiment.validate(exp)
        self.assertIn("decision_rule.improves", str(cm.exception))

    def test_good(self):
        exp = climb()
        exp["decision_rule"]["improves"] = {"test": "task_sign", "max_p": 0.1}
        experiment.validate(exp)
        exp["decision_rule"]["improves"]["max_p"] = 1e-9
        experiment.validate(copy.deepcopy(exp))

    def test_bad(self):
        for improves in ("task_sign", None, [], {}, {"test": "task_sign"}, {"max_p": 0.1},
                         {"test": "paired_sign", "max_p": 0.1}, {"test": "task_sign", "max_p": 0.1, "x": 1},
                         {"test": "task_sign", "max_p": 0}, {"test": "task_sign", "max_p": 1},
                         {"test": "task_sign", "max_p": 1.5}, {"test": "task_sign", "max_p": -0.1},
                         {"test": "task_sign", "max_p": True}, {"test": "task_sign", "max_p": "0.05"},
                         {"test": "task_sign", "max_p": float("nan")}):
            self.bad(improves)


if __name__ == "__main__":
    unittest.main()
