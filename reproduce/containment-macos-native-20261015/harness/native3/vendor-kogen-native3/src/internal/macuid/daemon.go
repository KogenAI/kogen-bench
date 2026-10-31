package macuid

import (
	"bufio"
	"bytes"
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"
	"syscall"
	"time"
)

// Serve is a root launchd service with a deliberately narrow control plane:
// `status`, `reconcile`, operator `diagnostic-lease`, and `launch`. Launch takes
// a Policy-shaped request (no raw profile text, no shell string, no uid), compiles
// the Seatbelt profile itself and runs one Build as the per-Build user (see
// launch.go). Startup always drains any previous UID processes and quarantines
// unresolved prior ownership. Nothing here is a qualification claim.
func Serve(ctx context.Context, configPath string) error {
	if os.Geteuid() != 0 {
		return fmt.Errorf("root LaunchDaemon required")
	}
	c, err := LoadConfig(configPath)
	if err != nil {
		return err
	}
	if _, err = CheckAccount(NativeAccounts{}, c.Account, c.ControllerUID); err != nil {
		return err
	}
	if err = CheckInstalledPath(c.Helper, false); err != nil {
		return err
	}
	if err = CheckInstalledPath(c.State, true); err != nil {
		return err
	}
	st, err := os.Stat(c.State)
	if err != nil || st.Mode().Perm() != 0700 {
		return fmt.Errorf("private root journal directory required")
	}
	if err = CheckInstalledPath(filepath.Dir(c.Socket), true); err != nil {
		return err
	}
	table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
	if err != nil {
		return err
	}
	// A daemon-wide flock prevents two custodians of the same installed slot.
	lock, err := os.OpenFile(filepath.Join(c.State, "service.lock"), os.O_CREATE|os.O_RDWR|syscall.O_NOFOLLOW, 0600)
	if err != nil {
		return err
	}
	defer lock.Close()
	if err = syscall.Flock(int(lock.Fd()), syscall.LOCK_EX|syscall.LOCK_NB); err != nil {
		return ErrBusy
	}
	bootID, err := opaqueID()
	if err != nil {
		return err
	}
	journal, err := OpenJournal(c.State, "journal-"+bootID+".jsonl")
	if err != nil {
		Drain(context.Background(), table, RealClock{}, unavailableJournal{err}, c.Account.UID, "storage-failure-"+bootID, "infrastructure-failure", c.Timing())
		return err
	}
	defer journal.Close()
	activePath := filepath.Join(c.State, "active.json")
	quarantinePath := filepath.Join(c.State, "quarantined.json")
	_, activeErr := os.Lstat(activePath)
	startup := Drain(ctx, table, RealClock{}, journal, c.Account.UID, "startup-"+bootID, "worker-death", c.Timing())
	if activeErr != nil && !os.IsNotExist(activeErr) {
		return activeErr
	}
	if activeErr == nil || !startup.Empty || startup.Fault != "" {
		b, _ := json.Marshal(map[string]any{"prior_active": activeErr == nil, "startup": startup, "contract_status": "cleanup-uncertain"})
		if err = durableInstalled(quarantinePath, b); err != nil && !os.IsExist(err) {
			return err
		}
	}
	if _, err = os.Lstat(c.Socket); err == nil {
		old, er := os.Lstat(c.Socket)
		if er != nil || old.Mode()&os.ModeSocket == 0 {
			return fmt.Errorf("unexpected control socket object")
		}
		if err = os.Remove(c.Socket); err != nil {
			return err
		}
	} else if !os.IsNotExist(err) {
		return err
	}
	listener, err := net.ListenUnix("unix", &net.UnixAddr{Name: c.Socket, Net: "unix"})
	if err != nil {
		return err
	}
	defer listener.Close()
	if err = os.Chown(c.Socket, int(c.ControllerUID), 0); err != nil {
		return err
	}
	if err = os.Chmod(c.Socket, 0600); err != nil {
		return err
	}
	leases := &Leases{}
	custodian := &Custodian{Cfg: c, ConfigPath: configPath, Table: table, Runner: NativeRunner{UID: c.Account.UID, GID: c.Account.GID, Helper: c.Helper}, Clock: RealClock{}, Journal: journal, Leases: leases, Home: lookupHome}
	for {
		if err = ctx.Err(); err != nil {
			Drain(context.Background(), table, RealClock{}, journal, c.Account.UID, "shutdown-"+bootID, "worker-death", c.Timing())
			return nil
		}
		// Timeout keeps the no-owner UID scrub alive without requiring a live client.
		listener.SetDeadline(time.Now().Add(c.Timing().Poll))
		conn, acceptErr := listener.AcceptUnix()
		if acceptErr != nil {
			if ne, ok := acceptErr.(net.Error); !ok || !ne.Timeout() {
				return acceptErr
			}
			ps, scanErr := table.Snapshot(ctx, c.Account.UID)
			if scanErr != nil || len(ps) != 0 {
				Drain(ctx, table, RealClock{}, journal, c.Account.UID, "unleased-"+bootID, "owner-death", c.Timing())
			}
			continue
		}
		uid, peerErr := PeerUID(conn)
		if peerErr != nil || (uid != c.ControllerUID && uid != 0) {
			conn.Close()
			continue
		}
		conn.SetReadDeadline(time.Now().Add(5 * time.Second))
		reader := bufio.NewReaderSize(conn, 64<<10)
		frame, readErr := readFrame(reader, MaxLaunchFrame)
		if readErr != nil {
			conn.Close()
			continue
		}
		switch {
		case string(frame) == "{\"operation\":\"status\",\"version\":1}\n":
			writeFrame(conn, map[string]any{"status": "ready", "launch": LaunchVersion, "qualified": false, "quarantined": custodian.quarantined()})
			conn.Close()
			continue
		case string(frame) == "{\"operation\":\"reconcile\",\"version\":1}\n":
			writeFrame(conn, custodian.Reconcile(ctx))
			conn.Close()
			continue
		case bytes.HasPrefix(frame, []byte("{\"operation\":\"launch\"")):
			custodian.ServeLaunch(ctx, conn, reader, frame)
			conn.Close()
			continue
		case string(frame) != "{\"operation\":\"diagnostic-lease\",\"version\":1}\n":
			conn.Close()
			continue
		}
		if _, err = os.Lstat(quarantinePath); !os.IsNotExist(err) {
			io.WriteString(conn, "{\"status\":\"quarantined\",\"qualified\":false}\n")
			conn.Close()
			continue
		}
		scope, tokenErr := opaqueID()
		if tokenErr != nil {
			conn.Close()
			return tokenErr
		}
		if err = leases.Acquire(scope); err != nil {
			conn.Close()
			continue
		}
		// Intent persists before acknowledging the diagnostic owner. No automatic
		// command spawn occurs anywhere in this service.
		active, _ := json.Marshal(map[string]any{"scope": scope, "uid": c.Account.UID, "owner_uid": uid, "started_at": time.Now().UTC(), "diagnostic_only": true})
		if err = durableInstalled(activePath, active); err != nil {
			conn.Close()
			return err
		}
		conn.SetReadDeadline(time.Time{})
		ownerLost := make(chan struct{})
		go func() { defer close(ownerLost); var b [1]byte; _, _ = reader.Read(b[:]) }()
		// The RSS/CPU sampler is a separate worker. Death closes its private pipe;
		// the custodian still has a native table and can perform whole-UID cleanup.
		watchTable, watchdogLost, closeWatch, watchErr := StartWatchdog(ctx, c, configPath, table)
		var obs Observation
		if watchErr != nil {
			obs.Cause = "watchdog-death"
			obs.Cleanup = Drain(ctx, table, RealClock{}, journal, c.Account.UID, scope, obs.Cause, c.Timing())
		} else {
			ack, _ := json.Marshal(map[string]any{"status": "observing", "scope": scope, "qualified": false})
			if _, err = conn.Write(append(ack, '\n')); err != nil {
				conn.Close()
			}
			obs = (Supervisor{Table: watchTable, CleanupTable: table, Clock: RealClock{}, Journal: journal, UID: c.Account.UID, Timing: c.Timing()}).Watch(ctx, scope, c.Limits(), ownerLost, watchdogLost)
			closeWatch()
		}
		conn.Close() // releases the blocking EOF observer too
		result, _ := json.Marshal(obs)
		if err = durableInstalled(filepath.Join(c.State, "observation-"+scope+".json"), result); err != nil {
			return err
		}
		if !obs.Cleanup.Empty || obs.Cleanup.Fault != "" {
			_ = leases.Quarantine(scope)
			if err = durableInstalled(quarantinePath, result); err != nil && !os.IsExist(err) {
				return err
			}
		} else {
			if err = leases.ReleaseDiagnostic(scope, obs.Cleanup); err != nil {
				return err
			}
			if err = os.Remove(activePath); err != nil {
				return err
			}
		}
	}
}

