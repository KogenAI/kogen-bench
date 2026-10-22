package mini

import "testing"

func TestAddPositive(t *testing.T) {
	if Add(2, 3) != 5 {
		t.Fatal("Add(2, 3) != 5")
	}
}

func TestAddNegative(t *testing.T) {
	if Add(-2, 5) != 3 {
		t.Fatal("Add(-2, 5) != 3")
	}
}
