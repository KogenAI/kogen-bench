import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import standard_record, validate_round
import cost_calc

SNAPSHOT_SPEC=importlib.util.spec_from_file_location('lane_snapshot',HERE/'lane-snapshot.py')
lane_snapshot=importlib.util.module_from_spec(SNAPSHOT_SPEC)
SNAPSHOT_SPEC.loader.exec_module(lane_snapshot)


class SyntheticHost:
    @staticmethod
    def system(): return 'Linux'
    @staticmethod
    def release(): return 'synthetic-kernel'
    @staticmethod
    def machine(): return 'x86_64'
    @staticmethod
    def freedesktop_os_release(): return {'PRETTY_NAME':'Synthetic Linux'}


class StandardRecordTests(unittest.TestCase):
    def plan_fixture(self):
        return {'cells':[{
            'round_id':'synthetic','audit_round':'synthetic','cell_id':'synthetic-cell',
            'arm':'arm-synthetic','harness':'codex','harness_version':'codex-cli 0.160.0',
            'recipe':'recipe-v1','task':'synthetic-task','model':'gpt-6-luna','effort':'high',
            'effective_effort':'high','effective_model':'gpt-6-luna',
            'itt':{'class':'counted','cohort':'scored','evidence_ref':'rounds/synthetic/ITT.md'},
            'repetition':1,'base_repo':'github.com/kogen/synthetic-task',
            'base_revision':{'kind':'git-commit','hash':'a'*40},
            'launcher_sha256':'b'*64,'adapter_harness_sha':'c'*64,
            'deps_source':'task-derived','ledger_sha256':'d'*64,
            'kogen_sha':'e'*64,'source_ref':'rounds/synthetic/README.md',
        }]}

    def make_snapshot(self, root):
        bindir=root/'fake-bin'; bindir.mkdir()
        for command,_pin in lane_snapshot.SPECS.values():
            exe=bindir/command[0]
            if not exe.exists():
                exe.write_text('#!/bin/sh\nexit 0\n'); exe.chmod(0o755)
        codex=bindir/'codex'; codex.write_text('#!/bin/sh\nexit 0\n'); codex.chmod(0o755)
        proc=root/'proc'; proc.mkdir()
        (proc/'meminfo').write_text('MemTotal:       8388608 kB\nMemAvailable:   4194304 kB\n')
        (proc/'cpuinfo').write_text('model name : Synthetic CPU\n')
        def command_runner(argv):
            if argv[0]==str(codex): return 'codex-cli 0.160.0'
            return {
                'python3':'Python 3.14.7','ruby':'ruby 3.4.8','elixir':'Elixir 1.20.2',
                'erl':'OTP 29','rustc':'rustc 1.97.1','node':'v24.20.0',
                'go':'go version go1.27.1','bun':'1.4.2','gleam':'1.18.1',
            }[argv[0]]
        old_path=os.environ.get('PATH','')
        try:
            os.environ['PATH']=str(bindir)
            return lane_snapshot.collect(standard_record.ROOT,venue='eu',account='owner',
                command_runner=command_runner,host_platform=SyntheticHost,core_count=8,
                proc_root=proc,codex_path=str(codex))
        finally:
            os.environ['PATH']=old_path

    def phase_receipt(self):
        start={'utc':'2026-10-09T12:00:00.000Z','monotonic_ns':1000000}
        end={'utc':'2026-10-09T12:00:01.000Z','monotonic_ns':1001000000}
        phases={'cell':{'start':start,'end':end}}
        for phase in ('setup','shape','plan','develop','review','gate','grade'):
            phases[phase]={'start':start,'end':end}
        return {'phases':phases,'attempts':[{'attempt':1,'start_utc':start['utc'],'end_utc':end['utc']}]}

    def sample_receipt(self,plan):
        return {
            'start':{'timestamp_utc':'2026-10-09T12:00:00Z','load1':0.2,'memory_available_kib':4000000,
                     'pressure':0,'running_bench_units':1,'cap':3600,'queue_position':2,
                     'dispatcher_id':plan['launcher_sha256']},
            'end':{'timestamp_utc':'2026-10-09T12:00:01Z','load1':0.3,'memory_available_kib':3999000,
                   'pressure':0,'running_bench_units':0,'cap':3600,'queue_position':2,
                   'dispatcher_id':plan['launcher_sha256']},
        }

    def make_result(self, root, events=None, privacy=False, snapshot_gap=False):
        result=root/'result'; result.mkdir()
        plan_path=root/'plan-input.json'; plan_path.write_text(json.dumps(self.plan_fixture()))
        resolved=subprocess.run([sys.executable,str(HERE/'lane-plan.py'),'--plan',str(plan_path),
            '--cell','synthetic-cell','--task','synthetic-task','--model','gpt-6-luna','--effort','high'],
            capture_output=True,text=True)
        self.assertEqual(resolved.returncode,0,resolved.stderr)
        plan=json.loads(resolved.stdout)
        (result/'plan.json').write_text(json.dumps(plan))
        (result/'launch-snapshot.json').write_text(json.dumps(self.make_snapshot(root)))
        snapshot=json.loads((result/'launch-snapshot.json').read_text())
        if snapshot_gap:
            snapshot['sandbox']['egress_profile']={'missing':'m14'}
            (result/'launch-snapshot.json').write_text(json.dumps(snapshot))
        manifest={
            'task':'synthetic-task','base_repo':'github.com/kogen/synthetic-task',
            'base_sha':'a'*40,'model':'gpt-6-luna','effective_model':'gpt-6-luna',
            'effort':'high','effective_effort':'high','runner_rc':0,'timeout_cap_s':3600,
            'kit_revision':'f'*40,'grader_sha256':'1'*64,'candidate_revision':'a'*40,
            'stall':False,'timeout':False,'patch_error':None,'capture_failures':[],
        }
        raw=(json.dumps(manifest,sort_keys=True)+'\n').encode()
        (result/'manifest.json').write_bytes(raw)
        (result/'manifest-sha256.txt').write_text(hashlib.sha256(raw).hexdigest()+'\n')
        (result/'grade.json').write_text(json.dumps({'pass_':True,'tests_ran':2}))
        (result/'lane-timing.json').write_text(json.dumps(self.phase_receipt()))
        (result/'boundary-samples.json').write_text(json.dumps(self.sample_receipt(plan)))
        if events is None:
            events=[{'type':'turn.completed','model':'gpt-6-luna','usage':{
                'input_tokens':100,'cached_input_tokens':20,'output_tokens':10,
                'reasoning_tokens':3,
            }}]
        (result/'codex.jsonl').write_text(''.join(json.dumps(event)+'\n' for event in events))
        if privacy:
            users='/'+'Users'
            home='/'+'home'
            at=chr(64)
            private_email='private'+at+'example.invalid'
            secret_email='secret'+at+'example.invalid'
            harness_email='example'+at+'example.invalid'
            receipt={'record':{
                'task':{'base_repo':users+'/private-user/work/'+private_email},
                'itt':{'evidence_ref':home+'/private-user/'+secret_email},
                'tools':{'harness':'harness at '+users+'/private-user/bin/'+harness_email},
            }}
            (result/'standard-receipts.json').write_text(json.dumps(receipt))
        return result

    def strict_validate(self, row, root):
        validator=root/'validator-root'; (validator/'schema').mkdir(parents=True)
        (validator/'results').mkdir(); (validator/'rounds'/'synthetic').mkdir(parents=True)
        (validator/'schema/run-record.schema.json').write_text((standard_record.ROOT/'schema/run-record.schema.json').read_text())
        (validator/'results/missing-reasons.json').write_text((standard_record.ROOT/'results/missing-reasons.json').read_text())
        for name in ('README.md','MEASURED.md'):
            (validator/'rounds/synthetic'/name).write_text('synthetic fixture\n')
        old_root,old_codes=validate_round.ROOT,validate_round.MISSING_CODES
        try:
            validate_round.ROOT=validator
            from missing_reasons import load_legend
            validate_round.MISSING_CODES=load_legend(validator/'results/missing-reasons.json')
            gaps=validate_round.gaps([row])
            fields={p:{'count':sum(counts.values()),'reasons':counts,'affects_verdict':'strict completion'} for p,counts in gaps.items()}
            declaration={'round':'synthetic','cells':1,'fields':fields,
                'gap_sources':validate_round.gap_sources([row]),
                'protocol_deviations':['synthetic incomplete receipt'] if gaps else []}
            (validator/'rounds/synthetic/MISSING.md').write_text('```json\n'+json.dumps(declaration)+'\n```\n')
            return validate_round.validate('synthetic',[row],strict=True)
        finally:
            validate_round.ROOT,validate_round.MISSING_CODES=old_root,old_codes

    def test_planned_fixture_with_no_prefilled_record_passes_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.make_result(Path(tmp))
            self.assertFalse((result/'standard-receipts.json').exists())
            row=standard_record.finalize(result)
            report=self.strict_validate(row,Path(tmp))
            self.assertEqual(report['missing'],0,report)
            self.assertFalse(report['errors'],report)
            self.assertTrue(report['strict_release_eligible'])
            self.assertEqual(row['effort']['effective'],'high')
            self.assertEqual(row['task']['base_repo'],'github.com/kogen/synthetic-task')
            self.assertEqual(row['task']['base_revision'],{'kind':'git-commit','hash':'a'*40})
            self.assertEqual(row['setup']['task_base'],row['task']['base_revision'])
            self.assertIn('go=',row['environment']['toolchains']['other_inventory'])
            self.assertIn('go=',row['tools']['toolchains']['other_inventory'])

    def test_receipt_gap_fails_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.make_result(Path(tmp),snapshot_gap=True)
            row=standard_record.finalize(result)
            report=self.strict_validate(row,Path(tmp))
            self.assertGreater(report['missing'],0)
            self.assertFalse(report['strict_release_eligible'])

    def test_record_redacts_home_paths_and_emails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.make_result(Path(tmp),privacy=True)
            standard_record.finalize(result)
            raw=(result/'standard.json').read_text()
            self.assertNotIn('/'+'Users'+'/private-user',raw)
            self.assertNotIn('/'+'home'+'/private-user',raw)
            self.assertNotIn('private'+chr(64)+'example.invalid',raw)
            self.assertNotIn('secret'+chr(64)+'example.invalid',raw)
            self.assertNotIn('example'+chr(64)+'example.invalid',raw)
            self.assertIsNone(standard_record.EMAIL_RE.search(raw))
            self.assertIsNone(standard_record.HOME_PATH_RE.search(raw))

    def test_cost_uses_each_event_model_not_the_last_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            events=[
                {'type':'turn.completed','model':'gpt-6-luna','usage':{
                    'input_tokens':6555555,'cached_input_tokens':5555555,
                    'output_tokens':6000000,'reasoning_tokens':0}},
                {'type':'turn.completed','model':'gpt-6.1-sol','usage':{
                    'input_tokens':28000000,'cached_input_tokens':0,
                    'output_tokens':144444,'reasoning_tokens':0}},
            ]
            result=self.make_result(Path(tmp),events=events)
            row=standard_record.finalize(result)
            self.assertAlmostEqual(row['cost']['usd'],60.6,places=4)
            stale=cost_calc.calculate('gpt-6.1-sol',34555555,5555555,6144444)
            self.assertAlmostEqual(float(stale['usd']),120.0,places=4)
            self.assertEqual(row['model']['effective'],{'missing':'m39'})

    def test_absent_usage_counter_is_missing_and_cost_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            events=[{'type':'turn.completed','model':'gpt-6-luna','usage':{
                'input_tokens':100,'output_tokens':10,'reasoning_tokens':2}}]
            result=self.make_result(Path(tmp),events=events)
            row=standard_record.finalize(result)
            self.assertEqual(row['tokens']['total']['cached_input'],{'missing':'m39'})
            self.assertEqual(row['cost']['usd'],{'missing':'m70'})
            self.assertIn('incomplete',row['cost']['accounting'])

    def test_empty_usage_event_makes_mixed_run_cost_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            events=[
                {'type':'turn.completed','model':'gpt-6-luna','usage':{}},
                {'type':'turn.completed','model':'gpt-6-luna','usage':{
                    'input_tokens':100,'cached_input_tokens':20,'output_tokens':10,
                    'reasoning_tokens':3,
                }},
            ]
            result=self.make_result(Path(tmp),events=events)
            row=standard_record.finalize(result)
            self.assertEqual(row['cost']['usd'],{'missing':'m70'})
            self.assertIn('incomplete',row['cost']['accounting'])


if __name__=='__main__': unittest.main()
