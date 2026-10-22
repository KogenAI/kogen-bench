import os
import subprocess


BIN = os.environ["KOGEN_TASK_BIN"]
HELP = (
    b"Usage: kogen-vm [--steps N] [--stack N] [FILE|-]\n"
    b"Run a bounded integer stack program.\nOptions:\n"
    b"  --steps N    Maximum instructions executed (default 10000).\n"
    b"  --stack N    Maximum stack depth (default 256).\n"
    b"  --help       Show this help.\n"
)


def invoke(data=b"", *args):
    return subprocess.run(
        [BIN, *map(str, args)], input=data, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=15, check=False,
    )


def expect(result, code, stdout, stderr=b""):
    assert (result.returncode, result.stdout, result.stderr) == (code, stdout, stderr)


def test_help_is_exact_and_does_not_read_input():
    expect(invoke(b"BOGUS\n", "--help"), 0, HELP)


def test_duplicate_steps_precedes_missing_value():
    expect(invoke(b"", "--steps", "1", "--steps"), 2, b"", b"vm: duplicate option '--steps'\n")


def test_duplicate_stack_precedes_missing_value():
    expect(invoke(b"", "--stack", "1", "--stack"), 2, b"", b"vm: duplicate option '--stack'\n")


def test_options_consume_tokens_starting_with_dash():
    expect(invoke(b"", "--steps", "-x"), 2, b"", b"vm: invalid value for '--steps': '-x'\n")


def test_missing_and_malformed_option_values():
    expect(invoke(b"", "--steps"), 2, b"", b"vm: option '--steps' requires a value\n")
    expect(invoke(b"", "--stack", "+2"), 2, b"", b"vm: invalid value for '--stack': '+2'\n")


def test_option_ranges_and_leading_zeroes():
    expect(invoke(b"PUSH 1\nOUT\n", "--steps", "0002"), 0, b"1\n")
    expect(invoke(b"", "--steps", "0"), 2, b"", b"vm: value out of range for '--steps': '0'\n")
    expect(invoke(b"", "--stack", "4097"), 2, b"", b"vm: value out of range for '--stack': '4097'\n")


def test_unknown_option_and_second_path_are_argument_errors(tmp_path):
    expect(invoke(b"", "--wat"), 2, b"", b"vm: unknown option '--wat'\n")
    expect(invoke(b"", str(tmp_path / "one"), str(tmp_path / "two")), 2, b"", b"vm: expected at most one input path\n")


def test_dash_path_reads_stdin_and_a_file_path_reads_the_file(tmp_path):
    path = tmp_path / "program.vm"
    path.write_bytes(b"PUSH 5\nOUT\n")
    expect(invoke(b"PUSH 4\nOUT\n", "-"), 0, b"4\n")
    expect(invoke(b"", str(path)), 0, b"5\n")


def test_file_read_failure_has_stable_error(tmp_path):
    missing = tmp_path / "missing" / "program.vm"
    expect(invoke(b"", str(missing)), 1, b"", b"vm: cannot read input\n")


def test_binary_arithmetic_operand_order_and_output_format():
    source = b"PUSH 20\nPUSH 6\nSUB\nOUT\nPUSH 20\nPUSH 6\nDIV\nOUT\nPUSH 20\nPUSH 6\nMOD\nOUT\n"
    expect(invoke(source), 0, b"14\n3\n2\n")


def test_multiplication_addition_and_canonical_zero():
    source = b"PUSH 0002\nPUSH +3\nMUL\nOUT\nPUSH 2\nPUSH 3\nADD\nOUT\nPUSH -0\nOUT\n"
    expect(invoke(source), 0, b"6\n5\n0\n")


def test_division_and_remainder_truncate_toward_zero():
    source = b"PUSH -7\nPUSH 3\nDIV\nOUT\nPUSH -7\nPUSH 3\nMOD\nOUT\n"
    expect(invoke(source), 0, b"-2\n-1\n")


def test_stack_manipulation_instructions():
    source = b"PUSH 4\nDUP\nPUSH 9\nSWAP\nDROP\nOUT\nOUT\n"
    expect(invoke(source), 0, b"9\n4\n")


def test_jz_takes_the_zero_branch_and_pops_its_condition():
    source = b"PUSH 10\nPUSH 0\nJZ yes\nPUSH 99\nOUT\nyes:\nPUSH 2\nADD\nOUT\n"
    expect(invoke(source), 0, b"12\n")


def test_jz_nonzero_falls_through():
    source = b"PUSH 10\nPUSH -2\nJZ skipped\nPUSH 2\nADD\nOUT\nJMP end\nskipped:\nPUSH 9\nOUT\nend:\n"
    expect(invoke(source), 0, b"12\n")


def test_jump_to_end_and_halt_keep_prior_output_only():
    expect(invoke(b"PUSH 3\nOUT\nJMP end\nPUSH 4\nOUT\nend:\n"), 0, b"3\n")
    expect(invoke(b"PUSH 5\nOUT\nHALT\nPUSH 6\nOUT\n"), 0, b"5\n")


def test_parse_and_label_validation_reaches_code_after_halt():
    expect(invoke(b"HALT\nBOGUS\n"), 1, b"", b"vm:2:1: unknown instruction\n")
    expect(invoke(b"HALT\nJMP absent\n"), 1, b"", b"vm:2:5: unknown label\n")


