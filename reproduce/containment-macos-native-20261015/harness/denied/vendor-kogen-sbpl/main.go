// cmpmac-sbpl runs Kogen's macOS launch planning for one CMP-MAC cell.
//
// macuid/policy.go is a byte-identical copy of closer-D's patched
// kogen-containment/impl/internal/macuid/policy.go (dyld root read, runtime
// sysctls, ancestor metadata); cmp_mac.py pins its sha256.
//
// Input: one JSON macuid.Policy on stdin. Output: the macuid.LaunchPlan result
// (path, args, cwd, env) as JSON. LaunchPlan's UID/GID fields describe M2's
// reserved-user drop, which needs admin provisioning; this harness runs
// unprivileged and discards them (it passes the caller's uid for both).
package main

import (
	"encoding/json"
	"fmt"
	"os"

	"host-withheld/cmpmac-sbpl/macuid"
)

type out struct {
	Path        string   `json:"path"`
	Args        []string `json:"args"`
	Cwd         string   `json:"cwd"`
	Env         []string `json:"env"`
	StdinClosed bool     `json:"stdin_closed"`
	Profile     string   `json:"profile"`
}

func main() {
	var p macuid.Policy
	dec := json.NewDecoder(os.Stdin)
	dec.DisallowUnknownFields()
	if err := dec.Decode(&p); err != nil {
		fmt.Fprintln(os.Stderr, "policy decode:", err)
		os.Exit(2)
	}
	uid := uint32(os.Getuid())
	spec, err := macuid.LaunchPlan(p, uid, uid)
	if err != nil {
		fmt.Fprintln(os.Stderr, "launch plan:", err)
		os.Exit(3)
	}
	sb, err := macuid.CompileSeatbelt(p)
	if err != nil {
		fmt.Fprintln(os.Stderr, "compile:", err)
		os.Exit(3)
	}
	if err := json.NewEncoder(os.Stdout).Encode(out{spec.Path, spec.Args, spec.Cwd, spec.Env, spec.StdinClosed, sb}); err != nil {
		os.Exit(4)
	}
}
