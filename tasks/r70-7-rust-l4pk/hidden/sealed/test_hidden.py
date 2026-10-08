"""Public-contract justifications in docstrings; no source/build-tree inspection."""
import os
import subprocess

BIN = os.environ['KOGEN_TASK_BIN']
HELP = 'Usage: kogen <command> [options] [FILE|-]\nCommands:\n  sum     Sum signed integers.\n  status  Count job states.\nOptions:\n  -h, --help  Show help.\n  --version   Show version.\n'
SUM_HELP = 'Usage: kogen sum [--scale N] [--format text|json] [FILE|-]\nSum one signed integer per nonempty line (default scale: 1).\n'
STATUS_HELP = 'Usage: kogen status [--format text|json] [FILE|-]\nCount ID,STATE records (states: queued,running,done,failed).\n'
EMPTY_STATUS = 'total=0\nqueued=0\nrunning=0\ndone=0\nfailed=0\n'


def expect(args=(), data='', out='', err='', code=0):
    p = subprocess.run([BIN, *args], input=data.encode('ascii') if isinstance(data, str) else data,
                       capture_output=True, timeout=15)
    assert (p.returncode, p.stdout, p.stderr) == (code, out.encode(), err.encode())


def test_global_help():
    """Help: exact bytes and no input read for three routes."""
    for args in [[], ['--help'], ['-h']]:
        expect(args, data='invalid', out=HELP)


def test_version():
    """Version: sole argument exact bytes."""
    expect(['--version'], out='kogen 1.0.0\n')


def test_subcommand_help():
    """Help: each subcommand both help spellings."""
    for command, output in [('sum', SUM_HELP), ('status', STATUS_HELP)]:
        for flag in ['-h', '--help']:
            expect([command, flag], data='invalid', out=output)


def test_unknown_command_and_global_option():
    """Arguments: exact unknown-command versus unknown-option error."""
    for args, msg in [(['wat'], "unknown command 'wat'"), (['SUM'], "unknown command 'SUM'"),
                      (['--format', 'json', 'sum'], "unknown option '--format'"),
                      (['--help', 'sum'], "unknown option '--help'")]:
        expect(args, code=2, err=f'kogen: {msg}\n')


def test_empty_sum():
    """Sum: empty input, stdin marker, empty lines and JSON."""
    expect(['sum'], out='sum=0\n')
    expect(['sum', '-', '--format', 'json'], '\n\n', out='{"sum":0}\n')


def test_signed_sum():
    """Sum grammar: plus, leading zeros, range boundaries, CRLF/final CR."""
    expect(['sum'], '+0002\r\n-1\r\n1000000\r\n-1000000\r', out='sum=1\n')
    expect(['sum'], '+' + '0' * 6000 + '2', out='sum=2\n')


def test_sum_scale_and_json(tmp_path):
    """Arguments: options after file; core sum then multiply; exact JSON."""
    path = tmp_path / 'numbers file'
    path.write_text('3\n-2\n5')
    expect(['sum', str(path), '--scale', '7', '--format', 'json'], out='{"sum":42}\n')


def test_scale_zero_and_large_total():
    """Sum: no negative zero; at most 10000 lines and safe large arithmetic."""
    expect(['sum', '--scale', '0'], '-5', out='sum=0\n')
    expect(['sum', '--scale', '100'], '1000000\n' * 10000, out='sum=1000000000000\n')


def test_invalid_sum_lines():
    """Sum: whitespace/comments/decimal/out-of-range invalid, physical line."""
    for value in [' ', ' 1', '1 ', '1.0', '1#x', '1000001', '-1000001', '+', '999999999999999999999999']:
        expect(['sum'], '\n2\n' + value, code=1, err='kogen:3: expected integer -1000000..1000000\n')


def test_empty_status():
    """Status: empty input and ignored empty lines, canonical zeros."""
    expect(['status'], out=EMPTY_STATUS)
    expect(['status', '-'], '\n\n', out=EMPTY_STATUS)


def test_status_counts():
    """Status: all states, allowed ID characters, order-independent counts."""
    data = 'job_1,done\na-2,queued\nb,running\nc,failed\nd,done'
    expect(['status'], data, out='total=5\nqueued=1\nrunning=1\ndone=2\nfailed=1\n')
    expect(['status'], '\n'.join(reversed(data.splitlines())), out='total=5\nqueued=1\nrunning=1\ndone=2\nfailed=1\n')


