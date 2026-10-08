"""Each test cites its public contract clause; subprocess/files only, no source inspection."""
import os
import subprocess

BIN = os.environ['KOGEN_TASK_BIN']
HELP = 'Usage: kogen-config [FILE|-]\nParse a strict YAML-subset configuration from FILE or stdin.\nOptions:\n  --help  Show this help.\n'
DEFAULT = 'name=kogen\nworkers=1\nenabled=true\ndirectory=.\n'


def run(data='', args=()):
    return subprocess.run([BIN, *args], input=data.encode('ascii') if isinstance(data, str) else data,
                          capture_output=True, timeout=15)


def expect(data='', args=(), out='', err='', code=0):
    p = run(data, args)
    assert (p.returncode, p.stdout, p.stderr) == (code, out.encode(), err.encode())


def bad(data, line, col, message):
    expect(data, err=f'config:{line}:{col}: {message}\n', code=1)


def test_help():
    """CLI: sole help is exact and ignores malformed input."""
    expect('broken', ['--help'], out=HELP)


def test_empty_defaults():
    """Schema: empty mapping defaults; CLI absent path / explicit stdin."""
    expect(out=DEFAULT)
    expect(args=['-'], out=DEFAULT)


def test_comments_and_crlf():
    """Grammar: blank/comment lines, CRLF and final CR ignored."""
    expect(' # ignored\r\n   \r\n# ignored\r', out=DEFAULT)


def test_all_keys_order_and_file(tmp_path):
    """Schema: arbitrary order; CLI file read; canonical order."""
    path = tmp_path / 'config with spaces.yml'
    path.write_text('enabled: false\ndirectory: /tmp/jobs\nworkers: 64\nname: runner')
    expect(args=[str(path)], out='name=runner\nworkers=64\nenabled=false\ndirectory=/tmp/jobs\n')


def test_unknown_options():
    """CLI: option error before argument count, first option wins."""
    for args, flag in [(['--wat'], '--wat'), (['a', 'b', '-h'], '-h'), (['--help', '-x'], '--help')]:
        expect(args=args, code=2, err=f"config: unknown option '{flag}'\n")


def test_extra_paths():
    """CLI: at most one path, including help combined with path."""
    expect(args=['a', 'b'], code=2, err='config: expected at most one input path\n')
    expect(args=['--help', 'a'], code=2, err="config: unknown option '--help'\n")


def test_unreadable_file(tmp_path):
    """CLI: missing file is runtime error with no partial output."""
    expect(args=[str(tmp_path / 'missing')], code=1, err='config: cannot read input\n')


def test_unknown_key():
    """Grammar: unknown key precedes malformed/missing scalar."""
    bad('name: okay\nother:', 2, 1, "unknown key 'other'")


def test_duplicate_key():
    """Grammar: repeats rejected even equal; duplicate before value syntax."""
    bad('workers: 2\nworkers: 2', 2, 1, "duplicate key 'workers'")
    bad('name: a\nname: "', 2, 1, "duplicate key 'name'")


def test_indentation():
    """Grammar: no nesting or non-comment indentation."""
    bad(' name: x', 1, 1, 'unexpected indentation')
    bad('name: x\n  workers: 2', 2, 1, 'unexpected indentation')


def test_tabs():
    """Grammar: tab column and precedence over indentation/syntax."""
    bad(' name:\tfoo', 1, 7, 'tab is not allowed')
    bad('#\tcomment', 1, 2, 'tab is not allowed')


def test_key_grammar():
    """Grammar: key regex, missing colon and space before colon."""
    for data in ['Name: x', 'name : x', 'name x', '---', 'a1: x', '- name: x']:
        bad(data, 1, 1, 'expected key: value')


def test_missing_scalar():
    """Grammar: absent/comment-only scalar exact start column."""
    bad('name:', 1, 6, 'missing value')
    bad('name:   ', 1, 9, 'missing value')
    bad('name: # comment', 1, 7, 'missing value')


def test_bare_comments_and_hash():
    """Grammar: spaced comments versus literal hash, retained internal spaces."""
    expect('name: a#b two  words   # comment\ndirectory: ./a:b',
           out='name=a#b two  words\nworkers=1\nenabled=true\ndirectory=./a:b\n')


def test_invalid_bare():
    """Grammar: unsupported flow/anchors/tags/backslash/control chars."""
    for data in ['name: [a]', 'name: &a', 'name: !tag', 'name: a\\b', 'name: a\x01', 'name: a\r\r']:
        bad(data, 1, 7, 'invalid bare scalar')


def test_single_quote():
    """Grammar: doubled quote and literal punctuation/hash."""
    expect("name: 'it''s # okay' # comment\ndirectory: 'a\\b'",
           out="name=it's # okay\nworkers=1\nenabled=true\ndirectory=a\\b\n")


def test_double_quote():
    """Grammar: only quote/backslash escapes, literal punctuation."""
    expect('name: "a\\"b\\\\c # d"\ndirectory: "[x]"',
           out='name=a"b\\c # d\nworkers=1\nenabled=true\ndirectory=[x]\n')


def test_invalid_escape():
    """Grammar: unknown or trailing escape column."""
    bad('name: "a\\n"', 1, 9, 'invalid escape')
    bad('name: "a\\', 1, 9, 'invalid escape')


def test_unterminated_and_control_quotes():
    """Grammar: missing close and quoted control characters."""
    for data in ['name: "abc', "name: 'abc"]:
        bad(data, 1, 7, 'unterminated quoted scalar')
    bad('name: "a\x01"', 1, 7, 'invalid quoted scalar')


def test_trailing_quote_text():
    """Grammar: adjacent comment disallowed; first nonspace column."""
    bad('name: "a"#x', 1, 10, 'unexpected trailing text')
    bad("name: 'a'  x", 1, 12, 'unexpected trailing text')


def test_integer_types_and_bounds():
    """Schema: workers unquoted canonical positive integer, 1..64."""
    for value in ['0', '65', '01', '-1', '1.0', '99999999999999999999999', '"2"', "'2'"]:
        bad('workers: ' + value, 1, 10, 'expected integer 1..64')
    bad('workers: +1', 1, 10, 'invalid bare scalar')
    expect('workers: 1', out=DEFAULT)


def test_boolean_and_empty_strings():
    """Schema: strict bool and nonempty decoded strings; strings not coerced."""
    for value in ['True', 'yes', '0', '"false"']:
        bad('enabled: ' + value, 1, 10, 'expected true or false')
    bad('name: ""', 1, 7, 'expected nonempty string')
    bad("directory: ''", 1, 12, 'expected nonempty string')
    expect('name: false\ndirectory: 123', out='name=false\nworkers=1\nenabled=true\ndirectory=123\n')


def test_first_error_and_no_partial_output():
    """Grammar: physical lines and first grammar error, atomic output."""
    bad('# comment\n\nworkers: nope\nunknown: x', 3, 10, 'expected integer 1..64')


def test_ascii_validation():
    """CLI: byte-column ASCII validation precedes parsing."""
    expect(b'bad\nname: \xff', code=1, err='config:2:7: expected ASCII input\n')
