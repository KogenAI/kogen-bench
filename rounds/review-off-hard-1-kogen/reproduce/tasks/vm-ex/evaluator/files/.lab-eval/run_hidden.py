"""Run the hidden suite without pytest and write Lab's lab_jsonl results (EVL-6)."""
import importlib.util
import inspect
import json
import os
import pathlib
import shutil
import sys
import tempfile

out = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
os.environ['KOGEN_TASK_BIN'] = os.path.join(os.getcwd(), 'run')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
spec = importlib.util.spec_from_file_location('test_hidden', os.path.join(here, 'test_hidden.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with open(out, 'w') as results:
    for name, fn in list(vars(module).items()):
        if not (name.startswith('test_') and callable(fn)):
            continue
        params = list(inspect.signature(fn).parameters)
        tmp = tempfile.mkdtemp(prefix='lab-eval-')
        try:
            if [p for p in params if p != 'tmp_path']:
                state = 'invalid'
            else:
                fn(**({'tmp_path': pathlib.Path(tmp)} if 'tmp_path' in params else {}))
                state = 'passed'
        except Exception:
            state = 'failed'
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        results.write(json.dumps({'id': 'test_hidden:' + name, 'state': state}) + '\n')
        results.flush()
    results.write(json.dumps({'suite': 'finished'}) + '\n')