def test_status_json(tmp_path):
    """Status: file input, CRLF, final CR and exact JSON field order."""
    path = tmp_path / 'records'
    path.write_bytes(b'a,queued\r\n\r\nb,failed\r')
    expect(['status', '--format', 'json', str(path)], out='{"total":2,"queued":1,"running":0,"done":0,"failed":1}\n')


def test_bad_records():
    """Status grammar: ID/state/one comma/whitespace validation."""
    for row in ['a,DONE', ',done', 'A,done', '1a,done', 'a,done,x', 'a', ' a,done',
                'a,done ', 'a' * 33 + ',done', 'a.b,done', ' ', 'a,done\r\r']:
        expect(['status'], '\n' + row, code=1, err='kogen:2: expected ID,STATE\n')
    expect(['status'], 'a' * 32 + ',done', out='total=1\nqueued=0\nrunning=0\ndone=1\nfailed=0\n')


def test_duplicate_id():
    """Status: duplicate across states, physical line and exact ID."""
    expect(['status'], 'a,queued\n\na,done', code=1, err="kogen:3: duplicate id 'a'\n")


def test_record_validation_before_duplicate():
    """Status: malformed record before duplicate check."""
    expect(['status'], 'a,done\na,wat', code=1, err='kogen:2: expected ID,STATE\n')


def test_missing_option_values():
    """Arguments: separate value required for recognized options."""
    for command, flag in [('sum', '--scale'), ('sum', '--format'), ('status', '--format')]:
        expect([command, flag], code=2, err=f"kogen: option '{flag}' requires a value\n")


def test_invalid_option_values():
    """Arguments: strict bounds/lexemes, consume flag-looking value."""
    for flag, values in [('--scale', ['-1', '101', '01', '+1', '1.0', '--format', '999999999999999999']),
                         ('--format', ['JSON', 'yaml', '-'])]:
        for value in values:
            expect(['sum', flag, value], code=2, err=f"kogen: invalid value for '{flag}': '{value}'\n")


def test_duplicate_options():
    """Arguments: duplication precedes missing or bad value."""
    expect(['sum', '--scale', '2', '--scale'], code=2, err="kogen: duplicate option '--scale'\n")
    expect(['status', '--format', 'text', '--format', 'bad'], code=2, err="kogen: duplicate option '--format'\n")


def test_unknown_options():
    """Arguments: unsupported flags, equals syntax, separator and combined help."""
    for command, flag, rest in [('sum', '--scale=2', []), ('sum', '--format=json', []),
                                ('status', '--scale', ['2']), ('sum', '--', []),
                                ('sum', '--help', ['-']), ('status', '-h', ['x']), ('sum', '-x', [])]:
        expect([command, flag, *rest], code=2, err=f"kogen: unknown option '{flag}'\n")


def test_extra_paths_and_precedence():
    """Arguments: first left-to-right error, two paths include stdin marker."""
    expect(['sum', '-', 'x', '--wat'], code=2, err='kogen: expected at most one input path\n')
    expect(['sum', '--wat', 'x', 'y'], code=2, err="kogen: unknown option '--wat'\n")


def test_file_read_failure(tmp_path):
    """Runtime: missing path gives exact read error for both commands."""
    for command in ['sum', 'status']:
        expect([command, str(tmp_path / 'missing')], code=1, err='kogen: cannot read input\n')


def test_ascii_validation():
    """Runtime: ASCII validation before content parsing."""
    for command in ['sum', 'status']:
        expect([command], b'bad\n\xff', code=1, err='kogen: input is not ASCII\n')


def test_no_partial_output_on_first_error():
    """Core: atomic output and first invalid line."""
    expect(['sum'], '4\nwat\n999999999', code=1, err='kogen:2: expected integer -1000000..1000000\n')
    expect(['status'], 'a,done\nwrong\na,done', code=1, err='kogen:2: expected ID,STATE\n')


def test_format_text_explicit_and_scale_boundary():
    """Options: explicit text/default equivalence and accepted maximum scale."""
    expect(['sum', '--format', 'text', '--scale', '100', '-'], '-2\n3', out='sum=100\n')
    expect(['status', '--format', 'text'], 'a,running', out='total=1\nqueued=0\nrunning=1\ndone=0\nfailed=0\n')
