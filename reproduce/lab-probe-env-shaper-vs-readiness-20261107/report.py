# Recompute the 2x2 table from data/*.txt. usage: python3 -I report.py data
import sys, os, re
d = sys.argv[1]
rows = {}
for m in ("a", "b", "a-noci", "b-ci"):
    t = open(os.path.join(d, m + ".txt")).read()
    names = re.search(r"env names:\n(.*)\n", t).group(1).split()
    out = t.split("probe command output:\n")[1].strip()
    vers = tuple(re.findall(r"^\s+\* (\S+) \((.*)\)$", t, re.M)) + (("ruby", re.search(r"^ruby: ruby (\S+)", t, re.M).group(1)),)
    rows[m] = (names, out, vers)
print("mode\tCI_PROGRESS_BAR\tcounting word\tvariable names\tversions")
for m, (names, out, vers) in rows.items():
    word = "runs" if re.match(r"\d+ runs,", out) else "tests" if re.match(r"\d+ tests,", out) else "other"
    print("%s\t%s\t%s\t%s\t%s" % (m, "CI_PROGRESS_BAR" in names, word, " ".join(n for n in names if n not in ("_", "PWD", "SHLVL")), "; ".join("%s %s" % v for v in vers)))
same = len({r[2] for r in rows.values()}) == 1
print("versions identical in all four runs:", same)
a, b = rows["a"], rows["b"]
print("a and b differ in counting word:", a[1] != b[1])
print("variables only in a:", sorted(set(a[0]) - set(b[0]) - {"_", "PWD", "SHLVL"}))
print("variables only in b:", sorted(set(b[0]) - set(a[0]) - {"_", "PWD", "SHLVL"}))
