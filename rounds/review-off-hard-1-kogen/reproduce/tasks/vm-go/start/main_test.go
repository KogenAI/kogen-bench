package main

import "testing"

func TestPhysicalLines(t *testing.T) {
	lines := physicalLines([]byte("a\r\n\nb\r"))
	if len(lines) != 3 || lines[0] != "a" || lines[1] != "" || lines[2] != "b" {
		t.Fatalf("unexpected physical lines: %q", lines)
	}
}
