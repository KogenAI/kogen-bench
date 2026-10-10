import json
import os
import tempfile
import unittest

import audit_cell


def command_event(command, output="", event_type="item.completed", item_id="i1"):
    return {
        "type": event_type,
        "item": {
            "id": item_id,
            "type": "command_execution",
            "command": command,
            "aggregated_output": output,
        },
    }


class AuditCellTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.results = os.path.join(self.temp_dir.name, "results")
        os.makedirs(self.results)

    def counts(self, lines):
        run_dir = os.path.join(self.results, "run")
        os.makedirs(run_dir)
        path = os.path.join(run_dir, "codex.jsonl")
        with open(path, "w", encoding="utf-8") as stream:
            for line in lines:
                if isinstance(line, str):
                    stream.write(line + "\n")
                else:
                    stream.write(json.dumps(line) + "\n")
        result = audit_cell._run_counts(path)
        self.assertIsNotNone(result)
        return result

    def test_github_only_in_output_is_descriptive(self):
        result = self.counts([command_event("printf ok", "found github.com here")])
        self.assertEqual(result["flagged"], 0)
        self.assertEqual(result["output_mentions_github"], 1)

    def test_wrapped_curl_positive(self):
        result = self.counts([command_event("bash -lc 'curl -sL https://github.com/x/y'")])
        self.assertGreaterEqual(result["flagged"], 1)
        self.assertEqual(result["cmd_fetch"], 1)

    def test_git_clone_ssh_positive(self):
        result = self.counts([command_event("git clone ssh://github.com/x/y.git")])
        self.assertGreaterEqual(result["flagged"], 1)
        self.assertEqual(result["cmd_fetch"], 1)

    def test_web_search_item_positive(self):
        result = self.counts([{
            "type": "item.completed",
            "item": {"id": "w", "type": "web_search", "query": "x"},
        }])
        self.assertEqual(result["web_search"], 1)
        self.assertEqual(result["flagged"], 1)

    def test_loopback_curls_are_not_flagged(self):
        result = self.counts([
            command_event("curl http://localhost:4000/health", item_id="local1"),
            command_event("curl -s http://localhost:4000", item_id="local2"),
        ])
        self.assertEqual(result["flagged"], 0)
        self.assertEqual(result["cmd_url"], 0)

    def test_build_and_test_commands_are_not_flagged(self):
        result = self.counts([
            command_event("cargo build", item_id="cargo"),
            command_event("mix test", item_id="mix"),
            command_event("go build ./...", item_id="go"),
            command_event("bun test", item_id="bun"),
        ])
        self.assertEqual(result["flagged"], 0)

    def test_unparsable_line_counted(self):
        result = self.counts(["{not json"])
        self.assertEqual(result["unparsable"], 1)
        self.assertEqual(result["flagged"], 0)

    def test_started_and_completed_same_id_count_once(self):
        result = self.counts([
            command_event("curl https://example.org", event_type="item.started", item_id="same"),
            command_event("curl https://example.org", event_type="item.completed", item_id="same"),
        ])
        self.assertEqual(result["cmd_fetch"], 1)
        self.assertEqual(result["cmd_url"], 1)
        self.assertEqual(result["flagged"], 2)


if __name__ == "__main__":
    unittest.main()
