package main

import (
	"bufio"
	"encoding/json"
	"os"
	"sort"
	"strings"
)

type command struct {
	Name        string `json:"name"`
	Adapter     string `json:"adapter"`
	Status      int    `json:"status"`
	TimedOut    bool   `json:"timed_out"`
	ResultsPath string `json:"results_path"`
}

type expected struct {
	Requested  []string `json:"requested"`
	Regression []string `json:"regression"`
}

type input struct {
	Commands []command `json:"commands"`
	Expected expected  `json:"expected"`
}

// parsed is one results file: test id to the states seen, and whether the file is complete.
type parsed struct {
	ids      map[string][]string
	complete bool
}

// maxLine is the longest results line read; a longer one makes the file incomplete.
var maxLine = 1 << 26

// parse reads a results file; a missing file or an unknown adapter is an incomplete, empty result.
func parse(adapter, path string) parsed {
	if adapter != "go_test_json" && adapter != "exunit_lab" && adapter != "lab_jsonl" {
		return parsed{ids: map[string][]string{}}
	}
	f, err := os.Open(path)
	if err != nil {
		return parsed{ids: map[string][]string{}}
	}
	defer f.Close()
	var rows []map[string]any
	bad := false
	sc := bufio.NewScanner(f)
	sc.Buffer(make([]byte, 0, 4096), maxLine)
	for sc.Scan() {
		line := strings.TrimRight(sc.Text(), "\r")
		if line == "" {
			continue
		}
		var row map[string]any
		if json.Unmarshal([]byte(line), &row) != nil || row == nil {
			bad = true
			continue
		}
		rows = append(rows, row)
	}
	bad = bad || sc.Err() != nil
	if adapter == "go_test_json" {
		return parseGo(rows, bad)
	}
	return parseLab(rows, bad)
}

func goState(action any) string {
	switch action {
	case "pass":
		return "passed"
	case "fail":
		return "failed"
	case "skip":
		return "skipped"
	}
	return ""
}

// parseGo: test id is "<package>/<test>"; complete when every package got a pass/fail event.
func parseGo(rows []map[string]any, bad bool) parsed {
	ids := map[string][]string{}
	seen, done := map[string]bool{}, map[string]bool{}
	for _, r := range rows {
		pkg, _ := r["Package"].(string)
		test, hasTest := r["Test"].(string)
		if pkg == "" {
			continue
		}
		seen[pkg] = true
		state := goState(r["Action"])
		switch {
		case hasTest && state != "":
			ids[pkg+"/"+test] = append(ids[pkg+"/"+test], state)
		case !hasTest && (state == "passed" || state == "failed"):
			done[pkg] = true
		}
	}
	complete := len(seen) > 0 && !bad
	for pkg := range seen {
		complete = complete && done[pkg]
	}
	return parsed{ids, complete}
}

func labState(s string) string {
	switch s {
	case "pass":
		return "passed"
	case "fail":
		return "failed"
	case "skip":
		return "skipped"
	case "error":
		return "errored"
	}
	return s
}

// parseLab handles the ExUnit formatter and JSONL: {"id","state"} rows then {"suite":"finished"}.
func parseLab(rows []map[string]any, bad bool) parsed {
	ids := map[string][]string{}
	finished := false
	for i, r := range rows {
		if _, ok := r["suite"]; ok {
			if r["suite"] == "finished" && i == len(rows)-1 {
				finished = true
			} else {
				bad = true
			}
			continue
		}
		id, ok1 := r["id"].(string)
		state, ok2 := r["state"].(string)
		if !ok1 || !ok2 {
			bad = true
			continue
		}
		ids[id] = append(ids[id], labState(state))
	}
	return parsed{ids, finished && !bad}
}

type occurrence struct {
	state string
	cmd   int
}

// verdict is the Lab's Adapters.verdict: an expected id passes only when seen once, passed,
// in a command that exited 0 within its deadline and wrote a complete results file.
func verdict(in input) map[string]any {
	results := make([]parsed, len(in.Commands))
	occ := map[string][]occurrence{}
	anyTimedOut, allComplete, commandFailures := false, true, false
	for i, c := range in.Commands {
		results[i] = parse(c.Adapter, c.ResultsPath)
		for id, states := range results[i].ids {
			for _, s := range states {
				occ[id] = append(occ[id], occurrence{s, i})
			}
		}
		anyTimedOut = anyTimedOut || c.TimedOut
		allComplete = allComplete && results[i].complete
		commandFailures = commandFailures || c.Status != 0 || c.TimedOut || !results[i].complete
	}
	var want []string
	isWanted := map[string]bool{}
	for _, id := range append(append([]string{}, in.Expected.Requested...), in.Expected.Regression...) {
		if !isWanted[id] {
			isWanted[id] = true
			want = append(want, id)
		}
	}
	ids := map[string]string{}
	allIDsPassed := true
	for _, id := range want {
		ids[id] = idState(occ[id], in.Commands, results, anyTimedOut)
		allIDsPassed = allIDsPassed && ids[id] == "passed"
	}
	byState := func(state string) []string {
		out := []string{}
		for id, s := range ids {
			if s == state {
				out = append(out, id)
			}
		}
		sort.Strings(out)
		return out
	}
	unexpected, observed := []string{}, []string{}
	for id := range occ {
		observed = append(observed, id)
		if !isWanted[id] {
			unexpected = append(unexpected, id)
		}
	}
	sort.Strings(unexpected)
	sort.Strings(observed)
	rows := []map[string]any{}
	for i, c := range in.Commands {
		ok := c.Status == 0 && !c.TimedOut && results[i].complete
		rows = append(rows, map[string]any{"name": c.Name, "status": c.Status, "timed_out": c.TimedOut, "ok": ok})
	}
	return map[string]any{
		"all_passed":   allIDsPassed && !commandFailures,
		"complete":     allComplete,
		"ids":          ids,
		"observed_ids": observed,
		"expected":     map[string]any{"requested": nonNil(in.Expected.Requested), "regression": nonNil(in.Expected.Regression)},
		"unexpected":   unexpected,
		"missing":      byState("missing"),
		"duplicates":   byState("duplicate"),
		"failed":       byState("failed"),
		"skipped":      byState("skipped"),
		"errored":      byState("errored"),
		"timed_out":    byState("timed_out"),
		"commands":     rows,
	}
}

func idState(occ []occurrence, cmds []command, results []parsed, anyTimedOut bool) string {
	switch {
	case len(occ) == 0 && anyTimedOut:
		return "timed_out"
	case len(occ) == 0:
		return "missing"
	case len(occ) > 1:
		return "duplicate"
	}
	o, c := occ[0], cmds[occ[0].cmd]
	switch {
	case c.TimedOut:
		return "timed_out"
	case o.state == "failed" || o.state == "skipped":
		return o.state
	case o.state != "passed", c.Status != 0, !results[o.cmd].complete:
		return "errored"
	}
	return "passed"
}

func nonNil(s []string) []string {
	if s == nil {
		return []string{}
	}
	return s
}
