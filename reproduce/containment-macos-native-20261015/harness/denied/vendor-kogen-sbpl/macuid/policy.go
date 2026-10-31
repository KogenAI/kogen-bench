package macuid

import (
	"fmt"
	"path/filepath"
	"sort"
	"strings"
	"unicode/utf8"
)

type Policy struct {
	Command   string
	Argv      []string
	Cwd       string
	Env       map[string]string
	Read      []string
	Write     []string
	Protected []string
	Network   string
}

type Unsupported struct{ Capability, Clause, Reason string }

func (e *Unsupported) Error() string { return e.Reason }

func pathOK(p string) bool {
	return filepath.IsAbs(p) && filepath.Clean(p) == p && !strings.ContainsAny(p, "\x00\\") && utf8.ValidString(p)
}
func within(p, root string) bool { return root == "/" || p == root || strings.HasPrefix(p, root+"/") }

// CompileSeatbelt emits one default-deny profile. The only implicit grants are the
// literal dyld root-directory read (dyldRootRule), a fixed read-only host-constant
// sysctl set (runtimeSysctlRule) and stat-only ancestor traversal of declared
// paths (ancestors); no other runtime/library,
// device, directory, DNS, loopback, Unix socket, Mach or credential grants exist.
// Lexical paths alone are insufficient for object/race confinement qualification.
func CompileSeatbelt(p Policy) (string, error) {
	if p.Network != "deny" {
		return "", &Unsupported{"network-denial", "CONT-3.2", "destination/DNS/HTTPS mediation is unimplemented"}
	}
	if !pathOK(p.Command) || !pathOK(p.Cwd) || len(p.Read) > 128 || len(p.Write) > 128 || len(p.Read)+len(p.Write) == 0 {
		return "", fmt.Errorf("explicit canonical command, cwd and bounded roots required")
	}
	roots := append(append([]string{}, p.Read...), p.Write...)
	seen := map[string]bool{}
	commandOK, cwdOK := false, false
	for _, root := range roots {
		if !pathOK(root) || seen[root] {
			return "", fmt.Errorf("invalid or duplicate root")
		}
		seen[root] = true
		commandOK = commandOK || within(p.Command, root)
		cwdOK = cwdOK || within(p.Cwd, root)
		for _, protected := range p.Protected {
			if !pathOK(protected) {
				return "", fmt.Errorf("invalid protected root")
			}
			if within(root, protected) || within(protected, root) {
				return "", fmt.Errorf("grant overlaps protected authority")
			}
		}
	}
	if !commandOK || !cwdOK {
		return "", fmt.Errorf("command/cwd outside grants")
	}
	for _, arg := range p.Argv {
		if strings.ContainsRune(arg, 0) || !utf8.ValidString(arg) {
			return "", fmt.Errorf("invalid argv")
		}
	}
	for key, val := range p.Env {
		if key == "" || strings.ContainsAny(key, "=\x00") || strings.ContainsRune(val, 0) || !utf8.ValidString(key+val) {
			return "", fmt.Errorf("invalid literal environment")
		}
		if strings.HasPrefix(key, "DYLD_") || key == "LD_PRELOAD" || key == "LD_AUDIT" || key == "BASH_ENV" || key == "ENV" || strings.HasPrefix(key, "GIT_CONFIG") || key == "GIT_EXEC_PATH" {
			return "", fmt.Errorf("trusted launcher configuration injection is denied")
		}
		for _, protected := range p.Protected {
			if strings.Contains(val, protected) {
				return "", fmt.Errorf("environment references protected authority")
			}
		}
	}
	var sb strings.Builder
	sb.WriteString("(version 1)\n(deny default)\n(deny network*)\n(allow process-fork)\n")
	// dyld loader allowance (implicit grant 1 of 3). Under (deny default) every
	// dynamically linked Mach-O, including /bin/bash, aborts with SIGABRT at
	// startup because dyld opens the root directory (denied: "file-read-data /").
	// Verified on macOS 26.7.1/arm64: with only this rule bash, git, mix/erl and
	// go all start; the dyld shared cache itself is mapped without a path check and
	// needs no file grant. The rule is a SBPL (literal), i.e. the single inode "/":
	// it does not cover any child path, grants no write, no file-map-executable, no
	// process-exec, no sysctl, no mach-lookup and no network. Its only disclosure
	// is the list of top-level directory names of the read-only system volume.
	sb.WriteString(dyldRootRule)
	sb.WriteString(runtimeSysctlRule)
	// Ancestor traversal (implicit grant 3, derived only from declared paths):
	// metadata (stat/lstat) of each proper ancestor directory of every declared
	// root, command and cwd, as (literal ...) so children are not covered.
	// Without it shells canonicalising a toolchain path under $HOME (bash `cd`,
	// `pwd -P`; Elixir's bin/elixir readlink_f) fail with ENOTDIR/EPERM. It
	// reveals only the stat of directories whose names the manifest already
	// states; no read-data (listing), no sibling, no write, no exec.
	for _, a := range ancestors(append([]string{p.Command, p.Cwd}, roots...)) {
		sb.WriteString("(allow file-read-metadata (literal " + sbString(a) + "))\n")
	}
	// All paths are SBPL string literals, not interpolated Scheme expressions.
	for _, root := range roots {
		sb.WriteString("(allow file-read* (subpath " + sbString(root) + "))\n")
		sb.WriteString("(allow process-exec (subpath " + sbString(root) + "))\n")
	}
	for _, root := range p.Write {
		sb.WriteString("(allow file-write* (subpath " + sbString(root) + "))\n")
	}
	// No signal/process-inspection grants are emitted: portable signals are not
	// advertised by this backend. The trusted custodian lives outside Seatbelt.
	return sb.String(), nil
}

