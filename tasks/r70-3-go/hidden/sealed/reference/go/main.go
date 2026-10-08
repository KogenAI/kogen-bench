package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

func physicalLines(data []byte) []string {
	lines := strings.Split(string(data), "\n")
	for i := range lines {
		lines[i] = strings.TrimSuffix(lines[i], "\r")
	}
	return lines
}

func Load(path string, hasPath bool, prefix string) ([]byte, error) {
	var data []byte
	var err error
	if !hasPath || path == "-" {
		data, err = io.ReadAll(os.Stdin)
	} else {
		data, err = os.ReadFile(path)
	}
	if err != nil {
		return nil, fmt.Errorf("%s: cannot read input", prefix)
	}
	return data, nil
}

func main() {
	output, code, err := execute(os.Args[1:])
	if err != nil {
		_, _ = fmt.Fprintln(os.Stderr, err)
	} else {
		_, _ = fmt.Fprint(os.Stdout, output)
	}
	os.Exit(code)
}
