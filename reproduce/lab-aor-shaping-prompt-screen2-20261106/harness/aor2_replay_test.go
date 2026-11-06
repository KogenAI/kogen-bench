package shape

import (
	"encoding/json"
	"os"
	"slices"
	"strings"
	"testing"

	"github.com/KogenAI/kogen-coordinator/project"
	"github.com/KogenAI/kogen-verification/verify"
)

// Research harness (not part of any patch), no model: replays recorded gate inputs.
type aor2Case struct {
	ID          string           `json:"id"`
	Gate        string           `json:"gate"`
	Items       []map[string]any `json:"items"`
	Request     string           `json:"request"`
	Intent      string           `json:"intent"`
	Recorded    int              `json:"recorded"`
	Feasibility []string         `json:"feasibility"`
	Acceptance  []string         `json:"acceptance"`
}

func aor2Items(raw []map[string]any) []decisionItem {
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

func TestAOR2Replay(t *testing.T) {
	in := os.Getenv("AOR2_CASES")
	if in == "" {
		t.Skip("no cases")
	}
	b, err := os.ReadFile(in)
	if err != nil {
		t.Fatal(err)
	}
	var cases []aor2Case
	if err := json.Unmarshal(b, &cases); err != nil {
		t.Fatal(err)
	}
	var rows []map[string]any
	for _, c := range cases {
		row := map[string]any{"id": c.ID, "gate": c.Gate, "arm": os.Getenv("AOR2_ARM")}
		switch c.Gate {
		case "decision_check":
			_, lines := decisionOutcome(aor2Items(c.Items), c.Request, c.Intent)
			row["recorded"] = c.Recorded
			row["problems"] = max(len(lines)-2, 0)
			if len(lines) > 0 {
				row["head"] = lines[0]
			}
		case "evidence_rule":
			run := func(acc []string) string {
				intent := &project.Intent{Feasibility: c.Feasibility, Acceptance: acc}
				_, err := verify.Declarations(intent)
				if err == nil {
					return "valid"
				}
				e, ok := err.(interface{ Error() string })
				_ = e
				msg := err.Error()
				if se, ok2 := asSysLines(err); ok2 {
					msg = strings.Join(se, " | ")
				} else if ok {
					msg = err.Error()
				}
				return msg
			}
			row["as_written"] = run(c.Acceptance)
			// the same declaration with every observer path added to Acceptance
			acc := slices.Clone(c.Acceptance)
			for _, l := range c.Feasibility {
				var d struct{ Observers []string }
				raw := strings.TrimPrefix(l, "- evidence:")
				if json.Unmarshal([]byte(strings.TrimSpace(raw)), &d) == nil {
					for _, o := range d.Observers {
						if !slices.Contains(acc, o) {
							acc = append(acc, o)
						}
					}
				}
			}
			row["observers_added_to_acceptance"] = run(acc)
			row["hinted"] = aor2Hinted(row["as_written"].(string))
		}
		rows = append(rows, row)
	}
	out, _ := json.MarshalIndent(rows, "", " ")
	if err := os.WriteFile(os.Getenv("AOR2_OUT"), out, 0o600); err != nil {
		t.Fatal(err)
	}
}
