"""The release gate allows hidden tests only in the evaluator folder of a closed, hash-matching round."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import published_hidden
from published_hidden import allowed, plan_publication_spans, sha256_file, sha256_tree

HIDDEN = "files/.lab-eval/test_hidden.py"


class PublishedHiddenTests(unittest.TestCase):
    def setUp(self):
        published_hidden._cache.clear()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.round = self.root / "rounds" / "r1"
        self.evaluator = self.round / "reproduce" / "tasks" / "t1" / "evaluator"
        self.hidden = self.evaluator / HIDDEN
        self.hidden.parent.mkdir(parents=True)
        self.hidden.write_text("def test_x():\n    assert True\n")
        (self.evaluator / "evaluate.toml").write_text("overlay = 'files'\n")

    def plan(self, closed=True, tree=None, files=None):
        rel = "reproduce/tasks/t1/evaluator/"
        plan = {"hashes": {"tasks": {"t1": {"hidden_tests": tree or sha256_tree(self.evaluator)}}}}
        if closed is not None:
            plan["publication"] = {"closed": closed, "closed_at": "2026-10-23T00:00:00Z",
                                   "files": files if files is not None else {rel + HIDDEN: sha256_file(self.hidden)}}
        (self.round / "PLAN.json").write_text(json.dumps(plan))
        published_hidden._cache.clear()

    def test_allowed_when_closed_and_hashes_match(self):
        self.plan()
        self.assertTrue(allowed(self.hidden, self.root))

    def test_blocked_when_the_file_differs_from_the_pre_run_hash(self):
        self.plan()
        self.hidden.write_text("def test_x():\n    assert False\n")
        self.assertFalse(allowed(self.hidden, self.root))

    def test_blocked_when_the_tree_hash_differs(self):
        self.plan(tree="0" * 64)
        self.assertFalse(allowed(self.hidden, self.root))

    def test_blocked_when_the_round_is_not_closed(self):
        self.plan(closed=False)
        self.assertFalse(allowed(self.hidden, self.root))
        self.plan(closed=None)
        self.assertFalse(allowed(self.hidden, self.root))

    def test_blocked_when_the_file_is_not_listed(self):
        self.plan(files={})
        self.assertFalse(allowed(self.hidden, self.root))

    def test_blocked_elsewhere_in_the_round_or_repo(self):
        self.plan()
        for rel in ("rounds/r1/test_hidden.py", "rounds/r1/reproduce/tasks/t1/reference/test_hidden.py",
                    "rounds/r1/reproduce/tasks/t1/test_hidden.py", "tasks/t1/test_hidden.py", "test_hidden.py"):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.hidden.read_text())
            self.assertFalse(allowed(path, self.root), rel)

    def test_other_sensitive_names_and_sealed_paths_stay_blocked(self):
        for rel in ("files/auth.json", "files/grade.sh", "files/transcript.jsonl", "files/solution.patch",
                    "files/sealed/test_hidden.py", "files/author-private/test_hidden.py", "files/author_private/test_hidden.py"):
            path = self.evaluator / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x\n")
        self.plan()
        listed = {"reproduce/tasks/t1/evaluator/" + p.relative_to(self.evaluator).as_posix(): sha256_file(p)
                  for p in self.evaluator.rglob("*") if p.is_file()}
        self.plan(files=listed)
        for p in self.evaluator.rglob("*"):
            if p.is_file():
                self.assertEqual(allowed(p, self.root), p.name == "test_hidden.py" and "sealed" not in p.parts
                                 and "author-private" not in p.parts and "author_private" not in p.parts, str(p))

    def scan_text(self, files, closed=True, extra=""):
        return json.dumps({"hashes": {}, "note": extra, "publication": {"closed": closed, "files": files}}, sort_keys=True)

    def covered(self, text, rel="rounds/r1/PLAN.json"):
        """The test_hidden.py mentions of `text` that no allowed span covers."""
        spans = plan_publication_spans(text, rel)
        return [m.start() for m in __import__("re").finditer(r"test_hidden\.py", text)
                if not any(a <= m.start() and m.end() <= b for a, b in spans)]

    def test_plan_scan_exempts_only_the_listed_evaluator_paths_of_a_closed_round(self):
        key = "reproduce/tasks/t1/evaluator/" + HIDDEN
        self.assertEqual(self.covered(self.scan_text({key: "0" * 64})), [])
        self.assertTrue(self.covered(self.scan_text({key: "0" * 64}, extra="see test_hidden.py")))
        self.assertTrue(self.covered(self.scan_text({key: "0" * 64}, closed=False)))
        self.assertTrue(self.covered(self.scan_text({"reproduce/tasks/t1/reference/test_hidden.py": "0" * 64})))
        self.assertTrue(self.covered(self.scan_text({"reproduce/tasks/t1/evaluator/../x/test_hidden.py": "0" * 64})))
        self.assertTrue(self.covered(self.scan_text({key: "0" * 64}), rel="rounds/r1/README.md"))
        self.assertTrue(self.covered(self.scan_text({key: "0" * 64}), rel="PLAN.json"))
        self.assertTrue(self.covered("not json test_hidden.py"))

    def test_blocked_for_a_symlink(self):
        self.plan()
        link = self.evaluator / "files" / "test_hidden.py"
        os.symlink(self.hidden, link)
        self.assertFalse(allowed(link, self.root))


if __name__ == "__main__":
    unittest.main()
