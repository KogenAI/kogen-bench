"""Race 3 request-boundary and UTF-8 launch regressions; no model or sockets."""
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

from kogen_conformance.fake_provider import FakeProviderState
from kogen_conformance.gherkin_runner import _script_fixture
from kogen_conformance.process_control import run_process
from kogen_conformance.quint_runner import (
    CaptureProcess, ITFMap, ScriptedProvider, TraceWorld, Variant, _binary_metadata,
)
from kogen_conformance.runner import CaseWorld, Comparator

LOCALE = 'en_US.UTF-8'


class Race3ContractTest(unittest.TestCase):
    def test_json_transcript_cannot_add_legacy_request_assertions(self):
        state = FakeProviderState([{'assistant_text': 'ok'}])
        record = {'body': {'model': 'test-model', 'reasoning': {'effort': 'high'}}}
        state.take(record)
        world = CaseWorld.__new__(CaseWorld)
        world.case = {'id': 'request-boundary', 'provider_expect': [{'headers': {'X-Account': 'old'}}]}
        world.fake = SimpleNamespace(state=state)
        world.comparator = Comparator()
        world.failures = []; world.results = []; world.keep = False
        result = world.finish()
        self.assertEqual(result['status'], 'pass', result['failures'])
        self.assertEqual(result['provider_requests'][0]['body'], record['body'])

    def test_json_and_gherkin_fake_ignore_other_request_fields(self):
        expected = {'role': 'shaper', 'headers': {'X-Account': 'old'}, 'tools': ['write'],
                    'body': {'model': 'test-model', 'reasoning': {'effort': 'high'},
                             'instructions': 'old', 'input': ['old'], 'tools': ['old']}}
        actual = {'body': {'model': 'test-model', 'reasoning': {'effort': 'high'}}}
        state = FakeProviderState([{'expect': expected, 'assistant_text': 'ok'}])
        self.assertIsNotNone(state.take(actual))
        self.assertNotIn('script_error', actual)
        for body in ({'model': 'wrong', 'reasoning': {'effort': 'high'}},
                     {'model': 'test-model', 'reasoning': {'effort': 'low'}}):
            record = {'body': body}
            state = FakeProviderState([{'expect': expected, 'assistant_text': 'ok'}])
            self.assertIsNone(state.take(record))
            self.assertIn('script_error', record)

    def test_quint_request_needs_no_input_and_ignores_headers(self):
        provider = ScriptedProvider({}, lambda value: value)
        expected = {'method': 'POST', 'headers': {'X-Account': 'old'},
                    'equals': {'/model': 'test-model', '/reasoning/effort': 'high',
                               '/instructions': 'old', '/tools': ['old']},
                    'present': ['/input', '/tools']}
        record = {'method': 'POST', 'headers': {},
                  'body': {'model': 'test-model', 'reasoning': {'effort': 'high'}}}
        self.assertEqual(provider._match_request(record, expected), [])
        record['body']['model'] = 'wrong'
        self.assertTrue(provider._match_request(record, expected))
        record['body']['model'] = 'test-model'
        record['body']['reasoning']['effort'] = 'low'
        self.assertTrue(provider._match_request(record, expected))

    def test_gherkin_effective_fixtures_only_pin_model_and_effort(self):
        scripts = ('basic-farewell', 'research-account-shape', 'farewell-questions',
                   'cargo-farewell', 'no-provider-turns', 'farewell-build',
                   'farewell-build-held', 'farewell-build-delayed',
                   'farewell-build-crash', 'farewell-build-hook')
        for name in scripts:
            with self.subTest(script=name):
                turns, contract = _script_fixture(name)
                self.assertLessEqual(set(contract), {'min', 'max', 'model', 'effort'})
                for turn in turns:
                    self.assertEqual(set(turn['expect']), {'body'})
                    body = turn['expect']['body']
                    self.assertEqual(set(body), {'model', 'reasoning'})
                    self.assertEqual(set(body['reasoning']), {'effort'})

    def test_case_and_trace_overrides_cannot_change_or_unset_locale(self):
        with tempfile.TemporaryDirectory(prefix='race3-locale-env-') as td:
            root = Path(td).resolve()
            case = CaseWorld.__new__(CaseWorld)
            case.home = root; case.tmp = root; case.gitconfig = root/'gitconfig'
            env = case._enforce_sandbox_env({'LANG': 'C', 'LC_ALL': 'C.UTF-8'})
            self.assertEqual((env['LANG'], env['LC_ALL']), (LOCALE, LOCALE))
            world = TraceWorld.__new__(TraceWorld)
            world.root = root
            world._base_env = lambda: {'HOME': str(root), 'TMPDIR': str(root),
                                      'KOGEN_CREDENTIAL_STORE': 'file',
                                      'LANG': 'C', 'LC_ALL': 'C'}
            overrides = ITFMap((('LANG', Variant('UnsetEnv', ())),
                                ('LC_ALL', Variant('SetEnv', 'C.UTF-8'))))
            env = world._environment(overrides)
            self.assertEqual((env['LANG'], env['LC_ALL']), (LOCALE, LOCALE))

    def test_sync_and_background_launches_force_utf8_locale(self):
        code = "import json,os;print(json.dumps([os.environ['LANG'],os.environ['LC_ALL'],'hëllo']))"
        with tempfile.TemporaryDirectory(prefix='race3-locale-launch-') as td:
            env = dict(os.environ, LANG='C', LC_ALL='C.UTF-8')
            result = run_process([sys.executable, '-c', code], cwd=td, env=env, timeout_s=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), [LOCALE, LOCALE, 'hëllo'])
            captured = CaptureProcess.start([sys.executable, '-c', code], td, env, b'', 5000)
            try:
                self.assertTrue(captured.wait(5000))
                self.assertEqual(captured.exit_code(), 0)
                self.assertEqual(json.loads(captured.output()[0]), [LOCALE, LOCALE, 'hëllo'])
            finally:
                captured.terminate()

    def test_binary_version_probe_uses_utf8_locale(self):
        with tempfile.TemporaryDirectory(prefix='race3-locale-version-') as td:
            root = Path(td); binary = root/'kogen'
            binary.write_text('#!/bin/sh\nprintf "%s %s\\n" "$LANG" "$LC_ALL"\n')
            binary.chmod(0o755)
            _, version = _binary_metadata(binary, workdir=root)
            self.assertEqual(version, f'{LOCALE} {LOCALE}')


if __name__ == '__main__':
    unittest.main()
