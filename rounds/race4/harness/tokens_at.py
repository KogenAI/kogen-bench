"""Import adapter for the self-contained, hyphen-named tokens-at.py CLI."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location('race_tokens_at', Path(__file__).with_name('tokens-at.py'))
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
TOKEN_FIELDS = _module.TOKEN_FIELDS
usage_at = _module.usage_at
snapshot_time = _module.snapshot_time
