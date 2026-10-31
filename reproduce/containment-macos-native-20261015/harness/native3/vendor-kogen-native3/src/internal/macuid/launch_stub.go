//go:build !darwin || !cgo

package macuid

import (
	"context"
	"fmt"
	"io"
	"os"
)

func LaunchProbe(Policy, uint32, uint32, *os.File, *os.File) (*os.Process, error) {
	return nil, fmt.Errorf("native macOS probe launcher unavailable")
}

// NativeRunner is unavailable off darwin/cgo; the custodian refuses to launch.
type NativeRunner struct {
	UID, GID uint32
	Helper   string
}

func (NativeRunner) Start(context.Context, LaunchSpec, io.Writer, io.Writer) (Running, error) {
	return nil, fmt.Errorf("native macOS runner unavailable")
}
