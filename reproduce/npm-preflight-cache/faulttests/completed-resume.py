# Provenance copy of the fault test as run on 30 October 2026. Paths are parameters: set the environment variables named below to a scratch
# directory, your lanes release and your task-kit directory. It needs pinned Kogen artifacts; it is not runnable standalone.
from pathlib import Path
import hashlib
import json
import os
import sys
from unittest import mock

ROOT = Path(os.environ['FAULT_ROOT'])
L = ROOT / 'repo/lanes'
proof = ROOT / 'proof'
sys.path.insert(0, str(L))
from lanes import dispatch, preflight
events = proof / 'cell-events.txt'
before = events.read_bytes()
with mock.patch.object(preflight, 'check_one', side_effect=AssertionError('completed task was reapproved')) as check:
    code = dispatch.run_all(str(proof/'run'), str(proof/'tasks'), str(proof/'hosts.json'),
                            lanes_dir=str(L/'tests/fixtures/fake-lanes'))
assert code == 0 and check.call_count == 0
assert events.read_bytes() == before
(proof/'completed-resume.json').write_text(json.dumps(dict(exit=code, new_approvals=0, new_cells=0,
    final_preflight_sha256=hashlib.sha256((L/'lanes/preflight.py').read_bytes()).hexdigest()), indent=2)+'\n')
