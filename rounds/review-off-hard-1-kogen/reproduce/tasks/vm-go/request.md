# Bounded stack virtual machine

Implement `kogen-vm`, a small command-line interpreter for a stack program. Keep parsing and execution in an in-process module called by the CLI. All behavior below is language neutral. `make build` must create the executable used by `./run`; `./run` forwards arguments and streams without building. `make check` must run the provided stack checks. Builds and checks must work offline.

## Command line

`kogen-vm --help` as the only argument prints exactly the following bytes to stdout, including the final LF, exits 0, and reads no input:

```text
Usage: kogen-vm [--steps N] [--stack N] [FILE|-]
Run a bounded integer stack program.
Options:
  --steps N    Maximum instructions executed (default 10000).
  --stack N    Maximum stack depth (default 256).
  --help       Show this help.
```

Unless that sole help argument is present, scan arguments from left to right and stop at the first argument error before reading input. `--steps` and `--stack` may each appear at most once. On a duplicate, report the duplicate before checking whether that occurrence has a value. Each option consumes the next token as its value even when it begins with `-`. A missing value gives exactly `vm: option '--steps' requires a value` or `vm: option '--stack' requires a value`, followed by one LF. A value must consist of one or more ASCII decimal digits; otherwise give exactly `vm: invalid value for '--steps': 'VALUE'` or `vm: invalid value for '--stack': 'VALUE'`, followed by one LF. Parse these values in base 10. `--steps` must be from 1 through 100000 inclusive, and `--stack` must be from 1 through 4096 inclusive; an out-of-range value gives exactly `vm: value out of range for '--steps': 'VALUE'` or `vm: value out of range for '--stack': 'VALUE'`, followed by one LF. Leading zeroes in option values are accepted.

Any unrecognized token beginning with `-`, except the single token `-`, gives exactly `vm: unknown option 'TOKEN'` followed by LF. Every other token is an input path; a second path gives exactly `vm: expected at most one input path` followed by LF. These argument errors exit 2 with empty stdout. With no path or path `-`, read standard input. With any other path, read that file. A file read failure gives exactly `vm: cannot read input` followed by LF and exits 1. Read the selected input completely before parsing. Every error has empty stdout and exactly one stderr line ending in LF. Success exits 0 with empty stderr.

For every duplicate option, the exact stderr bytes are the option-specific `vm: duplicate option '--steps'` or `vm: duplicate option '--stack'` line above, followed by one LF.
A duplicate `--steps` gives exactly `vm: duplicate option '--steps'` followed by LF, and a duplicate `--stack` gives exactly `vm: duplicate option '--stack'` followed by LF; report a duplicate before checking whether that occurrence has a value.

The default step limit is 10000 and the default stack limit is 256. The input limit is 1,048,576 bytes; a larger input gives exactly `vm: input too large` followed by LF and exit 1. The size check happens before line normalization or ASCII validation.

Every source diagnostic prints LINE as a base-10 integer in 1..1,048,577 and COL as a base-10 integer in 1..1,048,576, with no leading zeroes.

## Source bytes and parsing

Input is ASCII bytes with LF or CRLF line endings. Remove a CR immediately before LF and remove one final CR at end of input. Line numbers and byte columns are one-based and counted after this removal. A final LF creates a final empty physical line. Before examining line grammar, scan the entire normalized input in line order and then byte-column order for non-ASCII bytes. The first such byte gives exactly `vm:LINE:COL: expected ASCII` followed by LF and exit 1; this whole-input check takes precedence over every source-line error.

Process physical lines from top to bottom. An empty line, a line containing only ASCII spaces or tabs, or a line whose first non-space-or-tab byte is `#` is ignored. Ignored comment lines may contain tabs. After those ignored-line checks, the 10000-record limit is checked: if 10000 non-ignored source records have already been counted, the next non-ignored line gives `vm:LINE:1: too many records` before any other check of that line. A source record is any non-ignored line, including a label. On every remaining line, the first tab is rejected before parsing with `vm:LINE:COL: tab is not allowed`, where COL is the first tab's one-based byte column. Leading ASCII spaces are allowed and do not change the token columns reported below.

After leading spaces, a comment marker is recognized only when it is the first byte of the line or is preceded by one or more spaces. Such a marker and the rest of that line are ignored. Thus `PUSH 4 # note` is valid, while `PUSH 4#note` is not a comment. After removing an allowed comment suffix and surrounding spaces, split the remaining text into tokens at one or more ASCII spaces.