// ancestors returns the sorted, de-duplicated proper ancestor directories of the
// given canonical absolute paths, including "/".
func ancestors(paths []string) []string {
	seen := map[string]bool{}
	for _, p := range paths {
		for d := filepath.Dir(p); !seen[d]; d = filepath.Dir(d) {
			seen[d] = true
			if d == "/" {
				break
			}
		}
	}
	out := make([]string, 0, len(seen))
	for d := range seen {
		out = append(out, d)
	}
	sort.Strings(out)
	return out
}

// dyldRootRule is emitted by CompileSeatbelt regardless of the policy.
const dyldRootRule = "(allow file-read-data (literal \"/\"))\n"

// runtimeSysctlRule is the read-only sysctl set that language runtimes need
// before main(), measured on macOS 26.7.1/arm64 (see evidence/seatbelt):
//
//	hw.pagesize_compat  Go's darwin runtime; denied => "fatal error: failed to
//	                    get system page size".
//	kern.ostype, kern.osrelease, kern.version, kern.hostname, hw.machine
//	                    the five sysctls behind uname(3), which fails as a whole
//	                    when any is denied; Erlang/OTP's beam.smp calls uname()
//	                    at start and aborts with "BROKEN KQUEUE!" without it.
//
// They are static host constants (page size, OS name/release/build string, CPU
// architecture, host name). They are not process, user, file or network data and
// there is no sysctl write. kern.hostname discloses this machine's host name.
const runtimeSysctlRule = "(allow sysctl-read (sysctl-name \"hw.pagesize_compat\" \"kern.ostype\" \"kern.osrelease\" \"kern.version\" \"kern.hostname\" \"hw.machine\"))\n"

func sbString(s string) string {
	var b strings.Builder
	b.WriteByte('"')
	for _, r := range s {
		switch r {
		case '"', '\\':
			b.WriteByte('\\')
			b.WriteRune(r)
		case '\n':
			b.WriteString("\\n")
		case '\r':
			b.WriteString("\\r")
		case '\t':
			b.WriteString("\\t")
		default:
			if r < 32 || r == 127 {
				fmt.Fprintf(&b, "\\x%02x;", r)
			} else {
				b.WriteRune(r)
			}
		}
	}
	b.WriteByte('"')
	return b.String()
}

type LaunchSpec struct {
	Path        string
	Args        []string
	Cwd         string
	Env         []string
	UID, GID    uint32
	StdinClosed bool
}

// LaunchPlan has no shell/sudo/su/nono wrapper and exactly one sandbox-exec.
// Execution is available only to explicit operator diagnostic probes; the
// containment package refuses admission while mandatory effects are missing.
func LaunchPlan(p Policy, uid, gid uint32) (LaunchSpec, error) {
	if uid < 501 || gid < 501 {
		return LaunchSpec{}, fmt.Errorf("reserved unprivileged user/group required")
	}
	sb, err := CompileSeatbelt(p)
	if err != nil {
		return LaunchSpec{}, err
	}
	keys := make([]string, 0, len(p.Env))
	for k := range p.Env {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	env := []string{}
	for _, k := range keys {
		env = append(env, k+"="+p.Env[k])
	}
	args := []string{"/usr/bin/sandbox-exec", "-p", sb, p.Command}
	args = append(args, p.Argv...)
	return LaunchSpec{Path: "/usr/bin/sandbox-exec", Args: args, Cwd: p.Cwd, Env: env, UID: uid, GID: gid, StdinClosed: true}, nil
}
