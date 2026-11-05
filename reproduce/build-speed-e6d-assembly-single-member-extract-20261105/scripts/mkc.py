"""Arm C = arm B + assembly_test.go extracts only the bin/kogen member it inspects. Usage: mkc.py <assembly_test.go>"""
import sys
p = sys.argv[1]; t = open(p).read()
old = '''	if out, err := exec.Command("tar", "-xzf", archive, "-C", dir).CombinedOutput(); err != nil {
		t.Fatalf("extract: %v\\n%s", err, out)
	}
'''
assert old in t
new = '''	// ARM C (Lab E6): this test inspects one executable; extract that member, not the whole archive.
	listing, err := exec.Command("tar", "-tzf", archive).Output()
	if err != nil {
		t.Fatalf("list: %v", err)
	}
	member := ""
	for _, name := range strings.Split(string(listing), "\\n") {
		if strings.HasSuffix(name, "/bin/kogen") && strings.Count(name, "/") == 2 {
			member = name
			break
		}
	}
	if member == "" {
		t.Fatalf("no bin/kogen in %s", archive)
	}
	if out, err := exec.Command("tar", "-xzf", archive, "-C", dir, member).CombinedOutput(); err != nil {
		t.Fatalf("extract: %v\\n%s", err, out)
	}
'''
t = t.replace(old, new)
t = t.replace('\t"path/filepath"\n', '\t"path/filepath"\n\t"strings"\n', 1)
open(p, 'w').write(t)
