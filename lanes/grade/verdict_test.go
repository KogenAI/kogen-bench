package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
)

func write(t *testing.T, name, body string) string {
	p := filepath.Join(t.TempDir(), name)
	if err := os.WriteFile(p, []byte(body), 0o644); err != nil {
		t.Fatal(err)
	}
	return p
}

const goPass = `{"Action":"run","Package":"m","Test":"TestA"}
{"Action":"pass","Package":"m","Test":"TestA"}
{"Action":"fail","Package":"m","Test":"TestB"}
{"Action":"fail","Package":"m"}
`

func TestGoAdapter(t *testing.T) {
	p := write(t, "r.jsonl", goPass)
	v := verdict(input{
		Commands: []command{{Name: "go", Adapter: "go_test_json", Status: 1, ResultsPath: p}},
		Expected: expected{Requested: []string{"m/TestA", "m/TestB", "m/TestC"}},
	})
	ids := v["ids"].(map[string]string)
	// go test exited 1, so TestA's pass is not trusted
	if ids["m/TestA"] != "errored" || ids["m/TestB"] != "failed" || ids["m/TestC"] != "missing" {
		t.Fatalf("ids = %v", ids)
	}
	if v["all_passed"] != false {
		t.Fatal("all_passed should be false")
	}
}

func TestLabAdapterAndTimeout(t *testing.T) {
	p := write(t, "r.jsonl", `{"id":"M:a","state":"passed"}`+"\n"+`{"suite":"finished"}`+"\n")
	in := input{
		Commands: []command{{Name: "ex", Adapter: "exunit_lab", ResultsPath: p}},
		Expected: expected{Requested: []string{"M:a"}},
	}
	if v := verdict(in); v["all_passed"] != true {
		t.Fatalf("verdict = %v", v)
	}
	in.Commands[0].TimedOut = true
	if v := verdict(in); v["all_passed"] != false || v["ids"].(map[string]string)["M:a"] != "timed_out" {
		t.Fatalf("timed out verdict = %v", v)
	}
}

func TestIncompleteFile(t *testing.T) {
	p := write(t, "r.jsonl", `{"id":"M:a","state":"passed"}`+"\n")
	v := verdict(input{
		Commands: []command{{Name: "ex", Adapter: "lab_jsonl", ResultsPath: p}},
		Expected: expected{Requested: []string{"M:a"}},
	})
	if v["all_passed"] != false || v["ids"].(map[string]string)["M:a"] != "errored" {
		t.Fatalf("verdict = %v", v)
	}
}

func TestUnknownAdapterAndLongLine(t *testing.T) {
	p := write(t, "r.jsonl", `{"id":"M:a","state":"passed"}`+"\n"+`{"suite":"finished"}`+"\n")
	in := input{Commands: []command{{Name: "x", Adapter: "nope", ResultsPath: p}}, Expected: expected{Requested: []string{"M:a"}}}
	if v := verdict(in); v["all_passed"] != false || v["ids"].(map[string]string)["M:a"] != "missing" {
		t.Fatalf("unknown adapter verdict = %v", v)
	}
	in.Commands[0].Adapter = "lab_jsonl"
	if v := verdict(in); v["all_passed"] != true {
		t.Fatalf("control verdict = %v", v)
	}
	old := maxLine
	maxLine = 16 // the scanner fails on the long line below, so the file counts as incomplete
	defer func() { maxLine = old }()
	in.Commands[0].ResultsPath = write(t, "long.jsonl", `{"id":"`+strings.Repeat("x", 5000)+`","state":"passed"}`+"\n"+`{"id":"M:a","state":"passed"}`+"\n"+`{"suite":"finished"}`+"\n")
	if v := verdict(in); v["all_passed"] != false {
		t.Fatalf("over-long line: all_passed = %v", v["all_passed"])
	}
}

// TestCorpusMatchesLab checks every recorded results file of the Lab's adapter corpus
// (testdata/corpus, with the Lab's expected parse and verdict in corpus_expected.json) against this port.
func TestCorpusMatchesLab(t *testing.T) {
	raw, err := os.ReadFile("testdata/corpus_expected.json")
	if err != nil {
		t.Fatal(err)
	}
	var want map[string]struct {
		Parse struct {
			Complete bool                `json:"complete"`
			IDs      map[string][]string `json:"ids"`
		} `json:"parse"`
		Verdicts []struct {
			Status   int            `json:"status"`
			TimedOut bool           `json:"timed_out"`
			Verdict  map[string]any `json:"verdict"`
		} `json:"verdicts"`
	}
	if err := json.Unmarshal(raw, &want); err != nil || len(want) < 60 {
		t.Fatalf("corpus_expected.json: %d entries, %v", len(want), err)
	}
	exp := expected{Requested: []string{"pkg/TestA", "pkg/TestB"}, Regression: []string{"pkg/TestC", "pkg/TestA"}}
	for file, w := range want {
		adapter := strings.TrimPrefix(filepath.Ext(file), ".")
		path := filepath.Join("testdata", "corpus", file)
		got := parse(adapter, path)
		if got.complete != w.Parse.Complete || !reflect.DeepEqual(nonNilIDs(got.ids), nonNilIDs(w.Parse.IDs)) {
			t.Errorf("%s: parse = %v complete=%v, want %v complete=%v", file, got.ids, got.complete, w.Parse.IDs, w.Parse.Complete)
		}
		for _, v := range w.Verdicts {
			c := command{Name: "c", Adapter: adapter, Status: v.Status, TimedOut: v.TimedOut, ResultsPath: path}
			out := verdict(input{Commands: []command{c}, Expected: exp})
			gotJSON, _ := json.Marshal(out)
			var back map[string]any
			json.Unmarshal(gotJSON, &back)
			for key, wantVal := range v.Verdict {
				if !reflect.DeepEqual(back[key], wantVal) {
					t.Errorf("%s status=%d timed_out=%v: %s = %v, want %v", file, v.Status, v.TimedOut, key, back[key], wantVal)
				}
			}
		}
	}
}

func nonNilIDs(m map[string][]string) map[string][]string {
	if m == nil {
		return map[string][]string{}
	}
	return m
}
