package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

const help = "Usage: kogen-config [FILE|-]\nParse a strict YAML-subset configuration from FILE or stdin.\nOptions:\n  --help  Show this help.\n"

var keyPattern = regexp.MustCompile(`^([a-z][a-z_]*):`)
var barePattern = regexp.MustCompile(`^[A-Za-z0-9 _./:#-]+$`)
var workerPattern = regexp.MustCompile(`^[1-9][0-9]*$`)

func execute(args []string) (string, int, error) {
	if len(args) == 1 && args[0] == "--help" {
		return help, 0, nil
	}
	for _, arg := range args {
		if strings.HasPrefix(arg, "-") && arg != "-" {
			return "", 2, fmt.Errorf("config: unknown option '%s'", arg)
		}
	}
	if len(args) > 1 {
		return "", 2, fmt.Errorf("config: expected at most one input path")
	}
	path := ""
	if len(args) == 1 {
		path = args[0]
	}
	raw, err := Load(path, len(args) == 1, "config")
	if err != nil {
		return "", 1, err
	}
	line, col := 1, 1
	for _, b := range raw {
		if b > 127 {
			return "", 1, fmt.Errorf("config:%d:%d: expected ASCII input", line, col)
		}
		if b == '\n' {
			line++
			col = 1
		} else {
			col++
		}
	}
	out, err := parseConfig(physicalLines(raw))
	if err != nil {
		return "", 1, err
	}
	return out, 0, nil
}

func scalar(line string, start int) (string, bool, int, string) {
	col := start + 1
	if start == len(line) || line[start] == '#' {
		return "", false, col, "missing value"
	}
	quote := line[start]
	if quote != '\'' && quote != '"' {
		value := line[start:]
		if at := strings.Index(value, " #"); at >= 0 {
			value = value[:at]
		}
		value = strings.TrimRight(value, " ")
		if !barePattern.MatchString(value) {
			return "", false, col, "invalid bare scalar"
		}
		return value, false, 0, ""
	}
	var value strings.Builder
	pos := start + 1
	closed := false
	for pos < len(line) {
		ch := line[pos]
		if ch == quote {
			if quote == '\'' && pos+1 < len(line) && line[pos+1] == quote {
				value.WriteByte(ch)
				pos += 2
				continue
			}
			pos++
			closed = true
			break
		}
		if ch == '\\' && quote == '"' {
			if pos+1 >= len(line) || (line[pos+1] != '"' && line[pos+1] != '\\') {
				return "", true, pos + 1, "invalid escape"
			}
			value.WriteByte(line[pos+1])
			pos += 2
			continue
		}
		if ch < 32 || ch > 126 {
			return "", true, col, "invalid quoted scalar"
		}
		value.WriteByte(ch)
		pos++
	}
	if !closed {
		return "", true, col, "unterminated quoted scalar"
	}
	end := pos
	for pos < len(line) && line[pos] == ' ' {
		pos++
	}
	if pos < len(line) && (pos <= end || line[pos] != '#') {
		return "", true, pos + 1, "unexpected trailing text"
	}
	return value.String(), true, 0, ""
}

func parseConfig(lines []string) (string, error) {
	values := map[string]string{"name": "kogen", "workers": "1", "enabled": "true", "directory": "."}
	seen := map[string]bool{}
	for i, line := range lines {
		fail := func(col int, message string) (string, error) {
			return "", fmt.Errorf("config:%d:%d: %s", i+1, col, message)
		}
		if at := strings.IndexByte(line, '\t'); at >= 0 {
			return fail(at+1, "tab is not allowed")
		}
		trim := strings.TrimLeft(line, " ")
		if trim == "" || strings.HasPrefix(trim, "#") {
			continue
		}
		if line[0] == ' ' {
			return fail(1, "unexpected indentation")
		}
		match := keyPattern.FindStringSubmatch(line)
		if match == nil {
			return fail(1, "expected key: value")
		}
		key := match[1]
		if _, ok := values[key]; !ok {
			return fail(1, fmt.Sprintf("unknown key '%s'", key))
		}
		if seen[key] {
			return fail(1, fmt.Sprintf("duplicate key '%s'", key))
		}
		seen[key] = true
		start := len(match[0])
		for start < len(line) && line[start] == ' ' {
			start++
		}
		value, quoted, col, message := scalar(line, start)
		if message != "" {
			return fail(col, message)
		}
		switch key {
		case "workers":
			n, err := strconv.Atoi(value)
			if quoted || !workerPattern.MatchString(value) || err != nil || n < 1 || n > 64 {
				return fail(start+1, "expected integer 1..64")
			}
			value = strconv.Itoa(n)
		case "enabled":
			if quoted || (value != "true" && value != "false") {
				return fail(start+1, "expected true or false")
			}
		default:
			if value == "" {
				return fail(start+1, "expected nonempty string")
			}
		}
		values[key] = value
	}
	return fmt.Sprintf("name=%s\nworkers=%s\nenabled=%s\ndirectory=%s\n", values["name"], values["workers"], values["enabled"], values["directory"]), nil
}
