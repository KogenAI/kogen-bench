package mini

import "testing"

func TestAddZero(t *testing.T) {
	if Add(0, 0) != 0 {
		t.Fatal("Add(0, 0) != 0")
	}
}
