package macuid

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"io"
	"net"
	"os/user"
	"strconv"
	"sync"
	"time"
)

var errFrameTooLarge = errors.New("control frame too large")

// readFrame reads one newline-terminated frame of at most max bytes.
func readFrame(r *bufio.Reader, max int) ([]byte, error) {
	var out []byte
	for {
		part, err := r.ReadSlice('\n')
		out = append(out, part...)
		if len(out) > max {
			return nil, errFrameTooLarge
		}
		if err == nil {
			return out, nil
		}
		if err != bufio.ErrBufferFull {
			return nil, err
		}
	}
}

func lookupHome(uid uint32) (string, error) {
	u, err := user.LookupId(strconv.FormatUint(uint64(uid), 10))
	if err != nil {
		return "", err
	}
	return u.HomeDir, nil
}

func decodeLaunch(frame []byte) (LaunchRequest, error) {
	var req LaunchRequest
	frame = bytes.TrimSuffix(frame, []byte("\n"))
	if !uniqueJSON(frame) {
		return req, errors.New("closed bounded launch JSON required")
	}
	d := json.NewDecoder(bytes.NewReader(frame))
	d.DisallowUnknownFields()
	if err := d.Decode(&req); err != nil {
		return req, err
	}
	var tail any
	if d.Decode(&tail) != io.EOF {
		return req, errors.New("trailing launch JSON")
	}
	return req, nil
}

func writeFrame(conn net.Conn, v any) error {
	b, err := json.Marshal(v)
	if err != nil {
		return err
	}
	conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
	_, err = conn.Write(append(b, '\n'))
	return err
}

// ServeLaunch handles one authenticated `launch` connection: it decodes the
// Policy-shaped request, runs the Build, relays `started`, honors a later
// `stop` frame, treats connection loss as owner death, and finally sends the
// complete result. The caller closes conn afterwards.
func (c *Custodian) ServeLaunch(ctx context.Context, conn net.Conn, reader *bufio.Reader, frame []byte) {
	req, err := decodeLaunch(frame)
	if err != nil {
		writeFrame(conn, map[string]any{"status": "refused", "code": "invalid", "reason": err.Error()})
		return
	}
	conn.SetReadDeadline(time.Time{})
	stop, lost := make(chan struct{}), make(chan struct{})
	var once sync.Once
	go func() {
		defer close(lost)
		for {
			line, rerr := readFrame(reader, 4096)
			if rerr != nil {
				return
			}
			if string(line) == "{\"operation\":\"stop\",\"version\":1}\n" {
				once.Do(func() { close(stop) })
			}
		}
	}()
	res, refusal := c.Launch(ctx, req, LaunchControl{Stop: stop, OwnerLost: lost}, func(scope string, pid int) {
		writeFrame(conn, map[string]any{"status": "started", "scope": scope, "pid": pid, "qualified": false})
	})
	if refusal != nil {
		writeFrame(conn, map[string]any{"status": "refused", "code": refusal.Code, "reason": refusal.Reason})
		return
	}
	status := "finished"
	if res.Uncertain {
		status = "uncertain"
	}
	writeFrame(conn, map[string]any{"status": status, "result": res})
}
