package steps

import (
	"testing"

	"mini"
)

// Steps for acceptance.feature; `go test ./features/steps/` is the acceptance run.
func TestAcceptanceSum(t *testing.T) {
	if got := mini.Add(2, 3); got != 5 {
		t.Fatalf("When I add 2 and 3, the result is %d, want 5", got)
	}
}

func TestAcceptanceNegative(t *testing.T) {
	if got := mini.Add(-2, 3); got != 1 {
		t.Fatalf("When I add -2 and 3, the result is %d, want 1", got)
	}
}
