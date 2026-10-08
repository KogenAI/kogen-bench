package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"syscall"
	"unicode/utf8"
)

type job struct {
	ID       string   `json:"id"`
	Argv     []string `json:"argv"`
	Attempts int      `json:"attempts"`
	Done     bool     `json:"done"`
	ExitCode int      `json:"exit_code"`
	Stdout   string   `json:"stdout"`
	Stderr   string   `json:"stderr"`
}
type storeState struct {
	Jobs []job `json:"jobs"`
}
type result struct {
	ID       string `json:"id"`
	Attempt  int    `json:"attempt"`
	ExitCode int    `json:"exit_code"`
	Stdout   string `json:"stdout"`
	Stderr   string `json:"stderr"`
	Status   string `json:"status"`
}

var idPattern = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`)

func execute(args []string) (string, int, error) {
	cmd, vals, ok := parseArgs(args)
	if !ok {
		return "", 2, errors.New("error: invalid arguments")
	}
	store := vals["--store"]
	if err := os.MkdirAll(store, 0755); err != nil {
		return "", 4, errors.New("error: store failure")
	}
	lock, err := os.OpenFile(filepath.Join(store, ".lock"), os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		return "", 4, errors.New("error: store failure")
	}
	defer func() { _ = lock.Close() }()
	if err = syscall.Flock(int(lock.Fd()), syscall.LOCK_EX); err != nil {
		return "", 4, errors.New("error: store failure")
	}
	defer syscall.Flock(int(lock.Fd()), syscall.LOCK_UN) //nolint:errcheck
	state, err := readState(store)
	if err != nil {
		return "", 4, errors.New("error: store failure")
	}
	switch cmd {
	case "add":
		id := vals["--id"]
		for _, item := range state.Jobs {
			if item.ID == id {
				return "", 3, errors.New("error: duplicate job id")
			}
		}
		var argv []string
		if json.Unmarshal([]byte(vals["--argv"]), &argv) != nil || len(argv) == 0 {
			return "", 2, errors.New("error: invalid arguments")
		}
		for _, value := range argv {
			if value == "" || strings.ContainsRune(value, 0) {
				return "", 2, errors.New("error: invalid arguments")
			}
		}
		state.Jobs = append(state.Jobs, job{ID: id, Argv: argv})
		if err := writeState(store, state); err != nil {
			return "", 4, errors.New("error: store failure")
		}
		return "queued " + id + "\n", 0, nil
	case "status":
		var out strings.Builder
		for _, item := range state.Jobs {
			if !item.Done {
				fmt.Fprintf(&out, "%s pending\n", item.ID)
			} else if item.ExitCode == 0 {
				fmt.Fprintf(&out, "%s succeeded\n", item.ID)
			} else {
				fmt.Fprintf(&out, "%s failed %d\n", item.ID, item.ExitCode)
			}
		}
		return out.String(), 0, nil
	case "run":
		results := make([]result, 0)
		for i := range state.Jobs {
			item := &state.Jobs[i]
			if item.Done {
				continue
			}
			item.Attempts++
			if err := writeState(store, state); err != nil {
				return "", 4, errors.New("error: store failure")
			}
			cmd := exec.Command(item.Argv[0], item.Argv[1:]...)
			var stdout, stderr bytes.Buffer
			cmd.Stdout, cmd.Stderr = &stdout, &stderr
			runErr := cmd.Run()
			code := 0
			if runErr != nil {
				var exitErr *exec.ExitError
				if errors.As(runErr, &exitErr) {
					code = exitErr.ExitCode()
					if code < 0 {
						if ws, ok := exitErr.Sys().(syscall.WaitStatus); ok {
							code = 128 + int(ws.Signal())
						}
					}
				} else {
					code, stderr = 127, *bytes.NewBufferString("exec failed\n")
				}
			}
			item.Done, item.ExitCode = true, code
			item.Stdout, item.Stderr = replaceInvalid(stdout.Bytes()), replaceInvalid(stderr.Bytes())
			if err := writeState(store, state); err != nil {
				return "", 4, errors.New("error: store failure")
			}
			status := "failed"
			if code == 0 {
				status = "succeeded"
			}
			results = append(results, result{ID: item.ID, Attempt: item.Attempts, ExitCode: code, Stdout: item.Stdout, Stderr: item.Stderr, Status: status})
		}
		var out strings.Builder
		enc := json.NewEncoder(&out)
		enc.SetEscapeHTML(false)
		for _, row := range results {
			if err := enc.Encode(row); err != nil {
				return "", 4, errors.New("error: store failure")
			}
		}
		return out.String(), 0, nil
	}
	return "", 2, errors.New("error: invalid arguments")
}

func parseArgs(args []string) (string, map[string]string, bool) {
	if len(args) < 2 || args[0] != "queue" {
		return "", nil, false
	}
	cmd := args[1]
	if cmd != "add" && cmd != "run" && cmd != "status" {
		return "", nil, false
	}
	allowed := map[string]bool{"--store": true}
	if cmd == "add" {
		allowed["--id"], allowed["--argv"] = true, true
	}
	vals := make(map[string]string)
	for i := 2; i < len(args); i++ {
		key := args[i]
		_, duplicate := vals[key]
		if !allowed[key] || duplicate || i+1 >= len(args) {
			return "", nil, false
		}
		i++
		vals[key] = args[i]
	}
	if vals["--store"] == "" {
		return "", nil, false
	}
	if cmd == "add" {
		if vals["--id"] == "" || !idPattern.MatchString(vals["--id"]) || vals["--argv"] == "" {
			return "", nil, false
		}
	}
	return cmd, vals, true
}
func readState(store string) (storeState, error) {
	data, err := os.ReadFile(filepath.Join(store, "state.json"))
	if errors.Is(err, os.ErrNotExist) {
		return storeState{Jobs: []job{}}, nil
	}
	if err != nil {
		return storeState{}, err
	}
	var state storeState
	if err = json.Unmarshal(data, &state); err != nil || state.Jobs == nil {
		return storeState{}, errors.New("corrupt state")
	}
	return state, nil
}
func writeState(store string, state storeState) error {
	data, err := json.Marshal(state)
	if err != nil {
		return err
	}
	tmp, err := os.CreateTemp(store, ".state-*")
	if err != nil {
		return err
	}
	name := tmp.Name()
	defer func() { _ = os.Remove(name) }()
	if _, err = tmp.Write(data); err == nil {
		err = tmp.Sync()
	}
	if closeErr := tmp.Close(); err == nil {
		err = closeErr
	}
	if err != nil {
		return err
	}
	if err = os.Rename(name, filepath.Join(store, "state.json")); err != nil {
		return err
	}
	dir, err := os.Open(store)
	if err != nil {
		return err
	}
	syncErr := dir.Sync()
	closeErr := dir.Close()
	if syncErr != nil {
		return syncErr
	}
	return closeErr
}
func replaceInvalid(data []byte) string {
	var b strings.Builder
	for len(data) > 0 {
		r, size := utf8.DecodeRune(data)
		if r == utf8.RuneError && size == 1 {
			b.WriteRune('\uFFFD')
			data = data[1:]
		} else {
			b.Write(data[:size])
			data = data[size:]
		}
	}
	return b.String()
}
