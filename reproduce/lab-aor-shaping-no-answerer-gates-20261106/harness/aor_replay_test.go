package shape

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/KogenAI/kogen-coordinator/git"
	"github.com/KogenAI/kogen-coordinator/project"
)

// Research harness (not part of any patch), no model: replays the recorded inputs of the gates
// through the package's own gate functions. AOR_REPLAY names the case file, AOR_OUT the result
// file, AOR_ARM the arm label.

type aorCase struct {
	ID          string           `json:"id"`
	Tree        string           `json:"tree"`
	Slug        string           `json:"slug"`
	RequestFile string           `json:"request_file"`
	Attempt     int              `json:"attempt"`
	Gate        string           `json:"gate"`
	Recorded    int              `json:"recorded"`
	Items       []map[string]any `json:"items"`
	IntentFile  string           `json:"intent_file"`
	IntentSynth string           `json:"intent_synth"`
	Paths       []string         `json:"paths"`
	Kind        string           `json:"kind"`
	Mode        string           `json:"mode"`
	Expect      string           `json:"expect"` // negative and held-out cases: "refused" or "accepted" (as A)
	Extra       map[string]any   `json:"extra"`
	Contents    map[string]int   `json:"contents"`
}

type aorRow struct {
	ID       string   `json:"id"`
	Arm      string   `json:"arm"`
	Gate     string   `json:"gate"`
	Refused  bool     `json:"refused"`
	Problems int      `json:"problems"`
	Recorded int      `json:"recorded"`
	Lines    []string `json:"lines,omitempty"`
}

func aorDecisionItems(raw []map[string]any) []decisionItem {
	var items []decisionItem
	for _, m := range raw {
		it := decisionItem{}
		it.statement, _ = m["statement"].(string)
		it.verdict, _ = m["verdict"].(string)
		it.intentValue, _ = m["intent_value"].(string)
		it.requestValue, _ = m["request_value"].(string)
		it.difference, _ = m["difference"].(string)
		it.why, _ = m["why"].(string)
		it.quotes = []string{}
		if qs, ok := m["request_quotes"].([]any); ok {
			for _, q := range qs {
				it.quotes = append(it.quotes, q.(string))
			}
		}
		items = append(items, it)
	}
	return items
}

func aorRun(t *testing.T, arm string, c aorCase) aorRow {
	row := aorRow{ID: c.ID, Arm: arm, Gate: c.Gate, Recorded: c.Recorded}
	intent := c.IntentSynth
	if c.IntentFile != "" {
		b, err := os.ReadFile(c.IntentFile)
		if err != nil {
			t.Fatal(err)
		}
		intent = string(b)
	}
	switch c.Gate {
	case "decision_check":
		req := ""
		if c.RequestFile != "" {
			b, err := os.ReadFile(c.RequestFile)
			if err != nil {
				t.Fatal(err)
			}
			req = string(b)
		}
		_, lines := decisionOutcome(aorDecisionItems(c.Items), req, intent)
		if len(lines) > 0 {
			row.Refused, row.Problems, row.Lines = true, len(lines)-2, lines[2:]
		}
	case "decision_evidence":
		dir := filepath.Join(t.TempDir(), "shaping")
		ev, err := NewEvidence(dir, c.Slug)
		if err != nil {
			t.Fatal(err)
		}
		inspected := c.Mode != "unread"
		sh := &shaping{repo: git.New(c.Tree, shpEnv()), root: c.Tree, slug: c.Slug, ext: &shapeExec{t: t}, ev: ev, stateDir: dir, round: 1,
			inspected: inspected, proposed: map[string]string{}, ranCommand: true}
		problems, _, err := sh.evidenceCheck(intent)
		if err != nil {
			t.Fatal(err)
		}
		if len(problems) > 0 {
			row.Refused, row.Problems, row.Lines = true, len(problems), problems
		}
	case "validation":
		sh := &shaping{slug: c.Slug, cfg: &project.Config{Acceptance: &project.Acceptance{Run: "npx cucumber-js", StepsDir: "features/steps"}}}
		var list []any
		for _, p := range c.Paths {
			list = append(list, map[string]any{"path": p, "content": strings.Repeat("x", c.Contents[p])})
		}
		_, problems, err := sh.validateFiles(list)
		if err != nil {
			t.Fatal(err)
		}
		if len(problems) > 0 {
			row.Refused, row.Problems, row.Lines = true, len(problems), problems
		}
	default:
		t.Fatalf("gate %s", c.Gate)
	}
	return row
}

func aorLoad(t *testing.T, env string) []aorCase {
	b, err := os.ReadFile(os.Getenv(env))
	if err != nil {
		t.Skip("no " + env)
	}
	var cases []aorCase
	if err := json.Unmarshal(b, &cases); err != nil {
		t.Fatal(err)
	}
	return cases
}

func aorWrite(t *testing.T, env string, rows []aorRow) {
	b, _ := json.MarshalIndent(rows, "", " ")
	if err := os.WriteFile(os.Getenv(env), b, 0o600); err != nil {
		t.Fatal(err)
	}
}

// TestAORReplay: recorded gate inputs of the five refused trees (every recorded refusal).
func TestAORReplay(t *testing.T) {
	if os.Getenv("AOR_REPLAY") == "" {
		t.Skip("no replay")
	}
	arm := os.Getenv("AOR_ARM")
	var rows []aorRow
	for _, c := range aorLoad(t, "AOR_REPLAY") {
		if c.Gate == "intent" {
			continue
		}
		rows = append(rows, aorRun(t, arm, c))
	}
	aorWrite(t, "AOR_OUT", rows)
}

// TestAORCases: negative cases and held-out cases of the same shape (kind of case in "expect").
func TestAORCases(t *testing.T) {
	if os.Getenv("AOR_CASES") == "" {
		t.Skip("no cases")
	}
	arm := os.Getenv("AOR_ARM")
	var rows []aorRow
	for _, c := range aorLoad(t, "AOR_CASES") {
		rows = append(rows, aorRun(t, arm, c))
	}
	aorWrite(t, "AOR_CASES_OUT", rows)
	fmt.Println("cases", len(rows))
}
