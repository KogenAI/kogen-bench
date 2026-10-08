"""Source-join regression checks: telemetry scope, timestamps and corrected ops."""
import copy,json,unittest
from backfill_context import ROOT, enrich, empty_record
from partitioned_jsonl import read_partitions
class ContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=read_partitions(ROOT/'reproduce/inputs/run-evidence')[1][0]
    def manifest(self,venue='us-worker'):
        return {'venue':venue,'harness':'codex','source':'source-id:public-result','started_at':'2026-10-05T08:00:00Z','ended_at':'2026-10-05T08:01:00Z','host':{'load_avg':0.5},'sandbox':{},'timestamps':{}}
    def row(self,m,events=[],samples=[]):return enrich(copy.deepcopy(self.base),m,{},events,samples,'')
    def test_block_count_does_not_become_host_count(self):
        ev={'event':'start','timestamp':'2026-10-05T08:00:00Z','source':'dispatch:r68b:us','values':{'running':'2','cap':'3','load':'1.2'}}
        r=self.row(self.manifest(),[ev]);self.assertIn('missing',r['circumstances']['concurrent_cells_start']);self.assertEqual(r['circumstances']['load1_start'],1.2)
    def test_host_dispatch_count_includes_new_cell(self):
        ev={'event':'launch','timestamp':'2026-10-05T08:00:00Z','source':'dispatch:r71:host-us','values':{'active':'2','cap':'3'}}
        r=self.row(self.manifest(),[ev]);self.assertEqual(r['circumstances']['concurrent_cells_start'],3)
    def test_periodic_sample_is_not_boundary_measurement(self):
        sample={'timestamp_utc':'2026-10-05T08:00:30Z','load1':8.0,'pressure':1}
        r=self.row(self.manifest('studio'),samples=[sample]);self.assertEqual(r['circumstances']['load_samples'],[sample]);self.assertIn('missing',r['circumstances']['load1_end'])
    def test_uncertain_account_switch_is_missing(self):
        m=self.manifest();m.update(started_at='2026-10-05T07:31:00Z',ended_at='2026-10-05T07:32:00Z');r=self.row(m);self.assertIn('missing',r['environment']['account_class'])
    def test_studio_repetition_does_not_own_round(self):
        m=self.manifest('studio');m['alias']='dev-spec-task-r1-r69-studio'
        r=empty_record(self.base,m,m['alias'],'task','SPEC');self.assertEqual(r['audit_round'],'r69')
    def test_native_gate_boundary_preserved(self):
        m=self.manifest();m['phase_boundaries']={'gate':[{'start_utc':'2026-10-05T08:00:31Z','end_utc':'2026-10-05T08:00:45Z'}]}
        self.assertEqual(self.row(m)['timestamps']['phases']['gate'],m['phase_boundaries']['gate'][0])
if __name__=='__main__':unittest.main()
