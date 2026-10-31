//go:build darwin

package macuid

import (
	"bytes"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"testing"
	"time"
)

// These tests enforce the generated v1 profile with the REAL /usr/bin/sandbox-exec
// as the CURRENT user (no uid drop, no root, no sudo, no account). They prove
// the profile semantics; uid-based cleanup needs the installed custodian.

type sbFixture struct {
	root, ws, secretDir, secret, outside string
}

func newSandboxFixture(t *testing.T) sbFixture {
	t.Helper()
	probe := exec.Command("/usr/bin/sandbox-exec", "-p", "(version 1)(allow default)", "/usr/bin/true")
	if err := probe.Run(); err != nil {
		t.Skip("sandbox-exec cannot apply a profile here:", err)
	}
	base, err := filepath.EvalSymlinks(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}
	f := sbFixture{root: base, ws: filepath.Join(base, "ws"), secretDir: filepath.Join(base, "home", ".ssh"), outside: filepath.Join(base, "outside")}
	f.secret = filepath.Join(f.secretDir, "id_test")
	for _, d := range []string{f.ws, f.secretDir, f.outside} {
		if err = os.MkdirAll(d, 0o755); err != nil {
			t.Fatal(err)
		}
	}
	os.WriteFile(f.secret, []byte("PLANTED-SECRET\n"), 0o600)
	os.WriteFile(filepath.Join(f.outside, "readable.txt"), []byte("public\n"), 0o644)
	return f
}

func (f sbFixture) policy(env map[string]string, argv ...string) Policy {
	return Policy{Command: "/bin/sh", Argv: argv, Cwd: f.ws, Env: env, Read: []string{"/bin"}, Write: []string{f.ws},
		Protected: append(SecretPaths(filepath.Join(f.root, "home")), f.secretDir), ReadBroad: true}
}

func (f sbFixture) run(t *testing.T, p Policy) (string, int) {
	t.Helper()
	spec, err := LaunchPlan(p, 501, 501)
	if err != nil {
		t.Fatal(err)
	}
	cmd := exec.Command(spec.Path, spec.Args[1:]...)
	cmd.Dir, cmd.Env = spec.Cwd, spec.Env
	var out bytes.Buffer
	cmd.Stdout, cmd.Stderr = &out, &out
	err = cmd.Run()
	code := 0
	if ee, ok := err.(*exec.ExitError); ok {
		code = ee.ExitCode()
	} else if err != nil {
		t.Fatal(err)
	}
	return out.String(), code
}

func TestRealSeatbeltWritesConfinedToWritableRoots(t *testing.T) {
	f := newSandboxFixture(t)
	out, code := f.run(t, f.policy(map[string]string{}, "-c", "echo ok > "+f.ws+"/in.txt && echo inside-ok"))
	if code != 0 || !strings.Contains(out, "inside-ok") {
		t.Fatal("write inside the writable root must work", out)
	}
	for name, script := range map[string]string{
		"outside-root": "echo x > " + f.outside + "/evil.txt",
		"secret-dir":   "echo x > " + f.secretDir + "/evil.txt",
		"rename-out":   "mv " + f.ws + "/in.txt " + f.outside + "/moved.txt",
		"home-dotfile": "echo x > " + f.root + "/home/.bashrc",
		"mkdir-out":    "mkdir " + f.outside + "/newdir",
		"unlink-out":   "rm " + f.outside + "/readable.txt",
	} {
		_, code = f.run(t, f.policy(map[string]string{}, "-c", script))
		if code == 0 {
			t.Fatalf("%s: write outside the writable roots was allowed", name)
		}
	}
	// A symlink planted inside the writable root cannot redirect a write out of it.
	if err := os.Symlink(f.outside, filepath.Join(f.ws, "escape")); err != nil {
		t.Fatal(err)
	}
	if _, code = f.run(t, f.policy(map[string]string{}, "-c", "echo x > "+f.ws+"/escape/via-link.txt")); code == 0 {
		t.Fatal("write through a symlink left the writable root")
	}
	if _, err := os.Lstat(filepath.Join(f.outside, "via-link.txt")); err == nil {
		t.Fatal("symlink write landed outside the writable root")
	}
	for _, p := range []string{"evil.txt", "moved.txt", "newdir", ".bashrc"} {
		for _, dir := range []string{f.outside, f.secretDir, filepath.Join(f.root, "home")} {
			if _, err := os.Lstat(filepath.Join(dir, p)); err == nil {
				t.Fatalf("%s appeared in %s", p, dir)
			}
		}
	}
	if _, err := os.Stat(filepath.Join(f.outside, "readable.txt")); err != nil {
		t.Fatal("unlink outside root succeeded")
	}
}

