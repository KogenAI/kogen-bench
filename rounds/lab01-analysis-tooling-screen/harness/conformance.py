#!/usr/bin/env python3
"""Static stack checks plus evidence that run.sh invoked the required tool."""
import json
import os
from pathlib import Path
import re
import shlex
import sys


def libraries(workspace, arm):
    root = Path(workspace)
    if arm == "PY":
        path = root / "uv.lock"
        project_path = root / "pyproject.toml"
        if not path.is_file() or not project_path.is_file():
            return []
        try:
            import tomllib
            lock = tomllib.loads(path.read_text())
            project = tomllib.loads(project_path.read_text())
            root_package = project.get("project", {}).get("name", "").lower()
            return sorted({item["name"] for item in lock.get("package", [])
                           if item.get("name", "").lower() != root_package})
        except (ImportError, ValueError):
            match = re.search(r"(?ms)^name\s*=\s*['\"]([^'\"]+)['\"].*?^\[\[package\]\](.*)", path.read_text())
            root_name = match.group(1).lower() if match else ""
            return sorted(set(name for name in re.findall(r'(?m)^name\s*=\s*"([^"]+)"', path.read_text())
                              if name.lower() != root_name))
    if arm == "EX":
        for manifest in (root / "mix.exs", *root.glob("*.exs")):
            if not manifest.is_file():
                continue
            text = manifest.read_text(errors="replace")
            found = re.findall(r"\{\s*:([a-zA-Z0-9_]+)\s*,", text)
            if found:
                return sorted(set(found))
        return []
    if arm == "GO":
        path = root / "go.mod"
        if not path.is_file():
            return []
        text = path.read_text()
        deps = []
        block = re.search(r"(?ms)^require\s*\((.*?)^\)", text)
        if block:
            deps.extend(line.split()[0] for line in block.group(1).splitlines()
                        if line.strip() and not line.lstrip().startswith("//"))
        else:
            deps.extend(line.split()[1] for line in text.splitlines()
                        if line.startswith("require ") and len(line.split()) >= 2)
        return sorted(deps)
    return []


def run_script_check(text, arm):
    """Allow setup/build/invocation commands; reject shell-side analysis or output writes."""
    allowed = {"set", "cd", "export", "exec", "env", "mkdir", "rm", "uv", "mix", "elixir", "go"}
    forbidden_tools = {"awk", "jq", "tee", "sed", "perl", "ruby", "rscript", "php"}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # Shell redirections can create or transform outputs outside the arm program.
        if re.search(r"(?<![0-9])(?:>|>>)|\btee\b", line):
            return False, "run.sh contains output redirection or tee"
        try:
            words = shlex.split(line, comments=True, posix=True)
        except ValueError:
            return False, "run.sh has an unparseable command"
        # Handle common compound commands while checking their command heads.
        segments = re.split(r"&&|\|\||[;|]", line)
        for segment in segments:
            try:
                tokens = shlex.split(segment, comments=True, posix=True)
            except ValueError:
                return False, "run.sh has an unparseable command"
            if not tokens:
                continue
            head = tokens[0]
            if head.startswith("#") or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head):
                continue
            if head not in allowed:
                return False, f"run.sh command is outside install/build/invoke scope: {head}"
            command_words = {Path(token).name.lower() for token in tokens[1:]}
            if command_words & forbidden_tools:
                return False, "run.sh invokes a shell-side analysis or output tool"
            python_words = {word for word in command_words if re.fullmatch(r"python(?:3(?:\.\d+)?)?", word)}
            if python_words and not (arm == "PY" and "uv" in command_words and "run" in command_words):
                return False, "run.sh invokes Python outside the arm program"
            if head in {"mkdir", "rm"}:
                # These are permitted only for creating/removing the output directory itself.
                operands = [x for x in tokens[1:] if not x.startswith("-")]
                if not operands or any(x not in {"out", "out/"} for x in operands):
                    return False, f"run.sh {head} may only prepare out/"
    return True, ""


