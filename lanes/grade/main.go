// Command grade turns evaluator result files into a per-test verdict.
//
// It reads {"commands": [...], "expected": {...}} on stdin, one command per evaluate.toml
// [[command]] with {name, adapter, status, timed_out, results_path}, and writes the verdict
// JSON to stdout. Adapted from the Lab's evaluate adapters (go test -json, ExUnit via
// lab_formatter.exs, JSONL); the evaluation.json key names are the Lab's.
package main

import (
	"encoding/json"
	"fmt"
	"os"
)

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, "grade: invalid input:", err)
		os.Exit(2)
	}
	out, err := json.MarshalIndent(verdict(in), "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, "grade:", err)
		os.Exit(2)
	}
	fmt.Println(string(out))
}