func opaqueID() (string, error) {
	var b [24]byte
	if _, err := rand.Read(b[:]); err != nil {
		return "", err
	}
	return hex.EncodeToString(b[:]), nil
}

// DiagnosticLease is for operator tests, not containment Submit or approval.
// Closing the returned connection (including process death) triggers revocation.
func DiagnosticLease(ctx context.Context, socket string) (*net.UnixConn, string, error) {
	if !pathOK(socket) {
		return nil, "", fmt.Errorf("canonical installed socket required")
	}
	d := net.Dialer{}
	conn, err := d.DialContext(ctx, "unix", socket)
	if err != nil {
		return nil, "", err
	}
	u, ok := conn.(*net.UnixConn)
	if !ok {
		conn.Close()
		return nil, "", fmt.Errorf("private Unix transport required")
	}
	peer, err := PeerUID(u)
	if err != nil || peer != 0 {
		u.Close()
		return nil, "", fmt.Errorf("root custodian peer required")
	}
	u.SetDeadline(time.Now().Add(time.Second))
	if _, err = io.WriteString(u, "{\"operation\":\"diagnostic-lease\",\"version\":1}\n"); err != nil {
		u.Close()
		return nil, "", err
	}
	reader := bufio.NewReaderSize(u, 1024)
	line, err := reader.ReadSlice('\n')
	if err != nil {
		u.Close()
		return nil, "", err
	}
	var ack struct {
		Status, Scope string
		Qualified     bool
	}
	if err = json.Unmarshal(line, &ack); err != nil || ack.Status != "observing" || len(ack.Scope) != 48 || ack.Qualified {
		u.Close()
		return nil, "", fmt.Errorf("custodian refused diagnostic lease")
	}
	u.SetDeadline(time.Time{})
	return u, ack.Scope, nil
}
