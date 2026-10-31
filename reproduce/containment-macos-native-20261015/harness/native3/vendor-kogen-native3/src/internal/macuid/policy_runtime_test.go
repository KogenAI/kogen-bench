package macuid

import (
	"encoding/json"
	"reflect"
	"regexp"
	"strings"
	"testing"
)

// The only implicit (policy-independent) Seatbelt rules. Any change here is a
// containment-surface change and must update this test deliberately.
const wantImplicitHeader = "(version 1)\n(deny default)\n(deny network*)\n(allow process-fork)\n" +
	"(allow file-read-data (literal \"/\"))\n" +
	"(allow sysctl-read (sysctl-name \"hw.pagesize_compat\" \"kern.ostype\" \"kern.osrelease\" \"kern.version\" \"kern.hostname\" \"hw.machine\"))\n"

func TestSeatbeltDyldAndRuntimeAllowanceIsExactAndMinimal(t *testing.T) {
	p := testPolicy()
	sb, err := CompileSeatbelt(p)
	if err != nil {
		t.Fatal(err)
	}
	if !strings.HasPrefix(sb, wantImplicitHeader) {
		t.Fatalf("implicit header changed:\n%s", sb)
	}
	// dyld root read is the literal inode "/" only: never a subpath, never "/*".
	if !strings.Contains(sb, "(allow file-read-data (literal \"/\"))\n") || strings.Contains(sb, "(subpath \"/\")") {
		t.Fatal("dyld root rule must be literal \"/\" only", sb)
	}
	// Whitelist every emitted rule shape; anything else is a widening.
	allowed := []*regexp.Regexp{
		regexp.MustCompile(`^\(version 1\)$`),
		regexp.MustCompile(`^\(deny default\)$`),
		regexp.MustCompile(`^\(deny network\*\)$`),
		regexp.MustCompile(`^\(allow process-fork\)$`),
		regexp.MustCompile(`^\(allow file-read-data \(literal "/"\)\)$`),
		regexp.MustCompile(`^\(allow sysctl-read \(sysctl-name( "[a-z._]+")+\)\)$`),
		regexp.MustCompile(`^\(allow file-read-metadata \(literal "[^"]+"\)\)$`),
		regexp.MustCompile(`^\(allow file-read\* \(subpath "[^"]+"\)\)$`),
		regexp.MustCompile(`^\(allow process-exec \(subpath "[^"]+"\)\)$`),
		regexp.MustCompile(`^\(allow file-write\* \(subpath "[^"]+"\)\)$`),
		regexp.MustCompile(`^\(deny file-read\* file-write\* process-exec \(subpath "[^"]+"\)\)$`),
	}
	writes := 0
	for _, line := range strings.Split(strings.TrimSuffix(sb, "\n"), "\n") {
		ok := false
		for _, re := range allowed {
			ok = ok || re.MatchString(line)
		}
		if !ok {
			t.Fatalf("unexpected rule shape %q in\n%s", line, sb)
		}
		if strings.HasPrefix(line, "(allow file-write*") {
			writes++
		}
	}
	if writes != len(p.Write) {
		t.Fatalf("write rules %d != declared write roots %d", writes, len(p.Write))
	}
	for _, forbidden := range []string{"allow network", "mach-lookup", "allow signal", "process-info", "file-map-executable", "file-ioctl", "iokit", "system-socket", "ipc-posix", "(regex", "sysctl-write", "user-preference", "/dev", "/tmp", "/usr", "/System", "/Library", "(subpath \"/\")"} {
		if strings.Contains(sb, forbidden) {
			t.Fatalf("widening %q present:\n%s", forbidden, sb)
		}
	}
	// Protected authority is an explicit deny AFTER every allow (last match wins).
	deny := "(deny file-read* file-write* process-exec (subpath \"/controller\"))\n"
	if !strings.HasSuffix(sb, deny) {
		t.Fatal("protected deny must be the final rule", sb)
	}
	// Nothing else may write: file-write* only for the declared write roots.
	if strings.Count(sb, "(allow file-write") != 1 || !strings.Contains(sb, "(allow file-write* (subpath \"/build\"))") {
		t.Fatal("unexpected write authority", sb)
	}
}

