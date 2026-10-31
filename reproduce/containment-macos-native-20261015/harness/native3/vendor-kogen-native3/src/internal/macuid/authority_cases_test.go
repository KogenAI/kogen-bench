package macuid

import (
	"encoding/json"
	"os"
	"testing"
)

// The setup audit (setup/test_dry_run.py) replays the same vectors through
// setup/common.sh, so runtime and setup share one exact matcher definition.
func TestDisabledAuthenticationSharedVectors(t *testing.T) {
	raw, err := os.ReadFile("authority_cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var doc struct {
		Cases []struct {
			Value  *string `json:"value"`
			Accept bool    `json:"accept"`
		} `json:"cases"`
	}
	if err := json.Unmarshal(raw, &doc); err != nil {
		t.Fatal(err)
	}
	if len(doc.Cases) < 8 {
		t.Fatalf("too few shared vectors: %d", len(doc.Cases))
	}
	for _, c := range doc.Cases {
		fields := map[string]string{}
		label := "<absent>"
		if c.Value != nil {
			fields["AuthenticationAuthority"] = *c.Value
			label = *c.Value
		}
		if got := disabledAuthentication(fields); got != c.Accept {
			t.Errorf("AuthenticationAuthority %q: got accept=%v want %v", label, got, c.Accept)
		}
	}
	// A multi-line dscl record joins continuation values; mixed values still refuse.
	fields, err := directoryFields("AuthenticationAuthority:\n ;DisabledUser;\n ;ShadowHash;\n")
	if err != nil || disabledAuthentication(fields) {
		t.Fatalf("multi-line mixed authority accepted: %v %v", fields, err)
	}
}
