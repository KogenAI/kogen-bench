package main

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

const cronHelp = "Usage: kogen-cron [--after YYYY-MM-DDTHH:MM] [--count N] [--format text|json] [FILE|-]\n" +
	"Find upcoming UTC minutes for named cron expressions.\nOptions:\n" +
	"  --after VALUE    Exclusive UTC starting minute (default 2000-01-01T00:00).\n" +
	"  --count N        Occurrences per expression (default 3; range 1..20).\n" +
	"  --format FORMAT  Output text (default) or json.\n" +
	"  --help           Show this help.\n"

type cronError struct {
	line int
	col  int
	msg  string
}

func (e cronError) Error() string { return fmt.Sprintf("cron:%d:%d: %s", e.line, e.col, e.msg) }

type cronOptions struct {
	after   int64
	count   int
	format  string
	path    string
	hasPath bool
}

type cronField struct {
	selected [60]bool
	min      int
	max      int
	wildcard bool
}

type schedule struct {
	name   string
	fields [5]cronField
	line   int
	col    int
}

func execute(args []string) (string, int, error) {
	options, help, err := parseCronArgs(args)
	if err != nil {
		return "", 2, err
	}
	if help {
		return cronHelp, 0, nil
	}

	data, err := Load(options.path, options.hasPath, "cron")
	if err != nil {
		return "", 1, err
	}
	if len(data) > 1_048_576 {
		return "", 1, fmt.Errorf("cron: input too large")
	}

	schedules, err := parseSchedules(data)
	if err != nil {
		return "", 1, err
	}
	seen := make(map[string]bool)
	for _, item := range schedules {
		if seen[item.name] {
			return "", 1, cronError{item.line, item.col, "duplicate name"}
		}
		seen[item.name] = true
	}

	runResults := make([][]int64, 0, len(schedules))
	for i := range schedules {
		runs := findRuns(schedules[i], options.after, options.count)
		if len(runs) != options.count {
			return "", 1, cronError{schedules[i].line, 1, "not enough occurrences in search horizon"}
		}
		runResults = append(runResults, runs)
	}
	return renderSchedules(schedules, runResults, options.format), 0, nil
}

func parseCronArgs(args []string) (cronOptions, bool, error) {
	options := cronOptions{after: parseAnchor(), count: 3, format: "text"}
	seen := map[string]bool{}
	paths := 0
	for i := 0; i < len(args); i++ {
		arg := args[i]
		if arg == "--help" {
			if len(args) == 1 {
				return options, true, nil
			}
			return options, false, fmt.Errorf("cron: unknown option '--help'")
		}
		if arg == "--after" || arg == "--count" || arg == "--format" {
			if seen[arg] {
				return options, false, fmt.Errorf("cron: duplicate option '%s'", arg)
			}
			seen[arg] = true
			if i+1 >= len(args) {
				return options, false, fmt.Errorf("cron: option '%s' requires a value", arg)
			}
			i++
			value := args[i]
			switch arg {
			case "--after":
				minute, ok := parseTimestamp(value)
				if !ok {
					return options, false, fmt.Errorf("cron: invalid value for '--after': '%s'", value)
				}
				options.after = minute
			case "--count":
				if !decimalDigits(value) {
					return options, false, fmt.Errorf("cron: invalid value for '--count': '%s'", value)
				}
				count, err := strconv.ParseUint(value, 10, 64)
				if err != nil || count < 1 || count > 20 {
					return options, false, fmt.Errorf("cron: value out of range for '--count': '%s'", value)
				}
				options.count = int(count)
			case "--format":
				if value != "text" && value != "json" {
					return options, false, fmt.Errorf("cron: invalid value for '--format': '%s'", value)
				}
				options.format = value
			}
			continue
		}
		if strings.HasPrefix(arg, "-") && arg != "-" {
			return options, false, fmt.Errorf("cron: unknown option '%s'", arg)
		}
		paths++
		if paths > 1 {
			return options, false, fmt.Errorf("cron: expected at most one input path")
		}
		options.path, options.hasPath = arg, true
	}
	return options, false, nil
}