def _ex_has_dependencies(text):
    # Mix projects commonly put dependency tuples in a private deps/0 function.
    return bool(re.search(r"\{\s*:[a-zA-Z0-9_]+\s*,", text))


def _go_has_require(text):
    return bool(re.search(r"(?m)^\s*require\s+(?:\(|\S+\s+\S+)", text))


def check(workspace, arm, evidence=None):
    root = Path(workspace)
    arm = arm.upper()
    if arm not in {"PY", "EX", "GO"}:
        raise ValueError("ARM must be PY, EX or GO")
    reasons = []
    run_path = root / "run.sh"
    run_text = run_path.read_text(errors="replace") if run_path.is_file() else ""
    if not run_path.is_file():
        reasons.append("run.sh missing")
    elif not os.access(run_path, os.X_OK):
        reasons.append("run.sh is not executable")
    source_exts = {"PY": {".py"}, "EX": {".ex", ".exs"}, "GO": {".go"}}
    foreign_exts = set().union(*(v for k, v in source_exts.items() if k != arm))
    generated_dirs = {".git", "out", ".venv", "deps", "_build", "vendor", "node_modules",
                      "target", ".cache", ".mix", ".elixir_ls"}
    candidates = [p for p in root.rglob("*") if p.is_file() and not (generated_dirs & set(p.parts))]
    code_files = [p for p in candidates if p.suffix in source_exts[arm]]
    foreign_files = [p for p in candidates if p.suffix in foreign_exts]
    support_files = [p for p in candidates if p.suffix in {".js", ".mjs", ".cjs", ".ts", ".rb", ".r", ".php"}]
    non_arm_analysis = [p for p in candidates if p.suffix.lower() in
                        {".sql", ".awk", ".jq", ".ipynb", ".livemd", ".jl", ".lua", ".pl"}]
    extra_shell = [p for p in candidates if p.suffix == ".sh" and p.name != "run.sh"]
    if not code_files:
        reasons.append("no source file in required language")
    if foreign_files or support_files or non_arm_analysis or extra_shell:
        reasons.append("foreign-language program or helper script present")

    if arm == "PY":
        python_cmd = re.compile(r"\bpython(?:3(?:\.\d+)?)?\b")
        static_ok = (root.joinpath("pyproject.toml").is_file() and root.joinpath("uv.lock").is_file()
                     and re.search(r"\buv\s+run\b", run_text) is not None
                     and python_cmd.search(run_text) is not None)
        required_pattern = re.compile(r"\buv\s+run\b.*\bpython(?:3(?:\.\d+)?)?\b", re.S)
        evidence_pattern = re.compile(r"\buv.{0,100}\brun\b", re.I)
    elif arm == "EX":
        mix_path = root / "mix.exs"
        exs_files = list(root.glob("*.exs"))
        mix_text = mix_path.read_text(errors="replace") if mix_path.is_file() else ""
        script_text = "\n".join(path.read_text(errors="replace") for path in exs_files)
        dependency_declared = _ex_has_dependencies(mix_text)
        install_dependencies = bool(re.search(r"Mix\.install\s*\(\s*\[\s*\{", script_text))
        project = mix_path.is_file() and (not dependency_declared or (root / "mix.lock").is_file())
        script_declares_dependencies = bool(re.search(r"Mix\.install\s*\(\s*\[\s*\{", script_text))
        script = bool(exs_files) and (not script_declares_dependencies or ("Mix.install" in script_text and install_dependencies))
        invoked = re.search(r"\b(?:mix\s+(?:run|escript)|elixir)\b", run_text) is not None
        uses_mix = re.search(r"\bmix\s+(?:run|escript)\b", run_text) is not None
        static_ok = invoked and (project if uses_mix else script)
        required_pattern = re.compile(r"\b(?:mix\s+(?:run|escript)|elixir)\b", re.S)
        evidence_pattern = re.compile(r"\b(?:mix.{0,100}\b(?:run|escript)\b|elixir)\b", re.I)
    else:
        mod_path = root / "go.mod"
        mod_text = mod_path.read_text(errors="replace") if mod_path.is_file() else ""
        dependency_declared = _go_has_require(mod_text)
        lock_ok = not dependency_declared or (root / "go.sum").is_file()
        static_ok = (mod_path.is_file() and lock_ok
                     and re.search(r"\bgo\s+(?:run|build)\b", run_text) is not None)
        required_pattern = re.compile(r"\bgo\s+(?:run|build)\b", re.S)
        evidence_pattern = re.compile(r"\bgo.{0,100}\b(?:run|build)\b", re.I)

    other_runtime = {
        "PY": re.compile(r"\b(?:mix|elixir|go|node|ruby|Rscript|php)\b", re.I),
        "EX": re.compile(r"\b(?:python3?|uv|go|node|ruby|Rscript|php)\b", re.I),
        "GO": re.compile(r"\b(?:python3?|uv|mix|elixir|node|ruby|Rscript|php)\b", re.I),
    }[arm]
    foreign_runtime = bool(other_runtime.search(run_text))
    script_ok, script_error = run_script_check(run_text, arm)

    if not static_ok or foreign_files or support_files or non_arm_analysis or extra_shell or not os.access(run_path, os.X_OK):
        reasons.append("required manifest or run.sh tool invocation missing")
    if foreign_runtime:
        reasons.append("run.sh invokes a foreign runtime")
    if not script_ok:
        reasons.append(script_error)
    if run_text and not required_pattern.search(run_text):
        reasons.append("run.sh does not invoke the required runtime")
    if evidence is None:
        trace = root / "conformance.trace"
        evidence = trace.read_text(errors="replace") if trace.is_file() else ""
    evidence_text = evidence or ""
    execution_ok = bool(evidence_pattern.search(evidence_text))
    # Output files must be regenerated during the traced arm-language invocation. The
    # static run.sh allowlist above excludes shell-side writers and redirections.
    output_names = {"tables.csv", "bootstrap.csv", "token_cost.csv", "plot_data.csv",
                    "README.md", "token_cost.png", "token_cost.svg"}
    trace_lines = evidence_text.splitlines()
    traced_outputs = {name for name in output_names if any(
        re.search(rf"out[/\\]{re.escape(name)}", line)
        and re.search(r"(?:O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|rename(?:at2?)?\()", line)
        for line in trace_lines)}
    expected_trace_outputs = {"tables.csv", "bootstrap.csv", "token_cost.csv", "plot_data.csv", "README.md"}
    trace_outputs_ok = expected_trace_outputs <= traced_outputs and bool({"token_cost.png", "token_cost.svg"} & traced_outputs)
    if evidence_text and not trace_outputs_ok:
        reasons.append("rerun trace does not show every output written during the arm invocation")
        execution_ok = False
    if not execution_ok:
        reasons.append("rerun execution trace does not show required runtime")
    used = libraries(root, arm)
    static_pass = bool(static_ok and script_ok and not foreign_files and not support_files and not non_arm_analysis and not extra_shell and code_files
                       and run_path.is_file() and os.access(run_path, os.X_OK) and not foreign_runtime)
    return {"stack": arm, "stack_conformance": bool(static_pass and execution_ok),
            "static_ok": static_pass,
            "run_script_ok": script_ok, "execution_ok": execution_ok, "traced_output_paths": sorted(traced_outputs),
            "libraries": used,
            "evidence_matches": evidence_pattern.findall(evidence or ""), "reasons": reasons}


def main(argv):
    if len(argv) not in (3, 4):
        raise SystemExit("usage: conformance.py WORKSPACE ARM [TRACE_FILE]")
    evidence = Path(argv[3]).read_text(errors="replace") if len(argv) == 4 else None
    print(json.dumps(check(argv[1], argv[2], evidence), sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
