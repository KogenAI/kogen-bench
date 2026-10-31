package macuid

import (
	"fmt"
	"path/filepath"
	"sort"
	"strings"
	"unicode/utf8"
)

// Network is NOT a policy or manifest input. It is a fixed property of the two
// profile shapes: the v1 native read model (ReadBroad) always runs with the
// network open ((allow network*)), and the strict (non-ReadBroad) shape used
// only by diagnostic probes never allows any network. Nothing a caller sends
// can select, widen or narrow it. v1 on macOS has no 169.254.169\x2e254 deny
// (main ruling 11:13Z; optional post-v1 hardening, same as Linux).

// Policy is the only input to CompileSeatbelt; there is no raw profile text.
// ReadBroad selects the v1 native read model: every path is readable (and
// executable) except the Protected deny list, which is emitted after all
// allows. Without ReadBroad, reads are limited to the Read/Write roots.
// Write authority is always exactly the Write roots.
type Policy struct {
	Command   string            `json:"command"`
	Argv      []string          `json:"argv"`
	Cwd       string            `json:"cwd"`
	Env       map[string]string `json:"env"`
	Read      []string          `json:"read"`
	Write     []string          `json:"write"`
	Protected []string          `json:"protected"`
	ReadBroad bool              `json:"read_broad"`
}

type Unsupported struct{ Capability, Clause, Reason string }

func (e *Unsupported) Error() string { return e.Reason }

func pathOK(p string) bool {
	return filepath.IsAbs(p) && filepath.Clean(p) == p && !strings.ContainsAny(p, "\x00\\") && utf8.ValidString(p)
}
func within(p, root string) bool { return root == "/" || p == root || strings.HasPrefix(p, root+"/") }