A label record contains exactly one token matching `[a-z][a-z0-9_]{0,15}:`; the colon is part of the token and is not part of the label name. A label maps to the instruction immediately following it, including the position just beyond the final instruction. A label record with extra tokens gives `wrong operand count` at the first token's column. A one-token record ending in `:` but not matching the label pattern gives `invalid label` at that token's first byte column.

Instruction names are case-sensitive uppercase words. The accepted instructions and their exact operand counts are `PUSH INTEGER`, `DUP`, `DROP`, `SWAP`, `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `OUT`, `JMP LABEL`, `JZ LABEL`, and `HALT`. An unknown instruction gives `unknown instruction` at the first token's column. A known instruction with the wrong number of operands gives `wrong operand count` at the instruction token's column. A label operand must match `[a-z][a-z0-9_]{0,15}`; otherwise give `invalid label` at the operand's column.

An INTEGER is an optional `+` or `-` followed by one or more ASCII digits. Leading zeroes and a leading plus are accepted. Its value must be in -999999999 through 999999999 inclusive. A token not matching the grammar gives `invalid integer` at the INTEGER token's column. A matching token outside that range gives `integer out of range` at that column. All error messages in this section are emitted as exactly `vm:LINE:COL: MESSAGE` followed by LF, exit 1, and empty stdout.

Parse every source record before resolving labels or executing. If any source record has a syntax error, report the first syntax error in source order. If syntax is valid, report the first duplicate label in source order as `duplicate label` at the duplicate label token's column. If there are no duplicate labels, report the first unresolved `JMP` or `JZ` target in instruction source order as `unknown label` at its operand column. These label checks happen before execution, even if a prior `HALT` or unconditional jump would make the bad instruction unreachable. The first duplicate-label check takes precedence over every unresolved-target check.

## Execution

The stack starts empty. Instructions execute in source order, and labels do not execute. Falling past the last instruction succeeds. `HALT` succeeds immediately and skips all remaining instructions. The parser and label checks still apply to instructions after `HALT`.

`PUSH` adds its integer to the top of the stack. `DUP` copies the top value. `DROP` removes the top value. `SWAP` exchanges the top two values. `ADD`, `SUB`, `MUL`, `DIV`, and `MOD` pop the right operand first and then the left operand, compute left operator right, and push the result. `OUT` pops one value and appends its decimal representation followed by one LF to the program output. `JMP` sets the instruction position to its label. `JZ` pops one value and sets the instruction position to its label only when that value is zero; otherwise it continues with the next instruction. A jump to the position after the last instruction succeeds by falling off the program.

Before an instruction that needs more stack values runs, check its full required operand count. If the stack is too short, report `stack underflow` at that instruction's first token column. `DUP` and `OUT` require one value; `DROP` requires one stack value; `SWAP` and all five arithmetic instructions require two; `JZ` requires one; `JMP`, `PUSH`, and `HALT` require none. Before `PUSH` or `DUP` adds a value, if the stack is already at the selected stack limit, report `stack overflow` at that instruction's first token column. A failed instruction does not produce output. Any runtime error discards all output produced earlier in that run.

Division by zero is checked after the two-operand underflow check and gives `division by zero` at the `DIV` instruction's first token column. `DIV` rounds its quotient toward zero. `MOD` uses that same quotient, so its result is `left - quotient * right` and has the sign of the left operand or is zero. For every arithmetic operation, calculate using exact integers; if its result is outside -999999999 through 999999999 inclusive, report `integer overflow` at the operator instruction's first token column. A zero divisor for `MOD` gives `division by zero` at the `MOD` instruction's first token column.

Count each executed instruction, including `HALT`, jumps, and instructions that then fail. Labels do not count. Before executing an instruction, if the number already executed equals the selected step limit, report `step limit exceeded` at the next instruction's first token column. Reaching the end of the program or executing `HALT` on the last allowed step succeeds.

Every runtime error is emitted as exactly `vm:LINE:COL: MESSAGE` followed by LF, exits 1, and has empty stdout. Every integer printed by `OUT` uses base-10 digits, an optional minus only for negative values, and no leading zeroes except that zero is printed as `0`. Every printed integer is in -999999999 through 999999999. Each output line has exactly one LF. With no executed `OUT`, successful stdout is empty.

## Build checks

Stack: Go.
Build: `make build`.
Checks: `make check` runs gofmt, go vet, go test.
