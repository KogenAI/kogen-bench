import os
import subprocess
from datetime import datetime, timezone


BIN = os.environ["KOGEN_TASK_BIN"]
HELP = (
    b"Usage: kogen-cron [--after YYYY-MM-DDTHH:MM] [--count N] [--format text|json] [FILE|-]\n"
    b"Find upcoming UTC minutes for named cron expressions.\nOptions:\n"
    b"  --after VALUE    Exclusive UTC starting minute (default 2000-01-01T00:00).\n"
    b"  --count N        Occurrences per expression (default 3; range 1..20).\n"
    b"  --format FORMAT  Output text (default) or json.\n"
    b"  --help           Show this help.\n"
)


def invoke(data=b"", *args):
    return subprocess.run(
        [BIN, *map(str, args)], input=data, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=15, check=False,
    )


def expect(result, code, stdout, stderr=b""):
    assert (result.returncode, result.stdout, result.stderr) == (code, stdout, stderr)


def minute(year, month, day, hour=0, minute_value=0):
    stamp = datetime(year, month, day, hour, minute_value, tzinfo=timezone.utc)
    return int(stamp.timestamp() // 60)


def text_line(name, *runs):
    return (name + "\t" + "\t".join(map(str, runs)) + "\n").encode("ascii")


def test_help_is_exact_and_does_not_read_input():
    expect(invoke(b"broken\n", "--help"), 0, HELP)


def test_duplicate_count_is_checked_before_missing_value():
    expect(invoke(b"", "--count", "1", "--count"), 2, b"", b"cron: duplicate option '--count'\n")


def test_duplicate_after_and_format_options():
    expect(invoke(b"", "--after", "2000-01-01T00:00", "--after"), 2, b"", b"cron: duplicate option '--after'\n")
    expect(invoke(b"", "--format", "text", "--format"), 2, b"", b"cron: duplicate option '--format'\n")


def test_option_values_consume_dash_tokens_and_missing_is_exact():
    expect(invoke(b"", "--count", "-1"), 2, b"", b"cron: invalid value for '--count': '-1'\n")
    expect(invoke(b"", "--after"), 2, b"", b"cron: option '--after' requires a value\n")


def test_count_syntax_range_and_leading_zeroes():
    expect(invoke(b"every * * * * *\n", "--after", "1970-01-01T00:00", "--count", "02"), 0, text_line("every", 1, 2))
    expect(invoke(b"", "--count", "1x"), 2, b"", b"cron: invalid value for '--count': '1x'\n")
    expect(invoke(b"", "--count", "0"), 2, b"", b"cron: value out of range for '--count': '0'\n")
    expect(invoke(b"", "--count", "21"), 2, b"", b"cron: value out of range for '--count': '21'\n")


def test_after_timestamp_format_and_supported_year_bounds():
    expect(invoke(b"", "--after", "2000-1-01T00:00"), 2, b"", b"cron: invalid value for '--after': '2000-1-01T00:00'\n")
    expect(invoke(b"", "--after", "1969-12-31T23:59"), 2, b"", b"cron: invalid value for '--after': '1969-12-31T23:59'\n")
    expect(invoke(b"", "--after", "2191-01-01T00:00"), 2, b"", b"cron: invalid value for '--after': '2191-01-01T00:00'\n")


def test_invalid_calendar_timestamp_is_rejected():
    expect(invoke(b"", "--after", "2001-02-29T00:00"), 2, b"", b"cron: invalid value for '--after': '2001-02-29T00:00'\n")


def test_unknown_option_and_second_path_are_argument_errors(tmp_path):
    expect(invoke(b"", "--bogus"), 2, b"", b"cron: unknown option '--bogus'\n")
    expect(invoke(b"", str(tmp_path / "one"), str(tmp_path / "two")), 2, b"", b"cron: expected at most one input path\n")


def test_file_path_and_dash_path_use_the_selected_input(tmp_path):
    path = tmp_path / "jobs.cron"
    path.write_bytes(b"filejob 1 0 1 1 *\n")
    args = ("--after", "1970-01-01T00:00", "--count", "1")
    expect(invoke(b"ignored * * * * *\n", *args, "-"), 0, text_line("ignored", 1))
    expect(invoke(b"", *args, str(path)), 0, text_line("filejob", 1))


def test_missing_file_error_uses_a_fresh_tmp_path(tmp_path):
    missing = tmp_path / "absent" / "jobs.cron"
    expect(invoke(b"", str(missing)), 1, b"", b"cron: cannot read input\n")


def test_default_anchor_count_and_text_format():
    result = invoke(b"every * * * * *\n")
    start = minute(2000, 1, 1)
    expect(result, 0, text_line("every", start + 1, start + 2, start + 3))


def test_starting_minute_is_exclusive_and_epoch_output_is_base_ten():
    expect(invoke(b"every * * * * *\n", "--after", "1970-01-01T00:00", "--count", "3"), 0, text_line("every", 1, 2, 3))


def test_default_text_is_in_source_record_order():
    source = b"zeta 1 * * * *\nalpha 2 * * * *\n"
    expected = text_line("zeta", 1, 61, 121) + text_line("alpha", 2, 62, 122)
    expect(invoke(source, "--after", "1970-01-01T00:00"), 0, expected)


def test_compact_json_field_order_and_integer_runs():
    source = b"one 1 * * * *\ntwo 2 * * * *\n"
    expected = b'{"schedules":[{"name":"one","runs":[1,61,121]},{"name":"two","runs":[2,62,122]}]}\n'
    expect(invoke(source, "--after", "1970-01-01T00:00", "--format", "json"), 0, expected)


def test_empty_json_has_exact_top_level_field():
    expect(invoke(b"", "--format", "json"), 0, b'{"schedules":[]}\n')


def test_blank_and_full_line_comment_records_are_ignored():
    data = b"  # header\twith tab\n \t\njob 1 0 1 1 *\n"
    expect(invoke(data, "--after", "1970-01-01T00:00", "--count", "1"), 0, text_line("job", 1))


def test_field_lists_ranges_and_steps_are_combined_as_sets():
    source = b"picks 1,3-7/2 * * * *\n"
    expect(invoke(source, "--after", "1970-01-01T00:00", "--count", "4"), 0, text_line("picks", 1, 3, 5, 7))


def test_stepped_wildcard_and_stepped_single_value():
    a = invoke(b"quarter */15 * * * *\n", "--after", "1970-01-01T00:00", "--count", "4")
    b = invoke(b"start 5/10 * * * *\n", "--after", "1970-01-01T00:00", "--count", "3")
    expect(a, 0, text_line("quarter", 15, 30, 45, 60))
    expect(b, 0, text_line("start", 5, 15, 25))


def test_leading_zeroes_in_field_numbers_are_accepted():
    expect(invoke(b"padded 005 00 01 01 7\n", "--after", "1970-01-01T00:00", "--count", "1"), 0, text_line("padded", 5))


def test_weekday_seven_is_the_same_sunday_as_zero():
    source = b"sun0 0 0 * * 0\nsun7 0 0 * * 7\n"
    expected = text_line("sun0", 4320) + text_line("sun7", 4320)
    expect(invoke(source, "--after", "1970-01-01T00:00", "--count", "1"), 0, expected)


def test_day_of_month_and_weekday_use_or_when_both_are_restricted():
    source = b"day 0 0 1 * 0\n"
    expected = text_line("day", 4320, 14400, 24480)
    expect(invoke(source, "--after", "1970-01-01T00:00", "--count", "3"), 0, expected)


def test_exact_wildcard_makes_the_other_day_field_decide():
    sunday = invoke(b"sun 0 0 * * 0\n", "--after", "1970-01-01T00:00", "--count", "2")
    first = invoke(b"first 0 0 1 * *\n", "--after", "1970-01-01T00:00", "--count", "1")
    expect(sunday, 0, text_line("sun", 4320, 14400))
    expect(first, 0, text_line("first", 44640))


def test_stepped_wildcard_is_restricted_for_day_matching():
    source = b"stepday 0 0 */1 * 0\n"
    expect(invoke(source, "--after", "1970-01-01T00:00", "--count", "2"), 0, text_line("stepday", 1440, 2880))


def test_month_selection_and_leap_day_are_gregorian():
    source = b"leap 0 0 29 2 *\n"
    expected = text_line("leap", minute(2000, 2, 29), minute(2004, 2, 29))
    expect(invoke(source, "--after", "2000-01-01T00:00", "--count", "2"), 0, expected)


def test_each_field_has_its_own_inclusive_numeric_bounds():
    cases = (
        (b"minute 60 * * * *\n", b"cron:1:8: invalid minute field\n"),
        (b"hour * 24 * * *\n", b"cron:1:8: invalid hour field\n"),
        (b"month * * * 13 *\n", b"cron:1:13: invalid month field\n"),
        (b"weekday * * * * 8\n", b"cron:1:17: invalid day-of-week field\n"),
    )
    for source, error in cases:
        expect(invoke(source), 1, b"", error)


def test_field_grammar_rejects_empty_terms_wrapping_ranges_and_bad_steps():
    for field in (b"1,,2", b"59-0", b"*/0", b"1/61", b"1-2/0", b"1-2-3"):
        source = b"job " + field + b" * * * *\n"
        expect(invoke(source), 1, b"", b"cron:1:5: invalid minute field\n")


def test_record_field_count_is_checked_before_name_and_field_values():
    expect(invoke(b"Bad 60 *\n"), 1, b"", b"cron:1:1: wrong field count\n")


def test_invalid_name_uses_the_name_column():
    expect(invoke(b"Bad * * * * *\n"), 1, b"", b"cron:1:1: invalid name\n")
    expect(invoke(b"9job * * * * *\n"), 1, b"", b"cron:1:1: invalid name\n")


def test_duplicate_name_check_follows_all_syntax_checks():
    source = b"same * * * * *\nsame 60 * * * *\n"
    expect(invoke(source), 1, b"", b"cron:2:6: invalid minute field\n")


def test_duplicate_name_reports_the_second_occurrence_column():
    source = b"  same * * * * *\n   same 0 * * * *\n"
    expect(invoke(source), 1, b"", b"cron:2:4: duplicate name\n")


def test_ascii_validation_precedes_earlier_record_errors():
    expect(invoke(b"bad 60 * * * *\nname\xff * * * * *\n"), 1, b"", b"cron:2:5: expected ASCII\n")


def test_tabs_on_records_are_rejected_before_field_count():
    expect(invoke(b"job\t0 * * * *\n"), 1, b"", b"cron:1:4: tab is not allowed\n")


def test_crlf_and_final_cr_are_removed_before_parsing():
    source = b"job 1 * * * *\r\n"
    expect(invoke(source, "--after", "1970-01-01T00:00", "--count", "1"), 0, text_line("job", 1))
    expect(invoke(b"job 1 * * * *\r", "--after", "1970-01-01T00:00", "--count", "1"), 0, text_line("job", 1))


def test_syntax_error_on_later_record_prevents_any_output():
    source = b"good * * * * *\nbad * * *\n"
    expect(invoke(source), 1, b"", b"cron:2:1: wrong field count\n")


def test_insufficient_occurrences_in_horizon_discards_pending_output():
    source = b"often * * * * *\nrare 0 0 29 2 *\n"
    expect(invoke(source, "--after", "2096-03-01T00:00", "--count", "20"), 1, b"", b"cron:2:1: not enough occurrences in search horizon\n")


def test_record_limit_precedes_tabs_and_other_line_errors():
    lines = b"".join(f"n{i} * * * * *\n".encode("ascii") for i in range(1000))
    expect(invoke(lines + b"\tbad\n"), 1, b"", b"cron:1001:1: too many schedules\n")


def test_input_size_limit_precedes_ascii_validation():
    data = b"?" * 1_048_577
    expect(invoke(data), 1, b"", b"cron: input too large\n")
