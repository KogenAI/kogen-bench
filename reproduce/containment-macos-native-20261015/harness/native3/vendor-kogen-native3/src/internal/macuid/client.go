package macuid

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"time"
)

// Client is the controller-side (non-root) end of the custodian's local
// channel. Every connection verifies that the peer is the root custodian.
type Client struct{ Socket string }

func (c Client) dial(ctx context.Context) (*net.UnixConn, *bufio.Reader, error) {
	if !pathOK(c.Socket) {
		return nil, nil, fmt.Errorf("canonical installed socket required")
	}
	conn, err := (&net.Dialer{}).DialContext(ctx, "unix", c.Socket)
	if err != nil {
		return nil, nil, err
	}
	u, ok := conn.(*net.UnixConn)
	if !ok {
		conn.Close()
		return nil, nil, fmt.Errorf("private Unix transport required")
	}
	if peer, perr := PeerUID(u); perr != nil || peer != 0 {
		u.Close()
		return nil, nil, fmt.Errorf("root custodian peer required")
	}
	return u, bufio.NewReaderSize(u, 64<<10), nil
}

func oneShot(ctx context.Context, c Client, frame string, out any) error {
	u, r, err := c.dial(ctx)
	if err != nil {
		return err
	}
	defer u.Close()
	dl := time.Now().Add(30 * time.Second)
	if d, ok := ctx.Deadline(); ok {
		dl = d
	}
	u.SetDeadline(dl)
	if _, err = io.WriteString(u, frame); err != nil {
		return err
	}
	line, err := readFrame(r, MaxLaunchFrame)
	if err != nil {
		return err
	}
	return json.Unmarshal(line, out)
}

type StatusFrame struct {
	Status      string `json:"status"`
	Launch      int    `json:"launch"`
	Qualified   bool   `json:"qualified"`
	Quarantined bool   `json:"quarantined"`
}

// Status proves a live custodian that supports `launch`.
func (c Client) Status(ctx context.Context) (StatusFrame, error) {
	var s StatusFrame
	err := oneShot(ctx, c, "{\"operation\":\"status\",\"version\":1}\n", &s)
	if err == nil {
		err = s.Check()
	}
	return s, err
}

// Check is the admission rule for a status answer: a live custodian that offers
// native launch and is not qualified-claiming.
func (s StatusFrame) Check() error {
	if s.Status != "ready" || s.Launch != LaunchVersion || s.Qualified {
		return fmt.Errorf("custodian does not offer native launch")
	}
	return nil
}

func (c Client) Reconcile(ctx context.Context) (ReconcileResult, error) {
	var r ReconcileResult
	return r, oneShot(ctx, c, "{\"operation\":\"reconcile\",\"version\":1}\n", &r)
}

type StartedFrame struct {
	Status string `json:"status"`
	Scope  string `json:"scope"`
	PID    int    `json:"pid"`
	Code   string `json:"code"`
	Reason string `json:"reason"`
}

// Session is one running Build owned by this connection. Closing it (or the
// controller dying) revokes the Build: the custodian terminates and verifies.
type Session struct {
	conn    *net.UnixConn
	reader  *bufio.Reader
	Started StartedFrame
}

// Launch sends the request and returns after the custodian acknowledged that
// the candidate was spawned (or refused, as a *Refusal).
func (c Client) Launch(ctx context.Context, req LaunchRequest) (*Session, error) {
	req.Operation, req.Version = "launch", LaunchVersion
	b, err := json.Marshal(req)
	if err != nil {
		return nil, err
	}
	u, r, err := c.dial(ctx)
	if err != nil {
		return nil, err
	}
	u.SetDeadline(time.Now().Add(30 * time.Second))
	if _, err = u.Write(append(b, '\n')); err != nil {
		u.Close()
		return nil, err
	}
	line, err := readFrame(r, MaxLaunchFrame)
	if err != nil {
		u.Close()
		return nil, err
	}
	var ack StartedFrame
	if err = json.Unmarshal(line, &ack); err != nil {
		u.Close()
		return nil, err
	}
	if ack.Status == "refused" {
		u.Close()
		return nil, &Refusal{Code: ack.Code, Reason: ack.Reason}
	}
	if ack.Status != "started" || ack.Scope == "" {
		u.Close()
		return nil, fmt.Errorf("unexpected custodian acknowledgement")
	}
	u.SetDeadline(time.Time{})
	return &Session{conn: u, reader: r, Started: ack}, nil
}

func (s *Session) Stop() error {
	s.conn.SetWriteDeadline(time.Now().Add(5 * time.Second))
	_, err := io.WriteString(s.conn, "{\"operation\":\"stop\",\"version\":1}\n")
	return err
}

// Wait returns the custodian's final result. A closed connection without a
// result is reported as an error (the caller must Reconcile).
func (s *Session) Wait(ctx context.Context) (*LaunchResult, error) {
	stop := context.AfterFunc(ctx, func() { s.conn.SetReadDeadline(time.Now()) })
	defer stop()
	line, err := readFrame(s.reader, MaxLaunchFrame)
	if err != nil {
		return nil, err
	}
	var f struct {
		Status string        `json:"status"`
		Result *LaunchResult `json:"result"`
	}
	if err = json.Unmarshal(line, &f); err != nil {
		return nil, err
	}
	if (f.Status != "finished" && f.Status != "uncertain") || f.Result == nil {
		return nil, fmt.Errorf("unexpected custodian result frame")
	}
	return f.Result, nil
}

func (s *Session) Close() error { return s.conn.Close() }
