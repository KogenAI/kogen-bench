package macuid

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"syscall"
)

const JournalBudget = 8 << 20
const JournalRecordBudget = 1 << 20
const StateBudget = 32 << 20
const StateFileLimit = 128

// FileJournal is bounded root-owned diagnostic history, distinct from the
// package's CJ-1 result/evidence store. It cannot produce a qualified result.
type FileJournal struct {
	mu   sync.Mutex
	file *os.File
	used int64
}

// Failure to retain evidence may never remove the cleanup obligation. This
// fallback records no successful history and causes a diagnostic fault, while
// leaving the independent native kill/rescan path operational.
type unavailableJournal struct{ err error }

func (j unavailableJournal) Append(Record) error { return j.err }

func OpenJournal(state, name string) (*FileJournal, error) {
	if err := CheckInstalledPath(state, true); err != nil {
		return nil, err
	}
	if filepath.Base(name) != name || name == "." || name == ".." {
		return nil, fmt.Errorf("invalid diagnostic journal token")
	}
	if err := stateCapacity(state, 1, 0); err != nil {
		return nil, err
	}
	f, err := os.OpenFile(filepath.Join(state, name), os.O_CREATE|os.O_EXCL|os.O_WRONLY|syscall.O_NOFOLLOW, 0600)
	if err != nil {
		return nil, err
	}
	return &FileJournal{file: f}, nil
}
func (j *FileJournal) Append(r Record) error {
	j.mu.Lock()
	defer j.mu.Unlock()
	b, err := json.Marshal(r)
	if err != nil {
		return err
	}
	if len(b) > JournalRecordBudget || j.used+int64(len(b)+1) > JournalBudget {
		return fmt.Errorf("bounded diagnostic journal exhausted")
	}
	if err := stateCapacity(filepath.Dir(j.file.Name()), 0, int64(len(b)+1)); err != nil {
		return err
	}
	b = append(b, '\n')
	n, err := j.file.Write(b)
	j.used += int64(n)
	if err != nil {
		return err
	}
	if n != len(b) {
		return fmt.Errorf("partial diagnostic journal write")
	}
	return j.file.Sync()
}
func (j *FileJournal) Close() error { return j.file.Close() }

func durableInstalled(path string, raw []byte) error {
	if len(raw) > JournalRecordBudget {
		return fmt.Errorf("bounded installed record required")
	}
	if err := stateCapacity(filepath.Dir(path), 1, int64(len(raw))); err != nil {
		return err
	}
	f, err := os.OpenFile(path, os.O_CREATE|os.O_EXCL|os.O_WRONLY|syscall.O_NOFOLLOW, 0600)
	if err != nil {
		return err
	}
	if _, err = f.Write(raw); err == nil {
		err = f.Sync()
	}
	if ce := f.Close(); err == nil {
		err = ce
	}
	if err != nil {
		return err
	}
	d, err := os.Open(filepath.Dir(path))
	if err != nil {
		return err
	}
	defer d.Close()
	return d.Sync()
}

func stateCapacity(state string, additionalFiles int, additionalBytes int64) error {
	entries, err := os.ReadDir(state)
	if err != nil {
		return err
	}
	if len(entries)+additionalFiles > StateFileLimit {
		return fmt.Errorf("diagnostic state file capacity exhausted; archive evidence as operator")
	}
	var bytes int64
	for _, entry := range entries {
		st, err := entry.Info()
		if err != nil {
			return err
		}
		if !st.Mode().IsRegular() {
			return fmt.Errorf("unexpected diagnostic state object")
		}
		if st.Size() > StateBudget-bytes {
			return fmt.Errorf("diagnostic state byte capacity exhausted")
		}
		bytes += st.Size()
	}
	if additionalBytes > StateBudget-bytes {
		return fmt.Errorf("diagnostic state byte capacity exhausted; archive evidence as operator")
	}
	return nil
}
