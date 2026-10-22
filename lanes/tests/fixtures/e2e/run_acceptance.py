import json, subprocess, sys
report, feature = sys.argv[1], sys.argv[2]
text = open(feature).read().splitlines()
scen = [(i + 1, l.split(":", 1)[1].strip()) for i, l in enumerate(text) if l.strip().startswith("Scenario:")]
p = subprocess.run(["go", "test", "-json", "-count=1", "./features/steps/"], capture_output=True, text=True)
order, res = [], {}
for line in p.stdout.splitlines():
    try:
        e = json.loads(line)
    except ValueError:
        continue
    if e.get("Test"):
        if e["Test"] not in order:
            order.append(e["Test"])
        if e["Action"] in ("pass", "fail"):
            res[e["Test"]] = e["Action"]
msgs = [{"gherkinDocument": {"feature": {"children": [
    {"scenario": {"id": "s%d" % n, "location": {"line": ln}}} for n, (ln, _) in enumerate(scen)]}}}]
failed = False
for n, (ln, name) in enumerate(scen):
    status = {"pass": "PASSED", "fail": "FAILED"}.get(res.get(order[n]) if n < len(order) else None, "UNDEFINED")
    failed |= status != "PASSED"
    msgs += [{"pickle": {"id": "p%d" % n, "uri": feature, "name": name, "astNodeIds": ["s%d" % n]}},
             {"testCase": {"id": "c%d" % n, "pickleId": "p%d" % n, "testSteps": [{"id": "t%d" % n}]}},
             {"testCaseStarted": {"id": "st%d" % n, "testCaseId": "c%d" % n}},
             {"testStepFinished": {"testCaseStartedId": "st%d" % n, "testStepId": "t%d" % n,
                                   "testStepResult": {"status": status}}},
             {"testCaseFinished": {"testCaseStartedId": "st%d" % n, "willBeRetried": False}}]
open(report, "w").write("".join(json.dumps(m) + "\n" for m in msgs))
sys.exit(1 if failed else 0)
