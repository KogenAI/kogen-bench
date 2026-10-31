package main

import (
	"context"
	"flag"
	"fmt"
	"io"
	"host-withheld/containment/internal/macuid"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	if handled, err := macuid.SignalRole(os.Args[1:]); handled {
		finish(err)
		return
	}
	ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer cancel()
	if len(os.Args) == 3 && os.Args[1] == "--macuid-watchdog" {
		finish(macuid.WatchdogRole(ctx, os.Args[2], os.Stdin, os.Stdout))
		return
	}
	config := flag.String("config", "", "absolute root-installed service descriptor")
	lease := flag.Bool("diagnostic-lease", false, "hold operator-only diagnostic lease until stdin EOF; never runs a candidate")
	inspect := flag.Bool("inspect", false, "inspect reserved UID membership without signaling")
	reset := flag.Bool("reset-diagnostic-slot", false, "root-only drain and diagnostic fence reset; launchd job must be booted out")
	flag.Parse()
	if *config == "" || flag.NArg() != 0 {
		finish(fmt.Errorf("--config is required"))
		return
	}
	modes := 0
	for _, enabled := range []bool{*lease, *inspect, *reset} {
		if enabled {
			modes++
		}
	}
	if modes > 1 {
		finish(fmt.Errorf("one operator mode at a time"))
		return
	}
	if *inspect {
		finish(macuid.OperatorInspect(ctx, *config, os.Stdout))
		return
	}
	if *reset {
		finish(macuid.OperatorResetDiagnostic(ctx, *config, os.Stdout))
		return
	}
	if *lease {
		c, err := macuid.LoadConfig(*config)
		if err != nil {
			finish(err)
			return
		}
		conn, scope, err := macuid.DiagnosticLease(ctx, c.Socket)
		if err != nil {
			finish(err)
			return
		}
		defer conn.Close()
		fmt.Printf("diagnostic scope %s; qualified=false\n", scope)
		stdinDone := make(chan error, 1)
		go func() { _, err := io.Copy(io.Discard, os.Stdin); stdinDone <- err }()
		select {
		case err = <-stdinDone:
			finish(err)
		case <-ctx.Done():
			_ = conn.Close()
		}
		return
	}
	finish(macuid.Serve(ctx, *config))
}
func finish(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
