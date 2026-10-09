import hashlib
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cost_calc

class CostCalculatorTests(unittest.TestCase):
    def test_known_standard_usage_is_exact_and_does_not_double_count_reasoning(self):
        result=cost_calc.calculate('gpt-6-luna',1_000_000,200_000,100_000)
        self.assertEqual(result['usd'],Decimal('0.132'))
        self.assertFalse(result['flagged'])
        self.assertEqual(result['status'],'priced')
    def test_unlisted_model_with_declared_third_party_rate_is_flagged(self):
        table={'models': {'third-party-model': {
            'input': 1, 'cached_input': 0.5, 'output': 2,
            'source': 'unlisted; third-party', 'source_url': 'synthetic test fixture'}}}
        result=cost_calc.calculate('third-party-model',1_000_000,200_000,100_000,table)
        self.assertEqual(result['usd'],Decimal('1.1'))
        self.assertTrue(result['flagged'])
        self.assertEqual(result['status'],'declared_estimate')
    def test_model_without_sourced_rate_stays_flagged_and_unpriced(self):
        result=cost_calc.calculate('unknown-model',1000,0,100)
        self.assertIsNone(result['usd'])
        self.assertTrue(result['flagged'])
        self.assertEqual(result['status'],'unlisted_model')
    def test_price_table_sidecar_matches_content_hash(self):
        expected=(Path(__file__).with_name('price-table-v1.sha256').read_text().strip())
        actual=hashlib.sha256(cost_calc.TABLE_PATH.read_bytes()).hexdigest()
        self.assertEqual(expected,actual)
    def test_requested_rows_have_official_sources_and_rates(self):
        table=cost_calc.load_table()
        self.assertEqual(set(table['models']),{'gpt-6-luna','gpt-6.1-sol','gpt-6-astra'})
        self.assertIn('https://platform.openai.com/pricing',table['models']['gpt-6.1-sol']['source_url'])
        self.assertIn('https://openai.com/index/introducing-gpt-6-1-sol/',table['models']['gpt-6.1-sol']['additional_sources'])

if __name__=='__main__': unittest.main()
