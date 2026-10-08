package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type event struct {
	ID   string
	Type string
	Job  string
	TS   int64
	Line int
}

var eventID = regexp.MustCompile(`^e-[a-z0-9]{1,16}$`)
var jobID = regexp.MustCompile(`^[a-z][a-z0-9-]{0,31}$`)

func parseEvent(raw []byte, line int) (event, error) {
	var out event
	dec := json.NewDecoder(bytes.NewReader(raw))
	tok, err := dec.Token()
	if err != nil || tok != json.Delim('{') {
		return out, errors.New("invalid")
	}
	seen := map[string]bool{}
	vals := map[string]json.RawMessage{}
	for dec.More() {
		keyToken, e := dec.Token()
		if e != nil {
			return out, errors.New("invalid")
		}
		key, ok := keyToken.(string)
		if !ok || seen[key] {
			return out, errors.New("invalid")
		}
		seen[key] = true
		var value json.RawMessage
		if e = dec.Decode(&value); e != nil {
			return out, errors.New("invalid")
		}
		vals[key] = value
	}
	if _, err = dec.Token(); err != nil {
		return out, errors.New("invalid")
	}
	if _, err = dec.Token(); err != io.EOF {
		return out, errors.New("invalid")
	}
	if len(vals) != 4 || !seen["id"] || !seen["type"] || !seen["job"] || !seen["ts"] {
		return out, errors.New("invalid")
	}
	if json.Unmarshal(vals["id"], &out.ID) != nil || json.Unmarshal(vals["type"], &out.Type) != nil || json.Unmarshal(vals["job"], &out.Job) != nil {
		return out, errors.New("invalid")
	}
	var number json.Number
	nd := json.NewDecoder(bytes.NewReader(vals["ts"]))
	nd.UseNumber()
	if nd.Decode(&number) != nil {
		return out, errors.New("invalid")
	}
	var nerr error
	out.TS, nerr = strconv.ParseInt(number.String(), 10, 64)
	if nerr != nil || out.TS < 0 || !eventID.MatchString(out.ID) || !jobID.MatchString(out.Job) {
		return out, errors.New("invalid")
	}
	if out.Type != "created" && out.Type != "started" && out.Type != "completed" && out.Type != "failed" {
		return out, fmt.Errorf("unknown:%s", out.Type)
	}
	out.Line = line
	return out, nil
}

func readLog(path string) ([]event, error) {
	data, err := os.ReadFile(path)
	if err != nil && !os.IsNotExist(err) {
		return nil, errors.New("eventlog: cannot access log")
	}
	if os.IsNotExist(err) {
		return []event{}, nil
	}
	lines := bytes.Split(data, []byte("\n"))
	complete := len(lines) - 1
	if len(data) == 0 {
		complete = 0
	}
	events := []event{}
	ids := map[string]bool{}
	for i := 0; i < complete; i++ {
		if len(lines[i]) == 0 {
			return nil, fmt.Errorf("eventlog:%d: invalid event", i+1)
		}
		e, eerr := parseEvent(lines[i], i+1)
		if eerr != nil {
			if strings.HasPrefix(eerr.Error(), "unknown:") {
				return nil, fmt.Errorf("eventlog:%d: unknown event type '%s'", i+1, strings.TrimPrefix(eerr.Error(), "unknown:"))
			}
			return nil, fmt.Errorf("eventlog:%d: invalid event", i+1)
		}
		if ids[e.ID] {
			return nil, fmt.Errorf("eventlog:%d: duplicate event id '%s'", i+1, e.ID)
		}
		ids[e.ID] = true
		events = append(events, e)
	}
	return events, nil
}

func transitionErr(e event) error {
	return fmt.Errorf("eventlog:%d: invalid transition for job '%s'", e.Line, e.Job)
}

func reconcile(events []event) (string, error) {
	ordered := append([]event(nil), events...)
	sort.Slice(ordered, func(i, j int) bool {
		if ordered[i].TS == ordered[j].TS {
			return ordered[i].Line < ordered[j].Line
		}
		return ordered[i].TS < ordered[j].TS
	})
	states := map[string]string{}
	lastTS := map[string]int64{}
	seenTS := map[string]bool{}
	counts := map[string]int{"queued": 0, "running": 0, "done": 0, "failed": 0}
	for _, e := range ordered {
		if seenTS[e.Job] && lastTS[e.Job] == e.TS {
			return "", transitionErr(e)
		}
		seenTS[e.Job] = true
		lastTS[e.Job] = e.TS
		state := states[e.Job]
		switch e.Type {
		case "created":
			if state != "" {
				return "", transitionErr(e)
			}
			states[e.Job] = "queued"
		case "started":
			if state != "queued" {
				return "", transitionErr(e)
			}
			states[e.Job] = "running"
		case "completed":
			if state != "running" {
				return "", transitionErr(e)
			}
			states[e.Job] = "done"
		case "failed":
			if state != "running" {
				return "", transitionErr(e)
			}
			states[e.Job] = "failed"
		}
	}
	for _, state := range states {
		counts[state]++
	}
	return fmt.Sprintf("total=%d\nqueued=%d\nrunning=%d\ndone=%d\nfailed=%d\n", len(states), counts["queued"], counts["running"], counts["done"], counts["failed"]), nil
}

func eventJSON(e event) string {
	b, _ := json.Marshal(struct {
		ID   string `json:"id"`
		Type string `json:"type"`
		Job  string `json:"job"`
		TS   int64  `json:"ts"`
	}{e.ID, e.Type, e.Job, e.TS})
	return string(b)
}

func task6(args []string) (string, int, error) {
	if len(args) == 3 && args[0] == "reconcile" && args[1] == "--log" {
		events, err := readLog(args[2])
		if err != nil {
			return "", 1, err
		}
		out, err := reconcile(events)
		if err != nil {
			return "", 1, err
		}
		return out, 0, nil
	}
	if len(args) == 5 && args[0] == "append" && args[1] == "--log" && args[3] == "--event" {
		path := args[2]
		e, err := parseEvent([]byte(args[4]), 1)
		if err != nil {
			if strings.HasPrefix(err.Error(), "unknown:") {
				return "", 1, fmt.Errorf("eventlog:1: unknown event type '%s'", strings.TrimPrefix(err.Error(), "unknown:"))
			}
			return "", 1, errors.New("eventlog:1: invalid event")
		}
		old, err := os.ReadFile(path)
		if err != nil && !os.IsNotExist(err) {
			return "", 1, errors.New("eventlog: cannot access log")
		}
		if len(old) > 0 && old[len(old)-1] != '\n' {
			return "", 1, fmt.Errorf("eventlog:%d: invalid event", bytes.Count(old, []byte("\n"))+1)
		}
		if len(old) > 0 {
			existing, er := readLog(path)
			if er != nil {
				return "", 1, er
			}
			for _, x := range existing {
				if x.ID == e.ID {
					return "", 1, fmt.Errorf("eventlog:%d: duplicate event id '%s'", x.Line, e.ID)
				}
			}
		}
		f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
		if err != nil {
			return "", 1, errors.New("eventlog: cannot access log")
		}
		_, err = f.WriteString(eventJSON(e) + "\n")
		closeErr := f.Close()
		if err != nil || closeErr != nil {
			return "", 1, errors.New("eventlog: cannot access log")
		}
		return "appended " + e.ID + "\n", 0, nil
	}
	return "", 2, errors.New("eventlog: usage error")
}

func execute(args []string) (string, int, error) { return task6(args) }
