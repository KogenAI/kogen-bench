package macuid

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"
)

// OperatorInspect has no signaling side effect. Failed enumeration is never an
// empty-success observation. It is intentionally separate from Engine.Query.
func OperatorInspect(ctx context.Context, configPath string, out io.Writer) error {
	c, err := LoadConfig(configPath)
	if err != nil {
		return err
	}
	if _, err = CheckAccount(NativeAccounts{}, c.Account, c.ControllerUID); err != nil {
		return err
	}
	table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
	if err != nil {
		return err
	}
	ps, scanErr := table.Snapshot(ctx, c.Account.UID)
	if err = json.NewEncoder(out).Encode(map[string]any{"uid": c.Account.UID, "processes": ps, "observation_complete": scanErr == nil, "qualified": false, "error": errorText(scanErr)}); err != nil {
		return err
	}
	return scanErr
}

// OperatorResetDiagnostic must run as root with the launchd job BOOTED OUT. It
// drains the reserved account before clearing only the diagnostic lease fences.
// All old journals/observations remain. It cannot reconcile or mark any contract
// handle finished, and never authorizes containment Submit.
func OperatorResetDiagnostic(ctx context.Context, configPath string, out io.Writer) error {
	if os.Geteuid() != 0 {
		return fmt.Errorf("explicit administrator diagnostic reset required")
	}
	c, err := LoadConfig(configPath)
	if err != nil {
		return err
	}
	if _, err = CheckAccount(NativeAccounts{}, c.Account, c.ControllerUID); err != nil {
		return err
	}
	if err = CheckInstalledPath(c.State, true); err != nil {
		return err
	}
	lock, err := os.OpenFile(filepath.Join(c.State, "service.lock"), os.O_CREATE|os.O_RDWR|syscall.O_NOFOLLOW, 0600)
	if err != nil {
		return err
	}
	defer lock.Close()
	if err = syscall.Flock(int(lock.Fd()), syscall.LOCK_EX|syscall.LOCK_NB); err != nil {
		return ErrBusy
	}
	table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
	if err != nil {
		return err
	}
	id, err := opaqueID()
	if err != nil {
		return err
	}
	j, err := OpenJournal(c.State, "operator-reset-"+id+".jsonl")
	if err != nil {
		r := Drain(ctx, table, RealClock{}, unavailableJournal{err}, c.Account.UID, "operator-reset-"+id, "infrastructure-failure", c.Timing())
		_ = json.NewEncoder(out).Encode(r)
		return err
	}
	defer j.Close()
	r := Drain(ctx, table, RealClock{}, j, c.Account.UID, "operator-reset-"+id, "stopped", c.Timing())
	if err = json.NewEncoder(out).Encode(r); err != nil {
		return err
	}
	if !r.Empty || r.Fault != "" {
		return fmt.Errorf("UID still occupied or observation failed; diagnostic fences retained")
	}
	for _, name := range []string{"active.json", "quarantined.json"} {
		if err = os.Remove(filepath.Join(c.State, name)); err != nil && !os.IsNotExist(err) {
			return err
		}
	}
	d, err := os.Open(c.State)
	if err != nil {
		return err
	}
	defer d.Close()
	return d.Sync()
}
