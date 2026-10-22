package main

import (
	"fmt"
	"strconv"
	"strings"
)

const vmHelp = "Usage: kogen-vm [--steps N] [--stack N] [FILE|-]\n" +
	"Run a bounded integer stack program.\nOptions:\n" +
	"  --steps N    Maximum instructions executed (default 10000).\n" +
	"  --stack N    Maximum stack depth (default 256).\n" +
	"  --help       Show this help.\n"

type sourceError struct {
	line int
	col  int
	msg  string
}

func (e sourceError) Error() string { return fmt.Sprintf("vm:%d:%d: %s", e.line, e.col, e.msg) }

type instruction struct {
	op     string
	value  int64
	label  string
	line   int
	col    int
	argCol int
}

type labelTarget struct {
	pc   int
	line int
	col  int
}

func execute(args []string) (string, int, error) {
	stepsLimit := 10000
	stackLimit := 256
	seenSteps := false
	seenStack := false
	path := ""
	hasPath := false

	for i := 0; i < len(args); i++ {
		arg := args[i]
		switch arg {
		case "--help":
			if len(args) == 1 {
				return vmHelp, 0, nil
			}
			return "", 2, fmt.Errorf("vm: unknown option '--help'")
		case "--steps", "--stack":
			isSteps := arg == "--steps"
			if isSteps && seenSteps {
				return "", 2, fmt.Errorf("vm: duplicate option '--steps'")
			}
			if !isSteps && seenStack {
				return "", 2, fmt.Errorf("vm: duplicate option '--stack'")
			}
			if isSteps {
				seenSteps = true
			} else {
				seenStack = true
			}
			if i+1 >= len(args) {
				return "", 2, fmt.Errorf("vm: option '%s' requires a value", arg)
			}
			i++
			value := args[i]
			if !decimalDigits(value) {
				return "", 2, fmt.Errorf("vm: invalid value for '%s': '%s'", arg, value)
			}
			parsed, err := strconv.ParseUint(value, 10, 64)
			if err != nil {
				return "", 2, fmt.Errorf("vm: value out of range for '%s': '%s'", arg, value)
			}
			if isSteps {
				if parsed < 1 || parsed > 100000 {
					return "", 2, fmt.Errorf("vm: value out of range for '--steps': '%s'", value)
				}
				stepsLimit = int(parsed)
			} else {
				if parsed < 1 || parsed > 4096 {
					return "", 2, fmt.Errorf("vm: value out of range for '--stack': '%s'", value)
				}
				stackLimit = int(parsed)
			}
		default:
			if strings.HasPrefix(arg, "-") && arg != "-" {
				return "", 2, fmt.Errorf("vm: unknown option '%s'", arg)
			}
			if hasPath {
				return "", 2, fmt.Errorf("vm: expected at most one input path")
			}
			path, hasPath = arg, true
		}
	}

	data, err := Load(path, hasPath, "vm")
	if err != nil {
		return "", 1, err
	}
	if len(data) > 1_048_576 {
		return "", 1, fmt.Errorf("vm: input too large")
	}

	program, targets, err := parseProgram(data)
	if err != nil {
		return "", 1, err
	}
	return runProgram(program, targets, stepsLimit, stackLimit)
}

func decimalDigits(value string) bool {
	if value == "" {
		return false
	}
	for i := 0; i < len(value); i++ {
		if value[i] < '0' || value[i] > '9' {
			return false
		}
	}
	return true
}

func parseProgram(data []byte) ([]instruction, map[string]int, error) {
	lines := physicalLines(data)
	for lineIndex, line := range lines {
		for col := 0; col < len(line); col++ {
			if line[col] >= 0x80 {
				return nil, nil, sourceError{lineIndex + 1, col + 1, "expected ASCII"}
			}
		}
	}

	program := make([]instruction, 0)
	labels := make(map[string]labelTarget)
	duplicates := make([]sourceError, 0)
	for lineIndex, original := range lines {
		lineNo := lineIndex + 1
		first := firstNonSpaceOrTab(original)
		if first < 0 || original[first] == '#' {
			continue
		}
		if len(program)+len(labels)+len(duplicates) >= 10000 {
			return nil, nil, sourceError{lineNo, 1, "too many records"}
		}
		if tab := strings.IndexByte(original, '\t'); tab >= 0 {
			return nil, nil, sourceError{lineNo, tab + 1, "tab is not allowed"}
		}

		content := stripComment(original)
		tokens := splitTokens(content)
		if len(tokens) == 0 {
			continue
		}
		firstCol := tokens[0].col
		if strings.HasSuffix(tokens[0].text, ":") {
			if len(tokens) != 1 {
				return nil, nil, sourceError{lineNo, firstCol, "wrong operand count"}
			}
			name := strings.TrimSuffix(tokens[0].text, ":")
			if !validLabel(name) {
				return nil, nil, sourceError{lineNo, firstCol, "invalid label"}
			}
			if _, exists := labels[name]; exists {
				duplicates = append(duplicates, sourceError{lineNo, firstCol, "duplicate label"})
			} else {
				labels[name] = labelTarget{len(program), lineNo, firstCol}
			}
			continue
		}

		op := tokens[0].text
		need := 1
		switch op {
		case "PUSH", "JMP", "JZ":
			need = 2
		case "DUP", "DROP", "SWAP", "ADD", "SUB", "MUL", "DIV", "MOD", "OUT", "HALT":
		default:
			return nil, nil, sourceError{lineNo, firstCol, "unknown instruction"}
		}
		if len(tokens) != need {
			return nil, nil, sourceError{lineNo, firstCol, "wrong operand count"}
		}
		inst := instruction{op: op, line: lineNo, col: firstCol}
		if op == "PUSH" {
			value, ok, inRange := parseVMInteger(tokens[1].text)
			if !ok {
				return nil, nil, sourceError{lineNo, tokens[1].col, "invalid integer"}
			}
			if !inRange {
				return nil, nil, sourceError{lineNo, tokens[1].col, "integer out of range"}
			}
			inst.value = value
		} else if op == "JMP" || op == "JZ" {
			if !validLabel(tokens[1].text) {
				return nil, nil, sourceError{lineNo, tokens[1].col, "invalid label"}
			}
			inst.label = tokens[1].text
			inst.argCol = tokens[1].col
		}
		program = append(program, inst)
	}

	if len(duplicates) > 0 {
		return nil, nil, duplicates[0]
	}
	resolved := make(map[string]int, len(labels))
	for name, target := range labels {
		resolved[name] = target.pc
	}
	for _, inst := range program {
		if inst.op == "JMP" || inst.op == "JZ" {
			if _, exists := resolved[inst.label]; !exists {
				return nil, nil, sourceError{inst.line, inst.argCol, "unknown label"}
			}
		}
	}
	return program, resolved, nil
}