// CompileSeatbelt emits one default-deny profile. The implicit grants are the
// literal dyld root-directory read (dyldRootRule), a fixed read-only host-constant
// sysctl set (runtimeSysctlRule) and either stat-only ancestor traversal of
// declared paths (strict mode, ancestors) or the v1 broad-read block
// (ReadBroad, broadReadRule: read + exec everywhere, signals within the same
// sandbox only, with the Protected deny list emitted last). Network is open in
// ReadBroad mode (v1 native Builds, fixed invariant) and denied otherwise. No device, directory, Mach, IOKit,
// sysctl-write or credential grants exist in either mode.
// Lexical paths alone are insufficient for object/race confinement qualification.
func CompileSeatbelt(p Policy) (string, error) {
	if !pathOK(p.Command) || !pathOK(p.Cwd) || len(p.Read) > 128 || len(p.Write) > 128 || len(p.Protected) > 256 || len(p.Read)+len(p.Write) == 0 {
		return "", fmt.Errorf("explicit canonical command, cwd and bounded roots required")
	}
	if p.ReadBroad && len(p.Write) == 0 {
		return "", fmt.Errorf("broad-read policy requires explicit write roots")
	}
	for _, protected := range p.Protected {
		if !pathOK(protected) || protected == "/" {
			return "", fmt.Errorf("invalid protected root")
		}
		if within(p.Command, protected) || within(p.Cwd, protected) {
			return "", fmt.Errorf("command or cwd inside protected authority")
		}
	}
	roots := append(append([]string{}, p.Read...), p.Write...)
	seen := map[string]bool{}
	commandOK, cwdOK := false, false
	for i, root := range roots {
		if !pathOK(root) || seen[root] {
			return "", fmt.Errorf("invalid or duplicate root")
		}
		seen[root] = true
		commandOK = commandOK || within(p.Command, root)
		cwdOK = cwdOK || within(p.Cwd, root)
		isWrite := i >= len(p.Read)
		for _, protected := range p.Protected {
			// Under ReadBroad a read root grants nothing extra (every path is
			// readable and the deny list wins), so only write roots must not
			// overlap protected authority.
			if (isWrite || !p.ReadBroad) && (within(root, protected) || within(protected, root)) {
				return "", fmt.Errorf("grant overlaps protected authority")
			}
		}
	}
	if !cwdOK || (!commandOK && !p.ReadBroad) {
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
	if p.ReadBroad {
		// v1 native read model (guarantee 2): everything is readable and
		// executable; the protected deny list below overrides these allows
		// because SBPL evaluates the LAST matching rule. No write, mach-lookup,
		// iokit, ipc or sysctl-write is granted by this block. The signal rule
		// is limited to processes inside this same sandbox (the Build's own
		// tree); without it `kill` of a Build's own child fails EPERM.
		sb.WriteString(broadReadRule)
	} else {
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
	}
	for _, root := range p.Write {
		sb.WriteString("(allow file-write* (subpath " + sbString(root) + "))\n")
	}
	if p.ReadBroad {
		// v1 native Builds: network is open by backend invariant (internet,
		// localhost, LAN, cloud metadata address included in v1). Emitted after
		// (deny network*) so it wins.
		sb.WriteString(networkOpenRule)
	}
	// Protected/secret deny rules come LAST so they win over every allow above.
	// Read, write and exec are all denied; the deny covers the path and its
	// whole subtree. Seatbelt matches resolved vnode paths, so symlink and
	// /System/Volumes/Data firmlink spellings of a protected path are covered.
	for _, protected := range sortedUnique(p.Protected) {
		sb.WriteString("(deny file-read* file-write* process-exec (subpath " + sbString(protected) + "))\n")
	}
	// No other signal/process-inspection grants are emitted. The trusted
	// custodian lives outside Seatbelt.
	return sb.String(), nil
}

func sortedUnique(in []string) []string {
	seen := map[string]bool{}
	out := []string{}
	for _, s := range in {
		if !seen[s] {
			seen[s] = true
			out = append(out, s)
		}
	}
	sort.Strings(out)
	return out
}

const broadReadRule = "(allow file-read*)\n(allow process-exec)\n(allow signal (target same-sandbox))\n"
const networkOpenRule = "(allow network*)\n"

// KogenPrivateEntries are the ONLY entries of ~/.kogen the fixed list protects
// (ruling 10:32Z/10:33Z, architect CONTAINMENT-V1-1015.md section 6). ~/.kogen as
// a whole is NOT protected: ~/.kogen/workspaces/<build> must stay a legal
// writable root, and reads elsewhere under ~/.kogen (bin, releases, ...) are
// ordinary global reads. Names, from the product tree
// ~/Scratch.noindex/replay-mac/kogen-v1/core-e/lib (kogen_home() = $KOGEN_HOME or ~/.kogen):
//
//	accounts.yaml                      provider/protocol/provider.ex:3084 accounts_path
//	providers/<provider>/<label>/      provider.ex:3085 provider_home, credentials.json (provider/supergrok/store.ex:5): the logins
//	provider-tests.jsonl               provider.ex:2199 private provider-test ledger
//	logins, credentials                login stores of other product layouts (credentials/ exists in the installed ~/.kogen)
//	state, engine, approvals, receipts, journal(s)
//	                                   the Engine/controller private state named by the ruling; the product keeps these
//	                                   per project under <root>/.kogen/local (build.ex:942 private_root, receipt_ledger.ex:158,
//	                                   status_report.ex "journal"), so they are listed here only as reserved home names
//
// Nonexistent entries deny nothing; they reserve the name so a later product
// version cannot create a readable secret there.
var KogenPrivateEntries = []string{
	"accounts.yaml", "accounts", "logins", "providers", "credentials", "provider-tests.jsonl",
	"state", "engine", "approvals", "receipts", "journal", "journals",
}

// SecretPaths is the fixed v1 secret-location deny list for one user's home
// directory: credentials, key material, keychains, browser profiles and the
// private entries of the Kogen home (KogenPrivateEntries). Callers add canonical
// (symlink-resolved) spellings.
func SecretPaths(home string) []string {
	rel := []string{
		".ssh", ".gnupg", ".aws", ".kube", ".config/gcloud",
		"Library/Keychains",
		"Library/Application Support/Google/Chrome", "Library/Application Support/Chromium",
		"Library/Application Support/Firefox", "Library/Application Support/BraveSoftware",
		"Library/Application Support/Microsoft Edge", "Library/Application Support/Arc",
		"Library/Safari", "Library/Cookies", "Library/Containers/com.apple.Safari",
		".netrc", ".config/gh", ".docker", ".password-store",
	}
	for _, e := range KogenPrivateEntries {
		rel = append(rel, filepath.Join(".kogen", e))
	}
	out := []string{"/Library/Keychains"}
	for _, r := range rel {
		out = append(out, filepath.Join(home, r))
	}
	return out
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
// It is the only place a profile becomes a launch: the root custodian calls it
// for v1 native Builds (launch.go) and operator probes call it directly. The
// env is exactly Policy.Env; fd 0 is closed.
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
