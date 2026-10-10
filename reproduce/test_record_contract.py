"""The release gate couples the record writer to the current Standard schema."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from record_contract import ROOT, validate_fixture


class RecordContractTests(unittest.TestCase):
    def write_schema(self, root, schema):
        path = root / 'run-record.schema.json'
        path.write_text(json.dumps(schema, sort_keys=True) + '\n', encoding='utf-8')
        return path

    def base_schema(self):
        return json.loads((ROOT / 'schema/run-record.schema.json').read_text(encoding='utf-8'))

    def test_checked_in_fixture_is_emitted_and_strictly_valid(self):
        report = validate_fixture()
        self.assertTrue(report['contract_ok'], report)
        self.assertEqual(report['missing'], 0)
        self.assertTrue(report['schema_valid'], report['schema_errors'])
        self.assertTrue(report['model_effective_set'])

    def test_new_required_schema_field_blocks_record_writer(self):
        schema = self.base_schema()
        current = schema['$defs']['current']
        current['properties']['contract_required_probe'] = {'type': 'string', 'minLength': 1}
        current['required'].append('contract_required_probe')
        with tempfile.TemporaryDirectory(prefix='record-contract-required-') as temporary:
            path = self.write_schema(Path(temporary), schema)
            report = validate_fixture(path)
        self.assertFalse(report['contract_ok'])
        self.assertFalse(report['schema_valid'])
        self.assertTrue(any('contract_required_probe' in error for error in report['schema_errors']))

    def test_dropped_schema_field_rejects_writer_output(self):
        schema = self.base_schema()
        current = schema['$defs']['current']
        self.assertIn('outcome', current['properties'])
        self.assertIn('outcome', current['required'])
        del current['properties']['outcome']
        current['required'].remove('outcome')
        with tempfile.TemporaryDirectory(prefix='record-contract-dropped-') as temporary:
            path = self.write_schema(Path(temporary), schema)
            report = validate_fixture(path)
        self.assertFalse(report['contract_ok'])
        self.assertFalse(report['schema_valid'])
        self.assertTrue(any('outcome: unexpected field' in error for error in report['schema_errors']))


if __name__ == '__main__':
    unittest.main()
