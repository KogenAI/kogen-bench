"""Regression checks for silent omissions, strict enforcement and declarations."""
import copy, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import validate_round as vr

class StandardRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema=json.loads((vr.ROOT/'schema/run-record.schema.json').read_text());cls.current=cls.schema['$defs']['current']
        cls.sample=vr.records()[0]

    def check_schema(self,row):return vr.schema_errors(row,self.current,self.schema)

    def test_current_record_conforms(self):self.assertEqual(self.check_schema(self.sample),[])
    def test_silent_nested_absence_fails(self):
        r=copy.deepcopy(self.sample);del r['tokens']['phases']['plan']['reasoning']
        self.assertTrue(self.check_schema(r))
    def test_empty_missing_reason_fails(self):
        r=copy.deepcopy(self.sample);r['tools']['runner']={'missing':''}
        self.assertTrue(self.check_schema(r))
    def test_boolean_is_not_numeric_usage(self):
        r=copy.deepcopy(self.sample);r['tokens']['total']['input']=True
        self.assertTrue(self.check_schema(r))
    def test_stop_vocabulary_is_closed(self):
        r=copy.deepcopy(self.sample);r['stop_reason']='something happened'
        self.assertTrue(self.check_schema(r))
    def test_unknown_schema_keyword_fails_closed(self):
        self.assertTrue(vr.schema_errors('value',{'mystery':True},{}))

    def with_fixture(self,fn):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'schema').mkdir();(root/'schema/run-record.schema.json').write_text(json.dumps(self.schema))
            folder=root/'rounds/test';folder.mkdir(parents=True)
            for f in ['README.md','MEASURED.md']:(folder/f).write_text('test fixture')
            r=copy.deepcopy(self.sample);r.update({'audit_round':'test','round_id':'test'})
            doc={'round':'test','cells':1,'fields':{p:{'count':sum(c.values()),'reasons':c,'affects_verdict':'limits inference'} for p,c in vr.gaps([r]).items()},'gap_sources':vr.gap_sources([r])}
            (folder/'MISSING.md').write_text('```json\n'+json.dumps(doc)+'\n```')
            with patch.object(vr,'ROOT',root):fn(r,folder,doc)

    def test_declared_gaps_pass_historical_and_fail_strict(self):
        def run(r,folder,doc):
            self.assertFalse(vr.validate('test',[r])['errors'])
            self.assertTrue(vr.validate('test',[r],strict=True)['errors'])
        self.with_fixture(run)
    def test_stale_reason_and_duplicate_identity_fail(self):
        def run(r,folder,doc):
            r['tools']['runner']={'missing':'New undeclared reason'}
            self.assertTrue(vr.validate('test',[r])['errors'])
            self.assertTrue(vr.validate('test',[r,r])['errors'])
        self.with_fixture(run)
    def test_complete_record_can_pass_strict(self):
        def fill(value,schema):
            if isinstance(value,dict) and 'missing' in value:
                choice=schema['anyOf'][0]
                if '$ref' in choice:
                    target=self.schema
                    for part in choice['$ref'][2:].split('/'):target=target[part]
                    choice=target
                if 'enum' in choice:return choice['enum'][0]
                if choice.get('format')=='date-time':return '2026-10-05T00:00:00Z'
                return {'string':'test receipt','integer':choice.get('minimum',0),'number':float(choice.get('minimum',0)),'boolean':False,'array':[]}[choice['type']]
            if '$ref' in schema:
                target=self.schema
                for part in schema['$ref'][2:].split('/'):target=target[part]
                schema=target
            if isinstance(value,dict) and ('not_applicable' in value or 'withheld' in value):return value
            if isinstance(value,dict) and 'not_applicable' not in value:
                return {k:fill(v,schema['properties'][k]) for k,v in value.items()}
            return value
        def run(r,folder,doc):
            complete=fill(r,self.current)
            doc['fields']={}
            doc['gap_sources']=vr.gap_sources([complete])
            (folder/'MISSING.md').write_text('```json\n'+json.dumps(doc)+'\n```')
            self.assertFalse(vr.validate('test',[complete],strict=True)['errors'])
        self.with_fixture(run)

    def test_legacy_schema_still_accepts_1_0(self):
        from partitioned_jsonl import read_partitions
        row=read_partitions(vr.ROOT/'reproduce/inputs/run-evidence')[1][0]
        self.assertEqual(vr.schema_errors(row,self.schema,self.schema),[])
        self.assertTrue(any('schema 1.2' in e for e in vr.validate(row['audit_round'],[row],strict=True)['errors']))

    def test_new_missing_requires_reconstruction_source(self):
        r=copy.deepcopy(self.sample);r['circumstances']['load1_end']={'missing':'unknown-code'}
        self.assertTrue(self.check_schema(r))

    def test_compact_missing_code_is_valid(self):
        r=copy.deepcopy(self.sample);r['circumstances']['load1_end']={'missing':'m08'}
        self.assertEqual(self.check_schema(r),[])

    def test_non_utc_and_invalid_boundaries_fail(self):
        for timestamp in ['not a date','2026-10-05T00:00:00+03:00','2026-10-05 00:00:00+00:00']:
            r=copy.deepcopy(self.sample);r['timestamps']['cell']['start_utc']=timestamp
            self.assertTrue(self.check_schema(r))

    def test_missing_inside_attempt_array_fails_strict(self):
        r=copy.deepcopy(self.sample)
        r['timestamps']['attempts']=[{'attempt':1,'start_utc':{'missing':'No boundary','reconstructable_from':'none'},'end_utc':'2026-10-05T00:00:00Z'}]
        self.assertIn('timestamps.attempts[].start_utc',vr.gaps([r]))
        self.assertTrue(vr.validate(r['audit_round'],[r],strict=True)['errors'])

    def test_account_identity_rejected(self):
        r=copy.deepcopy(self.sample);r['environment']['account_class']='person'+'@'+'example'+'.invalid'
        self.assertTrue(self.check_schema(r))

    def test_empty_strict_cohort_fails(self):
        self.assertTrue(vr.validate('r70',[],strict=True)['errors'])

if __name__=='__main__':unittest.main()