func TestSeatbeltAncestorTraversalIsMetadataOnlyLiteralAndDerivedFromDeclaredPaths(t *testing.T) {
	p := Policy{Command: "/opt/tc/elixir/bin/mix", Argv: []string{"--version"}, Cwd: "/work/ws", Read: []string{"/opt/tc/elixir"}, Write: []string{"/work/ws"}}
	sb, err := CompileSeatbelt(p)
	if err != nil {
		t.Fatal(err)
	}
	want := []string{"/", "/opt", "/opt/tc", "/opt/tc/elixir", "/opt/tc/elixir/bin", "/work"}
	var got []string
	for _, line := range strings.Split(sb, "\n") {
		if strings.HasPrefix(line, "(allow file-read-metadata ") {
			got = append(got, strings.TrimSuffix(strings.TrimPrefix(line, "(allow file-read-metadata (literal \""), "\"))"))
		}
	}
	if strings.Join(got, ",") != strings.Join(want, ",") {
		t.Fatalf("ancestors %v want %v\n%s", got, want, sb)
	}
	// Siblings and children of ancestors must not be covered: no subpath rule
	// exists for any ancestor, and metadata rules never name a root's children.
	for _, bad := range []string{"(subpath \"/opt\")", "(subpath \"/opt/tc\")", "(subpath \"/work\")", "(subpath \"/\")"} {
		if strings.Contains(sb, bad) {
			t.Fatalf("ancestor widened to subtree %s", bad)
		}
	}
	if got := ancestors([]string{"/a/b/c", "/a/b/d", "/a"}); strings.Join(got, ",") != "/,/a,/a/b" {
		t.Fatalf("ancestors dedupe/order %v", got)
	}
}

func TestSeatbeltImplicitRulesDoNotAdmitInjectionOrNetwork(t *testing.T) {
	// The implicit rules must not create a route around the existing refusals.
	p := testPolicy()
	p.Read = []string{"/"}
	if _, err := CompileSeatbelt(p); err == nil {
		t.Fatal("root read grant accepted")
	}
	p = testPolicy()
	p.Env["DYLD_FALLBACK_LIBRARY_PATH"] = "/tool"
	if _, err := CompileSeatbelt(p); err == nil {
		t.Fatal("DYLD_ env accepted")
	}
}

func broadPolicy() Policy {
	p := testPolicy()
	p.ReadBroad = true
	p.Read = []string{"/tool"}
	p.Protected = append(SecretPaths("/Users/u"), "/controller")
	return p
}

