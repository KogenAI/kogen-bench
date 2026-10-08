#!/usr/bin/env python3
"""New task's black-box grader entry; invocation reserved for MacBook poll.py.
Accept candidate workdir as argv[1] (defaults to cwd). It never applies a
reference or restores sealed material. Reads only this task's own staged suite.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def main():
    work = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    suite = Path(__file__).resolve().parent / 'test_hidden.py'
    result = {'tests_ran': False, 'pass_': False, 'checks': [], 'cause': None}
    for argv in [['./setup.sh'], ['make', 'build'], ['make', 'check']]:
        proc = subprocess.run(argv, cwd=work, stdout=sys.stderr, stderr=sys.stderr, check=False)
        result['checks'].append({'argv': argv, 'rc': proc.returncode})
        if proc.returncode:
            print(json.dumps(result))
            return 1
    with tempfile.TemporaryDirectory(prefix='r70-blackbox-') as tmp:
        report = Path(tmp) / 'report.xml'
        env = {**os.environ, 'KOGEN_TASK_BIN': str(work / 'run'),
               'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
        proc = subprocess.run([str(work / 'run-hidden'), '--junitxml', str(report), str(suite)],
                              cwd=work, env=env, stdout=sys.stderr, stderr=sys.stderr, check=False)
        if report.exists():
            suites = ET.parse(report).getroot().findall('testsuite')
            counts = {key: sum(int(s.attrib[key]) for s in suites)
                      for key in ['tests', 'failures', 'errors', 'skipped']}
            result.update(counts)
            result['tests_ran'] = counts['tests'] == 24 and counts['errors'] == 0
            result['pass_'] = (proc.returncode == 0 and counts ==
                               {'tests': 24, 'failures': 0, 'errors': 0, 'skipped': 0})
    receipt = os.environ.get('BENCH_GRADE_RECEIPT')
    if receipt:
        Path(receipt).write_text(json.dumps(result) + '\n')
    print(json.dumps(result))
    return 0 if result['pass_'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
