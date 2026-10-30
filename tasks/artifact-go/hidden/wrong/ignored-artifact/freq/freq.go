package freq

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	"strings"
)

// Load returns the whole input: stdin when there is no path or the path is "-", else the file.
func Load(path string, hasPath bool, stdin io.Reader) ([]byte, error) {
	if !hasPath || path == "-" {
		return io.ReadAll(stdin)
	}
	return os.ReadFile(path)
}

type entry struct {
	word  string
	count int
}

func isWordByte(b byte) bool {
	return (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z') || (b >= '0' && b <= '9')
}

// count returns the words of data with their counts, highest count first, ties by word.
func count(data []byte) []entry {
	counts := map[string]int{}
	start := -1
	flush := func(end int) {
		if start >= 0 {
			counts[strings.ToLower(string(data[start:end]))]++
			start = -1
		}
	}
	for i, b := range data {
		if isWordByte(b) {
			if start < 0 {
				start = i
			}
		} else {
			flush(i)
		}
	}
	flush(len(data))
	entries := make([]entry, 0, len(counts))
	for w, c := range counts {
		entries = append(entries, entry{w, c})
	}
	sort.Slice(entries, func(i, j int) bool {
		if entries[i].count != entries[j].count {
			return entries[i].count > entries[j].count
		}
		return entries[i].word < entries[j].word
	})
	return entries
}

type options struct {
	top, min int
	format   string
	path     string
	hasPath  bool
}

func parseLimit(flag, value string) (int, error) {
	n, err := strconv.Atoi(value)
	valid := err == nil && n >= 1 && n <= 1000000 && value == strconv.Itoa(n)
	if !valid {
		return 0, fmt.Errorf("wordfreq: invalid value for '%s': '%s'", flag, value)
	}
	return n, nil
}

func parse(args []string) (options, error) {
	opts := options{min: 1, format: "text"}
	seen := map[string]bool{}
	for i := 0; i < len(args); i++ {
		arg := args[i]
		switch arg {
		case "--top", "--min", "--format":
			if seen[arg] {
				return opts, fmt.Errorf("wordfreq: duplicate option '%s'", arg)
			}
			seen[arg] = true
			if i+1 >= len(args) {
				return opts, fmt.Errorf("wordfreq: option '%s' requires a value", arg)
			}
			i++
			value := args[i]
			switch arg {
			case "--format":
				if value != "text" && value != "json" {
					return opts, fmt.Errorf("wordfreq: invalid value for '%s': '%s'", arg, value)
				}
				opts.format = value
			default:
				n, err := parseLimit(arg, value)
				if err != nil {
					return opts, err
				}
				if arg == "--top" {
					opts.top = n
				} else {
					opts.min = n
				}
			}
		default:
			if strings.HasPrefix(arg, "-") && arg != "-" {
				return opts, fmt.Errorf("wordfreq: unknown option '%s'", arg)
			}
			if opts.hasPath {
				return opts, fmt.Errorf("wordfreq: expected at most one input path")
			}
			opts.path, opts.hasPath = arg, true
		}
	}
	return opts, nil
}

func render(entries []entry, format string) string {
	var out strings.Builder
	if format == "json" {
		out.WriteString("[")
		for i, e := range entries {
			if i > 0 {
				out.WriteString(",")
			}
			word, _ := json.Marshal(e.word)
			fmt.Fprintf(&out, `{"word":%s,"count":%d}`, word, e.count)
		}
		out.WriteString("]\n")
		return out.String()
	}
	for _, e := range entries {
		fmt.Fprintf(&out, "%s %d\n", e.word, e.count)
	}
	return out.String()
}

// Run executes wordfreq with the given arguments and returns the exit status.
func Run(args []string, stdin io.Reader, stdout, stderr io.Writer) int {
	opts, err := parse(args)
	if err != nil {
		fmt.Fprintln(stderr, err)
		return 2
	}
	data, err := Load(opts.path, opts.hasPath, stdin)
	if err != nil {
		fmt.Fprintln(stderr, "wordfreq: cannot read input")
		return 1
	}
	var kept []entry
	for _, e := range count(data) {
		if e.count >= opts.min {
			kept = append(kept, e)
		}
	}
	if opts.top > 0 && len(kept) > opts.top {
		kept = kept[:opts.top]
	}
	fmt.Fprint(stdout, render(kept, opts.format))
	return 0
}