// v1 native profile: every emitted rule must be one of these shapes, and the
// exact guarantee-bearing rules must be present in the right order.
func TestSeatbeltBroadReadProfileShapeAndOrdering(t *testing.T) {
	p := broadPolicy()
	sb, err := CompileSeatbelt(p)
	if err != nil {
		t.Fatal(err)
	}
	allowed := []*regexp.Regexp{
		regexp.MustCompile(`^\(version 1\)$`), regexp.MustCompile(`^\(deny default\)$`), regexp.MustCompile(`^\(deny network\*\)$`),
		regexp.MustCompile(`^\(allow process-fork\)$`), regexp.MustCompile(`^\(allow file-read-data \(literal "/"\)\)$`),
		regexp.MustCompile(`^\(allow sysctl-read \(sysctl-name( "[a-z._]+")+\)\)$`),
		regexp.MustCompile(`^\(allow file-read\*\)$`), regexp.MustCompile(`^\(allow process-exec\)$`),
		regexp.MustCompile(`^\(allow signal \(target same-sandbox\)\)$`),
		regexp.MustCompile(`^\(allow file-write\* \(subpath "[^"]+"\)\)$`), regexp.MustCompile(`^\(allow network\*\)$`),
		regexp.MustCompile(`^\(deny file-read\* file-write\* process-exec \(subpath "[^"]+"\)\)$`),
	}
	lines := strings.Split(strings.TrimSuffix(sb, "\n"), "\n")
	lastAllow, firstDeny := -1, -1
	for i, line := range lines {
		ok := false
		for _, re := range allowed {
			ok = ok || re.MatchString(line)
		}
		if !ok {
			t.Fatalf("unexpected rule %q", line)
		}
		if strings.HasPrefix(line, "(allow ") {
			lastAllow = i
		}
		if strings.HasPrefix(line, "(deny file-read*") && firstDeny < 0 {
			firstDeny = i
		}
	}
	if firstDeny <= lastAllow {
		t.Fatal("secret deny rules must come after every allow", sb)
	}
	// (1) write authority is exactly the declared write roots.
	if strings.Count(sb, "(allow file-write*") != len(p.Write) || !strings.Contains(sb, "(allow file-write* (subpath \"/build\"))") {
		t.Fatal(sb)
	}
	// (2) each secret location is denied for read, write and exec.
	for _, secret := range p.Protected {
		if !strings.Contains(sb, "(deny file-read* file-write* process-exec (subpath \""+secret+"\"))") {
			t.Fatalf("secret %s not denied", secret)
		}
	}
	for _, want := range []string{"/Volumes/u/.ssh", "/Volumes/u/.gnupg", "/Volumes/u/.aws", "/Volumes/u/.kube", "/Volumes/u/.config/gcloud", "/Volumes/u/.kogen/accounts.yaml", "/Volumes/u/.kogen/providers", "/Volumes/u/.kogen/logins", "/Volumes/u/.kogen/state", "/Volumes/u/.kogen/engine", "/Volumes/u/.kogen/approvals", "/Volumes/u/.kogen/receipts", "/Volumes/u/.kogen/journal", "/Volumes/u/Library/Keychains", "/Library/Keychains", "/Volumes/u/Library/Application Support/Google/Chrome", "/Volumes/u/Library/Application Support/Firefox", "/Volumes/u/Library/Safari"} {
		if !strings.Contains(sb, "(subpath \""+want+"\")") {
			t.Fatalf("secret list lacks %s", want)
		}
	}
	// No other capability class is introduced by broad reads.
	for _, forbidden := range []string{"mach-lookup", "iokit", "sysctl-write", "file-map-executable", "ipc-posix", "process-info", "(allow default)", "(allow file-write*)", "(allow file-write* (subpath \"/\"))"} {
		if strings.Contains(sb, forbidden) {
			t.Fatalf("widening %q", forbidden)
		}
	}
}

// Network is a fixed property of the profile shape, never an input: the v1
// native (ReadBroad) shape is open exactly once, after the default deny; the
// strict shape never allows network; Policy has no network field and the wire
// decoder rejects one.
func TestSeatbeltNetworkIsAFixedInvariantNotAnInput(t *testing.T) {
	sb, err := CompileSeatbelt(broadPolicy())
	if err != nil || strings.Count(sb, "(allow network*)") != 1 || strings.Index(sb, "(deny network*)") > strings.Index(sb, "(allow network*)") {
		t.Fatal("native profile must open the network once, after the default deny", err, sb)
	}
	strict, err := CompileSeatbelt(testPolicy())
	if err != nil || strings.Contains(strict, "(allow network") {
		t.Fatal("strict profile must never allow network", err, strict)
	}
	if _, ok := reflect.TypeOf(Policy{}).FieldByName("Network"); ok {
		t.Fatal("Policy must not carry a network field")
	}
	if wire, _ := json.Marshal(broadPolicy()); strings.Contains(string(wire), "network") {
		t.Fatal("policy wire form must not mention network", string(wire))
	}
	frame, _ := json.Marshal(nativeRequest())
	withNet := strings.Replace(string(frame), `"policy":{`, `"policy":{"network":"deny",`, 1)
	if _, err = decodeLaunch([]byte(withNet)); err == nil {
		t.Fatal("a launch frame carrying a network field must be rejected")
	}
	if _, err = decodeLaunch(frame); err != nil {
		t.Fatal(err)
	}
}

// v1 has no metadata-address (169.254.169\x2e254) deny on macOS (optional post-v1
// hardening; Seatbelt cannot express a per-IP deny), and the profile must not
// pretend to: no IP literal of any kind may appear in a generated profile.
func TestSeatbeltProfileCarriesNoPerIPRule(t *testing.T) {
	sb, _ := CompileSeatbelt(broadPolicy())
	if strings.Contains(sb, "169.254") || strings.Contains(sb, "remote ip") {
		t.Fatal(sb)
	}
}

