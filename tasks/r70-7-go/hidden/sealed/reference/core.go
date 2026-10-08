package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

const help = "Usage: kogen <command> [options] [FILE|-]\nCommands:\n  sum     Sum signed integers.\n  status  Count job states.\nOptions:\n  -h, --help  Show help.\n  --version   Show version.\n"
const sumHelp = "Usage: kogen sum [--scale N] [--format text|json] [FILE|-]\nSum one signed integer per nonempty line (default scale: 1).\n"
const statusHelp = "Usage: kogen status [--format text|json] [FILE|-]\nCount ID,STATE records (states: queued,running,done,failed).\n"

var scalePattern = regexp.MustCompile(`^(0|[1-9][0-9]*)$`)
var numberPattern = regexp.MustCompile(`^[+-]?[0-9]+$`)
var recordPattern = regexp.MustCompile(`^([a-z][a-z0-9_-]{0,31}),(queued|running|done|failed)$`)

type options struct {
	command, format, path string
	scale                 int64
	hasPath               bool
}

func parseOptions(args []string) (options, string, error) {
	opts := options{format: "text", scale: 1}
	if len(args) == 0 || len(args) == 1 && (args[0] == "--help" || args[0] == "-h") {
		return opts, help, nil
	}
	if len(args) == 1 && args[0] == "--version" {
		return opts, "kogen 1.0.0\n", nil
	}
	opts.command = args[0]
	if opts.command != "sum" && opts.command != "status" {
		kind := "command"
		if strings.HasPrefix(args[0], "-") {
			kind = "option"
		}
		return opts, "", fmt.Errorf("kogen: unknown %s '%s'", kind, args[0])
	}
	if len(args) == 2 && (args[1] == "--help" || args[1] == "-h") {
		if opts.command == "sum" {
			return opts, sumHelp, nil
		}
		return opts, statusHelp, nil
	}
	seen := map[string]bool{}
	hasPath := false
	for i := 1; i < len(args); i++ {
		arg := args[i]
		switch {
		case arg == "--format" || (arg == "--scale" && opts.command == "sum"):
			if seen[arg] {
				return opts, "", fmt.Errorf("kogen: duplicate option '%s'", arg)
			}
			seen[arg] = true
			i++
			if i == len(args) {
				return opts, "", fmt.Errorf("kogen: option '%s' requires a value", arg)
			}
			value := args[i]
			valid := false
			if arg == "--format" {
				valid = value == "text" || value == "json"
				opts.format = value
			} else {
				n, err := strconv.ParseInt(value, 10, 64)
				valid = scalePattern.MatchString(value) && err == nil && n >= 0 && n <= 100
				opts.scale = n
			}
			if !valid {
				return opts, "", fmt.Errorf("kogen: invalid value for '%s': '%s'", arg, value)
			}
		case strings.HasPrefix(arg, "-") && arg != "-":
			return opts, "", fmt.Errorf("kogen: unknown option '%s'", arg)
		default:
			if hasPath {
				return opts, "", fmt.Errorf("kogen: expected at most one input path")
			}
			opts.path = arg
			opts.hasPath = true
			hasPath = true
		}
	}
	return opts, "", nil
}

func execute(args []string) (string, int, error) {
	opts, early, err := parseOptions(args)
	if err != nil {
		return "", 2, err
	}
	if early != "" {
		return early, 0, nil
	}
	raw, err := Load(opts.path, opts.hasPath, "kogen")
	if err != nil {
		return "", 1, err
	}
	for _, b := range raw {
		if b > 127 {
			return "", 1, fmt.Errorf("kogen: input is not ASCII")
		}
	}
	out, err := aggregate(physicalLines(raw), opts)
	if err != nil {
		return "", 1, err
	}
	return out, 0, nil
}

func aggregate(lines []string, opts options) (string, error) {
	if opts.command == "sum" {
		var total int64
		for i, line := range lines {
			if line == "" {
				continue
			}
			magnitude := strings.TrimLeft(strings.TrimLeft(line, "+-"), "0")
			if magnitude == "" {
				magnitude = "0"
			}
			n, err := strconv.ParseInt(magnitude, 10, 64)
			if !numberPattern.MatchString(line) || err != nil || n > 1000000 {
				return "", fmt.Errorf("kogen:%d: expected integer -1000000..1000000", i+1)
			}
			if strings.HasPrefix(line, "-") {
				n = -n
			}
			total += n
		}
		total *= opts.scale
		if opts.format == "json" {
			return fmt.Sprintf("{\"sum\":%d}\n", total), nil
		}
		return fmt.Sprintf("sum=%d\n", total), nil
	}
	counts := map[string]int{"queued": 0, "running": 0, "done": 0, "failed": 0}
	ids := map[string]bool{}
	for i, line := range lines {
		if line == "" {
			continue
		}
		match := recordPattern.FindStringSubmatch(line)
		if match == nil {
			return "", fmt.Errorf("kogen:%d: expected ID,STATE", i+1)
		}
		id, state := match[1], match[2]
		if ids[id] {
			return "", fmt.Errorf("kogen:%d: duplicate id '%s'", i+1, id)
		}
		ids[id] = true
		counts[state]++
	}
	total := len(ids)
	if opts.format == "json" {
		return fmt.Sprintf("{\"total\":%d,\"queued\":%d,\"running\":%d,\"done\":%d,\"failed\":%d}\n", total, counts["queued"], counts["running"], counts["done"], counts["failed"]), nil
	}
	return fmt.Sprintf("total=%d\nqueued=%d\nrunning=%d\ndone=%d\nfailed=%d\n", total, counts["queued"], counts["running"], counts["done"], counts["failed"]), nil
}