func parseAnchor() int64 {
	t, _ := time.Parse("2006-01-02T15:04", "2000-01-01T00:00")
	return t.Unix() / 60
}

func parseTimestamp(value string) (int64, bool) {
	if len(value) != 16 || value[4] != '-' || value[7] != '-' || value[10] != 'T' || value[13] != ':' {
		return 0, false
	}
	for i := 0; i < len(value); i++ {
		if i == 4 || i == 7 || i == 10 || i == 13 {
			continue
		}
		if value[i] < '0' || value[i] > '9' {
			return 0, false
		}
	}
	t, err := time.Parse("2006-01-02T15:04", value)
	if err != nil || t.Year() < 1970 || t.Year() > 2190 || t.Format("2006-01-02T15:04") != value {
		return 0, false
	}
	return t.Unix() / 60, true
}

func parseSchedules(data []byte) ([]schedule, error) {
	lines := physicalLines(data)
	for lineIndex, line := range lines {
		for col := 0; col < len(line); col++ {
			if line[col] >= 0x80 {
				return nil, cronError{lineIndex + 1, col + 1, "expected ASCII"}
			}
		}
	}

	result := make([]schedule, 0)
	for lineIndex, line := range lines {
		lineNo := lineIndex + 1
		first := firstNonSpaceOrTab(line)
		if first < 0 || line[first] == '#' {
			continue
		}
		if len(result) >= 1000 {
			return nil, cronError{lineNo, 1, "too many schedules"}
		}
		if tab := strings.IndexByte(line, '\t'); tab >= 0 {
			return nil, cronError{lineNo, tab + 1, "tab is not allowed"}
		}
		tokens := splitCronTokens(line)
		if len(tokens) != 6 {
			return nil, cronError{lineNo, first + 1, "wrong field count"}
		}
		name := tokens[0].text
		if !validName(name) {
			return nil, cronError{lineNo, tokens[0].col, "invalid name"}
		}
		item := schedule{name: name, line: lineNo, col: tokens[0].col}
		fieldKinds := [5]string{"minute", "hour", "day-of-month", "month", "day-of-week"}
		mins := [5]int{0, 0, 1, 1, 0}
		maxs := [5]int{59, 23, 31, 12, 7}
		for fieldIndex := 0; fieldIndex < 5; fieldIndex++ {
			field, ok := parseCronField(tokens[fieldIndex+1].text, mins[fieldIndex], maxs[fieldIndex], fieldIndex == 4)
			if !ok {
				return nil, cronError{lineNo, tokens[fieldIndex+1].col, "invalid " + fieldKinds[fieldIndex] + " field"}
			}
			item.fields[fieldIndex] = field
		}
		result = append(result, item)
	}
	return result, nil
}

