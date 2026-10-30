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

func TestCountOrdersByCountThenWord(t *testing.T) {
	got := count([]byte("b a a, b\nc b"))
	want := []entry{{"b", 3}, {"a", 2}, {"c", 1}}
	if len(got) != len(want) {
		t.Fatalf("unexpected entries: %v", got)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("entry %d: got %v, want %v", i, got[i], want[i])
		}
	}
}
