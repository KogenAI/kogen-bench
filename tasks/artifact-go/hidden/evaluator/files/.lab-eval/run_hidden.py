"""Run the hidden suite without pytest and write Lab's lab_jsonl results (EVL-6).

Parametrized tests are expanded to one result per case, id `test_hidden:test_x[case]`.
The system git the suite may drive sees no user or system configuration.
"""
import importlib.util
import inspect
import itertools
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import types

out = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
os.environ['KOGEN_TASK_BIN'] = os.path.join(os.getcwd(), 'run')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['GIT_CONFIG_GLOBAL'] = os.devnull
os.environ['GIT_CONFIG_NOSYSTEM'] = '1'

try:
    import pytest  # noqa: F401
except ModuleNotFoundError:
    class _Mark:
        def __init__(self, name, args, kwargs):
            self.name, self.args, self.kwargs = name, args, kwargs

    class _MarkGenerator:
        def __getattr__(self, name):
            def decorator(*args, **kwargs):
                def wrap(fn):
                    fn.pytestmark = list(getattr(fn, 'pytestmark', [])) + [_Mark(name, args, kwargs)]
                    return fn
                return wrap
            return decorator

    stub = types.ModuleType('pytest')
    stub.mark = _MarkGenerator()
    sys.modules['pytest'] = stub

SAFE = re.compile(r'^[A-Za-z0-9_.-]+$')


def case_id(argname, index, value):
    if isinstance(value, str) and SAFE.match(value):
        return value
    if isinstance(value, (int, float, bool)) or value is None:
        return str(value)
    return f'{argname}{index}'


def cases(fn):
    """Yield (suffix, kwargs) for every parametrize combination; one empty case if none."""
    marks = [m for m in getattr(fn, 'pytestmark', []) if getattr(m, 'name', '') == 'parametrize']
    if not marks:
        yield '', {}
        return
    axes = []
    for mark in marks:
        names, values = mark.args[0], list(mark.args[1])
        names = [n.strip() for n in names.split(',')] if isinstance(names, str) else list(names)
        axis = []
        for index, value in enumerate(values):
            row = list(value) if len(names) > 1 else [value]
            ident = '-'.join(case_id(n, index, v) for n, v in zip(names, row))
            axis.append((ident, dict(zip(names, row))))
        axes.append(axis)
    for combo in itertools.product(*axes):
        ident = '-'.join(c[0] for c in combo)
        kwargs = {}
        for _, kw in combo:
            kwargs.update(kw)
        yield f'[{ident}]', kwargs


spec = importlib.util.spec_from_file_location('test_hidden', os.path.join(here, 'test_hidden.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with open(out, 'w') as results:
    for name, fn in list(vars(module).items()):
        if not (name.startswith('test_') and callable(fn)):
            continue
        params = list(inspect.signature(fn).parameters)
        seen = set()
        for suffix, kwargs in cases(fn):
            ident = 'test_hidden:' + name + suffix
            if ident in seen:
                ident += f'#{len(seen)}'
            seen.add(ident)
            tmp = tempfile.mkdtemp(prefix='lab-eval-')
            try:
                missing = [p for p in params if p != 'tmp_path' and p not in kwargs]
                if missing:
                    state = 'invalid'
                else:
                    if 'tmp_path' in params:
                        kwargs = {**kwargs, 'tmp_path': pathlib.Path(tmp)}
                    fn(**kwargs)
                    state = 'passed'
            except Exception:
                state = 'failed'
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            results.write(json.dumps({'id': ident, 'state': state}) + '\n')
            results.flush()
    results.write(json.dumps({'suite': 'finished'}) + '\n')