func TestRealSeatbeltSecretsUnreadableButOtherReadsWork(t *testing.T) {
	f := newSandboxFixture(t)
	out, code := f.run(t, f.policy(map[string]string{}, "-c", "cat "+f.outside+"/readable.txt"))
	if code != 0 || strings.TrimSpace(out) != "public" {
		t.Fatal("broad reads outside the secret list must work", out)
	}
	for name, script := range map[string]string{
		"cat":      "cat " + f.secret,
		"ls":       "ls " + f.secretDir,
		"stat":     "stat " + f.secret,
		"firmlink": "cat /System/Volumes/Data" + f.secret,
		"exec":     "cp /bin/echo " + f.ws + "/e && " + f.secretDir + "/id_test",
	} {
		out, code = f.run(t, f.policy(map[string]string{}, "-c", script))
		if code == 0 || strings.Contains(out, "PLANTED-SECRET") {
			t.Fatalf("%s: secret readable: %q", name, out)
		}
	}
	// A symlink inside the writable root pointing at the secret is still denied.
	if err := os.Symlink(f.secret, filepath.Join(f.ws, "alias")); err != nil {
		t.Fatal(err)
	}
	out, code = f.run(t, f.policy(map[string]string{}, "-c", "cat "+f.ws+"/alias"))
	if code == 0 || strings.Contains(out, "PLANTED-SECRET") {
		t.Fatal("symlink alias leaked the secret", out)
	}
}

func TestRealSeatbeltEnvironmentIsExactlyTheAllowlist(t *testing.T) {
	f := newSandboxFixture(t)
	t.Setenv("KOGEN_LEAK_PROBE", "leaked")
	t.Setenv("HOME", f.root)
	env := map[string]string{"B": "two words", "A": "$HOME", "PATH": "/usr/bin:/bin"}
	out, code := f.run(t, f.policy(env, "-c", "/usr/bin/env"))
	if code != 0 {
		t.Fatal(out)
	}
	got := strings.Split(strings.TrimSpace(out), "\n")
	sort.Strings(got)
	// /bin/sh (bash) may add PWD, SHLVL and _; nothing inherited may appear.
	filtered := []string{}
	for _, l := range got {
		if !strings.HasPrefix(l, "PWD=") && !strings.HasPrefix(l, "SHLVL=") && !strings.HasPrefix(l, "_=") && !strings.HasPrefix(l, "OLDPWD=") {
			filtered = append(filtered, l)
		}
	}
	if strings.Join(filtered, "|") != "A=$HOME|B=two words|PATH=/usr/bin:/bin" {
		t.Fatalf("environment is not the exact allowlist: %q", filtered)
	}
}

// The native profile always has the network open (internet, localhost, LAN); a
// local listener started here is reachable from inside the sandbox.
func TestRealSeatbeltNativeProfileNetworkIsOpenToLoopbackListener(t *testing.T) {
	f := newSandboxFixture(t)
	ln, err := net.Listen("tcp", "127.0.0\x2e1:0")
	if err != nil {
		t.Fatal(err)
	}
	defer ln.Close()
	go func() {
		for {
			c, err := ln.Accept()
			if err != nil {
				return
			}
			c.Write([]byte("REACHED\n"))
			c.Close()
		}
	}()
	script := fmt.Sprintf("exec 3<>/dev/tcp/127.0.0\x2e1/%d && read -t 3 -u 3 line && echo $line", ln.Addr().(*net.TCPAddr).Port)
	p := f.policy(map[string]string{}, "-c", script)
	p.Command = "/bin/bash"
	if out, code := f.run(t, p); code != 0 || !strings.Contains(out, "REACHED") {
		t.Fatal("network must be reachable under the native profile", out, code)
	}
}

