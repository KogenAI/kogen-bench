package build

// Lab C6 arm A (fix a): the budget-off test compares an allow-list projection of what a Build recorded
// instead of the whole record minus a deny-list of volatile keys. It asserts only what the test is about:
// the requests the Build sent, the order and role of its events, the keys the checkpoint holds, the outcome
// of the result, the commit message, and that no budget field or event exists anywhere in the budget-off Build.
// Scratch copy for the Lab; added next to build_request_budget_test.go in a scratch tree, never committed.

import (
	"os"
	"reflect"
	"sort"
	"strings"
	"testing"
)

// allowLogKey: the keys of a logged event that the budget-off claim is about. Everything else (timings,
// offsets, load, probe statuses, identities, byte counts) is not compared. Any key that mentions "budget" is kept.
func allowLogKey(k string) bool {
	switch k {
	case "event", "role", "repair", "pass", "name", "tool", "outcome", "count", "limit":
		return true
	}
	return strings.Contains(k, "budget")
}

type budgetProjection struct {
	requests, log, checkpointKeys, result, commit string
}

func sortedKeys(m map[string]any) []string {
	out := make([]string, 0, len(m))
	for k := range m {
		out = append(out, k)
	}
	sort.Strings(out)
	return out
}

func projectEvents(events []map[string]any) string {
	var lines []string
	for _, ev := range events {
		keep := map[string]any{}
		for k, v := range ev {
			if allowLogKey(k) {
				keep[k] = v
			}
		}
		lines = append(lines, jsonText(keep))
	}
	return strings.Join(lines, "\n")
}

func projectBuild(t *testing.T, e *env, id string) budgetProjection {
	t.Helper()
	// requests and the commit message keep their existing normalisation (they are content, not timing)
	full := observeBuild(t, e, id)
	doc, state := e.checkpoint(id)
	res := e.result(id)
	keepRes := map[string]any{}
	for _, k := range []string{"outcome", "passes"} {
		if v, ok := res[k]; ok {
			keepRes[k] = v
		}
	}
	return budgetProjection{
		requests:       full.requests,
		log:            projectEvents(e.events(id)),
		checkpointKeys: strings.Join(sortedKeys(doc), ",") + "|" + strings.Join(sortedKeys(state), ","),
		result:         jsonText(keepRes),
		commit:         full.outcome,
	}
}

func TestBuildRequestBudgetOffAllow(t *testing.T) {
	t.Parallel()
	run := func(zero bool) (budgetProjection, int) {
		e := newEnv(t)
		f := e.prov
		for i := 0; i < 5; i++ {
			f.then(f.calls("read_file", map[string]any{"path": "app.txt"}))
		}
		f.then(redTry(f, 1), redTry(f, 2))
		f.then(landScript(f)...)
		a := e.build(func(in *Input) {
			if zero {
				in.BuildRequestBudget = 0
			}
		})
		if a.exit != 0 {
			t.Fatalf("exit %d: %s", a.exit, a.shown())
		}
		id := e.onlyRun()
		// No budget field or event anywhere in a budget-off Build: read the raw files, not the projection.
		for _, name := range []string{"log.jsonl", "checkpoint.json", "result.json"} {
			b, err := os.ReadFile(e.runPath(id, name))
			if err != nil {
				t.Fatal(err)
			}
			lacks(t, name, string(b), "build_request_budget")
		}
		if ev := budgetEvents(e, id); len(ev) != 0 {
			t.Fatalf("events: %v", ev)
		}
		_, state := e.checkpoint(id)
		if _, ok := state["build_request_budget"]; ok {
			t.Fatal("budget field in checkpoint state")
		}
		return projectBuild(t, e, id), f.count()
	}
	omitted, n := run(false)
	zero, m := run(true)
	if n != 8 || m != 8 {
		t.Fatalf("requests %d and %d, want 8", n, m)
	}
	if !reflect.DeepEqual(omitted, zero) {
		for _, p := range [][3]string{
			{"requests", omitted.requests, zero.requests}, {"log", omitted.log, zero.log},
			{"checkpoint keys", omitted.checkpointKeys, zero.checkpointKeys}, {"result", omitted.result, zero.result}, {"commit", omitted.commit, zero.commit},
		} {
			if p[1] != p[2] {
				t.Errorf("%s differs:\nomitted: %.300s\nzero:    %.300s", p[0], p[1], p[2])
			}
		}
	}
}

// The projection keeps what the claim is about and drops timing: a budget field changes it, a timing field does not.
func TestBudgetProjectionSensitivity(t *testing.T) {
	t.Parallel()
	events := []map[string]any{{"event": "provider_attempt", "role": "build", "request_offset_ms": 1.0, "status": "ok"}}
	base := projectEvents(events)
	timing := projectEvents([]map[string]any{{"event": "provider_attempt", "role": "build", "request_offset_ms": 999.0, "status": "timed_out", "load_average": []any{9.0}}})
	if base != timing {
		t.Errorf("timing or status values change the projection:\n%s\n%s", base, timing)
	}
	for name, ev := range map[string]map[string]any{
		"budget field":   {"event": "provider_attempt", "role": "build", "build_request_budget": map[string]any{"limit": 5.0}},
		"budget event":   {"event": "build_request_budget", "role": "build"},
		"role":           {"event": "provider_attempt", "role": "review"},
		"event name":     {"event": "other", "role": "build"},
	} {
		if projectEvents([]map[string]any{ev}) == base {
			t.Errorf("%s: the changed value is masked", name)
		}
	}
}