type sourceToken struct {
	text string
	col  int
}

func firstNonSpaceOrTab(line string) int {
	for i := 0; i < len(line); i++ {
		if line[i] != ' ' && line[i] != '\t' {
			return i
		}
	}
	return -1
}

func stripComment(line string) string {
	for i := 0; i < len(line); i++ {
		if line[i] == '#' && (i == 0 || line[i-1] == ' ') {
			return strings.TrimRight(line[:i], " ")
		}
	}
	return strings.TrimRight(line, " ")
}

func splitTokens(line string) []sourceToken {
	tokens := make([]sourceToken, 0, 3)
	for i := 0; i < len(line); {
		if line[i] == ' ' {
			i++
			continue
		}
		start := i
		for i < len(line) && line[i] != ' ' {
			i++
		}
		tokens = append(tokens, sourceToken{text: line[start:i], col: start + 1})
	}
	return tokens
}

func validLabel(value string) bool {
	if len(value) < 1 || len(value) > 16 || value[0] < 'a' || value[0] > 'z' {
		return false
	}
	for i := 1; i < len(value); i++ {
		c := value[i]
		if !((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_') {
			return false
		}
	}
	return true
}

func parseVMInteger(token string) (int64, bool, bool) {
	if token == "" {
		return 0, false, false
	}
	negative := false
	start := 0
	if token[0] == '+' || token[0] == '-' {
		negative = token[0] == '-'
		start = 1
	}
	if start == len(token) {
		return 0, false, false
	}
	var value int64
	for i := start; i < len(token); i++ {
		if token[i] < '0' || token[i] > '9' {
			return 0, false, false
		}
		digit := int64(token[i] - '0')
		if value <= 1_000_000_000 {
			value = value*10 + digit
		}
	}
	if value > 999_999_999 {
		return 0, true, false
	}
	if negative {
		value = -value
	}
	return value, true, true
}

func runProgram(program []instruction, labels map[string]int, stepsLimit, stackLimit int) (string, int, error) {
	stack := make([]int64, 0)
	var output strings.Builder
	pc := 0
	steps := 0
	for pc >= 0 && pc < len(program) {
		inst := program[pc]
		if steps == stepsLimit {
			return "", 1, sourceError{inst.line, inst.col, "step limit exceeded"}
		}
		steps++
		underflow := func() (string, int, error) {
			return "", 1, sourceError{inst.line, inst.col, "stack underflow"}
		}
		push := func(value int64) bool {
			if len(stack) >= stackLimit {
				return false
			}
			stack = append(stack, value)
			return true
		}
		switch inst.op {
		case "PUSH":
			if !push(inst.value) {
				return "", 1, sourceError{inst.line, inst.col, "stack overflow"}
			}
		case "DUP":
			if len(stack) < 1 {
				return underflow()
			}
			if !push(stack[len(stack)-1]) {
				return "", 1, sourceError{inst.line, inst.col, "stack overflow"}
			}
		case "DROP":
			if len(stack) < 1 {
				return underflow()
			}
			stack = stack[:len(stack)-1]
		case "SWAP":
			if len(stack) < 2 {
				return underflow()
			}
			top := len(stack) - 1
			stack[top], stack[top-1] = stack[top-1], stack[top]
		case "ADD", "SUB", "MUL", "DIV", "MOD":
			if len(stack) < 2 {
				return underflow()
			}
			top := len(stack) - 1
			right, left := stack[top], stack[top-1]
			if (inst.op == "DIV" || inst.op == "MOD") && right == 0 {
				return "", 1, sourceError{inst.line, inst.col, "division by zero"}
			}
			var value int64
			switch inst.op {
			case "ADD":
				value = left + right
			case "SUB":
				value = left - right
			case "MUL":
				value = left * right
			case "DIV":
				value = left / right
			case "MOD":
				value = left % right
			}
			if value < -999_999_999 || value > 999_999_999 {
				return "", 1, sourceError{inst.line, inst.col, "integer overflow"}
			}
			stack[top-1] = value
			stack = stack[:top]
		case "OUT":
			if len(stack) < 1 {
				return underflow()
			}
			top := len(stack) - 1
			_, _ = fmt.Fprintf(&output, "%d\n", stack[top])
			stack = stack[:top]
		case "JMP":
			pc = labels[inst.label]
			continue
		case "JZ":
			if len(stack) < 1 {
				return underflow()
			}
			top := len(stack) - 1
			condition := stack[top]
			stack = stack[:top]
			if condition == 0 {
				pc = labels[inst.label]
				continue
			}
		case "HALT":
			return output.String(), 0, nil
		}
		pc++
	}
	return output.String(), 0, nil
}