func TestRealSeatbeltBuildMaySignalOnlyItsOwnSandbox(t *testing.T) {
	f := newSandboxFixture(t)
	victim := exec.Command("/bin/sleep", "30")
	if err := victim.Start(); err != nil {
		t.Fatal(err)
	}
	defer func() { victim.Process.Kill(); victim.Wait() }()
	out, code := f.run(t, f.policy(map[string]string{}, "-c", "sleep 30 & kill $!; echo child-killed"))
	if code != 0 || !strings.Contains(out, "child-killed") {
		t.Fatal("a Build must be able to signal its own children", out)
	}
	_, code = f.run(t, f.policy(map[string]string{}, "-c", fmt.Sprintf("kill -9 %d", victim.Process.Pid)))
	if code == 0 {
		t.Fatal("a Build signalled a process outside its sandbox")
	}
	time.Sleep(50 * time.Millisecond)
	if err := victim.Process.Signal(syscallZero()); err != nil {
		t.Fatal("victim was killed", err)
	}
}

// ~/.kogen is protected entry by entry, not as a whole: a Build whose writable
// root is ~/.kogen/workspaces/<build> can write there and read the rest of
// ~/.kogen, but cannot read, list, write or execute the private entries
// (accounts.yaml, logins/providers, state, engine, approvals, receipts, journal).
func TestRealSeatbeltKogenHomeWorkspaceWritableButPrivateEntriesDenied(t *testing.T) {
	f := newSandboxFixture(t)
	home := filepath.Join(f.root, "home")
	kogen := filepath.Join(home, ".kogen")
	ws := filepath.Join(kogen, "workspaces", "build-1")
	for _, d := range []string{ws, filepath.Join(kogen, "bin")} {
		if err := os.MkdirAll(d, 0o755); err != nil {
			t.Fatal(err)
		}
	}
	private := []string{"state", "engine", "approvals", "receipts", "journal", "logins", "providers/xai/default"}
	for _, d := range private {
		if err := os.MkdirAll(filepath.Join(kogen, d), 0o700); err != nil {
			t.Fatal(err)
		}
		os.WriteFile(filepath.Join(kogen, d, "item"), []byte("PLANTED-SECRET\n"), 0o600)
	}
	os.WriteFile(filepath.Join(kogen, "accounts.yaml"), []byte("PLANTED-SECRET\n"), 0o600)
	os.WriteFile(filepath.Join(kogen, "bin", "kogen"), []byte("public-wrapper\n"), 0o644)
	p := func(argv ...string) Policy {
		pol := f.policy(map[string]string{}, argv...)
		pol.Write, pol.Cwd, pol.Protected = []string{ws}, ws, SecretPaths(home)
		return pol
	}
	if out, code := f.run(t, p("-c", "echo ok > "+ws+"/out.txt && cat "+kogen+"/bin/kogen")); code != 0 || !strings.Contains(out, "public-wrapper") {
		t.Fatal("workspace write and non-private ~/.kogen reads must work", out, code)
	}
	if b, err := os.ReadFile(filepath.Join(ws, "out.txt")); err != nil || strings.TrimSpace(string(b)) != "ok" {
		t.Fatal("workspace write did not land", err)
	}
	for _, d := range private {
		for name, script := range map[string]string{
			"cat":   "cat " + filepath.Join(kogen, d, "item"),
			"ls":    "ls " + filepath.Join(kogen, d),
			"write": "echo x > " + filepath.Join(kogen, d, "evil"),
		} {
			if out, code := f.run(t, p("-c", script)); code == 0 || strings.Contains(out, "PLANTED-SECRET") {
				t.Fatalf("%s %s: private entry reachable: %q", d, name, out)
			}
		}
	}
	if out, code := f.run(t, p("-c", "cat "+filepath.Join(kogen, "accounts.yaml"))); code == 0 || strings.Contains(out, "PLANTED-SECRET") {
		t.Fatal("accounts.yaml readable", out)
	}
	if out, code := f.run(t, p("-c", "echo x > "+filepath.Join(kogen, "accounts.yaml"))); code == 0 {
		t.Fatal("accounts.yaml writable", out)
	}
	// Outside the workspace nothing under ~/.kogen is writable, protected or not.
	if _, code := f.run(t, p("-c", "echo x > "+filepath.Join(kogen, "bin", "evil"))); code == 0 {
		t.Fatal("write outside the workspace root was allowed")
	}
}