// ~/.kogen is NOT protected as a whole: only its private entries are, so a
// Build workspace under ~/.kogen/workspaces/<build> is a legal writable root.
func TestKogenHomeProtectsOnlyPrivateEntries(t *testing.T) {
	list := SecretPaths("/Users/u")
	for _, p := range list {
		if p == "/Volumes/u/.kogen" || p == "/Volumes/u/.kogen/workspaces" || strings.HasPrefix(p, "/Volumes/u/.kogen/workspaces/") || p == "/Volumes/u/.kogen/bin" || p == "/Volumes/u/.kogen/releases" {
			t.Fatalf("%s must not be protected", p)
		}
	}
	got := map[string]bool{}
	for _, p := range list {
		got[p] = true
	}
	for _, e := range []string{"accounts.yaml", "logins", "providers", "state", "engine", "approvals", "receipts", "journal"} {
		if !got["/Volumes/u/.kogen/"+e] {
			t.Fatalf("private entry %s is not protected", e)
		}
	}
	p := broadPolicy()
	p.Write, p.Cwd = []string{"/Volumes/u/.kogen/workspaces/b-123"}, "/Volumes/u/.kogen/workspaces/b-123"
	p.Protected = list
	sb, err := CompileSeatbelt(p)
	if err != nil || !strings.Contains(sb, `(allow file-write* (subpath "/Volumes/u/.kogen/workspaces/b-123"))`) {
		t.Fatal("a ~/.kogen/workspaces/<build> writable root must be accepted", err)
	}
	for name, root := range map[string]string{
		"kogen-home":    "/Volumes/u/.kogen",
		"accounts-file": "/Volumes/u/.kogen/accounts.yaml",
		"state":         "/Volumes/u/.kogen/state",
		"state-child":   "/Volumes/u/.kogen/state/b-1",
		"engine":        "/Volumes/u/.kogen/engine/x",
		"approvals":     "/Volumes/u/.kogen/approvals",
		"receipts":      "/Volumes/u/.kogen/receipts/r",
		"journal":       "/Volumes/u/.kogen/journal",
		"logins":        "/Volumes/u/.kogen/logins/x",
		"providers":     "/Volumes/u/.kogen/providers/xai/default",
		"ssh":           "/Volumes/u/.ssh",
	} {
		q := p
		q.Write, q.Cwd = []string{root}, root
		if _, err := CompileSeatbelt(q); err == nil {
			t.Fatalf("writable root %s (%s) overlaps a listed entry and must be refused", name, root)
		}
	}
}

func TestSeatbeltBroadReadStillRefusesUnsafeGrants(t *testing.T) {
	for name, mod := range map[string]func(*Policy){
		"write-root-is-secret":       func(p *Policy) { p.Write = []string{"/Volumes/u/.ssh"}; p.Cwd = "/Volumes/u/.ssh" },
		"write-root-contains-secret": func(p *Policy) { p.Write = []string{"/Users/u"}; p.Cwd = "/Users/u" },
		"write-root-is-slash":        func(p *Policy) { p.Write = []string{"/"}; p.Cwd = "/" },
		"command-in-secret":          func(p *Policy) { p.Command = "/Volumes/u/.aws/run" },
		"no-write-roots":             func(p *Policy) { p.Write = nil },
		"dyld-env":                   func(p *Policy) { p.Env["DYLD_LIBRARY_PATH"] = "/x" },
		"env-names-secret":           func(p *Policy) { p.Env["X"] = "/Volumes/u/.ssh/id_rsa" },
		"protected-slash":            func(p *Policy) { p.Protected = append(p.Protected, "/") },
		"noncanonical-root":          func(p *Policy) { p.Write = []string{"/build/../etc"} },
	} {
		p := broadPolicy()
		mod(&p)
		if _, err := CompileSeatbelt(p); err == nil {
			t.Fatalf("%s accepted", name)
		}
	}
	// A broad READ root that merely contains a secret grants nothing extra and is allowed.
	p := broadPolicy()
	p.Read = []string{"/Users/u"}
	if sb, err := CompileSeatbelt(p); err != nil || !strings.Contains(sb, "(deny file-read* file-write* process-exec (subpath \"/Volumes/u/.ssh\"))") {
		t.Fatal(err)
	}
	// Strict mode (default) is unchanged: no broad read rules.
	q := testPolicy()
	sb, _ := CompileSeatbelt(q)
	if strings.Contains(sb, "(allow file-read*)\n") || strings.Contains(sb, "(allow process-exec)\n") {
		t.Fatal("strict mode must not read broadly")
	}
}
