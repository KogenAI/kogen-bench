package verify

// Family D fixtures (model-free): Kogen's 60 s dead-command stop at its REAL default grace
// (noLiveGrace = 1 min), not the shortened test value. Copy to cli/verify/ of a private checkout.

import (
	"testing"
	"time"

	"kogen-loop/sys"
)

// A command whose group has ended but whose result never arrives: wall to the stop at default grace.
func TestFPHDeadCommandStopAtDefaultGrace(t *testing.T) {
	root := t.TempDir()
	s := sys.NewWith(testEnv(), root)
	before := groupSet(s)
	if res, err := s.Run("printf done", root, sys.Options{}); err != nil || res.Output != "done" {
		t.Fatalf("%+v %v", res, err)
	}
	log := &memLog{}
	t0 := time.Now()
	_, err := awaitResult(s, before, "acceptance", "printf done", log, make(chan outcome))
	wall := time.Since(t0)
	e, ok := sys.AsError(err)
	if !ok || e.Reason != "command_no_progress" {
		t.Fatalf("error = %v", err)
	}
	t.Logf("FPH dead-command stop after %.2fs (grace %s); events=%d detail=%q", wall.Seconds(), noLiveGrace, len(log.named("command_no_progress")), e.Detail)
	if wall < 59*time.Second || wall > 63*time.Second {
		t.Errorf("wall %v outside 59-63 s", wall)
	}
}

// A live, silent command (no output for 75 s, longer than the grace) must not be stopped.
func TestFPHLiveSilentCommandNotStopped(t *testing.T) {
	root := t.TempDir()
	s := sys.NewWith(testEnv(), root)
	log := &memLog{}
	t0 := time.Now()
	res, err := RunWatched(s, "setup", "sleep 75; printf ok", log, func() (sys.Result, error) {
		return s.Run("sleep 75; printf ok", root, sys.Options{})
	})
	t.Logf("FPH live silent command: wall %.2fs err=%v out=%q events=%d", time.Since(t0).Seconds(), err, res.Output, len(log.named("command_no_progress")))
	if err != nil || res.Output != "ok" || len(log.named("command_no_progress")) != 0 {
		t.Fatalf("false stop: %v %q", err, res.Output)
	}
}

// A command that exits leaving a background child holding the output pipe (group still live, then dead).
func TestFPHBackgroundChildHoldsPipe(t *testing.T) {
	root := t.TempDir()
	s := sys.NewWith(testEnv(), root)
	log := &memLog{}
	cmd := "(sleep 70 &) ; printf hi"
	t0 := time.Now()
	res, err := RunWatched(s, "setup", cmd, log, func() (sys.Result, error) { return s.Run(cmd, root, sys.Options{}) })
	t.Logf("FPH bg child: wall %.2fs err=%v out=%q events=%d", time.Since(t0).Seconds(), err, res.Output, len(log.named("command_no_progress")))
	if err != nil || len(log.named("command_no_progress")) != 0 {
		t.Fatalf("unexpected stop: %v", err)
	}
}
