//go:build darwin && seatbeltmatrix

package macuid

// Operator-only evidence matrix (build tag seatbeltmatrix; never part of the
// default build). It calls the real CompileSeatbelt/LaunchPlan generator with a
// realistic Kogen Build policy and runs the resulting /usr/bin/sandbox-exec
// launch plan as the CURRENT user (no uid drop, no sudo). Output goes to
// $KOGEN_SB_EVIDENCE/<label>/.

import (
	"bytes"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"syscall"
	"testing"
	"time"
)

type mcase struct {
	name    string
	cwd     string
	command string
	argv    []string
	read    []string
	write   []string
	env     map[string]string
	expect  string // "pass" or "deny"
	post    func(t *testing.T, ws string) string
}

func sh(t *testing.T, dir string, name string, args ...string) string {
	t.Helper()
	c := exec.Command(name, args...)
	c.Dir = dir
	// Hermetic repo creation: ignore the operator's global git config/templates/hooks.
	c.Env = []string{"PATH=/usr/bin:/bin", "HOME=/var/empty", "GIT_CONFIG_GLOBAL=/dev/null", "GIT_CONFIG_SYSTEM=/dev/null"}
	out, err := c.CombinedOutput()
	if err != nil {
		t.Fatalf("%s %v: %v\n%s", name, args, err, out)
	}
	return strings.TrimSpace(string(out))
}

