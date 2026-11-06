package shape

import (
	"encoding/json"
	"os"
	"strings"
	"testing"
)

// Research harness (not part of any patch): the package's one-shot fixture with one observer
// file added to the Intent folder, to see whether a package that carries it reaches readiness.
func TestAORFixtureInIntentFolder(t *testing.T) {
	out := os.Getenv("AOR_FIX_OUT")
	if out == "" {
		t.Skip("no fixture out")
	}
	files := shpFiles()
	list := files["files"].([]any)
	list = append(list, map[string]any{"path": ".kogen/intents/is-even/observer-control.cjs", "content": "process.exit(0)\n"})
	files["files"] = list
	f := newShpFx(t, shpSubmit("c1", files), shpAck("c2"))
	exit, err := f.shape("Add calc.is_even(n). Non-integers raise TypeError.")
	res := map[string]any{"arm": os.Getenv("AOR_ARM"), "exit": exit, "observer_file_written": f.exists(".kogen/intents/is-even/observer-control.cjs"),
		"readiness_receipt": f.exists(".kogen/local/readiness/is-even.json"), "approval_written": f.exists(".kogen/local/approvals/is-even.json"),
		"scenarios_line": strings.Contains(f.Stdout.String(), "Scenarios: 2 (2 fail now, 0 pass now)")}
	if err != nil {
		res["err"] = strings.SplitN(err.Error(), "\n", 2)[0]
	}
	b, _ := json.MarshalIndent(res, "", " ")
	os.WriteFile(out, b, 0o600)
}
