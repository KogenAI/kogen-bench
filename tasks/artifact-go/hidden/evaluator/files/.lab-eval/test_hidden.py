"""Public-contract tests for wordfreq; each runs the tracked launcher ./run as a black box."""
import json
import os
import subprocess

import pytest

BIN = os.environ['KOGEN_TASK_BIN']


def run(args=(), data=b''):
    p = subprocess.run([BIN, *args], input=data, capture_output=True, timeout=20)
    return p.returncode, p.stdout, p.stderr


def expect(args=(), data=b'', out='', err='', code=0):
    got = run(args, data)
    assert got == (code, out.encode(), err.encode()), got


def test_counts_are_ordered_by_count_then_word():
    """Highest count first; equal counts in byte order of the word."""
    expect([], b'pear apple pear fig apple pear zed\n', out='pear 3\napple 2\nfig 1\nzed 1\n')


def test_case_is_folded():
    """The, THE and the are one word, printed lower-case."""
    expect([], b'The THE the Cat cat\n', out='the 3\ncat 2\n')


def test_digits_are_word_characters_and_punctuation_separates():
    """Letters and digits form words; every other ASCII byte separates them."""
    expect([], b'a1,b2;a1 -- b2/c_3 a1\n', out='a1 3\nb2 2\n3 1\nc 1\n')


def test_non_ascii_bytes_separate_words():
    """Each non-ASCII byte is a separator, not part of a word."""
    expect([], b'caf\xc3\xa9 caf\xc3\xa9 na\xc3\xafve\n', out='caf 2\nna 1\nve 1\n')


def test_input_without_final_newline_and_with_crlf():
    """Line endings are separators; a missing final newline does not matter."""
    expect([], b'one\r\ntwo\r\none', out='one 2\ntwo 1\n')


def test_empty_input_json_is_an_empty_array():
    """No words in JSON is exactly [] and a newline."""
    expect(['--format', 'json'], b' \n,,\n', out='[]\n')


def test_json_format():
    """JSON is one line, no spaces, objects in the same order as text."""
    expect(['--format', 'json'], b'b a b\n', out='[{"word":"b","count":2},{"word":"a","count":1}]\n')


def test_top_keeps_the_first_n_words():
    """--top N limits the ordered result."""
    expect(['--top', '2'], b'c c c b b a\n', out='c 3\nb 2\n')


def test_top_larger_than_result_keeps_everything():
    """--top beyond the number of words changes nothing."""
    expect(['--top', '10'], b'x y y\n', out='y 2\nx 1\n')


def test_min_keeps_words_with_count_at_least_n():
    """--min N keeps count >= N, including words with exactly N."""
    expect(['--min', '2'], b'c c c b b a\n', out='c 3\nb 2\n')


def test_min_and_top_combine_in_json():
    """--min is applied first, then --top."""
    expect(['--min', '2', '--top', '1', '--format', 'json'], b'c c c b b a\n', out='[{"word":"c","count":3}]\n')


def test_reads_file_argument(tmp_path):
    """A path argument reads that file and ignores stdin."""
    path = tmp_path / 'in.txt'
    path.write_bytes(b'file file other\n')
    expect([str(path)], b'stdin only\n', out='file 2\nother 1\n')


def test_dash_reads_stdin():
    """A lone - means stdin."""
    expect(['-'], b'x x y\n', out='x 2\ny 1\n')


def test_options_may_follow_the_path(tmp_path):
    """Options are accepted on either side of the path."""
    path = tmp_path / 'in.txt'
    path.write_bytes(b'a a b\n')
    expect([str(path), '--top', '1', '--format', 'json'], out='[{"word":"a","count":2}]\n')


def test_unreadable_input_file(tmp_path):
    """A missing file is a runtime error: exit 1, one line, empty stdout."""
    expect([str(tmp_path / 'missing.txt')], err='wordfreq: cannot read input\n', code=1)


def test_a_json_result_parses_back():
    """The JSON output is valid JSON with the counted words."""
    code, out, err = run(['--format', 'json'], b'Go go GO stop\n')
    assert code == 0 and err == b''
    assert json.loads(out) == [{'word': 'go', 'count': 3}, {'word': 'stop', 'count': 1}]


USAGE_CASES = [
    (['--top', '1', '--top', '2'], "duplicate option '--top'"),
    (['--top', '1', '--top'], "duplicate option '--top'"),
    (['--format'], "option '--format' requires a value"),
    (['--min', '0'], "invalid value for '--min': '0'"),
    (['--top', '007'], "invalid value for '--top': '007'"),
    (['--top', '1000001'], "invalid value for '--top': '1000001'"),
    (['--format', 'xml'], "invalid value for '--format': 'xml'"),
    (['--top', '--min'], "invalid value for '--top': '--min'"),
    (['--min=2'], "unknown option '--min=2'"),
    (['--help'], "unknown option '--help'"),
    (['--bogus', '--top', '0'], "unknown option '--bogus'"),
    (['--top', '0', '--bogus'], "invalid value for '--top': '0'"),
    (['one.txt', 'two.txt'], 'expected at most one input path'),
]


@pytest.mark.parametrize('case', USAGE_CASES)
def test_argument_errors_are_exact(case):
    """Argument errors: exit 2, empty stdout, one exact stderr line, first error wins."""
    args, message = case
    expect(args, b'ignored words\n', err='wordfreq: ' + message + '\n', code=2)
