import sys, os, subprocess, tempfile, json
sys.path.insert(0, ".")
import lanes_bare as lb
tmp = tempfile.mkdtemp(prefix="probe-")
tok = lb.read_token(os.environ["KOGEN_HOME"])
cfg = os.path.join(tmp, "cfg"); os.makedirs(cfg)
env = lb.agent_env({}, tmp, {"CLAUDE_CONFIG_DIR": cfg, "CLAUDE_CODE_OAUTH_TOKEN": tok, "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_TELEMETRY": "1"})
a = type("A", (), {"model": "claude-sonnet-5-5", "effort": "medium"})()
cmd = lb.claude_command(a, os.path.expanduser("~/.local/bin/claude"))
r = subprocess.run(cmd, input="Reply with the single word OK. Use no tools.", capture_output=True, text=True, env=env, cwd=tmp, timeout=300)
print("rc", r.returncode)
print(r.stderr[:500].replace(tok, "<tok>"))
for line in r.stdout.splitlines():
    e = json.loads(line); print(e.get("type"), e.get("subtype"), str(e.get("result", ""))[:100], e.get("total_cost_usd"), json.dumps(e.get("usage"))[:300] if e.get("type")=="result" else "")
