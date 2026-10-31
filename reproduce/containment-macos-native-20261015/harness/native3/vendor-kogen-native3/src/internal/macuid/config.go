package macuid

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"
	"time"
)

// ServiceConfig is root-installed infrastructure policy, not a candidate
// manifest or qualification record. The service exposes only diagnostic leases
// and custody; it cannot launch candidate commands or authorize execution.
type ServiceConfig struct {
	Version       int     `json:"version"`
	Account       Account `json:"account"`
	ControllerUID uint32  `json:"controller_uid"`
	Helper        string  `json:"helper"`
	State         string  `json:"state"`
	Socket        string  `json:"socket"`
	RSSBytes      uint64  `json:"rss_bytes"`
	CPUms         uint64  `json:"cpu_ms"`
	WallMS        int64   `json:"wall_ms"`
	ReactionMS    int64   `json:"reaction_ms"`
	GraceMS       int64   `json:"term_grace_ms"`
	CleanupMS     int64   `json:"cleanup_ms"`
	PollMS        int64   `json:"poll_ms"`
	// ProtectedPaths are extra root-installed secret/infrastructure locations
	// denied to every Build in addition to the fixed secret list (optional).
	ProtectedPaths []string `json:"protected_paths,omitempty"`
}

func (c ServiceConfig) Timing() Timing {
	return Timing{Reaction: time.Duration(c.ReactionMS) * time.Millisecond, Grace: time.Duration(c.GraceMS) * time.Millisecond, Cleanup: time.Duration(c.CleanupMS) * time.Millisecond, Poll: time.Duration(c.PollMS) * time.Millisecond}
}
func (c ServiceConfig) Limits() Limits {
	return Limits{RSSBytes: c.RSSBytes, CPUms: c.CPUms, Wall: time.Duration(c.WallMS) * time.Millisecond}
}

func (c ServiceConfig) Validate() error {
	if c.Version != 1 || c.ControllerUID < 501 || c.ControllerUID == c.Account.UID || c.Account.UID < 501 || c.Account.GID < 501 || c.RSSBytes > MaxCounter || c.CPUms > MaxCounter {
		return fmt.Errorf("invalid installed service/account/limit descriptor")
	}
	for _, n := range []int64{c.WallMS, c.ReactionMS, c.GraceMS, c.CleanupMS, c.PollMS} {
		if n < 0 || n > 86400000 {
			return fmt.Errorf("installed time budget out of range")
		}
	}
	if c.WallMS == 0 || c.PollMS > 1000 || c.Timing().Validate() != nil {
		return fmt.Errorf("invalid service timing")
	}
	if len(c.ProtectedPaths) > 64 {
		return fmt.Errorf("too many protected paths")
	}
	for _, p := range append([]string{c.Helper, c.State, c.Socket}, c.ProtectedPaths...) {
		if !pathOK(p) {
			return fmt.Errorf("canonical installed infrastructure paths required")
		}
	}
	if within(c.Helper, c.State) || within(c.Socket, c.State) {
		return fmt.Errorf("helper/socket must be outside private journal directory")
	}
	return nil
}

// ReadInstalled verifies every existing path component without following links.
// A hostile host administrator is outside the threat model. Candidate-granted
// paths may never overlap installed infrastructure.
func ReadInstalled(path string, max int64) ([]byte, error) {
	if err := CheckInstalledPath(path, false); err != nil {
		return nil, err
	}
	f, err := os.OpenFile(path, os.O_RDONLY|syscall.O_NOFOLLOW, 0)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	st, err := f.Stat()
	if err != nil || !st.Mode().IsRegular() || st.Size() > max {
		return nil, fmt.Errorf("bounded installed regular file required")
	}
	b, err := io.ReadAll(io.LimitReader(f, max+1))
	if err != nil {
		return nil, err
	}
	if int64(len(b)) > max {
		return nil, fmt.Errorf("installed file grew beyond bound")
	}
	return b, nil
}

func CheckInstalledPath(path string, directory bool) error {
	if !pathOK(path) {
		return fmt.Errorf("canonical installed path required")
	}
	for p := path; ; p = filepath.Dir(p) {
		st, err := os.Lstat(p)
		if err != nil {
			return err
		}
		raw, ok := st.Sys().(*syscall.Stat_t)
		if !ok || raw.Uid != 0 || st.Mode()&os.ModeSymlink != 0 || st.Mode().Perm()&0022 != 0 {
			return fmt.Errorf("root-owned nonaliased infrastructure required: %s", p)
		}
		if p != path && !st.IsDir() {
			return fmt.Errorf("infrastructure parent is not a directory")
		}
		if p == path && directory && !st.IsDir() {
			return fmt.Errorf("installed directory required")
		}
		if p == "/" {
			break
		}
	}
	return nil
}

func DecodeConfig(raw []byte) (ServiceConfig, error) {
	var c ServiceConfig
	// Duplicate keys are explicitly rejected rather than using encoding/json's
	// last-wins behavior for privileged installed policy.
	if len(raw) > 65536 || !uniqueJSON(raw) {
		return c, fmt.Errorf("closed bounded installed JSON required")
	}
	d := json.NewDecoder(bytes.NewReader(raw))
	d.DisallowUnknownFields()
	if err := d.Decode(&c); err != nil {
		return c, err
	}
	var tail any
	if d.Decode(&tail) != io.EOF {
		return c, fmt.Errorf("trailing installed JSON")
	}
	return c, c.Validate()
}

func uniqueJSON(raw []byte) bool {
	d := json.NewDecoder(bytes.NewReader(raw))
	d.UseNumber()
	var visit func() bool
	depth := 0
	visit = func() bool {
		depth++
		defer func() { depth-- }()
		if depth > 32 {
			return false
		}
		tok, err := d.Token()
		if err != nil {
			return false
		}
		if delim, ok := tok.(json.Delim); ok {
			switch delim {
			case '{':
				keys := map[string]bool{}
				for d.More() {
					key, err := d.Token()
					s, ok := key.(string)
					if err != nil || !ok || keys[s] {
						return false
					}
					keys[s] = true
					if !visit() {
						return false
					}
				}
				end, err := d.Token()
				return err == nil && end == json.Delim('}')
			case '[':
				for d.More() {
					if !visit() {
						return false
					}
				}
				end, err := d.Token()
				return err == nil && end == json.Delim(']')
			default:
				return false
			}
		}
		return true
	}
	if !visit() {
		return false
	}
	_, err := d.Token()
	return err == io.EOF
}

func LoadConfig(path string) (ServiceConfig, error) {
	b, err := ReadInstalled(path, 65536)
	if err != nil {
		return ServiceConfig{}, err
	}
	return DecodeConfig(b)
}