def test_duplicate_label_precedes_unresolved_target():
    source = b"JMP absent\nsame:\nsame:\n"
    expect(invoke(source), 1, b"", b"vm:3:1: duplicate label\n")


def test_syntax_error_precedes_duplicate_label():
    source = b"same:\nsame:\nNOPE\n"
    expect(invoke(source), 1, b"", b"vm:3:1: unknown instruction\n")


def test_comments_and_blank_lines_are_ignored_but_adjacent_hash_is_not():
    source = b" \t# ignored\n\nPUSH 4 # note\nOUT\n"
    expect(invoke(source), 0, b"4\n")
    expect(invoke(b"PUSH 4#note\n"), 1, b"", b"vm:1:6: invalid integer\n")


def test_tabs_on_code_lines_are_rejected_before_instruction_parsing():
    expect(invoke(b"PUSH\t1\n"), 1, b"", b"vm:1:5: tab is not allowed\n")


def test_non_ascii_scan_precedes_an_earlier_syntax_error():
    expect(invoke(b"BOGUS\na\xff\n"), 1, b"", b"vm:2:2: expected ASCII\n")


def test_crlf_and_one_final_cr_are_normalized_for_columns():
    expect(invoke(b"PUSH 2\r\nOUT\r"), 0, b"2\n")


def test_leading_spaces_are_allowed_and_columns_are_source_columns():
    expect(invoke(b"   WHAT\n"), 1, b"", b"vm:1:4: unknown instruction\n")


def test_invalid_and_out_of_range_integer_literals():
    for literal in (b"+", b"1.0", b"--1"):
        expect(invoke(b"PUSH " + literal + b"\n"), 1, b"", b"vm:1:6: invalid integer\n")
    expect(invoke(b"PUSH\n"), 1, b"", b"vm:1:1: wrong operand count\n")
    expect(invoke(b"PUSH 1000000000\n"), 1, b"", b"vm:1:6: integer out of range\n")


def test_integer_overflow_discards_earlier_output():
    source = b"PUSH 1\nOUT\nPUSH 999999999\nPUSH 1\nADD\n"
    expect(invoke(source), 1, b"", b"vm:5:1: integer overflow\n")


def test_all_instructions_check_underflow_before_other_runtime_errors():
    for instruction in (b"DUP", b"DROP", b"OUT"):
        expect(invoke(instruction + b"\n"), 1, b"", b"vm:1:1: stack underflow\n")
    expect(invoke(b"JZ target\ntarget:\n"), 1, b"", b"vm:1:1: stack underflow\n")
    for instruction in (b"SWAP", b"ADD", b"SUB", b"MUL", b"DIV", b"MOD"):
        expect(invoke(instruction + b"\n"), 1, b"", b"vm:1:1: stack underflow\n")


def test_division_and_modulo_by_zero_have_exact_runtime_error():
    for instruction in (b"DIV", b"MOD"):
        expect(invoke(b"PUSH 8\nPUSH 0\n" + instruction + b"\n"), 1, b"", b"vm:3:1: division by zero\n")


def test_configured_stack_depth_and_dup_limit():
    expect(invoke(b"PUSH 1\nPUSH 2\nOUT\nOUT\n", "--stack", "1"), 1, b"", b"vm:2:1: stack overflow\n")
    expect(invoke(b"PUSH 1\nDUP\n", "--stack", "1"), 1, b"", b"vm:2:1: stack overflow\n")


def test_default_stack_limit_is_256():
    fill = b"PUSH 0\n" * 256
    expect(invoke(fill + b"OUT\n" * 256), 0, b"0\n" * 256)
    expect(invoke(fill + b"PUSH 0\n"), 1, b"", b"vm:257:1: stack overflow\n")


def test_step_limit_fails_before_next_instruction_and_discards_output():
    source = b"PUSH 1\nOUT\nPUSH 2\nOUT\n"
    expect(invoke(source, "--steps", "2"), 1, b"", b"vm:3:1: step limit exceeded\n")


def test_exact_step_limit_succeeds_when_program_ends_or_halts():
    expect(invoke(b"PUSH 1\nOUT\n", "--steps", "2"), 0, b"1\n")
    expect(invoke(b"PUSH 2\nOUT\nHALT\n", "--steps", "3"), 0, b"2\n")


def test_default_step_limit_is_10000():
    exactly_10000 = (
        b"PUSH 1249\nloop:\nDUP\nPUSH 1\nSUB\nSWAP\nDROP\nDUP\nJZ done\nJMP loop\n"
        b"done:\nPUSH 0\nDROP\nPUSH 0\nDROP\nPUSH 0\nDROP\nJMP finish\nfinish:\nDROP\n"
    )
    expect(invoke(exactly_10000), 0, b"")
    expect(invoke(exactly_10000 + b"PUSH 0\n"), 1, b"", b"vm:21:1: step limit exceeded\n")


def test_loop_is_stopped_at_the_selected_step_limit():
    source = b"loop:\nJMP loop\n"
    expect(invoke(source, "--steps", "5"), 1, b"", b"vm:2:1: step limit exceeded\n")


def test_record_limit_precedes_tab_and_grammar_checks():
    lines = b"".join(f"n{i}:\n".encode("ascii") for i in range(10000))
    expect(invoke(lines + b"\tBOGUS\n"), 1, b"", b"vm:10001:1: too many records\n")


def test_input_size_limit_is_checked_before_source_validation():
    data = b"?" * 1_048_577
    expect(invoke(data), 1, b"", b"vm: input too large\n")