type cronToken struct {
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

func splitCronTokens(line string) []cronToken {
	start := 0
	for start < len(line) && line[start] == ' ' {
		start++
	}
	end := len(line)
	for end > start && line[end-1] == ' ' {
		end--
	}
	tokens := make([]cronToken, 0, 6)
	for i := start; i < end; {
		wordStart := i
		for i < end && line[i] != ' ' {
			i++
		}
		tokens = append(tokens, cronToken{line[wordStart:i], wordStart + 1})
		for i < end && line[i] == ' ' {
			i++
		}
	}
	return tokens
}

func validName(name string) bool {
	if len(name) < 1 || len(name) > 16 || name[0] < 'a' || name[0] > 'z' {
		return false
	}
	for i := 1; i < len(name); i++ {
		c := name[i]
		if !((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_' || c == '-') {
			return false
		}
	}
	return true
}

func parseCronField(raw string, minimum, maximum int, sundayAlias bool) (cronField, bool) {
	field := cronField{min: minimum, max: maximum, wildcard: raw == "*"}
	if raw == "" {
		return field, false
	}
	width := maximum - minimum + 1
	for _, term := range strings.Split(raw, ",") {
		if term == "" {
			return field, false
		}
		parts := strings.Split(term, "/")
		if len(parts) > 2 {
			return field, false
		}
		step := 1
		if len(parts) == 2 {
			parsed, ok := parseDecimal(parts[1])
			if !ok || parsed < 1 || parsed > width {
				return field, false
			}
			step = parsed
		}
		base := parts[0]
		start, end := 0, 0
		switch {
		case base == "*":
			start, end = minimum, maximum
		case strings.Count(base, "-") == 1:
			bounds := strings.SplitN(base, "-", 2)
			var ok bool
			start, ok = parseDecimal(bounds[0])
			if !ok {
				return field, false
			}
			end, ok = parseDecimal(bounds[1])
			if !ok || start < minimum || end > maximum || start > end {
				return field, false
			}
		case strings.Contains(base, "-"):
			return field, false
		default:
			var ok bool
			start, ok = parseDecimal(base)
			if !ok || start < minimum || start > maximum {
				return field, false
			}
			end = start
			if len(parts) == 2 {
				end = maximum
			}
		}
		for value := start; value <= end; value += step {
			selected := value
			if sundayAlias && selected == 7 {
				selected = 0
			}
			field.selected[selected] = true
		}
	}
	return field, true
}

func parseDecimal(value string) (int, bool) {
	if !decimalDigits(value) {
		return 0, false
	}
	parsed, err := strconv.Atoi(value)
	if err != nil {
		return 0, false
	}
	return parsed, true
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

func findRuns(item schedule, after int64, count int) []int64 {
	horizon := after + 8*366*24*60
	start := time.Unix(after*60, 0).UTC()
	day := time.Date(start.Year(), start.Month(), start.Day(), 0, 0, 0, 0, time.UTC)
	runs := make([]int64, 0, count)
	for day.Unix()/60 <= horizon {
		if item.fields[3].selected[int(day.Month())] && matchesDay(item, day) {
			for hour := 0; hour <= 23; hour++ {
				if !item.fields[1].selected[hour] {
					continue
				}
				for minute := 0; minute <= 59; minute++ {
					if !item.fields[0].selected[minute] {
						continue
					}
					candidate := day.Add(time.Duration(hour*60+minute)*time.Minute).Unix() / 60
					if candidate <= after || candidate > horizon {
						continue
					}
					runs = append(runs, candidate)
					if len(runs) == count {
						return runs
					}
				}
			}
		}
		day = day.AddDate(0, 0, 1)
	}
	return runs
}

func matchesDay(item schedule, day time.Time) bool {
	dom := item.fields[2]
	dow := item.fields[4]
	if dom.wildcard && dow.wildcard {
		return true
	}
	weekday := int(day.Weekday())
	if dom.wildcard {
		return dow.selected[weekday]
	}
	if dow.wildcard {
		return dom.selected[day.Day()]
	}
	return dom.selected[day.Day()] && dow.selected[weekday]
}

func renderSchedules(schedules []schedule, runs [][]int64, format string) string {
	var output strings.Builder
	if format == "text" {
		for i, item := range schedules {
			output.WriteString(item.name)
			for _, run := range runs[i] {
				output.WriteByte('\t')
				output.WriteString(strconv.FormatInt(run, 10))
			}
			output.WriteByte('\n')
		}
		return output.String()
	}
	output.WriteString(`{"schedules":[`)
	for i, item := range schedules {
		if i > 0 {
			output.WriteByte(',')
		}
		output.WriteString(`{"name":`)
		output.WriteString(strconv.Quote(item.name))
		output.WriteString(`,"runs":[`)
		for j, run := range runs[i] {
			if j > 0 {
				output.WriteByte(',')
			}
			output.WriteString(strconv.FormatInt(run, 10))
		}
		output.WriteString(`]}`)
	}
	output.WriteString("]}\n")
	return output.String()
}
