//go:build !darwin || !cgo

package macuid

import (
	"context"
	"fmt"
	"net"
)

type NativeTable struct{}

func NewNativeTable(uint32, uint32, string) (*NativeTable, error) {
	return nil, fmt.Errorf("macOS cgo/libproc unavailable")
}
func (*NativeTable) Snapshot(context.Context, uint32) ([]Process, error) { return nil, ErrObservation }
func (*NativeTable) SignalUID(context.Context, uint32, Signal) error {
	return fmt.Errorf("native UID signaling unavailable")
}
func SignalRole(args []string) (bool, error) {
	if len(args) > 0 && args[0] == "--macuid-signal" {
		return true, fmt.Errorf("native UID signal role unavailable")
	}
	return false, nil
}

type NativeAccounts struct{}

func (NativeAccounts) Lookup(string) (Account, error) {
	return Account{}, fmt.Errorf("macOS account lookup unavailable")
}
func PeerUID(*net.UnixConn) (uint32, error) { return 0, fmt.Errorf("native peer identity unavailable") }
