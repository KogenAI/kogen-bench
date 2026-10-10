import json, subprocess, sys, tempfile, unittest
from pathlib import Path
SCRIPT=Path(__file__).with_name('lane-plan.py')

class LanePlanTests(unittest.TestCase):
    def invoke(self, plan, model='m1'):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'plan.json'; path.write_text(json.dumps(plan))
            return subprocess.run([sys.executable,str(SCRIPT),'--plan',str(path),'--cell','c1','--task','t1','--model',model,'--effort','high'],capture_output=True,text=True)
    def fixture(self):
        return {'cells':[{'round_id':'r1','audit_round':'r1','cell_id':'c1','task':'t1','model':'m1','effort':'high','effective_model':'m1','effective_effort':'high','arm':'a','harness':'h','harness_version':'h1','recipe':'recipe-v1','itt':{'class':'counted','cohort':'scored','evidence_ref':'rounds/r1/ITT.md'},'repetition':1,'base_repo':'Public task fixture','base_revision':{'kind':'git-commit','hash':'a'*40},'launcher_sha256':'b'*64,'adapter_harness_sha':'c'*64,'deps_source':'task-derived','ledger_sha256':'d'*64,'kogen_sha':'e'*40,'source_ref':'rounds/r1/README.md','venue':'us','account_class':'billing','queue_position':'held'}]}
    def test_plan_identity_resolves(self):
        result=self.invoke(self.fixture())
        self.assertEqual(result.returncode,0,result.stderr)
        row=json.loads(result.stdout)
        self.assertEqual(row['cell_id'],'c1')
        self.assertEqual(row['dispatcher_id'],'b'*64)
        self.assertEqual(row['venue'],'us')
        self.assertEqual(row['account_class'],'billing')
        self.assertEqual(row['queue_position'],'held')
    def test_string_base_revision_is_normalized_object(self):
        plan=self.fixture(); plan['cells'][0]['base_revision']='a'*40
        result=self.invoke(plan)
        self.assertEqual(result.returncode,0,result.stderr)
        row=json.loads(result.stdout)
        self.assertEqual(row['base_revision'],{'kind':'git-commit','hash':'a'*40})
    def test_private_paths_and_email_are_not_returned(self):
        plan=self.fixture(); cell=plan['cells'][0]
        private_path='/'+'Users'+'/alice/private/repo'
        private_email='alice'+chr(64)+'example.invalid'
        cell['base_repo']=private_path
        result=self.invoke(plan)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('base_repo',result.stderr)
        self.assertNotIn(private_path,result.stdout+result.stderr)
        plan=self.fixture(); cell=plan['cells'][0]
        cell['harness_version']='harness for '+private_email
        result=self.invoke(plan)
        self.assertNotEqual(result.returncode,0)
        self.assertNotIn(private_email,result.stdout+result.stderr)
    def test_model_mismatch_fails_before_launch(self):
        result=self.invoke(self.fixture(),model='m2')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('model',result.stderr)

    def test_release_identity_inputs_fail_closed_before_launch(self):
        for key in ('effective_model','venue','account_class','queue_position','kogen_sha','base_repo'):
            with self.subTest(key=key):
                plan=self.fixture(); plan['cells'][0].pop(key)
                result=self.invoke(plan)
                self.assertNotEqual(result.returncode,0)
    def test_nonstandard_itt_values_fail_before_launch(self):
        for key,value in (('class','dry-cell'),('cohort','host-layout')):
            with self.subTest(key=key):
                plan=self.fixture(); plan['cells'][0]['itt'][key]=value
                result=self.invoke(plan)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('ITT',result.stderr)

if __name__=='__main__': unittest.main()
