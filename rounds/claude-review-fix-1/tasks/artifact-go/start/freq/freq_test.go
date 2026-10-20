package freq

import (
	"strings"
	"testing"
)

func TestLoadReadsStdinForDash(t *testing.T) {
	data, err := Load("-", true, strings.NewReader("a b"))
	if err != nil || string(data) != "a b" {
		t.Fatalf("unexpected result: %q, %v", data, err)
	}
}
