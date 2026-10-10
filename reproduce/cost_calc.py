#!/usr/bin/env python3
"""calc-v1: price token usage with the frozen API-equivalent table.

Reasoning tokens are already included in output_tokens; reasoning is a subset
of output and must not be added a second time.
"""
from __future__ import annotations
from decimal import Decimal
import hashlib
import json
from pathlib import Path

VERSION = 'calc-v1'
ROOT = Path(__file__).resolve().parents[1]
TABLE_PATH = ROOT / 'reproduce/price-table-v1.json'

class UnlistedModelError(LookupError):
    pass

def load_table(path: Path = TABLE_PATH):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def table_sha256(path: Path = TABLE_PATH) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def calculate(model: str, input_tokens: int, cached_input_tokens: int, output_tokens: int,
              table: dict | None = None) -> dict:
    """Return exact USD using total input, cached input, and output counters.

    Cost = (input - cached) * input_rate + cached * cached_rate + output *
    output_rate, with counters divided by one million. Output already includes
    reasoning tokens, which are a subset and are never added a second time.
    An unlisted model with no sourced rate returns a flagged, unpriced estimate.
    """
    for name, value in (('input_tokens', input_tokens),
                        ('cached_input_tokens', cached_input_tokens),
                        ('output_tokens', output_tokens)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f'{name} must be a non-negative integer')
    if cached_input_tokens > input_tokens:
        raise ValueError('cached_input_tokens cannot exceed input_tokens')
    table = table if table is not None else load_table()
    entry = table.get('models', {}).get(model)
    if not isinstance(entry, dict):
        return {'usd': None, 'status': 'unlisted_model', 'flagged': True,
                'reason': 'No sourced price row exists for this model.'}
    try:
        input_rate = Decimal(str(entry['input']))
        cached_rate = Decimal(str(entry['cached_input']))
        output_rate = Decimal(str(entry['output']))
    except (KeyError, ValueError, ArithmeticError):
        return {'usd': None, 'status': 'unpriced_model', 'flagged': True,
                'reason': 'The model price row has no complete numeric rate vector.'}
    uncached_tokens = input_tokens - cached_input_tokens
    usd = (Decimal(uncached_tokens) * input_rate
           + Decimal(cached_input_tokens) * cached_rate
           + Decimal(output_tokens) * output_rate) / Decimal(1_000_000)
    third_party = entry.get('source') == 'unlisted; third-party'
    return {'usd': usd, 'status': 'declared_estimate' if third_party else 'priced',
            'flagged': third_party,
            'reason': 'Third-party rate; estimate flagged.' if third_party else None}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model')
    parser.add_argument('input_tokens', type=int)
    parser.add_argument('cached_input_tokens', type=int)
    parser.add_argument('output_tokens', type=int)
    args = parser.parse_args()
    result = calculate(args.model, args.input_tokens, args.cached_input_tokens, args.output_tokens)
    result['usd'] = str(result['usd']) if result['usd'] is not None else None
    result['calculator_version'] = VERSION
    result['price_table_version'] = 'sha256:' + table_sha256()
    print(json.dumps(result, sort_keys=True))
