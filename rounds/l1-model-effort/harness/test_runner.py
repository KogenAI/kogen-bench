#!/usr/bin/env python3
"""Runner metric checks using synthetic receipts and interrupted command events."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('runner',Path(__file__).with_name('l1_runner.py'))
runner=importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)

class Metrics(unittest.TestCase):
    def test_cumulative_receipts_duplicates_resume_reset_missing_fields(self):
        values=[(1,dict(input_tokens=100,output_tokens=10)),(2,dict(input_tokens=100,output_tokens=10)),
                (3,dict(input_tokens=180,output_tokens=15)),(4,dict(input_tokens=30,output_tokens=5))]
        totals,count=runner.usage_rows(values+values[-1:])
        self.assertEqual(totals['input_tokens'],210)
        self.assertEqual(totals['output_tokens'],20)
        self.assertEqual(totals['reasoning_output_tokens'],'NA')
        self.assertEqual(count,4)

    def test_proxy_counts_once_and_clips_unfinished_at_cap(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); out=root/'out/go'; out.mkdir(parents=True)
            rows=[dict(type='item.started',item=dict(id='a',type='command_execution',command='go build ./...')),
                  dict(type='item.completed',item=dict(id='a',type='command_execution',command='go build ./...',exit_code=0)),
                  dict(type='item.started',item=dict(id='b',type='command_execution',command='go test ./...'))]
            (out/'turn-0.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
            (out/'turn-0.ts').write_text('10\tx\n14\tx\n18\tx\n')
            stats=runner.stream_stats(root,'go',20)
            self.assertEqual(stats['build_test_proxy']['count'],2)
            self.assertEqual(stats['build_test_proxy']['duration_seconds'],6)
            self.assertEqual(stats['build_test_proxy']['unfinished_clipped'],1)
            self.assertEqual(stats['successful_commands'],1)

    def test_quota_detector_ignores_assistant_text(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); out=root/'out/ex'; out.mkdir(parents=True)
            (out/'turn-0.jsonl').write_text(json.dumps(dict(type='item.completed',item=dict(type='agent_message',text='quota reached')))+'\n')
            self.assertEqual(runner.refusal(root,'ex',{}),[])
            with (out/'turn-0.jsonl').open('a') as f:
                f.write(json.dumps(dict(type='error',message='429 usage limit reached'))+'\n')
            self.assertEqual(len(runner.refusal(root,'ex',{})),1)

if __name__=='__main__': unittest.main()