func TestSeatbeltMatrix(t *testing.T) {
	home, _ := os.UserHomeDir()
	label := os.Getenv("KOGEN_SB_LABEL")
	evroot := os.Getenv("KOGEN_SB_EVIDENCE")
	if label == "" || evroot == "" {
		t.Skip("KOGEN_SB_LABEL and KOGEN_SB_EVIDENCE required")
	}
	ev := filepath.Join(evroot, label)
	os.MkdirAll(ev, 0o755)
	start := time.Now().Add(-2 * time.Second)

	// Fresh temp git repo = writable workspace root. Created outside the sandbox.
	top, err := os.MkdirTemp("/private/tmp", "kogen-sb-")
	if err != nil {
		t.Fatal(err)
	}
	ws := filepath.Join(top, "ws")
	os.Mkdir(ws, 0o755)
	sh(t, ws, "/usr/bin/git", "-c", "init.templateDir=", "init", "-q", "-b", "main", ".")
	os.WriteFile(filepath.Join(ws, "a.txt"), []byte("hello\n"), 0o644)
	os.WriteFile(filepath.Join(ws, "hello.go"), []byte("package main\nimport \"fmt\"\nfunc main(){fmt.Println(\"hello\")}\n"), 0o644)
	os.WriteFile(filepath.Join(ws, "go.mod"), []byte("module hello\n\ngo 1.25\n"), 0o644)
	// Planted secret and outside-write target, both outside every grant.
	secretDir := filepath.Join(top, "fakessh")
	os.Mkdir(secretDir, 0o700)
	secret := filepath.Join(secretDir, "id_fake")
	os.WriteFile(secret, []byte("PLANTED-SECRET\n"), 0o600)
	outside := filepath.Join(top, "outside-target")
	// Local TCP listener started by this test and closed by it.
	ln, err := net.Listen("tcp", "127.0.0\x2e1:0")
	if err != nil {
		t.Fatal(err)
	}
	defer ln.Close()
	defer os.RemoveAll(top)
	go func() {
		for {
			c, err := ln.Accept()
			if err != nil {
				return
			}
			c.Write([]byte("HTTP/1.0 200 OK\r\n\r\nLISTENER-REACHED\n"))
			c.Close()
		}
	}()
	port := ln.Addr().(*net.TCPAddr).Port
	// Victim process (started by us, outside the sandbox) for the signal test.
	victim := exec.Command("/bin/sleep", "3000")
	if err := victim.Start(); err != nil {
		t.Fatal(err)
	}
	defer func() { victim.Process.Kill(); victim.Wait() }()

	mise := filepath.Join(home, ".local/share/mise/installs")
	ex := mise + "/elixir/1.20.4-otp-29"
	er := mise + "/erlang/29.1.1"
	gor := mise + "/go/1.27.1"
	clt := "/Library/Developer/CommandLineTools"
	// Manifest-declared tool grants (read+exec). Toolchains come only from here.
	bashG := []string{"/bin/bash", "/bin/sh"}
	gitG := []string{"/usr/bin/git", clt}
	elixirG := []string{ex, er, "/usr/bin/env", "/bin/sh", "/bin/bash", "/bin/cat", "/bin/ls", "/usr/bin/uname", "/usr/bin/dirname", "/usr/bin/basename", "/bin/rm", "/bin/mkdir", "/bin/echo", "/usr/bin/sed", "/usr/bin/tr", "/usr/bin/grep", "/bin/expr", "/usr/bin/id", "/usr/bin/readlink", "/bin/ps"}
	goG := []string{gor, "/usr/bin/env", clt}
	// Manifest-declared system-object grants (not generator rules): /dev/null is
	// opened by bash redirections, git/xcrun, erl and go; /private/var/select/sh is
	// read by /bin/sh to pick its personality; /dev/urandom seeds the BEAM.
	devNull := "/dev/null"
	selSh := "/private/var/select"
	urandom := "/dev/urandom"
	bashG = append(bashG, selSh)
	gitG = append(gitG, "/System/Library/CoreServices/SystemVersion.plist", "/etc/gitconfig", "/private/etc/gitconfig", selSh, "/bin/sh", "/bin/bash")
	elixirG = append(elixirG, selSh, urandom)
	wsW := []string{ws, devNull}
	baseEnv := func(m map[string]string) map[string]string {
		e := map[string]string{"HOME": ws + "/.home", "TMPDIR": ws + "/.tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
		for k, v := range m {
			e[k] = v
		}
		return e
	}
	os.MkdirAll(ws+"/.home", 0o755)
	os.MkdirAll(ws+"/.tmp", 0o755)
	gitEnv := map[string]string{"DEVELOPER_DIR": clt, "TMPDIR": ws + "/.tmp"}
	gitID := []string{"-c", "user.name=Kogen", "-c", "user.email=addr-withheld"}
	cases := []mcase{
		{name: "bash-echo", command: "/bin/bash", argv: []string{"-c", "echo ok"}, read: bashG, write: wsW, env: baseEnv(nil), expect: "pass"},
		{name: "git-status", command: "/usr/bin/git", argv: []string{"-C", ws, "status"}, read: gitG, write: wsW, env: baseEnv(gitEnv), expect: "pass"},
		{name: "git-commit", command: "/usr/bin/git", argv: append(append([]string{"-C", ws}, gitID...), "commit", "-q", "--no-gpg-sign", "-m", "x", "--allow-empty"), read: gitG, write: wsW, env: baseEnv(gitEnv), expect: "pass"},
		{name: "git-add-commit-file", command: "/bin/bash", argv: []string{"-c", "cd " + ws + " && /usr/bin/git add a.txt && /usr/bin/git " + strings.Join(gitID, " ") + " commit -q --no-gpg-sign -m file"}, read: append(append([]string{}, bashG...), gitG...), write: wsW, env: baseEnv(gitEnv), expect: "pass"},
		{name: "mix-version", command: ex + "/bin/mix", argv: []string{"--version"}, read: elixirG, write: wsW, env: baseEnv(map[string]string{"PATH": ex + "/bin:" + er + "/bin:/usr/bin:/bin", "MIX_HOME": ws + "/.mix", "HEX_HOME": ws + "/.hex", "HEX_OFFLINE": "1", "MIX_OS_CONCURRENCY_LOCK": "0"}), expect: "pass"},
		{name: "mix-new", command: ex + "/bin/mix", argv: []string{"new", "demo", "--sup"}, read: elixirG, write: wsW, env: baseEnv(map[string]string{"PATH": ex + "/bin:" + er + "/bin:/usr/bin:/bin", "MIX_HOME": ws + "/.mix", "HEX_HOME": ws + "/.hex", "HEX_OFFLINE": "1", "MIX_OS_CONCURRENCY_LOCK": "0"}), expect: "pass"},
		{name: "mix-compile", command: ex + "/bin/mix", argv: []string{"compile"}, cwd: ws + "/demo", read: elixirG, write: wsW, env: baseEnv(map[string]string{"PATH": ex + "/bin:" + er + "/bin:/usr/bin:/bin", "MIX_HOME": ws + "/.mix", "HEX_HOME": ws + "/.hex", "HEX_OFFLINE": "1", "MIX_OS_CONCURRENCY_LOCK": "0"}), expect: "pass"},
		{name: "go-version", command: gor + "/bin/go", argv: []string{"version"}, read: goG, write: wsW, env: baseEnv(map[string]string{"GOROOT": gor, "GOCACHE": ws + "/.gocache", "GOPATH": ws + "/.gopath", "GOFLAGS": "-mod=mod", "GOTOOLCHAIN": "local", "GOPROXY": "off", "CGO_ENABLED": "0", "PATH": gor + "/bin:/usr/bin:/bin"}), expect: "pass"},
		{name: "go-build", command: gor + "/bin/go", argv: []string{"build", "-o", ws + "/hello.bin", "."}, read: goG, write: wsW, env: baseEnv(map[string]string{"GOROOT": gor, "GOCACHE": ws + "/.gocache", "GOPATH": ws + "/.gopath", "GOTOOLCHAIN": "local", "GOPROXY": "off", "CGO_ENABLED": "0", "PATH": gor + "/bin:/usr/bin:/bin"}), expect: "pass"},
		{name: "run-built-hello", command: ws + "/hello.bin", read: nil, write: wsW, env: baseEnv(nil), expect: "pass"},
		// Negative controls: each must be denied.
		{name: "NEG-write-outside-ws", command: "/bin/bash", argv: []string{"-c", "echo pwn > " + outside}, read: bashG, write: wsW, env: baseEnv(nil), expect: "deny", post: func(t *testing.T, _ string) string {
			if _, err := os.Stat(outside); err == nil {
				return "FILE EXISTS (ESCAPE)"
			}
			return "file absent"
		}},
		{name: "NEG-read-planted-secret", command: "/bin/bash", argv: []string{"-c", "/bin/cat " + secret}, read: append(append([]string{}, bashG...), "/bin/cat"), write: wsW, env: baseEnv(nil), expect: "deny"},
		{name: "NEG-stat-ungranted-home-sibling", command: "/bin/bash", argv: []string{"-c", "/usr/bin/stat " + home + "/Library"}, read: append(append([]string{}, bashG...), "/usr/bin/stat"), write: wsW, env: baseEnv(nil), expect: "deny"},
		{name: "NEG-list-home", command: "/bin/bash", argv: []string{"-c", "/bin/ls " + home}, read: append(append([]string{}, bashG...), "/bin/ls"), write: wsW, env: baseEnv(nil), expect: "deny"},
		{name: "NEG-write-to-ancestor-tmp", command: "/bin/bash", argv: []string{"-c", "echo x > /private/tmp/kogen-sb-ancestor-probe"}, read: bashG, write: wsW, env: baseEnv(nil), expect: "deny", post: func(t *testing.T, _ string) string {
			if _, err := os.Stat("/private/tmp/kogen-sb-ancestor-probe"); err == nil {
				os.Remove("/private/tmp/kogen-sb-ancestor-probe")
				return "FILE EXISTS (ESCAPE)"
			}
			return "file absent"
		}},
		{name: "NEG-exec-ungranted-binary", command: "/bin/bash", argv: []string{"-c", "/usr/bin/id"}, read: bashG, write: wsW, env: baseEnv(nil), expect: "deny"},
		{name: "NEG-network-devtcp", command: "/bin/bash", argv: []string{"-c", fmt.Sprintf("exec 3<>/dev/tcp/127.0.0\x2e1/%d && echo CONNECTED", port)}, read: bashG, write: wsW, env: baseEnv(nil), expect: "deny"},
		{name: "NEG-network-connect", command: "/usr/bin/curl", argv: []string{"-sS", "--max-time", "5", fmt.Sprintf("http://127.0.0\x2e1:%d/", port)}, read: []string{"/usr/bin/curl"}, write: wsW, env: baseEnv(nil), expect: "deny"},
		{name: "NEG-signal-outside-process", command: "/bin/bash", argv: []string{"-c", fmt.Sprintf("/bin/kill -TERM %d", victim.Process.Pid)}, read: append(append([]string{}, bashG...), "/bin/kill"), write: wsW, env: baseEnv(nil), expect: "deny", post: func(t *testing.T, _ string) string {
			out, _ := exec.Command("/bin/ps", "-o", "stat=", "-p", fmt.Sprint(victim.Process.Pid)).Output()
			if st := strings.TrimSpace(string(out)); st == "" || strings.HasPrefix(st, "Z") {
				return "VICTIM DEAD stat=" + st + " (ESCAPE)"
			}
			return "victim alive (ps stat " + strings.TrimSpace(string(out)) + ")"
		}},
	}

	var summary bytes.Buffer
	fmt.Fprintf(&summary, "label=%s ws=%s port=%d\n", label, ws, port)
	only := os.Getenv("KOGEN_SB_ONLY")
	for _, c := range cases {
		if only != "" && !strings.Contains(only+",", c.name+",") {
			continue
		}
		caseStart := time.Now().Add(-time.Second)
		cwd := c.cwd
		if cwd == "" {
			cwd = ws
		}
		if _, err := os.Stat(cwd); err != nil {
			fmt.Fprintf(&summary, "%-28s SKIPPED (cwd %s missing; earlier step failed)\n", c.name, cwd)
			continue
		}
		rd := map[string]bool{}
		for _, w := range c.write {
			rd[w] = true
		}
		var reads []string
		for _, r := range c.read {
			if !rd[r] {
				rd[r] = true
				reads = append(reads, r)
			}
		}
		p := Policy{Command: c.command, Argv: c.argv, Cwd: cwd, Env: c.env, Read: reads, Write: c.write}
		spec, err := LaunchPlan(p, 501, 501)
		if err != nil {
			fmt.Fprintf(&summary, "%-28s PROFILE-ERROR %v\n", c.name, err)
			continue
		}
		os.WriteFile(filepath.Join(ev, c.name+".sb"), []byte(spec.Args[2]), 0o644)
		cmd := exec.Command(spec.Path, spec.Args[1:]...)
		cmd.Args = spec.Args
		cmd.Dir = spec.Cwd
		cmd.Env = spec.Env
		var so, se bytes.Buffer
		cmd.Stdout, cmd.Stderr = &so, &se
		done := make(chan error, 1)
		if err := cmd.Start(); err != nil {
			t.Fatal(err)
		}
		go func() { done <- cmd.Wait() }()
		var werr error
		select {
		case werr = <-done:
		case <-time.After(40 * time.Second):
			cmd.Process.Kill()
			werr = <-done
		}
		code := 0
		if cmd.ProcessState != nil {
			code = cmd.ProcessState.ExitCode()
		}
		_ = werr
		sigs := ""
		if cmd.ProcessState != nil {
			if ws, ok := cmd.ProcessState.Sys().(syscall.WaitStatus); ok && ws.Signaled() {
				sigs = " signal=" + ws.Signal().String()
			}
		}
		extra := ""
		if c.post != nil {
			extra = c.post(t, ws)
		}
		time.Sleep(1200 * time.Millisecond)
		dl, _ := exec.Command("/usr/bin/log", "show", "--start", caseStart.Format("2006-01-02 15:04:05"), "--predicate", `sender == "Sandbox" AND eventMessage CONTAINS "deny"`, "--style", "compact").Output()
		seen := map[string]int{}
		for _, ln := range strings.Split(string(dl), "\n") {
			i := strings.Index(ln, "Sandbox: ")
			if i < 0 {
				continue
			}
			ln = ln[i+9:]
			if j := strings.Index(ln, "("); j >= 0 {
				if k := strings.Index(ln[j:], ")"); k >= 0 {
					ln = ln[:j] + ln[j+k+1:]
				}
			}
			if strings.Contains(ln, "deny") && !strings.Contains(ln, "sharingd") && !strings.Contains(ln, "duetexpertd") && !strings.Contains(ln, "biomesyncd") && !strings.Contains(ln, "usbmuxd") && !strings.Contains(ln, "nsattributed") {
				seen[ln]++
			}
		}
		var dn []string
		for k, v := range seen {
			dn = append(dn, fmt.Sprintf("%6d %s", v, k))
		}
		sort.Slice(dn, func(a, b int) bool { return dn[a] > dn[b] })
		os.WriteFile(filepath.Join(ev, c.name+".denials"), []byte(strings.Join(dn, "\n")+"\n"), 0o644)
		os.WriteFile(filepath.Join(ev, c.name+".stdout"), so.Bytes(), 0o644)
		os.WriteFile(filepath.Join(ev, c.name+".stderr"), se.Bytes(), 0o644)
		first := func(b []byte) string {
			s := strings.TrimSpace(string(b))
			if i := strings.IndexByte(s, '\n'); i >= 0 {
				s = s[:i]
			}
			if len(s) > 110 {
				s = s[:110]
			}
			return s
		}
		verdict := "OK"
		if (c.expect == "pass") != (code == 0) {
			verdict = "UNEXPECTED"
		}
		fmt.Fprintf(&summary, "%-28s expect=%-4s exit=%-3d%s %-10s %s | stdout=%q stderr=%q\n", c.name, c.expect, code, sigs, verdict, extra, first(so.Bytes()), first(se.Bytes()))
	}
	// Unsandboxed positive controls: the same negative commands succeed without the profile.
	for _, ctl := range []string{fmt.Sprintf("exec 3<>/dev/tcp/127.0.0\x2e1/%d && echo CONNECTED", port), fmt.Sprintf("kill -0 %d && echo SIGNAL-DELIVERABLE", victim.Process.Pid), "cat " + secret, "echo x > " + outside + ".ctl && echo WRITE-OK"} {
		co, cerr := exec.Command("/bin/bash", "-c", ctl).CombinedOutput()
		fmt.Fprintf(&summary, "CONTROL(unsandboxed) %-60.60s -> err=%v out=%q\n", ctl, cerr, strings.TrimSpace(string(co)))
	}
	os.Remove(outside + ".ctl")
	// Outside-the-sandbox verification of side effects.
	vlog, _ := exec.Command("/usr/bin/git", "-C", ws, "-c", "core.hooksPath=/dev/null", "log", "--oneline").CombinedOutput()
	fmt.Fprintf(&summary, "VERIFY git log in ws: %q\n", strings.TrimSpace(string(vlog)))
	for _, f := range []string{"hello.bin", "demo/mix.exs", "demo/_build", ".gocache"} {
		_, serr := os.Stat(filepath.Join(ws, f))
		fmt.Fprintf(&summary, "VERIFY exists %s: %v\n", f, serr == nil)
	}
	_, serr := os.Stat(outside)
	fmt.Fprintf(&summary, "VERIFY outside-target exists: %v\n", serr == nil)
	os.WriteFile(filepath.Join(ev, "SUMMARY.txt"), summary.Bytes(), 0o644)
	// Sandbox denials from unified log (best effort).
	lg := exec.Command("/usr/bin/log", "show", "--start", start.Format("2006-01-02 15:04:05"), "--predicate", `sender == "Sandbox"`, "--style", "compact")
	lo, lerr := lg.CombinedOutput()
	os.WriteFile(filepath.Join(ev, "sandbox-log.txt"), append([]byte(fmt.Sprintf("log show err=%v\n", lerr)), lo...), 0o644)
	t.Log("\n" + summary.String())
}
